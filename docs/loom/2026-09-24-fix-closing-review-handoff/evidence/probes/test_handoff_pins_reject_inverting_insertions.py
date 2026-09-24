"""Adversarial probe: the hand-off pins accept rewrites that invert the rule.

concern: false-green prose pin — `test_fix_handoff_text.py` claims a weakened
copy of the closing-review hand-off paragraph fails its pins, but each pin
only checks that its literals occur in order in one sentence with no
negation token, so a phrase inserted between or after the literals inverts
the rule and every pin still passes.

Each case below rewrites one sentence of the paragraph so it says the
opposite of an intent Acceptance line (fix from a subset, one hand-off per
finding, defer a class to a later round, name the class from the verdict
label, scope the fix from the failure record) with no negation word. The
probe asserts that the change's own pins reject every rewrite.

Run from the repo root:

    python3 -m pytest \
        docs/loom/2026-09-24-fix-closing-review-handoff/evidence/probes/test_handoff_pins_reject_inverting_insertions.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code" / "scripts"))

from prose_pin import affirms  # noqa: E402
from test_fix_handoff_text import LABEL, PARA, PINS  # noqa: E402

INVERSIONS = (
    ("Every fix starts from that whole list.",
     "Every fix starts from one finding picked from that whole list."),
    ("go to Build as one hand-off that names",
     "go to Build as one hand-off per finding that names"),
    ("findings of different classes go as separate hand-offs",
     "findings of different classes go in later rounds as separate hand-offs"),
    ("into one list.", "into one list per reviewer."),
    ("named in words taken from the findings themselves",
     "named in words taken from the findings themselves or from the verdict label"),
    ("is disclosure for the pull request only;",
     "is disclosure for the pull request only and the input each fix is scoped from;"),
    ("each fix is scoped from this list.",
     "each fix is scoped from the failure record and this list."),
    ("the reviewers and independent acceptance testing returned",
     "the reviewers and independent acceptance testing returned, once acceptance testing is skipped,"),
)


def _passes_every_pin(text: str) -> bool:
    return all(affirms(text, *pin) for pin in PINS) and LABEL in text


@pytest.mark.parametrize(("old", "new"), INVERSIONS, ids=[n for _, n in INVERSIONS])
def test_handoff_pins_inverting_insertion_rejected(old: str, new: str) -> None:
    """A rewrite that inverts the hand-off rule without a negation word fails the pins."""
    rewritten = PARA.replace(old, new, 1)
    assert rewritten != PARA, f"stale case: {old!r} no longer in the paragraph"
    assert not _passes_every_pin(rewritten), new
