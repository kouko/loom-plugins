"""Adversary probe for 2026-10-06-skill-prose-contradictions.
concern: a product change that writes no spec loses every one-way-door question, because the ① message routes product one-way doors to a ② that never runs.

The change tells the ① message (write-plan confirm-intent.md item 2 and
capture-intent SKILL.md step-4 item 2) that a product change's one-way
doors, class (e) included, are asked at decision point ② "never in this
message". Decision point ② only runs where a spec is written, and
write-plan SKILL.md step 4 says a product intent with `needs-design: no`
and an empty carried-details list forces no spec. So an irreversible
action on the user's data in such a change is asked nowhere. The probe
requires each ① copy to say affirmatively where those doors are asked
when no spec is written.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
FIRST_MESSAGE_COPIES = [
    REPO / "loom-code/skills/write-plan/references/confirm-intent.md",
    REPO / "loom-design/skills/capture-intent/SKILL.md",
]
LITERAL = re.compile(r"\bno spec\b|\bwithout a spec\b", re.IGNORECASE)
AFFIRMATIVE_VERB = re.compile(r"\bask(?:ed|s)?\b", re.IGNORECASE)
NEGATION = re.compile(r"\b(?:never|not|nothing|nor)\b|n't\b", re.IGNORECASE)


def _sentences(text: str) -> list[str]:
    flat = re.sub(r"\s+", " ", text)
    return re.split(r"(?<=[.;])\s+", flat)


def _routing_paragraph(text: str) -> str:
    """The numbered item that routes a product change's one-way doors."""
    for block in re.split(r"\n\s*\n", text):
        if re.search(r"product change's one-way doors", block, re.IGNORECASE):
            return block
    return ""


def _affirms_no_spec_route(paragraph: str) -> bool:
    for sentence in _sentences(paragraph):
        literal = LITERAL.search(sentence)
        if not literal:
            continue
        if NEGATION.search(sentence):
            continue
        if AFFIRMATIVE_VERB.search(sentence[: literal.start()]):
            return True
    return False


def test_detector_affirmative_example_accepted() -> None:
    """The detector accepts an affirmative no-spec routing sentence."""
    sample = (
        "A product change's one-way doors are asked at decision point 2. "
        "They are asked here instead when no spec is written."
    )
    assert _affirms_no_spec_route(sample)


def test_detector_negated_example_rejected() -> None:
    """The detector rejects a negated no-spec sentence."""
    sample = (
        "A product change's one-way doors are asked at decision point 2. "
        "They are never asked here, even when no spec is written."
    )
    assert not _affirms_no_spec_route(sample)


def test_first_message_product_door_without_spec_has_a_stop() -> None:
    """Each decision-point-1 copy names where a product one-way door is asked when no spec is written."""
    missing = []
    for path in FIRST_MESSAGE_COPIES:
        paragraph = _routing_paragraph(path.read_text(encoding="utf-8"))
        assert paragraph, f"routing paragraph not found in {path}"
        if not _affirms_no_spec_route(paragraph):
            missing.append(str(path.relative_to(REPO)))
    assert not missing, (
        "product one-way doors are sent to decision point 2 with no route "
        f"for a product change that writes no spec: {missing}"
    )
