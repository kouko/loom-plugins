"""Shape of the acceptance test report template (plan W0-01).

The report the user reads at decision point 3 is one table row per
Acceptance criterion -- verdict plus one plain sentence -- while the
evidence behind each row lives in a separate plain-markdown file under
the change's evidence directory. A re-run marks each verdict it did not
re-test as carried over, with a one-line reason; a re-tested row carries
no such reason. These tests pin that structure in the committed
template, not whole paragraphs.

Plan W1-01 adds the tester's side: it leaves the package suite to
finalize-review, re-tests a criterion in full over every surface its
Acceptance line names, and these rules live in the tester's contract and
the template, under no new gate marker.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from prose_pin import flat_prose, has_negation, split_sentences  # noqa: E402

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


# --- plan W1-01: the tester's contract and the station's §3 ------------------

TESTER = REPO_ROOT / "loom-code" / "agents" / "acceptance-tester.md"
STATION = REPO_ROOT / "loom-code" / "skills" / "closing-review" / "SKILL.md"
STATION_GATES = {
    "review.absence-recovery",
    "review.atomic-claude-dispatch",
    "review.probe-graduation",
    "review.bounded-episode",
}


def _tester() -> list[str]:
    return split_sentences(flat_prose(TESTER))


def _section3() -> str:
    text = STATION.read_text(encoding="utf-8")
    return text.split("## 3. Run acceptance testing", 1)[1].split("\n## 4.", 1)[0]


def _affirmed(sentences: list[str], *phrases: str) -> list[str]:
    return [
        s for s in sentences
        if all(p in s for p in phrases) and not has_negation(re.sub(r"`[^`]*`", "", s))
    ]


def test_suite_criterion_cites_finalize_review_command():
    """A1 positive: a suite-settled row cites the check, not a result."""
    sentences = _tester()
    assert _affirmed(
        sentences, "cites the suite command", "`finalize-review` executes it",
        "refuses the attestation",
    ), "tester does not cite finalize-review's suite check"
    assert _affirmed(sentences, "committed before `finalize-review` runs")
    assert _affirmed(sentences, "`package-tests` is skipped", "only that criterion's own tests")
    assert _affirmed(sentences, "setup check", "every run")
    section = " ".join(_section3().split())
    assert "cites the suite command" in section
    assert "`finalize-review` executes" in section


def test_no_full_suite_run_instruction():
    """A1 negative: nothing tells the tester to run the whole suite."""
    flat = flat_prose(TESTER)
    assert "the name of a test you ran" not in flat, "evidence wording still invites named tests"
    run_suite = re.compile(r"\brun\w*\b[^.;]*\b(?:package|whole|full|complete) suite\b", re.I)
    offending = [
        s for s in _tester()
        if run_suite.search(s) and not has_negation(s)
        and "Build and `finalize-review` run the package suite" not in s
    ]
    assert offending == [], offending
    assert [s for s in _tester() if "full package suite" in s and has_negation(s)], (
        "tester contract does not forbid running the full package suite"
    )


def test_rerun_retests_every_named_surface():
    """A3 positive: a re-tested criterion is re-tested over every surface."""
    sentences = _tester()
    assert _affirmed(sentences, "re-test only the criteria the fix could affect", "in full")
    assert _affirmed(sentences, "every surface its Acceptance line names")
    assert _affirmed(sentences, "`carried over — <one-line reason>`", "Re-run column")
    assert _affirmed(sentences, "against the fix diff")
    assert _affirmed(sentences, "any doubt", "in full")


def test_partial_surface_retest_forbidden():
    """A3 negative: re-testing only the part a fix touched is never allowed."""
    touched = [s for s in _tester() if "the part the fix touched" in s]
    assert touched, "tester contract does not name the partial re-test trap"
    assert all(has_negation(s) for s in touched), touched
    section = [s for s in split_sentences(" ".join(_section3().split())) if "the part the fix touched" in s]
    assert all(has_negation(s) for s in section), section


def test_rules_live_in_contract_and_template():
    """A4 positive: the tester's contract, the template and §3 carry the rules."""
    flat = flat_prose(TESTER)
    assert "loom-code/skills/closing-review/references/acceptance-test-report.md" in flat
    assert EVIDENCE_PATH in flat
    header, _ = _criterion_table()
    _column(header, "Re-run")
    section = " ".join(_section3().split())
    assert EVIDENCE_PATH in section
    assert _affirmed(split_sentences(section), "committed with the report")


def test_no_new_gate_marker():
    """A4 negative: no gate marker carries these rules."""
    for path in (TESTER, TEMPLATE):
        assert "<!-- gate:" not in path.read_text(encoding="utf-8"), path.name
    text = STATION.read_text(encoding="utf-8")
    assert set(re.findall(r"<!-- gate: ([\w.-]+) -->", text)) == STATION_GATES
    ungated = re.sub(r"<!-- gate: [\w.-]+ -->.*?<!-- /gate -->", "", text, flags=re.S)
    flat = " ".join(ungated.split())
    for phrase in ("cites the suite command", "the part the fix touched", EVIDENCE_PATH):
        assert phrase in flat, f"{phrase!r} sits inside a gate block"
