"""Pins the test budget (change 2026-09-25-keep-mechanical-tests-small).

One assertion per plan case. A4's rule count is already pinned by
`test_loom_checker_cli.py` (`--list-rules` has 26 lines), so it is not
repeated here.
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


def test_implementer_states_budget_and_net_lines():
    text = _read(IMPLEMENTER)
    assert (
        "at most one positive and one negative or boundary case per Acceptance line or finding"
        in text
        and "existing helpers and fixtures" in text
        and "no new test harness" in text
        and "no tests of tests" in text
        and "net_test_lines:" in text
    )


def test_budget_not_a_number_threshold():
    assert re.search(r"\b\d+\s+(?:net\s+)?(?:test\s+)?lines\b", _read(IMPLEMENTER)) is None


def test_adversarial_probe_small_reuses_helpers():
    text = _read(ADVERSARIAL)
    assert (
        "Each probe program stays small and reuses the repository's existing test helpers"
        in text
        and "no harness built for one case" in text
    )


def test_five_program_cap_unchanged():
    assert "A change commits **at most five** probe programs" in _read(ADVERSARIAL)


def test_tests_dimension_overbuilt_is_finding():
    row = next(line for line in LENSES.read_text(encoding="utf-8").splitlines()
               if line.startswith("| tests |"))
    assert "tests beyond what the behaviour needs" in row and "names the smaller shape" in row


def test_fix_adds_at_most_one_test():
    row = next(line for line in LENSES.read_text(encoding="utf-8").splitlines()
               if line.startswith("| tests |"))
    assert "adds at most one test, extending an existing test first" in row


def test_no_new_gate_marker():
    count = sum(p.read_text(encoding="utf-8").count("<!-- gate:")
                for p in (IMPLEMENTER, ADVERSARIAL, LENSES))
    # lenses.md already holds two: the charter.plan-omission-narrow marker and
    # the prose that explains the `<!-- gate: <id> -->` form.
    assert count == 2
