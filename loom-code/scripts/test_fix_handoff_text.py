"""Closing review hands Build every blocking finding, grouped by class (plan
W0-01; intent 2026-09-24-fix-closing-review-handoff Acceptance 1, 2, 3 and 5).

concern: false-green prose pin — a bare-substring pin passes a rule that is
negated or handed to the wrong actor, so each rule sentence is pinned with
`affirms` (actor before literal, no negation) and a weakened copy must fail.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from prose_pin import affirms, flat_prose

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "loom-code"
REVIEW = flat_prose(CODE / "skills/closing-review/SKILL.md")
RECORD = (
    "Before any fix round, pass each non-passing reviewer verdict to "
    "`loom_checker.py selection record-failure <change-id> --step reviewers --rule <verdict>`;"
)
PARA = REVIEW.split(RECORD)[0].rsplit("<!-- /gate -->", 1)[-1]

LIST_PIN = ("Before any fix begins, the main agent collects", "into one list",
            "every fatal or important finding", "the reviewers and independent acceptance testing",
            "the current functional-content digest")
WHOLE_PIN = ("Every fix starts from", "that whole list")
CLASS_PIN = ("Findings that share a defect class", "go to Build as one hand-off",
             "named in words taken from the findings themselves", "names every one of their instances")
SPLIT_PIN = ("findings of different classes go", "as separate hand-offs")
LABEL = "A verdict label such as `NEEDS_REVISION` names no class."
DISCLOSURE_PIN = ("The per-verdict failure record", "is disclosure for the pull request only")
SCOPE_PIN = ("each fix is scoped from", "this list")
PINS = (LIST_PIN, WHOLE_PIN, CLASS_PIN, SPLIT_PIN, DISCLOSURE_PIN, SCOPE_PIN)
WEAKENED = (
    ("the main agent collects", "the implementer collects"),
    ("the reviewers and independent acceptance testing", "the reviewers"),
    ("Every fix starts from", "Every fix never starts from"),
    ("go to Build as one hand-off", "never go to Build as one hand-off"),
    ("is disclosure for the pull request only", "is not disclosure for the pull request only"),
    ("each fix is scoped from", "no fix is scoped from"),
)


def test_list_covers_reviewers_and_acceptance_testing_and_no_subset_fix() -> None:
    assert affirms(PARA, *LIST_PIN) and affirms(PARA, *WHOLE_PIN)


def test_shared_class_is_one_handoff_named_from_the_findings() -> None:
    assert affirms(PARA, *CLASS_PIN) and affirms(PARA, *SPLIT_PIN)
    assert LABEL in PARA


def test_record_is_disclosure_only_and_kept_verbatim() -> None:
    assert affirms(PARA, *DISCLOSURE_PIN) and affirms(PARA, *SCOPE_PIN)
    assert RECORD in REVIEW


def test_weakened_paragraph_fails_the_pins() -> None:
    for old, new in WEAKENED:
        weakened = PARA.replace(old, new, 1)
        assert weakened != PARA, old
        assert not all(affirms(weakened, *pin) for pin in PINS), new


def test_no_gate_marker_dispatch_words_or_rule_growth() -> None:
    assert PARA and "<!-- gate" not in PARA and "Build §2" not in PARA
    for word in ("dispatch", "subagent", "new step", "extra step"):
        assert word not in PARA, word
    rules = subprocess.run(
        [sys.executable, str(CODE / "scripts/loom_checker.py"), "--list-rules"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    assert len(rules) == 26
