"""Adversary probe: run_ab.py --out refusal is bypassed by a case variant.

`set_output` refuses an output dir inside the 2026-09-14 change by comparing
resolved path strings. On a case-insensitive filesystem (the macOS default)
the same directory spelled with different case resolves to a different string,
so streams and results.md land inside the old change.

concern: the --out guard that keeps rerun output out of the 2026-09-14 change is bypassed by the same directory spelled in another case.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

AB = Path(__file__).resolve().parents[3] / "2026-09-14-loom-visualization-description-trigger/ab"
sys.path.insert(0, str(AB))
import run_ab  # noqa: E402


def test_run_ab_out_case_variant_of_old_change_refused() -> None:
    """The old change dir spelled in upper case is still refused when it is the same directory."""
    variant = run_ab.CHANGE_DIR.parent / run_ab.CHANGE_DIR.name.upper() / "evidence"
    if not variant.parent.exists():
        pytest.skip("case-sensitive filesystem: the variant is a different directory")
    with pytest.raises(SystemExit):
        run_ab.set_output(variant)
