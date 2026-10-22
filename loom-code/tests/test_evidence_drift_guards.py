"""Behaviour contract for the evidence drift guard rules.

The rules for change 2026-10-12-loom-evidence-drift-guards checked here at
the rule level: `intake.attestation-coverage` (row identity, duplicates and
Verdict parsing), `intake.commit-identity` (the v1/v2 bookkeeping split and
the functional-versus-evidence digest) and `intake.intent-version` (the pin
and its recovery path). `intake.plan-boundary-tests` keeps its tests in
test_loom_checker_intake.py.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from loom_checker.helpers import load_manifest
from loom_checker.rule_checks.commit_identity import check_commit_identity
from loom_checker.rule_checks.evidence_coverage import (
    acceptance_coverage,
    check_attestation_coverage,
)
from loom_checker.rule_checks.intent_version import (
    check_intent_version,
    intent_identity,
    recompute_command,
)

CHANGE = "2026-10-12-drift"

INTENT_SECTIONS = {"Acceptance": "1. first\n2. second\n3. third"}

INTENT_TEXT = """# A change
originator: tester
kind: engineering
needs-design: no — internal
status: confirmed 2026-10-12

## Problem
x

## Proposed outcome
y

## Acceptance
1. first
2. second
3. third

## Constraints
- none

## Out of scope
- none

## Open questions
- none
"""


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "seed.txt").write_text("seed\n", encoding="utf-8")
    git(repo, "add", "seed.txt")
    git(repo, "commit", "-q", "-m", "seed")
    return repo


def commit_files(repo: Path, files: dict[str, str], message: str) -> str:
    for rel, content in files.items():
        path = repo / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
    git(repo, "add", "-A")
    git(repo, "commit", "-q", "-m", message)
    return git(repo, "rev-parse", "HEAD")


def write_report(repo: Path, rows: str) -> Path:
    path = repo / "docs/loom" / CHANGE / "acceptance-test-report.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "# A change — what I tried and what happened\n\n"
        "Tried on 2026-10-22, in a clean copy of the project at abc1234.\n\n"
        "| # | What you asked for | Verdict | What happened | Re-run |\n"
        "|---|---|---|---|---|\n"
        f"{rows}",
        encoding="utf-8",
    )
    return path


# --- intake.attestation-coverage ---------------------------------------------


def test_coverage_fails_and_names_a_missing_line(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_report(repo, "| 1 | a | works | ok | — |\n| 2 | b | works | ok | — |\n")
    failures = check_attestation_coverage(
        load_manifest(), repo, CHANGE, INTENT_SECTIONS, {}
    )
    assert failures
    rule, message = failures[0]
    assert rule == "intake.attestation-coverage"
    assert "no row for Acceptance lines: 3" in message


def test_coverage_fails_and_names_an_extra_line(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_report(
        repo,
        "| 1 | a | works | ok | — |\n| 2 | b | works | ok | — |\n"
        "| 3 | c | works | ok | — |\n| 4 | d | works | ok | — |\n",
    )
    failures = check_attestation_coverage(
        load_manifest(), repo, CHANGE, INTENT_SECTIONS, {}
    )
    assert failures and "does not have: 4" in failures[0][1]


def test_coverage_fails_and_names_a_duplicated_line(tmp_path: Path) -> None:
    """A report whose only defect is a repeated row fails: the identity
    check counts rows, it does not collapse them into a set."""
    repo = make_repo(tmp_path)
    write_report(
        repo,
        "| 1 | a | works | ok | — |\n| 2 | b | works | ok | — |\n"
        "| 2 | b | works | ok | — |\n| 3 | c | works | ok | — |\n",
    )
    failures = check_attestation_coverage(
        load_manifest(), repo, CHANGE, INTENT_SECTIONS, {}
    )
    assert failures and "duplicate rows for Acceptance lines: 2" in failures[0][1]


def test_coverage_fails_and_names_an_unreadable_verdict(tmp_path: Path) -> None:
    """The template pins the Verdict cell to four words; a row that states
    something else has not stated a status the check can read."""
    repo = make_repo(tmp_path)
    write_report(
        repo,
        "| 1 | a | maybe | ok | — |\n| 2 | b | works | ok | — |\n"
        "| 3 | c | works | ok | — |\n",
    )
    failures = check_attestation_coverage(
        load_manifest(), repo, CHANGE, INTENT_SECTIONS, {}
    )
    assert failures and "no Verdict" in failures[0][1] and ": 1" in failures[0][1]


def test_coverage_passes_a_complete_report(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_report(
        repo,
        "| 1 | a | works | ok | — |\n| 2 | b | not verified | unrun | — |\n"
        "| 3 | c | fails | broke | — |\n",
    )
    assert check_attestation_coverage(
        load_manifest(), repo, CHANGE, INTENT_SECTIONS, {}
    ) == []


def test_coverage_passes_a_report_in_the_attestation_underscore_spelling(
    tmp_path: Path,
) -> None:
    """`not_verified` and `not verified` are the same status."""
    repo = make_repo(tmp_path)
    write_report(
        repo,
        "| 1 | a | works | ok | — |\n| 2 | b | not_verified | unrun | — |\n"
        "| 3 | c | works | ok | — |\n",
    )
    assert check_attestation_coverage(
        load_manifest(), repo, CHANGE, INTENT_SECTIONS, {}
    ) == []


def test_coverage_requires_a_report(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    failures = check_attestation_coverage(
        load_manifest(), repo, CHANGE, INTENT_SECTIONS, {}
    )
    assert failures and "acceptance test report missing" in failures[0][1]


# --- acceptance_status bookkeeping -------------------------------------------


def test_acceptance_status_reads_the_verdict_cell() -> None:
    """The attestation records what the report states, not row presence."""
    statuses = acceptance_coverage(
        INTENT_SECTIONS,
        "| 1 | a | works | ok | — |\n| 2 | b | fails | broke | — |\n"
        "| 3 | c | not verified | unrun | — |\n",
    )
    assert statuses == [
        {"acceptance": 1, "status": "works"},
        {"acceptance": 2, "status": "fails"},
        {"acceptance": 3, "status": "not_verified"},
    ]


def test_acceptance_status_shape_matches_the_validator_vocabulary() -> None:
    """Regression: the generated entries must keep the {acceptance, status}
    keys and the validator's four-word status vocabulary."""
    statuses = acceptance_coverage(
        INTENT_SECTIONS, "| 1 | a | works | ok | — |\n",
    )
    assert [sorted(entry) for entry in statuses] == [["acceptance", "status"]] * 3
    assert {
        entry["status"] for entry in statuses
    } <= {"works", "partly", "not_verified", "fails"}


