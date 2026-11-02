# concern: A forged non-null attestation selection must not read as valid or waive any step.
"""Change identification and verification status (plan W0-02).

Spec 2026-09-22-publication-floor-moves-to-github REQ-3 and REQ-10, Design
decisions "Identifying the change without an attestation", "Verification
status — local depth / CI depth" and "Reminder content". Status is a value
callers print; it never refuses.
"""

from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

import pytest

from loom_checker import digest
from loom_checker import verification
from loom_checker.helpers import load_manifest


CHANGE = "2026-09-22-example"
INTENT = f"docs/loom/intent/{CHANGE}.md"
PLAN = f"docs/loom/{CHANGE}/plan.md"
ATTESTATION = f"docs/loom/{CHANGE}/attestation.json"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def commit(repo: Path, message: str) -> str:
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def write(repo: Path, rel: str, text: str) -> None:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def branch_repo(tmp_path: Path, branch: str = f"feat/{CHANGE}") -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    write(repo, "src.py", "VALUE = 1\n")
    write(repo, "docs/loom/KICKOFF-DEFAULTS.md",
          "- package-tests: python3 -m pytest -q — fixture (2026-09-22)\n")
    commit(repo, "initial")
    git(repo, "switch", "-q", "-c", branch)
    return repo


def confirmed_intent(repo: Path, change_id: str = CHANGE) -> None:
    write(repo, f"docs/loom/intent/{change_id}.md",
          "# Example\n\noriginator: kouko\nstatus: confirmed 2026-09-22\n")


def attestation(repo: Path, *, skip: list[str] | None = None) -> dict:
    """A content-valid attestation at HEAD; `skip` claims a v2 selection,
    which nothing can bind any more."""
    head = git(repo, "rev-parse", "HEAD")
    package = "python3 -m pytest -q"
    adversarial = "python3 src.py"
    executions = [{
        "kind": "package-tests", "command": package, "artifact": "", "result": "pass",
        "command_digest": hashlib.sha256(package.encode()).hexdigest(),
    }]
    if "adversarial" not in (skip or []):
        executions.append({
            "kind": "adversarial", "command": adversarial, "artifact": "src.py",
            "result": "pass", "command_digest": hashlib.sha256(adversarial.encode()).hexdigest(),
        })
    payload = {
        "schema": "loom-attestation/v1" if skip is None else "loom-attestation/v2",
        "change_id": CHANGE,
        "content_digest": digest.functional_content_digest(repo, head, CHANGE, load_manifest()),
        "executions": executions,
        "verdicts": [
            {"reviewer": "r1", "verdict": "PASS"}, {"reviewer": "r2", "verdict": "PASS"},
        ],
        "findings": [],
    }
    if skip is not None:
        payload["selection"] = {"confirmations": [], "skip": skip, "source": "user-typed",
                                "prior_failures": []}
        payload["intent_confirmed_sha"] = None
        payload["tested_commit"] = None
        payload["reviewed_commit"] = head
        payload["acceptance_status"] = []
    return payload


def commit_attestation(repo: Path, payload: object, rel: str = ATTESTATION) -> None:
    write(repo, rel, payload if isinstance(payload, str) else json.dumps(payload))
    commit(repo, "attestation")


# --- identification ---------------------------------------------------------


def test_branch_name_identifies_committed_intent(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    confirmed_intent(repo, "2026-09-21-other")  # a second intent does not matter
    commit(repo, "intents")
    assert verification.identify_change(repo) == (CHANGE, None)


def test_single_delta_intent_identifies_when_branch_does_not(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path, "feat/something-else")
    confirmed_intent(repo)
    commit(repo, "intent")
    assert verification.identify_change(repo) == (CHANGE, None)


def test_unidentified_branch_named(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path, "wip")
    confirmed_intent(repo)
    confirmed_intent(repo, "2026-09-21-other")
    commit(repo, "two intents")
    change_id, error = verification.identify_change(repo)
    assert change_id is None
    assert "'wip'" in error
    assert "rename the branch" in error and "commit the intent" in error


def test_attestation_must_agree_with_identified_change(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, {"change_id": "2026-09-21-other"},
                       "docs/loom/2026-09-21-other/attestation.json")
    change_id, error = verification.identify_change(repo)
    assert change_id is None
    assert "2026-09-21-other" in error and CHANGE in error


# --- status -----------------------------------------------------------------


def test_claimed_selection_is_stale(tmp_path: Path) -> None:
    """No typed confirmation exists any more, so a non-null `selection`
    matches nothing: it is stale, never `valid (skipped: ...)`."""
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, attestation(repo, skip=["adversarial"]))
    status = verification.verification_status(repo, CHANGE)
    assert status.startswith("stale (") and "selection" in status


def test_plain_attestation_is_valid(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, attestation(repo))
    assert verification.verification_status(repo, CHANGE) == "valid"


