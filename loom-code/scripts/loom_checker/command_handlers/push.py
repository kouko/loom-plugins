from __future__ import annotations

from loom_checker.attestation import validate_attestation
from loom_checker.helpers import UsageError
from loom_checker.helpers import changed_paths
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_text
from loom_checker.helpers import glob_to_regex
from loom_checker.helpers import load_manifest
from loom_checker.helpers import repo_root
from loom_checker.helpers import report
from loom_checker.rule_checks.push import SHELL_PROGRAMS
from loom_checker.rule_checks.push import _program
from loom_checker.rule_checks.push import _shell_segments
from loom_checker.rule_checks.push import _strip_prefix
from loom_checker.rule_checks.push import _tokenise
from loom_checker.rule_checks.push import canonical_git_push
from loom_checker.rule_checks.push import canonical_pr_create_repo
from loom_checker.rule_checks.push import check_pr_create_remote_head
from loom_checker.rule_checks.push import git_dash_c_push_cwd
from loom_checker.rule_checks.push import is_git_push_command
from loom_checker.rule_checks.push import is_pr_create_command
from loom_checker.rule_checks.push import is_pr_merge_command
from loom_checker.rule_checks.push import is_push_command
from loom_checker.rule_checks.push import quote_all_shell_token
from loom_checker.rule_checks.selection_guard import FILE_TOOLS as SELECTION_GUARD_FILE_TOOLS
from loom_checker.rule_checks.selection_guard import RULE_ID as SELECTION_GUARD_RULE
from loom_checker.rule_checks.selection_guard import guard_reason as selection_guard_reason
from pathlib import Path
import io
import json
import os
import re
import shutil
import sys


