"""Adversarial probe: the "row carries no evidence" shape test must catch evidence pasted into a row.

Acceptance 2 moves the commands, output and file:line out of the report into
the evidence file. Its only executable guard is
`test_template_row_carries_no_how_or_evidence_cell`, which bans a few words in
the header and the literal strings "evidence", "command" and "file:line" in a
cell. This probe hands it two template copies that paste evidence back into the
report: a row whose sentence is a command, its output and a source location,
and a table with an extra "Details" column for typed input and captured
output. At the change as committed the shape test stays GREEN on both.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-23-lighter-acceptance-testing/evidence/probes/test_shape_test_evidence_in_row_false_green.py -q

concern: false-green guard -- the template negative for Acceptance 2 passes a report row that carries commands, output and a source location
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code" / "scripts"))
shape = importlib.import_module("test_acceptance_test_report_shape")

ROW1 = "| 1 | <the intent's first Acceptance line, verbatim> | works | <one plain sentence> | re-tested |"
HEADER = "| # | What you asked for | Verdict | What happened | Re-run |\n|---|---|---|---|---|"


def _template(tmp_path: Path, text: str) -> Path:
    path = tmp_path / "acceptance-test-report.md"
    path.write_text(text, encoding="utf-8")
    return path


def _shape_test_fails_on(monkeypatch, path: Path) -> bool:
    monkeypatch.setattr(shape, "TEMPLATE", path)
    try:
        shape.test_template_row_carries_no_how_or_evidence_cell()
    except AssertionError:
        return True
    return False


def test_rownegative_pastedcommandoutputlocation_turnsred(tmp_path, monkeypatch):
    """A row sentence that is a pasted command, its output and a file location must turn the shape test RED."""
    text = shape.TEMPLATE.read_text(encoding="utf-8")
    assert ROW1 in text, "probe anchor row is gone from the template"
    pasted = ROW1.replace(
        "<one plain sentence>", "ran `python3 -m pytest -q`: 42 passed; see loom-code/x.py:12"
    )
    path = _template(tmp_path, text.replace(ROW1, pasted, 1))
    assert _shape_test_fails_on(monkeypatch, path), (
        "shape test stayed GREEN on a row carrying a command, its output and a source location"
    )


def test_rownegative_extradetailscolumn_turnsred(tmp_path, monkeypatch):
    """An extra table column holding typed input and captured output must turn the shape test RED."""
    text = shape.TEMPLATE.read_text(encoding="utf-8")
    assert HEADER in text, "probe anchor header is gone from the template"
    text = (
        text.replace(HEADER, "| # | What you asked for | Verdict | What happened | Re-run | Details |\n|---|---|---|---|---|---|", 1)
        .replace("| re-tested |", "| re-tested | <typed input and captured stdout> |", 1)
        .replace(
            "| carried over — <one-line reason> |",
            "| carried over — <one-line reason> | <typed input and captured stdout> |",
            1,
        )
    )
    path = _template(tmp_path, text)
    assert _shape_test_fails_on(monkeypatch, path), (
        "shape test stayed GREEN on a table with a Details column for typed input and captured stdout"
    )


def test_rownegative_unmutatedtemplate_staysgreen(monkeypatch):
    """Control: the committed template itself passes the shape test, so a RED above is the mutation's doing."""
    assert not _shape_test_fails_on(monkeypatch, shape.TEMPLATE)
