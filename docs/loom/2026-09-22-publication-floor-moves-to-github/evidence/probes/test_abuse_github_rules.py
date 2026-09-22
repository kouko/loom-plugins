"""Adversarial probe: is the `github-rules` probe ever wrong?

REQ-7 and REQ-8: Ship prints what is missing only when it is known to be
missing; when the rules cannot be read or decided it prints "could not
confirm" and continues. Classic branch protection is readable only by
admins, and the `rules/branches` endpoint shows rulesets only. The attack:
a ruleset that covers one requirement while the other could still live in
unreadable classic protection, and a malformed API response. A fake `gh`
answers from fixtures; nothing reaches the network and nothing writes.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-22-publication-floor-moves-to-github/evidence/probes/test_abuse_github_rules.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from test_github_rules import REPO
from test_github_rules import assert_read_only
from test_github_rules import base_responses
from test_github_rules import fail
from test_github_rules import ok
from test_github_rules import probe
from test_github_rules import rule_check
from test_github_rules import rule_pr

NON_ADMIN = fail("gh: Not Found (HTTP 404)\n")  # classic protection, caller is not an admin


def test_github_rules_check_ruleset_classic_unreadable_unconfirmed(tmp_path: Path) -> None:
    """A ruleset requires the loom check but has no pull-request rule; classic
    protection (which may require pull requests) is unreadable. The PR
    requirement cannot be decided, so it must not be reported missing."""
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_check()]),
        f"{REPO}/branches/main/protection": NON_ADMIN,
    }))
    assert_read_only(calls)
    assert result.returncode == 0, result.stderr
    assert "does not require a pull request" not in result.stdout, (
        "reported 'missing' for a requirement that may live in unreadable classic "
        "protection:\n" + result.stdout)
    assert "could not confirm" in result.stdout


def test_github_rules_pr_ruleset_classic_unreadable_unconfirmed(tmp_path: Path) -> None:
    """A bypass-free ruleset requires pull requests but not the check; the
    check could be a classic required context nobody but an admin can read."""
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_pr(3)]),
        f"{REPO}/rulesets/3": ok({"id": 3, "bypass_actors": []}),
        f"{REPO}/branches/main/protection": NON_ADMIN,
    }))
    assert_read_only(calls)
    assert result.returncode == 0, result.stderr
    assert "does not require the check" not in result.stdout, (
        "reported the check 'missing' while classic protection is unreadable:\n"
        + result.stdout)
    assert "could not confirm" in result.stdout


def test_github_rules_malformed_rule_parameters_unconfirmed(tmp_path: Path) -> None:
    """A response the probe cannot decode is 'could not confirm' and exit 0,
    never an internal error that stops Ship."""
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([{"type": "required_status_checks",
                                            "ruleset_id": 1, "parameters": "x"}]),
    }))
    assert_read_only(calls)
    assert result.returncode == 0, result.stderr
    assert "could not confirm" in result.stdout, result.stdout + result.stderr


def test_github_rules_wrong_trigger_template_absent(tmp_path: Path) -> None:
    """Control: a trunk workflow with the job id but a `pull_request` trigger
    is not the template (a PR could rewrite it), so the ruleset is withheld."""
    wrong = ("on: [pull_request]\npermissions:\n  contents: read\n"
             "jobs:\n  loom-pr-floor:\n    runs-on: ubuntu-latest\n    steps: []\n")
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/contents/.github/workflows/loom-pr-floor.yml?ref=main": ok(wrong),
    }), "--print-setup")
    assert_read_only(calls)
    assert "template not on main" in result.stdout
    assert "rulesets --input" not in result.stdout


def test_github_rules_both_present_configured(tmp_path: Path) -> None:
    """Control: bypass-free PR rule plus the check reads as configured."""
    result, calls = probe(tmp_path, base_responses(**{
        f"{REPO}/rules/branches/main": ok([rule_pr(5), rule_check(ruleset_id=5)]),
        f"{REPO}/rulesets/5": ok({"id": 5, "bypass_actors": []}),
        f"{REPO}/branches/main/protection": NON_ADMIN,
    }))
    assert_read_only(calls)
    assert "requires a pull request (administrators included)" in result.stdout
    assert "could not confirm" not in result.stdout
