from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Literal
from git_exec import run_git
from loom_checker.helpers import UsageError
from loom_checker.helpers import artifact_path
from loom_checker.helpers import current_branch
from loom_checker.helpers import git_maybe
from loom_checker.helpers import git_ok
from loom_checker.helpers import git_text
from loom_checker.helpers import is_real_date
from loom_checker.helpers import load_manifest
from loom_checker.helpers import repo_root
from loom_checker.helpers import report
from loom_checker.parsing import parse_document
from loom_checker.rule_checks.publish import validate_contextual_pr_body
from loom_checker.rule_checks.publish import validate_disclosed_outcome
from loom_checker.rule_checks.publish import validate_stated_status
from loom_checker.rule_checks.push import CANONICAL_PUSH_FLAGS
from loom_checker.rule_checks.push import github_repo_from_origin
from loom_checker.rule_checks.intake import _parse_plan_task_fields, _split_respecting_backticks
from loom_checker.verification import identify_change
from loom_checker.verification import missing_clause
from loom_checker.verification import missing_records
from loom_checker.verification import verification_status
from pathlib import Path
from urllib.parse import quote
import json
import os
import re
import signal
import subprocess
import sys
import tempfile
import time


PUBLISH_REDIRECT_ENV = {
    "GIT_DIR", "GIT_COMMON_DIR", "GIT_WORK_TREE", "GIT_NAMESPACE", "GIT_OBJECT_DIRECTORY",
    "GIT_ALTERNATE_OBJECT_DIRECTORIES", "GIT_EXEC_PATH", "GIT_SSH",
    "GIT_SSH_COMMAND", "GIT_PROXY_COMMAND", "GIT_CONFIG", "GIT_CONFIG_SYSTEM",
    "GIT_CONFIG_GLOBAL", "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_COUNT",
    "GIT_CONFIG_PARAMETERS", "GH_HOST", "GH_REPO",
}


PUBLISH_REDIRECT_CONFIG = (
    r"^(remote\.origin\.(pushurl|proxy|vcs|receivepack|uploadpack)"
    r"|url\..*\.(push)?insteadof|core\.sshcommand)$"
)


PUBLISH_EXECUTABLE_DIRS = (
    Path("/usr/bin"), Path("/usr/local/bin"), Path("/opt/homebrew/bin"),
    Path("/home/linuxbrew/.linuxbrew/bin"),
)


def resolve_publish_executable(name: str) -> str | None:
    """Resolve publication tools from host install roots, never caller PATH."""
    for directory in PUBLISH_EXECUTABLE_DIRS:
        candidate = directory / name
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate.resolve())
    return None


def run_publish_external(argv: list[str], **kwargs) -> subprocess.CompletedProcess:
    """Run one trusted publication argv; kept as a seam for isolated tests."""
    return subprocess.run(argv, capture_output=True, text=True, timeout=30, **kwargs)


wait_publish_interval = time.sleep


PUBLISH_CI_POLL_SECONDS = 10


PUBLISH_CI_REGISTRATION_WAITS = 6


PUBLISH_CI_PENDING_WAITS = 360


def _publish_usage(reason: str, err) -> int:
    err.write(f"publish: {reason}\n")
    return 2


def _publish_block(reason: str, err, next_action: str | None = None,
                   *, rule: str = "publish.preconditions") -> int:
    remedy = (next_action or
              "Inspect the publication diagnostics and reconcile the named condition before "
              "retrying publish; preserve work and do not switch merge routes.")
    return report([(rule, f"{reason}; next: {remedy}")], err)


def _publish_origin_state(repo: Path, expected_branch: str) -> tuple[str | None, str | None]:
    """Return the single literal origin URL or a publication identity error."""
    branch = current_branch(repo)
    if branch != expected_branch:
        return None, "symbolic branch changed before publication"
    origin_urls = (git_maybe(repo, "config", "--get-all", "remote.origin.url") or "").splitlines()
    if len(origin_urls) != 1:
        return None, "literal origin must have exactly one fetch URL"
    redirect_config = git_maybe(repo, "config", "--get-regexp", PUBLISH_REDIRECT_CONFIG)
    if redirect_config:
        return None, (
            "origin redirection, transport, remote executable, pushurl, insteadOf, "
            "sshCommand, or proxy configuration must be removed"
        )
    return origin_urls[0], None


def _publish_args(args: list[str]) -> tuple[str, Path, Path | None, bool] | str:
    authorized = False
    title: str | None = None
    body_file: Path | None = None
    intent_file: Path | None = None
    rest = list(args)
    while rest:
        token = rest.pop(0)
        if token == "--confirm-authorized":
            if authorized:
                return "--confirm-authorized may appear only once"
            authorized = True
        elif token in {"--title", "--body-file", "--intent"}:
            if not rest:
                return f"{token} needs a value"
            value = rest.pop(0)
            if token == "--title":
                if title is not None:
                    return "--title may appear only once"
                title = value
            elif token == "--body-file":
                if body_file is not None:
                    return "--body-file may appear only once"
                body_file = Path(value)
            else:
                if intent_file is not None:
                    return "--intent may appear only once"
                intent_file = Path(value)
        else:
            return f"unexpected argument {token!r}"
    if not authorized and intent_file is None:
        return "--intent or --confirm-authorized is required for publication authorization"
    if not title or not title.strip():
        return "--title needs non-empty text"
    if body_file is None or not body_file.is_absolute():
        return "--body-file must name an absolute path"
    if not body_file.is_file() or not os.access(body_file, os.R_OK):
        return f"--body-file is not a readable file: {body_file}"
    if intent_file is not None:
        if not intent_file.is_absolute():
            return "--intent must name an absolute path"
        if not intent_file.is_file() or not os.access(intent_file, os.R_OK):
            return f"--intent is not a readable file: {intent_file}"
    return title, body_file, intent_file, authorized


