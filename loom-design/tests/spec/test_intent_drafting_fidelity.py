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
    ("Write", "user's conversation language"),
    ("Connect", "sourced project or function purpose", "established direction", "this request"),
    ("Keep", "missing required facts", "existing interview"),
    ("Repair", "assistant shorthand", "already supplied role"),
    ("Preserve", "interface boundary", "private helpers"),
    ("Borrow", "information connections", "case-specific facts"),
    ("Require", "actual-request support or evidence", "date, role, impact and constraint"),
    ("Check", "each sentence", "grounded context", "scope", "outcome", "required decision or consent"),
    ("Retain", "required disclosures", "WARN", "cost/egress", "one-way-door", "carried details"),
    ("Ground", "every factual clause", "this request/current evidence"),
    ("Preserve", "abstraction", "present-versus-desired quantifiers"),
    ("Treat", "rule role separately from", "unverified representation", "list, file, cache, algorithm or UI"),
    ("Keep", "present affected population distinct from desired coverage"),
    ("Include", "only supplied boundaries"),
)
LOAD_RULE = ("Read", "confirmation-template.md", "before drafting or replying")
FINAL_CHECK = ("Apply", "confirmation-template.md", "final-message check", "before sending")
AUTH_RULE = ("Explain", "only after review AND publication checks pass",
             "BOTH uploading the change branch", "AND opening a pull request ready for review",
             "anytime before publication", "separate merge decision", "publication is enabled")
