"""`push --hook`: the PreToolUse hook every host runs before a tool call.

The selection-store guard judges first and is the only refusal left here.
A publication command is never refused: its most common shape earns one
reminder line naming the branch's verification status, every other shape is
silent, and a failure inside that path allows (spec
2026-09-22-publication-floor-moves-to-github REQ-4, REQ-12).
"""
from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import repo_root
from loom_checker.rule_checks.push import publication_kind
from loom_checker.rule_checks.selection_guard import FILE_TOOLS as SELECTION_GUARD_FILE_TOOLS
from loom_checker.rule_checks.selection_guard import RULE_ID as SELECTION_GUARD_RULE
from loom_checker.rule_checks.selection_guard import guard_reason as selection_guard_reason
from loom_checker.verification import identify_change
from loom_checker.verification import missing_clause
from loom_checker.verification import missing_records
from loom_checker.verification import verification_status
from pathlib import Path
import json
import os
import sys


def read_hook_payload(stdin=sys.stdin) -> dict | None:
    """PreToolUse payload (Claude Code and Codex share the shape) when the
    checker is invoked as a hook; None when run from a terminal or with an
    empty stdin. Malformed JSON is a UsageError → exit 2 (fail-closed)."""
    if stdin is None or stdin.isatty():
        return None
    raw = stdin.read()
    if not raw.strip():
        return None
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise UsageError(f"hook payload is not JSON: {exc}")
    if not isinstance(payload, dict):
        raise UsageError("hook payload must be a JSON object.")
    return payload


def cmd_push(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """`--hook` is what selects hook mode, never the shape of stdin: a
    checker run from a station (or a terminal, or any harness that hands it
    a pipe nobody ever closes) must never block on `stdin.read()`."""
    if list(args) != ["--hook"]:
        raise UsageError("push runs only as a hook: push --hook.")

    payload = read_hook_payload()
    if payload is None:
        raise UsageError("push --hook expects a PreToolUse JSON payload on stdin.")
    # The record-store guard judges every matched tool call first.
    try:
        guard_reason = selection_guard_reason(payload)
    except Exception as exc:  # a guard that cannot judge refuses: never loosened
        guard_reason = f"the guard failed ({type(exc).__name__}: {exc})"
    if guard_reason:
        print(f"BLOCK {SELECTION_GUARD_RULE}: {guard_reason}", file=err)
        return 2
    if payload.get("tool_name") in SELECTION_GUARD_FILE_TOOLS:
        return 0
    command = str((payload.get("tool_input") or {}).get("command", ""))
    kind = publication_kind(command)
    if kind is None:
        return 0
    try:
        line = _reminder(kind, Path(str(payload.get("cwd") or os.getcwd())))
    except Exception as exc:  # a reminder that cannot be computed never blocks
        line = f"loom: publication hook failed ({exc}); allowing."
    if line:
        _emit(line, out, err)
    return 0


def _reminder(kind: str, cwd: Path) -> str | None:
    """The one line a direct push, PR create or PR merge earns, or None."""
    repo = repo_root(cwd)
    change_id, _unidentified = identify_change(repo)
    status = verification_status(repo, change_id, depth="local") if change_id else None
    clause = missing_clause(missing_records(repo, change_id, status)) if change_id else ""
    clause = f" {clause}" if clause else ""
    if kind == "merge":
        return f"loom: this merges outside loom_checker.py land{clause}; merging anyway."
    if change_id is None:
        return "loom: change not identified (no intent for this branch); publishing anyway."
    if status == "valid":
        return None
    return f"loom: verification {status}{clause}; publishing anyway."


def _emit(line: str, out, err) -> None:
    """Claude Code reads a PreToolUse `systemMessage` from stdout; Codex and
    a terminal read stderr."""
    out.write(json.dumps({"systemMessage": line}, ensure_ascii=False) + "\n")
    err.write(line + "\n")
