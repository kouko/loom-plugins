"""The spec recipe's own rules: `adversarial-spec.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

Two kinds of assertion, both against the working tree:

- the rules this recipe states, pinned sentence by sentence, so that an
  edit which guts one of them turns this file red and no other file;
- the one-home check that moved out of `test_build_mechanical_checks.py`,
  where the same fragment was checked against the whole procedure at once,
  so a spec-recipe edit could turn a test about the code recipe red.

Nothing here is frozen. The recipe stays free to be edited -- reworded,
extended, reordered -- and only an edit that drops or reverses a rule is
caught. What the split did, once, is `test_adversary_layout.py`'s business
and is read from git there, not from these files.
"""
from __future__ import annotations

from pathlib import Path

import pytest

# The readers and the two matchers are `prose_pin`'s, under this module's own
# names: the protocol's test module, every other recipe's and
# `test_build_mechanical_checks.py` carried byte-identical copies of them.
# `_rules` drops the heading lines: a heading is structure, not a rule, and
# `test_adversary_layout.py` owns it.
from prose_pin import (
    affirms as _affirms,
    flat_prose as _flat,
    has_negation,
    pins_exact_sentence as _pins_exact_sentence,
    rule_prose as _rules,
)


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
RECIPE = REFERENCES / "adversarial-spec.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


ADVERSARIAL_SPEC = _flat(RECIPE)
ADVERSARY_PROSE = _flat(ADVERSARY)
RULES = _rules(RECIPE)


# --- The rules this recipe states -------------------------------------------
#
# Two pin shapes, both the repository's own. A rule stated affirmatively is
# pinned as an affirmative verb before its literal, with a negation anywhere
# in the same sentence rejected. A rule whose own wording carries the
# negation -- "the author clearly did not want", "the states the spec never
# mentions" -- cannot be pinned that way, because the matcher would reject
# the rule itself; it is pinned as an exact sentence instead, which is
# stricter, and its synthetic cases show a gutted rewrite failing.

# name: (sentence, rewrites that must fail)
SENTENCE_PINS = {
    "spec-red-team-every-requirement": (
        "Red-team it: for each `REQ-<n>`, name a behaviour the requirement "
        "permits that the author clearly did not want.",
        ("Red-team it: for each `REQ-<n>`, state a behaviour the requirement "
         "allows that the author clearly did not want.",
         "Red-team it: for some `REQ-<n>`, name a behaviour the requirement "
         "permits that the author clearly did not want.",
         "Red-team it: name a behaviour the requirement permits.",
         "Red-team it: for each `REQ-<n>`, name a behaviour the requirement permits."),
    ),
    "spec-hunt-the-states-never-mentioned": (
        "Then look for the states the spec never mentions — the second user, "
        "the interrupted run, the empty account, the migration from what "
        "exists today.",
        ("Then look for the states the spec never mentions.",
         "Then consider the states the spec never mentions — the second user, "
         "the interrupted run, the empty account, the migration from what "
         "exists today.",
         "Then look for the states the spec never mentions — the second user, "
         "the interrupted run."),
    ),
}

# name: (verb, literal, extras, affirmative example, rejected examples)
AFFIRMATIVE_PINS = {
    "spec-every-finding-anchored-to-its-requirement": (
        "Each one is", "a finding with the requirement as its anchor", (),
        "Each one is a finding with the requirement as its anchor.",
        ("Each one is never a finding with the requirement as its anchor.",
         "Each one is worth a mention in the report."),
    ),
}


@pytest.mark.parametrize("pin", sorted(SENTENCE_PINS))
def test_sentence_pin_helpers_synthetic(pin: str) -> None:
    sentence, rejected = SENTENCE_PINS[pin]
    assert _pins_exact_sentence(f"Attack the spec. {sentence}", sentence), pin
    for example in rejected:
        assert not _pins_exact_sentence(f"Attack the spec. {example}", sentence), example


@pytest.mark.parametrize("pin", sorted(SENTENCE_PINS))
def test_recipe_states_the_rule(pin: str) -> None:
    sentence, _rejected = SENTENCE_PINS[pin]
    assert _pins_exact_sentence(RULES, sentence), (pin, sentence)


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


# --- One home for the spec recipe's rules: adversary.md repeats none of them -

# Each fragment names one rule the spec recipe owns; it lives in this file
# and nowhere in adversary.md.
PROCEDURE_FRAGMENTS = ("did not want",)


def _procedure_fragments_in_both(agent: str, ref: str) -> list[str]:
    return [f for f in PROCEDURE_FRAGMENTS if f in agent and f in ref]


def test_procedure_fragments_helper_synthetic() -> None:
    ref = "Name a behaviour the requirement permits that the author clearly did not want."
    assert _procedure_fragments_in_both("Read the reference first.", ref) == []
    duplicated = "Name what the author did not want."
    assert _procedure_fragments_in_both(duplicated, ref) == ["did not want"]


def test_procedure_sentence_in_both_files_rejected() -> None:
    assert _procedure_fragments_in_both(ADVERSARY_PROSE, ADVERSARIAL_SPEC) == []
    assert [f for f in PROCEDURE_FRAGMENTS if f not in ADVERSARIAL_SPEC] == []
