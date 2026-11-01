"""Build advances to Closing Review after its required checks pass."""

from pathlib import Path

from prose_pin import affirms


ROOT = Path(__file__).resolve().parents[2]
BUILD = ROOT / "loom-code/skills/build/SKILL.md"


def _handoff() -> str:
    return " ".join(BUILD.read_text(encoding="utf-8").split("## 4. Hand off to closing-review", 1)[1].split())


def test_passing_build_calls_closing_review_in_same_turn() -> None:
    handoff = _handoff()
    assert affirms(
        handoff, "call", "`loom-code:closing-review`", "same turn",
        "functional changes", "package suite", "adversarial programs",
    )


def test_progress_only_handoff_is_incomplete() -> None:
    handoff = _handoff()
    assert "progress report" in handoff
    assert "does not complete the hand-off" in handoff


def test_failed_required_checks_still_block_review() -> None:
    handoff = _handoff()
    assert "failed required check" in handoff
    assert "blocks dependent review" in handoff