def _intent_authorizes_publication(
    repo: Path, intent_file: Path, change_id: str
) -> tuple[bool, str | None]:
    """Trust only the identified change's canonical intent as committed at HEAD."""
    manifest = load_manifest()
    canonical = artifact_path(manifest, "intent", change_id, repo).resolve()
    if intent_file.resolve() != canonical:
        return False, "intent path does not match the identified change"
    intent_rel = canonical.relative_to(repo)
    try:
        committed = git_text(repo, "show", f"HEAD:{intent_rel}")
    except UsageError:
        return False, "automatic publication requires a committed intent at HEAD"
    front, _sections = parse_document(committed)
    if not re.fullmatch(r"confirmed \d{4}-\d{2}-\d{2}", front.get("status", "")):
        return False, "committed intent is not confirmed"
    publication = front.get("publication", "")
    match = re.fullmatch(
        r"automatic — authorized (\d{4}-\d{2}-\d{2}) by (\S(?:.*\S)?)",
        publication,
    )
    if match is None or not is_real_date(match.group(1)):
        return False, "committed intent has no valid automatic-publication authorization"
    try:
        working_front, _ = parse_document(canonical.read_text(encoding="utf-8"))
    except (OSError, UnicodeError):
        return False, "automatic-publication authorization revoked: working intent is unavailable"
    if working_front.get("publication") != publication:
        return False, "automatic-publication authorization revoked in the working intent"
    return True, None


@dataclass(frozen=True)
class CheckObservation:
    state: str
    reason: str
    next: str
    issues: tuple[tuple[str, str], ...] = ()


# External-interface grounding:
# https://cli.github.com/manual/gh_pr_checks documents JSON bucket fields and
# pending exit 8. The pinned implementation and tests cover the no-(required)-
# checks stderr forms; issue 7401 describes the check-registration race:
# https://github.com/cli/cli/blob/v2.88.1/pkg/cmd/pr/checks/checks.go
# https://github.com/cli/cli/blob/v2.88.1/pkg/cmd/pr/checks/checks_test.go
# https://github.com/cli/cli/issues/7401
# In v2.88.1 the JSON exporter returns before non-JSON failure/pending exits;
# accepting valid JSON with exit 1 below is defensive compatibility, not a
# claim that this pinned exporter produces that combination.
def classify_checks(result: subprocess.CompletedProcess, *, required: bool) -> CheckObservation:
    """Classify one gh snapshot; callers retain their own selection and wait policy."""
    diagnostic = "Inspect gh authentication, permissions and response diagnostics; retry the same route."
    unavailable = lambda reason: CheckObservation("unconfirmed", reason, diagnostic)
    no_checks = (result.returncode == 1 and not result.stdout.strip() and re.fullmatch(
        r"no (?:required )?checks reported on the '.*' branch", result.stderr.strip()) is not None)
    if result.returncode not in {0, 1, 8} or (
        result.returncode != 0 and not result.stdout.strip() and not no_checks
    ):
        return unavailable("could not be observed: " +
                           (result.stderr or result.stdout or f"exit {result.returncode}").strip())
    if no_checks or (required and result.returncode == 0 and not result.stdout.strip()):
        checks = []
    elif not result.stdout.strip():
        return unavailable("could not be observed")
    else:
        try:
            checks = json.loads(result.stdout)
        except json.JSONDecodeError as exc:
            return unavailable(f"cannot decode checks response: {exc}")
    if not isinstance(checks, list) or any(not isinstance(check, dict) for check in checks):
        return unavailable("response is not a list of checks")
    if not checks:
        if result.returncode == 1 and not no_checks:
            return unavailable("could not be observed: " + (result.stderr or "exit 1").strip())
        return CheckObservation("empty", "no required checks registered" if required else
                                "no checks registered", "No check result exists; retain the repository check policy.")
    states = [(str(c.get("name", "unnamed")), str(c.get("state", "")).upper(),
               str(c.get("bucket", "")).casefold()) for c in checks]
    groups = (
        ("action_required", "requires user action", lambda s, b: s == "ACTION_REQUIRED",
         "Inspect the named check and obtain its required approval before retrying."),
        ("cancelled", "cancelled", lambda s, b: s in {"CANCELLED", "CANCELED"} or b == "cancel",
         "Inspect why the check was cancelled and rerun it through the existing CI route."),
        ("failed", "failed", lambda s, b: s in {"FAILURE", "TIMED_OUT", "STARTUP_FAILURE"} or b == "fail",
         "Inspect the named CI logs, fix the failure and rerun checks before retrying."),
        ("pending", "pending", lambda s, b: s in {"PENDING", "QUEUED", "IN_PROGRESS", "WAITING", "REQUESTED"} or b == "pending",
         "Continue bounded check observation; wait for a terminal result before proceeding."),
        ("unconfirmed", "requires user action because its state is unknown", lambda s, b: b not in {"pass", "skipping"}, diagnostic),
    )
    refused = tuple((name, state or bucket) for name, state, bucket in states
                    if any(predicate(state, bucket) for _, _, predicate, _ in groups[:3]))
    terminal_categories = {
        next(category for category, _, predicate, _ in groups[:3] if predicate(state, bucket))
        for _, state, bucket in states
        if any(predicate(state, bucket) for _, _, predicate, _ in groups[:3])
    }
    for category, description, predicate, remedy in groups:
        issues = tuple((n, s or b or "unknown") for n, s, b in states if predicate(s, b))
        if issues:
            if len(terminal_categories) > 1:
                remedy = ("Inspect the named CI logs and fix failures, determine why checks were cancelled, "
                          "and obtain any required approval; rerun only the appropriate checks through the "
                          "existing CI route after resolving those conditions.")
            return CheckObservation(category, description + ": " + ", ".join(n for n, _ in issues),
                                    remedy, refused or issues)
    return CheckObservation("passed", "passed", "Await acceptance before requesting an authorized merge.")


