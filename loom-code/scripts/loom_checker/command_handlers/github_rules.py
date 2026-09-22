"""`github-rules [--print-setup]`: advisory probe of the trunk's GitHub rules.

Ship calls it before publishing. It reads, with `gh api`, whether the trunk
requires a pull request (administrators included) and the loom PR-floor
check, prints what is missing and the one command that would add it, and
never changes anything on GitHub. It has no rule id and always exits 0 --
an unreadable or undecidable answer is "could not confirm", never "missing".
"""
from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import repo_root
from loom_checker.rule_checks.push import github_repo_from_origin
from pathlib import Path
import json
import shutil
import subprocess
import sys

import yaml


# Manual pages this module relies on:
# gh api --hostname / -H: https://cli.github.com/manual/gh_api
# gh auth status --hostname: https://cli.github.com/manual/gh_auth_status
# rules for a branch (read access): https://docs.github.com/rest/repos/rules#get-rules-for-a-branch
# a ruleset's bypass_actors: https://docs.github.com/rest/repos/rules#get-a-repository-ruleset
# classic protection (admin only): https://docs.github.com/rest/branches/branch-protection#get-branch-protection
# create a ruleset: https://docs.github.com/rest/repos/rules#create-a-repository-ruleset


REQUIRED_CONTEXT = "loom-pr-floor / PR floor"
TEMPLATE_PATH = ".github/workflows/loom-pr-floor.yml"
TEMPLATE_JOB = "loom-pr-floor"
PLUGIN_TEMPLATE = Path(__file__).resolve().parents[3] / "templates" / "loom-pr-floor.yml"
GH_TIMEOUT = 30


class Unconfirmed(Exception):
    """The answer could not be read or decided; the message is the reason."""


def run_gh(argv: list[str]) -> subprocess.CompletedProcess:
    """Run one read-only `gh` argv."""
    return subprocess.run(argv, capture_output=True, text=True, timeout=GH_TIMEOUT)


def _api(gh: str, host: str, path: str, raw: bool = False) -> tuple[bool, str]:
    """(succeeded, stdout on success else the error text)."""
    argv = [gh, "api", path, "--hostname", host]
    if raw:
        argv += ["-H", "Accept: application/vnd.github.raw"]
    try:
        result = run_gh(argv)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Unconfirmed(f"gh did not run: {type(exc).__name__}")
    if result.returncode == 0:
        return True, result.stdout
    return False, (result.stderr or result.stdout or f"exit {result.returncode}").strip()


def _json(gh: str, host: str, path: str):
    succeeded, text = _api(gh, host, path)
    if not succeeded:
        raise Unconfirmed(f"{path}: {text}")
    try:
        return json.loads(text)
    except ValueError:
        raise Unconfirmed(f"{path}: unreadable response")


def _template_on_trunk(gh: str, host: str, slug: str, trunk: str) -> bool:
    """True when the trunk head carries the caller workflow: triggered by
    `pull_request_target` with job id `loom-pr-floor`. Absent is False;
    unreadable raises Unconfirmed."""
    path = f"{slug}/contents/{TEMPLATE_PATH}?ref={trunk}"
    succeeded, text = _api(gh, host, path, raw=True)
    if not succeeded:
        if "HTTP 404" in text:
            return False
        raise Unconfirmed(f"{path}: {text}")
    try:
        workflow = yaml.safe_load(text)
    except yaml.YAMLError:
        return False
    if not isinstance(workflow, dict):
        return False
    # YAML 1.1 reads a bare `on:` key as boolean True.
    triggers = workflow.get("on", workflow.get(True))
    if isinstance(triggers, str):
        triggers = [triggers]
    jobs = workflow.get("jobs")
    return (
        isinstance(triggers, (list, dict)) and "pull_request_target" in triggers
        and isinstance(jobs, dict) and TEMPLATE_JOB in jobs
    )


def _ruleset_state(gh: str, host: str, slug: str, rules: list) -> tuple[str, bool]:
    """(pull-request state 'present' | 'absent' | 'unconfirmed', check present)."""
    pr_state = "absent"
    check = False
    for rule in rules:
        if not isinstance(rule, dict):
            continue
        if rule.get("type") == "required_status_checks":
            parameters = rule.get("parameters") or {}
            contexts = (
                parameters.get("required_status_checks") or []
                if isinstance(parameters, dict) else None
            )
            if not isinstance(contexts, list):
                raise Unconfirmed("unreadable required status checks rule")
            check = check or any(
                isinstance(c, dict) and c.get("context") == REQUIRED_CONTEXT for c in contexts
            )
        if rule.get("type") == "pull_request" and pr_state != "present":
            try:
                ruleset = _json(gh, host, f"{slug}/rulesets/{rule.get('ruleset_id')}")
            except Unconfirmed:
                pr_state = "unconfirmed"
                continue
            bypass = ruleset.get("bypass_actors") if isinstance(ruleset, dict) else None
            if bypass == []:
                pr_state = "present"
            elif bypass is None:
                pr_state = "unconfirmed"
    return pr_state, check


