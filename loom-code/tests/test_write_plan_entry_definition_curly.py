# concern: a negating contraction typed with a typographic apostrophe (can’t, isn’t) slips past the entry-definition pin, so an inverted write-plan entry definition still passes
"""Adversarial probe for the write-plan entry-definition pin (A2).

Intent A2 says the pin fails on a sentence that inverts the entry definition
with "cannot" or a similar negating contraction. The pin's NEGATION pattern
matches only the ASCII apostrophe in "n't", so the same contraction written
with U+2019 (common in Markdown typed on macOS or pasted from prose) reads as
an affirmative definition and the pin stays green.
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


def test_entrypin_curlycontractionexample_rejected() -> None:
    """A can’t-negated sentence naming outside callers is rejected."""
    assert not _pin()._pins_outside_callers(
        "Files marks the entry, which can’t be the function other modules call."
    )


def test_entrypin_curlyinvertedskilltext_rejected() -> None:
    """The real Task size text inverted with can’t is rejected."""
    pin = _pin()
    paragraph = pin._task_size_paragraph(pin.SKILL.read_text(encoding="utf-8"))
    inverted = paragraph.replace(
        "the entry other modules call", "the entry other modules can’t call"
    )
    assert inverted != paragraph, "Task size text no longer holds the pinned clause"
    assert not pin._pins_outside_callers(inverted)
