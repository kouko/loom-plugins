"""PreToolUse guard over the selection record store.

The store lives at `<git common dir>/loom/selections/`. The guard stops an
agent taking a shortcut: running the capture command itself, or writing a
record through a recognised shell write form or a file-writing tool. A
command deliberately disguised to evade text matching is outside the local
guarantee; that boundary is the one the attestation design already keeps.
"""
from __future__ import annotations

from loom_checker.helpers import git_maybe
from loom_checker.rule_checks.push import _shell_segments
from loom_checker.rule_checks.push import _strip_prefix
from loom_checker.rule_checks.push import _tokenise
from pathlib import Path
import os
import re


RULE_ID = "selection.guard"

FILE_TOOLS = {"Write", "Edit", "MultiEdit", "NotebookEdit", "apply_patch"}

ALWAYS_DENIED = [
    (re.compile(r"selection\s+capture"), "the selection capture command runs only from the prompt hook"),
    (re.compile(r"loom/selections/"), "names the selection record store"),
    (re.compile(r"\.git/loom"), "names the loom record directory"),
]

BARE_SELECTIONS = re.compile(r"(?<![\w.-])selections/")

GIT_DIR_NAMES = re.compile(r"git-common-dir|--git-dir|\bGIT_DIR\b")

WRITE_COMMANDS = {"tee", "cp", "mv", "dd", "install"}

INTERPRETER = re.compile(r"(python[0-9.]*|perl|ruby|node)")

INLINE_CODE_FLAG = re.compile(r"-[A-Za-z]*[ce]|--eval")

REDIRECT = re.compile(r">>?(&?)\s*(\S*)")

PATCH_HEADER = re.compile(r"^\*\*\* (?:Add File|Update File|Delete File|Move to): (.+?)\s*$", re.M)


def _has_redirect_write(text: str) -> bool:
    for match in REDIRECT.finditer(text):
        if match.group(1) or match.group(2) == "/dev/null":
            continue  # a descriptor duplicate or a discard writes no file
        return True
    return False


def _has_write_form(command: str, depth: int = 0) -> bool:
    if _has_redirect_write(command):
        return True
    for segment in _shell_segments(command):
        tokens = _tokenise(segment)
        program = _strip_prefix(tokens)
        while program and program[0].startswith("-"):
            program = program[1:]  # options of a stripped wrapper such as xargs
        if program:
            name = Path(program[0]).name
            if name in WRITE_COMMANDS:
                return True
            if name == "sed" and any(
                t == "--in-place" or re.match(r"-[^-]*i", t) for t in program[1:]
            ):
                return True
        for index, token in enumerate(tokens):
            if token in {"-exec", "-execdir"} and index + 1 < len(tokens):
                if Path(tokens[index + 1]).name in WRITE_COMMANDS:
                    return True
            if INTERPRETER.fullmatch(Path(token).name) and any(
                INLINE_CODE_FLAG.fullmatch(t) for t in tokens[index + 1:]
            ):
                return True
            if depth < 2 and " " in token and _has_write_form(token, depth + 1):
                return True  # `bash -c '…'`, `eval '…'`
    return False


def bash_guard_reason(command: str) -> str | None:
    """Why a Bash command is denied, or None when it passes."""
    for pattern, reason in ALWAYS_DENIED:
        if pattern.search(command):
            return reason
    if BARE_SELECTIONS.search(command) and _has_write_form(command):
        return "writes a selections/ path"
    if GIT_DIR_NAMES.search(command) and _has_write_form(command):
        return "writes through the git directory"
    return None


def file_targets(tool_input: dict) -> list[str]:
    """Target paths of a file-writing tool call: Claude Code path fields and
    Codex apply_patch file headers found in any string field."""
    targets: list[str] = []
    for key, value in tool_input.items():
        if not isinstance(value, str):
            continue
        if key in {"file_path", "notebook_path"}:
            targets.append(value)
        targets.extend(PATCH_HEADER.findall(value))
    return targets


def _under(path: Path, directory: Path) -> bool:
    return path == directory or directory in path.parents


def guard_reason(payload: dict) -> str | None:
    """Why a PreToolUse payload is denied, or None when it passes."""
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return None
    if tool_name not in FILE_TOOLS:
        return bash_guard_reason(str(tool_input.get("command", "")))
    targets = file_targets(tool_input)
    if not targets:
        return None
    cwd = Path(str(payload.get("cwd") or os.getcwd()))
    common = git_maybe(cwd, "rev-parse", "--git-common-dir") if cwd.is_dir() else None
    loom_dir = Path(os.path.realpath(cwd / common / "loom")) if common else None
    for target in targets:
        resolved = Path(os.path.realpath(cwd / os.path.expanduser(target)))
        if (loom_dir and _under(resolved, loom_dir)) or "/.git/loom" in f"{resolved}/":
            return f"{target} resolves under the loom record directory"
    return None
