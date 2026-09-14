#!/usr/bin/env python3
"""Antigravity CLI (agy) hook adapter for loom-code.

agy runs plugin hooks from ``<plugin-root>/hooks.json`` via ``sh -c`` with
cwd = the plugin root, camelCase JSON on stdin and one JSON object expected
on stdout. It has no SessionStart and its PostToolUse cannot inject, so this
adapter maps agy events onto the handlers Claude Code and Codex already use:

    push-gate       PreToolUse(run_command) -> scripts/loom_checker.py push --hook
    pre-invocation  PreInvocation           -> hooks/session-start (first turn only)
                                               + language-anchor on a loom SKILL.md read

Exit status is always 0; decisions travel in the JSON. The push gate fails
closed: when the checker is missing or cannot answer, only a closed set of
read-only commands is allowed (the same set as the Codex stale-root fallback).
"""
from __future__ import annotations

import importlib.util
import json
import os
import re
import shlex
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
CHECKER = PLUGIN_ROOT / "scripts" / "loom_checker.py"
SESSION_START = PLUGIN_ROOT / "hooks" / "session-start"
LANGUAGE_ANCHOR = PLUGIN_ROOT / "hooks" / "language-anchor.py"
LOOM_PLUGIN_SEGMENTS = ("/loom-code/", "/loom-design/", "/loom-workflow/")
USER_REQUEST_RE = re.compile(r"<USER_REQUEST>(.*?)</USER_REQUEST>", re.DOTALL)


def _emit(obj: dict) -> int:
    print(json.dumps(obj, ensure_ascii=False))
    return 0


# --- push gate ---------------------------------------------------------------

def _options_ok(args, exact, prefixes=()):
    return all(
        not t.startswith("-") or t == "--" or t in exact or any(t.startswith(p) for p in prefixes)
        for t in args
    )


def _closed_read_only(command: str) -> bool:
    """The Codex stale-root fallback's read-only set, ported verbatim in logic."""
    try:
        tokens = shlex.split(command)
    except ValueError:
        return False
    if not tokens or any(ch in command for ch in "\n;&|<>$`()") or "/" in tokens[0]:
        return False
    name = tokens[0]
    if name == "git":
        index = 3 if len(tokens) > 2 and tokens[1] == "-C" and not tokens[2].startswith("-") else 1
        if len(tokens) <= index:
            return False
        sub, args = tokens[index], tokens[index + 1:]
        common = {"--stat", "--shortstat", "--name-only", "--name-status", "--oneline", "--no-patch",
                  "--patch", "-p", "--decorate", "--no-decorate", "--all", "--first-parent",
                  "--reverse", "--check", "--cached", "--staged", "--quiet", "--exit-code", "--"}
        prefixes = ("--max-count=", "--format=", "--pretty=", "--since=", "--until=", "--author=",
                    "--grep=", "--date=", "--diff-filter=")
        if sub == "status":
            return _options_ok(
                args,
                {"-s", "--short", "-b", "--branch", "--porcelain", "--show-stash", "--ahead-behind",
                 "--no-ahead-behind", "-z", "--ignored", "--no-renames", "--"},
                ("--porcelain=", "--untracked-files=", "--ignored=", "--find-renames="),
            )
        if sub in {"log", "show", "diff"}:
            return all(
                not a.startswith("-") or a in common or re.fullmatch(r"-[0-9]+", a)
                or any(a.startswith(p) for p in prefixes)
                for a in args
            )
        if sub == "branch":
            return all(not a.startswith("-") or a in {"--list", "--"} for a in args)
        return False
    if name == "cat":
        return all(a == "--" or not a.startswith("-") or re.fullmatch(r"-[benstuv]+", a) for a in tokens[1:])
    if name == "ls":
        return all(a == "--" or not a.startswith("-") or re.fullmatch(r"-[AabdFfGghiklmnopqrstuwx1@%]+", a)
                   for a in tokens[1:])
    if name == "rg":
        return _options_ok(
            tokens[1:],
            {"-n", "--line-number", "-l", "--files-with-matches", "--files", "--hidden", "-S",
             "--smart-case", "-i", "--ignore-case", "-F", "--fixed-strings", "--no-heading", "--"},
            ("--glob=", "--type=", "--color="),
        )
    if name == "find":
        values = {"-maxdepth", "-mindepth", "-type", "-name", "-iname", "-path", "-ipath"}
        flags = {"-print", "-xdev", "-depth", "-L", "-H", "-P", "!"}
        i = 1
        while i < len(tokens):
            token = tokens[i]
            if token in values:
                i += 1
                if i >= len(tokens):
                    return False
            elif token.startswith("-") and token not in flags:
                return False
            i += 1
        return True
    return False


def _command_cwd(args: dict, payload: dict) -> str:
    workspaces = payload.get("workspacePaths") or []
    base = workspaces[0] if workspaces and isinstance(workspaces[0], str) else os.getcwd()
    cwd = args.get("Cwd")
    if not isinstance(cwd, str) or not cwd:
        return base
    return cwd if os.path.isabs(cwd) else os.path.normpath(os.path.join(base, cwd))


