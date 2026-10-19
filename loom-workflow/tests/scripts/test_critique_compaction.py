"""Structure checks for the merged critique skill.

`proposal-critique` and `complexity-critique` became one skill with two
modes at loom 1.0. What is checked here is the mode tokens, the heading
order and that the two retired skill names are gone; the modes' procedure
wording is review-only, and routing to `critique` is proven by
tests/test_loom_skill_description_catalog.py.
"""
from pathlib import Path


SKILL = Path(__file__).resolve().parents[2] / "skills" / "critique" / "SKILL.md"


def test_mode_routing_is_declared_before_either_lens():
    text = SKILL.read_text(encoding="utf-8")

    assert "mode: proposal" in text
    assert "mode: complexity" in text
    headings = ["## Choosing the mode", "## Shared discipline", "## Mode: proposal", "## Mode: complexity"]
    positions = [text.index(heading) for heading in headings]
    assert positions == sorted(positions)


def test_routing_boundaries_survive_the_merge():
    text = SKILL.read_text(encoding="utf-8")

    # The merge deleted the two skills that used to route to each other.
    for gone in ("proposal-critique", "complexity-critique", "brief-before-asking"):
        assert gone not in text, f"critique still names the deleted {gone}"
