# concern: capture-intent's complexity-check exemption reads as covering a wording change that adds a mechanism, or critique's own questions reach the user as a second stop
"""capture-intent Step 4 item 6 — the exemption and critique's questions.

Whole-sentence pins, matched after whitespace flattening against Step 4.
"""

from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SKILL = REPO / "loom-design/skills/capture-intent/SKILL.md"
STEP_4 = "## Step 4 — Decision point ①: restate and confirm"

EXEMPTION_BOUNDARY = (
    "A wording change that adds a mechanism, field, rule or step still runs it."
)
NO_QUESTIONS_TO_USER = (
    "Answer critique's own questions from the draft intent; never put them "
    "to the user."
)


def _step_4() -> str:
    text = SKILL.read_text(encoding="utf-8")
    m = re.search(rf"^{re.escape(STEP_4)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert m, f"section {STEP_4!r} missing"
    return " ".join(m.group(0).split())


def test_wording_change_that_adds_cost_still_runs_the_check() -> None:
    assert EXEMPTION_BOUNDARY in _step_4()


def test_critique_questions_are_answered_from_the_draft_intent() -> None:
    assert NO_QUESTIONS_TO_USER in _step_4()
