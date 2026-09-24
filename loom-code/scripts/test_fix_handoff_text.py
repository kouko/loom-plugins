"""Closing review hands Build every blocking finding, grouped by class (plan
W0-01, W0-02; intent 2026-09-24-fix-closing-review-handoff Acceptance 1, 2, 3
and 5).

concern: false-green prose pin — an ordered-words pin passes a rule that is
negated, handed to the wrong actor, or inverted by a phrase inserted between
or after its words, so each rule sentence is pinned exactly and every
weakened or insertion rewrite must fail.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from prose_pin import flat_prose, pins_exact_sentence

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "loom-code"
REVIEW = flat_prose(CODE / "skills/closing-review/SKILL.md")
RECORD = (
    "Before any fix round, pass each non-passing reviewer verdict to "
    "`loom_checker.py selection record-failure <change-id> --step reviewers --rule <verdict>`;"
)
PARA = REVIEW.split(RECORD)[0].rsplit("<!-- /gate -->", 1)[-1].strip()

SENTENCES = (
    "Before any fix begins, the main agent collects every fatal or important finding that the "
    "reviewers and independent acceptance testing returned on the current functional-content "
    "digest into one list.",
    "Every fix starts from that whole list.",
    "Findings that share a defect class, named in words taken from the findings themselves, go "
    "to Build as one hand-off that names every one of their instances;",
    "findings of different classes go as separate hand-offs.",
    "Every hand-off from the list goes to Build in the same fix round, before the reviewers resume.",
    "A verdict label such as `NEEDS_REVISION` names no class.",
    "The per-verdict failure record below is disclosure for the pull request only;",
    "each fix is scoped from this list.",
)
WEAKENED = (
    ("the main agent collects", "the implementer collects"),
    ("the reviewers and independent acceptance testing", "the reviewers"),
    ("Every fix starts from", "Every fix never starts from"),
    ("go to Build as one hand-off", "never go to Build as one hand-off"),
    ("is disclosure for the pull request only", "is not disclosure for the pull request only"),
    ("each fix is scoped from", "no fix is scoped from"),
    ("go as separate hand-offs", "go as separate hand-offs in later rounds"),
    ("in the same fix round", "in its own fix round"),
    ("Every fix starts from that whole list.",
     "Every fix starts from one finding picked from that whole list."),
    ("go to Build as one hand-off that names", "go to Build as one hand-off per finding that names"),
    ("findings of different classes go as separate hand-offs",
     "findings of different classes go in later rounds as separate hand-offs"),
    ("into one list.", "into one list per reviewer."),
    ("named in words taken from the findings themselves",
     "named in words taken from the findings themselves or from the verdict label"),
    ("is disclosure for the pull request only;",
     "is disclosure for the pull request only and the input each fix is scoped from;"),
    ("each fix is scoped from this list.", "each fix is scoped from the failure record and this list."),
    ("the reviewers and independent acceptance testing returned",
     "the reviewers and independent acceptance testing returned, once acceptance testing is skipped,"),
)


def all_pinned(text: str) -> bool:
    return all(pins_exact_sentence(text, s) for s in SENTENCES)


def test_every_rule_sentence_is_pinned_exactly_and_record_kept_verbatim() -> None:
    assert all_pinned(PARA)
    assert RECORD in REVIEW


def test_weakened_or_inserted_paragraph_fails_the_pins() -> None:
    for old, new in WEAKENED:
        weakened = PARA.replace(old, new, 1)
        assert weakened != PARA, old
        assert not all_pinned(weakened), new


def test_no_gate_marker_dispatch_words_or_rule_growth() -> None:
    assert PARA and "<!-- gate" not in PARA and "Build §2" not in PARA
    for word in ("dispatch", "subagent", "new step", "extra step", "names the defect's class",
                 "--name-only", "the places searched"):
        assert word not in PARA, word
    rules = subprocess.run(
        [sys.executable, str(CODE / "scripts/loom_checker.py"), "--list-rules"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    assert len(rules) == 26
