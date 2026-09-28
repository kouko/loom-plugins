"""W0-02 — a fresh `plan` lens reviewer checks each plan for a simpler shape.

One positive and one negative case per Acceptance line the task owns
(intent 2026-09-25-plan-simplicity-check, lines 1, 3 and 5).
"""
from __future__ import annotations

import re
from pathlib import Path

from prose_pin import has_negation, split_sentences

REPO = Path(__file__).resolve().parents[2]
WRITE_PLAN = REPO / "loom-code/skills/write-plan/SKILL.md"
PLAN_SIMPLICITY = REPO / "loom-code/skills/write-plan/references/plan-simplicity.md"
LENSES = REPO / "loom-code/skills/closing-review/references/lenses.md"
STATIONS = (
    WRITE_PLAN,
    REPO / "loom-design/skills/capture-intent/SKILL.md",
    REPO / "loom-design/skills/write-spec/SKILL.md",
)


def _step() -> str:
    """The `**Simplicity check.**` step: write-plan's pointer, then the reference it loads, flattened."""
    pointer = re.search(r"\*\*Simplicity check\.\*\*(.*?)\n\n", WRITE_PLAN.read_text(encoding="utf-8"), re.S)
    assert pointer, "write-plan has no **Simplicity check.** step"
    assert "references/plan-simplicity.md" in pointer.group(1)
    match = re.search(r"\*\*Simplicity check\.\*\*(.*?)(?:\n\n|\Z)", PLAN_SIMPLICITY.read_text(encoding="utf-8"), re.S)
    assert match, "plan-simplicity.md has no **Simplicity check.** step"
    return " ".join(match.group(1).split())


def test_a1_no_station_table_copy_says_no_formal_plan_review() -> None:
    for station in STATIONS:
        assert "no formal plan review" not in station.read_text(encoding="utf-8"), station


def test_a3_plan_step_names_no_loom_workflow_skill() -> None:
    assert "loom-workflow" not in _step()


def test_a5_plan_step_asks_the_user_nothing() -> None:
    user_sentences = [s for s in split_sentences(_step()) if "user" in s]
    assert all(has_negation(s) for s in user_sentences), user_sentences


def _plan_lens() -> str:
    """The `## Plan lens` section of lenses.md, flattened."""
    match = re.search(r"^## Plan lens\n(.*?)(?=^## |\Z)", LENSES.read_text(encoding="utf-8"), re.S | re.M)
    assert match, "lenses.md has no ## Plan lens section"
    return " ".join(match.group(1).split())


def test_a1_no_both_checks_pass_precondition() -> None:
    assert "After both checks pass" not in PLAN_SIMPLICITY.read_text(encoding="utf-8")


def test_a5_plan_lens_has_no_fix_round() -> None:
    assert "Return either" not in _plan_lens()
