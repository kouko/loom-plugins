"""The live plan contract has one ordinary task-id form."""

import re
from pathlib import Path


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


def test_product_gate_presents_product_one_way_doors() -> None:
    """Decision point ② lists the product one-way doors routed to it from ①."""
    gate = _section(_STEP4).split(_PRODUCT_GATE, 1)[1].split("### ", 1)[0]
    assert "product one-way doors" in re.sub(r"\s+", " ", gate)


def test_template_placeholder_names_table_and_diagram() -> None:
    """A4 boundary: the spec-minimal UI flows section is one placeholder line."""
    text = SPEC_MINIMAL.read_text(encoding="utf-8")
    body = text.split("## UI flows", 1)[1].split("\n", 1)[1].strip()
    assert body.startswith("<") and body.endswith(">") and "\n" not in body
