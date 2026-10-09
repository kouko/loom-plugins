#!/usr/bin/env python3
"""Execute one consented outside review with an explicit CLI profile.

This boundary does not judge the review: the owning skill validates its output.
It never substitutes a model, an effort, or an executor after failure.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
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
        return (isinstance(quote, str) and bool(quote.strip()) and
                bool(re.search(names.get(executor, r"$^"), quote, re.IGNORECASE)))
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


def _run(runner: Runner, argv: list[str], prompt: str, timeout: int, scope: str):
    return runner(argv, input=prompt, capture_output=True, text=True,
                  timeout=timeout, check=False, cwd=scope)


def _codex_candidates(runner: Runner, scope: str) -> list[str]:
    requests = (
        {"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {"clientInfo": {"name": "loom-external-review", "title": "Loom External Review", "version": "1"}}},
        {"jsonrpc": "2.0", "method": "initialized"},
        {"jsonrpc": "2.0", "id": 2, "method": "model/list", "params": {}},
    )
    response = _run(runner, ["codex", "app-server"],
                    "".join(json.dumps(item) + "\n" for item in requests), 15, scope)
    if response.returncode != 0:
        raise ValueError("codex model/list failed")
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
            detail = error.get("message") if isinstance(error, dict) else str(error)
            raise ValueError(f"codex model/list error: {detail}")
        result = message.get("result")
        rows = result.get("data") if isinstance(result, dict) else None
        if not isinstance(rows, list):
            raise ValueError("codex model/list result missing data array")
        return [row["id"] for row in rows if isinstance(row, dict) and isinstance(row.get("id"), str)]
    raise ValueError("codex model/list response missing")


def _agy_candidates(runner: Runner, scope: str) -> list[str]:
    response = _run(runner, ["agy", "models"], "", 15, scope)
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


def discover(executor: str, scope: str, consent: Mapping[str, Any] | None,
             *, runner: Runner = subprocess.run) -> dict[str, Any]:
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
            models = ["opus", "sonnet", "haiku"]
            result["source"] = "documented aliases; explicit IDs also accepted"
        else:
            raise ValueError("unknown executor")
    except subprocess.TimeoutExpired as exc:
        result["reason"] = f"discovery-timeout: {exc.timeout}s"
        return result
    except (OSError, ValueError, TypeError, KeyError) as exc:
        result["reason"] = f"discovery-error: {exc}"
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


def _execution_failure_reason(executor: str, output: str, stderr: str) -> str:
    if executor != "claude":
        return stderr.strip()[:300] or "unknown error"
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return "unknown error"
    if (not isinstance(data, dict) or data.get("type") != "result"
            or data.get("is_error") is not True
            or data.get("terminal_reason") != "api_error"):
        return "unknown error"
    status = data.get("api_error_status")
    if type(status) is not int or not 400 <= status <= 599:
        return "unknown error"
    message = data.get("result")
    if status == 429 and isinstance(message, str) and "session limit" in message.lower():
        return "Claude session limit (HTTP 429)"
    return f"Claude API HTTP {status}"


def _command(executor: str, model: str, effort: str, prompt: str,
             scope: str) -> list[str]:
    if executor == "codex":
        return ["codex", "exec", "--sandbox", "read-only", "--skip-git-repo-check",
                "--ephemeral", "-m", model, "-c", f"model_reasoning_effort={effort}", "-"]
    if executor == "claude":
        return ["claude", "-p", "--model", model, "--effort", effort,
                "--permission-mode", "plan", "--tools", "Read,Glob,Grep",
                "--permission-prompts", "none", "--output-format", "json",
                "--no-session-persistence"]
    return ["agy", "--add-dir", scope, "-p", prompt,
            "--model", model, "--effort", effort,
            "--mode", "plan", "--sandbox", "--disable-slash-commands",
            "--output-format", "text"]


def execute(
    executor: str, model: str, effort: str, family: str, scope: str,
    prompt: str, consent: Mapping[str, Any] | None, *,
    runner: Runner = subprocess.run, probe_timeout: int = 45,
    review_timeout: int = 600,
) -> dict[str, Any]:
    """Return provenance and raw review text; never infer a reviewer verdict."""
    result: dict[str, Any] = {
        "status": "failed", "reason": None, "executor": executor, "requested_model": model,
        "requested_effort": effort, "requested_family": family,
        "observed_model": None, "observed_effort": None,
        "evidence_level": "none", "review_output": None,
        "filesystem_boundary": "working-root-only; outside-root reads and CLI writes not excluded",
    }

    def fail(reason: str) -> dict[str, Any]:
        result["reason"] = reason
        return result

    if not _consent_valid(consent, executor, scope, model, effort, family):
        return fail("consent-missing-or-stale")
    if not Path(scope).is_absolute():
        return fail("scope-must-be-absolute")
    if (executor not in {"codex", "claude", "agy"} or not model or
            effort not in EFFORTS or family not in FAMILIES or
            not 0 < probe_timeout <= 120 or
            not probe_timeout < review_timeout <= 1800):
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
            argv = _command(executor, model, effort, text, scope)
            response = _run(runner, argv, "" if executor == "agy" else text,
                            timeout, scope)
            if stage == "probe":
                result["probe"] = {
                    "returncode": response.returncode,
                    "timeout_seconds": timeout,
                }
                if response.returncode == 0:
                    result["probe"].update(stdout=response.stdout,
                                           stderr=response.stderr)
            if response.returncode != 0:
                detail = _execution_failure_reason(executor, response.stdout,
                                                   response.stderr)
                return fail(f"{stage}-exit-{response.returncode}: {detail}")
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
    except (OSError, ValueError, TypeError, KeyError) as exc:
        return fail(f"execution-error: {exc}")
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
    parser.add_argument("--review-timeout-seconds", type=int, default=600)
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
                         review_timeout=args.review_timeout_seconds)
    print(json.dumps(result, ensure_ascii=False), file=out)
    return 0 if result["status"] == "completed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
