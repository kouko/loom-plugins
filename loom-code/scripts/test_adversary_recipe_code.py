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


def _rules(path: Path) -> str:
    """The recipe's prose, flattened, with its heading lines dropped.

    A heading is structure, not a rule, and `test_adversary_layout.py` owns
    it. Left in, it would be swept into the first sentence after it and a
    rename would break a pin that is not about names.
    """
    text = re.sub(r"^#{1,6} .*$", "", path.read_text(encoding="utf-8"), flags=re.M)
    return " ".join(re.sub(r"^> ?", "", text, flags=re.M).split())


ADVERSARIAL_CODE = _flat(RECIPE)
RULES = _rules(RECIPE)
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


# --- The rest of the rules this recipe states -------------------------------
#
# The three floor pins above cover what counts toward the floor. These cover
# the rest: which procedure applies, what a case must be, where cases come
# from, and what a case that never ran is worth. Two pin shapes, both the
# repository's own -- an affirmative verb before the pinned literal with a
# negation in the same sentence rejected, and, where the rule's own wording
# carries the negation ("is not evidence"), an exact sentence, which the
# matcher could not otherwise accept.

# name: (verb, literal, extras, affirmative example, rejected examples)
AFFIRMATIVE_PINS = {
    "code-declared-tooling-is-run-and-survivors-reported": (
        "run it over the", "changed modules and report survivors",
        ("a surviving mutant is a test that asserts nothing", "a finding against `tests`"),
        "**If the repo declares mutation or fuzz tooling** — a `mutmut`, `cosmic-ray`, "
        "`stryker` or fuzz target in its config — run it over the changed modules and "
        "report survivors: a surviving mutant is a test that asserts nothing, and a "
        "finding against `tests`.",
        ("**If the repo declares mutation or fuzz tooling** — run it over the changed "
         "modules and report survivors: a surviving mutant is not a test that asserts "
         "nothing, and a finding against `tests`.",
         "**If the repo declares mutation or fuzz tooling** — run it over the changed "
         "modules and report survivors.",
         "**If the repo declares mutation or fuzz tooling** — run it over the changed "
         "modules and report survivors: a surviving mutant is a test that asserts nothing."),
    ),
    "code-three-cases-written-run-and-recorded": (
        "write", "**at least three**",
        ("executable abuse or boundary cases against the changed behaviour",
         "run them", "record each one"),
        "**If it declares none** (the common case), write **at least three** executable "
        "abuse or boundary cases against the changed behaviour, run them, and record each one.",
        ("**If it declares none** (the common case), write **at least three** executable "
         "abuse or boundary cases against the changed behaviour, run them, and record no "
         "one.",
         "**If it declares none** (the common case), write **at least three** executable "
         "abuse or boundary cases against the changed behaviour.",
         "**If it declares none** (the common case), write a case or two against the "
         "changed behaviour, run them, and record each one."),
    ),
    "code-cases-prefer-to-live-as-real-tests": (
        "Prefer", "cases that live as real tests afterwards", (),
        "Prefer cases that live as real tests afterwards.",
        ("Prefer no cases that live as real tests afterwards.",
         "Discard cases once they have run."),
    ),
}

# name: (sentence, rewrites that must fail)
SENTENCE_PINS = {
    "code-a-case-that-only-ran-in-the-head-is-not-evidence": (
        "A case that only ran in the adversary's head is not evidence.",
        ("A case that only ran in the adversary's head is evidence.",
         "A case that only ran in the adversary's head is weak evidence.",
         "A case that only ran in the adversary's head is not always evidence."),
    ),
}

# The classes the recipe tells the adversary to draw cases from, as the
# table's first column spells them.
CASE_CLASSES = (
    "Empty and absent", "Boundary", "Hostile input", "Wrong order",
    "Failure of a dependency",
)


def _case_classes_found(text: str) -> list[str]:
    return [c for c in CASE_CLASSES if f"| {c} |" in text]


@pytest.mark.parametrize("pin", sorted(AFFIRMATIVE_PINS))
def test_affirmative_pin_helpers_synthetic(pin: str) -> None:
    verb, literal, extras, affirmative, rejected = AFFIRMATIVE_PINS[pin]
    assert _affirms(affirmative, verb, literal, *extras), pin
    assert any(has_negation(r) for r in rejected), pin
    for example in rejected:
        assert not _affirms(example, verb, literal, *extras), example


@pytest.mark.parametrize("pin", sorted(AFFIRMATIVE_PINS))
def test_recipe_affirms_the_rule(pin: str) -> None:
    verb, literal, extras, _affirmative, _rejected = AFFIRMATIVE_PINS[pin]
    assert _affirms(RULES, verb, literal, *extras), (pin, verb, literal)


@pytest.mark.parametrize("pin", sorted(SENTENCE_PINS))
def test_sentence_pin_helpers_synthetic(pin: str) -> None:
    sentence, rejected = SENTENCE_PINS[pin]
    assert _pins_exact_sentence(f"Attack the code. {sentence}", sentence), pin
    for example in rejected:
        assert not _pins_exact_sentence(f"Attack the code. {example}", sentence), example


@pytest.mark.parametrize("pin", sorted(SENTENCE_PINS))
def test_recipe_states_the_rule(pin: str) -> None:
    sentence, _rejected = SENTENCE_PINS[pin]
    assert _pins_exact_sentence(RULES, sentence), (pin, sentence)


def test_case_class_helper_synthetic() -> None:
    table = "| Class | The question | |---|---| | Empty and absent | zero items | | Boundary | one less |"
    assert _case_classes_found(table) == ["Empty and absent", "Boundary"]
    assert _case_classes_found("Draw them from the usual classes.") == []


def test_recipe_names_every_class_to_draw_cases_from() -> None:
    assert _affirms(RULES, "Draw", "them from"), RULES
    assert _case_classes_found(RULES) == list(CASE_CLASSES), _case_classes_found(RULES)


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
