"""The live plan contract has one ordinary task-id form."""

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRITE_PLAN = ROOT / "loom-code/skills/write-plan/SKILL.md"
SPEC_MINIMAL = ROOT / "loom-code/contract/templates/spec-minimal.md"
WRITE_SPEC_REFS = ROOT / "loom-design/skills/write-spec/references"


def test_task_ids_use_one_numeric_form_without_reserved_process_tasks() -> None:
    text = WRITE_PLAN.read_text(encoding="utf-8")
    shape = text.split("**Shape.**", 1)[1].split("**Sections.**", 1)[0]
    assert "Task ids are `W<n>-<nn>`" in shape
    assert "W<n>-memory" not in shape


# --- W1-03 (2026-09-15-readable-flow-details): write-plan mirrors the
# carried-details and flow-form guidance of capture-intent and write-spec ---

_STEP1 = "## Step 1 — Find the intent"
_STEP3 = "## Step 3 — Decision point ①: restate and confirm"
_STEP4 = "## Step 4 — Does this need a spec?"
_PRODUCT_GATE = "<!-- gate: write-plan.product-spec-needs-confirmed-behavior -->"


def _flat(text: str) -> str:
    return " ".join(text.split())


def _text() -> str:
    return WRITE_PLAN.read_text(encoding="utf-8")


def _section(heading: str) -> str:
    m = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", _text(), re.M | re.S)
    assert m, f"section {heading!r} missing"
    return m.group(0)


def _sentences(flat: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.])\s+", flat) if s.strip()]


def _readback_paragraph() -> str:
    """The paragraph that sits just before the product-spec gate marker."""
    before = _section(_STEP4).split(_PRODUCT_GATE, 1)[0]
    return _flat(before.rstrip().rsplit("\n\n", 1)[-1])


def test_carried_details_force_minimal_spec() -> None:
    """A1 positive: a non-empty carried-details list forces a minimal spec."""
    step3 = _flat(_section(_STEP3))
    assert "**Keep a carried-details list**" in step3
    assert "the user stated or explicitly agreed to" in step3
    assert "never an agent proposal or detail you inferred" in step3
    assert "never enters the intent file" in step3
    step4 = _flat(_section(_STEP4))
    assert re.search(
        r"non-empty carried-details list — from `capture-intent`'s hand-off or "
        r"your own intake — forces that spec",
        step4,
    )
    assert "record each carried detail" in step4.lower()
    assert "as a UI flows line when visible" in step4
    assert "an agent proposal the user did not agree to is not recorded" in step4


def test_no_details_keeps_evidence_only_plan() -> None:
    """A1 negative: an empty list forces no spec; the evidence-only plan stays."""
    step4 = _flat(_section(_STEP4))
    assert "An empty list forces no spec" in step4
    forcing = [s for s in _sentences(step4) if "forces that spec" in s]
    assert forcing and all("non-empty" in s for s in forcing)
    assert "The plan carries the Current State Evidence section instead of a spec." in step4
    gate = _text().split("<!-- gate: write-plan.no-plan-without-confirmed-intent -->", 1)[1]
    assert "carried-details" not in gate.split("<!-- /gate -->", 1)[0]


def test_write_plan_readback_leads_with_table_or_text_diagram() -> None:
    """A3 positive: ② for a spec write-plan wrote leads with a table or text diagram."""
    para = _readback_paragraph()
    assert "② on a product spec you wrote" in para
    assert re.search(
        r"parallel cases or branches, lead with a table or a text \(ASCII\) diagram",
        para,
    )
    assert "then the per-case sentences" in para


def test_write_plan_readback_has_no_mermaid() -> None:
    """A3 negative: no Mermaid in the chat read-back; gate text untouched."""
    para = _readback_paragraph()
    assert "never put Mermaid in this message" in para
    assert "a terminal shows it as raw code" in para
    assert "```mermaid" not in _text()
    gate = _section(_STEP4).split(_PRODUCT_GATE, 1)[1].split("### ", 1)[0]
    assert "per-case sentences" not in gate
    assert "Mermaid" not in gate


def test_both_stations_share_form_rules() -> None:
    """A4 positive: write-plan and write-spec state the same flow-form rules."""
    plan = _flat(_section(_STEP4))
    flows = _flat((WRITE_SPEC_REFS / "ui-flows.md").read_text(encoding="utf-8"))
    forms = _flat((WRITE_SPEC_REFS / "spec-forms.md").read_text(encoding="utf-8"))
    for text in (plan, flows):
        assert "several parallel cases on one surface" in text.lower()
        assert "`case | what the user does | what they see`" in text
        assert re.search(
            r"branch or go back and forth.*`stateDiagram-v2` or `flowchart`", text
        )
    assert "`<action> → <reaction>` lines" in plan
    assert "`stateDiagram-v2` or `flowchart`" in forms
    back = _flat((WRITE_SPEC_REFS / "ui-flows.md").read_text(encoding="utf-8"))
    for text in (_readback_paragraph(), back):
        assert "lead with a table or a text (ASCII) diagram" in text
        assert "a terminal shows it as raw code" in text


def test_template_placeholder_names_table_and_diagram() -> None:
    """A4 boundary: the spec-minimal UI flows placeholder points to the forms."""
    text = SPEC_MINIMAL.read_text(encoding="utf-8")
    body = text.split("## UI flows", 1)[1].split("\n", 1)[1].strip()
    assert body.startswith("<") and body.endswith(">") and "\n" not in body
    for phrase in ("`<action> → <reaction>`", "table", "`case | what the user does | what they see`",
                   "stateDiagram-v2", "flowchart", "N/A"):
        assert phrase in body, phrase


def test_write_plan_intake_shows_carried_details_table() -> None:
    """A5 positive: write-plan's own ① shows carried details as a table."""
    step3 = _flat(_section(_STEP3))
    assert "**The carried details, `kind: engineering` only**" in step3
    assert "as a table, one row per detail in the user's language" in step3
    assert "confirmed by the same yes; no extra stop" in step3
    step1 = _flat(_section(_STEP1))
    assert "Any intent section may use a Markdown table or diagram" in step1
    assert "Acceptance stays a numbered list" in step1
    assert "no UI reactions or state transitions" in step1
    assert "Mermaid node ids included" in step1
    assert "text tables or text diagrams, not Mermaid" in step1


def test_write_plan_no_details_no_table() -> None:
    """A5 boundary: an empty list shows no table."""
    step3 = _flat(_section(_STEP3))
    assert "With an empty list, no table appears" in step3
    tables = [s for s in _sentences(step3) if "as a table" in s]
    assert tables and all("engineering" in s for s in tables)