def _classic_state(gh: str, host: str, slug: str, trunk: str) -> tuple[bool, bool] | None:
    """(pull request with administrators, check) from classic protection, or
    None when it cannot be read (it needs admin access)."""
    path = f"{slug}/branches/{trunk}/protection"
    succeeded, text = _api(gh, host, path)
    if not succeeded:
        return (False, False) if "Branch not protected" in text else None
    try:
        protection = json.loads(text)
    except ValueError:
        return None
    if not isinstance(protection, dict):
        return None
    try:
        pr = bool(protection.get("required_pull_request_reviews")) and bool(
            (protection.get("enforce_admins") or {}).get("enabled") is True
        )
        checks = protection.get("required_status_checks") or {}
        contexts = list(checks.get("contexts") or []) + [
            c.get("context") for c in checks.get("checks") or [] if isinstance(c, dict)
        ]
    except (AttributeError, TypeError):
        return None  # a malformed response is as unreadable as a refused one
    return pr, REQUIRED_CONTEXT in contexts


def setup_command(host: str, slug: str, trunk: str) -> str:
    """The one command that would add both rules; printed, never run here."""
    ruleset = {
        "name": "loom publication floor",
        "target": "branch",
        "enforcement": "active",
        "conditions": {"ref_name": {"include": [f"refs/heads/{trunk}"], "exclude": []}},
        "bypass_actors": [],
        "rules": [
            {"type": "pull_request", "parameters": {
                "required_approving_review_count": 0,
                "dismiss_stale_reviews_on_push": False,
                "require_code_owner_review": False,
                "require_last_push_approval": False,
                "required_review_thread_resolution": False,
            }},
            {"type": "required_status_checks", "parameters": {
                "strict_required_status_checks_policy": False,
                "required_status_checks": [{"context": REQUIRED_CONTEXT}],
            }},
        ],
    }
    hostname = "" if host == "github.com" else f" --hostname {host}"
    return (
        f"gh api -X POST {slug}/rulesets --input -{hostname} <<'JSON'\n"
        f"{json.dumps(ruleset, indent=2)}\nJSON\n"
    )


def template_step(trunk: str) -> str:
    return (
        f"loom: template not on {trunk} — land it first, then add the rules\n"
        f"  copy {PLUGIN_TEMPLATE} to {TEMPLATE_PATH}, land it on {trunk}, "
        f"then run: loom_checker.py github-rules --print-setup\n"
    )


def _gh_knows_host(gh: str, host: str) -> bool:
    """True when gh is logged into `host` (a GitHub Enterprise host)."""
    try:
        return run_gh([gh, "auth", "status", "--hostname", host]).returncode == 0
    except (OSError, subprocess.TimeoutExpired):
        return False


def _probe(print_setup: bool) -> str:
    trunk = "the trunk"
    try:
        target = github_repo_from_origin(repo_root(Path.cwd()))
        if target is None:
            raise Unconfirmed("no GitHub remote")
        host, owner, name = target.split("/", 2)
        slug = f"repos/{owner}/{name}"
        gh = shutil.which("gh")
        if gh is None:
            raise Unconfirmed("gh not installed")
        if host != "github.com" and not _gh_knows_host(gh, host):
            raise Unconfirmed("no GitHub remote")
        repository = _json(gh, host, slug)
        trunk = repository.get("default_branch") if isinstance(repository, dict) else None
        if not isinstance(trunk, str) or not trunk:
            trunk = "the trunk"
            raise Unconfirmed("no default branch")
        if not _template_on_trunk(gh, host, slug, trunk):
            return template_step(trunk)
        if print_setup:
            return setup_command(host, slug, trunk)
        rules = _json(gh, host, f"{slug}/rules/branches/{trunk}")
        if not isinstance(rules, list):
            raise Unconfirmed("unreadable rules response")
        pr_state, check = _ruleset_state(gh, host, slug, rules)
        classic = _classic_state(gh, host, slug, trunk)
    except (Unconfirmed, UsageError) as exc:
        return f"loom: could not confirm GitHub rules for {trunk} ({exc})\n"

    if classic is not None:
        if classic[0]:
            pr_state = "present"
        check = check or classic[1]
    lines = []
    unconfirmed = []
    if pr_state == "unconfirmed":
        unconfirmed.append("bypass actors unreadable")
    # Classic protection may hold what the rulesets lack; unreadable, a
    # requirement the rulesets do not satisfy is undecided, never missing.
    if classic is None and (pr_state != "present" or not check):
        unconfirmed.append("classic protection unreadable")
    if unconfirmed:
        lines.append(f"loom: could not confirm GitHub rules for {trunk} ({'; '.join(unconfirmed)})\n")
    missing = False
    if pr_state == "absent" and classic is not None:
        lines.append(f"loom: {trunk} does not require a pull request (administrators included)\n")
        missing = True
    if not check and classic is not None:
        lines.append(f'loom: {trunk} does not require the check "{REQUIRED_CONTEXT}"\n')
        missing = True
    if missing:
        lines.append(setup_command(host, slug, trunk))
    if not lines:
        lines.append(
            f'loom: {trunk} requires a pull request (administrators included) '
            f'and the check "{REQUIRED_CONTEXT}"\n'
        )
    return "".join(lines)


def cmd_github_rules(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    """Advisory: print the trunk's rule state and setup; always exit 0."""
    if args not in ([], ["--print-setup"]):
        raise UsageError("usage: loom_checker.py github-rules [--print-setup]")
    out.write(_probe(print_setup=bool(args)))
    return 0
