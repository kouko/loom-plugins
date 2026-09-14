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

import getpass
import hashlib
import importlib.util
import json
import os
import re
import shlex
import stat
import subprocess
import sys
import tempfile
from pathlib import Path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent
CHECKER = PLUGIN_ROOT / "scripts" / "loom_checker.py"
SESSION_START = PLUGIN_ROOT / "hooks" / "session-start"
LANGUAGE_ANCHOR = PLUGIN_ROOT / "hooks" / "language-anchor.py"
# <loom-plugin>/[<version>/]skills/<name>/SKILL.md, as agy, Claude Code and a checkout lay it out.
LOOM_SKILL_PATH_RE = re.compile(
    r"/loom-(?:code|design|workflow)/(?:[^/]+/)?skills/[^/]+/SKILL\.md$")
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
    if not isinstance(text, str) or not text:
        return ""
    if not workspaces:
        text += ("\n\nNo workspace is attached to this agy session, so the project's kickoff defaults "
                 "were not loaded. Ask the user to restart agy from the project with "
                 "`agy --add-dir <project>` before working on it.")
    return text


def _state_file(kind: str, payload: dict) -> Path:
    conversation = str(payload.get("conversationId") or os.environ.get("ANTIGRAVITY_CONVERSATION_ID")
                       or payload.get("transcriptPath") or "unknown")
    name = re.sub(r"[^A-Za-z0-9_.-]", "_", conversation)
    if not name.strip("."):  # "." and ".." name the directory itself, not a file in it
        name = "_" + hashlib.sha256(conversation.encode("utf-8")).hexdigest()[:16]
    return Path(tempfile.gettempdir()) / f"{kind}-{_user_tag()}" / name


def _user_tag() -> str:
    """A per-user suffix so users sharing one tempdir never share marker files."""
    if hasattr(os, "getuid"):
        return str(os.getuid())
    try:
        user = getpass.getuser()
    except Exception:  # no login name on this platform
        return "user"
    return re.sub(r"[^A-Za-z0-9_.-]", "_", user).strip(".") or "user"


def _open_state(path: Path, flags: int) -> int:
    """Open a marker inside a private (0o700) state directory this user owns,
    never through a symlink."""
    directory = path.parent
    try:
        directory.mkdir(mode=0o700)
    except FileExistsError:
        pass
    info = os.lstat(directory)
    if not stat.S_ISDIR(info.st_mode) or (hasattr(os, "getuid") and info.st_uid != os.getuid()):
        raise OSError(f"untrusted state directory {directory}")
    return os.open(path, flags | getattr(os, "O_NOFOLLOW", 0), 0o600)


def _read_state(path: Path) -> str | None:
    try:
        with os.fdopen(_open_state(path, os.O_RDONLY), "r", encoding="utf-8") as fh:
            return fh.read()
    except (OSError, ValueError):
        return None


def _write_state(path: Path, text: str) -> None:
    try:
        with os.fdopen(_open_state(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC), "w",
                       encoding="utf-8") as fh:
            fh.write(text)
    except OSError:
        pass


def _first_turn_session_context(payload: dict) -> tuple[str, Path | None]:
    """agy resets invocationNum to 0 on every user turn, so the first turn is
    invocationNum 0 with at most one prior step; a per-conversation marker
    keeps a resumed or compacted conversation from being re-injected.

    Returns the context and the marker to write once the output is built."""
    initial_steps = payload.get("initialNumSteps", 0)
    if payload.get("invocationNum") != 0 or not isinstance(initial_steps, int) or initial_steps > 1:
        return "", None
    marker = _state_file("loom-code-agy-session", payload)
    if _read_state(marker) is not None:
        return "", None
    text = _session_context(payload)
    return (text, marker) if text else ("", None)


def _write_marker(marker: Path) -> None:
    _write_state(marker, "injected")


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_steps(path: str) -> list[dict]:
    steps = []
    # agy appends while hooks run: a read may end mid multibyte character.
    with open(path, "r", encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                step = json.loads(line)
            except ValueError:
                continue
            if isinstance(step, dict):
                steps.append(step)
    return steps


def _arg_value(value):
    """agy's transcript.jsonl stores each tool arg as a JSON string literal
    (``"\\"/path\\""``); transcript_full.jsonl stores it plain. Unwrap one layer."""
    if isinstance(value, str) and len(value) >= 2 and value[0] == value[-1] == '"':
        try:
            decoded = json.loads(value)
        except ValueError:
            return value
        if isinstance(decoded, str):
            return decoded
    return value


def _reads_loom_skill(step: dict) -> bool:
    for call in step.get("tool_calls") or []:
        if not isinstance(call, dict) or call.get("name") != "view_file":
            continue
        args = call.get("args")
        path = _arg_value(args.get("AbsolutePath")) if isinstance(args, dict) else None
        if isinstance(path, str) and LOOM_SKILL_PATH_RE.search(path.replace("\\", "/")):
            return True
    return False


def _language_anchor(payload: dict) -> str:
    transcript = payload.get("transcriptPath")
    if not isinstance(transcript, str) or not transcript:
        return ""
    try:
        steps = _read_steps(transcript)
    except (OSError, ValueError):
        return ""
    # agy invokes the model again after the view_file result step lands, so look
    # back through the current user turn for the latest loom skill read.
    skill_read = None
    for line_no in range(len(steps) - 1, -1, -1):
        step = steps[line_no]
        if step.get("type") == "USER_INPUT":
            break
        if step.get("source") == "MODEL" and _reads_loom_skill(step):
            skill_read = (line_no, step)
            break
    if skill_read is None:
        return ""
    line_no, step = skill_read
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

    # One anchor per skill-read step: every later invocation in the same turn
    # finds the same read again.
    state = _state_file("loom-code-agy-anchor", payload)
    if _read_state(state) == step_key:
        return ""
    _write_state(state, step_key)
    return text


def pre_invocation(payload: dict) -> int:
    session, marker = _first_turn_session_context(payload)
    try:
        anchor = _language_anchor(payload)
    except Exception:  # a transcript problem must not cost the session context
        anchor = ""
    steps = [{"ephemeralMessage": m} for m in (session, anchor) if m]
    output = json.dumps({"injectSteps": steps} if steps else {}, ensure_ascii=False)
    if marker is not None:
        _write_marker(marker)
    print(output)
    return 0


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
