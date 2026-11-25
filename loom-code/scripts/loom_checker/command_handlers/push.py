"""Shell feedback and explicitly installed native Git branch protection.

Direct Git merge, commit, or push on main/master is refused. A publication command's most
common shape earns one reminder line naming the branch's verification
status, every other shape is silent, and a failure inside that path allows
(spec 2026-09-22-publication-floor-moves-to-github REQ-4, REQ-12). The one
other refusal is an unreadable hook call: a missing, empty, malformed
or non-object payload exits 2.
"""
from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import current_branch
from loom_checker.helpers import git_maybe
from loom_checker.helpers import repo_root
from loom_checker.rule_checks.push import ASSIGNMENT
from loom_checker.rule_checks.push import _operator_segments
from loom_checker.rule_checks.push import _tokenise
from loom_checker.rule_checks.push import publication_kind
from loom_checker.verification import identify_change
from loom_checker.verification import missing_clause
from loom_checker.verification import missing_records
from loom_checker.verification import verification_status
from pathlib import Path
import json
import os
import sys
import subprocess


# Static, relocatable POSIX shell: no installed launcher or Python at runtime.
# These hooks do not intercept reset/rebase or fast-forward merges. Remote PR
# rules remain necessary; hooks are ordinary Git safeguards, not a security wall.
# Git's hook interface: https://git-scm.com/docs/githooks (DESCRIPTION,
# pre-commit, pre-merge-commit, pre-push). Git runs executable hooks from its
# hooks directory; a nonzero exit aborts the corresponding commit/merge/push.
# pre-push receives remote name/location as arguments and stdin lines containing
# <local-ref> <local-object-name> <remote-ref> <remote-object-name>, in that order.
NATIVE_HOOK = b'''#!/bin/sh
# loom managed native branch protection v1
fail() { printf 'loom: %s\\n' "$*" >&2; exit 1; }
owner=$(CDPATH= cd -P -- "$(dirname -- "$0")/.." && pwd -P) || exit 1
common=$(git rev-parse --git-common-dir) || exit 1
common=$(CDPATH= cd -P -- "$common" && pwd -P) || exit 1
[ "$owner" = "$common" ] || exit 0
default=$(git symbolic-ref -q refs/remotes/origin/HEAD) ||
    fail 'origin default metadata unavailable. Next: inspect origin, fetch, then git remote set-head origin -a.'
case "$default" in refs/remotes/origin/?*) ;; *) fail 'Invalid origin default. Next: inspect origin, fetch, then git remote set-head origin -a.' ;; esac
git check-ref-format "$default" >/dev/null 2>&1 &&
git rev-parse --verify "$default^{commit}" >/dev/null 2>&1 ||
    fail 'Invalid origin default commit. Next: inspect origin, fetch, then git remote set-head origin -a.'
default=${default#refs/remotes/origin/}
protected() { [ "$1" = main ] || [ "$1" = master ] || [ "$1" = "$default" ]; }
deny() { fail "Protected branch $1. Next: preserve your work on a feature branch or worktree and publish its PR."; }
case "${0##*/}" in
pre-push)
    while read -r local_ref local_oid remote_ref remote_oid; do
        case "$remote_ref" in refs/heads/*)
            branch=${remote_ref#refs/heads/}
            protected "$branch" && deny "$branch"
        esac
    done
    ;;
*)
    branch=$(git symbolic-ref -q HEAD) || exit 0
    case "$branch" in refs/heads/*) branch=${branch#refs/heads/} ;; *) exit 0 ;; esac
    protected "$branch" && deny "$branch"
    ;;
esac
exit 0
'''
NATIVE_NAMES = ("pre-commit", "pre-merge-commit", "pre-push")


def _native_git(repo: Path, *args: str) -> str:
    result = subprocess.run(["git", "-C", str(repo), *args], capture_output=True,
                            text=True, timeout=10)
    if result.returncode:
        raise ValueError(f"Git {' '.join(args)} unavailable. Next: inspect repository metadata and origin.")
    return result.stdout.strip()