def push_gate(payload: dict) -> int:
    args = ((payload.get("toolCall") or {}).get("args") or {})
    command = args.get("CommandLine")
    if not isinstance(command, str) or not command.strip():
        return _emit({"decision": "deny",
                      "reason": "BLOCK push.attestation: run_command payload carries no CommandLine"})
    claude_payload = {
        "hook_event_name": "PreToolUse",
        "tool_name": "Bash",
        "tool_input": {"command": command},
        "cwd": _command_cwd(args, payload),
    }
    rc, reason = None, ""
    if CHECKER.is_file():
        try:
            result = subprocess.run(
                [sys.executable, str(CHECKER), "push", "--hook"],
                input=json.dumps(claude_payload), capture_output=True, text=True,
                cwd=str(PLUGIN_ROOT), timeout=25,
            )
            rc, reason = result.returncode, result.stderr.strip()
        except (OSError, subprocess.SubprocessError):
            rc = None
    if rc == 0:
        return _emit({"decision": "allow"})
    if rc == 2:
        return _emit({"decision": "deny", "reason": reason or "BLOCK push.attestation: checker refused"})
    if _closed_read_only(command):
        return _emit({"decision": "allow"})
    return _emit({"decision": "deny", "reason": (
        f"BLOCK push.attestation: loom checker unavailable at {CHECKER}; "
        "reinstall the loom-code plugin (agy plugin install) before running this command"
    )})


# --- pre-invocation ------------------------------------------------------------

def _session_context(payload: dict) -> str:
    workspaces = payload.get("workspacePaths") or []
    cwd = workspaces[0] if workspaces and isinstance(workspaces[0], str) and os.path.isdir(workspaces[0]) else None
    try:
        result = subprocess.run(["bash", str(SESSION_START)], stdin=subprocess.DEVNULL,
                                capture_output=True, text=True, cwd=cwd, timeout=10)
        data = json.loads(result.stdout)
    except (OSError, subprocess.SubprocessError, ValueError):
        return ""
    text = (data.get("hookSpecificOutput") or {}).get("additionalContext") or data.get("additionalContext")
    return text if isinstance(text, str) else ""


def _state_file(kind: str, payload: dict) -> Path:
    conversation = str(payload.get("conversationId") or os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
                       or payload.get("transcriptPath") or "unknown")
    return Path(tempfile.gettempdir()) / kind / re.sub(r"[^A-Za-z0-9_.-]", "_", conversation)


def _first_turn_session_context(payload: dict) -> str:
    """agy resets invocationNum to 0 on every user turn, so the first turn is
    invocationNum 0 with at most one prior step; a per-conversation marker
    keeps a resumed or compacted conversation from being re-injected."""
    initial_steps = payload.get("initialNumSteps", 0)
    if payload.get("invocationNum") != 0 or not isinstance(initial_steps, int) or initial_steps > 1:
        return ""
    marker = _state_file("loom-code-agy-session", payload)
    if marker.is_file():
        return ""
    text = _session_context(payload)
    if text:
        try:
            marker.parent.mkdir(parents=True, exist_ok=True)
            marker.write_text("injected", encoding="utf-8")
        except OSError:
            pass
    return text


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_steps(path: str) -> list[dict]:
    steps = []
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            try:
                step = json.loads(line)
            except ValueError:
                continue
            if isinstance(step, dict):
                steps.append(step)
    return steps


def _reads_loom_skill(step: dict) -> bool:
    for call in step.get("tool_calls") or []:
        if not isinstance(call, dict) or call.get("name") != "view_file":
            continue
        path = str((call.get("args") or {}).get("AbsolutePath", ""))
        if path.endswith("/SKILL.md") and any(seg in path for seg in LOOM_PLUGIN_SEGMENTS):
            return True
    return False


def _language_anchor(payload: dict) -> str:
    transcript = payload.get("transcriptPath")
    if not isinstance(transcript, str) or not transcript:
        return ""
    try:
        steps = _read_steps(transcript)
    except OSError:
        return ""
    model_steps = [(i, s) for i, s in enumerate(steps) if s.get("source") == "MODEL"]
    if not model_steps or not _reads_loom_skill(model_steps[-1][1]):
        return ""
    line_no, step = model_steps[-1]
    step_key = str(step.get("step_index", f"line{line_no}"))

    anchor = _load_module("loom_language_anchor", LANGUAGE_ANCHOR)
    lang_detect = anchor._load_lang_detect()
    texts = []
    for s in steps:
        if s.get("type") != "USER_INPUT":
            continue
        content = lang_detect.extract_text(s.get("content"))
        requests = USER_REQUEST_RE.findall(content)
        texts.extend(requests if requests else [content])
    text = anchor._ANCHOR_TEXT.get(lang_detect.majority_language(texts))
    if not text:
        return ""

    # One anchor per skill-read step: agy may call the model more than once
    # before a new MODEL step lands in the transcript.
    state = _state_file("loom-code-agy-anchor", payload)
    try:
        if state.is_file() and state.read_text(encoding="utf-8") == step_key:
            return ""
        state.parent.mkdir(parents=True, exist_ok=True)
        state.write_text(step_key, encoding="utf-8")
    except OSError:
        pass
    return text


def pre_invocation(payload: dict) -> int:
    messages = [_first_turn_session_context(payload), _language_anchor(payload)]
    steps = [{"ephemeralMessage": m} for m in messages if m]
    return _emit({"injectSteps": steps} if steps else {})


def main(argv: list[str]) -> int:
    mode = argv[0] if argv else ""
    try:
        payload = json.loads(sys.stdin.read())
        if not isinstance(payload, dict):
            raise ValueError("payload is not an object")
        if mode == "push-gate":
            return push_gate(payload)
        if mode == "pre-invocation":
            return pre_invocation(payload)
    except Exception as exc:  # never crash the agent loop; the gate still fails closed
        if mode == "push-gate":
            return _emit({"decision": "deny", "reason": f"BLOCK push.attestation: agy adapter error: {exc}"})
        return _emit({})
    return _emit({"decision": "deny", "reason": f"agy_adapter: unknown mode {mode!r}"} if mode == "push-gate" else {})


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
