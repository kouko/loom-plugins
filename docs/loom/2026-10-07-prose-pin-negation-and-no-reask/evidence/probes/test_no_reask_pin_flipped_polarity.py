# concern: a prose pin that requires a negation token accepts a sentence flipped to the opposite rule
"""Probe: the write-plan no-reask pin must reject a re-ask rewrite.

`test_product_gate_and_merge_gate_skip_doors_asked_at_one` accepts any
sentence holding "①", "again at ②" and some negation word. A rewrite that
moves the negation off the verb ("are asked again at ②, never skipped")
flips the rule to re-asking and still satisfies the pin. Each case below
rewrites one pinned sentence of the committed text, word count unchanged,
and runs the real repository test against it; the test must fail.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/scripts"))
sys.path.insert(0, str(REPO / "loom-code/tests"))

import test_write_plan_shape_text as shape  # noqa: E402

CASES = {
    "write-plan-gate": (
        "WRITE_PLAN",
        "Doors asked at ① are not asked again at ②.",
        "Doors at ① are asked again at ②, never skipped.",
    ),
    "one-way-door-merge": (
        "ONE_WAY_DOOR",
        "a spec written later does not ask them again at ②, as they\n"
        "   were already asked at ①.",
        "a spec written later asks them again at ②, not trusting\n"
        "   that ① already asked them.",
    ),
}


@pytest.mark.parametrize("case", sorted(CASES))
def test_noReaskPin_reaskRewrite_fails(case: str, tmp_path: Path, monkeypatch) -> None:
    """The no-reask pin fails when a pinned sentence is rewritten to re-ask at ②."""
    attr, original, rewrite = CASES[case]
    source: Path = getattr(shape, attr)
    text = source.read_text(encoding="utf-8")
    assert text.count(original) == 1, f"{case}: pinned sentence moved"
    mutated = tmp_path / source.name
    mutated.write_text(text.replace(original, rewrite), encoding="utf-8")
    monkeypatch.setattr(shape, attr, mutated)
    with pytest.raises(AssertionError):
        shape.test_product_gate_and_merge_gate_skip_doors_asked_at_one()
