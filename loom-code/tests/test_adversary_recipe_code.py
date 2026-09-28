"""The code recipe's own checks: `adversarial-code.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

No assertion here pins a sentence of the code recipe. What is left is
structure: the recipe's table names every class to draw cases from, and
adversary.md repeats none of the recipe's rules.

An edit to the code recipe that drops a case class or copies a rule into
adversary.md turns this file red and names it; an edit to the spec recipe,
to the skill-and-gate recipe or to the shared protocol does not.
"""
from __future__ import annotations

from pathlib import Path

# The reader is `prose_pin`'s, under this module's own name: the protocol's
# test module, every other recipe's and `test_build_mechanical_checks.py`
# carried byte-identical copies of it.
from prose_pin import flat_prose as _flat

ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
RECIPE = REFERENCES / "adversarial-code.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


ADVERSARIAL_CODE = _flat(RECIPE)
ADVERSARY_PROSE = _flat(ADVERSARY)


# --- Where cases come from --------------------------------------------------

# The classes the recipe tells the adversary to draw cases from, as the
# table's first column spells them.
CASE_CLASSES = (
    "Empty and absent", "Boundary", "Hostile input", "Wrong order",
    "Failure of a dependency",
)


def _case_classes_found(text: str) -> list[str]:
    return [c for c in CASE_CLASSES if f"| {c} |" in text]


def test_case_class_helper_synthetic() -> None:
    table = "| Class | The question | |---|---| | Empty and absent | zero items | | Boundary | one less |"
    assert _case_classes_found(table) == ["Empty and absent", "Boundary"]
    assert _case_classes_found("Draw them from the usual classes.") == []


def test_recipe_names_every_class_to_draw_cases_from() -> None:
    found = _case_classes_found(ADVERSARIAL_CODE)
    assert found == list(CASE_CLASSES), found


# --- One home for the code recipe's rules: adversary.md repeats none of them -

# Each fragment names one rule the code recipe owns; it lives in this file
# and nowhere in adversary.md.
PROCEDURE_FRAGMENTS = (
    "abuse or boundary cases", "surviving mutant", "wrong type",
)


def _procedure_fragments_in_both(agent: str, ref: str) -> list[str]:
    return [f for f in PROCEDURE_FRAGMENTS if f in agent and f in ref]


def test_procedure_fragments_helper_synthetic() -> None:
    ref = "Write at least three executable abuse or boundary cases: a wrong type, an empty input."
    assert _procedure_fragments_in_both("Read the reference first.", ref) == []
    duplicated = "Feed it the wrong type and see what happens."
    assert _procedure_fragments_in_both(duplicated, ref) == ["wrong type"]


def test_procedure_sentence_in_both_files_rejected() -> None:
    assert _procedure_fragments_in_both(ADVERSARY_PROSE, ADVERSARIAL_CODE) == []
