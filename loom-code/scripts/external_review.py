#!/usr/bin/env python3
"""Execute one consented outside review with an explicit CLI profile.

This boundary does not judge the review: the owning skill validates its output.
It never substitutes a model, an effort, or an executor after failure.
"""
from __future__ import annotations

import argparse
import errno
import json
import math
import os
import re
import signal
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, Mapping, TextIO


EFFORTS = {"low", "medium", "high", "xhigh", "max"}
FAMILIES = {"openai", "anthropic", "google"}
PROBE_PROMPT = "Reply with the single word ok. Do not inspect files."
Runner = Callable[..., subprocess.CompletedProcess[str]]


def provider_family(model: str) -> str | None:
    name = model.lower()
    if name.startswith(("claude-", "anthropic/")) or name in {"opus", "sonnet", "haiku"}:
        return "anthropic"
    if name.startswith(("gemini-", "google/")):
        return "google"
    if name.startswith(("gpt-", "openai/", "o3", "o4")):
        return "openai"
    return None


def claude_model_matches(requested: str, observed: str) -> bool:
    """An alias may vary by version, but never by Opus/Sonnet/Haiku tier."""
    if requested in {"opus", "sonnet", "haiku"}:
        return bool(re.search(rf"(?:^|[-/]){requested}(?:[-/]|$)", observed.lower()))
    return observed == requested


def _authorization_valid(source: object, executor: str) -> bool:
    if not isinstance(source, Mapping):
        return False
    target = source.get("target")
    if not isinstance(target, str) or not target.strip():
        return False
    names = {"codex": r"(?<![A-Za-z])codex(?![A-Za-z])",
             "claude": r"(?<![A-Za-z])claude(?![A-Za-z])",
             "agy": r"(?<![A-Za-z])(?:agy|antigravity)(?![A-Za-z])"}
    if source.get("kind") == "direct-user-request":
        quote = source.get("quote")
        name = names.get(executor, r"$^")
        return (isinstance(quote, str) and bool(quote.strip())
                and source.get("selected_executor") == executor
                and bool(re.search(name, quote, re.IGNORECASE)))
    if source.get("kind") == "accepted-selection":
        selection = source.get("selection")
        return (isinstance(selection, str) and
                bool(re.fullmatch(names.get(executor, r"$^"), selection.strip(), re.IGNORECASE)))
    return False


def _consent_valid(record: Mapping[str, Any] | None, executor: str, scope: str,
                   model: str | None = None, effort: str | None = None,
                   family: str | None = None) -> bool:
    if not isinstance(record, Mapping):
        return False
    disclosures = record.get("disclosures")
    base = (
        record.get("approved") is True
        and _authorization_valid(record.get("authorization_source"), executor)
        and record.get("executor") == executor
        and record.get("review_root") == scope
        and isinstance(disclosures, Mapping)
        and all(disclosures.get(key) is True for key in
                ("cost", "vendor_egress", "local_execution",
                 "filesystem_access_outside_root", "filesystem_write_not_guaranteed"))
    )
    allowed_families = record.get("allowed_families")
    record_family = record.get("family")
    if record_family is not None and (
            not isinstance(record_family, str) or record_family not in FAMILIES):
        return False
    if allowed_families is not None:
        if (not isinstance(allowed_families, list) or not allowed_families
                or any(not isinstance(item, str) or item not in FAMILIES
                       for item in allowed_families)):
            return False
        if record_family is not None and record_family not in allowed_families:
            return False
    if not base or model is None or effort is None:
        return base
    if record_family is not None and record_family != family:
        return False
    exact = record.get("model") == model and record.get("effort") == effort
    family_allowed = (record_family == family if allowed_families is None
                      else family in allowed_families)
    if allowed_families is not None and not family_allowed:
        return False
    bounded = (record.get("selection_authorized") is True
               and family_allowed
               and isinstance(record.get("allowed_efforts"), list)
               and effort in record["allowed_efforts"])
    return exact or bounded


PROGRESS_INTERVAL = 60  # seconds between "still running" lines on stderr


def _duration(seconds: float) -> str:
    whole = max(int(seconds), 0)
    return f"{whole}s" if whole < 60 else f"{whole // 60}m{whole % 60:02d}s"


