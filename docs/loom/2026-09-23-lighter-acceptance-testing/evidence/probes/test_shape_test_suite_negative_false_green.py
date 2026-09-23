"""Adversarial probe: the "no full-suite run" shape test must catch a contract that says to run it.

The shape test `test_no_full_suite_run_instruction` is the only executable
guard behind Acceptance 1 ("the acceptance tester does not run the full
package suite"). This probe feeds it a copy of the tester's contract with one
added sentence that tells the tester to run the whole package's tests, and
expects the shape test to go RED. At the change as committed the shape test
stays GREEN on both copies, so a contract that re-instates the full-suite run
would pass its own guard.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-23-lighter-acceptance-testing/evidence/probes/test_shape_test_suite_negative_false_green.py -q

concern: false-green guard -- the tester-contract negative for Acceptance 1 passes a contract that instructs a full package-suite run
"""
from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code" / "scripts"))
shape = importlib.import_module("test_acceptance_test_report_shape")

ANCHOR = "remembered result is not evidence."


def _mutated_contract(tmp_path: Path, extra: str) -> Path:
    text = shape.TESTER.read_text(encoding="utf-8")
    assert ANCHOR in text, "probe anchor sentence is gone from the tester contract"
    path = tmp_path / "acceptance-tester.md"
    path.write_text(text.replace(ANCHOR, ANCHOR + " " + extra, 1), encoding="utf-8")
    return path


def _shape_test_fails_on(monkeypatch, path: Path) -> bool:
    monkeypatch.setattr(shape, "TESTER", path)
    try:
        shape.test_no_full_suite_run_instruction()
    except AssertionError:
        return True
    return False


def test_suitenegative_pytestoverwholepackage_turnsred(tmp_path, monkeypatch):
    """A sentence telling the tester to run pytest over the whole package must turn the shape test RED."""
    path = _mutated_contract(
        tmp_path,
        "Then run `python3 -m pytest loom-code -q` over the whole package and record its output.",
    )
    assert _shape_test_fails_on(monkeypatch, path), (
        "shape test stayed GREEN on a contract that tells the tester to run the whole package's tests"
    )


def test_suitenegative_negationelsewhereinsentence_turnsred(tmp_path, monkeypatch):
    """A full-suite run instruction must not escape because an unrelated clause carries a negation token."""
    path = _mutated_contract(
        tmp_path, "Run the full package suite first, unless it is not installed."
    )
    assert _shape_test_fails_on(monkeypatch, path), (
        "shape test stayed GREEN: any negation token anywhere in the sentence exempts a full-suite run instruction"
    )


def test_suitenegative_unmutatedcontract_staysgreen(monkeypatch):
    """Control: the committed contract itself passes the shape test, so a RED above is the mutation's doing."""
    assert not _shape_test_fails_on(monkeypatch, shape.TESTER)
