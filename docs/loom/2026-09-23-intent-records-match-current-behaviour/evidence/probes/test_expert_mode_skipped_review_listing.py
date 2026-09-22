"""Adversarial probe: the expert-mode note omits Acceptance 8, which #43 also broke.

Acceptance 8 of 2026-09-14-expert-mode-step-selection says the user can list
the merged changes that skipped review. After PR #43 a reviewer skip asked
for in plain words leaves the change unattested (closing-review §5), and
`selection skipped-review` lists only merged changes whose attestation
records the skip. A plain-words reviewer skip is therefore never listed, so
Acceptance 8 no longer holds for the skip route #43 made the default. The
note names Acceptance 1, 2 and clauses of 3 and 4 as replaced, not 8.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-23-intent-records-match-current-behaviour/evidence/probes/test_expert_mode_skipped_review_listing.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import inspect
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code" / "scripts"))

from loom_checker.command_handlers import selection as selection_handler  # noqa: E402

NEGATIONS = re.compile(r"\b(?:no|not|never|nor|without|none)\b|n't", re.I)


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.:;])\s+", " ".join(text.split())) if s.strip()]


def affirms(text: str, verb: str, literal: str) -> bool:
    """True when a sentence has `verb` before `literal` and carries no negation token."""
    for sentence in sentences(text):
        index = sentence.find(literal)
        if index >= 0 and re.search(rf"\b{verb}\b", sentence[:index]) and not NEGATIONS.search(sentence):
            return True
    return False


def test_affirms_affirmativesentence_accepted() -> None:
    """Synthetic: an affirmative sentence is accepted."""
    assert affirms("Then skip it and leave the change unattested: tell the user.",
                   "leave", "the change unattested")


def test_affirms_negatedsentence_rejected() -> None:
    """Synthetic: a negated sentence is rejected."""
    assert not affirms("Never leave the change unattested.", "leave", "the change unattested")


def test_closingreview_plainwordsskip_unattested() -> None:
    """closing-review leaves a plain-words reviewer skip unattested."""
    text = (REPO / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8")
    assert affirms(text, "leave", "the change unattested")


def test_skippedreview_attestationonly_read() -> None:
    """`selection skipped-review` reads attestations only, so an unattested skip is invisible."""
    source = inspect.getsource(selection_handler._skipped_review)
    assert '["artifacts"]["attestation"]' in source
    assert '"reviewers" not in' in source
    assert "plan.md" not in source and "skipped-by-instruction" not in source


def test_expertmodenote_acceptance8_named() -> None:
    """The expert-mode note names Acceptance 8 among the lines #43 replaced or narrowed."""
    text = (REPO / "docs/loom/intent/2026-09-14-expert-mode-step-selection.md").read_text(encoding="utf-8")
    note = text.split("## Later changes", 1)[1].split("\n## ", 1)[0]
    assert re.search(r"Acceptance (?:\d+, )*(?:\d+ and )?8\b", note), (
        "the note does not say that a plain-words reviewer skip is missing from "
        "`selection skipped-review` (Acceptance 8)")