@dataclass(frozen=True)
class DeliveryResult:
    state: Literal["local", "uncommitted", "unpublished", "missing_pr", "mismatched_pr",
                   "pending", "failed", "cancelled", "action_required", "published",
                   "merged", "unconfirmed"]
    reason: str
    next: str
    evidence: dict
    complete: bool = False


def _delivery_scope(repo: Path, change_id: str, head: str, base: str | None) -> set[str]:
    """Concrete committed plan paths plus the committed branch delta, never the working plan."""
    plan = artifact_path(load_manifest(), "plan", change_id, repo).relative_to(repo).as_posix()
    committed = git_maybe(repo, "show", f"{head}:{plan}")
    paths: set[str] = set()
    if committed is not None:
        _, sections = parse_document(committed)
        for fields in _parse_plan_task_fields(sections.get("Task DAG", "")).values():
            for entry in _split_respecting_backticks(fields.get("Files") or ""):
                value = entry.strip("`")
                if (value and not Path(value).is_absolute() and ".." not in Path(value).parts
                        and not re.search(r"[<>*?\[\]]", value)):
                    paths.add(value)
    if base:
        fork = git_maybe(repo, "merge-base", head, base)
        if fork:
            delta = run_git(repo, "diff", "--name-only", "-z", fork, head,
                            timeout=30, strip=False)
            if delta is None:
                raise UsageError("cannot attribute the committed branch delta")
            paths.update(p for p in delta.split("\0") if p)
    return paths


def _delivery_pending(repo: Path, paths: set[str]) -> list[str]:
    status = run_git(repo, "status", "--porcelain=v1", "-z", "--untracked-files=all",
                     "--", *(":(literal)" + path for path in sorted(paths)),
                     timeout=30, strip=False)
    if status is None:
        raise UsageError("cannot observe the scoped working tree")
    # Renames carry a second NUL-separated path. Keep both for diagnostics.
    return [entry[3:] if entry[:2] in {"??", "!!"} or entry[2:3] == " " else entry
            for entry in status.split("\0") if entry]