def _native_hooks(install: bool, out, err) -> int:
    """Explicit adopter action; preflight every path before any mutation."""
    created: list[Path] = []
    removed: list[tuple[Path, int]] = []
    hooks = None
    made_directory = False
    try:
        repo = Path.cwd()
        override = subprocess.run(["git", "config", "--get-all", "core.hooksPath"],
                                  cwd=repo, capture_output=True, text=True)
        if override.returncode != 1:
            raise ValueError("core.hooksPath override present or unreadable. Next: integrate protection with the hook owner explicitly.")
        raw = Path(_native_git(repo, "rev-parse", "--git-common-dir"))
        common = raw if raw.is_absolute() else repo / raw
        # Reject symlinked parents as well as a symlinked hooks directory.
        common = common.absolute()
        if any(p.is_symlink() for p in (common, *common.parents)):
            raise ValueError("Symlinked Git directory. Next: integrate protection with the repository owner.")
        hooks = common / "hooks"
        if hooks.is_symlink() or (hooks.exists() and not hooks.is_dir()):
            raise ValueError("Foreign hooks location. Next: integrate protection with the hook owner.")
        paths = [hooks / name for name in NATIVE_NAMES]
        for path in paths:
            if path.is_symlink() or (path.exists() and
                    (not path.is_file() or path.stat().st_nlink != 1 or
                     path.read_bytes() != NATIVE_HOOK)):
                raise ValueError(f"Foreign or edited hook: {path}. Next: preserve it and arrange explicit hook-owner integration.")
        if install:
            local = _native_git(repo, "symbolic-ref", "refs/remotes/origin/HEAD")
            prefix = "refs/remotes/origin/"
            if not local.startswith(prefix) or not local[len(prefix):]:
                raise ValueError("Invalid origin default metadata.")
            remote_ref = "refs/heads/" + local[len(prefix):]
            _native_git(repo, "check-ref-format", remote_ref)
            _native_git(repo, "rev-parse", "--verify", local + "^{commit}")
            live = _native_git(repo, "ls-remote", "--symref", "origin", "HEAD")
            if f"ref: {remote_ref}\tHEAD" not in live.splitlines():
                raise ValueError("Live origin default is unavailable or conflicts with local metadata.")
            if not hooks.exists():
                hooks.mkdir()
                made_directory = True
            for path in paths:
                if not path.exists():
                    with path.open("xb") as stream:
                        created.append(path)
                        stream.write(NATIVE_HOOK)
                    path.chmod(0o755)
                elif not os.access(path, os.X_OK):
                    raise ValueError(f"Managed hook is not executable: {path}.")
        else:
            for path in paths:
                if path.exists():
                    mode = path.stat().st_mode & 0o777
                    path.unlink()
                    removed.append((path, mode))
        out.write("loom: native Git protection " + ("installed" if install else "removed") + ".\n")
        return 0
    except (OSError, ValueError, subprocess.SubprocessError) as exc:
        for path in created:
            path.unlink()
        for path, mode in removed:
            with path.open("xb") as stream:
                stream.write(NATIVE_HOOK)
            path.chmod(mode)
        if made_directory and hooks is not None:
            hooks.rmdir()
        err.write(f"loom: {exc} Next: inspect origin; fetch and git remote set-head origin -a when metadata needs repair.\n")
        return 2


def read_hook_payload(stdin=sys.stdin) -> dict | None:
    """PreToolUse payload (Claude Code and Codex share the shape) when the
    checker is invoked as a hook; None when run from a terminal or with an
    empty stdin. Malformed JSON or a non-object payload is a UsageError →
    exit 2."""
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
    if list(args) in (["--install-git-hooks"], ["--remove-git-hooks"]):
        return _native_hooks(args[0] == "--install-git-hooks", out, err)
    if list(args) != ["--hook"]:
        raise UsageError("push expects --hook, --install-git-hooks or --remove-git-hooks.")

    payload = read_hook_payload()
    if payload is None:
        raise UsageError("push --hook expects a PreToolUse JSON payload on stdin.")
    command = str((payload.get("tool_input") or {}).get("command", ""))
    cwd = Path(str(payload.get("cwd") or os.getcwd()))
    if _protect_main(command, cwd):
        err.write("loom: direct git merge, commit, or push on main/master is blocked. "
                  "Next: preserve your work on a feature branch or worktree and open its PR.\n")
        return 2
    kind = publication_kind(command)
    if kind is None:
        return 0
    try:
        line = _reminder(kind, cwd)
    except Exception as exc:  # a reminder that cannot be computed never blocks
        line = f"loom: push hook failed ({exc}); allowing."
    if line:
        _emit(line, out, err)
    return 0


