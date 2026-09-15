"""Build and closing review run `sync-trunk` before any reviewer is dispatched
(plan W2-01; intent Acceptance 1 and 5).

Acceptance 1 is shown end to end on real repositories: `sync-trunk` merges
the fetched trunk tip, the functional-content digest the attestation binds
moves with that merge, and both stations order the sync before reviewer
dispatch and finalize. Acceptance 5 is pinned in the station text.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from loom_checker.digest import functional_content_digest
from prose_pin import split_sentences


ROOT = Path(__file__).resolve().parents[2]
CHECKER = Path(__file__).with_name("loom_checker.py")
BUILD = (ROOT / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
REVIEW = (ROOT / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8")
COMMAND = "`python3 <loom-code>/scripts/loom_checker.py sync-trunk`"
NO_PUBLICATION_PATHS = {"publication_only_paths": []}


def _flat(text: str) -> str:
    return " ".join(text.split())


def _section(text: str, heading: str) -> str:
    return _flat(text.split(heading, 1)[1].split("\n## ", 1)[0])


VERIFY = _section(BUILD, "## 3. Verify integration")
HANDOFF = _section(BUILD, "## 4. Hand off to Review")
DEPTH = _section(REVIEW, "## 2. Compute review depth")
REVIEW_WORDS = _flat(REVIEW)


def _sentence(text: str, fragment: str) -> str:
    return next(s for s in split_sentences(text) if fragment in s)


def _git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def _commit(repo: Path, name: str, text: str) -> str:
    (repo / name).write_text(text, encoding="utf-8")
    _git(repo, "add", name)
    _git(repo, "commit", "-q", "-m", f"change {name}")
    return _git(repo, "rev-parse", "HEAD")


def _behind_branch(tmp_path: Path) -> tuple[Path, str]:
    """A change branch that lacks a commit a teammate landed on origin/main."""
    origin = tmp_path / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", "-b", "main", str(origin)], check=True)
    clones = {}
    for name in ("seed", "change", "teammate"):
        clone = tmp_path / name
        subprocess.run(["git", "clone", "-q", str(origin), str(clone)], check=True, capture_output=True)
        _git(clone, "config", "user.email", "test@example.com")
        _git(clone, "config", "user.name", "Test")
        clones[name] = clone
        if name == "seed":
            _git(clone, "switch", "-q", "-c", "main")
            _commit(clone, "base.txt", "base\n")
            _git(clone, "push", "-q", "origin", "main")
    change, teammate = clones["change"], clones["teammate"]
    _git(change, "switch", "-q", "-c", "feature")
    head = _commit(change, "feature.txt", "feature\n")
    _commit(teammate, "main.txt", "landed first\n")
    _git(teammate, "push", "-q", "origin", "main")
    return change, head


def _sync(repo: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "sync-trunk"], capture_output=True, text=True, cwd=str(repo)
    )


def _digest(repo: Path, sha: str) -> str:
    digest = functional_content_digest(repo, sha, "change", NO_PUBLICATION_PATHS)
    assert digest
    return digest


# --- Acceptance 1 --------------------------------------------------------


def test_behind_branch_synced_then_attestation_validates_at_head(tmp_path: Path) -> None:
    change, before = _behind_branch(tmp_path)
    result = _sync(change)
    assert result.returncode == 0, result.stderr
    assert "sync-trunk: content changed" in result.stdout
    after = _git(change, "rev-parse", "HEAD")
    tip = _git(change, "rev-parse", "refs/remotes/origin/main")
    subprocess.run(["git", "-C", str(change), "merge-base", "--is-ancestor", tip, after], check=True)
    # The digest a reviewer-then-finalize run binds is computed at the synced
    # HEAD, so it is the one that validates there.
    assert _digest(change, after) != _digest(change, before)
    assert _digest(change, after) == _digest(change, _git(change, "rev-parse", "HEAD"))
    # Both stations sync before any reviewer is dispatched or finalize runs.
    assert COMMAND in VERIFY
    assert VERIFY.index(COMMAND) < VERIFY.index("Run the repository's complete package suite")
    assert COMMAND in DEPTH
    assert DEPTH.index(COMMAND) < DEPTH.index("loom_checker.py reviewer-count")
    assert REVIEW_WORDS.index(COMMAND) < REVIEW_WORDS.index("## 5. Finalize")


def test_sync_after_finalize_invalidates_attestation(tmp_path: Path) -> None:
    change, finalized_head = _behind_branch(tmp_path)
    bound = _digest(change, finalized_head)
    assert _sync(change).returncode == 0
    assert _digest(change, _git(change, "rev-parse", "HEAD")) != bound
    # Hence no sync step is placed after finalize in closing review.
    finalize = _flat(REVIEW.split("## 5. Finalize", 1)[1])
    assert "sync-trunk" not in finalize


# --- Acceptance 5 --------------------------------------------------------


def test_merged_sync_returns_to_build_checks_before_dispatch() -> None:
    run = _sentence(DEPTH, COMMAND)
    assert "Round 1" in run, run
    changed = _sentence(DEPTH, "reports `content changed`")
    for element in (
        "dispatch no reviewer", "Build §3", "complete package suite",
        "existing adversarial programs", "Round 1 again",
    ):
        assert element in changed, changed
    blocked = _sentence(DEPTH, "`BLOCK review.sync`")
    assert "dispatch no reviewer" in blocked and "Build" in blocked, blocked
    warned = _sentence(DEPTH, "`WARN review.sync`")
    assert "round report" in warned and "continue" in warned, warned
    assert DEPTH.index(changed) < DEPTH.index("loom_checker.py reviewer-count")
    # Build syncs before its suite, so merged content is checked there.
    step = _sentence(VERIFY, COMMAND)
    assert "change worktree" in step, step
    conflict = _sentence(VERIFY, "`BLOCK review.sync`")
    assert "inside Build" in conflict and "new build round" in conflict, conflict
    assert "never by the command" in conflict, conflict
    assert "`WARN review.sync`" in VERIFY
    assert "`sync-trunk` result" in HANDOFF
    assert "warning" in _sentence(HANDOFF, "`sync-trunk` result")


def test_no_op_sync_dispatches_without_rerun() -> None:
    current = _sentence(DEPTH, "reports `up to date`")
    assert "continue" in current, current
    for rerun in ("package suite", "adversarial", "Build", "re-run"):
        assert rerun not in current, current
    # Re-sync in later rounds is out of scope: the sync names Round 1 only.
    assert REVIEW_WORDS.count("sync-trunk") == 1
