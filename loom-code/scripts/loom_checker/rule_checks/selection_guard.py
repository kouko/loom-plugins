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
    (re.compile(r"loom/selections/"), "names the selection record store"),
    (re.compile(r"\.git/loom"), "names the loom record directory"),
]

CHECKER_PROGRAM = re.compile(r"loom_checker(?:\.py)?")

HOST_PROGRAMS = {"claude", "codex"}

ENTRY_POINT = re.compile(r"(?<![\w-])[/$](?:loom-code:)?expert-mode(?![\w-])")

BARE_SELECTIONS = re.compile(r"(?<![\w.-])selections/")

LOOM_OR_GIT_NAME = re.compile(r"(?<![\w-])(?:loom|\.git)(?![\w-])")

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


def _token_lists(command: str, depth: int = 0):
    """Tokens of every shell segment, including code quoted for `bash -c`."""
    for segment in _shell_segments(command):
        tokens = _tokenise(segment)
        yield tokens
        if depth < 2:
            for token in tokens:
                if " " in token:
                    yield from _token_lists(token, depth + 1)


def _runs_capture(tokens: list[str]) -> bool:
    """The checker program followed by the `selection capture` words."""
    for index, token in enumerate(tokens):
        if CHECKER_PROGRAM.fullmatch(Path(token).name):
            rest = tokens[index + 1:]
            return any(rest[i:i + 2] == ["selection", "capture"] for i in range(len(rest)))
    return False


def _runs_host(tokens: list[str]) -> bool:
    program = _strip_prefix(tokens)
    while program and program[0].startswith("-"):
        program = program[1:]  # options of a stripped wrapper such as xargs
    return bool(program) and Path(program[0]).name in HOST_PROGRAMS


def bash_guard_reason(command: str) -> str | None:
    """Why a Bash command is denied, or None when it passes."""
    token_lists = list(_token_lists(command))
    if any(_runs_capture(tokens) for tokens in token_lists):
        return "the selection capture command runs only from the prompt hook"
    for pattern, reason in ALWAYS_DENIED:
        if pattern.search(command):
            return reason
    if ENTRY_POINT.search(command) and any(_runs_host(tokens) for tokens in token_lists):
        return "a nested host session's expert-mode prompt would pass as user-typed"
    if (BARE_SELECTIONS.search(command) and LOOM_OR_GIT_NAME.search(command)
            and _has_write_form(command)):
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


def _loom_dir(cwd: Path) -> Path | None:
    """`<git common dir>/loom` of the repository at cwd; None when git fails."""
    common = git_maybe(cwd, "rev-parse", "--git-common-dir") if cwd.is_dir() else None
    return Path(os.path.realpath(cwd / common / "loom")) if common else None


def guard_reason(payload: dict) -> str | None:
    """Why a PreToolUse payload is denied, or None when it passes."""
    tool_name = payload.get("tool_name")
    tool_input = payload.get("tool_input") or {}
    if not isinstance(tool_input, dict):
        return None
    cwd = Path(str(payload.get("cwd") or os.getcwd()))
    if tool_name not in FILE_TOOLS:
        command = str(tool_input.get("command", ""))
        reason = bash_guard_reason(command)
        if reason is None and re.search(r"\.git|loom", str(cwd)) and _has_write_form(command):
            loom_dir = _loom_dir(cwd)  # git runs only for a cwd that could be the store
            if loom_dir and _under(Path(os.path.realpath(cwd)), loom_dir):
                return "writes from a working directory inside the loom record directory"
        return reason
    targets = file_targets(tool_input)
    if not targets:
        return None
    loom_dir = _loom_dir(cwd)
    for target in targets:
        resolved = Path(os.path.realpath(cwd / os.path.expanduser(target)))
        if (loom_dir and _under(resolved, loom_dir)) or "/.git/loom" in f"{resolved}/":
            return f"{target} resolves under the loom record directory"
    return None