PROTECTED = {"main", "master"}
# Git global options that take their value as the next word (git(1) OPTIONS).
GIT_VALUE_OPTIONS = {"-c", "--git-dir", "--work-tree", "--namespace", "--super-prefix", "--config-env"}
PUSH_VALUE_OPTIONS = {"--repo", "-o", "--push-option", "--receive-pack", "--exec"}


def _resolve(base: Path | None, target: str) -> Path | None:
    """`target` read from `base`; None when it is not an existing directory."""
    if base is None:
        return None
    path = base / Path(target).expanduser()
    return path if path.is_dir() else None


def _protect_main(command: str, cwd: Path) -> bool:
    """Each simple command of the text, read in order: a `cd <dir>` moves the
    effective directory, `git -C <dir>` moves it for that call, and a Git
    commit, merge or push on main/master there, or a push whose destination
    is main/master from any branch, is refused. A directory that cannot be
    resolved leaves that command unjudged; `bash -c`, scripts and other
    wrappers stay outside the guard."""
    here: Path | None = cwd
    for segment in _operator_segments(command):
        tokens = _tokenise(segment)
        while tokens and ASSIGNMENT.match(tokens[0]):
            tokens = tokens[1:]
        if tokens[:1] == ["cd"]:
            rest = [t for t in tokens[1:] if t not in {"-P", "-L", "-e", "--"}]
            here = _resolve(here, rest[0] if rest else "~") if rest[:1] != ["-"] else None
        elif tokens[:1] == ["git"] and _git_on_main(tokens[1:], here):
            return True
    return False


def _git_on_main(args: list[str], where: Path | None) -> bool:
    index = 0
    while index < len(args) and args[index].startswith("-"):
        if args[index] == "-C" and index + 1 < len(args):
            where = _resolve(where, args[index + 1])
        index += 2 if args[index] in GIT_VALUE_OPTIONS | {"-C"} else 1
    verb, rest = (args[index], args[index + 1:]) if index < len(args) else ("", [])
    if verb not in {"merge", "commit", "push"} or where is None:
        return False
    # https://git-scm.com/docs/git-config (--local limits scope; --bool normalizes false values)
    if git_maybe(where, "config", "--local", "--bool", "--get", "loom.protectMain") == "false":
        return False
    branch = current_branch(where)
    if branch in PROTECTED:
        return True
    if verb == "push" and "--mirror" in rest:
        return True
    # --all pushes every local branch, so a local main/master reaches the remote one.
    if verb == "push" and "--all" in rest and any(
            git_maybe(where, "rev-parse", "--verify", "--quiet", f"refs/heads/{name}")
            for name in PROTECTED):
        return True
    return verb == "push" and any(_branch_name(dst, branch) in PROTECTED
                                  for dst in _push_destinations(rest))


def _push_destinations(args: list[str]) -> list[str]:
    """Destination side of each refspec after the remote (git-push(1) <refspec>)."""
    positional: list[str] = []
    skip = False
    for arg in args:
        if skip:
            skip = False
        elif arg in PUSH_VALUE_OPTIONS:
            skip = True
        elif not arg.startswith("-"):
            positional.append(arg)
    return [spec.lstrip("+").rsplit(":", 1)[-1] for spec in positional[1:]]


def _branch_name(ref: str, branch: str | None) -> str:
    if ref == "HEAD":
        return branch or ""
    return ref[len("refs/heads/"):] if ref.startswith("refs/heads/") else ref


def _reminder(kind: str, cwd: Path) -> str | None:
    """The one line a direct push, PR create or PR merge earns, or None."""
    repo = repo_root(cwd)
    change_id, _unidentified = identify_change(repo)
    status = verification_status(repo, change_id) if change_id else None
    clause = missing_clause(missing_records(repo, change_id, status)) if change_id else ""
    clause = f" {clause}" if clause else ""
    if kind == "merge":
        return f"loom: this merges outside loom_checker.py land{clause}; merging anyway."
    if change_id is None:
        return "loom: change not identified (no intent for this branch); proceeding."
    if status == "valid":
        return None
    return f"loom: verification {status}{clause}; proceeding."


def _emit(line: str, out, err) -> None:
    """Claude Code reads a PreToolUse `systemMessage` from stdout; Codex and
    a terminal read stderr."""
    out.write(json.dumps({"systemMessage": line}, ensure_ascii=False) + "\n")
    err.write(line + "\n")
