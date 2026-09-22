"""Non-negotiable 2 plain-words-skip amendment in PRINCIPLES.md (REQ-11).

A step the user skips by plain instruction falls outside the quality
guarantee; the skip is disclosed on the pull request and the verification
status there is recomputed. The ratified-by line is appended, never rewritten.
"""
from pathlib import Path

PRINCIPLES = Path(__file__).resolve().parents[2] / "PRINCIPLES.md"

NEW_SENTENCE = (
    "A step the user skips by plain instruction falls outside this guarantee; "
    "every such skip must be disclosed on the pull request, and the "
    "attestation-level verification status there is recomputed rather than claimed."
)
ORIGINAL_RATIFIED = (
    "ratified-by: kouko 2026-09-05; Fixed-choices plugin clause amended "
    "(three plugins to four, loom-memory independent) by kouko 2026-09-11; "
    "reverted (four plugins back to three, loom-memory retired into loom-workflow) "
    "by kouko 2026-09-11; reviewer-floor clause amended by kouko 2026-09-12; "
    "hosts clause amended (Antigravity CLI added) by kouko 2026-09-14; "
    "non-negotiable 2 user-skipped-steps amendment ratified by kouko 2026-09-15"
)
APPENDED = "; non-negotiable 2 plain-words-skip amendment by kouko 2026-09-22"


def _text():
    return PRINCIPLES.read_text(encoding="utf-8")


def _nn2():
    return next(line for line in _text().splitlines() if line.startswith("2. "))


def test_nn2_states_pr_disclosure_and_ratified_line_appended():
    assert NEW_SENTENCE in _nn2()
    ratified = next(line for line in _text().splitlines() if line.startswith("ratified-by:"))
    assert ratified == ORIGINAL_RATIFIED + APPENDED


def test_typed_confirmation_clause_gone():
    assert "typed confirmation" not in _nn2()
    assert "explicitly skips" not in _text()
