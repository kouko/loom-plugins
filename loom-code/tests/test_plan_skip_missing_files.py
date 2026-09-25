# concern: the simplicity skip-line path crashes on a task missing its Files line instead of reporting the missing field
"""Adversarial probe: a charter 1.1 plan whose task lacks a Files line and
whose Simplicity check is the narrow skip line must be blocked with the
ordinary `T1.Files missing` finding, not crash the checker.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-25-plan-simplicity-check/evidence/probes/test_plan_skip_missing_files.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-code" / "tests"))
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))

from test_plan_field_caps import _plan  # noqa: E402
from loom_checker.rule_checks.intake import check_plan_field_caps  # noqa: E402


def test_fieldcaps_skiplinewithmissingfiles_reportsfilesmissing() -> None:
    """A task missing its Files line under a skip-line record yields the
    `T1.Files missing` block rather than raising TypeError."""
    plan = _plan(charter="charter: 1.1", simplicity="- skipped — narrow change")
    plan = plan.replace("- Files: src/a.py, src/b.py\n", "")
    failures = check_plan_field_caps(plan)
    assert ("plan.field-caps", "T1.Files missing") in failures
