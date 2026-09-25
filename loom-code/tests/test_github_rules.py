"""`loom_checker.py github-rules [--print-setup]` (plan W1-06; intent Acceptance 2, 7, 8).

The probe is advisory: it reads GitHub's trunk rules with `gh api`, prints
what is missing and the setup command, never writes to GitHub, and exits 0.

No network: a fake `gh` on PATH answers each `gh api` endpoint from a JSON
fixture and logs every argv it was called with, so a test can prove no
write was attempted.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "loom_checker.py"
CONTEXT = "loom-pr-floor / PR floor"
REPO = "repos/o/r"

TEMPLATE = """\
name: loom PR floor
on:
  pull_request_target:
    types: [opened, edited, synchronize, reopened]
permissions:
  contents: read
jobs:
  loom-pr-floor:
    uses: kouko/loom-plugins/.github/workflows/loom-pr-floor-reusable.yml@main
"""

FAKE_GH = """\
#!{python}
import json, os, sys
with open(os.environ["FAKE_GH_LOG"], "a", encoding="utf-8") as log:
    log.write(json.dumps(sys.argv[1:]) + "\\n")
responses = json.load(open(os.environ["FAKE_GH_RESPONSES"], encoding="utf-8"))
args = sys.argv[1:]
if args[:2] == ["auth", "status"]:
    sys.exit(0 if args[-1] == os.environ.get("FAKE_GH_AUTH_HOST") else 1)
endpoint = next((a for a in args[1:] if a.startswith("repos/")), None)
answer = responses.get(endpoint)
if args[:1] != ["api"] or answer is None:
    sys.stderr.write("gh: Not Found (HTTP 404)\\n")
    sys.exit(1)
code, body = answer
if code == 0:
    sys.stdout.write(body if isinstance(body, str) else json.dumps(body))
else:
    sys.stderr.write(body)