def _say(text: str) -> None:
    # Progress lines carry only step name, outcome and durations: never CLI
    # or packet text. stdout stays the single JSON result. They are
    # diagnostics: a closed or failing stderr never reaches stdout or the result.
    if sys.stderr is None:
        return
    try:
        print(f"external-review: {text}", file=sys.stderr, flush=True)
    except (OSError, ValueError):
        # Drop the failed stream: its unflushed line would otherwise fail
        # again at interpreter exit and turn the exit code into 120.
        sys.stderr = None


def _launch(argv: list[str], *, input: str, timeout: int, cwd: str,
            until_response_id: int | None = None, progress: str | None = None,
            **_: Any):
    """Run argv bounded by timeout, killing its whole process group.

    Without until_response_id, stdin is closed after input and output is
    collected until the process exits; a descendant still holding a pipe is
    given a short grace, then killed. With until_response_id, stdin stays
    open and reading stops at the JSON line carrying that id, or once the
    process exits without it (the same grace applies). With progress (a step
    name), a line goes to stderr every PROGRESS_INTERVAL seconds while the
    step runs, and one closing line when it ends.
    """
    if not Path(cwd).is_dir():
        raise FileNotFoundError(errno.ENOENT, "missing review root", cwd)
    proc = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE, text=True, cwd=cwd,
                            start_new_session=True)
    start = time.monotonic()
    out: list[str] = []
    err: list[str] = []
    stamps: list[float] = []  # arrival time of each complete output line
    answered = threading.Event()

    def read_out() -> None:
        for line in proc.stdout:
            stamps.append(time.monotonic())
            out.append(line)
            if until_response_id is None:
                continue
            try:
                if json.loads(line).get("id") == until_response_id:
                    answered.set()
                    return
            except (json.JSONDecodeError, AttributeError):
                continue

    def read_err() -> None:
        for line in proc.stderr:
            stamps.append(time.monotonic())
            err.append(line)

    def close_line(outcome: str, end: float) -> None:
        marks = [start, *sorted(t for t in stamps if t <= end), end]
        silence = max(b - a for a, b in zip(marks, marks[1:]))
        _say(f"{progress} {outcome} after {_duration(end - start)}"
             f" · longest silence {_duration(silence)}")

    def write_in() -> None:
        # A child that never reads blocks this write once input exceeds the
        # pipe buffer, so it runs off the main thread, inside the deadline.
        try:
            proc.stdin.write(input)
            proc.stdin.flush()
            if until_response_id is None:
                proc.stdin.close()
        except (OSError, ValueError):
            pass

    readers = [threading.Thread(target=read_out, daemon=True),
               threading.Thread(target=read_err, daemon=True)]
    writer = threading.Thread(target=write_in, daemon=True)
    try:
        for reader in readers:
            reader.start()
        writer.start()
        if until_response_id is None and progress is not None:
            deadline = start + timeout
            while True:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    close_line("timed out", time.monotonic())
                    raise subprocess.TimeoutExpired(argv, timeout)
                try:
                    proc.wait(min(remaining, PROGRESS_INTERVAL))
                    break
                except subprocess.TimeoutExpired:
                    now = time.monotonic()
                    if now >= deadline:
                        continue
                    last = (f"last output {_duration(now - stamps[-1])} ago"
                            if stamps else "no output yet")
                    _say(f"{progress} still running · {_duration(now - start)}"
                         f" elapsed · {last}")
            end = time.monotonic()
            for reader in readers:
                reader.join(1)  # grace for a descendant still holding a pipe
            close_line(f"exited {proc.returncode}", end)
        elif until_response_id is None:
            try:
                proc.wait(timeout)
            except subprocess.TimeoutExpired:
                raise subprocess.TimeoutExpired(argv, timeout) from None
            for reader in readers:
                reader.join(1)  # grace for a descendant still holding a pipe
        else:
            # Wait for the reply or the direct process's exit, whichever is
            # first; a descendant holding stdout must not turn exit into timeout.
            deadline = time.monotonic() + timeout
            while readers[0].is_alive():
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(argv, timeout)
                if proc.poll() is not None:
                    readers[0].join(1)  # same grace as the branch above
                    break
                readers[0].join(min(remaining, 0.05))
    finally:
        try:
            os.killpg(proc.pid, signal.SIGKILL)
        except (ProcessLookupError, PermissionError):
            pass
        proc.wait()
        for thread in (*readers, writer):
            if thread.ident is not None:
                thread.join(1)
        # Never close a stream under a still-blocked reader or writer.
        streams = [s for s, t in zip((proc.stdin, proc.stdout, proc.stderr),
                                     (writer, *readers)) if not t.is_alive()]
        for stream in streams:
            try:
                stream.close()
            except OSError:
                pass
    returncode = 0 if answered.is_set() else proc.returncode
    return subprocess.CompletedProcess(argv, returncode, "".join(out), "".join(err))