@pytest.mark.parametrize("new_confirmation", [False, True])
def test_historical_v2_and_complete_extension_keep_exact_shapes(
    tmp_path: Path, new_confirmation: bool,
) -> None:
    from loom_checker.attestation import ATTESTATION_BOOKKEEPING, validate_attestation
    from loom_checker.intent_state import intent_delivery_state
    from loom_checker.rule_checks.commit_identity import check_commit_identity
    from loom_checker.rule_checks.intent_version import intent_identity

    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    pin = None
    if new_confirmation:
        pin = intent_identity(repo / INTENT)
        write(repo, INTENT, (repo / INTENT).read_text().replace(
            "status: confirmed 2026-09-22\n", f"status: confirmed 2026-09-22\nintent_confirmed_sha: {pin}\n",
        ))
    write(repo, f"docs/loom/{CHANGE}/acceptance-test-report.md", "Historical report\n")
    write(repo, f"docs/loom/{CHANGE}/evidence/results.md", "Historical evidence\n")
    head = commit(repo, f"docs(loom): intent {CHANGE} confirmed" if new_confirmation else "historical intent")
    legacy = attestation(repo)
    legacy_manifest = dict(load_manifest(), publication_only_paths=[
        "docs/loom/<change-id>/attestation.json",
    ])
    old_digest = digest.functional_content_digest(repo, head, CHANGE, legacy_manifest)
    current_digest = legacy["content_digest"]
    assert old_digest != current_digest
    legacy.update(schema="loom-attestation/v2", selection=None, content_digest=old_digest)
    for verdict in legacy["verdicts"]:
        verdict.update(vendor="test", model="test", lens="code", findings=[])
    expanded = dict(legacy, intent_confirmed_sha=pin, tested_commit=head,
                    reviewed_commit=head, acceptance_status=[], content_digest=current_digest)
    v1 = dict(legacy, schema="loom-attestation/v1")
    del v1["selection"]
    for payload in (v1, legacy, expanded):
        allowed = payload is expanded or not new_confirmation
        assert bool(validate_attestation(repo, head, CHANGE, payload)) is not allowed
        assert bool(check_commit_identity(load_manifest(), repo, CHANGE, {}, payload, commit=head)) is not allowed
        commit_attestation(repo, payload)
        git(repo, "update-ref", "refs/remotes/origin/main", "HEAD")
        git(repo, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main")
        state, _ = intent_delivery_state(repo, CHANGE)
        assert state == ("delivered" if allowed else "active")
    for field in ATTESTATION_BOOKKEEPING:
        partial = dict(expanded)
        del partial[field]
        assert validate_attestation(repo, head, CHANGE, partial)
    unknown = dict(legacy, unexpected=True)
    assert validate_attestation(repo, head, CHANGE, unknown)


@pytest.mark.parametrize("mutation", [
    "status-mismatch", "intent-pin", "reviewed-content", "boundary-file",
    "report-provenance", "valid-report-edit", "status-list", "status-object",
])
def test_evidence_revalidation_reads_the_selected_tree(tmp_path: Path, mutation: str) -> None:
    from loom_checker.rule_checks.intent_version import intent_identity

    repo = branch_repo(tmp_path)
    base = git(repo, "rev-parse", "main")
    report = f"docs/loom/{CHANGE}/acceptance-test-report.md"
    plan = f"docs/loom/{CHANGE}/plan.md"
    intent_text = "# Example\nstatus: confirmed 2026-11-02\n\n## Acceptance\n1. Works\n"
    write(repo, INTENT, intent_text)
    pin = intent_identity(repo / INTENT)
    write(repo, INTENT, intent_text.replace(
        "status: confirmed 2026-11-02\n", f"status: confirmed 2026-11-02\nintent_confirmed_sha: {pin}\n",
    ))
    program = "tests/test_edge.py"
    plan_text = (
        "# Plan\ncharter: 1.1\n\n## Task DAG\n"
        "**W1-01 Boundary test for empty input** after: none acceptance: 1\n"
        f"- Files: `{program}`\n- Test: boundary: `{program}`\n"
        "- Risk: empty input\n\n## Risks\n1. Empty input; boundary test W1-01\n"
    )
    write(repo, plan, plan_text)
    write(repo, program, "def test_empty(): pass\n")
    tested = commit(repo, "implemented content")
    report_text = f"Tried on 2026-11-02, in a clean copy of the project at {tested}.\n\n| 1 | Works | works | tried | — |\n"
    write(repo, report, report_text)
    reviewed = commit(repo, "complete evidence")
    payload = attestation(repo)
    payload.update(schema="loom-attestation/v2", selection=None,
                   tested_commit=tested, reviewed_commit=reviewed, intent_confirmed_sha=pin,
                   acceptance_status=[{"acceptance": 1, "status": "works"}])
    commit_attestation(repo, payload)
    valid = git(repo, "rev-parse", "HEAD")
    assert verification.verification_status(repo, CHANGE, base=base, head=valid) == "valid"
    if mutation == "status-mismatch":
        write(repo, report, report_text.replace("| works |", "| partly |"))
    elif mutation == "intent-pin":
        payload["intent_confirmed_sha"] = None
    elif mutation in {"status-list", "status-object"}:
        payload["acceptance_status"][0]["status"] = [] if mutation == "status-list" else {}
    elif mutation == "reviewed-content":
        payload.update(tested_commit=base, reviewed_commit=base)
    elif mutation == "boundary-file":
        write(repo, plan, plan_text.replace(program, "tests/test_missing.py"))
        head = commit(repo, "name an absent boundary program")
        payload.update(tested_commit=head, reviewed_commit=head,
                       content_digest=digest.functional_content_digest(repo, head, CHANGE))
        write(repo, report, report_text.replace(tested, head))
    elif mutation == "report-provenance":
        write(repo, report, report_text.replace(tested, "not-a-commit"))
    else:
        write(repo, report, report_text + "\nEvidence clarification.\n")
    write(repo, ATTESTATION, json.dumps(payload))
    damaged = commit(repo, mutation)
    assert verification.verification_status(repo, CHANGE, base=base, head=valid) == "valid"
    # A good mutable checkout cannot replace the selected committed evidence.
    write(repo, report, report_text)
    write(repo, plan, plan_text)
    status = verification.verification_status(repo, CHANGE, base=base, head=damaged)
    if mutation == "valid-report-edit":
        assert status == "valid", status
    else:
        assert status.startswith("stale ("), status
        if mutation == "boundary-file":
            assert "Named boundary/probe test files" in status


def test_two_attestations_and_bad_json_are_stale(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, "{not json")
    status = verification.verification_status(repo, CHANGE)
    assert status.startswith("stale (") and "JSON" in status

    commit_attestation(repo, attestation(repo), "docs/loom/2026-09-21-other/attestation.json")
    status = verification.verification_status(repo, CHANGE)
    assert status == "stale (branch carries 2 attestations)"


def test_unparseable_recorded_command_is_stale(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    payload = attestation(repo)
    command = "python3 src.py ;"
    payload["executions"][1].update(
        command=command, command_digest=hashlib.sha256(command.encode()).hexdigest()
    )
    commit_attestation(repo, payload)
    status = verification.verification_status(repo, CHANGE)
    assert status.startswith("stale (")


def test_content_failure_is_stale_with_reason(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, attestation(repo))
    write(repo, "src.py", "VALUE = 2\n")
    commit(repo, "functional change after review")
    status = verification.verification_status(repo, CHANGE)
    assert status == (
        "stale (attestation functional content digest does not match the selected tree)"
    )


def test_explicit_base_and_head_read_committed_delta(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    base = git(repo, "rev-parse", "main")
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, attestation(repo))
    head = git(repo, "rev-parse", "HEAD")
    git(repo, "switch", "-q", "--detach", head)
    assert verification.verification_status(
        repo, CHANGE, base=base, head=head
    ) == "valid"
    assert verification.identify_change(
        repo, base=base, head=head, branch=f"fix/{CHANGE}"
    ) == (CHANGE, None)


# --- missing records --------------------------------------------------------


def test_absent_lists_missing_records(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    write(repo, INTENT, "# Example\n\nstatus: draft\n")
    commit(repo, "draft intent")
    status = verification.verification_status(repo, CHANGE)
    assert status == "absent"
    missing = verification.missing_records(repo, CHANGE, status)
    assert missing == ["confirmed intent", "plan", "attestation"]
    assert verification.missing_clause(missing) == "(missing: confirmed intent, plan, attestation)"

    confirmed_intent(repo)
    write(repo, PLAN, "# Plan\n")
    commit(repo, "confirmed with plan")
    assert verification.missing_records(repo, CHANGE, "absent") == ["attestation"]
    assert verification.missing_records(repo, CHANGE, "stale (x)") == []
    assert verification.missing_clause([]) == ""


def test_status_never_raises_without_a_branch_base(tmp_path: Path) -> None:
    repo = branch_repo(tmp_path)
    git(repo, "switch", "-q", "main")
    status = verification.verification_status(repo, CHANGE)
    assert status.startswith("stale (")
    change_id, error = verification.identify_change(repo)
    assert change_id is None and error


def test_explicit_base_diffs_from_the_fork_point_when_trunk_moved(tmp_path: Path) -> None:
    """`base` is the trunk tip at event time; another change landing on the
    trunk after the fork is not this branch's delta."""
    repo = branch_repo(tmp_path)
    confirmed_intent(repo)
    commit(repo, "intent")
    commit_attestation(repo, attestation(repo))
    git(repo, "switch", "-q", "main")
    confirmed_intent(repo, "2026-09-21-other")
    write(repo, "docs/loom/2026-09-21-other/attestation.json",
          json.dumps({"change_id": "2026-09-21-other"}))
    commit(repo, "land the other change")
    base = git(repo, "rev-parse", "main")
    head = git(repo, "rev-parse", f"feat/{CHANGE}")
    assert verification.verification_status(
        repo, CHANGE, base=base, head=head
    ) == "valid"
    assert verification.identify_change(
        repo, base=base, head=head, branch=f"feat/{CHANGE}"
    ) == (CHANGE, None)
