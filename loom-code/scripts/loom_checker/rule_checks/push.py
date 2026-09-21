from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_text
from loom_checker.helpers import repo_root
from pathlib import Path
from urllib.parse import quote
import os
import re
import shlex
import shutil
import subprocess


SEGMENT_SPLIT = re.compile(r"\|\||&&|[;\n|&]")


ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")


GIT_VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}


GH_VALUE_OPTIONS = {"-R", "--repo", "--hostname"}


GIT_REPOSITORY_ENV = {"GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GH_REPO"}


ENV_VALUE_OPTIONS = {"-u", "--unset", "-C", "--chdir", "-S", "--split-string"}


PREFIX_WORDS = {"sudo", "command", "env", "nohup", "time", "nice", "builtin", "exec", "xargs"}


SHELL_PROGRAMS = {"bash", "sh", "zsh", "dash"}


# Words a shell reads as grammar rather than as the command word, so that the
# heredoc owned by `if …; then bash <<EOF` is still owned by `bash`, and so that
# merge recognition reads `if …; then gh pr merge` as the merge it runs.
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

    `_strip_merge_prefix`, not `_strip_prefix`: the narrow one stops at the
    first `-` token, so `sudo -u bob bash <<EOF` would read its command word as
    `-u` and carve an executed body out as content. The narrow helper is right
    for push recognition, where over-reading refuses a command that runs today;
    here over-reading judges a body that would otherwise reach no rule, so the
    wide one is the one that fails in the safe direction.

    The bare `<<` form names no command word and the shell reads that body
    itself, so an absent command word reads as executing."""
    tokens = _strip_merge_prefix(_tokenise(text.lstrip("({ \t")))
    while tokens and tokens[0] in HEREDOC_GRAMMAR_WORDS:
        tokens = _strip_merge_prefix(tokens[1:])
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


def _strip_merge_prefix(tokens: list[str]) -> list[str]:
    """`_strip_prefix` widened by the shell grammar and the wrapper options a
    merge can sit behind: `if …; then`, `( … )`, `{ …; }`, `sudo -u bob`,
    `xargs -n1`.

    Merge recognition alone gets this. The push recognisers keep the narrower
    `_strip_prefix`, because a wrapped push they do not see today still runs
    today: seeing it would send it to the canonical-form check that refuses it,
    turning a command that runs into a blocked one."""
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


def _subcommand_at(tokens: list[str], value_options: set[str]) -> tuple[int, str] | None:
    """The position and value of the first non-option, non-value word."""
    index = 0
    while index < len(tokens):
        token = tokens[index]
        if token == "--":
            return None
        if token in value_options:
            index += 2
            continue
        if token.startswith("-"):
            index += 1
            continue
        return index, token
    return None


def _subcommand(tokens: list[str], value_options: set[str]) -> str | None:
    """The first word that is neither an option nor an option's value."""
    found = _subcommand_at(tokens, value_options)
    return found[1] if found else None


def is_push_command(command: str) -> bool:
    """True when any segment of this shell line pushes or opens/merges a PR."""
    if is_git_push_command(command):
        return True
    for segment in _shell_segments(command):
        tokens = _strip_prefix(_tokenise(segment))
        if not tokens:
            continue
        program = _program(tokens[0])
        if program == "eval":
            if is_push_command(" ".join(tokens[1:])):
                return True
        elif program in SHELL_PROGRAMS and "-c" in tokens[1:]:
            index = tokens.index("-c")
            if index + 1 < len(tokens) and is_push_command(tokens[index + 1]):
                return True
        elif program == "gh":
            rest = tokens[1:]
            found = _subcommand_at(rest, GH_VALUE_OPTIONS)
            if found and found[1] == "pr":
                after = rest[found[0] + 1:]
                if _subcommand(after, GH_VALUE_OPTIONS) in {"create", "merge"}:
                    return True
    return False


def is_pr_create_command(command: str) -> bool:
    """True when a shell segment creates a PR."""
    for segment in _shell_segments(command):
        tokens = _strip_prefix(_tokenise(segment))
        if not tokens or _program(tokens[0]) != "gh":
            continue
        rest = tokens[1:]
        found = _subcommand_at(rest, GH_VALUE_OPTIONS)
        if found and found[1] == "pr":
            after = rest[found[0] + 1:]
            if _subcommand(after, GH_VALUE_OPTIONS) == "create":
                return True
    return False