def _run(runner: Runner, argv: list[str], prompt: str, timeout: int, scope: str,
         **kwargs: Any):
    return runner(argv, input=prompt, capture_output=True, text=True,
                  timeout=timeout, check=False, cwd=scope, **kwargs)


CODEX_DISCOVERY_TIMEOUT = 15
AGY_DISCOVERY_TIMEOUT = 15


def _codex_candidates(runner: Runner, scope: str) -> list[str]:
    requests = (
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"clientInfo": {"name": "loom-external-review", "title": "Loom External Review", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "model/list", "params": {}},
    )
    payload = "".join(json.dumps(item) + "\n" for item in requests)
    # app-server exits on stdin EOF before answering, so stdin stays open
    # until the model/list (id 2) reply arrives.
    response = _run(runner, ["codex", "app-server"], payload,
                    CODEX_DISCOVERY_TIMEOUT, scope, until_response_id=2)
    if response.returncode != 0:
        raise ValueError(f"codex model/list failed: exit {response.returncode}")
    for line in response.stdout.splitlines():
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(message, dict):
            continue
        if message.get("id") != 2:
            continue
        if "error" in message:
            error = message["error"]
            detail = error.get("message") if isinstance(error, dict) else None
            detail = "not initialized" if detail == "not initialized" else "unknown error"
            raise ValueError(f"codex model/list error: {detail}")
        result = message.get("result")
        rows = result.get("data") if isinstance(result, dict) else None
        if not isinstance(rows, list):
            raise ValueError("codex model/list result missing data array")
        return [row["id"] for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)]
    raise ValueError(f"codex model/list failed: exit {response.returncode}")


def _agy_candidates(runner: Runner, scope: str) -> list[str]:
    response = _run(runner, ["agy", "models"], "", AGY_DISCOVERY_TIMEOUT, scope)
    if response.returncode != 0:
        raise ValueError("agy models failed")
    try:
        parsed = json.loads(response.stdout)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, list):
        return [item if isinstance(item, str) else item.get("id") for item in parsed
                if isinstance(item, str) or isinstance(item, dict) and isinstance(item.get("id"), str)]
    # Agy's human-readable list may contain descriptions; only take its first
    # slug column, and require a recognizable provider family.
    return [line.split()[0] for line in response.stdout.splitlines()
            if line.split() and provider_family(line.split()[0])]


_DISCOVERY_REASONS = {"codex model/list error: not initialized",
                      "codex model/list error: unknown error",
                      "codex model/list result missing data array",
                      "agy models failed"}


def _is_discovery_reason(text: str) -> bool:
    """Whether text is a known discovery failure reason safe to report verbatim."""
    return text in _DISCOVERY_REASONS or bool(
        re.fullmatch(r"codex model/list failed: exit -?\d+", text))


def discover(executor: str, scope: str, consent: Mapping[str, Any] | None,
             *, runner: Runner = _launch) -> dict[str, Any]:
    """List observed candidates after scope and egress consent, before pair approval."""
    result: dict[str, Any] = {"status": "failed", "reason": None,
                              "executor": executor, "candidates": []}
    if not _consent_valid(consent, executor, scope):
        result["reason"] = "consent-missing-or-stale"
        return result
    if not Path(scope).is_absolute():
        result["reason"] = "scope-must-be-absolute"
        return result
    try:
        if executor == "codex":
            models = _codex_candidates(runner, scope)
            result["source"] = "model/list"
        elif executor == "agy":
            models = _agy_candidates(runner, scope)
            result["source"] = "agy models"
        elif executor == "claude":
            if not Path(scope).is_dir():
                result["reason"] = "discovery-error: review-root-not-found"
                return result
            models = ["opus", "sonnet", "haiku"]
            result["source"] = "documented aliases; explicit IDs also accepted"
        else:
            raise ValueError("unknown executor")
    except subprocess.TimeoutExpired as exc:
        result["reason"] = f"discovery-timeout: {exc.timeout}s"
        return result
    except FileNotFoundError as exc:
        missing_root = exc.filename == scope or not Path(scope).is_dir()
        category = "review-root-not-found" if missing_root else "executor-not-installed"
        result["reason"] = f"discovery-error: {category}"
        return result
    except (OSError, ValueError, TypeError, KeyError) as exc:
        detail = str(exc) if isinstance(exc, ValueError) and (
            _is_discovery_reason(str(exc)) or str(exc) == "unknown executor"
        ) else "unknown error"
        result["reason"] = f"discovery-error: {detail}"
        return result
    result["status"] = "completed"
    result["candidates"] = models
    return result


