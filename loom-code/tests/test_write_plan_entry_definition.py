# concern: circular entry definition lets a planner mark whatever its tests call as the module entry, so internal-function tests read as entry tests
"""Adversarial probe for write-plan's Task size entry rule.

An earlier draft read "Files marks the module entry tests call". Under time
pressure a planner marks whichever function its tests call, so an internal
helper becomes an "entry" and the closing-review `tests` row (internal =
non-entry) never fires. This probe requires the Task size paragraph to tie
the entry to its callers outside the module in an affirmative sentence.

Per engineering-baseline §5 item 8, it judges whole sentences and rejects
any negation token in the same sentence, ";" clauses included. A sentence
ends only before a capitalised word, so "i.e. not" stays one sentence but
"i.e. Never" splits. It is a
cheap fixed check (a tripwire), not a semantic guarantee: inversions
phrased with "rather than", "instead of" or "neither ... nor" pass it and
are left to closing-review reviewers.
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
NEGATION = re.compile(r"\b(?:not|cannot|never|no|none|without)\b|n['’]t\b", re.IGNORECASE)


def _task_size_paragraph(text: str) -> str:
    start = text.index("**Task size.**")
    end = text.find("\n\n", start)
    return text[start:end if end != -1 else None]


def _pins_outside_callers(paragraph: str) -> bool:
    sentences = re.split(r"(?<=[.!?])\s+(?=[A-Z])", " ".join(paragraph.split()))
    return any(
        "entry" in s.lower() and AFFIRMATIVE_PIN.search(s) and not NEGATION.search(s)
        for s in sentences
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


def test_entrypin_siblingclausenegation_rejected() -> None:
    """A ";" clause negating the pinned sentence is rejected."""
    assert not _pins_outside_callers(
        "Files marks the entry other modules call; it is not that function."
    )


def test_taskentry_skilltext_definedbyoutsidecallers() -> None:
    """write-plan Task size defines the entry by callers outside the module."""
    paragraph = _task_size_paragraph(SKILL.read_text(encoding="utf-8"))
    assert _pins_outside_callers(paragraph), (
        "write-plan Task size has no affirmative sentence tying the module "
        "entry to callers outside the module, so marking a tested internal as "
        "the entry looks compliant:\n" + paragraph
    )
