"""Adversarial probe: does test_sync_before_review_text.py catch weakened sync prose?

Each mutant copies `loom-code/` and `loom-design/skills` into a temporary
sandbox, weakens one sentence the change added to a station (never the repo
files), and runs the guard test file there. A mutant the guard lets through
is a SURVIVOR: the station text can be weakened with every test still green.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-sync-main-before-review/evidence/probes/test_sync_text_pins_mutation.py -q

Each mutant test asserts the mutant is killed; a failing mutant test is a
finding. test_syncpins_unmutated_green proves a kill comes from the mutation,
not from a broken sandbox.
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
GUARD = "test_sync_before_review_text.py"
IGNORE = shutil.ignore_patterns("__pycache__", ".pytest_cache")


def _sandbox(dest: Path) -> Path:
    shutil.copytree(REPO / "loom-code", dest / "loom-code", ignore=IGNORE)
    shutil.copytree(REPO / "loom-design/skills", dest / "loom-design/skills", ignore=IGNORE)
    return dest


def _mutate(root: Path, path: str, old: str, new: str) -> None:
    target = root / path
    text = target.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"mutation anchor not unique in {path}: {old!r}"
    target.write_text(text.replace(old, new), encoding="utf-8")


def _guard(root: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", GUARD],
        cwd=root / "loom-code/scripts", capture_output=True, text=True,
    )


MUTANTS = [
    pytest.param(
        BUILD,
        "so the adversary,\n   the suite and the programs all see the fetched trunk tip.",
        "once the adversary\n   returns, so the suite and the programs see the fetched trunk tip.",
        id="build-sync-moved-after-adversary-dispatch",
    ),
    pytest.param(
        REVIEW,
        "When it reports `up to date`, continue.",
        "When it reports `up to date`, or `content changed` on a small merge, continue.",
        id="review-small-content-change-dispatches-reviewers-unchecked",
    ),
    pytest.param(
        REVIEW,
        "state the warning in the\nround report and continue.",
        "continue, and leave the warning out of the\nround report so reviewers stay focused.",
        id="review-warning-dropped-from-round-report",
    ),
    pytest.param(
        REVIEW,
        "When it prints `BLOCK review.sync`, dispatch no",
        "When it prints `BLOCK review.sync`, resolve a one-line conflict in place, then dispatch no",
        id="review-block-conflict-resolved-in-place",
    ),
]


def test_syncpins_unmutated_green(tmp_path: Path) -> None:
    """The unmodified sandbox passes the guard, so every kill below is the mutation's."""
    result = _guard(_sandbox(tmp_path))
    assert result.returncode == 0, result.stdout + result.stderr


@pytest.mark.parametrize(("path", "old", "new"), MUTANTS)
def test_syncpins_mutated_killed(tmp_path: Path, path: str, old: str, new: str) -> None:
    """A weakened sync sentence must turn the guard red."""
    root = _sandbox(tmp_path)
    _mutate(root, path, old, new)
    result = _guard(root)
    assert result.returncode != 0, f"SURVIVOR: guard stayed green after mutating {path}"
