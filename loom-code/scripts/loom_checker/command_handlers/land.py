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
    # --- W3-01 extension point: the merge is verified; trunk fast-forward and
    # change cleanup start here. ---------------------------------------------
    return 0


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
