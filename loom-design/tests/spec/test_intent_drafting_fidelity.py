"""W1-01 continued: fidelity applies before any outcome is drafted."""

from pathlib import Path
import sys

import pytest

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "loom-code/scripts"))
from prose_pin import affirms  # noqa: E402

RULES = (
    ("Preserve", "supplied facts", "outcome strength", "qualifiers"),
    ("Leave", "unknown facts unresolved", "user answers", "evidence"),
    ("Keep", "own-rule isolation separate from", "same-worker", "same-result guarantees"),
)


@pytest.mark.parametrize(("path", "draft_boundary"), [
    ("loom-design/skills/capture-intent/SKILL.md", "Draft directly when already sufficient."),
    ("loom-code/skills/write-plan/references/confirm-intent.md", "Problem holds present pain"),
])
def test_fidelity_precedes_first_drafting_instruction(path: str, draft_boundary: str) -> None:
    text = " ".join((REPO / path).read_text(encoding="utf-8").split())
    before_draft = text[:text.index(draft_boundary)]
    for verb, literal, *extras in RULES:
        assert affirms(before_draft, verb, literal, *extras), (path, literal)


@pytest.mark.parametrize("rule", RULES)
def test_drafting_rule_polarity_and_late_placement(rule: tuple[str, ...]) -> None:
    verb, literal, *extras = rule
    sentence = f"{verb} {literal}, {', '.join(extras)}."
    assert affirms(sentence, verb, literal, *extras)
    assert not affirms("Do not " + sentence, verb, literal, *extras)
    if "separate from" in literal:
        assert not affirms(sentence.replace("separate from", "equivalent to"),
                           verb, literal, *extras)
    late = "Draft directly when already sufficient. " + sentence
    assert not affirms(late.split("Draft directly", 1)[0], verb, literal, *extras)
