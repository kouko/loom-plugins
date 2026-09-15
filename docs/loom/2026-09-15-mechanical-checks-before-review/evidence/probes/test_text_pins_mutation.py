"""Adversarial probe: do the branch's text-contract tests catch weakened prose?

Each mutant copies the station, agent and test files into a temporary
sandbox, weakens one sentence the change added (never the repo files), and
runs the test file that guards it. A mutant the guard lets through is a
SURVIVOR: the prose can be weakened with every test still green.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-mechanical-checks-before-review/evidence/probes/test_text_pins_mutation.py -q

RECORDED_KILLS are attacks the guards already catch; they pass. MUTANTS
expose a gap: each test asserts its mutant is killed, so it FAILS until the
guard is strengthened. test_harness_unmutated_green proves a kill comes from
the mutation, not from a broken sandbox.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
BUILD = "loom-code/skills/build/SKILL.md"
REVIEW = "loom-code/skills/closing-review/SKILL.md"
REVIEWER = "loom-code/agents/reviewer.md"
ADVERSARY = "loom-code/agents/adversary.md"
T_BUILD = "test_build_mechanical_checks.py"
T_REVIEWER = "test_reviewer_mechanical_evidence.py"
T_CONVERGE = "test_review_convergence_contract.py"


def _sandbox(dest: Path) -> Path:
    for tree in ("loom-code/skills", "loom-code/agents", "loom-design/skills"):
        shutil.copytree(REPO / tree, dest / tree)
    scripts = dest / "loom-code/scripts"
    scripts.mkdir(parents=True)
    for source in (REPO / "loom-code/scripts").glob("*.py"):
        shutil.copy2(source, scripts / source.name)
    return dest


def _mutate(root: Path, path: str, old: str, new: str) -> None:
    target = root / path
    text = target.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"mutation anchor not unique in {path}: {old!r}"
    target.write_text(text.replace(old, new), encoding="utf-8")


def _guards_green(root: Path, test_files: tuple[str, ...]) -> bool:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", *test_files],
        cwd=root / "loom-code/scripts",
        capture_output=True,
        text=True,
    )
    return result.returncode == 0


MUTANTS = [
    # --- weakenings the guards let through today -------------------------
    pytest.param(
        BUILD,
        "every adversarial program pass.\n",
        "every adversarial program pass.\nWhen the diff is small, hand off to Review "
        "while the suite is still running.\n",
        (T_BUILD,),
        id="build-escape-sentence-hands-off-before-suite-finishes",
    ),
    pytest.param(
        BUILD,
        "after the fix: run the complete package suite",
        "after the fix: optionally run the complete package suite",
        (T_BUILD,),
        id="build-fix-loop-suite-made-optional",
    ),
    pytest.param(
        REVIEWER,
        "In every round, you never run",
        "In Round 1, you never run",
        (T_REVIEWER, T_CONVERGE),
        id="reviewer-suite-ban-scoped-to-round-1",
    ),
    pytest.param(
        REVIEWER,
        "never actually executes, is a `tests`",
        "never actually executes, is not a `tests`",
        (T_REVIEWER, T_CONVERGE),
        id="reviewer-skipped-changed-test-no-longer-a-finding",
    ),
    pytest.param(
        REVIEW,
        "Build and dispatch no reviewer. Reviewers read",
        "Build and dispatch no reviewer. Under time pressure, dispatch reviewers "
        "while Build's checks still run. Reviewers read",
        (T_CONVERGE, T_REVIEWER),
        id="review-escape-sentence-dispatches-reviewers-during-build-checks",
    ),
    pytest.param(
        REVIEW,
        "must pass the next review round (§4) before",
        "may skip the next review round (§4) before",
        (T_CONVERGE, T_REVIEWER),
        id="review-finalize-failure-may-skip-next-round",
    ),
]

RECORDED_KILLS = [
    pytest.param(
        REVIEW,
        "Before dispatching reviewers in any round",
        "Before dispatching reviewers in the first round",
        (T_CONVERGE,),
        id="review-dispatch-gate-scoped-to-first-round",
    ),
    pytest.param(
        ADVERSARY,
        "by the build station",
        "by the review station",
        (T_BUILD,),
        id="adversary-description-back-to-review-station",
    ),
    pytest.param(
        REVIEW,
        "Earlier verdicts are never reused for the fixed content.",
        "",
        (T_CONVERGE,),
        id="review-verdict-reuse-ban-deleted",
    ),
]


def test_harness_unmutated_green(tmp_path: Path) -> None:
    """The unmutated sandbox passes every guard, so a kill means the mutation."""
    root = _sandbox(tmp_path)
    assert _guards_green(root, (T_BUILD, T_REVIEWER, T_CONVERGE))


@pytest.mark.parametrize("path,old,new,guards", RECORDED_KILLS)
def test_guards_recordedattack_killed(tmp_path: Path, path, old, new, guards) -> None:
    """Attacks the guards already catch; recorded so the catalogue is an eval."""
    root = _sandbox(tmp_path)
    _mutate(root, path, old, new)
    assert not _guards_green(root, guards), f"mutant survived: {path}"


@pytest.mark.parametrize("path,old,new,guards", MUTANTS)
def test_guards_weakenedprose_killed(tmp_path: Path, path, old, new, guards) -> None:
    """A weakened sentence of the change's prose must turn a guard red."""
    root = _sandbox(tmp_path)
    _mutate(root, path, old, new)
    assert not _guards_green(root, guards), (
        f"SURVIVOR: {path} weakened ({old!r} -> {new!r}) and {guards} stay green"
    )