def _codex_observation(output: str, model: str, effort: str) -> tuple[str | None, str | None]:
    observed_models = re.findall(r"(?m)^model:\s*(\S+)\s*$", output)
    observed_efforts = re.findall(r"(?m)^reasoning effort:\s*(\S+)\s*$", output)
    found_model = observed_models[0] if len(observed_models) == 1 else None
    found_effort = observed_efforts[0] if len(observed_efforts) == 1 else None
    if found_model != model or found_effort != effort:
        raise ValueError("codex observable model/effort mismatch or missing")
    return found_model, found_effort


def _claude_observation(output: str, model: str, family: str) -> tuple[str, str]:
    try:
        data = json.loads(output)
    except json.JSONDecodeError as exc:
        raise ValueError("claude JSON result missing") from exc
    if not isinstance(data, dict):
        raise ValueError("claude JSON result is not an object")
    if data.get("is_error") is True:
        raise ValueError("claude result reports error")
    usage = data.get("modelUsage")
    if not isinstance(usage, dict) or not usage:
        raise ValueError("claude modelUsage missing")
    names = list(usage)
    if any(provider_family(name) != family for name in names):
        raise ValueError("claude observed provider family mismatch")
    if any(not claude_model_matches(model, name) for name in names):
        raise ValueError("claude observed model mismatch")
    result = data.get("result")
    if not isinstance(result, str) or not result.strip():
        raise ValueError("claude result empty")
    return names[0], result


def _stderr_failure_reason(executor: str, stderr: str) -> str:
    line = stderr.strip().splitlines()[0].lower() if stderr.strip() else ""
    line = re.sub(r"^error:\s*", "", line)
    if re.match(r"unsupported effort\b", line):
        return "unsupported effort"
    if re.match(r"(?:authentication (?:required|failed)|not logged in|unauthorized)\b", line):
        return "authentication error"
    if line.startswith(("you've hit your session limit", "session limit reached")):
        return "Claude session limit" if executor == "claude" else "session limit"
    return "unknown error"


def _execution_failure_reason(executor: str, output: str, stderr: str) -> str:
    if executor != "claude":
        return _stderr_failure_reason(executor, stderr)
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return _stderr_failure_reason(executor, stderr)
    if (not isinstance(data, dict) or data.get("type") != "result"
            or data.get("is_error") is not True):
        return _stderr_failure_reason(executor, stderr)
    if data.get("terminal_reason") == "rapid_refill_breaker":
        return "rapid-refill-breaker"
    if data.get("terminal_reason") != "api_error":
        return _stderr_failure_reason(executor, stderr)
    status = data.get("api_error_status")
    if type(status) is not int or not 400 <= status <= 599:
        return _stderr_failure_reason(executor, stderr)
    message = data.get("result")
    if status == 429 and isinstance(message, str) and "session limit" in message.lower():
        return "Claude session limit (HTTP 429)"
    return f"Claude API HTTP {status}"


def _claude_failure_action(reason: str) -> str:
    if "unknown error" in reason:
        return ("Run claude doctor locally; inspect CLI diagnostics privately, "
                "then request a new authorized review.")
    if "authentication error" in reason:
        return "Sign in to Claude locally, then request a new authorized review."
    if "session limit" in reason:
        return "Wait for the Claude session limit to reset, then request a new authorized review."
    if "unsupported effort" in reason:
        return "Select a supported Claude effort, then request a new authorized review."
    if "executor-not-installed" in reason:
        return "Install Claude CLI locally, then request a new authorized review."
    if "review-root-not-found" in reason:
        return "Restore the review root, then request a new authorized review."
    if reason.startswith("execution-timeout"):
        return "Check Claude CLI health and timeout settings locally, then request a new authorized review."
    if "Claude API HTTP" in reason:
        return "Check Claude API status locally, then request a new authorized review."
    return "Inspect Claude CLI diagnostics privately, then request a new authorized review."


