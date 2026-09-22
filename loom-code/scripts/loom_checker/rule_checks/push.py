"""Shell reading shared by the PreToolUse hook and the selection-store guard.

The hook recognises a publication command only in its most common shape
(`publication_kind`); the segment splitter, tokeniser and prefix stripper
serve `selection_guard.py`; `github_repo_from_origin` and
`CANONICAL_PUSH_FLAGS` serve `publish`, `land` and `github-rules`.
"""
from __future__ import annotations

from loom_checker.helpers import git_maybe
from pathlib import Path
import re
import shlex


SEGMENT_SPLIT = re.compile(r"\|\||&&|[;\n|&]")


ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


ENV_VALUE_OPTIONS = {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"}


PREFIX_WORDS = {"sudo", "command", "env", "nohup", "time", "nice", "builtin", "exec", "xargs"}


SHELL_PROGRAMS = {"bash", "sh", "zsh", "dash"}


# Words a shell reads as grammar rather than as the command word, so that the
# heredoc owned by `if …; then bash <<EOF` is still owned by `bash`.
HEREDOC_GRAMMAR_WORDS = {"!", "then", "else", "elif", "do"}


# Every option a `PREFIX_WORDS` wrapper spends a separate token on before the
# program it runs, read from the wrappers' own manuals: sudo -u/-g/-C,
# xargs -n/-L/-I/-P/-d/-s/-a, nice -n, exec -a, env's own set below. An option
# carrying its value in one token (`-n1`) spends one and needs no entry.
WRAPPER_VALUE_OPTIONS = ENV_VALUE_OPTIONS | {
    "-g", "--group", "--user", "-n", "--max-args", "-L", "--max-lines",
    "-I", "--replace", "-P", "--max-procs", "-d", "--delimiter",
    "-s", "--max-chars", "-a", "--arg-file",
}


# Every character that ends a heredoc delimiter word, as a shell ends one.
HEREDOC_WORD_END = frozenset(" \t\n;&|<>()")


def _command_word_is_a_shell(text: str) -> bool:
    """Whether one pipeline member runs what it is handed as commands.

    `_strip_command_word_prefix`, not `_strip_prefix`: the narrow one stops at the
    first `-` token, so `sudo -u bob bash <<EOF` would read its command word as
    `-u` and carve an executed body out as content. Over-reading here judges a
    body that would otherwise reach no rule, so the wide one is the one that
    fails in the safe direction.

    The bare `<<` form names no command word and the shell reads that body
    itself, so an absent command word reads as executing."""
    tokens = _strip_command_word_prefix(_tokenise(text.lstrip("({ \t")))
    while tokens and tokens[0] in HEREDOC_GRAMMAR_WORDS:
        tokens = _strip_command_word_prefix(tokens[1:])
    if not tokens:
        return True
    return _program(tokens[0]) in SHELL_PROGRAMS


def _heredoc_executes_body(pipeline: str) -> bool:
    """True when a heredoc's body reaches something that runs it as commands.

    The question is the whole pipeline, not the command word owning the
    redirect: in `cat <<EOF | bash` the body is `cat`'s stdin and `bash`'s
    stdin in turn, so a shell does execute it. Judging only the owner carves
    the body out of the very pipeline that runs it, and a carved body reaches
    no rule at all.

    Over-reading a member here only sends a body to the recognisers that would
    otherwise be treated as file content, so any doubt answers True."""
    return any(
        _command_word_is_a_shell(member)
        for member in _operator_segments(pipeline)
    )


def _heredoc_delimiter(command: str, index: int) -> tuple[str, int] | None:
    """Read the delimiter word at ``index`` as the literal a shell matches.

    A delimiter may be written bare, quoted (`'EOF'`, `"EOF"`) or
    backslash-escaped (`\\EOF`); the quoting selects expansion inside the body,
    which no recogniser reads, so only the literal survives here. None when no
    word is there. Returns the literal and the position just past the word."""
    while index < len(command) and command[index] in " \t":
        index += 1
    delimiter: list[str] = []
    quote: str | None = None
    while index < len(command):
        character = command[index]
        if quote:
            if character == quote:
                quote = None
            else:
                delimiter.append(character)
        elif character in {"'", '"'}:
            quote = character
        elif character == "\\" and index + 1 < len(command):
            index += 1
            delimiter.append(command[index])
        elif character in HEREDOC_WORD_END:
            break
        else:
            delimiter.append(character)
        index += 1
    if quote or not delimiter:
        return None
    return "".join(delimiter), index


def _consume_heredoc_bodies(
    command: str,
    start: int,
    pending: list[tuple[str, bool, bool]],
    executed: list[str],
) -> int | None:
    """Carve the bodies that follow a logical line, left to right.

    Each executed body is appended to ``executed`` for the caller to judge as
    commands in its own right. None when a terminator is not where a shell
    would find it, which makes the whole pass fail toward judging."""
    index = start
    for delimiter, strip_tabs, executes in pending:
        body: list[str] = []
        while True:
            end = command.find("\n", index)
            line = command[index:] if end < 0 else command[index:end]
            if (line.lstrip("\t") if strip_tabs else line) == delimiter:
                index = len(command) if end < 0 else end + 1
                break
            if end < 0:  # the terminator line never arrives
                return None
            body.append(line)
            index = end + 1
        if executes:
            executed.append("\n".join(body))
    return index


def _without_unexecuted_heredocs(command: str) -> tuple[str, list[str]]:
    """Carve every heredoc body out of ``command``.

    Returns the remaining text plus the bodies a shell interpreter executes.
    A body its command word does not execute -- `cat`, `tee`, a redirect to a
    file -- is file content, and judging it as commands is what makes the same
    bytes refused through Bash and allowed through a file-writing tool.

    A body begins after the end of the *logical* line, so a backslash
    continuation is joined before the body is located, and `<<<` is a
    herestring rather than a heredoc. Anything this cannot locate exactly as a
    shell would returns the original text and no bodies: the fail direction is
    toward judging, never toward silence."""
    kept: list[str] = []
    executed: list[str] = []
    pending: list[tuple[str, bool, bool]] = []
    copied = 0
    segment_start = 0
    index = 0
    quote: str | None = None
    escaped = False
    while index < len(command):
        character = command[index]
        if escaped:
            escaped = False
        elif character == "\\" and quote != "'":
            escaped = True
        elif quote:
            if character == quote:
                quote = None
        elif character in {"'", '"'}:
            quote = character
        elif character == "<" and command[index + 1:index + 2] == "<":
            if command[index + 2:index + 3] == "<":
                index += 3
                continue
            after = index + 2
            strip_tabs = command[after:after + 1] == "-"
            found = _heredoc_delimiter(command, after + 1 if strip_tabs else after)
            if found is None:
                return command, []
            delimiter, after = found
            # Whether the body is executed cannot be decided here: the pipeline
            # member that runs it may still be to the right (`cat <<EOF | bash`).
            # Keep where this command began and decide at the end of the line.
            pending.append((delimiter, strip_tabs, segment_start))
            index = after
            continue
        elif character == "\n" and pending:
            kept.append(command[copied:index + 1])
            line = command[:index]
            resolved = [
                (delimiter, strip_tabs, _heredoc_executes_body(line[start:]))
                for delimiter, strip_tabs, start in pending
            ]
            consumed = _consume_heredoc_bodies(command, index + 1, resolved, executed)
            if consumed is None:
                return command, []
            copied = index = segment_start = consumed
            pending = []
            continue
        elif character in ";\n|&":
            segment_start = index + 1
        index += 1
    if quote or escaped or pending:
        return command, []
    kept.append(command[copied:])
    return "".join(kept), executed


def _shell_segments(command: str) -> list[str]:
    """Split on shell operators outside quotes, reading each heredoc body as
    its command word reads it: an executed body is re-fed as commands, and a
    body that is file content is dropped before the split."""
    stripped, executed = _without_unexecuted_heredocs(command)
    segments = _operator_segments(stripped)
    for body in executed:
        segments.extend(_shell_segments(body))
    return segments


def _operator_segments(command: str) -> list[str]:
    """Split on shell operators outside quotes; malformed input stays strict."""
    segments: list[str] = []
    conservative_command = list(command)
    start = 0
    quote: str | None = None
    escaped = False
    dynamic = False
    index = 0
    while index < len(command):
        character = command[index]
        if escaped:
            escaped = False
        elif character == "\\" and quote != "'":
            escaped = True
        elif (
            character == "$"
            and quote != "'"
            and index + 1 < len(command)
            and command[index + 1] == "("
        ):
            dynamic = True
            conservative_command[index] = "\n"
            conservative_command[index + 1] = "\n"
        elif character == "`" and quote != "'":
            dynamic = True
            conservative_command[index] = "\n"
        elif quote:
            if character == quote:
                quote = None
        elif character in {"'", '"'}:
            quote = character
        elif character in ";\n|&":
            segments.append(command[start:index])
            if (
                character in "|&"
                and index + 1 < len(command)
                and command[index + 1] == character
            ):
                index += 1
            start = index + 1
        index += 1
    if quote or escaped or dynamic:
        return SEGMENT_SPLIT.split("".join(conservative_command))
    segments.append(command[start:])
    return segments


def _tokenise(segment: str) -> list[str]:
    try:
        return shlex.split(segment)
    except ValueError:  # an unbalanced quote is still worth judging
        return segment.split()


def _program(token: str) -> str:
    """Executable basename, case-folded: a case-insensitive filesystem (default
    macOS) runs ``GIT push`` as git."""
    return Path(token).name.lower()


def _strip_prefix(tokens: list[str]) -> list[str]:
    """Drop `VAR=…` assignments and wrapper words that precede the program."""
    index = 0
    while index < len(tokens):
        if ASSIGNMENT.match(tokens[index]):
            index += 1
            continue
        wrapper = _program(tokens[index])
        if wrapper not in PREFIX_WORDS:
            break
        index += 1
        if wrapper == "env":
            while index < len(tokens) and tokens[index].startswith("-"):
                option = tokens[index]
                index += 2 if option in ENV_VALUE_OPTIONS else 1
    return tokens[index:]


def _strip_command_word_prefix(tokens: list[str]) -> list[str]:
    """`_strip_prefix` widened by the shell grammar and the wrapper options a
    command word can sit behind: `if …; then`, `( … )`, `{ …; }`,
    `sudo -u bob`, `xargs -n1`. Heredoc carving alone uses it, to find the
    command word that owns a body."""
    index = 0
    while index < len(tokens):
        token = tokens[index].lstrip("({")
        if not token or ASSIGNMENT.match(token):
            index += 1
            continue
        word = _program(token)
        if word in HEREDOC_GRAMMAR_WORDS:
            index += 1
            continue
        if word not in PREFIX_WORDS:
            return [token, *tokens[index + 1:]]
        index += 1
        while index < len(tokens) and tokens[index].startswith("-"):
            option = tokens[index]
            index += 2 if option in WRAPPER_VALUE_OPTIONS else 1
    return []


def publication_kind(command: str) -> str | None:
    """`push`, `create` or `merge` when the first simple command of the text,
    after leading `VAR=value` assignments, is literally `git push`,
    `gh pr create` or `gh pr merge`; None for every other shape.

    Shallow on purpose: the hook only reminds, so a shape read here costs a
    reminder line and a shape missed costs nothing. A wrapper, a prefix
    command, a `bash -c` script, a heredoc body and a mere mention of the
    words are all None."""
    first = next((segment for segment in _operator_segments(command) if segment.strip()), "")
    tokens = _tokenise(first)
    while tokens and ASSIGNMENT.match(tokens[0]):
        tokens = tokens[1:]
    if tokens[:2] == ["git", "push"]:
        return "push"
    if tokens[:2] == ["gh", "pr"] and tokens[2:3] in (["create"], ["merge"]):
        return tokens[2]
    return None


def github_repo_from_origin(repo: Path) -> str | None:
    """Return GH_REPO syntax derived from the literal configured origin URL."""
    url = git_maybe(repo, "remote", "get-url", "origin")
    if not url:
        return None
    match = re.fullmatch(r"https?://([^/]+)/([^/]+)/(.+?)(?:\.git)?", url)
    if not match:
        match = re.fullmatch(r"git@([^:]+):([^/]+)/(.+?)(?:\.git)?", url)
    if not match:
        match = re.fullmatch(r"ssh://git@([^/]+)/([^/]+)/(.+?)(?:\.git)?", url)
    if not match:
        return None
    host, owner, name = match.groups()
    return f"{host}/{owner}/{name}"


CANONICAL_PUSH_FLAGS = ["--no-follow-tags", "--recurse-submodules=no", "-u", "--no-verify"]
