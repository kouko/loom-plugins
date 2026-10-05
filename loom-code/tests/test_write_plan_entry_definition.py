# concern: circular entry definition lets a planner mark whatever its tests call as the module entry, so internal-function tests read as entry tests
"""Adversarial probe for write-plan's Task size entry rule.

An earlier draft read "Files marks the module entry tests call". Under time
pressure a planner marks whichever function its tests call, so an internal
helper becomes an "entry" and the closing-review `tests` row (internal =
non-entry) never fires. This probe requires the Task size paragraph to tie
the entry to its callers outside the module in an affirmative sentence.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
SKILL = REPO / "loom-code/skills/write-plan/SKILL.md"

AFFIRMATIVE_PIN = re.compile(
    r"\b(?:is|are|means|marks|names|calls?)\b[^.]*\b(?:(?:other|another) modules?|outside (?:the|its) module)\b",
    re.IGNORECASE,
)
NEGATION = re.compile(r"\b(?:not|cannot|never|no|none|without)\b|n't\b", re.IGNORECASE)


def _task_size_paragraph(text: str) -> str:
    start = text.index("**Task size.**")
    end = text.find("\n\n", start)
    return text[start:end if end != -1 else None]


def _pins_outside_callers(paragraph: str) -> bool:
    # Judge clause by clause: a negation in a sibling ";" clause must not veto
    # an affirmative pin in its own clause.
    clauses = re.split(r"(?<=[.;])\s+", " ".join(paragraph.split()))
    return any(
        "entry" in c.lower() and AFFIRMATIVE_PIN.search(c) and not NEGATION.search(c)
        for c in clauses
    )


def test_entrypin_affirmativeexample_accepted() -> None:
    """A sentence defining the entry by outside callers is accepted."""
    assert _pins_outside_callers(
        "Code tasks: Files marks the module entry, the function other modules call."
    )


def test_entrypin_negatedexample_rejected() -> None:
    """A negated sentence naming outside callers is rejected."""
    assert not _pins_outside_callers(
        "Files marks the entry, not the function other modules call."
    )


def test_entrypin_cannotnegatedexample_rejected() -> None:
    """A "cannot"-negated sentence naming outside callers is rejected."""
    assert not _pins_outside_callers(
        "Files marks the entry, which cannot be the function other modules call."
    )


def test_taskentry_skilltext_definedbyoutsidecallers() -> None:
    """write-plan Task size defines the entry by callers outside the module."""
    paragraph = _task_size_paragraph(SKILL.read_text(encoding="utf-8"))
    assert _pins_outside_callers(paragraph), (
        "write-plan Task size has no affirmative sentence tying the module "
        "entry to callers outside the module, so marking a tested internal as "
        "the entry looks compliant:\n" + paragraph
    )
