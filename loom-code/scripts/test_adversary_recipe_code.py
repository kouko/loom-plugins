"""The code recipe's own rules: `adversarial-code.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

Every assertion here pins a sentence of the code recipe. Each one moved out
of `test_build_mechanical_checks.py` with its pinned text and its assertion
shape unchanged: a pin that pins a sentence still names the affirmative
verb before the literal and still rejects a negation of it.

An edit to the code recipe turns this file red and names it; an edit to the
spec recipe, to the skill-and-gate recipe or to the shared protocol does
not.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences as _sentences


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
RECIPE = REFERENCES / "adversarial-code.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


def _flat(path: Path) -> str:
    return " ".join(re.sub(r"^> ?", "", path.read_text(encoding="utf-8"), flags=re.M).split())


ADVERSARIAL_CODE = _flat(RECIPE)
ADVERSARY_PROSE = _flat(ADVERSARY)
# The whole procedure — protocol plus every recipe — for the one pin that
# asserts a code-recipe literal occurs once across all of it.
ADVERSARIAL_PROCEDURE = " ".join(
    (
        _flat(REFERENCES / "adversarial.md"),
        ADVERSARIAL_CODE,
        _flat(REFERENCES / "adversarial-spec.md"),
        _flat(REFERENCES / "adversarial-skill-gate.md"),
    )
)


def _affirms(text: str, verb: str, literal: str, *extras: str) -> bool:
    """Some sentence carries `verb` before `literal`, every extra, and no negation."""
    for s in _sentences(text):
        v, lit = s.find(verb), s.find(literal)
        if 0 <= v < lit and all(e in s for e in extras) and not has_negation(s):
            return True
    return False


def _pins_exact_sentence(section: str, sentence: str) -> bool:
    return _sentences(section).count(sentence) == 1


# --- The floor rules the code recipe owns -----------------------------------
#
# (doc, verb, literal, extras, affirmative example, rejected examples)

RECIPE_PINS = {
    "ref-branch-tests-excluded-from-floor": (
        "ref-code", "Reuse toward the floor counts",
        "(a) the programs the adversary committed for this change",
        ("(b) tests that exist unchanged outside this change's branch",),
        "Reuse toward the floor counts only (a) the programs the adversary committed for this "
        "change and (b) tests that exist unchanged outside this change's branch.",
        ("Reuse toward the floor counts not only (a) the programs the adversary committed for "
         "this change and (b) tests that exist unchanged outside this change's branch.",
         "Reuse toward the floor counts (a) the programs the adversary committed for this change "
         "and (b) any test on this change's branch."),
    ),
    "ref-branch-tests-named-related-coverage": (
        "ref-code", "Any other test added or changed on the branch",
        "is named as related coverage only", ("such as an implementer's pin",),
        "Any other test added or changed on the branch, such as an implementer's pin, is named "
        "as related coverage only.",
        ("Any other test added or changed on the branch, such as an implementer's pin, is not "
         "named as related coverage only.",
         "Any other test added or changed on the branch, such as an implementer's pin, counts "
         "toward the floor."),
    ),
    "ref-floor-counts-reuse": (
        "ref-code", "Reused and modified cases count", "toward the floor", (),
        "Reused and modified cases count toward the floor.",
        ("Reused and modified cases do not count toward the floor.",),
    ),
}
FLOOR_NOT_TARGET = "Three is the floor, not the target."
_PIN_DOCS = {"ref-code": ADVERSARIAL_CODE}


@pytest.mark.parametrize("pin", sorted(RECIPE_PINS))
def test_probe_maintenance_pin_helpers_synthetic(pin: str) -> None:
    _doc, verb, literal, extras, affirmative, rejected = RECIPE_PINS[pin]
    assert _affirms(affirmative, verb, literal, *extras)
    assert any(has_negation(r) for r in rejected), pin
    for example in rejected:
        assert not _affirms(example, verb, literal, *extras), example


@pytest.mark.parametrize("pin", sorted(RECIPE_PINS))
def test_adversary_probe_maintenance_rule_stated(pin: str) -> None:
    doc, verb, literal, extras, _affirmative, _rejected = RECIPE_PINS[pin]
    assert _affirms(_PIN_DOCS[doc], verb, literal, *extras), (pin, verb, literal)


def test_code_recipe_states_the_floor_once() -> None:
    assert ADVERSARIAL_PROCEDURE.count("**at least three**") == 1
    assert _pins_exact_sentence(ADVERSARIAL_CODE, FLOOR_NOT_TARGET), ADVERSARIAL_CODE


# --- One home for the code recipe's rules: adversary.md repeats none of them -

# Each fragment names one rule the code recipe owns; it lives in this file
# and nowhere in adversary.md.
PROCEDURE_FRAGMENTS = (
    "floor counts only", "as related coverage only",
    "**at least three**", "surviving mutant", "wrong type",
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
    assert [f for f in PROCEDURE_FRAGMENTS if f not in ADVERSARIAL_CODE] == []
