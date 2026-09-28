"""Build and closing review run `sync-trunk` before any reviewer is dispatched
(plan W2-01; intent Acceptance 1 and 5).

Acceptance 1 is shown end to end on real repositories: `sync-trunk` merges
the fetched trunk tip, and the functional-content digest the attestation
binds moves with that merge. Acceptance 5 keeps the no-rerun absences.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from loom_checker.digest import functional_content_digest
from prose_pin import split_sentences


ROOT = Path(__file__).resolve().parents[2]
CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "loom_checker.py"
REVIEW = (ROOT / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8")
NO_PUBLICATION_PATHS = {"publication_only_paths": []}


def _flat(text: str) -> str:
    return " ".join(text.split())


def _section(text: str, heading: str) -> str:
    return _flat(text.split(heading, 1)[1].split("\n## ", 1)[0])


DEPTH = _section(REVIEW, "## 2. Compute review depth")
REVIEW_WORDS = _flat(REVIEW)


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
    # Committing a publication-only path after the sync leaves the bound digest unchanged.
    publication = {"publication_only_paths": ["report.txt"]}
    report_head = _commit(change, "report.txt", "report\n")
    assert functional_content_digest(change, report_head, "change", publication) == (
        functional_content_digest(change, after, "change", publication)
    )


def test_sync_after_finalize_invalidates_attestation(tmp_path: Path) -> None:
    change, finalized_head = _behind_branch(tmp_path)
    bound = _digest(change, finalized_head)
    assert _sync(change).returncode == 0
    assert _digest(change, _git(change, "rev-parse", "HEAD")) != bound
    # Hence no sync step is placed after finalize in closing review.
    finalize = _flat(REVIEW.split("## 5. Finalize", 1)[1])
    assert "sync-trunk" not in finalize


# --- Acceptance 5 --------------------------------------------------------


def test_no_op_sync_dispatches_without_rerun() -> None:
    # Every §2 sentence naming the checker's `up to date` output, not one
    # sentence located by its wording.
    for current in (s for s in split_sentences(DEPTH) if "`up to date`" in s):
        for rerun in ("package suite", "adversarial", "Build", "re-run"):
            assert rerun not in current, current
    # Re-sync in later rounds is out of scope: the sync names Round 1 only.
    assert REVIEW_WORDS.count("sync-trunk") == 1
