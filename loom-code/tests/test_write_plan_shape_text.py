"""The live plan contract has one ordinary task-id form."""

import re
from pathlib import Path

import pytest

from prose_pin import has_negation


ROOT = Path(__file__).resolve().parents[2]
WRITE_PLAN = ROOT / "loom-code/skills/write-plan/SKILL.md"
SPEC_MINIMAL = ROOT / "loom-code/contract/templates/spec-minimal.md"
CONFIRM_INTENT = ROOT / "loom-code/skills/write-plan/references/confirm-intent.md"
NO_INTENT_INTERVIEW = ROOT / "loom-code/skills/write-plan/references/no-intent-interview.md"
SELF_WRITTEN_SPEC = ROOT / "loom-code/skills/write-plan/references/self-written-spec.md"

_STEP1 = "## Step 1 — Find the intent"
_STEP3 = "## Step 3 — Decision point ①: restate and confirm"
_STEP4 = "## Step 4 — Does this need a spec?"
_STEP5 = "## Step 5 — Write the plan"
_PRODUCT_GATE = "<!-- gate: write-plan.product-spec-needs-confirmed-behavior -->"


def _text() -> str:
    return WRITE_PLAN.read_text(encoding="utf-8")


def _product_gate() -> str:
    """The product-spec gate, held by the self-written spec reference."""
    text = SELF_WRITTEN_SPEC.read_text(encoding="utf-8")
    return text.split(_PRODUCT_GATE, 1)[1].split("### ", 1)[0]


