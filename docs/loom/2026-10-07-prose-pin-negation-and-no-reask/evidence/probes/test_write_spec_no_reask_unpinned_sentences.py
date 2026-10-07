# concern: a no-reask sentence the change added can be deleted or reversed while its contract test stays green
"""Probe: every write-spec no-reask sentence the change added is pinned.

`test_one_way_door_asked_at_decision_point_one_is_not_asked_again` pins one
exact clause in Step 3 and in ui-flows.md. Three other edits of this change
carry the same rule and are not pinned: the "What you will be asked" item 2
sentence, the `merge` gate qualifier, and "class (e) included". Each case
removes or reverses one of them in the committed SKILL.md and runs the real
repository test against it; the test must fail.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
_SPEC = importlib.util.spec_from_file_location(
    "write_spec_contract", REPO / "loom-design/tests/spec/test_write_spec_contract.py"
)
contract = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(contract)

CASES = {
    "item-2-sentence-deleted": (
        " One already\n   asked when your intent was confirmed is not asked again.",
        "",
    ),
    "merge-qualifier-dropped": (
        "this change not already asked at ① is asked once",
        "this change is asked once",
    ),
    "class-e-excluded": (
        "class (e)\n   included",
        "class (e)\n   excluded",
    ),
}


@pytest.mark.parametrize("case", sorted(CASES))
def test_writeSpecNoReaskPin_sentenceRemovedOrReversed_fails(case: str, monkeypatch) -> None:
    """The write-spec no-reask contract test fails when one added sentence is removed or reversed."""
    original, rewrite = CASES[case]
    text = contract.SKILL.read_text(encoding="utf-8")
    assert text.count(original) == 1, f"{case}: sentence moved"
    mutated = text.replace(original, rewrite)
    monkeypatch.setattr(contract, "_text", lambda: mutated)
    with pytest.raises(AssertionError):
        contract.test_one_way_door_asked_at_decision_point_one_is_not_asked_again()
