"""Prose regression pins; cold-read cases separately test agent decisions."""

import re
from pathlib import Path

import pytest


PLUGIN = Path(__file__).resolve().parents[1]
PLAN = PLUGIN / "skills/write-plan/SKILL.md"
IMPLEMENTER = PLUGIN / "agents/implementer.md"
LENSES = PLUGIN / "skills/review/references/lenses.md"


def affirmative(text: str, anchor: str) -> str:
    """Require an affirmative instruction before the pinned contract phrase."""
    sentences = re.split(r"[.!?]", " ".join(text.split()))
    for sentence in sentences:
        if anchor not in sentence:
            continue
        prefix = sentence.split(anchor, 1)[0]
        assert re.search(r"\b(choose|keep|treat|record|verify|reject)\b", prefix, re.I)
        assert not re.search(r"\b(not|never|neither|without|cannot)\b|n't\b", sentence, re.I)
        return sentence
    raise AssertionError(f"Missing affirmative contract: {anchor}")


def test_affirmative_pin_accepts_instruction():
    affirmative("Choose a boundary around a separable responsibility.", "a separable responsibility")


@pytest.mark.parametrize("text", [
    "Never choose a boundary around a separable responsibility.",
    "Do not choose a boundary around a separable responsibility.",
    "A separable responsibility is something to choose later.",
])
def test_affirmative_pin_rejects_negation_or_late_verb(text):
    with pytest.raises(AssertionError):
        affirmative(text, "a separable responsibility")


def test_plan_extracts_for_responsibility_and_reduced_context():
    text = PLAN.read_text()
    sentence = affirmative(text, "a separable responsibility")
    assert "dependencies" in sentence and "context" in sentence
    assert "requested change" in sentence


def test_plan_keeps_cohesive_long_file_and_rejects_length_only_trigger():
    text = PLAN.read_text()
    affirmative(text, "cohesive code together")
    sentence = affirmative(text, "file length as a warning")
    assert "only" in sentence


def test_existing_stations_own_boundary_decision():
    text = PLAN.read_text()
    sentence = affirmative(text, "the boundary reason")
    assert "existing task Risk line" in sentence
    assert "agent-decided" in sentence
    assert "how the work is split is your decision" in " ".join(text.split())


def test_implementation_verifies_independence_and_rejects_shallow_split():
    text = IMPLEMENTER.read_text()
    sentence = affirmative(text, "the planned boundary")
    assert "focused test" in sentence and "callers" in sentence
    sentence = affirmative(text, "a file split")
    for coupling in ("dependencies", "shared state", "change scope"):
        assert coupling in sentence


def test_review_accepts_independent_boundary_and_requires_coupling_evidence():
    text = LENSES.read_text()
    sentence = affirmative(text, "boundaries that support")
    for benefit in ("independent understanding", "focused testing", "local changes"):
        assert benefit in sentence
    sentence = affirmative(text, "a shallow file split")
    for evidence in ("anchored evidence", "responsibilities", "shared state", "tests", "change scope"):
        assert evidence in sentence


def test_review_rejects_length_or_style_only_boundary_findings():
    text = LENSES.read_text()
    sentence = affirmative(text, "file length and style preference")
    assert "insufficient" in sentence and "boundary finding" in sentence
    assert "100 is a finding on its own" not in text