def _command(executor: str, model: str, effort: str, prompt: str,
             scope: str, max_budget_usd: float | None = None) -> list[str]:
    if executor == "codex":
        return ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check",
                "--ephemeral", "-m", model, "-c", f"model_reasoning_effort={effort}", "-"]
    if executor == "claude":
        # CLI flag contract: https://code.claude.com/docs/en/cli-reference
        # Profile verified with Claude Code 2.1.310; recheck after CLI upgrades.
        command = ["claude", "-p", "--model", model, "--effort", effort,
                "--safe-mode", "--restricted", "--autocompact", "auto",
                "--strict-mcp-config", "--tools", "Read,Glob,Grep",
                "--permission-prompts", "none", "--output-format", "json",
                "--no-session-persistence"]
        if max_budget_usd is not None:
            command.extend(("--max-budget-usd", str(max_budget_usd)))
        return command
    return ["agy", "--add-dir", scope, "-p", prompt,
            "--model", model, "--effort", effort,
            "--mode", "plan", "--sandbox", "--disable-slash-commands",
            "--output-format", "text"]


def execute(
    executor: str, model: str, effort: str, family: str, scope: str,
    prompt: str, consent: Mapping[str, Any] | None, *,
    runner: Runner = _launch, probe_timeout: int = 45,
    review_timeout: int = 1800, max_budget_usd: float | None = None,
) -> dict[str, Any]:
    """Return provenance and raw review text; never infer a reviewer verdict."""
    result: dict[str, Any] = {
        "status": "failed", "reason": None, "executor": executor, "requested_model": model,
        "requested_effort": effort, "requested_family": family,
        "observed_model": None, "observed_effort": None,
        "evidence_level": "none", "review_output": None,
        "filesystem_boundary": (
            "Claude model file tools confined to review root; CLI startup writes outside root not excluded"
            if executor == "claude" else
            "working-root-only; outside-root reads and CLI writes not excluded"),
    }

    def fail(reason: str, diagnostic: dict[str, Any] | None = None) -> dict[str, Any]:
        if "probe" in result:
            result["probe"].pop("stdout", None)
            result["probe"].pop("stderr", None)
        if executor == "claude":
            result["observed_model"] = None
            result["evidence_level"] = "none"
        result["reason"] = reason
        if executor == "claude" and reason.startswith(("probe-", "review-", "execution-")):
            result["next_action"] = _claude_failure_action(reason)
            if diagnostic is not None:
                result["diagnostic"] = diagnostic
        return result

    if not _consent_valid(consent, executor, scope, model, effort, family):
        return fail("consent-missing-or-stale")
    if not Path(scope).is_absolute():
        return fail("scope-must-be-absolute")
    if (executor not in {"codex", "claude", "agy"} or not model or
            effort not in EFFORTS or family not in FAMILIES or
            not 0 < probe_timeout <= 120 or
            not probe_timeout < review_timeout <= 1800 or
            (max_budget_usd is not None and
             (executor != "claude" or isinstance(max_budget_usd, bool)
              or not isinstance(max_budget_usd, (int, float))
              or not math.isfinite(max_budget_usd) or max_budget_usd <= 0))):
        return fail("invalid-explicit-profile")
    if provider_family(model) != family:
        return fail("selected-provider-family-mismatch-or-unknown")

    try:
        if executor == "codex":
            candidates = _codex_candidates(runner, scope)
        elif executor == "agy":
            candidates = _agy_candidates(runner, scope)
        else:
            # Claude exposes aliases and explicit IDs, but no documented
            # machine-readable model list. Its bounded run tests acceptance.
            candidates = [model]
        if model not in candidates:
            return fail("selected-model-not-in-current-candidates")
        result["candidate_source"] = {"codex": "model/list", "agy": "agy models",
                                      "claude": "alias-or-explicit-id"}[executor]
        for stage, text, timeout in (("probe", PROBE_PROMPT, probe_timeout),
                                     ("review", prompt, review_timeout)):
            argv = _command(executor, model, effort, text, scope, max_budget_usd)
            response = _run(runner, argv, "" if executor == "agy" else text,
                            timeout, scope, progress=stage)
            if stage == "probe":
                result["probe"] = {
                    "returncode": response.returncode,
                    "timeout_seconds": timeout,
                }
                if response.returncode == 0:
                    result["probe"].update(stdout=response.stdout,
                                           stderr=response.stderr)
            if (executor == "claude" and
                    _execution_failure_reason(executor, response.stdout,
                                              response.stderr) == "rapid-refill-breaker"):
                return fail(f"{stage}-rapid-refill-breaker")
            if response.returncode != 0:
                detail = _execution_failure_reason(executor, response.stdout,
                                                   response.stderr)
                diagnostic = None
                if executor == "claude" and detail == "unknown error":
                    try:
                        json.loads(response.stdout)
                        parseable = True
                    except (json.JSONDecodeError, TypeError):
                        parseable = False
                    diagnostic = {"stage": stage, "exit_code": response.returncode,
                                  "stdout_present": bool(response.stdout),
                                  "stderr_present": bool(response.stderr),
                                  "stdout_json_parseable": parseable}
                return fail(f"{stage}-exit-{response.returncode}: {detail}", diagnostic)
            if executor == "codex":
                observed_model, observed_effort = _codex_observation(
                    response.stderr, model, effort)
                result["observed_model"] = observed_model
                result["observed_effort"] = observed_effort
                result["evidence_level"] = "observed-model-and-effort"
                body = response.stdout
            elif executor == "claude":
                observed_model, body = _claude_observation(response.stdout, model, family)
                result["observed_model"] = observed_model
                result["evidence_level"] = "accepted-explicit-settings"
            else:
                if not response.stdout.strip():
                    return fail(f"{stage}-empty-output")
                result["evidence_level"] = "accepted-explicit-settings"
                body = response.stdout
            if not body.strip():
                return fail(f"{stage}-empty-output")
            if stage == "review":
                result["review_output"] = body
    except subprocess.TimeoutExpired as exc:
        return fail(f"execution-timeout: {exc.timeout}s")
    except FileNotFoundError as exc:
        missing_root = exc.filename == scope or not Path(scope).is_dir()
        category = "review-root-not-found" if missing_root else "executor-not-installed"
        return fail(f"execution-error: {category}")
    except (OSError, ValueError, TypeError, KeyError) as exc:
        known = {"codex observable model/effort mismatch or missing",
                 "claude JSON result missing", "claude JSON result is not an object",
                 "claude result reports error",
                 "claude modelUsage missing", "claude observed provider family mismatch",
                 "claude observed model mismatch", "claude result empty"}
        detail = str(exc) if isinstance(exc, ValueError) and (
            str(exc) in known or _is_discovery_reason(str(exc))
        ) else "unknown error"
        return fail(f"execution-error: {detail}")
    result["status"] = "completed"
    return result