def observe_delivery(
    repo: Path, *, goal: str, intent_file: Path | None, trusted_git: str,
    trusted_gh: str | None,
) -> DeliveryResult:
    """Read current delivery once; neither permission nor this result performs writes."""
    evidence: dict = {}

    def result(state, reason, next_action, complete=False):
        return DeliveryResult(state, reason, next_action, dict(evidence), complete)

    diagnostic = ("Inspect remote availability, gh authentication, permissions and response "
                  "diagnostics; retry the same delivery route without switching merge routes.")
    try:
        change_id, _ = identify_change(repo)
        if not change_id:
            return result("unconfirmed", "cannot identify a committed change",
                          "Name the feature branch <type>/<change-id> and commit its confirmed intent.")
        canonical = artifact_path(load_manifest(), "intent", change_id, repo).resolve()
        if intent_file is not None and intent_file.resolve() != canonical:
            return result("unconfirmed", "intent path does not match the identified change",
                          "Select the identified change's canonical committed intent.")
        head = git_text(repo, "rev-parse", "HEAD")
        branch = current_branch(repo)
        evidence.update(change_id=change_id, head=head, branch=branch)
        if not branch or not git_ok(repo, "check-ref-format", "--branch", branch):
            return result("unconfirmed", "a safe symbolic feature branch is required",
                          "Preserve the current work on a named feature branch before continuing.")
        intent_rel = canonical.relative_to(repo).as_posix()
        committed = git_maybe(repo, "show", f"{head}:{intent_rel}")
        front, _ = parse_document(committed or "")
        if not re.fullmatch(r"confirmed \d{4}-\d{2}-\d{2}", front.get("status", "")):
            return result("unconfirmed", "identified intent is not committed and confirmed",
                          "Obtain intent confirmation and commit the canonical intent.")
        authorized, authorization_reason = _intent_authorizes_publication(repo, canonical, change_id)
        evidence["automatic_publication_authorized"] = authorized
        if authorization_reason:
            evidence["automatic_publication_reason"] = authorization_reason
        publication_next = (
            "Resume publish for this feature branch only while its automatic authorization remains valid."
            if authorized else
            "If an existing explicit user decision authorizes publication, resume publish with "
            "--confirm-authorized; otherwise obtain that user decision before writing. "
            "Observation grants no write permission."
        )

        local_base = git_maybe(repo, "symbolic-ref", "--quiet", "refs/remotes/origin/HEAD")
        scope = _delivery_scope(repo, change_id, head, local_base)

        def pending_result():
            if not scope:
                return result("unconfirmed", "change attribution is unavailable",
                              "Commit concrete Files entries in the change plan or establish its branch delta; "
                              "unseen working-tree code cannot be certified as delivered.")
            evidence["scope"] = sorted(scope)
            pending = _delivery_pending(repo, scope | {intent_rel})
            if pending:
                evidence["pending_paths"] = pending
                return result("uncommitted", "attributable work is not committed",
                              "Review and commit the named change paths; preserve unrelated work.")
            return None

        if goal == "local":
            pending = pending_result()
            if pending:
                return pending
            if git_text(repo, "rev-parse", "HEAD") != head or current_branch(repo) != branch:
                return result("unconfirmed", "local HEAD or branch changed during observation",
                              "Stabilize the selected branch and rerun delivery.")
            return result("local", "attributable work is committed locally",
                          "Report the explicit local goal; publication needs separate authorization.", True)

        origin, origin_error = _publish_origin_state(repo, branch)
        identity = github_repo_from_origin(repo)
        if origin_error or not identity or not trusted_gh:
            return result("unconfirmed", origin_error or "trusted GitHub origin and gh are required", diagnostic)
        env = _publish_env(identity, repo, (trusted_git, trusted_gh))
        evidence["repository"] = identity

        def read(argv):
            response = run_publish_external(argv, cwd=repo, env=env)
            if response.returncode != 0:
                raise UsageError((response.stderr or response.stdout or
                                  f"exit {response.returncode}").strip())
            return response.stdout

        base = read([trusted_gh, "repo", "view", identity, "--json", "defaultBranchRef",
                     "--jq", ".defaultBranchRef.name"]).strip()
        if not base or base == branch or not git_ok(repo, "check-ref-format", "--branch", base):
            return result("unconfirmed", "origin default branch is missing, unsafe or equals the head", diagnostic)
        evidence["base"] = base
        # The server selects the base name; local base objects only attribute paths.
        base_ref = next((ref for ref in (f"refs/remotes/origin/{base}", f"refs/heads/{base}")
                         if git_ok(repo, "rev-parse", "--verify", ref)), None)
        scope.update(_delivery_scope(repo, change_id, head, base_ref))
        pending = pending_result()
        if pending:
            return pending
        remote_argv = [trusted_git, "-C", str(repo), "ls-remote", "--heads", "origin",
                       f"refs/heads/{branch}"]

        def remote_head():
            rows = [line.split() for line in read(remote_argv).splitlines() if line.strip()]
            if not rows:
                return None
            if (len(rows) != 1 or len(rows[0]) != 2 or rows[0][1] != f"refs/heads/{branch}"
                    or not re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", rows[0][0])):
                raise UsageError("remote branch identity response is malformed or ambiguous")
            return rows[0][0]

        remote = remote_head()
        evidence["remote_head"] = remote
        host, owner, name = identity.split("/", 2)
        expected_repo = f"{owner}/{name}".casefold()
        endpoint = (f"repos/{quote(owner, safe='')}/{quote(name, safe='')}/pulls"
                    f"?state=all&head={quote(f'{owner}:{branch}', safe='')}")
        candidates = json.loads(read([trusted_gh, "api", "--hostname", host, endpoint]))
        if not isinstance(candidates, list):
            raise UsageError("PR response is not a list")
        matching = []
        for candidate in candidates:
            try:
                if (candidate["head"]["sha"] == head and candidate["head"]["ref"] == branch
                    and candidate["head"]["repo"]["full_name"].casefold() == expected_repo
                    and candidate["base"]["ref"] == base
                    and candidate["base"]["repo"]["full_name"].casefold() == expected_repo):
                    matching.append(candidate)
            except (KeyError, TypeError, AttributeError):
                raise UsageError("PR response lacks exact head/base/repository identity")
        if git_text(repo, "rev-parse", "HEAD") != head or _publish_origin_state(repo, branch) != (origin, None):
            return result("unconfirmed", "HEAD, branch or origin changed during observation", diagnostic)
        if remote_head() != remote:
            return result("unconfirmed", "remote branch changed during observation", diagnostic)
        if remote is not None and remote != head:
            return result("unpublished", "local HEAD differs from the live remote branch",
                          "Fetch and inspect remote divergence. " + publication_next)
        if not matching:
            if remote != head:
                return result("unpublished", "selected HEAD is absent from the live remote branch",
                              publication_next)
            return result("mismatched_pr" if candidates else "missing_pr",
                          "no PR matches selected HEAD, branch, repository and base",
                          "Inspect the PR identity and preserve the feature branch. " + publication_next)
        if len(matching) != 1:
            return result("unconfirmed", "multiple PRs match the selected delivery identity", diagnostic)
        pr = matching[0]
        url = pr.get("html_url", "")
        if not isinstance(url, str) or not url.startswith(f"https://{host}/{owner}/{name}/pull/"):
            raise UsageError("PR URL does not match the selected repository")
        evidence["pr"] = url
        if pr.get("state") == "closed" and pr.get("merged_at"):
            merge_sha = pr.get("merge_commit_sha")
            if not isinstance(merge_sha, str) or not re.fullmatch(r"[0-9a-f]{40}(?:[0-9a-f]{24})?", merge_sha):
                raise UsageError("merged PR has no valid server merge SHA")
            evidence["merge_sha"] = merge_sha
            return result("merged", "server confirms the selected PR was merged",
                          "Report the merged PR and its server merge SHA.", True)
        if remote != head:
            return result("unpublished", "open PR HEAD has no matching live remote branch",
                          "Inspect branch deletion and preserve the feature branch. " + publication_next)
        if pr.get("state") != "open" or pr.get("draft") is not False:
            return result("mismatched_pr", "selected PR is closed or still a draft",
                          "A matching Ready PR is required. " + publication_next)
        checks = classify_checks(run_publish_external(
            [trusted_gh, "pr", "checks", url, "--required", "--json", "name,state,bucket"],
            cwd=repo, env=env,
        ), required=True)
        evidence["checks"] = checks.state
        # Check observation can race with local edits, a new commit or remote publication.
        if (git_text(repo, "rev-parse", "HEAD") != head
                or _publish_origin_state(repo, branch) != (origin, None) or remote_head() != head):
            return result("unconfirmed", "delivery identity changed while observing checks", diagnostic)
        pending = pending_result()
        if pending:
            return pending
        if checks.state not in {"passed", "empty"}:
            return result(checks.state, "required CI " + checks.reason, checks.next)
        return result("published", "matching Ready PR; required CI " + checks.reason,
                      "Await maintainer acceptance; merge requires separate authorization.", goal == "published")
    except (UsageError, OSError, subprocess.TimeoutExpired, ValueError) as exc:
        return result("unconfirmed", f"delivery evidence unavailable: {exc}", diagnostic)


def _delivery_stop(out, err) -> int:
    """Documented Claude/Codex Stop decision; one deadline, no retry or writes."""
    class DeadlineExpired(RuntimeError):
        pass  # Git/remote helpers catch OSError; deadline must cross those catches.

    def expired(_signum, _frame):
        raise DeadlineExpired("20-second total delivery deadline expired")

    previous_handler = signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, 20)
    previous_path = os.environ.get("PATH")
    try:
        payload = json.load(sys.stdin)
        if (not isinstance(payload, dict) or payload.get("hook_event_name") != "Stop"
                or payload.get("agent_id") or payload.get("parent_session_id")):
            return 0
        trusted_git = resolve_publish_executable("git")
        trusted_gh = resolve_publish_executable("gh")
        redirected = any(key in PUBLISH_REDIRECT_ENV or key.startswith(
            ("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_")) for key in os.environ)
        if redirected or not trusted_git:
            raise UsageError("trusted Git environment is unavailable; remove redirects and provide trusted Git")
        os.environ["PATH"] = os.pathsep.join(dict.fromkeys(
            [str(Path(trusted_git).parent), "/usr/bin", "/bin"]))
        repo = repo_root(Path(payload.get("cwd") or os.getcwd())).resolve()
        change_id, _ = identify_change(repo)
        if not change_id:
            return 0
        intent = artifact_path(load_manifest(), "intent", change_id, repo)
        authorized, _ = _intent_authorizes_publication(repo, intent, change_id)
        if not authorized:
            return 0
        front, _ = parse_document(git_text(repo, "show", f"HEAD:{intent.relative_to(repo)}"))
        spec = artifact_path(load_manifest(), "spec", change_id, repo)
        if front.get("kind") == "product" and spec.exists():
            spec_front, _ = parse_document(spec.read_text(encoding="utf-8"))
            if not spec_front.get("confirmed-behavior"):
                return 0
        observed = observe_delivery(repo, goal="published", intent_file=intent,
                                    trusted_git=trusted_git, trusted_gh=trusted_gh)
        if observed.complete:
            return 0  # Publication is the boundary; acceptance never grants merge.
        feedback = f"Delivery incomplete ({observed.state}): {observed.reason}\nnext: {observed.next}"
        if payload.get("stop_hook_active") or observed.state == "unconfirmed":
            err.write(feedback + "\n")
        else:
            feedback = ("If you are waiting for the user's answer or publication was withdrawn, "
                        "stop again and say so; otherwise: " + feedback)
            out.write(json.dumps({"decision": "block", "reason": feedback}, ensure_ascii=False) + "\n")
    except (OSError, UnicodeError, ValueError, TypeError, UsageError, DeadlineExpired) as exc:
        err.write(f"Delivery unconfirmed: {exc}\nnext: Restore the missing prerequisites and run "
                  "loom-python --ready delivery --json before claiming completion.\n")
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous_handler)
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
    return 0