def _merge_word(token: str | None) -> str:
    """A gh subcommand word as the shell hands it over, case-folded.

    `shlex` knows nothing of ANSI-C (`$'merge'`) or locale (`$"merge"`)
    quoting: it removes the quotes and leaves `$merge`, where the shell passes
    `merge`. A leading `$` is therefore dropped. That also reads a genuine
    expansion (`$merge`) as the word, which is the fail-closed direction: the
    token stands in the subcommand position of `gh pr`, so what it expands to
    cannot be resolved here and the refusal is the safe answer.

    Case-folded because a case-insensitive filesystem runs `GH` as `gh`, and
    gh matches its own subcommands case-insensitively."""
    if token is None:
        return ""
    return token.lstrip("$").strip("'\"").lower()


def is_pr_merge_command(command: str) -> bool:
    """True when a shell segment merges a PR, whatever shell grammar or wrapper
    options stand in front of it.

    Backslash-continuations are joined first: the shell joins them before it
    reads a command word, so `gh pr \\<newline>merge 7` is one command, while
    `_shell_segments` splits on the raw newline and would read two."""
    for segment in _shell_segments(command.replace("\\\n", "")):
        tokens = _strip_merge_prefix(_tokenise(segment))
        if not tokens or _program(tokens[0]) != "gh":
            continue
        rest = tokens[1:]
        found = _subcommand_at(rest, GH_VALUE_OPTIONS)
        if found and _merge_word(found[1]) == "pr":
            after = rest[found[0] + 1:]
            if _merge_word(_subcommand(after, GH_VALUE_OPTIONS)) == "merge":
                return True
    return False


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


# Every trailing option the canonical PR-create form may carry, with the number
# of tokens it spends: 2 for an option and its value, 1 for a flag.
#
# An allowlist rather than a list of refused spellings, because the refused list
# can only ever be as current as gh's release notes: a body-determining flag
# added in a later gh release would be admitted by a refused-list check and then
# read by `pr_create_body` as an empty body, which is the shape of F8. Here an
# option this repository has never heard of is simply not canonical.
#
# Only the separate-value spelling is canonical. `--body-file=<path>` and the
# short forms (`-F`, `-H`, `-b`, `-t`) are not: `-F` is the one option the hook
# and the shell could resolve differently, because `check_pr_create_remote_head`
# requires an absolute path of `--body-file` and `--body-file=` alone, while the
# hook resolves a relative path against the repository root it chdirs to and the
# shell resolves it against the payload's `cwd`.
#
# GitHub CLI documents every `gh pr create` flag, its short form and whether it
# takes a value -- the arities below are read from that list:
# https://cli.github.com/manual/gh_pr_create
CANONICAL_PR_CREATE_OPTIONS = {
    "--base": 2, "--head": 2, "--title": 2, "--body-file": 2, "--draft": 1,
}


def canonical_pr_create_trailing(trailing: list[str]) -> bool:
    """True when every trailing token belongs to an allowlisted option.

    An option consumes its own value, so a value that looks like an option is
    read as a value -- which is how gh's flag parser reads it too."""
    # gh parses its flags with spf13/pflag, whose `parseLongArg` takes the next
    # argument as the value of a flag that declares no `NoOptDefVal`, without
    # testing it for a leading dash. That is the rule the walk below repeats:
    # https://github.com/spf13/pflag/blob/master/flag.go
    index = 0
    while index < len(trailing):
        width = CANONICAL_PR_CREATE_OPTIONS.get(trailing[index])
        if width is None or index + width > len(trailing):
            return False
        index += width
    return True


def is_canonical_pr_create_command(repo: Path, command: str) -> bool:
    """True only for one function-proof, origin-bound PR creation command."""
    trusted = shutil.which("gh")
    trusted_env = shutil.which("env")
    gh_repo = github_repo_from_origin(repo)
    if not trusted or not trusted_env or not gh_repo:
        return False
    gh_tokens = _tokenise(command)
    expected_prefix = [
        "command", str(Path(trusted_env).resolve()), f"LOOM_REPO_ROOT={repo.resolve()}",
        f"GH_REPO={gh_repo}", str(Path(trusted).resolve()), "pr", "create",
    ]
    return (
        gh_tokens[:7] == expected_prefix
        and canonical_pr_create_trailing(gh_tokens[7:])
        and command == render_quote_all(gh_tokens)
    )


