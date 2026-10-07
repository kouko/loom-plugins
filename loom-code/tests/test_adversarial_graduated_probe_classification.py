"""Graduated adversary probe for 2026-10-06-skill-prose-contradictions; guards against regression.
concern: the fix for contradiction 4 opens a new one by declaring a graduated probe no adversarial program while the adversarial protocol keeps it in the adversarial record.

An earlier draft of lenses.md said a probe graduated into the repository's tests "is no
longer an adversarial program but an ordinary changed test file".
adversarial.md's Recording section still lists the graduated probe as an
`adversarial` entry ("the same probe after graduation, named where the
selected commit holds it") that `finalize-review` executes and counts
against the cap and the `concern:` line. One file answers "is it an
adversarial program?" with yes, the other with no.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REFS = REPO / "loom-code/skills/closing-review/references"


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _contradicts(lenses: str, protocol: str) -> bool:
    says_not_program = "no longer an adversarial program" in lenses
    keeps_in_record = "same probe after graduation" in protocol
    return says_not_program and keeps_in_record


def test_detector_contradiction_example_caught() -> None:
    """The detector flags the yes/no pair."""
    assert _contradicts(
        "a graduated probe is no longer an adversarial program",
        "the same probe after graduation, named where it lives",
    )


def test_detector_consistent_example_accepted() -> None:
    """The detector accepts a lenses sentence that keeps the classification."""
    assert not _contradicts(
        "a graduated probe is also a changed test file, which reviewers run",
        "the same probe after graduation, named where it lives",
    )


def test_graduated_probe_lenses_and_protocol_agree() -> None:
    """lenses.md and adversarial.md give a graduated probe one classification."""
    assert not _contradicts(_flat(REFS / "lenses.md"), _flat(REFS / "adversarial.md"))