def cmd_delivery(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Observe an explicit local, published or merged delivery target without writes."""
    if "--hook" in args:
        if args != ["--hook"]:
            err.write("delivery: --hook must be used alone\n")
            return 2
        return _delivery_stop(out, err)
    goal, intent_file, as_json = "published", None, False
    seen: set[str] = set()
    rest = list(args)
    while rest:
        token = rest.pop(0)
        if token in seen or token not in {"--goal", "--intent", "--json", "--hook"}:
            err.write(f"delivery: unexpected or repeated argument {token!r}\n")
            return 2
        seen.add(token)
        if token in {"--goal", "--intent"}:
            if not rest or rest[0].startswith("--"):
                err.write(f"delivery: {token} needs a value\n")
                return 2
            value = rest.pop(0)
            if token == "--goal":
                goal = value
            else:
                intent_file = Path(value)
        elif token == "--json":
            as_json = True
    if goal not in {"local", "published", "merged"}:
        err.write("delivery: --goal must be local, published or merged\n")
        return 2
    trusted_git = resolve_publish_executable("git")
    trusted_gh = resolve_publish_executable("gh") if goal != "local" else None
    redirected = [key for key in os.environ if key in PUBLISH_REDIRECT_ENV
                  or key.startswith(("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"))]
    previous_path = os.environ.get("PATH")
    try:
        if redirected or not trusted_git:
            observed = DeliveryResult("unconfirmed", "trusted Git environment is unavailable",
                                      "Remove redirect environment variables and provide trusted Git.", {})
        else:
            os.environ["PATH"] = os.pathsep.join(dict.fromkeys(
                [str(Path(trusted_git).parent), "/usr/bin", "/bin"]))
            observed = observe_delivery(repo_root(Path.cwd()).resolve(), goal=goal,
                                        intent_file=intent_file, trusted_git=trusted_git,
                                        trusted_gh=trusted_gh)
    except UsageError as exc:
        observed = DeliveryResult("unconfirmed", str(exc), "Run delivery inside the selected repository.", {})
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path
    if as_json:
        out.write(json.dumps(asdict(observed), ensure_ascii=False) + "\n")
    else:
        out.write(f"Delivery {observed.state}: {observed.reason}\nnext: {observed.next}\n")
    return 0 if observed.complete else 1


def _publish_env(repo_identity: str, repo: Path, trusted_paths: tuple[str, str]) -> dict[str, str]:
    env = {
        key: value for key, value in os.environ.items()
        if key not in PUBLISH_REDIRECT_ENV and not key.startswith("GIT_CONFIG_KEY_")
        and not key.startswith("GIT_CONFIG_VALUE_")
    }
    safe_path = os.pathsep.join(dict.fromkeys(
        [str(Path(path).parent) for path in trusted_paths] + ["/usr/bin", "/bin"]
    ))
    env.update({"GH_REPO": repo_identity, "LOOM_REPO_ROOT": str(repo), "PATH": safe_path})
    return env


def _external_or_block(argv: list[str], *, repo: Path, env: dict[str, str], err):
    try:
        result = run_publish_external(argv, cwd=repo, env=env)
    except (OSError, subprocess.TimeoutExpired) as exc:
        _publish_block(f"publication command could not run: {type(exc).__name__}: {exc}", err)
        return None
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or f"exit {result.returncode}").strip()
        _publish_block(f"publication command failed: {detail}", err)
        return None
    return result


def _observe_required_ci(
    pr_url: str, *, trusted_gh: str, repo: Path, env: dict[str, str], out, err
) -> int:
    """Observe required PR checks in this process until a terminal state."""
    pending_waits = registration_waits = 0
    while True:
        try:
            result = run_publish_external(
                [trusted_gh, "pr", "checks", pr_url, "--required", "--json", "name,state,bucket"],
                cwd=repo, env=env,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return _publish_block(
                f"required CI could not be observed: {type(exc).__name__}: {exc}", err
            )
        observed = classify_checks(result, required=True)
        if observed.state == "empty":
            if registration_waits >= PUBLISH_CI_REGISTRATION_WAITS:
                out.write("No required checks registered\n")
                return 0
            registration_waits += 1
        elif observed.state == "pending":
            if pending_waits >= PUBLISH_CI_PENDING_WAITS:
                return _publish_block(
                    "required CI requires user action because no reliable terminal result "
                    "was available after 60 minutes", err, observed.next,
                )
            pending_waits += 1
        elif observed.state == "passed":
            out.write("Required CI passed\n")
            return 0
        else:
            return _publish_block("required CI " + observed.reason, err, observed.next)
        wait_publish_interval(PUBLISH_CI_POLL_SECONDS)


def cmd_publish(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Validate and publish one reviewed HEAD without caller-built shell text."""
    parsed = _publish_args(args)
    if isinstance(parsed, str):
        return _publish_usage(parsed, err)
    title, body_file, intent_file, authorized = parsed

    try:
        body = body_file.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        return _publish_usage(f"cannot read PR body as UTF-8: {exc}", err)
    body_error = validate_contextual_pr_body(body)
    if body_error:
        return _publish_block(body_error, err, rule="push.contextual-body")

    redirected = sorted(
        key for key in os.environ
        if key in PUBLISH_REDIRECT_ENV
        or key.startswith("GIT_CONFIG_KEY_") or key.startswith("GIT_CONFIG_VALUE_")
    )
    if redirected:
        return _publish_usage(
            "remove repository or host redirect environment variables: "
            + ", ".join(redirected), err,
        )

    trusted_git = resolve_publish_executable("git")
    trusted_gh = resolve_publish_executable("gh")
    if not trusted_git or not trusted_gh:
        return _publish_block("publication requires trusted git and gh executables", err)

    previous_path = os.environ.get("PATH")
    os.environ["PATH"] = os.pathsep.join(dict.fromkeys(
        [str(Path(trusted_git).parent), str(Path(trusted_gh).parent), "/usr/bin", "/bin"]
    ))
    try:
        with tempfile.TemporaryDirectory(prefix="loom-publish-") as snapshot_dir:
            body_snapshot = Path(snapshot_dir) / "pr-body.md"
            body_snapshot.write_text(body, encoding="utf-8")
            body_snapshot.chmod(0o600)
            return _cmd_publish_trusted(
                title, body_snapshot, intent_file, authorized,
                trusted_git, trusted_gh, out, err,
            )
    finally:
        if previous_path is None:
            os.environ.pop("PATH", None)
        else:
            os.environ["PATH"] = previous_path


def _no_program_reasons(repo: Path, head: str, attestation_rel: str) -> list[str]:
    """The no-program reasons the attestation committed at `head` records."""
    try:
        executions = json.loads(git_maybe(repo, "show", f"{head}:{attestation_rel}") or "")
        executions = executions.get("executions")
    except (ValueError, AttributeError):
        return []
    return [row["no_program"] for row in executions if isinstance(row, dict)
            and row.get("kind") == "adversarial" and isinstance(row.get("no_program"), str)
            ] if isinstance(executions, list) else []


def _cmd_publish_trusted(
    title: str, body_file: Path, intent_file: Path | None, authorized: bool,
    trusted_git: str, trusted_gh: str,
    out=sys.stdout, err=sys.stderr,
) -> int:
    try:
        repo = repo_root(Path.cwd()).resolve()
    except UsageError as exc:
        return _publish_block(str(exc), err)

    change_id, _unidentified = identify_change(repo)
    if change_id is None:
        return _publish_block("cannot identify the change — name the branch "
                              "<type>/<change-id> or commit its intent", err)

    intent_error: str | None = None
    if not authorized and intent_file is not None:
        intent_authorized, intent_error = _intent_authorizes_publication(
            repo, intent_file, change_id
        )
        authorized = intent_authorized
    if not authorized:
        return _publish_usage(
            f"{intent_error or 'intent has no confirmed automatic-publication authorization'}; "
            "obtain one publication decision and pass --confirm-authorized",
            err,
        )

    head = git_maybe(repo, "rev-parse", "HEAD")
    branch = current_branch(repo)
    if not head or not branch or not git_ok(repo, "check-ref-format", "--branch", branch):
        return _publish_block("publication requires a safe current symbolic branch and HEAD", err)
    origin_url, origin_error = _publish_origin_state(repo, branch)
    if origin_error:
        return _publish_block(origin_error, err)
    identity = github_repo_from_origin(repo)
    if not identity:
        return _publish_block("literal origin is not a supported GitHub repository URL", err)
    env = _publish_env(identity, repo, (trusted_git, trusted_gh))

    attestation_file = artifact_path(load_manifest(), "attestation", change_id, repo)
    attestation_rel = attestation_file.relative_to(repo).as_posix()
    # Ceiling: a gitignored attestation is invisible to git status; a git failure fails closed as 'not committed'.
    # git status --porcelain -- <pathspec> prints nothing for a clean tracked path: https://git-scm.com/docs/git-status
    if attestation_file.exists() and git_maybe(
        repo, "status", "--porcelain", "--", attestation_rel
    ) != "":
        return _publish_block(f"{attestation_rel} is not committed — "
                              "commit it, then publish again", err)
    status = verification_status(repo, change_id, head=head)
    stated_error = validate_stated_status(body_file.read_text(encoding="utf-8"), status)
    if stated_error:
        return _publish_block(stated_error, err, rule="push.contextual-body")
    outcome_error = validate_disclosed_outcome(
        body_file.read_text(encoding="utf-8"),
        _no_program_reasons(repo, head, attestation_rel),
    )
    if outcome_error:
        return _publish_block(outcome_error, err, rule="push.contextual-body")
    out.write(f"Verification {status} for {head}\n")
    if status != "valid":
        clause = missing_clause(missing_records(repo, change_id, status, head))
        err.write(f"loom: verification {status}{' ' + clause if clause else ''}; "
                  "publishing anyway.\n")

    base_result = _external_or_block(
        # gh repo view accepts [HOST/]OWNER/REPO and exposes defaultBranchRef:
        # https://cli.github.com/manual/gh_repo_view
        [trusted_gh, "repo", "view", identity, "--json", "defaultBranchRef",
         "--jq", ".defaultBranchRef.name"],
        repo=repo, env=env, err=err,
    )
    if base_result is None:
        return 1
    base = base_result.stdout.strip()
    if not base or base == branch or not git_ok(repo, "check-ref-format", "--branch", base):
        return _publish_block("origin default branch is missing, unsafe, or equals the head branch", err)
    out.write(f"Publication target: {identity} base {base}\n")

    remote_result = _external_or_block(
        # Git documents ls-remote as the read-only remote-ref query:
        # https://git-scm.com/docs/git-ls-remote
        [trusted_git, "-C", str(repo), "ls-remote", "--heads", "origin",
         f"refs/heads/{branch}"], repo=repo, env=env, err=err,
    )
    if remote_result is None:
        return 1
    remote_lines = [line for line in remote_result.stdout.splitlines() if line.strip()]
    if len(remote_lines) > 1:
        return _publish_block("origin returned multiple remote branch identities", err)
    remote_head = remote_lines[0].split()[0] if remote_lines else None
    if remote_head and remote_head != head:
        if not git_ok(repo, "cat-file", "-e", f"{remote_head}^{{commit}}") or not git_ok(
            repo, "merge-base", "--is-ancestor", remote_head, head
        ):
            return _publish_block(
                "remote branch is unknown or diverged; fetch and reconcile it before publishing",
                err,
            )

    if git_text(repo, "rev-parse", "HEAD") != head:
        return _publish_block("live HEAD moved before push", err)
    current_origin, origin_error = _publish_origin_state(repo, branch)
    if origin_error or current_origin != origin_url:
        return _publish_block(
            f"publication identity changed before push: {origin_error or 'origin URL changed'}", err
        )
    if remote_head != head:
        push_result = _external_or_block(
            [trusted_git, "-C", str(repo), "push", *CANONICAL_PUSH_FLAGS,
             "origin", f"{head}:refs/heads/{branch}"],
            repo=repo, env=env, err=err,
        )
        if push_result is None:
            return 1

    verify_result = _external_or_block(
        [trusted_git, "-C", str(repo), "ls-remote", "--heads", "origin",
         f"refs/heads/{branch}"], repo=repo, env=env, err=err,
    )
    if verify_result is None:
        return 1
    verified = [line.split()[0] for line in verify_result.stdout.splitlines() if line.strip()]
    if verified != [head]:
        return _publish_block("origin branch does not resolve to the selected HEAD after push", err)
    if git_text(repo, "rev-parse", "HEAD") != head:
        return _publish_block("live HEAD moved before PR creation", err)
    current_origin, origin_error = _publish_origin_state(repo, branch)
    if origin_error or current_origin != origin_url:
        return _publish_block(
            f"publication identity changed before PR creation: "
            f"{origin_error or 'origin URL changed'}", err,
        )

    host, owner, name = identity.split("/", 2)
    # GitHub's pulls endpoint exposes both head/base repository identity and SHA:
    # https://docs.github.com/en/rest/pulls/pulls#list-pull-requests
    pulls_endpoint = (
        f"repos/{quote(owner, safe='')}/{quote(name, safe='')}/pulls"
        f"?state=open&head={quote(f'{owner}:{branch}', safe='')}"
    )
    list_result = _external_or_block(
        [trusted_gh, "api", "--hostname", host, pulls_endpoint],
        repo=repo, env=env, err=err,
    )
    if list_result is None:
        return 1
    try:
        candidates = json.loads(list_result.stdout)
    except json.JSONDecodeError as exc:
        return _publish_block(f"cannot decode existing PR response: {exc}", err)
    if not isinstance(candidates, list):
        return _publish_block("existing PR response is not a list", err)
    candidate_matches: list[tuple[str, bool]] = []
    expected_repo = f"{owner}/{name}"
    for candidate in candidates:
        try:
            candidate_url = candidate["html_url"]
            head_data, base_data = candidate["head"], candidate["base"]
            matches = (
                head_data["sha"] == head
                and head_data["repo"]["full_name"].casefold() == expected_repo.casefold()
                and base_data["ref"] == base
                and base_data["repo"]["full_name"].casefold() == expected_repo.casefold()
                and isinstance(candidate_url, str) and candidate_url.startswith("https://")
            )
        except (KeyError, TypeError, AttributeError):
            matches = False
        if not matches:
            return _publish_block(
                "existing pull request identity does not match origin, HEAD, and base; "
                "right after a push GitHub may not yet show the new commit, so "
                "retry once, and stop if it is refused again", err,
            )
        candidate_matches.append((candidate_url, bool(candidate.get("draft", False))))
    if len(candidate_matches) > 1:
        return _publish_block("multiple open pull requests match the current branch", err)

    current_origin, origin_error = _publish_origin_state(repo, branch)
    if origin_error or current_origin != origin_url:
        return _publish_block(
            f"publication identity changed before PR creation: "
            f"{origin_error or 'origin URL changed'}", err,
        )
    pre_create_remote = _external_or_block(
        [trusted_git, "-C", str(repo), "ls-remote", "--heads", "origin",
         f"refs/heads/{branch}"], repo=repo, env=env, err=err,
    )
    if pre_create_remote is None:
        return 1
    current_remote = [
        line.split()[0] for line in pre_create_remote.stdout.splitlines() if line.strip()
    ]
    if current_remote != [head]:
        return _publish_block("remote branch moved before PR creation", err)
    if git_text(repo, "rev-parse", "HEAD") != head:
        return _publish_block("live HEAD moved before PR creation", err)
    current_origin, origin_error = _publish_origin_state(repo, branch)
    if origin_error or current_origin != origin_url:
        return _publish_block(
            f"publication identity changed before PR creation: "
            f"{origin_error or 'origin URL changed'}", err,
        )

    if candidate_matches:
        pr_url, is_draft = candidate_matches[0]
        update_result = _external_or_block(
            [trusted_gh, "pr", "edit", pr_url, "--title", title,
             "--body-file", str(body_file)],
            repo=repo, env=env, err=err,
        )
        if update_result is None:
            return 1
        if git_text(repo, "rev-parse", "HEAD") != head:
            return _publish_block("live HEAD moved after PR update", err)
        current_origin, origin_error = _publish_origin_state(repo, branch)
        if origin_error or current_origin != origin_url:
            return _publish_block(
                f"publication identity changed after PR update: "
                f"{origin_error or 'origin URL changed'}", err,
            )
        post_update_remote = _external_or_block(
            [trusted_git, "-C", str(repo), "ls-remote", "--heads", "origin",
             f"refs/heads/{branch}"], repo=repo, env=env, err=err,
        )
        if post_update_remote is None:
            return 1
        updated_remote = [
            line.split()[0] for line in post_update_remote.stdout.splitlines() if line.strip()
        ]
        if updated_remote != [head]:
            return _publish_block("remote branch moved after PR update", err)
        if is_draft:
            ready_result = _external_or_block(
                [trusted_gh, "pr", "ready", pr_url],
                repo=repo, env=env, err=err,
            )
            if ready_result is None:
                return 1
            if git_text(repo, "rev-parse", "HEAD") != head:
                return _publish_block("live HEAD moved after PR readiness", err)
            current_origin, origin_error = _publish_origin_state(repo, branch)
            if origin_error or current_origin != origin_url:
                return _publish_block(
                    f"publication identity changed after PR readiness: "
                    f"{origin_error or 'origin URL changed'}", err,
                )
            post_ready_remote = _external_or_block(
                [trusted_git, "-C", str(repo), "ls-remote", "--heads", "origin",
                 f"refs/heads/{branch}"], repo=repo, env=env, err=err,
            )
            if post_ready_remote is None:
                return 1
            ready_remote = [
                line.split()[0] for line in post_ready_remote.stdout.splitlines()
                if line.strip()
            ]
            if ready_remote != [head]:
                return _publish_block("remote branch moved after PR readiness", err)
        out.write(f"PR updated and ready: {pr_url}\n")
        return _observe_required_ci(
            pr_url, trusted_gh=trusted_gh, repo=repo, env=env, out=out, err=err
        )

    create_result = _external_or_block(
        [trusted_gh, "pr", "create", "--base", base, "--head", branch,
         "--title", title, "--body-file", str(body_file)],
        repo=repo, env=env, err=err,
    )
    if create_result is None:
        return 1
    url = create_result.stdout.strip()
    if not url:
        return _publish_block("gh pr create returned no pull request URL", err)
    if git_text(repo, "rev-parse", "HEAD") != head:
        return _publish_block("live HEAD moved after PR creation", err)
    current_origin, origin_error = _publish_origin_state(repo, branch)
    if origin_error or current_origin != origin_url:
        return _publish_block(
            f"publication identity changed after PR creation: "
            f"{origin_error or 'origin URL changed'}", err,
        )
    post_create_remote = _external_or_block(
        [trusted_git, "-C", str(repo), "ls-remote", "--heads", "origin",
         f"refs/heads/{branch}"], repo=repo, env=env, err=err,
    )
    if post_create_remote is None:
        return 1
    created_remote = [
        line.split()[0] for line in post_create_remote.stdout.splitlines() if line.strip()
    ]
    if created_remote != [head]:
        return _publish_block("remote branch moved after PR creation", err)
    out.write(f"Published PR: {url}\n")
    return _observe_required_ci(
        url, trusted_gh=trusted_gh, repo=repo, env=env, out=out, err=err
    )