sys.exit(code)
"""


def ok(body):
    return [0, body]


def fail(message):
    return [1, message]


def rule_pr(ruleset_id=1):
    return {"type": "pull_request", "ruleset_id": ruleset_id, "parameters": {}}


def rule_check(context=CONTEXT, ruleset_id=1):
    return {
        "type": "required_status_checks", "ruleset_id": ruleset_id,
        "parameters": {"required_status_checks": [{"context": context}]},
    }


def base_responses(**overrides):
    responses = {
        REPO: ok({"default_branch": "main"}),
        f"{REPO}/contents/.github/workflows/loom-pr-floor.yml?ref=main": ok(TEMPLATE),
        f"{REPO}/rules/branches/main": ok([]),
        f"{REPO}/branches/main/protection": fail("gh: Branch not protected (HTTP 404)\n"),
    }
    responses.update(overrides)
    return responses


def probe(tmp_path: Path, responses: dict, *args: str, origin="https://github.com/o/r.git"):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    if origin:
        subprocess.run(["git", "-C", str(repo), "remote", "add", "origin", origin], check=True)
    bindir = tmp_path / "bin"
    bindir.mkdir()
    gh = bindir / "gh"
    gh.write_text(FAKE_GH.format(python=sys.executable), encoding="utf-8")
    gh.chmod(0o755)
    fixture = tmp_path / "responses.json"
    fixture.write_text(json.dumps(responses), encoding="utf-8")
    log = tmp_path / "gh.log"
    log.write_text("", encoding="utf-8")
    env = {
        **os.environ,
        "PATH": os.pathsep.join([str(bindir), os.environ.get("PATH", "")]),
        "FAKE_GH_RESPONSES": str(fixture),
        "FAKE_GH_LOG": str(log),
    }
    result = subprocess.run(
        [sys.executable, str(CHECKER), "github-rules", *args],
        capture_output=True, text=True, cwd=str(repo), env=env,
    )
    calls = [json.loads(line) for line in log.read_text(encoding="utf-8").splitlines()]
    return result, calls


def assert_read_only(calls):
    for argv in calls:
        assert "-X" not in argv and "--method" not in argv, argv
        assert not any(a.startswith("--input") for a in argv), argv


def setup_json(stdout: str) -> dict:
    start = stdout.index("{")
    end = stdout.rindex("}") + 1
    return json.loads(stdout[start:end])


# --- Acceptance 2 ------------------------------------------------------------

def test_setup_json_requires_pr_with_empty_bypass(tmp_path):
    result, calls = probe(tmp_path, base_responses(), "--print-setup")
    assert result.returncode == 0, result.stderr
    assert "gh api -X POST repos/o/r/rulesets --input -" in result.stdout
    payload = setup_json(result.stdout)
    assert payload["bypass_actors"] == []
    assert payload["enforcement"] == "active"
    assert payload["conditions"]["ref_name"]["include"] == ["refs/heads/main"]
    types = [rule["type"] for rule in payload["rules"]]
    assert "pull_request" in types
    checks = next(r for r in payload["rules"] if r["type"] == "required_status_checks")
    assert checks["parameters"]["required_status_checks"] == [{"context": CONTEXT}]
    assert_read_only(calls)


def test_classic_without_enforce_admins_reported_missing(tmp_path):
    classic = {
        "required_pull_request_reviews": {"required_approving_review_count": 0},
        "enforce_admins": {"enabled": False},
        "required_status_checks": {"contexts": [CONTEXT], "checks": [{"context": CONTEXT}]},
    }
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/branches/main/protection": ok(classic),
    }))
    assert result.returncode == 0, result.stderr
    assert "loom: main does not require a pull request (administrators included)" in result.stdout
    assert "does not require the check" not in result.stdout
    assert_read_only(calls)


def test_classic_with_enforce_admins_and_check_is_satisfied(tmp_path):
    classic = {
        "required_pull_request_reviews": {"required_approving_review_count": 0},
        "enforce_admins": {"enabled": True},
        "required_status_checks": {"contexts": [CONTEXT]},
    }
    result, _calls = probe(tmp_path, base_responses(**{
        f"{REPO}/branches/main/protection": ok(classic),
    }))
    assert result.returncode == 0, result.stderr
    assert "does not require" not in result.stdout
    assert "gh api -X POST" not in result.stdout
    assert "could not confirm" not in result.stdout


def test_classic_with_pr_bypass_allowance_reported_missing(tmp_path):
    for kind in ("users", "teams", "apps"):
        classic = {
            "required_pull_request_reviews": {
                "required_approving_review_count": 0,
                "bypass_pull_request_allowances": {kind: [{"id": 1}]},
            },
            "enforce_admins": {"enabled": True},
            "required_status_checks": {"contexts": [CONTEXT]},
        }
        sub = tmp_path / kind
        sub.mkdir()
        result, _calls = probe(sub, base_responses(**{
            f"{REPO}/branches/main/protection": ok(classic),
        }))
        assert result.returncode == 0, result.stderr
        assert "loom: main does not require a pull request (administrators included)" \
            in result.stdout, kind
        assert "does not require the check" not in result.stdout, kind


# --- Acceptance 7 ------------------------------------------------------------

def test_missing_rules_listed_with_command(tmp_path):
    result, calls = probe(tmp_path, base_responses())
    assert result.returncode == 0, result.stderr
    assert "loom: main does not require a pull request (administrators included)" in result.stdout
    assert f'loom: main does not require the check "{CONTEXT}"' in result.stdout
    assert "gh api -X POST repos/o/r/rulesets --input -" in result.stdout
    assert_read_only(calls)


def test_ruleset_with_empty_bypass_satisfies_both(tmp_path):
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_pr(7), rule_check(ruleset_id=7)]),
        f"{REPO}/rulesets/7": ok({"id": 7, "bypass_actors": []}),
    }))
    assert result.returncode == 0, result.stderr
    assert "does not require" not in result.stdout
    assert "could not confirm" not in result.stdout
    assert any(f"{REPO}/rulesets/7" in argv for argv in calls)


def test_ruleset_with_bypass_actor_reports_pr_missing(tmp_path):
    result, _calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_pr(7), rule_check(ruleset_id=7)]),
        f"{REPO}/rulesets/7": ok({"id": 7, "bypass_actors": [{"actor_type": "RepositoryRole"}]}),
    }))
    assert "loom: main does not require a pull request (administrators included)" in result.stdout
    assert "does not require the check" not in result.stdout


def test_template_absent_withholds_ruleset(tmp_path):
    responses = base_responses()
    del responses[f"{REPO}/contents/.github/workflows/loom-pr-floor.yml?ref=main"]
    for args in ((), ("--print-setup",)):
        sub = tmp_path / ("setup" if args else "probe")
        sub.mkdir()
        result, calls = probe(sub, responses, *args)
        assert result.returncode == 0, result.stderr
        assert "loom: template not on main — land it first, then add the rules" in result.stdout
        assert "loom-pr-floor.yml" in result.stdout
        assert "gh api -X POST" not in result.stdout
        assert_read_only(calls)


def test_reusable_workflow_alone_is_not_the_template(tmp_path):
    reusable = "on:\n  workflow_call:\njobs:\n  loom-pr-floor:\n    runs-on: ubuntu-latest\n"
    result, _calls = probe(tmp_path, base_responses(**{
        f"{REPO}/contents/.github/workflows/loom-pr-floor.yml?ref=main": ok(reusable),
    }), "--print-setup")
    assert "loom: template not on main" in result.stdout
    assert "gh api -X POST" not in result.stdout


# --- Acceptance 8 ------------------------------------------------------------

def test_unreadable_could_not_confirm(tmp_path):
    result, _calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": fail("gh: Resource not accessible (HTTP 403)\n"),
    }))
    assert result.returncode == 0, result.stderr
    assert "loom: could not confirm GitHub rules for main (" in result.stdout
    assert "does not require" not in result.stdout


def test_no_github_remote_could_not_confirm(tmp_path):
    result, calls = probe(tmp_path, base_responses(), origin=None)
    assert result.returncode == 0, result.stderr
    assert "loom: could not confirm GitHub rules" in result.stdout
    assert "no GitHub remote" in result.stdout
    assert calls == []


def test_non_github_host_is_not_queried(tmp_path):
    result, calls = probe(tmp_path, base_responses(), origin="https://gitlab.com/o/r.git")
    assert result.returncode == 0, result.stderr
    assert result.stdout == "loom: could not confirm GitHub rules for the trunk (no GitHub remote)\n"
    assert [argv for argv in calls if argv[:1] == ["api"]] == []


def test_host_gh_is_logged_into_is_queried(tmp_path, monkeypatch):
    monkeypatch.setenv("FAKE_GH_AUTH_HOST", "ghe.example.com")
    result, calls = probe(tmp_path, base_responses(), origin="https://ghe.example.com/o/r.git")
    assert result.returncode == 0, result.stderr
    assert ["auth", "status", "--hostname", "ghe.example.com"] in calls
    assert ["api", REPO, "--hostname", "ghe.example.com"] in calls
    assert "no GitHub remote" not in result.stdout


def test_rulesets_empty_classic_unreadable_unconfirmed(tmp_path):
    result, _calls = probe(tmp_path, base_responses(**{
        f"{REPO}/branches/main/protection": fail("gh: Not Found (HTTP 404)\n"),
    }))
    assert result.returncode == 0, result.stderr
    assert "loom: could not confirm GitHub rules for main (" in result.stdout
    assert "does not require" not in result.stdout


NON_ADMIN = fail("gh: Not Found (HTTP 404)\n")


def test_check_ruleset_classic_unreadable_pr_unconfirmed(tmp_path):
    """The PR requirement may live in classic protection nobody but an admin reads."""
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_check()]),
        f"{REPO}/branches/main/protection": NON_ADMIN,
    }))
    assert result.returncode == 0, result.stderr
    assert "loom: could not confirm GitHub rules for main (" in result.stdout
    assert "does not require" not in result.stdout
    assert "gh api -X POST" not in result.stdout
    assert_read_only(calls)


def test_pr_ruleset_classic_unreadable_check_unconfirmed(tmp_path):
    result, _calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_pr(3)]),
        f"{REPO}/rulesets/3": ok({"id": 3, "bypass_actors": []}),
        f"{REPO}/branches/main/protection": NON_ADMIN,
    }))
    assert result.returncode == 0, result.stderr
    assert "loom: could not confirm GitHub rules for main (" in result.stdout
    assert "does not require" not in result.stdout


def test_malformed_shapes_could_not_confirm(tmp_path):
    cases = {
        "parameters": {f"{REPO}/rules/branches/main": ok([
            {"type": "required_status_checks", "ruleset_id": 1, "parameters": "x"}])},
        "contexts": {f"{REPO}/rules/branches/main": ok([
            {"type": "required_status_checks", "ruleset_id": 1,
             "parameters": {"required_status_checks": "x"}}])},
        "classic": {f"{REPO}/branches/main/protection": ok({
            "enforce_admins": "x", "required_status_checks": ["x"]})},
        "allowances": {f"{REPO}/branches/main/protection": ok({
            "required_pull_request_reviews": {"bypass_pull_request_allowances": {"users": "x"}},
            "enforce_admins": {"enabled": True},
            "required_status_checks": {"contexts": [CONTEXT]}})},
    }
    for name, overrides in cases.items():
        sub = tmp_path / name
        sub.mkdir()
        result, _calls = probe(sub, base_responses(**overrides))
        assert result.returncode == 0, (name, result.stderr)
        assert "loom: could not confirm GitHub rules for main (" in result.stdout, name
        assert "does not require" not in result.stdout, name


def test_unreadable_bypass_actors_could_not_confirm(tmp_path):
    result, _calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_pr(7), rule_check(ruleset_id=7)]),
        f"{REPO}/rulesets/7": ok({"id": 7}),
    }))
    assert "loom: could not confirm GitHub rules for main (" in result.stdout
    assert "does not require a pull request" not in result.stdout
