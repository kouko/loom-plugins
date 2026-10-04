"""Adversarial probe: the code-first backfill pin must hold Acceptance 1.

concern: a pin that stays green when the baseline rewrites the characterise-first order or moves the predates-the-flow record off the plan.

Each case copies engineering-baseline.md, applies one hostile rewrite that
reverses an Acceptance 1 obligation, points the change's own pin test at the
copy and expects that unchanged test to fail.
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


def test_backfillpin_characteriseafterchange_fails(tmp_path, monkeypatch) -> None:
    """A rewrite that characterises after changing the code fails the pin."""
    assert _pin_fails_on(tmp_path, monkeypatch,
                         "included — before changing it,", "included — after changing it,")


def test_backfillpin_firstdropped_fails(tmp_path, monkeypatch) -> None:
    """A rewrite that drops 'first' from the characterise step fails the pin."""
    assert _pin_fails_on(tmp_path, monkeypatch,
                         "characterises that code first", "characterises that code eventually")


def test_backfillpin_recordmovedoffplan_fails(tmp_path, monkeypatch) -> None:
    """A rewrite that records the predating code outside the plan fails the pin."""
    assert _pin_fails_on(tmp_path, monkeypatch,
                         "and the plan records which code", "and the PR body records which code")