HOLD_RULE = ("Honor", "prior publication hold or opt-out", "user explicitly lifts it")
PUBLIC_RULE = ("Keep", "whole public reply", "five sections", "private prefaces", "postscripts")
CONTEXT_RULE = ("Read", "available README or equivalent project overview", "current direction", "before composing")
DIAGRAM_RULE = ("Invoke", "loom-workflow:loom-visualization", "before composing a diagram", "when available")
FORMAT_LOAD = ("Read", "confirmation-format.md", "only when required facts are settled")
TARGET_RULE = ("Preserve", "source targets and qualifiers", "absence, preservation and exclusion claims", "unmentioned alternatives unknown")
BOUNDARY_RULE = ("Trace", "each boundary privately", "actual user or current-document clause")
CONSTRAINT_RULE = ("Keep", "already-fixed user/standing-policy boundaries")
EXCLUSION_RULE = ("Keep", "explicitly excluded", "source abstraction")
FORMAT_RULES = (
    ("Use", "five sections in this order"),
    ("Disclose", "same yes", "automatic publication", "opt-out", "separate merge", "publication is enabled"),
    PUBLIC_RULE, DIAGRAM_RULE, AUTH_RULE,
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
    assert affirms(before_draft, *LOAD_RULE), path
    link = re.search(r"Read `([^`]*confirmation-template\.md)` before drafting or replying", before_draft)
    assert link, path
    owner = REPO / path
    target = owner.parent / link.group(1)
    local_dir = owner.parent / "references" if owner.name == "SKILL.md" else owner.parent
    assert target.is_file() and target.resolve().parent == local_dir.resolve(), target


@pytest.mark.parametrize("filename", ["confirmation-template.md", "confirmation-examples.md", "confirmation-format.md"])
def test_local_confirmation_examples_are_portable_and_identical(filename: str) -> None:
    paths = [REPO / root / filename for root in (
        "loom-design/skills/capture-intent/references",
        "loom-code/skills/write-plan/references",
    )]
    text = paths[0].read_text(encoding="utf-8")
    assert text == paths[1].read_text(encoding="utf-8")
    assert "loom-design/" not in text and "loom-code/" not in text
    if filename == "confirmation-template.md":
        for rule in (*EXAMPLE_RULES, HOLD_RULE, CONTEXT_RULE, TARGET_RULE, BOUNDARY_RULE):
            assert affirms(" ".join(text.split()), *rule), rule
        assert "```markdown" not in text and "## Please confirm" not in text
        return
    if filename == "confirmation-format.md":
        for rule in FORMAT_RULES:
            assert affirms(" ".join(text.split()), *rule), rule
        skeleton = text.split("```markdown\n", 1)[1].split("```", 1)[0]
        assert re.findall(r"^## (.+)$", skeleton, re.M) == [
            "Background and current direction", "Current problem and impact",
            "What changes", "Scope and acceptance", "Please confirm"]
        return
    for case in ("Known correction", "Multiple problems", "Repairing shorthand", "Interface boundary"):
        example = text.split(f"## {case}", 1)[1].split("\n## ", 1)[0]
        assert "Good:" in example and "Bad:" in example
    grounding = paths[0].with_name("confirmation-template.md").read_text()
    pending = grounding.split("## Unknown date", 1)[1].split("\n## ", 1)[0]
    good_interview = pending.split("Good:", 1)[1].split("Bad:", 1)[0]
    assert "pull request" not in good_interview and "Saying yes" not in good_interview
    assert "blocked" in good_interview
    assert "old" not in pending.lower() and "customer" not in pending.lower()
    pair = text.split("## Known correction", 1)[1].split("\n## ", 1)[0]
    good, bad = pair.split("Good:", 1)[1].split("Bad:", 1)
    good = " ".join(line[2:] for line in good.splitlines() if line.startswith("> "))
    bad = " ".join(line[2:] for line in bad.splitlines() if line.startswith("> "))
    assert bad.startswith(good) and bad != good
    for case in ("Known correction", "Multiple problems", "Repairing shorthand", "Interface boundary"):
        section = text.split(f"## {case}", 1)[1].split("\n## ", 1)[0]
        positive = " ".join(section.split("Good:", 1)[1].split("Bad:", 1)[0].replace("> ", "").split())
        assert "Only after review and publication checks pass" in positive
        assert "both a non-forced branch upload and a pull request ready for review" in positive
        assert "anytime before publication" in positive
        headings = re.findall(r"^> ### (.+)$", section.split("Good:", 1)[1].split("Bad:", 1)[0], re.M)
        assert headings == ["Background and current direction", "Current problem and impact",
                            "What changes", "Scope and acceptance", "Please confirm"]
    ready = paths[0].with_name("confirmation-format.md").read_text()
    for case in ("Invoice currency correction", "Filtered CSV export"):
        section = ready.split(f"## {case}", 1)[1].split("\n## ", 1)[0]
        assert "Good:" in section and "Bad:" in section
        headings = re.findall(r"^> ### (.+)$", section.split("Good:", 1)[1].split("Bad:", 1)[0], re.M)
        assert headings == ["Background and current direction", "Current problem and impact",
                            "What changes", "Scope and acceptance", "Please confirm"]
        positive = section.split("Good:", 1)[1].split("Bad:", 1)[0]
        if case == "Invoice currency correction":
            assert "requirements only" in positive and "explicitly lift" in positive
            assert "Only after review and publication checks pass" not in positive
        else:
            assert "current filtered result" in positive and "visible" not in positive


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
    assert "Everything below goes" not in message
    assert "uploading the change branch" in message and "separate merge decision" in message
    assert "**Write down every question" not in message and "`decision_point" not in message
    assert "**The complexity check" not in message and "`second-vendor:" not in message
    assert affirms(" ".join(message.split()), *FINAL_CHECK)
    assert affirms(" ".join(message.split()), *AUTH_RULE)
    assert affirms(" ".join(message.split()), *HOLD_RULE)
    assert affirms(" ".join(message.split()), *FORMAT_LOAD)
    ready_link = re.search(r"Read `([^`]*confirmation-format\.md)` only when required facts are settled", message)
    assert ready_link and ((REPO / path).parent / ready_link.group(1)).is_file()
    assert "confirmation-format.md" not in text[:composer]
    final_link = re.search(r"Apply .*?`([^`]*confirmation-template\.md)`", message)
    assert final_link and ((REPO / path).parent / final_link.group(1)).is_file()


@pytest.mark.parametrize("path", [
    "loom-design/skills/capture-intent/SKILL.md",
    "loom-code/skills/write-plan/references/confirm-intent.md",
    "loom-design/skills/capture-intent/templates/intent.md",
    "loom-code/contract/templates/intent.md",
])
def test_intent_boundaries_retain_source_scope(path: str) -> None:
    text = " ".join((REPO / path).read_text().split())
    assert affirms(text, *CONSTRAINT_RULE)
    assert affirms(text, *EXCLUSION_RULE)


def test_main_code_entry_loads_examples_before_both_intake_routes() -> None:
    owner = REPO / "loom-code/skills/write-plan/SKILL.md"
    text = owner.read_text(encoding="utf-8")
    step1 = text.split("## Step 1 — Find the intent", 1)[1].split("\n## ", 1)[0]
    no_intent = step1.split("- `loom-design` is not installed", 1)[1]
    step3 = text.split("## Step 3 — Decision point ①: restate and confirm", 1)[1].split("\n## ", 1)[0]
    confirmed, open_intent = step3.split("Otherwise", 1)
    assert "confirmation-template.md" not in confirmed and "confirmation-examples.md" not in confirmed
    assert "confirmation-format.md" not in confirmed
    assert "confirmation-format.md" not in open_intent
    assert "confirmation-format.md" not in no_intent
    for route, child in ((no_intent, "references/no-intent-interview.md"),
                         (open_intent, "references/confirm-intent.md")):
        load = route.index("references/confirmation-template.md")
        assert load < route.index(child)
        assert affirms(" ".join(route.split()), *LOAD_RULE)
    reader = owner.parent / "references/no-intent-interview.md"
    before_draft = reader.read_text(encoding="utf-8").split("When you write the intent", 1)[0]
    assert affirms(" ".join(before_draft.split()), *LOAD_RULE)
    for entry in (text, (REPO / "loom-design/skills/capture-intent/SKILL.md").read_text()):
        assert re.search(r"Optional illustrations: read relevant sections of `references/confirmation-examples.md` only when needed", " ".join(entry.split()))
        assert not re.search(r"Read `[^`]*confirmation-examples\.md` before drafting or replying", entry)
    for child in (reader, owner.parent / "references/confirm-intent.md"):
        assert not re.search(r"Read `[^`]*confirmation-examples\.md`.*before drafting or replying", child.read_text())


@pytest.mark.parametrize("rule", (*RULES, LOAD_RULE, FINAL_CHECK, HOLD_RULE, CONTEXT_RULE,
                                 FORMAT_LOAD, TARGET_RULE, BOUNDARY_RULE, CONSTRAINT_RULE,
                                 EXCLUSION_RULE, *FORMAT_RULES, *EXAMPLE_RULES))
def test_drafting_rule_polarity_and_late_placement(rule: tuple[str, ...]) -> None:
    verb, literal, *extras = rule
    sentence = f"{verb} {literal}, {', '.join(extras)}."
    assert affirms(sentence, verb, literal, *extras)
    assert not affirms("Do not " + sentence, verb, literal, *extras)
    if rule == AUTH_RULE:
        assert not affirms(sentence.replace("publication is enabled", "publication is disabled"), *rule)
    if "separate from" in literal:
        assert not affirms(sentence.replace("separate from", "equivalent to"),
                           verb, literal, *extras)
    late = "Draft directly when already sufficient. " + sentence
    assert not affirms(late.split("Draft directly", 1)[0], verb, literal, *extras)


def test_required_readers_contain_their_phase_examples() -> None:
    """Examples needed to recognize a phase cannot depend on optional reading."""
    root = REPO / "loom-design/skills/capture-intent/references"
    grounding = (root / "confirmation-template.md").read_text()
    ready = (root / "confirmation-format.md").read_text()
    gallery = (root / "confirmation-examples.md").read_text()
    pending = grounding.split("## Unknown date", 1)[1].split("\n## ", 1)[0]
    positive = pending.split("Good:", 1)[1].split("Bad:", 1)[0]
    assert "blocked" in positive and "### Please confirm" not in positive
    assert "verification" in pending and "out of scope" in pending
    assert "## Unknown date" not in ready + gallery
    for case in ("Invoice currency correction", "Filtered CSV export"):
        assert f"## {case}" in ready and f"## {case}" not in gallery
    assert "templates/02-linear-steps.md" in ready
    assert "read" in ready.split("templates/02-linear-steps.md", 1)[0].splitlines()[-1].lower()
    assert "no diagrams" not in ready.lower()


def test_missing_fact_branch_stops_before_confirmation_preparation() -> None:
    for relative in ("loom-design/skills/capture-intent/SKILL.md",
                     "loom-code/skills/write-plan/references/confirm-intent.md"):
        text = (REPO / relative).read_text()
        branch = text.split("before drafting or replying.", 1)[1].split("Before drafting:", 1)[0]
        assert "missing" in branch.lower() and "stop" in branch
        assert "confirmation preparation" in branch
    main = (REPO / "loom-code/skills/write-plan/SKILL.md").read_text()
    assert "confirmation-format.md" not in main


def test_primary_reader_uses_literal_explanation_without_private_terms() -> None:
    text = (REPO / "loom-design/skills/capture-intent/references/confirmation-template.md").read_text()
    assert affirms(" ".join(text.split()), "State", "who does what", "user sees", "what changes")
    assert "metaphors or analogies" in text
    assert "new terminology" in text and "necessary" in text
