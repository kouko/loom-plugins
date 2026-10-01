"""Shell reading for the PreToolUse hook and the GitHub identity.

The hook recognises a publication command only in its most common shape
(`publication_kind`); `github_repo_from_origin` and `CANONICAL_PUSH_FLAGS`
serve `publish`, `land` and `github-rules`.
"""
from __future__ import annotations

from loom_checker.helpers import git_maybe
from pathlib import Path
import re
import shlex


SEGMENT_SPLIT = re.compile(r"\|\||&&|[;\n|&]")


ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


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