def canonical_pr_create_repo(command: str) -> Path | None:
    """Return the selected repo only when the whole PR-create form is trusted."""
    tokens = _tokenise(command)
    if len(tokens) < 7 or not tokens[2].startswith("LOOM_REPO_ROOT="):
        return None
    selected = Path(tokens[2].split("=", 1)[1])
    if not selected.is_absolute() or not selected.is_dir():
        return None
    try:
        repo = repo_root(selected.resolve())
    except UsageError:
        return None
    if repo.resolve() != selected.resolve():
        return None
    return repo if is_canonical_pr_create_command(repo, command) else None


def pr_create_body(command: str) -> str:
    """The PR body this `gh pr create` would send.

    Read from the last `--body-file`, because that is the one gh keeps when a
    command repeats the option: a gate that read the first would judge a body
    the pull request never receives. The ship station's form carries
    `--body-file` with an absolute path, which `check_pr_create_remote_head`
    requires of every command it admits.

    The inline spellings (`--body`, `-b`, `--body=`) are not read, because no
    command carrying one ever reaches this reader: `CANONICAL_PR_CREATE_OPTIONS`
    admits only `--base`, `--head`, `--title`, `--body-file` and `--draft`, and
    the sole caller (command_handlers/push.py) refuses anything else at
    admission. Were one ever allowlisted it would read as "" here, which
    discloses nothing and refuses.

    "" when the command names no body and when the named file cannot be read:
    an empty body discloses nothing, which is exactly what a body the gate
    cannot read has proven about itself.

    Only a readable regular file is read, which is the guard `_publish_args`
    (command_handlers/publish.py) already puts on `--body-file`. This runs
    inside a `PreToolUse` hook that has no timeout of its own, so an unguarded
    `read_text` on a FIFO blocks the agent forever and one on a character
    device reads without end. `-` is gh's spelling for stdin, which the gate
    cannot see at all, so it is never treated as a path."""
    tokens = _tokenise(command)
    body = ""
    for index, token in enumerate(tokens):
        following = tokens[index + 1] if index + 1 < len(tokens) else None
        if token in {"--body-file", "-F"} and following is not None:
            path = following
        elif token.startswith("--body-file="):
            path = token.split("=", 1)[1]
        else:
            continue
        body = ""
        named = Path(path)
        if path == "-" or not named.is_file() or not os.access(named, os.R_OK):
            continue
        try:
            body = named.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            body = ""
    return body


