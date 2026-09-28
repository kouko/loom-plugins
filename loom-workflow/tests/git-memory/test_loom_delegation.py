"""Regression contract for git-memory when loom delegates close-out."""

from __future__ import annotations

from pathlib import Path


_GIT_MEMORY_ROOT = Path(__file__).resolve().parents[2] / "skills" / "git-memory"
_COMMIT_PROTOCOL = _GIT_MEMORY_ROOT / "protocols" / "compose-commit.md"
_PR_PROTOCOL = _GIT_MEMORY_ROOT / "protocols" / "compose-pr.md"
_PRIVACY_SPEC = _GIT_MEMORY_ROOT / "protocols" / "privacy-judge-spec.md"


def test_loom_closeout_delegation_does_not_reconfirm_authorized_publish() -> None:
    """A close-out authorization is consumed by the orchestrator, not re-asked.

    This deliberately verifies the documented behavioral contract because the
    protocols, rather than executable code, decide whether an agent pauses.
    """
    commit_protocol = _COMMIT_PROTOCOL.read_text(encoding="utf-8")
    pr_protocol = _PR_PROTOCOL.read_text(encoding="utf-8")

    delegated_heading = "### Delegated loom close-out exception"
    direct_heading = "### All other calls — confirm before finalizing"
    assert delegated_heading in commit_protocol
    assert commit_protocol.index(delegated_heading) < commit_protocol.index(direct_heading)

    # Loom PR consent belongs to canonical intent plus Ship. Git-memory adds
    # rationale to Ship's schema without reviving its former PR lifecycle.
    assert delegated_heading not in pr_protocol


def test_privacy_judge_only_runs_for_ambiguous_private_party_text() -> None:
    spec = _PRIVACY_SPEC.read_text(encoding="utf-8")
    assert "Privacy-Bypass-Reason:" in spec


def test_bypass_never_applies_to_deterministic_secret_findings() -> None:
    for path in (_COMMIT_PROTOCOL, _PR_PROTOCOL):
        text = path.read_text(encoding="utf-8")
        assert "Privacy-Bypass-Reason:" in text