def test_acceptance_status_records_not_verified_for_a_missing_row() -> None:
    statuses = acceptance_coverage(INTENT_SECTIONS, "| 1 | a | works | ok | — |\n")
    assert statuses[-1] == {"acceptance": 3, "status": "not_verified"}


# --- intake.commit-identity --------------------------------------------------


def test_commit_identity_skips_a_v1_attestation(tmp_path: Path) -> None:
    """Pre-bookkeeping attestations carry neither commit; they stay valid."""
    repo = make_repo(tmp_path)
    head = commit_files(repo, {"code.py": "a\n"}, "one")
    attestation = {"schema": "loom-attestation/v1", "content_digest": "x"}
    assert check_commit_identity(load_manifest(), repo, CHANGE, {}, attestation) == []


def test_commit_identity_fails_when_a_v2_field_is_missing(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    attestation = {"schema": "loom-attestation/v2", "tested_commit": None}
    failures = check_commit_identity(load_manifest(), repo, CHANGE, {}, attestation)
    assert failures and "missing required bookkeeping fields" in failures[0][1]


def test_commit_identity_fails_on_functional_drift(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    tested = commit_files(repo, {"code.py": "a\n"}, "tested")
    reviewed = commit_files(repo, {"code.py": "b\n"}, "reviewed")
    attestation = {
        "schema": "loom-attestation/v2",
        "tested_commit": tested, "reviewed_commit": reviewed,
    }
    failures = check_commit_identity(load_manifest(), repo, CHANGE, {}, attestation)
    assert failures and "functional content differs" in failures[0][1]
    assert tested[:7] in failures[0][1] and reviewed[:7] in failures[0][1]


def test_commit_identity_ignores_evidence_only_drift(tmp_path: Path) -> None:
    """The report and its evidence are publication-only: a difference there
    between the two commits never fails the identity check."""
    repo = make_repo(tmp_path)
    tested = commit_files(repo, {"code.py": "a\n"}, "tested")
    reviewed = commit_files(
        repo,
        {"code.py": "a\n", f"docs/loom/{CHANGE}/evidence/acceptance-test-evidence.md": "new\n"},
        "reviewed",
    )
    attestation = {
        "schema": "loom-attestation/v2",
        "tested_commit": tested, "reviewed_commit": reviewed,
    }
    assert check_commit_identity(load_manifest(), repo, CHANGE, {}, attestation) == []


def test_commit_identity_passes_identical_functional_content(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    tested = commit_files(repo, {"code.py": "a\n"}, "tested")
    reviewed = commit_files(
        repo,
        {"code.py": "a\n", f"docs/loom/{CHANGE}/acceptance-test-report.md": "report\n"},
        "reviewed",
    )
    attestation = {
        "schema": "loom-attestation/v2",
        "tested_commit": tested, "reviewed_commit": reviewed,
    }
    assert check_commit_identity(load_manifest(), repo, CHANGE, {}, attestation) == []


# --- intake.intent-version ---------------------------------------------------


def write_pinned_intent(repo: Path, *, pin: bool = True) -> Path:
    path = repo / "docs/loom/intent" / f"{CHANGE}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(INTENT_TEXT, encoding="utf-8")
    if pin:
        path.write_text(
            path.read_text(encoding="utf-8").replace(
                "status: confirmed 2026-10-12\n",
                f"status: confirmed 2026-10-12\nintent_confirmed_sha: {intent_identity(path)}\n",
            ),
            encoding="utf-8",
        )
    return path


def test_intent_version_passes_while_the_intent_is_unchanged(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    path = write_pinned_intent(repo)
    attestation = {"intent_confirmed_sha": intent_identity(path)}
    assert check_intent_version(load_manifest(), repo, CHANGE, {}, attestation) == []


def test_intent_version_fails_after_a_post_confirmation_edit(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    path = write_pinned_intent(repo)
    attestation = {"intent_confirmed_sha": intent_identity(path)}
    path.write_text(
        path.read_text(encoding="utf-8").replace("1. first", "1. first\n2. second"),
        encoding="utf-8",
    )
    failures = check_intent_version(load_manifest(), repo, CHANGE, {}, attestation)
    assert failures and "re-confirm the intent" in failures[0][1]


def test_intent_version_recovers_by_re_pinning(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    path = write_pinned_intent(repo)
    attestation = {"intent_confirmed_sha": intent_identity(path)}
    path.write_text(
        path.read_text(encoding="utf-8").replace("1. first", "1. first\n2. second"),
        encoding="utf-8",
    )
    assert check_intent_version(load_manifest(), repo, CHANGE, {}, attestation)
    attestation = {"intent_confirmed_sha": intent_identity(path)}
    assert check_intent_version(load_manifest(), repo, CHANGE, {}, attestation) == []


def test_intent_version_skips_an_unpinned_attestation(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    write_pinned_intent(repo)
    assert check_intent_version(load_manifest(), repo, CHANGE, {}, {}) == []


def test_intent_version_skips_an_unconfirmed_intent(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    path = write_pinned_intent(repo)
    path.write_text(
        path.read_text(encoding="utf-8").replace(
            "status: confirmed 2026-10-12", "status: open"
        ),
        encoding="utf-8",
    )
    attestation = {"intent_confirmed_sha": "0" * 40}
    assert check_intent_version(load_manifest(), repo, CHANGE, {}, attestation) == []


def test_intent_version_accepts_an_abbreviated_pin(tmp_path: Path) -> None:
    repo = make_repo(tmp_path)
    path = write_pinned_intent(repo)
    attestation = {"intent_confirmed_sha": intent_identity(path)[:7]}
    assert check_intent_version(load_manifest(), repo, CHANGE, {}, attestation) == []


def test_recompute_command_works_under_posix_sh(tmp_path: Path) -> None:
    """The printed fix must survive a minimal shell: no bash-only
    process substitution."""
    repo = make_repo(tmp_path)
    path = write_pinned_intent(repo)
    relative = f"docs/loom/intent/{CHANGE}.md"
    command = recompute_command(relative).split("`")[1]
    result = subprocess.run(
        ["sh", "-c", command], cwd=repo, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == intent_identity(path)
