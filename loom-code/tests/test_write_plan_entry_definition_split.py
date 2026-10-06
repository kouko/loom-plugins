# concern: the entry-definition pin splits sentences at every ". ", so a negation placed after an abbreviation (i.e., e.g.) or an ellipsis escapes the same-sentence negation check and an inverted entry definition passes
"""Adversary probe for 2026-10-05-entry-pin-negation-gaps.

The change makes `_pins_outside_callers` judge whole sentences so a negation
anywhere in the pinned sentence rejects it (engineering-baseline section 5
item 8). Its splitter breaks on any "." followed by whitespace, so "i.e.",
"e.g." and "..." end a "sentence" early: the affirmative fragment before them
is judged alone and the negation after them is never seen.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
PIN_TEST = REPO / "loom-code/tests/test_write_plan_entry_definition.py"


def _pin():
    spec = importlib.util.spec_from_file_location("entry_pin", PIN_TEST)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_entrypin_negationafterabbreviation_rejected() -> None:
    """A negation after "i.e." in the pinned sentence is rejected."""
    assert not _pin()._pins_outside_callers(
        "Files marks the entry other modules call, i.e. never; it marks what its tests call."
    )


def test_entrypin_negationafterellipsis_rejected() -> None:
    """A negation after "..." in the pinned sentence is rejected."""
    assert not _pin()._pins_outside_callers(
        "Files marks the entry other modules call... not really."
    )


def test_entrypin_realtextinvertedafterabbreviation_rejected() -> None:
    """The real Task size text negated after "i.e." is rejected."""
    pin = _pin()
    paragraph = pin._task_size_paragraph(pin.SKILL.read_text(encoding="utf-8"))
    inverted = paragraph.replace(
        "the entry other modules call;", "the entry other modules call, i.e. not;"
    )
    assert inverted != paragraph
    assert not pin._pins_outside_callers(inverted)
