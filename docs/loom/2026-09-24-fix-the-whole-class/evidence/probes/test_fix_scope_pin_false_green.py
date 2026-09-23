"""Adversary probe for 2026-09-24-fix-the-whole-class.

concern: false-green prose pin — the committed text test
`loom-code/scripts/test_fix_scope_text.py` pins the Build §2 fix-scope rule by
bare substring, so a rule that is negated or handed to the wrong actor still
passes it.

Each case feeds a weakened copy of the real rule paragraph into the committed
test functions, unchanged, by swapping the module's RULE value. A sound pin
fails on every weakened copy. A positive control shows the unmodified rule
passes, so any failure here is caused by the mutation alone.
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))
pin = importlib.import_module("test_fix_scope_text")

RULE_TESTS = (
    pin.test_rule_names_class_search_and_acceptance_surfaces,
    pin.test_record_states_class_and_places_searched,
    pin.test_none_found_still_recorded,
    pin.test_no_new_dispatch_wording,
)

MUTATIONS = {
    "hand-off negated": (
        "The fix hand-off lists every instance found",
        "The fix hand-off never lists every instance found",
    ),
    "scoping moved off the main agent": (
        "the main agent names the defect's class",
        "the implementer names the defect's class",
    ),
    "none-found record negated": (
        "searched, even when the flagged instance is the only one found",
        "searched, but not even when the flagged instance is the only one found",
    ),
}


def _suite_passes(rule: str, monkeypatch: pytest.MonkeyPatch) -> bool:
    monkeypatch.setattr(pin, "RULE", rule)
    try:
        for check in RULE_TESTS:
            check()
    except AssertionError:
        return False
    return True


def test_fix_scope_pin_original_rule_passes(monkeypatch: pytest.MonkeyPatch) -> None:
    """Positive control: the rule as committed passes the committed pin."""
    assert _suite_passes(pin.RULE, monkeypatch)


@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_fix_scope_pin_weakened_rule_rejected(name: str, monkeypatch: pytest.MonkeyPatch) -> None:
    """A weakened rule paragraph must make the committed pin fail."""
    old, new = MUTATIONS[name]
    assert old in pin.RULE, f"mutation anchor missing from the real rule: {old!r}"
    weakened = pin.RULE.replace(old, new, 1)
    assert weakened != pin.RULE
    assert not _suite_passes(weakened, monkeypatch), (
        f"false green: the pin still passes with the rule weakened ({name}): {new!r}"
    )
