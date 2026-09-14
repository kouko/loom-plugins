from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from loom_checker.command_handlers.publish import PUBLISH_CI_PENDING_WAITS
from loom_checker.command_handlers.publish import PUBLISH_CI_POLL_SECONDS
from loom_checker.command_handlers.publish import PUBLISH_CI_REGISTRATION_WAITS
from loom_checker.command_handlers.publish import PUBLISH_REDIRECT_ENV
from loom_checker.command_handlers.publish import _publication_change_id
from loom_checker.command_handlers.publish import _publish_env
from loom_checker.command_handlers.publish import _publish_origin_state
from loom_checker.command_handlers.publish import resolve_publish_executable
from loom_checker.command_handlers.push import _cmd_push
from loom_checker.helpers import UsageError
from loom_checker.helpers import artifact_path
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_ok
from loom_checker.helpers import git_text
from loom_checker.helpers import load_manifest
from loom_checker.helpers import repo_root
from loom_checker.helpers import report
from loom_checker.parsing import parse_document
from loom_checker.rule_checks.push import github_repo_from_origin
from pathlib import Path
from urllib.parse import quote
import json
import os
import re
import subprocess
import sys
import tempfile
import time


LAND_READ_TIMEOUT = 30


# Reserved for gh pr merge, git fetch, git push and git worktree remove.
LAND_WRITE_TIMEOUT = 300


LAND_MERGE_STATE_WAITS = 6  # re-read UNKNOWN for up to 60 seconds


BLOCKING_MERGE_STATES = {"BLOCKED", "DIRTY", "BEHIND", "UNSTABLE"}


ACCEPTANCE_NOT_RECORDED = (
    "blind-run acceptance not recorded; pass --accepted-by <name> after the maintainer accepts"
)


def run_land_external(argv: list[str], timeout: int, **kwargs) -> subprocess.CompletedProcess:
    """Run one trusted land argv; kept as a seam for isolated tests."""
    return subprocess.run(argv, capture_output=True, text=True, timeout=timeout, **kwargs)


wait_land_interval = time.sleep


@dataclass(frozen=True)
class LandTarget:
    """Everything the merge step needs once the preconditions hold."""

    repo: Path
    head: str
    branch: str
    base: str
    identity: str
    number: int
    trusted_git: str
    trusted_gh: str
    env: dict[str, str]


def _usage(reason: str, err) -> int:
    err.write(f"land: {reason}\n")
    return 2


def _block(reason: str, err) -> int:
    return report([("land.merge", reason)], err)


def _land_args(args: list[str]) -> tuple[str, str | None] | str:
    """Return (form, value) for one of the three forms, or a usage error."""
    rest = list(args)
    form: str | None = None
    value: str | None = None
    confirm: str | None = None
    while rest:
        token = rest.pop(0)
        if token in {"--accepted-by", "--cleanup", "--confirm"}:
            if not rest or not rest[0].strip():
                return f"{token} needs a value"
            operand = rest.pop(0)
            if token == "--confirm":
                if confirm is not None:
                    return "--confirm may appear only once"
                confirm = operand
                continue
        elif token == "--sweep":
            operand = None
        else:
            return f"unexpected argument {token!r}"
        if form is not None:
            return "use exactly one of --accepted-by, --cleanup, or --sweep"
        form, value = token, operand
    if confirm is not None and form != "--sweep":
        return "--confirm applies only to --sweep"
    return form or "--accepted-by", value


