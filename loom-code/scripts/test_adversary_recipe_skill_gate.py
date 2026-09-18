"""The skill-and-gate recipe's own rules: `adversarial-skill-gate.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

Two kinds of assertion, both against the working tree:

- the rules this recipe states, pinned attempt by attempt, so that an edit
  which guts one of them turns this file red and no other file;
- the one-home check that moved out of `test_build_mechanical_checks.py`,
  where the same fragments were checked against the whole procedure at
  once, so a skill-and-gate edit could turn a test about another recipe
  red.

Nothing here is frozen. The recipe stays free to be edited -- reworded,
extended, reordered -- and only an edit that drops or reverses a rule is
caught. What the split did, once, is `test_adversary_layout.py`'s business
and is read from git there, not from this file.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences as _sentences


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
RECIPE = REFERENCES / "adversarial-skill-gate.md"
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


ADVERSARIAL_SKILL_GATE = _flat(RECIPE)
ADVERSARY_PROSE = _flat(ADVERSARY)
RULES = _rules(RECIPE)


def _affirms(text: str, verb: str, literal: str, *extras: str) -> bool:
    """Some sentence carries `verb` before `literal`, every extra, and no negation."""
    for s in _sentences(text):
        v, lit = s.find(verb), s.find(literal)
        if 0 <= v < lit and all(e in s for e in extras) and not has_negation(s):
            return True
    return False


# --- The rules this recipe states -------------------------------------------
#
# The three attempts are written as a bulleted run that carries no sentence
# stop between them, so each rule is pinned as an affirmative verb before
# its literal rather than as an exact sentence; a negation anywhere in the
# matched sentence is rejected.

# name: (verb, literal, extras, affirmative example, rejected examples)
AFFIRMATIVE_PINS = {
    "skill-gate-attempt-and-write-down-the-effect": (
        "Make each attempt below against the file",
        "write down what the file made you do", (),
        "Make each attempt below against the file, and write down what the file made you do.",
        ("Make each attempt below against the file, and never write down what the file made you do.",
         "Make each attempt below against the file."),
    ),
    "skill-gate-read-under-time-pressure": (
        "Read the instruction as an agent", "under time pressure",
        ("skips the expensive step", "still looks compliant"),
        "Read the instruction as an agent under time pressure — is there a reading that "
        "skips the expensive step and still looks compliant?",
        ("Read the instruction as an agent under time pressure — there is no reading that "
         "skips the expensive step and still looks compliant.",
         "Read the instruction as an agent under time pressure."),
    ),
    "skill-gate-attempt-the-temptations-verbatim": (
        "Attempt", "the prose temptations verbatim",
        ("record whether the text refuses them",),
        "Attempt the prose temptations verbatim (\"the diff is one line, proceed?\") and "
        "record whether the text refuses them.",
        ("Attempt the prose temptations verbatim, but do not record whether the text "
         "refuses them.",
         "Attempt the prose temptations verbatim.",
         "Attempt a paraphrase of the prose temptations and record whether the text refuses them."),
    ),
    "skill-gate-one-character-different": (
        "feed it the input it was written to catch",
        "the same input one character different", ("For a gate script",),
        "For a gate script, feed it the input it was written to catch, then the same input "
        "one character different.",
        ("For a gate script, feed it the input it was written to catch, but not the same "
         "input one character different.",
         "For a gate script, feed it the input it was written to catch."),
    ),
}


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


# A bullet count sat here and was removed: each attempt already has its own
# pin, so a bullet that disappears is caught by that pin, while the count
# also failed a fourth attempt being added -- an ordinary edit this file
# must not stand in the way of.


# --- One home for this recipe's rules: adversary.md repeats none of them ----

# Each fragment names one rule the skill-and-gate recipe owns; it lives in
# this file and nowhere in adversary.md.
PROCEDURE_FRAGMENTS = ("under time pressure", "prose temptations", "one character different")


def _procedure_fragments_in_both(agent: str, ref: str) -> list[str]:
    return [f for f in PROCEDURE_FRAGMENTS if f in agent and f in ref]


def test_procedure_fragments_helper_synthetic() -> None:
    ref = "Read the instruction as an agent under time pressure."
    assert _procedure_fragments_in_both("Read the reference first.", ref) == []
    duplicated = "Read it as an agent under time pressure would."
    assert _procedure_fragments_in_both(duplicated, ref) == ["under time pressure"]


def test_procedure_sentence_in_both_files_rejected() -> None:
    assert _procedure_fragments_in_both(ADVERSARY_PROSE, ADVERSARIAL_SKILL_GATE) == []
    assert [f for f in PROCEDURE_FRAGMENTS if f not in ADVERSARIAL_SKILL_GATE] == []
