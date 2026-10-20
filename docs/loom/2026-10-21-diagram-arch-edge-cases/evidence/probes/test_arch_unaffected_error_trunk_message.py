"""Adversarial probe: inputs outside the three defects that raised on trunk
5e850c70 must still raise the same message (Acceptance 4, and the
Constraint "no change to inputs that hit none of the three defects").

Defect 3 is exactly an empty title, ONE one-cell body line and no
components. The change makes the widest-character floor unconditional, so
these neighbouring inputs, which raised on trunk, now render instead.
"""
# concern: Acceptance 4 regression - inputs outside defect 3 (budget-forced width, two body lines, zero-width title) raised ValueError on trunk but render on the change, so error messages are no longer byte-identical to trunk.
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-workflow/skills/loom-visualization/scripts"))

from gen_arch import render_arch  # noqa: E402

TRUNK_MESSAGE = "max_width must be positive"

CASES = [
    ({"title": "", "body": ["abc"]}, 0),
    ({"title": "", "body": ["abc"]}, 1),
    ({"title": "", "body": ["abc"]}, -5),
    ({"title": "", "body": ["x", "y"]}, None),
    ({"title": "́", "body": ["x"]}, None),
]


@pytest.mark.parametrize(
    "name,width",
    CASES,
    ids=["budget-0", "budget-1", "budget-neg", "two-one-cell-lines", "zero-width-title"],
)
def test_renderarch_unaffectedinput_raisestrunkerror(name, width):
    """An input that hit none of the three defects raises trunk's exact error."""
    with pytest.raises(ValueError) as info:
        render_arch([{"name": name, "components": []}], width=width)
    assert str(info.value) == TRUNK_MESSAGE
