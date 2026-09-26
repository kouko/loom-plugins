"""W0-03 — write-plan reads ARCHITECTURE.md; the code lens scores conformance.

Acceptance 5: write-plan Step 5 places files by ARCHITECTURE.md's rules and
names the rule id on the task's Risk line; with no file, nothing changes.
Acceptance 6: the code lens has an `architecture-conformance` row, `N/A`
without the file; reviewer.md lists it; the reviewer-count wording stays.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
WRITE_PLAN = REPO / "loom-code/skills/write-plan/SKILL.md"
LENSES = REPO / "loom-code/skills/closing-review/references/lenses.md"
REVIEWER = REPO / "loom-code/agents/reviewer.md"
CLOSING = REPO / "loom-code/skills/closing-review/SKILL.md"


def _step5_architecture_paragraph() -> str:
    text = WRITE_PLAN.read_text(encoding="utf-8")
    step5 = text[text.index("## Step 5"):]
    step5 = step5[: step5.index("\n## ", 1)]
    paras = [" ".join(p.split()) for p in step5.split("\n\n")]
    hits = [p for p in paras if "ARCHITECTURE.md" in p]
    assert hits, "write-plan Step 5 never mentions ARCHITECTURE.md"
    return hits[0]


def test_write_plan_step5_reads_architecture_and_names_rule() -> None:
    para = _step5_architecture_paragraph()
    assert "Risk line" in para and "rule id" in para, para
    assert "ratified-by: <name> <date>" in para
    assert "Treat an unratified draft as advisory" in para


def test_absent_architecture_doc_adds_no_step() -> None:
    para = _step5_architecture_paragraph()
    assert re.search(r"[Ww]ith no `?ARCHITECTURE\.md`?, nothing changes", para), para
    assert "an implementer never changes a rule" in para, para


def test_code_lens_has_architecture_conformance_na_without_doc() -> None:
    text = LENSES.read_text(encoding="utf-8")
    code = text[text.index("## Code — twelve dimensions"):text.index("## Docs")]
    assert re.search(r"^\| architecture-conformance \|.*at least `important`", code, re.M), code
    assert re.search(r"^\| architecture \| .*SOLID", code, re.M), "SOLID row changed"
    na_rule = " ".join(text[text.index("A dimension with nothing to conform to"):].split())[:200]
    assert "`ARCHITECTURE.md`" in na_rule, na_rule
    assert "Scored only for ratified rules" in code
    assert "ratified-by: <name> <date>" in code


def test_reviewer_lists_it_and_reviewer_count_unchanged() -> None:
    row = next(
        line for line in REVIEWER.read_text(encoding="utf-8").splitlines()
        if line.startswith("| `code` |")
    )
    assert "architecture-conformance" in row, row
    closing = " ".join(CLOSING.read_text(encoding="utf-8").split())
    assert "fails closed to two when it cannot classify the whole change" in closing
