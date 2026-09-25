# concern: the adversarial auto-skip is recomputed from the branch delta at
# each call site instead of being recorded, so the same commit and the same
# attestation get opposite answers from finalize-review and from the
# attestation validator in a checkout that cannot compute the delta.
"""Attack the shared predicate behind the two call sites.

`finalize-review` (`command_handlers/finalize.py`) and `validate_attestation`
(`attestation.py`) both merge `auto_skipped_steps(...)` into `skip` and then
ask `missing_adversarial_execution(...)`. The merged message made the two
agree on *wording*; this asks whether they agree on the *answer*.

`auto_skipped_steps` fails closed through `committed_branch_paths`, which
returns an empty set when `branch_base` cannot resolve a trunk. The typed
selection a user confirms is recorded in the attestation and travels with it;
this skip is not recorded anywhere, so it has to be recomputed against
whatever git state the validator happens to run in. A fresh checkout that
holds only the branch is the ordinary CI case.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from loom_checker.probes import missing_adversarial_execution  # noqa: E402
from loom_checker.reviewers import auto_skipped_steps  # noqa: E402

CHANGE_ID = "2026-09-23-adversarial-probes-earn-their-place"
BRANCH = f"feat/{CHANGE_ID}"


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=repo, check=True, capture_output=True, text=True
    ).stdout.strip()


def _narrow_branch() -> tuple[Path, str]:
    """A repo on a branch whose whole delta is one documentation file."""
    repo = Path(tempfile.mkdtemp())
    _git(repo, "init", "-q", "-b", "main", ".")
    _git(repo, "config", "user.email", "adversary@example.invalid")
    _git(repo, "config", "user.name", "adversary")
    (repo / "README.md").write_text("# repo\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "trunk")
    _git(repo, "checkout", "-q", "-b", BRANCH)
    (repo / "README.md").write_text("# repo, reworded\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-qm", "delta")
    return repo, _git(repo, "rev-parse", "HEAD")


def _branch_only_checkout(origin: Path, head: str) -> Path:
    """The same commit, cloned the way a build fetches one branch."""
    clone = Path(tempfile.mkdtemp()) / "checkout"
    subprocess.run(
        ["git", "clone", "-q", "--single-branch", "--branch", BRANCH,
         "--no-tags", str(origin), str(clone)],
        check=True, capture_output=True,
    )
    subprocess.run(["git", "remote", "remove", "origin"], cwd=clone,
                   check=True, capture_output=True)
    assert _git(clone, "rev-parse", "HEAD") == head
    return clone


def test_auto_skip_same_commit_in_two_checkouts_gives_one_answer() -> None:
    """The step list a change skips is a property of the change, not of the
    clone the question is asked in."""
    origin, head = _narrow_branch()
    clone = _branch_only_checkout(origin, head)
    assert auto_skipped_steps(clone, CHANGE_ID, head) == auto_skipped_steps(
        origin, CHANGE_ID, head
    )


def test_missing_adversarial_execution_same_attestation_is_not_refused_in_ci() -> None:
    """An attestation generated where the step was waived, validated where
    the delta cannot be read. Finalize wrote no adversarial execution because
    it had waived the step; the validator must not then demand one."""
    origin, head = _narrow_branch()
    clone = _branch_only_checkout(origin, head)
    at_finalize = missing_adversarial_execution(0, auto_skipped_steps(origin, CHANGE_ID, head))
    at_validation = missing_adversarial_execution(0, auto_skipped_steps(clone, CHANGE_ID, head))
    assert at_finalize is None, "precondition: the step is waived where the attestation is made"
    assert at_validation == at_finalize


if __name__ == "__main__":
    raise SystemExit(pytest.main([__file__, "-q"]))
