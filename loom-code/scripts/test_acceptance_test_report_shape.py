"""Shape of the acceptance test report template (plan W0-01).

The report the user reads at decision point 3 is one table row per
Acceptance criterion -- verdict plus one plain sentence -- while the
evidence behind each row lives in a separate plain-markdown file under
the change's evidence directory. A re-run marks each verdict it did not
re-test as carried over, with a one-line reason; a re-tested row carries
no such reason. These tests pin that structure in the committed
template, not whole paragraphs.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
TEMPLATE = (
    REPO_ROOT / "loom-code" / "skills" / "closing-review" / "references"
    / "acceptance-test-report.md"
)
EVIDENCE_PATH = "docs/loom/<change-id>/evidence/acceptance-test-evidence.md"
ROWS_HEADING = "## What you asked for, one line at a time"
CARRIED = re.compile(r"^carried over — \S.*$")


def _fenced_blocks(text: str) -> list[str]:
    return re.findall(r"^```markdown\n(.*?)^```$", text, flags=re.M | re.S)


def _report_block() -> str:
    blocks = _fenced_blocks(TEMPLATE.read_text(encoding="utf-8"))
    assert blocks, "template has no ```markdown report block"
    return blocks[0]


def _criterion_table() -> tuple[list[str], list[list[str]]]:
    report = _report_block()
    assert ROWS_HEADING in report, "report block lost its criteria heading"
    section = report.split(ROWS_HEADING, 1)[1].split("\n## ", 1)[0]
    lines = [ln.strip() for ln in section.splitlines() if ln.strip().startswith("|")]
    assert len(lines) >= 3, "criteria section is not a table with rows"
    cells = [[c.strip() for c in ln.strip("|").split("|")] for ln in lines]
    header, rows = cells[0], cells[2:]
    assert set("".join(cells[1])) <= set("-: "), "second table line is not a separator"
    return header, rows


def _column(header: list[str], name: str) -> int:
    matches = [i for i, h in enumerate(header) if h.lower() == name.lower()]
    assert matches, f"criteria table has no {name!r} column: {header}"
    return matches[0]


def test_template_has_one_row_per_criterion_and_evidence_file_path():
    header, rows = _criterion_table()
    number = _column(header, "#")
    verdict = _column(header, "Verdict")
    assert all(len(r) == len(header) for r in rows), "ragged criteria rows"
    assert [r[number] for r in rows][:2] == ["1", "2"], "rows are not one per criterion"
    for row in rows:
        assert re.search(r"works|partly|not verified|fails", row[verdict]), row
    report = _report_block()
    assert "works / partly / not verified / fails" in TEMPLATE.read_text(encoding="utf-8")
    assert not re.search(r"^### \d+\.", report, flags=re.M), "per-criterion blocks remain"
    assert EVIDENCE_PATH in report, "report does not point to the evidence file"


def test_evidence_file_shape_is_given_and_is_plain_markdown():
    text = TEMPLATE.read_text(encoding="utf-8")
    blocks = _fenced_blocks(text)
    evidence = [b for b in blocks if "acceptance test evidence" in b.splitlines()[0].lower()]
    assert evidence, "template gives no shape for the evidence file"
    assert not evidence[0].startswith("#!")
    assert re.search(r"never[^\n]*`#!`", text), "template does not forbid `#!` evidence"


def test_template_row_carries_no_how_or_evidence_cell():
    header, rows = _criterion_table()
    banned = re.compile(r"how|evidence|command|tried|output|proof", re.I)
    assert not [h for h in header if banned.search(h)], header
    for row in rows:
        assert not [c for c in row if re.search(r"evidence|command|file:line", c, re.I)], row
    report = _report_block()
    assert "**How I tried it**" not in report
    assert "**Evidence**" not in report


def test_row_has_carried_over_marker_with_reason():
    header, rows = _criterion_table()
    rerun = _column(header, "Re-run")
    carried = [r[rerun] for r in rows if r[rerun].startswith("carried over")]
    assert carried, "no row shows the carried-over marker"
    assert all(CARRIED.match(c) for c in carried), carried
    assert all(c.split("—", 1)[1].strip() for c in carried), "carried row has an empty reason"


def test_retested_row_has_no_carry_reason():
    header, rows = _criterion_table()
    rerun = _column(header, "Re-run")
    retested = [r[rerun] for r in rows if r[rerun].startswith("re-tested")]
    assert retested, "no row shows a re-tested verdict"
    assert all(c == "re-tested" for c in retested), retested
