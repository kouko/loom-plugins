"""Adversarial probe: a body line with trailing whitespace already rendered
unbroken on trunk 5e850c70, so it hits none of the three defects and
Acceptance 4 requires byte-identical output.

The change sizes the interior from the raw body width + 1, so the trailing
space (which wrap_label drops at the trunk width) now widens the box.
"""
# concern: Acceptance 4 regression - a structured layer whose widest body line ends in whitespace was drawn unbroken on trunk, yet the change widens its box, so output is no longer byte-identical to trunk.
import pathlib
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-workflow/skills/loom-visualization/scripts"))

from gen_arch import render_arch  # noqa: E402

# Exact output of trunk 5e850c70 for each input (captured with git archive).
CASES = [
    (
        {"title": "Layer", "body": ["handles requests "]},
        "┌─────────────────┐\n│ Layer           │\n├─────────────────┤\n"
        "│ handles requests│\n├─────────────────┤\n│                 │\n"
        "└─────────────────┘",
    ),
    (
        {"title": "T", "body": ["ab "]},
        "┌───┐\n│ T │\n├───┤\n│ ab│\n├───┤\n│   │\n└───┘",
    ),
    (
        "T\nab ",
        "┌───┐\n│ T │\n├───┤\n│ ab│\n├───┤\n│   │\n└───┘",
    ),
]


@pytest.mark.parametrize("name,trunk", CASES, ids=["dict-words", "dict-short", "string"])
def test_renderarch_trailingspacebody_matchestrunk(name, trunk):
    """A body line ending in whitespace, unbroken on trunk, renders trunk's bytes."""
    assert render_arch([{"name": name, "components": []}]) == trunk
