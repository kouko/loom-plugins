"""Change-scoped probe: this change leaves the checker's finalize, attestation
and push code untouched.

The constraint belongs to this change only, so it lives here and not in the
permanent package suite: a later change may edit these files freely. The
probe compares `git merge-base HEAD origin/main` against HEAD and skips only
when origin/main is unavailable.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-mechanical-checks-before-review/evidence/probes/test_checker_code_untouched.py -q
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
GUARDED = (
    "loom-code/scripts/loom_checker/command_handlers/finalize.py",
    "loom-code/scripts/loom_checker/attestation.py",
    "loom-code/scripts/loom_checker/command_handlers/push.py",
)


def _git(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(REPO), *args], capture_output=True, text=True
    )


def test_guardedpaths_currenttree_exist() -> None:
    """Each guarded path is a file, so an empty diff means untouched, not renamed."""
    for path in GUARDED:
        assert (REPO / path).is_file(), path


def test_checkercode_sincemergebase_unchanged() -> None:
    """HEAD carries no diff to finalize, attestation or push code since origin/main."""
    if _git("rev-parse", "--verify", "--quiet", "origin/main^{commit}").returncode != 0:
        pytest.skip("origin/main is unavailable")
    base = _git("merge-base", "HEAD", "origin/main")
    assert base.returncode == 0, base.stderr
    diff = _git("diff", "--name-only", base.stdout.strip(), "HEAD", "--", *GUARDED)
    assert diff.returncode == 0, diff.stderr
    assert diff.stdout.strip() == "", diff.stdout
