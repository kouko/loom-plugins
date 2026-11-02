# concern: Missing named boundary programs and post-review coverage loss must be rejected.
"""Executable attacks against boundary existence and publication revalidation."""
from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-code/scripts"))
sys.path.insert(0, str(ROOT / "loom-code/tests"))

from loom_checker import verification
from loom_checker.helpers import load_manifest
from loom_checker.rule_checks.plan_boundary_tests import check_plan_boundary_tests
from test_verification_status import (
    ATTESTATION, CHANGE, INTENT, attestation, branch_repo, commit,
    commit_attestation, write,
)


@pytest.mark.parametrize("filename", ["tests/test_missing.py", "tests/test_missing.pY"])
def test_boundary_absent_rejected(tmp_path: Path, filename: str) -> None:
    """A plan naming a missing boundary test must fail, including a near miss."""
    repo = tmp_path
    write(repo, f"docs/loom/{CHANGE}/plan.md", f"""# Plan
charter: 1.1

## Task DAG
**W1-01 Exercise boundary** boundary test after: none acceptance: 1
- Files: `{filename}`
- Test: A1 positive: accepted; boundary: `{filename}`
- Risk: empty input

## Risks
1. Empty input; boundary test W1-01 in `{filename}`
""")
    assert not (repo / filename).exists()
    assert check_plan_boundary_tests(load_manifest(), repo, CHANGE, {}, {})


@pytest.mark.parametrize("mutation", ["missing-row", "duplicate-row", "unreadable-status", "missing-tested", "unresolved-tested"])
def test_publication_damaged_rejected(tmp_path: Path, mutation: str) -> None:
    """Publication must revalidate current coverage and commit identities."""
    repo = branch_repo(tmp_path)
    write(repo, INTENT, "# Example\noriginator: kouko\nstatus: confirmed 2026-11-02\n\n## Acceptance\n1. One requirement\n")
    report = f"docs/loom/{CHANGE}/acceptance-test-report.md"
    complete = "| 1 | One requirement | works | tried | — |\n"
    write(repo, report, complete)
    head = commit(repo, "tested content and complete report")
    payload = attestation(repo)
    payload.update(schema="loom-attestation/v2", selection=None,
                   tested_commit=head, reviewed_commit=head,
                   intent_confirmed_sha=None,
                   acceptance_status=[{"acceptance": 1, "status": "works"}])
    commit_attestation(repo, payload)
    assert verification.verification_status(repo, CHANGE) == "valid"
    if mutation == "missing-row":
        write(repo, report, "No rows remain.\n")
    elif mutation == "duplicate-row":
        write(repo, report, complete * 2)
    elif mutation == "unreadable-status":
        write(repo, report, complete.replace("works", "maybe"))
    else:
        payload["tested_commit"] = None if mutation == "missing-tested" else "f" * 40
        import json
        write(repo, ATTESTATION, json.dumps(payload))
    commit(repo, f"damage {mutation}")
    status = verification.verification_status(repo, CHANGE)
    assert status.startswith("stale ("), status


def test_compatibility_existingv2_accepted(tmp_path: Path) -> None:
    """An existing seven-key v2 attestation keeps its pre-change validity."""
    repo = branch_repo(tmp_path)
    write(repo, INTENT, "# Example\noriginator: kouko\nstatus: confirmed 2026-09-22\n")
    commit(repo, "existing intent")
    payload = attestation(repo)
    payload.update(schema="loom-attestation/v2", selection=None)
    assert len(payload) == 7
    commit_attestation(repo, payload)
    status = verification.verification_status(repo, CHANGE)
    assert status == "valid", status


def test_finalization_mechanical_accepted(tmp_path: Path) -> None:
    """A mechanical narrow change may finalize without independent acceptance testing."""
    from test_selection_finalize import (
        CHANGE as change, PASSING, commit_all, finalize, make_reported_repo, review_input,
    )
    repo = make_reported_repo(tmp_path)
    (repo / f"docs/loom/{change}/acceptance-test-report.md").unlink()
    commit_all(repo, "mechanical change needs no acceptance testing")
    result = finalize(repo, review_input(tmp_path, PASSING[:1], []))
    assert result.returncode == 0, result.stderr
