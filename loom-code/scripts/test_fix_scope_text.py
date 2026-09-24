"""Every fix is scoped to its defect's class before hand-off (plan W0-01;
intent 2026-09-24-fix-the-whole-class Acceptance 1, 2 and 4).

concern: false-green prose pin — a bare-substring pin passed a rule that was
negated or handed to the wrong actor, so each rule sentence is pinned with
`affirms` (actor before literal, no negation); graduated adversary probe.

The rule lives in Build §2 only; closing-review and Ship carry one-sentence
pointers, and the implementer contract accepts a multi-file fix hand-off.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from prose_pin import affirms, flat_prose, split_sentences

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "loom-code"
BUILD_TEXT = (CODE / "skills/build/SKILL.md").read_text(encoding="utf-8")
REVIEW = flat_prose(CODE / "skills/closing-review/SKILL.md")
SHIP = flat_prose(CODE / "skills/ship/SKILL.md")
IMPLEMENTER = flat_prose(CODE / "agents/implementer.md")
SECTION_2 = BUILD_TEXT.split("## 2. Implement test first", 1)[1].split("## 3.", 1)[0]
RULE = " ".join(("Before any fix" + SECTION_2.partition("Before any fix")[2]).split("\n\n", 1)[0].split())

SEARCH_PIN = (
    "the main agent names", "the defect's class",
    "Before any fix is handed to an implementer or made by the main agent itself",
    "the adversary, acceptance testing, a reviewer or a failing check",
    "searches the whole content of every file the change touches",
    "(`git diff --name-only <base>...HEAD`, where `<base>` is the branch base §1 reads)",
    "every surface named by the Acceptance line the finding maps to",
)
BOUND_PIN = ("The search is bounded by", "those files and those surfaces")
RECORD_PIN = (
    "The fix hand-off lists", "every instance found, the flagged one included",
    "the hand-off and the fix's commit message each state the class and the places searched",
    "even when the flagged instance is the only one found",
)
WEAKENED = (
    ("lists every instance found", "never lists every instance found"),
    ("even when the flagged", "but not even when the flagged"),
    ("the main agent names", "the implementer names"),
)


def test_rule_names_class_search_and_acceptance_surfaces() -> None:
    assert affirms(RULE, *SEARCH_PIN)
    assert affirms(RULE, *BOUND_PIN)


def test_record_states_class_and_places_searched_even_when_none_found() -> None:
    assert affirms(RULE, *RECORD_PIN)


def test_weakened_rule_fails_the_pins() -> None:
    for old, new in WEAKENED:
        weakened = RULE.replace(old, new, 1)
        assert weakened != RULE, old
        assert not (affirms(weakened, *SEARCH_PIN) and affirms(weakened, *RECORD_PIN)), new


def test_pointers_reach_every_fix_path() -> None:
    for phrase in ("names the defect's class", "--name-only", "the places searched"):
        assert phrase not in REVIEW and phrase not in SHIP, phrase
    pointers = [s for s in split_sentences(REVIEW) if "class" in s and "Build §2" in s]
    assert len(pointers) == 1 and "the main agent" in pointers[0], pointers
    assert affirms(SHIP, "The minimum fix covers", "every instance of the defect's class", "Build §2")
    assert affirms(IMPLEMENTER, "In a fix hand-off", "the task's scope", "the instances it lists and their files")
    assert "never silently widen the work" in IMPLEMENTER


def test_no_gate_marker_rule_count_26_or_dispatch_wording() -> None:
    assert "<!-- gate" not in SECTION_2
    rules = subprocess.run(
        [sys.executable, str(CODE / "scripts/loom_checker.py"), "--list-rules"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    assert len(rules) == 26
    for word in ("dispatch", "subagent", "new step", "extra step"):
        assert word not in RULE, word
