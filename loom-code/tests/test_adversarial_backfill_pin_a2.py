"""Adversarial probe: the code-first backfill pin must hold Acceptance 2.

concern: a pin that stays green when an appended qualifier reverses a boundary, counting a compile failure as RED or deferring the iron law for code written after the flow began.

Each case copies engineering-baseline.md, appends one qualifier that reverses
an Acceptance 2 boundary without a negation token, points the change's own
pin test at the copy and expects that unchanged test to fail.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(subprocess.run(["git", "rev-parse", "--show-toplevel"],
                           capture_output=True, text=True, check=True).stdout.strip())
sys.path[:0] = [str(REPO / "loom-code" / "scripts"), str(REPO / "loom-code" / "tests")]

import test_prose_pin_rule_text as pin  # noqa: E402


def _pin_fails_on(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, old: str, new: str) -> bool:
    text = pin.BASELINE_MD.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"rewrite anchor drifted: {old!r}"
    copy = tmp_path / "engineering-baseline.md"
    copy.write_text(text.replace(old, new), encoding="utf-8")
    monkeypatch.setattr(pin, "BASELINE_MD", copy)
    try:
        pin.test_engineeringbaselinemd_codefirstbackfill_present()
    except AssertionError:
        return True
    return False


def test_backfillpin_compilefailurecountedasred_fails(tmp_path, monkeypatch) -> None:
    """A rewrite that counts a compile failure as RED evidence fails the pin."""
    assert _pin_fails_on(tmp_path, monkeypatch,
                         "proves only that an\ninterface is missing;",
                         "proves only that an\ninterface is missing, which counts as RED evidence;")


def test_backfillpin_latercodeirondeferred_fails(tmp_path, monkeypatch) -> None:
    """A rewrite that defers the iron law for later code fails the pin."""
    assert _pin_fails_on(tmp_path, monkeypatch,
                         "Code written after the flow\nbegan follows the iron law.",
                         "Code written after the flow\nbegan follows the iron law once the backfill ends.")
