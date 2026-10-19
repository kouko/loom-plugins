# concern: the test-budget guidance being turned into a line cap
"""Test-budget structure checks (change 2026-09-25-keep-mechanical-tests-small).

The budget's wording in implementer.md, adversarial.md and the lenses `tests`
row is review-only; this file keeps the no-line-cap and no-new-gate checks.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
IMPLEMENTER = REPO / "loom-code/agents/implementer.md"
ADVERSARIAL = REPO / "loom-code/skills/closing-review/references/adversarial.md"
LENSES = REPO / "loom-code/skills/closing-review/references/lenses.md"


def _read(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_budget_not_a_number_threshold():
    assert re.search(r"\b\d+\s+(?:net\s+)?(?:test\s+)?lines\b", _read(IMPLEMENTER)) is None


def test_no_new_gate_marker():
    count = sum(p.read_text(encoding="utf-8").count("<!-- gate:")
                for p in (IMPLEMENTER, ADVERSARIAL, LENSES))
    # lenses.md holds: the charter.plan-omission-narrow marker (1), the prose in
    # the skill-lens section explaining the "<!-- gate: <id> -->" form (1), and
    # the carve-out sentence in the tests dimension referencing the same syntax (1).
    # Total 3; this test ensures no new *actual* gate markers are added beyond these.
    assert count == 3