def cmd_land(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Land one accepted change: merge preconditions, then the merge."""
    parsed = _land_args(args)
    if isinstance(parsed, str):
        return _usage(parsed, err)
    form, accepted_by = parsed
    if form != "--accepted-by":
        return _usage(f"{form} is not implemented yet", err)

    redirected = sorted(
        key for key in os.environ
        if key in PUBLISH_REDIRECT_ENV
        or key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_")
    )
    if redirected:
        return _usage(
            "remove repository or host redirect environment variables: "
            + ", ".join(redirected), err,
        )
    trusted_git = resolve_publish_executable("git")
    trusted_gh = resolve_publish_executable("gh")
    if not trusted_git or not trusted_gh:
        return _block("land requires trusted git and gh executables", err)

    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = os.pathsep.join(dict.fromkeys(
        [str(Path(trusted_git).parent), str(Path(trusted_gh).parent), "/usr/bin", "/bin"]
    ))
    try:
        return _land_accepted(accepted_by, trusted_git, trusted_gh, out, err)
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path


def _land_accepted(
    accepted_by: str | None, trusted_git: str, trusted_gh: str, out, err
) -> int:
    target = _merge_preconditions(accepted_by, trusted_git, trusted_gh, out, err)
    if isinstance(target, int):
        return target
    merged = _squash_merge(target, accepted_by, err)
    if merged is None:
        return 1
    merge_commit, title, body = merged
    out.write(f"Merged PR #{target.number} as {merge_commit[:7]}\n")
    if _verify_merge(target, merge_commit, title, body, err) != 0:
        return 1
    return _sync_and_clean(target, out, err)


def _sync_and_clean(target: LandTarget, out, err) -> int:
    """After a verified merge: fast-forward the trunk, then clean up the
    invoking worktree's change (spec 'Which worktree path')."""
    sync_trunk(target, out)
    return cleanup_change(target, out, err, worktree=target.repo)


REGENERABLE_IGNORED = {
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", ".venv",
    "node_modules", ".DS_Store",
}


@dataclass(frozen=True)
class Worktree:
    path: Path
    branch: str | None  # the porcelain `branch` field, e.g. refs/heads/main


@dataclass(frozen=True)
class CleanupPlan:
    """What cleanup of one change would do, once every precondition held."""

    branch: str
    head: str
    main: Path
    anchor: Path
    worktree: Path | None  # linked worktree to remove
    in_main: bool  # the branch is checked out in the main worktree
    local: bool
    remote: bool


def _cleanup_block(reason: str, err) -> int:
    return report([("land.cleanup", reason)], err)


def _git_run(
    target: LandTarget, where: Path, *args: str, timeout: int = LAND_READ_TIMEOUT
) -> tuple[int | None, str, str]:
    """(returncode or None when it could not run, stdout, failure detail)."""
    try:
        result = run_land_external(
            [target.trusted_git, "-C", str(where), *args], timeout,
            cwd=where, env=target.env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return None, "", f"{type(exc).__name__}: {exc}"
    detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
    return result.returncode, result.stdout, detail


def _worktrees(target: LandTarget, where: Path) -> tuple[list[Worktree], Path] | str:
    """(porcelain worktree entries, main worktree) or a failure reason."""
    code, stdout, detail = _git_run(target, where, "worktree", "list", "--porcelain", "-z")
    if code != 0:
        return f"cannot list worktrees: {detail}"
    entries: list[Worktree] = []
    path: Path | None = None
    branch: str | None = None
    for field in stdout.split("\0"):
        if field.startswith("worktree "):
            path, branch = Path(field[len("worktree "):]).resolve(), None
        elif field.startswith("branch "):
            branch = field[len("branch "):]
        elif not field and path is not None:
            entries.append(Worktree(path, branch))
            path = None
    code, stdout, detail = _git_run(
        target, where, "rev-parse", "--path-format=absolute", "--git-common-dir"
    )
    if code != 0:
        return f"cannot find the main worktree: {detail}"
    main = Path(stdout.strip()).resolve().parent
    if not entries or entries[0].path != main:
        return f"main worktree {main} is not the first worktree entry"
    return entries, main


def _tip(target: LandTarget, where: Path, ref: str) -> str | None | tuple[str]:
    """The ref's oid, None when absent, or a 1-tuple failure reason."""
    code, stdout, detail = _git_run(target, where, "rev-parse", "--verify", "--quiet", ref)
    if code == 0:
        return stdout.strip()
    if code == 1 and not stdout.strip():
        return None
    return (f"cannot read {ref}: {detail}",)


def _status_entries(target: LandTarget, where: Path, *extra: str) -> list[str] | str:
    code, stdout, detail = _git_run(target, where, "status", "--porcelain", "-z", *extra)
    if code != 0:
        return f"cannot read the status of {where}: {detail}"
    return [entry for entry in stdout.split("\0") if entry]


def sync_trunk(target: LandTarget, out) -> None:
    """Spec 'Trunk sync': fast-forward only; a skipped sync never stops cleanup."""
    trunk = target.base
    listed = _worktrees(target, target.repo)
    if isinstance(listed, str):
        out.write(f"trunk not updated: {listed}\n")
        return
    entries, main = listed
    checkout = next((e.path for e in entries if e.branch == f"refs/heads/{trunk}"), None)
    if checkout is not None:
        status = _status_entries(target, checkout)
        if isinstance(status, str):
            out.write(f"trunk not updated: {status}\n")
            return
        if status:
            out.write(f"trunk not updated: {checkout} has local changes\n")
            return
        where = checkout
        code, _stdout, detail = _git_run(
            target, checkout, "merge", "--ff-only", f"origin/{trunk}", timeout=LAND_WRITE_TIMEOUT
        )
    else:
        where = main
        code, _stdout, detail = _git_run(
            target, main, "fetch", "origin", f"{trunk}:{trunk}", timeout=LAND_WRITE_TIMEOUT
        )
    if code != 0:
        out.write(f"trunk not updated: {detail}\n")
        return
    tip = _tip(target, where, f"refs/heads/{trunk}")
    shown = tip[:7] if isinstance(tip, str) else "an unreadable tip"
    out.write(f"Trunk {trunk} fast-forwarded to {shown}\n")


def plan_cleanup(
    target: LandTarget, *, worktree: Path | None = None, fetch: bool = True
) -> CleanupPlan | str:
    """Spec 'Cleanup preconditions, per change', read-only apart from
    `git fetch --prune origin` (skip it with fetch=False when the caller has
    already fetched). `target.head` is the merged PR's headRefOid.

    `worktree` is the invoking worktree's own top-level path (`--accepted-by`);
    None looks the worktree up by exact equality of the porcelain branch field.
    Returns the plan, or the refusal reason."""
    branch, head, ref = target.branch, target.head, f"refs/heads/{target.branch}"
    where = target.repo
    try:
        view = run_land_external(
            [target.trusted_gh, "pr", "view", str(target.number), "--json", "state,headRefOid"],
            LAND_READ_TIMEOUT, cwd=where, env=target.env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return f"PR state lookup could not run: {type(exc).__name__}: {exc}"
    if view.returncode != 0:
        return "PR state lookup failed: " + (
            view.stderr or view.stdout or f"exit {view.returncode}"
        ).strip()
    try:
        payload = json.loads(view.stdout)
        state = str(payload.get("state", "")).upper()
        pr_head = str(payload.get("headRefOid", ""))
    except (json.JSONDecodeError, AttributeError) as exc:
        return f"cannot decode PR state response: {exc}"
    if state != "MERGED":
        return f"PR #{target.number} is not merged ({state or 'UNKNOWN'})"
    if pr_head != head:
        return f"PR #{target.number} head {pr_head[:7]} is not {head[:7]}"

    if fetch:
        code, _stdout, detail = _git_run(
            target, where, "fetch", "--prune", "origin", timeout=LAND_WRITE_TIMEOUT
        )
        if code != 0:
            return f"cannot fetch origin: {detail}"
    local = _tip(target, where, ref)
    if isinstance(local, tuple):
        return local[0]
    if local is not None and local != head:
        return f"local branch tip {local[:7]} is not PR head {head[:7]}"
    remote = _tip(target, where, f"refs/remotes/origin/{branch}")
    if isinstance(remote, tuple):
        return remote[0]
    if remote is not None and remote != head:
        return f"remote branch tip {remote[:7]} is not PR head {head[:7]}"

    listed = _worktrees(target, where)
    if isinstance(listed, str):
        return listed
    entries, main = listed
    if worktree is not None:
        path = worktree.resolve()
        entry = next((e for e in entries if e.path == path), None)
        if entry is None or entry.branch != ref:
            return f"worktree {path} does not have {branch} checked out"
    else:
        entry = next((e for e in entries if e.branch == ref), None)
    trunk_checkout = next(
        (e.path for e in entries if e.branch == f"refs/heads/{target.base}"), None
    )
    in_main = entry is not None and entry.path == main
    if in_main:
        status = _status_entries(target, main)
        if isinstance(status, str):
            return status
        if status:
            return f"main worktree {main} has local changes"
        if trunk_checkout is not None:
            return f"trunk is checked out in {trunk_checkout}"
    elif entry is not None:
        status = _status_entries(target, entry.path)
        if isinstance(status, str):
            return status
        if status:
            kind = "untracked" if all(e.startswith("?? ") for e in status) else "modified"
            return f"worktree {entry.path} has {kind} files"
        # `matching` names each ignored path by the pattern it matched; the
        # default mode collapses a directory of only ignored files (pkg/).
        ignored = _status_entries(target, entry.path, "--ignored=matching")
        if isinstance(ignored, str):
            return ignored
        outside = sorted(
            name for name in (e[3:].rstrip("/") for e in ignored if e.startswith("!! "))
            if name.rsplit("/", 1)[-1] not in REGENERABLE_IGNORED and not name.endswith(".pyc")
        )
        if outside:
            return (f"worktree {entry.path} has ignored files outside the regenerable set: "
                    + ", ".join(outside))
    return CleanupPlan(
        branch=branch, head=head, main=main,
        anchor=trunk_checkout or main,
        worktree=entry.path if entry is not None and not in_main else None,
        in_main=in_main, local=local is not None, remote=remote is not None,
    )


def execute_cleanup(target: LandTarget, plan: CleanupPlan, out, err) -> int:
    """Spec 'Cleanup actions, in order', for a plan from `plan_cleanup`."""
    branch, anchor = plan.branch, plan.anchor
    removed = False

    def finish(code: int) -> int:
        if removed:
            quoted = str(anchor).replace("'", "'\\''")
            out.write(f"next: cd '{quoted}'\n")
        return code

    if plan.worktree is not None:
        try:
            cwd = Path.cwd().resolve()
        except OSError:
            cwd = None
        if cwd is None or cwd == plan.worktree or plan.worktree in cwd.parents:
            os.chdir(anchor)
        code, _stdout, detail = _git_run(
            target, anchor, "worktree", "remove", str(plan.worktree), timeout=LAND_WRITE_TIMEOUT
        )
        if code != 0:
            err.write(f"{detail}\n")
            return _cleanup_block(
                f"worktree removal interrupted at {plan.worktree}; "
                "run git worktree prune after checking the directory", err,
            )
        out.write(f"Removed worktree {plan.worktree}\n")
        removed = True
    elif plan.in_main:
        code, _stdout, detail = _git_run(target, plan.main, "switch", target.base)
        if code != 0:
            return _cleanup_block(f"cannot switch {plan.main} to {target.base}: {detail}", err)

    if plan.local:
        code, _stdout, detail = _git_run(
            target, anchor, "update-ref", "-d", f"refs/heads/{branch}", plan.head
        )
        if code != 0:
            return finish(_cleanup_block(f"local branch {branch} not deleted: {detail}", err))
        out.write(f"Deleted local branch {branch}\n")
        # An absent section exits non-zero; that is the state we want.
        _git_run(target, anchor, "config", "--remove-section", f"branch.{branch}")

    if plan.remote:
        code, _stdout, detail = _git_run(
            target, anchor, "push", f"--force-with-lease=refs/heads/{branch}:{plan.head}",
            "origin", f":refs/heads/{branch}", timeout=LAND_WRITE_TIMEOUT,
        )
        if code != 0:
            return finish(_cleanup_block(f"remote branch {branch} not deleted: {detail}", err))
        out.write(f"Deleted remote branch {branch}\n")
    else:
        out.write("remote branch already deleted\n")
    return finish(0)


def cleanup_change(
    target: LandTarget, out, err, *, worktree: Path | None = None, fetch: bool = True
) -> int:
    """Check every precondition, then remove the change's worktree and refs.
    Exit 1 with `BLOCK land.cleanup` and nothing removed on any refusal."""
    plan = plan_cleanup(target, worktree=worktree, fetch=fetch)
    if isinstance(plan, str):
        return _cleanup_block(plan, err)
    return execute_cleanup(target, plan, out, err)


def _normalized(text: str) -> str:
    return " ".join(text.split())


def _acceptance_line(repo: Path, accepted_by: str) -> str:
    """`Accepted-by: <name> <date>`, citing the blind-run report blob when one
    is committed at HEAD."""
    line = f"Accepted-by: {accepted_by} {date.today().isoformat()}"
    change_id, _error = _publication_change_id(repo)
    if change_id:
        report_rel = artifact_path(
            load_manifest(), "blind-run-report", change_id, repo
        ).relative_to(repo)
        blob = git_maybe(repo, "rev-parse", "--verify", "--quiet", f"HEAD:{report_rel}")
        if blob:
            line += f" (blind-run-report {blob[:7]})"
    return line


def _merged_state(target: LandTarget, err) -> tuple[str, str] | None:
    """(state, mergeCommit oid) from GitHub, or None after a reported block."""
    result = _read(
        [target.trusted_gh, "pr", "view", str(target.number), "--json", "state,mergeCommit"],
        "PR state lookup", repo=target.repo, env=target.env, err=err,
    )
    if result is None:
        return None
    try:
        payload = json.loads(result.stdout)
        commit = payload.get("mergeCommit") or {}
        return str(payload.get("state", "")).upper(), str(commit.get("oid", ""))
    except (json.JSONDecodeError, AttributeError) as exc:
        _block(f"cannot decode PR state response: {exc}", err)
        return None


def _squash_merge(
    target: LandTarget, accepted_by: str, err
) -> tuple[str, str, str] | None:
    """Spec 'Merge command': squash with the PR title and body; returns
    (merge commit oid, title, body) once GitHub reports the PR merged."""
    view = _read(
        [target.trusted_gh, "pr", "view", str(target.number), "--json", "title,body"],
        "PR title and body lookup", repo=target.repo, env=target.env, err=err,
    )
    if view is None:
        return None
    try:
        payload = json.loads(view.stdout)
        title = str(payload["title"])
        body = str(payload.get("body") or "")
    except (json.JSONDecodeError, KeyError, TypeError, AttributeError) as exc:
        _block(f"cannot decode PR title and body: {exc}", err)
        return None
    message = f"{body.rstrip()}\n\n{_acceptance_line(target.repo, accepted_by)}\n"

    with tempfile.TemporaryDirectory(prefix="loom-land-") as message_dir:
        body_file = Path(message_dir) / "squash-body.md"
        body_file.write_text(message, encoding="utf-8")
        body_file.chmod(0o600)
        try:
            result = run_land_external(
                [target.trusted_gh, "pr", "merge", str(target.number), "--squash",
                 "--match-head-commit", target.head,
                 "--subject", f"{title} (#{target.number})",
                 "--body-file", str(body_file)],
                LAND_WRITE_TIMEOUT, cwd=target.repo, env=target.env,
            )
            detail = "" if result.returncode == 0 else (
                result.stderr or result.stdout or f"exit {result.returncode}"
            ).strip()
        except (OSError, subprocess.TimeoutExpired) as exc:
            detail = f"{type(exc).__name__}: {exc}"

    # A failed or timed-out command may still have merged: re-read up to 60s.
    state = ""
    for attempt in range(LAND_MERGE_STATE_WAITS + 1):
        observed = _merged_state(target, err)
        if observed is None:
            return None
        state, oid = observed
        if state == "MERGED" and oid:
            return oid, title, body
        if attempt < LAND_MERGE_STATE_WAITS:
            wait_land_interval(PUBLISH_CI_POLL_SECONDS)
    if not detail:
        detail = f"PR #{target.number} is {state or 'UNKNOWN'}"
    _block(f"merge not performed: {detail}", err)
    return None


def _verify_merge(
    target: LandTarget, merge_commit: str, title: str, body: str, err
) -> int:
    """Spec 'Verification': the squash commit carries the PR title and body."""
    def verify_block(reason: str) -> int:
        return report([("land.verify", reason)], err)

    try:
        fetched = run_land_external(
            [target.trusted_git, "fetch", "origin", target.base],
            LAND_WRITE_TIMEOUT, cwd=target.repo, env=target.env,
        )
        if fetched.returncode != 0:
            detail = (fetched.stderr or fetched.stdout or f"exit {fetched.returncode}").strip()
            return verify_block(f"cannot fetch origin {target.base}: {detail}")
        commit = run_land_external(
            [target.trusted_git, "cat-file", "commit", merge_commit],
            LAND_READ_TIMEOUT, cwd=target.repo, env=target.env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return verify_block(f"cannot read the squash commit: {type(exc).__name__}: {exc}")
    if commit.returncode != 0:
        detail = (commit.stderr or commit.stdout or f"exit {commit.returncode}").strip()
        return verify_block(f"cannot read the squash commit: {detail}")

    _header, _sep, message = commit.stdout.partition("\n\n")
    normalized = _normalized(message)
    if _normalized(title) not in normalized:
        return verify_block("squash commit lacks the PR title")
    if _normalized(body) not in normalized:
        return verify_block("squash commit lacks the PR body")
    return 0


def _accepted_names(repo: Path) -> tuple[set[str], str | None]:
    """Names that may accept: the committed intent's originator and the
    authorizer in its `publication:` line."""
    change_id, error = _publication_change_id(repo)
    if error:
        return set(), error
    intent_rel = artifact_path(load_manifest(), "intent", change_id, repo).relative_to(repo)
    try:
        committed = git_text(repo, "show", f"HEAD:{intent_rel}")
    except UsageError:
        return set(), "the attested change's intent is not committed at HEAD"
    front, _sections = parse_document(committed)
    names = set()
    if front.get("originator", "").strip():
        names.add(front["originator"].strip())
    match = re.fullmatch(
        r"automatic — authorized \d{4}-\d{2}-\d{2} by (\S(?:.*\S)?)",
        front.get("publication", ""),
    )
    if match:
        names.add(match.group(1))
    return names, None


def _read(argv: list[str], what: str, *, repo: Path, env: dict[str, str], err):
    try:
        result = run_land_external(argv, LAND_READ_TIMEOUT, cwd=repo, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        _block(f"{what} could not run: {type(exc).__name__}: {exc}", err)
        return None
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
        _block(f"{what} failed: {detail}", err)
        return None
    return result


def _merge_preconditions(
    accepted_by: str | None, trusted_git: str, trusted_gh: str, out, err
) -> LandTarget | int:
    """Spec 'Merge preconditions, in order'; every refusal is land.merge."""
    if not accepted_by:
        return _block(ACCEPTANCE_NOT_RECORDED, err)
    try:
        repo = repo_root(Path.cwd()).resolve()
    except UsageError as exc:
        return _block(str(exc), err)

    # (1) acceptance
    names, intent_error = _accepted_names(repo)
    if intent_error:
        return _block(intent_error, err)
    if accepted_by not in names:
        return _block(ACCEPTANCE_NOT_RECORDED, err)

    head = git_maybe(repo, "rev-parse", "HEAD")
    branch = git_maybe(repo, "symbolic-ref", "--quiet", "--short", "HEAD")
    if not head or not branch or not git_ok(repo, "check-ref-format", "--branch", branch):
        return _block("land requires a safe current symbolic branch and HEAD", err)
    _origin_url, origin_error = _publish_origin_state(repo, branch)
    if origin_error:
        return _block(origin_error, err)
    identity = github_repo_from_origin(repo)
    if not identity:
        return _block("literal origin is not a supported GitHub repository URL", err)
    env = _publish_env(identity, repo, (trusted_git, trusted_gh))

    # (2) attestation at live HEAD
    if _cmd_push(["--head", head, "--require-live-head"], out, err) != 0:
        return _block("attestation does not validate at HEAD; return to Review", err)

    # (3) exactly one open PR for this branch against the default base
    base_result = _read(
        [trusted_gh, "repo", "view", identity, "--json", "defaultBranchRef",
         "--jq", ".defaultBranchRef.name"],
        "default branch lookup", repo=repo, env=env, err=err,
    )
    if base_result is None:
        return 1
    base = base_result.stdout.strip()
    if not base or base == branch or not git_ok(repo, "check-ref-format", "--branch", base):
        return _block("origin default branch is missing, unsafe, or equals the head branch", err)
    host, owner, name = identity.split("/", 2)
    pulls_endpoint = (
        f"repos/{quote(owner, safe='')}/{quote(name, safe='')}/pulls"
        f"?state=open&head={quote(f'{owner}:{branch}', safe='')}"
    )
    list_result = _read(
        [trusted_gh, "api", "--hostname", host, pulls_endpoint],
        "open PR lookup", repo=repo, env=env, err=err,
    )
    if list_result is None:
        return 1
    try:
        candidates = json.loads(list_result.stdout)
    except json.JSONDecodeError as exc:
        return _block(f"cannot decode open PR response: {exc}", err)
    if not isinstance(candidates, list):
        return _block("open PR response is not a list", err)
    expected_repo = f"{owner}/{name}".casefold()
    matching = []
    for candidate in candidates:
        try:
            if (
                candidate["base"]["ref"] == base
                and candidate["base"]["repo"]["full_name"].casefold() == expected_repo
                and candidate["head"]["repo"]["full_name"].casefold() == expected_repo
            ):
                matching.append((int(candidate["number"]), str(candidate["head"]["sha"])))
        except (KeyError, TypeError, ValueError, AttributeError):
            return _block("open PR response has an unreadable pull request", err)
    if not matching:
        return _block(f"no open PR for {branch} against {base}; publish again", err)
    if len(matching) > 1:
        return _block(f"multiple open PRs for {branch} against {base}", err)
    number, pr_head = matching[0]
    if pr_head != head:
        return _block(
            f"PR #{number} head {pr_head[:7]} is not HEAD {head[:7]}; publish again", err
        )

    # (4) every check, not only required ones
    if _observe_all_checks(number, trusted_gh=trusted_gh, repo=repo, env=env,
                           out=out, err=err) != 0:
        return 1

    # (5) GitHub's merge state
    if _await_mergeable(number, trusted_gh=trusted_gh, repo=repo, env=env, err=err) != 0:
        return 1

    return LandTarget(repo, head, branch, base, identity, number, trusted_git, trusted_gh, env)


def _observe_all_checks(
    number: int, *, trusted_gh: str, repo: Path, env: dict[str, str], out, err
) -> int:
    pending_waits = 0
    registration_waits = 0
    announced = False
    while True:
        argv = [trusted_gh, "pr", "checks", str(number), "--json", "name,state,bucket"]
        try:
            result = run_land_external(argv, LAND_READ_TIMEOUT, cwd=repo, env=env)
        except (OSError, subprocess.TimeoutExpired) as exc:
            return _block(f"checks could not be observed: {type(exc).__name__}: {exc}", err)
        # gh exits 1 before a new branch's checks register (blank stdout,
        # quoted-branch message), 1 when a check failed, and 8 while pending;
        # the JSON stays authoritative whenever it is printed.
        no_checks_yet = (
            result.returncode == 1
            and not result.stdout.strip()
            and re.fullmatch(
                r"no (?:required )?checks reported on the '.*' branch",
                result.stderr.strip(),
            ) is not None
        )
        if not no_checks_yet and (
            result.returncode not in {0, 1, 8}
            or (result.returncode != 0 and not result.stdout.strip())
        ):
            detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
            return _block(f"checks could not be observed: {detail}", err)
        if no_checks_yet or not result.stdout.strip():
            checks = []
        else:
            try:
                checks = json.loads(result.stdout)
            except json.JSONDecodeError as exc:
                return _block(f"cannot decode checks response: {exc}", err)
        if not isinstance(checks, list) or any(not isinstance(check, dict) for check in checks):
            return _block("checks response is not a list of checks", err)
        if not checks:
            if registration_waits >= PUBLISH_CI_REGISTRATION_WAITS:
                out.write(f"No checks registered on PR #{number}\n")
                return 0
            wait_land_interval(PUBLISH_CI_POLL_SECONDS)
            registration_waits += 1
            continue

        states = [(str(check.get("name", "unnamed")),
                   str(check.get("state", "")).upper(),
                   str(check.get("bucket", "")).casefold()) for check in checks]
        refused = [
            (name, state or bucket) for name, state, bucket in states
            if bucket in {"fail", "cancel"}
            or state in {"FAILURE", "TIMED_OUT", "STARTUP_FAILURE",
                         "CANCELLED", "CANCELED", "ACTION_REQUIRED"}
        ]
        if refused:
            return report(
                [("land.merge", f"check {name}: {state}") for name, state in refused], err
            )
        pending = [name for name, state, bucket in states
                   if state in {"PENDING", "QUEUED", "IN_PROGRESS", "WAITING", "REQUESTED"}
                   or bucket == "pending"]
        if pending:
            if pending_waits >= PUBLISH_CI_PENDING_WAITS:
                return _block(
                    f"checks on PR #{number} still pending after 60 minutes: "
                    + ", ".join(pending), err,
                )
            if not announced:
                out.write(f"Waiting for checks on PR #{number}\n")
                announced = True
            wait_land_interval(PUBLISH_CI_POLL_SECONDS)
            pending_waits += 1
            continue
        unknown = [(name, state or bucket or "unknown") for name, state, bucket in states
                   if bucket not in {"pass", "skipping"}]
        if unknown:
            return report(
                [("land.merge", f"check {name}: {state}") for name, state in unknown], err
            )
        out.write(f"All checks passed on PR #{number}\n")
        return 0


def _await_mergeable(
    number: int, *, trusted_gh: str, repo: Path, env: dict[str, str], err
) -> int:
    status = mergeable = ""
    for attempt in range(LAND_MERGE_STATE_WAITS + 1):
        result = _read(
            [trusted_gh, "pr", "view", str(number), "--json", "mergeable,mergeStateStatus"],
            "merge state lookup", repo=repo, env=env, err=err,
        )
        if result is None:
            return 1
        try:
            payload = json.loads(result.stdout)
            mergeable = str(payload.get("mergeable", "")).upper()
            status = str(payload.get("mergeStateStatus", "")).upper()
        except (json.JSONDecodeError, AttributeError) as exc:
            return _block(f"cannot decode merge state response: {exc}", err)
        if status in BLOCKING_MERGE_STATES:
            return _block(f"PR #{number} is {status}", err)
        if mergeable == "CONFLICTING":
            return _block(f"PR #{number} is {status or mergeable}", err)
        if mergeable == "MERGEABLE" and status not in {"", "UNKNOWN"}:
            return 0
        if attempt < LAND_MERGE_STATE_WAITS:
            wait_land_interval(PUBLISH_CI_POLL_SECONDS)
    return _block(f"PR #{number} is {status or mergeable or 'UNKNOWN'}", err)