def check_pr_create_remote_head(repo: Path, command: str) -> str | None:
    """Require PR creation to reference the already-published current HEAD."""
    branch = git_maybe(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    head = git_maybe(repo, "rev-parse", "HEAD")
    if not branch or not head:
        return "PR creation requires a current symbolic branch and commit"

    tokens = _tokenise(command)
    head_values: list[str] = []
    for index, token in enumerate(tokens):
        if token in {"--head", "-H"} and index + 1 < len(tokens):
            head_values.append(tokens[index + 1])
        elif token.startswith("--head="):
            head_values.append(token.split("=", 1)[1])
        elif token.startswith("-H") and token != "-H":
            head_values.append(token[2:])
        if token == "--body-file" and (
            index + 1 >= len(tokens) or not Path(tokens[index + 1]).is_absolute()
        ):
            return "PR body file must be an absolute path"
        if token.startswith("--body-file=") and not Path(token.split("=", 1)[1]).is_absolute():
            return "PR body file must be an absolute path"
    if head_values != [branch]:
        if not head_values:
            return f"PR creation requires explicit current branch head {branch!r}"
        else:
            return f"PR head must be the current branch {branch!r}"

    gh_repo = github_repo_from_origin(repo)
    trusted_gh = shutil.which("gh")
    if not gh_repo or not trusted_gh:
        return "PR creation requires a trusted GitHub origin and gh executable"
    repo_parts = gh_repo.split("/")
    host, owner, name = repo_parts[0], repo_parts[-2], repo_parts[-1]
    try:
        # GitHub CLI documents the endpoint form plus --hostname and --jq:
        # https://cli.github.com/manual/gh_api
        # GitHub documents this reference endpoint and its object.sha response:
        # https://docs.github.com/en/rest/git/refs#get-a-reference
        observed = subprocess.run(
            [str(Path(trusted_gh).resolve()), "api", "--hostname", host,
             f"repos/{owner}/{name}/git/ref/heads/{quote(branch, safe='')}",
             "--jq", ".object.sha"],
            cwd=repo, capture_output=True, text=True, timeout=30,
            env={**os.environ, "GH_REPO": gh_repo, "LOOM_REPO_ROOT": str(repo)},
        )
    except (OSError, subprocess.TimeoutExpired):
        observed = None
    if observed is not None and observed.returncode == 0 and observed.stdout.strip() == head:
        return None
    return f"remote branch {branch!r} must already equal reviewed HEAD {head}"


def is_git_push_command(command: str) -> bool:
    """True when any shell segment can reach a Git push."""
    for segment in _shell_segments(command):
        tokens = _strip_prefix(_tokenise(segment))
        if not tokens:
            continue
        program = _program(tokens[0])
        if program == "eval":
            if is_git_push_command(" ".join(tokens[1:])):
                return True
        elif program in SHELL_PROGRAMS and "-c" in tokens[1:]:
            index = tokens.index("-c")
            if index + 1 < len(tokens) and is_git_push_command(tokens[index + 1]):
                return True
        elif program == "git" and _subcommand(tokens[1:], GIT_VALUE_OPTIONS) == "push":
            return True
    return False


def git_dash_c_push_cwd(command: str, fallback: str) -> str | None:
    """Return the one unambiguous repository selected by every Git push.

    The host-reported cwd is authoritative only when a push has no directory
    override. An absolute ``-C`` anchors later relative ``-C`` options. A
    relative first ``-C``, another directory-changing option, a missing or
    invalid directory, or pushes selecting distinct repositories is unsafe
    because the hook cannot prove which repository the shell will push.
    """
    selected_roots: set[str] = set()
    shell_root: Path | None = None
    repository_env_changed = False
    for segment in _shell_segments(command):
        raw_tokens = _tokenise(segment)
        tokens = _strip_prefix(raw_tokens)
        if not tokens:
            continue
        if any(_program(token) == "env" for token in raw_tokens) and any(
            token.startswith("-C")
            or token == "--chdir"
            or token.startswith("--chdir=")
            for token in raw_tokens
        ):
            return None
        segment_changes_repository_env = any(
            ASSIGNMENT.match(token)
            and token.split("=", 1)[0] in GIT_REPOSITORY_ENV
            for token in raw_tokens
        )
        program = _program(tokens[0]).lstrip("(")
        if program == "export" and any(
            token.split("=", 1)[0] in GIT_REPOSITORY_ENV
            for token in tokens[1:]
        ):
            segment_changes_repository_env = True
        repository_env_changed = (
            repository_env_changed or segment_changes_repository_env
        )
        if program in {"cd", "pushd"}:
            directory_args = [
                token for token in tokens[1:]
                if token != "--" and not token.startswith("-")
            ]
            if len(directory_args) != 1:
                return None
            candidate = Path(directory_args[0])
            if candidate.is_absolute():
                shell_root = candidate
            elif shell_root is not None:
                shell_root = shell_root / candidate
            else:
                return None
            if not shell_root.is_dir():
                return None
            continue
        if program == "popd":
            return None
        if program == "eval" and is_push_command(" ".join(tokens[1:])):
            return None
        if program in SHELL_PROGRAMS and "-c" in tokens[1:]:
            index = tokens.index("-c")
            if index + 1 < len(tokens) and is_push_command(tokens[index + 1]):
                return None
        if any(_program(token) == "xargs" for token in raw_tokens) and is_push_command(segment):
            return None
        if program == "gh" and is_push_command(segment):
            if repository_env_changed or any(
                token.startswith("-R")
                or token == "--repo"
                or token.startswith("--repo=")
                for token in tokens[1:]
            ):
                return None
            root = shell_root if shell_root is not None else Path(fallback)
            selected_roots.add(str(root.resolve()))
            continue
        if program != "git" or _subcommand(tokens[1:], GIT_VALUE_OPTIONS) != "push":
            continue
        if repository_env_changed:
            return None
        selected = shell_root
        index = 1
        while index < len(tokens):
            token = tokens[index]
            if token == "-C":
                if index + 1 >= len(tokens):
                    return None
                candidate = Path(tokens[index + 1])
                if candidate.is_absolute():
                    selected = candidate
                elif selected is not None:
                    selected = selected / candidate
                else:
                    return None
                index += 2
                continue
            if token.startswith("-C") or token in {"--git-dir", "--work-tree"}:
                return None
            if token.startswith("--git-dir=") or token.startswith("--work-tree="):
                return None
            if token in GIT_VALUE_OPTIONS:
                index += 2
                continue
            if token.startswith("-"):
                index += 1
                continue
            break
        root = selected if selected is not None else Path(fallback)
        if not root.is_dir():
            return None
        selected_roots.add(str(root.resolve()))
    if len(selected_roots) > 1:
        return None
    return next(iter(selected_roots)) if selected_roots else None


CANONICAL_PUSH_FLAGS = ["--no-follow-tags", "--recurse-submodules=no", "-u", "--no-verify"]


SAFE_REMOTE = re.compile(r"[A-Za-z0-9][A-Za-z0-9._-]*")


def quote_all_shell_token(token: str) -> str:
    """Render one argv token without leaving any shell expansion position."""
    return "'" + token.replace("'", "'\"'\"'") + "'"


def render_quote_all(tokens: list[str]) -> str:
    return " ".join(quote_all_shell_token(token) for token in tokens)


def canonical_git_push(
    command: str, fallback: str
) -> tuple[Path | None, str | None, str | None]:
    """Validate the complete shell bytes for the one supported Git push."""
    trusted = shutil.which("git")
    if not trusted:
        return None, None, "the hook environment has no trusted Git executable"
    trusted_git = str(Path(trusted).resolve())
    try:
        tokens = shlex.split(command, posix=True)
    except ValueError as exc:
        return None, None, f"the Git push command has malformed quoting: {exc}"
    if command != render_quote_all(tokens):
        return None, None, "the entire Git push command must use canonical quote-all rendering"
    if len(tokens) < 2 or tokens[0] != "command":
        return None, None, "the Git push must begin with the standard command builtin"
    if tokens[1] != trusted_git or not Path(tokens[1]).is_absolute():
        return None, None, f"the Git executable must be the trusted absolute path {trusted_git!r}"

    index = 2
    selected = Path(fallback)
    if index < len(tokens) and tokens[index] == "-C":
        if index + 1 >= len(tokens) or not Path(tokens[index + 1]).is_absolute():
            return None, None, "Git -C must name the selected repository by absolute path"
        selected = Path(tokens[index + 1])
        index += 2
    try:
        repo = repo_root(selected.resolve())
    except UsageError as exc:
        return None, None, str(exc)
    if "-C" in tokens[1:index] and selected.resolve() != repo.resolve():
        return None, None, "Git -C must name the selected repository root exactly"

    required = ["push", *CANONICAL_PUSH_FLAGS]
    if tokens[index:index + len(required)] != required:
        return None, None, (
            "Git push must use exactly --no-follow-tags --recurse-submodules=no -u --no-verify"
        )
    tail = tokens[index + len(required):]
    if len(tail) != 2:
        return None, None, "Git push must name one literal remote and one explicit refspec"
    remote, refspec = tail
    if not SAFE_REMOTE.fullmatch(remote):
        return None, None, f"Git push remote {remote!r} is not a safe literal name"
    if remote != "origin":
        return None, None, "the Git push remote must be literal 'origin'"

    head = git_text(repo, "rev-parse", "HEAD")
    branch = git_maybe(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    if not branch:
        return None, None, "the selected repository has no current symbolic branch"
    expected = f"{head}:refs/heads/{branch}"
    if refspec != expected:
        return None, None, f"Git push refspec must be exactly {expected!r}, got {refspec!r}"
    return repo, head, None
