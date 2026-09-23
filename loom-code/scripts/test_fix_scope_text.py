"""Every fix is scoped to its defect's class before hand-off (plan W0-01;
intent 2026-09-24-fix-the-whole-class Acceptance 1, 2 and 4).

The rule lives in Build §2 only; closing-review carries a one-sentence pointer.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from prose_pin import split_sentences

ROOT = Path(__file__).resolve().parents[2]
BUILD_TEXT = (ROOT / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
REVIEW = " ".join((ROOT / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8").split())
SECTION_2 = BUILD_TEXT.split("## 2. Implement test first", 1)[1].split("## 3.", 1)[0]
RULE = " ".join(SECTION_2.partition("Before any fix is handed to an implementer")[2].split("\n\n", 1)[0].split())
BODY_PHRASES = ("names the defect's class", "`git diff <base>...HEAD`", "the places searched")


def test_rule_names_class_search_and_acceptance_surfaces() -> None:
    for phrase in (
        "the adversary, acceptance testing, a reviewer or a failing check",
        "names the defect's class",
        "searches the change's own delta (`git diff <base>...HEAD`)",
        "every surface named by the Acceptance line the finding maps to",
        "lists every instance found, the flagged one included",
        "reaches no further than that delta and those surfaces",
    ):
        assert phrase in RULE, phrase


def test_rule_absent_from_other_station() -> None:
    for phrase in BODY_PHRASES:
        assert phrase not in REVIEW, phrase
    pointers = [s for s in split_sentences(REVIEW) if "class" in s and "Build §2" in s]
    assert len(pointers) == 1, pointers


def test_record_states_class_and_places_searched() -> None:
    assert "the hand-off and the fix's commit message each state the class and the places searched" in RULE


def test_none_found_still_recorded() -> None:
    assert "even when the flagged instance is the only one found" in RULE


def test_no_gate_marker_and_rule_count_26() -> None:
    assert "<!-- gate" not in SECTION_2
    rules = subprocess.run(
        [sys.executable, str(ROOT / "loom-code/scripts/loom_checker.py"), "--list-rules"],
        capture_output=True, text=True, check=True,
    ).stdout.splitlines()
    assert len(rules) == 26


def test_no_new_dispatch_wording() -> None:
    assert RULE
    for word in ("dispatch", "subagent", "new step", "extra step"):
        assert word not in RULE, word