def main(argv: list[str] | None = None, *, stdin: TextIO = sys.stdin,
         out: TextIO = sys.stdout) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list-candidates", action="store_true")
    parser.add_argument("--executor", required=True, choices=("codex", "claude", "agy"))
    parser.add_argument("--model")
    parser.add_argument("--effort")
    parser.add_argument("--family")
    parser.add_argument("--scope", required=True)
    parser.add_argument("--consent-record", required=True, type=Path)
    parser.add_argument("--probe-timeout-seconds", type=int, default=45)
    parser.add_argument("--review-timeout-seconds", type=int, default=1800)
    parser.add_argument("--max-budget-usd", type=float)
    args = parser.parse_args(argv)
    try:
        consent = json.loads(args.consent_record.read_text())
    except (OSError, json.JSONDecodeError):
        consent = None
    if args.list_candidates:
        result = discover(args.executor, args.scope, consent)
    elif not all((args.model, args.effort, args.family)):
        result = {"status": "failed", "reason": "explicit-model-effort-family-required"}
    else:
        result = execute(args.executor, args.model, args.effort, args.family,
                         args.scope, stdin.read(), consent,
                         probe_timeout=args.probe_timeout_seconds,
                         review_timeout=args.review_timeout_seconds,
                         max_budget_usd=args.max_budget_usd)
    print(json.dumps(result, ensure_ascii=False), file=out)
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
