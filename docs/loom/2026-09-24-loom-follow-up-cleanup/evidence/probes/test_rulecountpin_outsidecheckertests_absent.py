# concern: a test outside the checker's own tests still pins the checker's rule count as a literal integer
"""Adversarial probe for 2026-09-24-loom-follow-up-cleanup, Acceptance 4.

Acceptance 4: no test outside the checker's own tests pins the checker's
rule count as a literal. The checker's own tests are the
`test_loom_checker_*.py` modules, which the plan names as already pinning
the count.

The change's guard (`test_fix_scope_text.py`) allowlists
`test_probes_language_policy.py` as a "checker test" and looks only six
lines after a `--list-rules` mention. That language-policy probe still
asserts `len(lines) == 26` about sixteen lines after its `--list-rules`
mention, so the guard is green while the acceptance line is false.

This probe computes the current rule count from the checker itself and
flags any comparison against that integer that sits within twenty lines
after a `--list-rules` / `list_rules` / `RULES` mention, in every test
module of the three plugin trees except the checker's own tests.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
CHECKER = REPO / "loom-code/scripts/loom_checker.py"
TREES = ("loom-code", "loom-design", "loom-workflow")
WINDOW = 20
MENTION = re.compile(r"--list-rules|list_rules|\bRULES\b|\bRULE_IDS\b|\brule_ids\b")


def _rule_count() -> int:
    out = subprocess.run(
        [sys.executable, str(CHECKER), "--list-rules"],
        cwd=REPO, capture_output=True, text=True, check=True,
    ).stdout
    return len([line for line in out.splitlines() if line.strip()])


def _literal_pins(text: str, count: int) -> list[str]:
    compare = re.compile(rf"==\s*{count}\b|\b{count}\s*==")
    lines = text.splitlines()
    return [
        line.strip() for i, line in enumerate(lines)
        if compare.search(line)
        and any(MENTION.search(x) for x in lines[max(0, i - WINDOW):i + 1])
    ]


def _is_checker_own_test(path: Path) -> bool:
    return path.name.startswith("test_loom_checker_")


def test_rulecountpin_outsidecheckertests_absent() -> None:
    """No test module outside the checker's own tests compares against the
    checker's current rule count near a rule-list mention."""
    count = _rule_count()
    hits = {}
    for tree in TREES:
        for path in sorted((REPO / tree).rglob("test_*.py")):
            if _is_checker_own_test(path) or "__pycache__" in path.parts:
                continue
            found = _literal_pins(path.read_text(encoding="utf-8"), count)
            if found:
                hits[str(path.relative_to(REPO))] = found
    assert hits == {}, hits


def test_rulecountpin_farsample_detected() -> None:
    """Self-test: a pin sixteen lines after the mention is caught."""
    eq = "=="
    sample = 'run([CHECKER, "--list-rules"])\n' + "x = 1\n" * 15 + f"assert len(lines) {eq} 26\n"
    assert _literal_pins(sample, 26) == [f"assert len(lines) {eq} 26"]


def test_rulecountpin_cleansample_passes() -> None:
    """Self-test: a rule-list test with no literal count is not flagged."""
    sample = 'ids = run([CHECKER, "--list-rules"]).stdout.splitlines()\nassert ids == sorted(ids)\n'
    assert _literal_pins(sample, 26) == []