# The two legal routes out of a publication blocked for a missing attestation,
# appended to the reason that blocks it. One copy, because `land` refuses the
# merge at its own earlier site and appends this same text there: a caller must
# read the same routes wherever the block lands.
#
# One line, and no leading newline: report() writes one `BLOCK <rule>: <reason>`
# line per failure and every caller parses that prefix, so a wrapped reason
# would emit continuation lines that no longer carry it.
PUBLICATION_ROUTES = (
    "; two legal routes, both run by the agent: run the closing-review station,"
    " which generates the attestation, or propose a step selection"
    " (`loom_checker.py selection propose <change-id> --origin agent`) that the user"
    " confirms by typing the code, after which finalize-review drops the reviewer"
    " floor to zero and still emits an attestation recording the skip;"
    " never hand this command to the user to run"
)


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
    rest = list(args)
    if "--hook" not in rest:
        return _cmd_push(rest, out, err)
    rest.remove("--hook")

    payload = read_hook_payload()
    if payload is None:
        raise UsageError("push --hook expects a PreToolUse JSON payload on stdin.")
    # The record-store guard judges every matched tool call first.
    guard_reason = selection_guard_reason(payload)
    if guard_reason:
        print(f"BLOCK {SELECTION_GUARD_RULE}: {guard_reason}", file=err)
        return 2
    if payload.get("tool_name") in SELECTION_GUARD_FILE_TOOLS:
        return 0
    # The matcher is the tool name, so every Bash command arrives here; only
    # push-shaped commands are judged.
    command = str((payload.get("tool_input") or {}).get("command", ""))
    if contains_pr_merge(command):
        # `land` runs its own merge as a subprocess, never as a Bash tool
        # call, so refusing here leaves exactly one merge path.
        print(
            "BLOCK push.merge: merge through loom_checker.py land --accepted-by <name>",
            file=err,
        )
        return 2
    canonical_pr_repo = canonical_pr_create_repo(command)
    push_shaped = canonical_pr_repo is not None or is_push_command(command)
    git_push = is_git_push_command(command)
    malformed_canonical_push = False
    if not push_shaped:
        # A malformed quote can defeat the permissive recogniser, but not a
        # command that visibly starts with the canonical command trust root
        # and trusted executable.
        trusted = shutil.which("git")
        trusted_prefix = (
            f"{quote_all_shell_token('command')} "
            f"{quote_all_shell_token(str(Path(trusted).resolve()))}"
            if trusted
            else ""
        )
        malformed_canonical_push = bool(
            trusted_prefix
            and command.startswith(trusted_prefix)
            and quote_all_shell_token("push") in command
        )
        if not malformed_canonical_push:
            return 0
    cwd = str(payload.get("cwd") or os.getcwd())
    if git_push or malformed_canonical_push:
        repo, immutable_head, refspec_error = canonical_git_push(command, cwd)
        if refspec_error:
            # The push stays blocked either way; a missing or invalid
            # attestation is named first because it is what the user must fix.
            print(attestation_reason(command, cwd, rest), end="", file=err)
            print(f"BLOCK push.attestation: {refspec_error}", file=err)
            return 2
        assert repo is not None and immutable_head is not None
        os.chdir(repo)
        rc = _cmd_push(["--head", immutable_head, "--require-live-head"] + rest, out, err)
        return 2 if rc == 1 else rc

    # A metadata-only PR create carries its own function-proof repository
    # selection. Other gh actions keep the existing conservative parser.
    pr_create = canonical_pr_repo is not None or is_pr_create_command(command)
    if pr_create and canonical_pr_repo is None:
        print(
            "BLOCK push.attestation: PR creation must use the canonical "
            "trusted-gh command from loom-code:ship",
            file=err,
        )
        return 2
    push_cwd = str(canonical_pr_repo) if canonical_pr_repo else git_dash_c_push_cwd(command, cwd)
    if push_cwd is None:
        print(
            "BLOCK push.attestation: ambiguous repository selection; "
            "use one absolute git -C path, or cd to one absolute path first",
            file=err,
        )
        return 2
    os.chdir(push_cwd)
    if pr_create:
        remote_error = check_pr_create_remote_head(Path.cwd(), command)
        if remote_error:
            print(f"BLOCK push.attestation: {remote_error}", file=err)
            return 2
    rc = _cmd_push(rest, out, err)
    if pr_create and rc == 0:
        remote_error = check_pr_create_remote_head(Path.cwd(), command)
        if remote_error:
            print(f"BLOCK push.attestation: {remote_error}", file=err)
            return 2
    return 2 if rc == 1 else rc


# Word separators for the merge text rule: whitespace, quotes and shell
# punctuation, so `(gh`, `'gh'`, `{ gh` and `then gh` all yield the word `gh`;
# `$` separates too, so ANSI-C `$'merge'` and locale `$"merge"` yield `merge`.
MERGE_TEXT_WORD = re.compile(r"[^\s'\"`;|&(){}<>!$]+")


def mentions_pr_merge(command: str) -> bool:
    """Fail-closed text rule: after joining backslash-newlines, a word `gh`
    (or a path ending in `/gh`) followed later by the consecutive words `pr`
    `merge`, case-insensitively, anywhere in the command text.

    It ignores wrappers, options and shell grammar, so `sudo -u x`, `bash -lc`,
    `( … )`, `if … then` and `xargs -n1` cannot hide a merge. Ceiling: it also
    refuses commands that merely mention the words (`echo gh pr merge`, a
    search pattern, a commit message) — accepted, because `land` is the only
    merge path and a false refusal costs a rewording. It does not see a merge
    assembled at run time (`printf`, variables, `gh api …/merge`)."""
    words = [
        word.lower()
        for word in MERGE_TEXT_WORD.findall(command.replace("\\\n", ""))
    ]
    for index, word in enumerate(words):
        if word != "gh" and not word.endswith("/gh"):
            continue
        tail = words[index + 1:]
        if any(
            tail[i] == "pr" and tail[i + 1] == "merge"
            for i in range(len(tail) - 1)
        ):
            return True
    return False


