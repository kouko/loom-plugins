# concern: a carve-out sentence added beside the excess rule in reviewer.md makes the rule skippable while the exact-sentence pin stays green
"""Adversary probe for Acceptance 2 of 2026-11-28-review-unrequested-behaviour.

Acceptance 2: when the excess rule is deleted or made skippable, a package
suite test fails. The shipped pin checks only that the rule's sentence is
present verbatim. These cases leave that sentence untouched and add a
separate sentence that lets a reviewer skip the excess direction. Each case
copies `loom-code/` to a temporary directory, runs the reviewer-reading
tests on the pristine copy and on the copy with the carve-out, and requires
at least one test that passes on the pristine copy to fail on the carve-out.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
REVIEWER_REL = Path("loom-code/agents/reviewer.md")
RULE_END = "including one that skipped the spec."

CARVE_OUTS = {
    "adjacent_may_skip": (
        RULE_END,
        RULE_END + " You may skip the excess direction when the change is small.",
    ),
    "separate_paragraph_no_spec": (
        "never `important` or `fatal` on style alone.",
        "never `important` or `fatal` on style alone.\n\n"
        "**Excess, when the change skipped the spec.** Raise no excess "
        "finding for a change that has no spec; the spec lens owns that "
        "direction.",
    ),
}


def _reviewer_tests(tree: Path) -> list[str]:
    tests = tree / "loom-code/tests"
    return sorted(
        str(p.relative_to(tree))
        for p in tests.glob("test_*.py")
        if "reviewer.md" in p.read_text(encoding="utf-8")
    )


def _failures(tree: Path) -> set[str]:
    env = {k: v for k, v in os.environ.items()
           if k not in {"FORCE_COLOR", "CLAUDE_CODE_SESSION_ID", "PYTEST_ADDOPTS"}}
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", "-rf",
         "--continue-on-collection-errors", *_reviewer_tests(tree)],
        cwd=tree, env=env, capture_output=True, text=True,
    )
    return {line.split(" - ")[0] for line in proc.stdout.splitlines()
            if line.startswith(("FAILED ", "ERROR "))}


def _copy(dest: Path) -> Path:
    shutil.copytree(ROOT / "loom-code", dest / "loom-code",
                    ignore=shutil.ignore_patterns("__pycache__", "node_modules"))
    return dest


@pytest.mark.parametrize("case", sorted(CARVE_OUTS))
def test_excess_rule_carve_out_fails_package_test(case: str, tmp_path: Path) -> None:
    """A carve-out that makes the excess rule skippable must fail a test."""
    pristine = _copy(tmp_path / "pristine")
    mutated = _copy(tmp_path / "mutated")
    anchor, replacement = CARVE_OUTS[case]
    path = mutated / REVIEWER_REL
    text = path.read_text(encoding="utf-8")
    assert text.count(anchor) == 1, "mutation anchor must match exactly once"
    path.write_text(text.replace(anchor, replacement), encoding="utf-8")
    assert path.read_text(encoding="utf-8") != (pristine / REVIEWER_REL).read_text(encoding="utf-8")

    new_failures = _failures(mutated) - _failures(pristine)
    assert new_failures, (
        f"carve-out {case!r} left the excess rule skippable and every "
        "reviewer-reading test still passes"
    )
