"""W1-01 continued: fidelity applies before any outcome is drafted."""

from pathlib import Path
import re
import sys

import pytest

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "loom-code/scripts"))
from prose_pin import affirms  # noqa: E402

RULES = (
    ("Preserve", "supplied facts", "outcome strength", "qualifiers"),
    ("Leave", "unknown facts unresolved", "user answers", "evidence"),
    ("Keep", "own-rule isolation separate from", "same-worker", "same-result guarantees"),
    ("Keep", "missing required facts", "existing interview", "needed fact and why"),
)
EXAMPLE_RULES = (
    ("Use", "outline as content connections", "optional", "grouping", "length"),
    ("Repair", "assistant shorthand", "already supplied role"),
    ("Preserve", "interface boundary", "private helpers"),
    ("Disclose", "same yes", "automatic publication", "opt-out", "separate merge"),
)
LOAD_RULE = ("Read", "confirmation-examples.md", "before drafting or replying")


@pytest.mark.parametrize(("path", "draft_boundary"), [
    ("loom-design/skills/capture-intent/SKILL.md", "Draft directly when already sufficient."),
    ("loom-code/skills/write-plan/references/confirm-intent.md", "Problem holds present pain"),
])
def test_fidelity_precedes_first_drafting_instruction(path: str, draft_boundary: str) -> None:
    text = " ".join((REPO / path).read_text(encoding="utf-8").split())
    before_draft = text[:text.index(draft_boundary)]
    for verb, literal, *extras in RULES:
        assert affirms(before_draft, verb, literal, *extras), (path, literal)
    assert affirms(before_draft, *LOAD_RULE), path
    link = re.search(r"Read `([^`]*confirmation-examples\.md)` before drafting or replying", before_draft)
    assert link, path
    owner = REPO / path
    target = owner.parent / link.group(1)
    local_dir = owner.parent / "references" if owner.name == "SKILL.md" else owner.parent
    assert target.is_file() and target.resolve().parent == local_dir.resolve(), target


def test_local_confirmation_examples_are_portable_and_identical() -> None:
    paths = [REPO / root / "confirmation-examples.md" for root in (
        "loom-design/skills/capture-intent/references",
        "loom-code/skills/write-plan/references",
    )]
    text = paths[0].read_text(encoding="utf-8")
    assert text == paths[1].read_text(encoding="utf-8")
    assert "loom-design/" not in text and "loom-code/" not in text
    for rule in EXAMPLE_RULES:
        assert affirms(" ".join(text.split()), *rule), rule
    for case in ("Unknown date", "Known correction", "Multiple problems", "Repairing shorthand", "Interface boundary"):
        example = text.split(f"## {case}", 1)[1].split("\n## ", 1)[0]
        assert "Good:" in example and "Bad:" in example
    pending = text.split("## Unknown date", 1)[1].split("\n## ", 1)[0]
    good_interview = pending.split("Good:", 1)[1].split("Bad:", 1)[0]
    assert "pull request" not in good_interview and "Saying yes" not in good_interview


@pytest.mark.parametrize("path", [
    "loom-design/skills/capture-intent/SKILL.md",
    "loom-code/skills/write-plan/references/confirm-intent.md",
])
def test_user_composer_is_separate_from_private_work(path: str) -> None:
    text = (REPO / path).read_text(encoding="utf-8")
    preparation = text.index("### Private preparation")
    composer = text.index("### User message")
    records = text.index("### Private records and reply handling")
    assert preparation < composer < records
    message = text[composer:records]
    assert "Compose **one message**" in message and "Restate Problem and Acceptance" in message
    assert "uploading the change branch" in message and "separate merge decision" in message
    assert "**Write down every question" not in message and "`decision_point" not in message
    assert "**The complexity check" not in message and "`second-vendor:" not in message


@pytest.mark.parametrize("rule", (*RULES, LOAD_RULE, *EXAMPLE_RULES))
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