def contains_pr_merge(command: str) -> bool:
    """True when the fail-closed text rule matches, or a segment merges a PR
    directly or inside the `eval` and `<shell> -c` forms `is_push_command`
    unwraps."""
    if mentions_pr_merge(command) or is_pr_merge_command(command):
        return True
    for segment in _shell_segments(command):
        tokens = _strip_prefix(_tokenise(segment))
        if not tokens:
            continue
        program = _program(tokens[0])
        if program == "eval" and contains_pr_merge(" ".join(tokens[1:])):
            return True
        if program in SHELL_PROGRAMS and "-c" in tokens[1:]:
            index = tokens.index("-c")
            if index + 1 < len(tokens) and contains_pr_merge(tokens[index + 1]):
                return True
    return False


def attestation_reason(command: str, cwd: str, rest: list[str]) -> str:
    """BLOCK lines for the target branch's attestation, read-only and without
    replay; "" when it is valid or the repository cannot be determined
    safely, so the caller's own refusal stands alone (fail closed).

    The reported attestation state reflects the target repository's
    checked-out HEAD, not necessarily the ref being pushed; the push stays
    blocked either way."""
    target = git_dash_c_push_cwd(command, cwd)
    if target is None:
        return ""
    buffer = io.StringIO()
    previous = os.getcwd()
    try:
        os.chdir(target)
        rc = _cmd_push(list(rest), io.StringIO(), buffer)
    except Exception:  # any doubt keeps today's single refusal
        return ""
    finally:
        os.chdir(previous)
    return buffer.getvalue() if rc == 1 else ""


def _cmd_push(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    head = "HEAD"
    require_live_head = False
    rest = list(args)
    while rest:
        token = rest.pop(0)
        if token == "--head":
            if not rest:
                raise UsageError("--head needs a ref.")
            head = rest.pop(0)
        elif token == "--require-live-head":
            require_live_head = True
        else:
            raise UsageError(f"unexpected argument {token!r}.")

    manifest = load_manifest()
    repo = repo_root(Path.cwd())
    head_sha = git_maybe(repo, "rev-parse", head)
    if not head_sha:
        raise UsageError(f"cannot resolve {head!r} in {repo}.")

    # The 1.1 publication path reads one generated attestation from the
    # branch delta. It validates content identity and recorded outcomes but
    # deliberately does not replay functional executables.
    attestation_template = manifest.get("artifacts", {}).get("attestation", {}).get("path")
    if not attestation_template:
        raise UsageError("contract manifest declares no attestation artifact.")
    matcher = glob_to_regex(attestation_template.replace("<change-id>", "*"))
    candidates = sorted(path for path in changed_paths(repo) if matcher.fullmatch(path))
    if len(candidates) != 1:
        # The existing reason stays at the front; PUBLICATION_ROUTES only names
        # the way out, because the refusal alone left the agent nothing to do
        # but hand the blocked command back to the user.
        return report([(
            "push.attestation",
            f"branch must carry exactly one generated attestation; found {len(candidates)}"
            + PUBLICATION_ROUTES,
        )], err)
    attestation_rel = candidates[0]
    match = re.fullmatch(
        re.escape(attestation_template).replace(re.escape("<change-id>"), r"(?P<change_id>[^/]+)"),
        attestation_rel,
    )
    if match is None:
        return report([("push.attestation", "cannot derive change id from attestation path")], err)
    try:
        attestation = json.loads(git_text(repo, "show", f"{head_sha}:{attestation_rel}"))
    except (UsageError, json.JSONDecodeError) as exc:
        return report([("push.attestation", f"cannot read generated attestation: {exc}")], err)
    failures = validate_attestation(
        repo, head_sha, match.group("change_id"), attestation, manifest
    )
    if require_live_head and git_text(repo, "rev-parse", "HEAD") != head_sha:
        failures.append(("push.attestation", "live HEAD moved during publication validation"))
    return report(failures, err)
