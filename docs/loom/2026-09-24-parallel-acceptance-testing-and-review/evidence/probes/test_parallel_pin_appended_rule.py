"""Adversarial probe: an appended contradicting rule in the §3 paragraph fails the pins.
concern: false-green prose pin — the §3 acceptance-testing paragraph can gain a sentence
that reverses the parallel start and the not-a-verdict rule while every pin stays green.

`test_parallel_acceptance_review_text.py` states that "a reversed, re-assigned or appended
rule must fail". Its §3 slice ends at the skip sentence ("When `acceptance-test` is
skipped ..."), which sits in the same Markdown paragraph as the new rules, so a sentence
appended after the skip sentence is outside every pin.

This probe copies `loom-code/` from the working tree into a temporary directory, checks
that the pins pass there unchanged, appends one contradicting sentence to that paragraph
in the copy, and expects the pins to fail. Run from the repo root:

    python3 -m pytest docs/loom/2026-09-24-parallel-acceptance-testing-and-review/evidence/probes/test_parallel_pin_appended_rule.py -q
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SKILL_REL = "loom-code/skills/closing-review/SKILL.md"
PINS = (
    "loom-code/scripts/test_parallel_acceptance_review_text.py::test_new_rules_are_pinned_exactly",
    "loom-code/scripts/test_review_convergence_contract.py",
)
SKIP_END = "the user's plain-words instruction), run no acceptance testing.\n"
APPENDED = (
    "the user's plain-words instruction), run no acceptance testing. Otherwise\n"
    "dispatch the reviewers only after the report is committed, and a reviewer's\n"
    "return before the report is its verdict.\n"
)


def _copy(dst: Path) -> None:
    shutil.copytree(REPO / "loom-code", dst / "loom-code",
                    ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache"))


def _pins(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *PINS],
                          cwd=root, capture_output=True, text=True)


def test_parallelpin_appendedcontradiction_fails(tmp_path: Path) -> None:
    """The pins pass on an unchanged copy and fail once a contradicting rule is appended."""
    _copy(tmp_path)
    baseline = _pins(tmp_path)
    assert baseline.returncode == 0, "pins must pass on the unchanged copy:\n" + baseline.stdout
    skill = tmp_path / SKILL_REL
    text = skill.read_text(encoding="utf-8")
    assert text.count(SKIP_END) == 1
    skill.write_text(text.replace(SKIP_END, APPENDED, 1), encoding="utf-8")
    mutated = _pins(tmp_path)
    assert mutated.returncode != 0, (
        "an appended rule reversing the parallel start and the not-a-verdict rule "
        "left every pin green:\n" + mutated.stdout)
