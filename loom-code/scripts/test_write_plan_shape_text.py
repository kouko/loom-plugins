"""The live plan contract has one ordinary task-id form."""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prose_pin import has_negation, split_sentences  # noqa: E402


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
    return split_sentences(flat, ".;")


def _affirmed(text: str, *literals: str) -> list[str]:
    """Sentences holding every literal and no negation token outside code spans.

    Engineering baseline prose-pin rule: a pinned sentence rejects negation,
    so "Never assume that a non-empty carried-details list ... forces that
    spec" cannot pass a pin on "forces that spec". Backticked spans such as
    `needs-design: no` are field values, not negations.
    """
    return [
        s
        for s in _sentences(_flat(text))
        if all(lit in s for lit in literals)
        and not has_negation(re.sub(r"`[^`]*`", "", s))
    ]


def _readback_paragraph() -> str:
    """The paragraph that sits just before the product-spec gate marker."""
    before = _section(_STEP4).split(_PRODUCT_GATE, 1)[0]
    return _flat(before.rstrip().rsplit("\n\n", 1)[-1])


def _carried_item() -> str:
    step3 = _flat(_section(_STEP3))
    return step3.split("5. **The carried details", 1)[1].split("**Every question in this message", 1)[0]


def _record_bullet() -> str:
    step4 = _section(_STEP4)
    return "Record each carried detail" + step4.split("- Record each carried detail", 1)[1].split("\n\n", 1)[0]


def test_affirmedPin_syntheticAffirmativeSentence_accepted() -> None:
    """Self-test: an affirmative sentence satisfies the pin."""
    assert _affirmed("A non-empty carried-details list forces that spec.", "forces that spec")


def test_affirmedPin_syntheticNegatedSentence_rejected() -> None:
    """Self-test: the same sentence carrying a negation token fails the pin."""
    for negated in (
        "Never assume that a non-empty carried-details list forces that spec.",
        "It is not the case that a non-empty list forces that spec.",
        "Do not record it on its Requirement line.",
    ):
        literal = "Requirement line" if "Requirement" in negated else "forces that spec"
        assert not _affirmed(negated, literal), negated


def test_affirmedPin_syntheticCodeSpanNo_notNegation() -> None:
    """Self-test: a field value in backticks is not read as a negation token."""
    assert _affirmed("For a product change with `needs-design: no`, show them.", "show them")


def test_carried_details_force_minimal_spec() -> None:
    """A1 positive: a non-empty carried-details list forces a minimal spec."""
    step3 = _flat(_section(_STEP3))
    assert _affirmed(step3, "**Keep a carried-details list**", "the user stated or explicitly agreed to")
    assert "Never carry an agent proposal the user did not agree to, or detail you inferred" in step3
    assert "never enters the intent file" in step3
    step4 = _flat(_section(_STEP4))
    assert _affirmed(
        step4,
        "non-empty carried-details list — from `capture-intent`'s hand-off or "
        "your own intake — forces that spec",
    )
    assert _affirmed(_record_bullet(), "Record each carried detail as a UI flows line when visible")
    assert "An agent proposal the user did not agree to is not recorded" in _flat(_record_bullet())


def test_no_details_keeps_evidence_only_plan() -> None:
    """A1 negative: an empty list forces no spec; the evidence-only plan stays."""
    step4 = _flat(_section(_STEP4))
    assert "An empty list forces no spec" in step4
    forcing = [s for s in _sentences(step4) if "forces that spec" in s]
    assert forcing and all("non-empty" in s for s in forcing)
    assert all(_affirmed(s, "forces that spec") for s in forcing)
    assert _affirmed(step4, "The plan carries the Current State Evidence section instead of a spec.")
    gate = _text().split("<!-- gate: write-plan.no-plan-without-confirmed-intent -->", 1)[1]
    assert "carried-details" not in gate.split("<!-- /gate -->", 1)[0]


def test_write_plan_readback_leads_with_table_or_text_diagram() -> None:
    """A3 positive: ② for a spec write-plan wrote leads with a table or text diagram."""
    para = _readback_paragraph()
    assert _affirmed(para, "② on a product spec you wrote")
    assert _affirmed(
        para,
        "parallel cases or branches, lead with a table or a text (ASCII) diagram",
        "then the per-case sentences",
    )


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
    assert _affirmed(
        plan, "several parallel cases on one surface, a table `case | what the user does | what they see`"
    )
    assert _affirmed(plan, "branch or go back and forth", "`stateDiagram-v2` or `flowchart`")
    assert _affirmed(plan, "a short flow is `<action> → <reaction>` lines")
    assert "several parallel cases on one surface" in flows.lower()
    assert "`case | what the user does | what they see`" in flows
    assert re.search(r"branch or go back and forth.*`stateDiagram-v2` or `flowchart`", flows)
    assert "`stateDiagram-v2` or `flowchart`" in forms
    for text in (_readback_paragraph(), flows):
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
    """A5 positive: write-plan's own ① shows carried details as a table where it is their only stop."""
    step3 = _flat(_section(_STEP3))
    assert "**The carried details, where this is their only stop**" in step3
    item = _carried_item()
    assert _affirmed(item, "for `kind: engineering` and for a product change with `needs-design: no`")
    assert _affirmed(item, "Show them as a table, one row per detail in the user's language")
    assert "confirmed by the same yes; no extra stop" in item
    step1 = _flat(_section(_STEP1))
    assert _affirmed(step1, "Any intent section may use a Markdown table or a Mermaid `flowchart`")
    assert "Acceptance stays a numbered list" in step1
    assert "no UI reactions or state transitions" in step1
    assert "Mermaid node ids included" in step1
    assert "text tables or text diagrams, not Mermaid" in step1


def test_write_plan_no_details_no_table() -> None:
    """A5 boundary: an empty list shows no table; a needs-design: yes product defers to ②."""
    step3 = _flat(_section(_STEP3))
    item = _carried_item()
    assert "With an empty list, no table appears" in item
    assert step3.count("as a table") == item.count("as a table") >= 1
    assert _affirmed(item, "A product change with `needs-design: yes` shows them at decision point ② instead")


# --- W3-02: adversary findings (explicit yes, where a product detail lands) ---


def test_write_plan_only_explicit_yes_is_carried() -> None:
    """A1 positive: only the user's explicit yes makes a proposal a carried detail."""
    assert _affirmed(_section(_STEP3), "Only an explicit yes from the user counts as agreement")


def test_write_plan_unanswered_proposal_dropped() -> None:
    """A1 negative: silence, "later", or an answer about something else drops it."""
    assert _affirmed(
        _section(_STEP3),
        "a proposal left unanswered, deferred",
        "answered about something else is dropped",
    )


def test_product_non_visible_detail_on_requirement_line() -> None:
    """A3 positive: a non-visible carried detail lands on its Requirement line."""
    assert _affirmed(_record_bullet(), "as a UI flows line when visible, else on its Requirement line")


def test_product_detail_not_on_design_decision() -> None:
    """A3 negative: only an engineering change may record one on a Design decision line."""
    routing = [s for s in _sentences(_flat(_record_bullet())) if "Design decision line" in s]
    assert routing
    assert all(_affirmed(s, "only an engineering change may put one on a Design decision line") for s in routing)
