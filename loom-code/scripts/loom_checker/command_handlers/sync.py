"""`sync-trunk`: bring the change branch up to date with the remote trunk
before closing review dispatches reviewers (rule `review.sync`).

The attestation digest covers the whole tree, so a merge after review
invalidates it; this runs first. Merge only -- never rebase, never force --
so pushed history is never rewritten, and a conflict is aborted and named,
never resolved.
"""
from __future__ import annotations

from loom_checker.command_handlers.land import _git_reason
from loom_checker.command_handlers.publish import resolve_publish_executable
from loom_checker.helpers import TRUNK_BRANCH_NAMES
from loom_checker.helpers import TRUNK_CANDIDATES
from loom_checker.helpers import UsageError
from loom_checker.helpers import repo_root
from pathlib import Path
import os
import subprocess
import sys


# Manual pages this module relies on:
# git merge --no-edit / --abort: https://git-scm.com/docs/git-merge
# git merge-base --is-ancestor exit codes: https://git-scm.com/docs/git-merge-base
# git diff --diff-filter=U (unmerged paths): https://git-scm.com/docs/git-diff


RULE = "review.sync"
SYNC_READ_TIMEOUT = 30
SYNC_WRITE_TIMEOUT = 300
ORIGIN_HEAD = "refs/remotes/origin/HEAD"


def _git(git: str, repo: Path, *args: str, timeout: int = SYNC_READ_TIMEOUT) -> tuple[int | None, str, str]:
    """(returncode or None when it could not run, stdout, failure detail).
    A credential prompt would hang an agent, so the terminal prompt is off."""
    env = {**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    try:
        result = subprocess.run(
            [git, "-C", str(repo), *args], capture_output=True, timeout=timeout,
            env=env, text=True, encoding="utf-8", errors="surrogateescape",
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, "", f"{type(exc).__name__}: {exc}"
    detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
    return result.returncode, result.stdout, detail


def _oid(git: str, repo: Path, ref: str) -> str | None:
    code, stdout, _detail = _git(git, repo, "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}")
    return stdout.strip() if code == 0 and stdout.strip() else None


def _trunk_name(git: str, repo: Path) -> str | None:
    """origin/HEAD's target, else the first local trunk candidate -- no network."""
    code, stdout, _detail = _git(git, repo, "symbolic-ref", "--quiet", ORIGIN_HEAD)
    prefix = "refs/remotes/origin/"
    if code == 0 and stdout.strip().startswith(prefix):
        return stdout.strip()[len(prefix):]
    for candidate in TRUNK_CANDIDATES:
        name = candidate.removeprefix("origin/")
        if name not in TRUNK_BRANCH_NAMES:
            continue
        ref = f"refs/remotes/{candidate}" if candidate.startswith("origin/") else f"refs/heads/{name}"
        if _oid(git, repo, ref):
            return name
    return None


def _status(git: str, repo: Path) -> str | None:
    code, stdout, _detail = _git(git, repo, "status", "--porcelain", "-z", "--untracked-files=all")
    return stdout if code == 0 else None


def _block(err, *reasons: str) -> int:
    for reason in reasons:
        err.write(f"BLOCK {RULE}: {reason}\n")
    return 1


def cmd_sync_trunk(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    if args:
        raise UsageError("sync-trunk takes no arguments; run it from the change worktree.")
    git = resolve_publish_executable("git")
    if not git:
        raise UsageError("sync-trunk: no trusted git executable found in the host install roots.")
    repo = repo_root(Path.cwd())

    # Refusals: nothing below this block may run until every one has passed.
    code, stdout, _detail = _git(git, repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    branch = stdout.strip() if code == 0 else ""
    if not branch:
        return _block(err, "HEAD is detached; switch to the change branch before syncing.")
    trunk = _trunk_name(git, repo)
    if trunk is None:
        tried = ", ".join([ORIGIN_HEAD, *(c for c in TRUNK_CANDIDATES if c != "@{upstream}")])
        return _block(err, f"no trunk name resolves in {repo} (tried {tried}).")
    if branch == trunk or branch in TRUNK_BRANCH_NAMES:
        return _block(err, f"HEAD is the trunk branch {branch!r}; sync runs on a change branch, never the trunk.")
    status = _status(git, repo)
    if status is None:
        return _block(err, f"cannot read the status of {repo}.")
    if status:
        paths = [entry[3:] for entry in status.split("\0") if len(entry) > 3]
        shown = ", ".join(paths[:5]) + (", ..." if len(paths) > 5 else "")
        return _block(err, f"the worktree has uncommitted or untracked changes ({shown}); commit or remove them first.")

    remote_ref = f"refs/remotes/origin/{trunk}"
    code, _stdout, detail = _git(
        git, repo, "fetch", "--no-tags", "origin", f"+refs/heads/{trunk}:{remote_ref}",
        timeout=SYNC_WRITE_TIMEOUT,
    )
    tip = _oid(git, repo, remote_ref) if code == 0 else None
    if tip is None:
        reason = detail if code is None else _git_reason(detail, detail.splitlines()[-1] if detail else "fetch failed")
        err.write(
            f"WARN {RULE}: could not fetch origin/{trunk}, so the branch could not be checked "
            f"against {trunk}: {reason}; continuing without syncing.\n"
        )
        return 0

    head = _oid(git, repo, "HEAD")
    code, _stdout, detail = _git(git, repo, "merge-base", "--is-ancestor", tip, "HEAD")
    if code == 0:
        out.write(
            f"sync-trunk: up to date -- {branch} ({head}) already contains origin/{trunk} ({tip}); "
            "no commit added.\n"
        )
        return 0
    if code != 1 or head is None:
        return _block(err, f"cannot compare HEAD with origin/{trunk}: {detail}")

    code, _stdout, detail = _git(
        git, repo, "merge", "--no-edit", f"origin/{trunk}", timeout=SYNC_WRITE_TIMEOUT
    )
    if code == 0:
        new_head = _oid(git, repo, "HEAD")
        out.write(f"sync-trunk: merged origin/{trunk} ({tip}) into {branch}; HEAD is now {new_head}.\n")
        out.write(
            "sync-trunk: content changed -- re-run the package suite and adversarial programs "
            "before dispatching reviewers.\n"
        )
        return 0

    _code, unmerged, _detail = _git(git, repo, "diff", "--name-only", "--diff-filter=U", "-z")
    conflicts = [path for path in unmerged.split("\0") if path]
    if _oid(git, repo, "MERGE_HEAD"):
        _git(git, repo, "merge", "--abort", timeout=SYNC_WRITE_TIMEOUT)
    reasons = [f"conflict: {path}" for path in conflicts]
    if not conflicts:
        reason = detail if code is None else _git_reason(detail, "merge failed")
        reasons.append(f"merging origin/{trunk} failed without a conflict: {reason}")
    if _oid(git, repo, "HEAD") == head and _status(git, repo) == "":
        reasons.append(
            f"the merge was aborted; {branch} is back at {head} with a clean worktree. "
            "Conflicts are never resolved automatically -- resolve them in a new build round."
        )
    else:
        reasons.append(
            f"the aborted merge did not restore {branch} to {head} with a clean worktree; "
            f"inspect {repo} by hand before anything else runs."
        )
    return _block(err, *reasons)
