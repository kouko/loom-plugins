"""The live plan contract has one ordinary task-id form."""

import re
from pathlib import Path

import pytest

from prose_pin import has_negation


ROOT = Path(__file__).resolve().parents[2]
WRITE_PLAN = ROOT / "loom-code/skills/write-plan/SKILL.md"
SPEC_MINIMAL = ROOT / "loom-code/contract/templates/spec-minimal.md"
CONFIRM_INTENT = ROOT / "loom-code/skills/write-plan/references/confirm-intent.md"

_STEP3 = "## Step 3 — Decision point ①: restate and confirm"
_STEP4 = "## Step 4 — Does this need a spec?"
_STEP5 = "## Step 5 — Write the plan"
_PRODUCT_GATE = "<!-- gate: write-plan.product-spec-needs-confirmed-behavior -->"


def _text() -> str:
    return WRITE_PLAN.read_text(encoding="utf-8")


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


def test_write_plan_readback_has_no_mermaid() -> None:
    """A3 negative: no Mermaid in the chat read-back; gate text untouched."""
    assert "```mermaid" not in _text()
    gate = _section(_STEP4).split(_PRODUCT_GATE, 1)[1].split("### ", 1)[0]
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
    """Decision point ② presents the product one-way doors routed to it from ①."""
    gate = _section(_STEP4).split(_PRODUCT_GATE, 1)[1].split("### ", 1)[0]
    assert _presents_doors(gate)


ONE_WAY_DOOR = ROOT / "loom-code/skills/write-plan/references/one-way-door.md"


def _says_no_reask(text: str) -> bool:
    """A sentence says a door already asked at ① is not asked again at ②."""
    for sentence in re.split(r"(?<=[.;])\s+", re.sub(r"\s+", " ", text)):
        if "①" in sentence and "again at ②" in sentence and has_negation(sentence):
            return True
    return False


def test_product_gate_and_merge_gate_skip_doors_asked_at_one() -> None:
    """Acceptance 2: a product door asked at ① is not asked again at ②."""
    gate = _section(_STEP4).split(_PRODUCT_GATE, 1)[1].split("### ", 1)[0]
    assert _says_no_reask(gate)
    merge = ONE_WAY_DOOR.read_text(encoding="utf-8").split("**Merge.**", 1)[1]
    assert _says_no_reask(merge.split("\n## ", 1)[0])
    asked = _text().split("## What you will be asked", 1)[1]
    item2 = re.sub(r"\s+", " ", asked.split("\n2. ", 1)[1].split("\n3. ", 1)[0])
    assert "product one-way doors ① skips" in item2


def test_template_placeholder_names_table_and_diagram() -> None:
    """A4 boundary: the spec-minimal UI flows section is one placeholder line."""
    text = SPEC_MINIMAL.read_text(encoding="utf-8")
    body = text.split("## UI flows", 1)[1].split("\n", 1)[1].strip()
    assert body.startswith("<") and body.endswith(">") and "\n" not in body
