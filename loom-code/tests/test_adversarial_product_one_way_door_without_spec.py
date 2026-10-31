"""Guard the decision-point-① route for product changes without a spec.

Decision point ② only runs when a spec is written. Each ① copy must still
ask about an unresolved user outcome or missing authorization when no spec
will be written. In particular, action on the user's existing data needs
explicit consent; technical risk alone does not create a question.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from prose_pin import has_negation

REPO = Path(__file__).resolve().parents[2]
FIRST_MESSAGE_COPIES = [
    REPO / "loom-code/skills/write-plan/references/confirm-intent.md",
    REPO / "loom-design/skills/capture-intent/SKILL.md",
]
LITERAL = re.compile(r"\bno spec\b|\bwithout a spec\b", re.IGNORECASE)
AFFIRMATIVE_VERB = re.compile(r"\bask(?:ed|s)?\b", re.IGNORECASE)
NOTHING = re.compile(r"\bnothing\b", re.IGNORECASE)


def _negated(sentence: str) -> bool:
    """The shared prose-pin negation words, plus `nothing`."""
    return has_negation(sentence) or bool(NOTHING.search(sentence))


def _sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text)
    return re.split(r"(?<=[.;])\s+", flat)


def _routing_paragraph(text: str) -> str:
    """The numbered item that routes product questions at decision point ①."""
    match = re.search(
        r"^2\. \*\*The engineering one-way doors.*?(?=^3\. |\Z)",
        text, re.M | re.S,
    )
    return match.group(0) if match else ""


def _affirms_no_spec_route(paragraph: str) -> bool:
    if not (re.search(r"\boutcome\b", paragraph, re.I)
            and re.search(r"\bunresolved\b", paragraph, re.I)):
        return False
    if not re.search(r"authorization", paragraph, re.I):
        return False
    if not re.search(r"explicit consent", paragraph, re.I):
        return False
    saw_no_spec = False
    for sentence in _sentences(paragraph):
        literal = LITERAL.search(sentence)
        if literal:
            saw_no_spec = True
        # Mask the literal's own "no" before checking sentence polarity.
        checked = sentence[:literal.start()] + sentence[literal.end():] if literal else sentence
        if _negated(checked):
            continue
        if literal and AFFIRMATIVE_VERB.search(sentence[:literal.start()]):
            return True
        if saw_no_spec and re.search(r"\bask here\b", sentence, re.I):
            return True
    return False


def test_detector_affirmative_example_accepted() -> None:
    """The detector accepts an affirmative no-spec routing sentence."""
    sample = (
        "An unresolved outcome or missing authorization needs a question. "
        "Existing-data actions need explicit consent. "
        "They are asked here instead when no spec is written."
    )
    assert _affirms_no_spec_route(sample)
    assert _affirms_no_spec_route(
        "An unresolved outcome or missing authorization needs explicit consent. "
        "No spec will be written. Ask here for the user's choice."
    )


def test_detector_negated_example_rejected() -> None:
    """The detector rejects a negated no-spec sentence."""
    sample = (
        "An unresolved outcome or missing authorization needs explicit consent. "
        "They are never asked here, even when no spec is written."
    )
    assert not _affirms_no_spec_route(sample)


@pytest.mark.parametrize("sentence", [
    "No one has them asked here when no spec is written.",
    "They cannot be asked here when no spec is written.",
    "Without a review they are asked nowhere when no spec is written.",
    "Neither copy has them asked here when no spec is written.",
    "Nobody has them asked here when no spec is written.",
    "Nothing is asked here when no spec is written.",
])
def test_detector_rejects_shared_negation_words(sentence: str) -> None:
    """Every shared negation word, and `nothing`, defeats the pin."""
    prefix = "An unresolved outcome or missing authorization needs explicit consent. "
    assert not _affirms_no_spec_route(prefix + sentence)


def test_first_message_product_door_without_spec_has_a_stop() -> None:
    """Each ① copy asks for unresolved outcomes or consent without a spec."""
    missing = []
    for path in FIRST_MESSAGE_COPIES:
        paragraph = _routing_paragraph(path.read_text(encoding="utf-8"))
        assert paragraph, f"routing paragraph not found in {path}"
        if not _affirms_no_spec_route(paragraph):
            missing.append(str(path.relative_to(REPO)))
    assert not missing, (
        f"product questions have no decision-point-① route without a spec: {missing}"
    )
