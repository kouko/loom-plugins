"""Non-negotiable 2 narrow-delta-skip amendment in PRINCIPLES.md (REQ-11).

A step falls outside the quality guarantee in exactly two named cases: the
user skips it by plain instruction, or the checker proves from the branch's
committed delta that the change is narrow — the same computation that sets
the reviewer floor. Either kind of skip is disclosed on the pull request and
the attestation-level verification status there is recomputed. The
ratified-by line is appended, never rewritten.
"""
from pathlib import Path

PRINCIPLES = Path(__file__).resolve().parents[2] / "PRINCIPLES.md"

TWO_CASES_SENTENCE = (
    "A step falls outside this guarantee in two cases, and only these two: "
    "the user skips it by plain instruction, and the checker proves from the "
    "branch's committed delta that the change is narrow, which is stricter "
    "than the computation that sets the reviewer floor: the delta must "
    "also carry no file anything executes and remove no test, in which "
    "case the spec, plan, blind-run and adversarial steps are skipped "
    "with no one asked."
)
DISCLOSURE_SENTENCE = (
    "Every skip of either kind must be disclosed on the pull request, and "
    "the attestation-level verification status there is recomputed rather "
    "than claimed."
)
ORIGINAL_RATIFIED = (
    "ratified-by: kouko 2026-09-05; Fixed-choices plugin clause amended "
    "(three plugins to four, loom-memory independent) by kouko 2026-09-11; "
    "reverted (four plugins back to three, loom-memory retired into loom-workflow) "
    "by kouko 2026-09-11; reviewer-floor clause amended by kouko 2026-09-12; "
    "hosts clause amended (Antigravity CLI added) by kouko 2026-09-14; "
    "non-negotiable 2 user-skipped-steps amendment ratified by kouko 2026-09-15"
)
APPENDED_PLAIN_WORDS = "; non-negotiable 2 plain-words-skip amendment by kouko 2026-09-22"
APPENDED_NARROW_DELTA = "; non-negotiable 2 narrow-delta-skip amendment by kouko 2026-09-23"


def _text():
    return PRINCIPLES.read_text(encoding="utf-8")


def _nn2():
    return next(line for line in _text().splitlines() if line.startswith("2. "))


def test_nn2_states_pr_disclosure_and_ratified_line_appended():
    nn2 = _nn2()
    assert TWO_CASES_SENTENCE in nn2
    assert DISCLOSURE_SENTENCE in nn2
    ratified = next(line for line in _text().splitlines() if line.startswith("ratified-by:"))
    assert ratified == ORIGINAL_RATIFIED + APPENDED_PLAIN_WORDS + APPENDED_NARROW_DELTA


def test_typed_confirmation_clause_gone():
    assert "typed confirmation" not in _nn2()
    assert "explicitly skips" not in _text()