def _section(heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", _text(), re.M | re.S)
    assert m, f"section {heading!r} missing"
    return m.group(0)


def test_task_ids_use_one_numeric_form_without_reserved_process_tasks() -> None:
    assert "W<n>-memory" not in _section(_STEP5)


def _body_words(text: str) -> int:
    """Words after the YAML frontmatter, counted with `str.split`."""
    m = re.match(r"---\n.*?\n---\n", text, re.S)
    assert m, "frontmatter missing"
    return len(text[m.end():].split())


def test_writePlanBody_under3750Words() -> None:
    """A3 positive (write-plan-body-under-3750-words)."""
    assert _body_words(WRITE_PLAN.read_text(encoding="utf-8")) < 3750


def test_confirmedIntent_skipsReferenceLoad() -> None:
    """A3 boundary (confirmed-intent-skips-reference-load): Step 3 exists and
    the reference it loads is on disk."""
    _section(_STEP3)
    assert CONFIRM_INTENT.is_file()


def _flat(text: str) -> str:
    return re.sub(r"\s+", " ", text)


_MOVED_INTAKE_RULES = {
    "no-intent-interview.md": (
        "run step 3's restate-and-confirm as a short interview instead",
        "The user never hand-writes the file.",
        "with nothing open write exactly `- none` under the heading",
    ),
    "confirm-intent.md": (
        "<!-- gate: write-plan.no-plan-without-confirmed-intent -->",
        "When this station performs code-only intake, use the same capture boundary:",
        "**Keep, neutralize, defer, reopen, or delete**",
        "the intent must remain `open`. <!-- /gate -->",
        "Any intent section may use a Markdown table or a Mermaid `flowchart`;",
    ),
}


def test_intakeReferences_holdMovedRules_bodyDoesNot() -> None:
    """A2 positive (references-hold-moved-rules-verbatim); negative
    (body-no-longer-holds-moved-rules) -- the gate's first paragraph stays."""
    body = _flat(_text())
    for name, rules in _MOVED_INTAKE_RULES.items():
        ref = _flat((CONFIRM_INTENT.parent / name).read_text(encoding="utf-8"))
        for rule in rules:
            assert rule in ref, (name, rule)
            if "<!--" not in rule:
                assert rule not in body, rule
    assert "**No plan is written without a confirmed intent.**" in body
    assert "When this station performs code-only intake" not in body


def test_interviewPointer_onlyOnLoomDesignAbsentBullet() -> None:
    """A3 positive (pointer-only-on-loom-design-absent-bullet); negative
    (installed-bullet-and-confirm-intent-never-name-interview-file)."""
    step1 = _section(_STEP1)
    absent = step1.split("- `loom-design` is not installed", 1)[1].split("\n<!--", 1)[0]
    installed = step1.split("- `loom-design` is installed", 1)[1].split("\n- ", 1)[0]
    assert "references/no-intent-interview.md" in absent
    assert "no-intent-interview" not in installed
    assert _text().count("no-intent-interview") == 1
    assert "no-intent-interview" not in CONFIRM_INTENT.read_text(encoding="utf-8")
    assert "`confirm-intent.md`" in NO_INTENT_INTERVIEW.read_text(encoding="utf-8")


def test_specPointer_onNoAndAbsentBranches_notInstalledYes() -> None:
    """A3 positive (spec-pointer-on-no-and-absent-branches); negative
    (installed-yes-branch-has-no-pointer)."""
    step4 = _section(_STEP4)
    no = step4.split("**`no`**", 1)[1].split("**`yes`", 1)[0]
    installed = step4.split("**`yes`, spec missing, `loom-design` installed**", 1)[1]
    installed = installed.split("**`yes`", 1)[0]
    absent = step4.split("**`yes`, spec missing, `loom-design` not installed**", 1)[1]
    absent = absent.split("### ", 1)[0]
    exists = step4.split("**`yes`, and `docs/loom/<change-id>/spec.md` already exists**", 1)[1]
    exists = exists.split("**`yes`", 1)[0]
    for branch in (no, exists, absent):
        assert "`references/self-written-spec.md`" in branch
    assert "self-written-spec" not in installed
    assert _text().count("self-written-spec") == 3


def test_noBranchSpecPointer_firesOnAlreadyWrittenSpec() -> None:
    """A resumed `no` run whose spec is already on disk reaches the reference."""
    no = _section(_STEP4).split("**`no`**", 1)[1].split("**`yes`", 1)[0]
    pointer = next(s for s in _flat(no).split(". ") if "self-written-spec" in s)
    assert "already wrote `docs/loom/<change-id>/spec.md`" in pointer
    assert "read `references/self-written-spec.md`" in pointer
    assert not has_negation(pointer), pointer


def test_selfWrittenSpec_hasNoBranchHeadings() -> None:
    """The shared review dispatch and product gate sit under no yes-only heading."""
    text = SELF_WRITTEN_SPEC.read_text(encoding="utf-8")
    assert re.findall(r"^#{2,} ", text, re.M) == []


def test_write_plan_readback_has_no_mermaid() -> None:
    """A3 negative: no Mermaid in the chat read-back; gate text untouched."""
    assert "```mermaid" not in _text()
    assert "```mermaid" not in SELF_WRITTEN_SPEC.read_text(encoding="utf-8")
    gate = _product_gate()
    assert "per-case sentences" not in gate
    assert "Mermaid" not in gate


_DOORS = re.compile(r"\bproduct one-way doors\b", re.IGNORECASE)
_PRESENT = re.compile(r"\bpresent\b", re.IGNORECASE)
_NOTHING = re.compile(r"\bnothing\b", re.IGNORECASE)


def _negated(sentence: str) -> bool:
    """The shared prose-pin negation words, plus `nothing`."""
    return has_negation(sentence) or bool(_NOTHING.search(sentence))


def _presents_doors(text: str) -> bool:
    """A sentence affirmatively presents the product one-way doors.

    Sentences split after `.` or `;`, as in the graduated adversary probes.
    """
    for sentence in re.split(r"(?<=[.;])\s+", re.sub(r"\s+", " ", text)):
        doors = _DOORS.search(sentence)
        if doors and not _negated(sentence) \
                and _PRESENT.search(sentence[: doors.start()]):
            return True
    return False


def test_doors_detector_affirmative_accepted_negated_rejected() -> None:
    """Self-test: the detector accepts the affirmative form, rejects the negated one."""
    assert _presents_doors("Present the Requirements and product one-way doors in plain words.")
    assert not _presents_doors("Never present the Requirements or product one-way doors here.")


@pytest.mark.parametrize("sentence", [
    "Present no Requirements and no product one-way doors here.",
    "You cannot present the product one-way doors here.",
    "Present the Requirements without the product one-way doors.",
    "Neither agent may present the product one-way doors.",
    "Nobody may present the product one-way doors here.",
    "Present nothing about the product one-way doors.",
])
def test_doors_detector_rejects_shared_negation_words(sentence: str) -> None:
    """Self-test: every shared negation word, and `nothing`, defeats the pin."""
    assert not _presents_doors(sentence)


def test_product_gate_presents_product_one_way_doors() -> None:
    """Decision point ② discloses the product door consequences."""
    assert _presents_doors(_product_gate())


ONE_WAY_DOOR = ROOT / "loom-code/skills/write-plan/references/one-way-door.md"


_NO_REASK = re.compile(r"\b(?:not asked|does not ask (?:them|it|the same question))\s+again at ②")


def _says_no_reask(text: str) -> bool:
    """A question already asked at ① is not asked again at ②.

    The negation is tied to the verb right before "again at ②"; a negation
    elsewhere in the sentence ("asked again at ②, never skipped") flips it.
    """
    flat = re.sub(r"\s+", " ", text)
    for sentence in re.split(r"(?<=[.;])\s+", flat):
        if "①" in flat and _NO_REASK.search(sentence):
            return True
    return False


@pytest.mark.parametrize("sentence, expected", [
    ("Doors asked at ① are not asked again at ②.", True),
    ("Questions asked at ① are settled. A spec written later does not ask the same question again at ②.", True),
    ("Doors at ① are asked again at ②, never skipped.", False),
    ("a spec written later asks them again at ②, not trusting ①.", False),
    ("Questions asked at ① are settled. A spec written later asks the same question again at ②, not skipped.", False),
])
def test_no_reask_detector_ties_negation_to_verb(sentence: str, expected: bool) -> None:
    """Self-test: only a negated verb before "again at ②" counts as no-reask."""
    assert _says_no_reask(sentence) is expected


def test_product_gate_and_merge_gate_skip_doors_asked_at_one() -> None:
    """Acceptance 4: an answered outcome or authorization question is not repeated."""
    assert _says_no_reask(_product_gate())
    merge = ONE_WAY_DOOR.read_text(encoding="utf-8").split("**Merge.**", 1)[1]
    assert _says_no_reask(merge.split("\n## ", 1)[0])
    asked = _text().split("## What you will be asked", 1)[1]
    item2 = re.sub(r"\s+", " ", asked.split("\n2. ", 1)[1].split("\n3. ", 1)[0])
    assert "unresolved product outcome or authorization questions not asked at ①" in item2


def test_template_placeholder_names_table_and_diagram() -> None:
    """A4 boundary: the spec-minimal UI flows section is one placeholder line."""
    text = SPEC_MINIMAL.read_text(encoding="utf-8")
    body = text.split("## UI flows", 1)[1].split("\n", 1)[1].strip()
    assert body.startswith("<") and body.endswith(">") and "\n" not in body
