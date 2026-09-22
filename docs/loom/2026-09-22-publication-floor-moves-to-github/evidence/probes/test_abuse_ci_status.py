"""Adversarial probe: is the CI verification status ever wrong?

REQ-3: the PR-floor check recomputes `valid`, `valid (skipped: ...)`,
`absent` or `stale (...)` from committed content. The workflow passes
`--base github.event.pull_request.base.sha`, which is the trunk TIP at event
time, not the branch's fork point. The attack: move the trunk after the
branch forks (the normal state of a busy trunk) and see whether trunk-only
content is read as this branch's delta; then feed malformed claims that
must never read as plain `valid`.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-22-publication-floor-moves-to-github/evidence/probes/test_abuse_ci_status.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.command_handlers.pr_floor import cmd_pr_floor
from loom_checker.rule_checks.publish import CONTEXTUAL_PR_HEADINGS
from test_verification_status import CHANGE
from test_verification_status import attestation
from test_verification_status import branch_repo
from test_verification_status import commit
from test_verification_status import commit_attestation
from test_verification_status import confirmed_intent
from test_verification_status import git
from test_verification_status import write

OTHER = "2026-09-21-other"


def body() -> str:
    return "\n".join(f"## {h}\n\nThe {h.lower()} section says something concrete here.\n"
                     for h in CONTEXTUAL_PR_HEADINGS)


def ci_status(repo: Path, tmp_path: Path, monkeypatch) -> str:
    """Run pr-floor as the reusable workflow does: base = trunk tip, head =
    PR head, branch = head ref; return the published notice status."""
    body_file = tmp_path / "body.md"
    body_file.write_text(body(), encoding="utf-8")
    monkeypatch.delenv("GITHUB_STEP_SUMMARY", raising=False)
    monkeypatch.chdir(repo)
    out, err = io.StringIO(), io.StringIO()
    code = cmd_pr_floor(["--body-file", str(body_file),
                         "--base", git(repo, "rev-parse", "main"),
                         "--head", git(repo, "rev-parse", f"feat/{CHANGE}"),
                         "--branch", f"feat/{CHANGE}"], out, err)
    assert code == 0, err.getvalue()
    return out.getvalue().strip().split("::notice title=verification::", 1)[1]


def advance_trunk_with_other_change(repo: Path) -> None:
    """Another change lands on the trunk after this branch forked."""
    git(repo, "switch", "-q", "main")
    confirmed_intent(repo, OTHER)
    write(repo, f"docs/loom/{OTHER}/attestation.json", json.dumps({"change_id": OTHER}))
    commit(repo, "land the other change")
    git(repo, "switch", "-q", f"feat/{CHANGE}")


def attested_branch(tmp_path: Path) -> Path:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, attestation(repo))
    return repo


def test_ci_status_trunk_unmoved_valid(tmp_path: Path, monkeypatch) -> None:
    """Control: a content-valid attestation reads `valid`."""
    assert ci_status(attested_branch(tmp_path), tmp_path, monkeypatch) == "valid"


def test_ci_status_trunk_moved_still_valid(tmp_path: Path, monkeypatch) -> None:
    """The same branch after the trunk landed another loom change. Nothing on
    the branch changed, so the recomputed status must not change."""
    repo = attested_branch(tmp_path)
    advance_trunk_with_other_change(repo)
    status = ci_status(repo, tmp_path, monkeypatch)
    assert status == "valid", (
        f"trunk-only content read as this branch's delta: {status!r}")


def test_ci_status_trunk_moved_still_absent(tmp_path: Path, monkeypatch) -> None:
    """A branch with no attestation after the trunk moved must read `absent`,
    not an unidentified change."""
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    advance_trunk_with_other_change(repo)
    status = ci_status(repo, tmp_path, monkeypatch)
    assert status == "absent", f"trunk-only attestation changes the status: {status!r}"


@pytest.mark.parametrize("selection", [
    {"confirmations": [], "skip": "adversarial", "source": "user-typed", "prior_failures": []},
    {"confirmations": [], "skip": [None], "source": "user-typed", "prior_failures": []},
    {"confirmations": [], "source": "user-typed", "prior_failures": []},
    ["adversarial"],
])
def test_ci_status_malformed_skip_claim_not_plain_valid(tmp_path: Path, monkeypatch, selection) -> None:
    """A v2 attestation whose skip claim is malformed is never plain `valid`."""
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    payload = attestation(repo, skip=[])
    payload["selection"] = selection
    commit_attestation(repo, payload)
    status = ci_status(repo, tmp_path, monkeypatch)
    assert status != "valid", status


def test_ci_status_skip_claim_with_full_evidence_disclosed(tmp_path: Path, monkeypatch) -> None:
    """A claimed skip is shown even when every execution is present."""
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    payload = attestation(repo)
    payload["schema"] = "loom-attestation/v2"
    payload["selection"] = {"confirmations": [], "skip": ["blind-run"],
                            "source": "user-typed", "prior_failures": []}
    commit_attestation(repo, payload)
    assert ci_status(repo, tmp_path, monkeypatch) == "valid (skipped: blind-run)"


def test_ci_status_attestation_json_array_stale(tmp_path: Path, monkeypatch) -> None:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, "[]")
    assert ci_status(repo, tmp_path, monkeypatch).startswith("stale (")
