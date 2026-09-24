"""Adversarial probe: the gate-count pin does not depend on where `origin/main` points.
concern: hidden-state test — a pin that compares against the moving `origin/main` ref turns
red on a stale or fork remote without any change to the tree, and is vacuous on trunk.

`test_parallel_acceptance_review_text.py::test_one_fix_list_report_shape_gates_and_rules_kept`
counts `<!-- gate` markers in closing-review SKILL.md and compares them with
`git show origin/main:...`. That ref is local state: a contributor whose `origin` is a fork
with an older main, or who has not fetched, gets a different answer for the same commit.
After the merge the ref points at the change itself, so the comparison pins nothing.

This probe clones the repository into a temporary directory, checks out the current
commit, and runs that test twice: once with `origin/main` at the checked-out commit
(sanity), once with `origin/main` at `b568ba1a`, an earlier trunk commit whose
closing-review SKILL.md has three gates. The tree is identical in both runs, so both must
pass. It exercises committed content only. Run from the repo root:

    python3 -m pytest docs/loom/2026-09-24-parallel-acceptance-testing-and-review/evidence/probes/test_gate_count_stale_trunk_ref.py -q
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
STALE_TRUNK = "b568ba1a"
TEST = ("loom-code/scripts/test_parallel_acceptance_review_text.py::"
        "test_one_fix_list_report_shape_gates_and_rules_kept")


def _git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], capture_output=True, text=True,
                          check=True).stdout.strip()


def _run(clone: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", TEST],
                          cwd=clone, capture_output=True, text=True)


def test_gatecountpin_staletrunkref_passes(tmp_path: Path) -> None:
    """The same commit passes whether `origin/main` is current or an older trunk commit."""
    head = _git(REPO, "rev-parse", "HEAD")
    clone = tmp_path / "clone"
    subprocess.run(["git", "clone", "--quiet", "--shared", "--no-checkout", str(REPO), str(clone)],
                   check=True)
    _git(clone, "checkout", "--quiet", "--detach", head)
    _git(clone, "update-ref", "refs/remotes/origin/main", head)
    current = _run(clone)
    assert current.returncode == 0, "sanity run failed:\n" + current.stdout
    _git(clone, "update-ref", "refs/remotes/origin/main", _git(REPO, "rev-parse", STALE_TRUNK))
    stale = _run(clone)
    assert stale.returncode == 0, (
        "the same commit failed only because origin/main points elsewhere:\n" + stale.stdout)
