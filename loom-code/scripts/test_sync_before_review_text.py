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
from prose_pin import has_negation, split_sentences


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
    # Committing a publication-only path after the sync leaves the bound digest unchanged.
    publication = {"publication_only_paths": ["report.txt"]}
    report_head = _commit(change, "report.txt", "report\n")
    assert functional_content_digest(change, report_head, "change", publication) == (
        functional_content_digest(change, after, "change", publication)
    )
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


REVIEW_SYNC_SENTENCES = (
    f"Before dispatching reviewers in Round 1, run {COMMAND} from the change worktree.",
    "When it reports `up to date`, continue.",
    "When it reports `content changed`, dispatch no reviewer and return to Build §3 to "
    "re-run the complete package suite and the existing adversarial programs, then start "
    "Round 1 again.",
    "When it prints `WARN review.sync`, state the warning in the round report and continue.",
    "When it prints `BLOCK review.sync`, dispatch no reviewer and return the change to Build.",
    "Any other result, including exit 2, dispatches no reviewer and reports the printed message.",
    "Run it before the blind run (§3), so the blind run exercises the synced content.",
)
BUILD_SYNC_SENTENCES = (
    f"From the change worktree, run {COMMAND}, so the adversary, the suite and the "
    "programs all see the fetched trunk tip.",
    "On `BLOCK review.sync`, fix the cause inside Build, where a conflict is resolved as "
    "implementation work in a new build round, never by the command.",
    "On `WARN review.sync`, continue unsynced.",
    "Any other result, including exit 2, does not continue and reports the printed message.",
)


def _pinned_run(text: str, first: str, count: int) -> tuple[str, ...]:
    """The `count` consecutive sentences starting at the one containing `first`."""
    sentences = split_sentences(text)
    start = next(i for i, s in enumerate(sentences) if first in s)
    return tuple(sentences[start:start + count])


def test_merged_sync_returns_to_build_checks_before_dispatch() -> None:
    # Whole governing sentences, byte for byte: an added condition ("or on a
    # small merge"), a dropped round-report duty or an in-place conflict
    # resolution each changes a pinned sentence.
    assert _pinned_run(DEPTH, COMMAND, 7) == REVIEW_SYNC_SENTENCES
    run, current, changed, warned, blocked, other, order = REVIEW_SYNC_SENTENCES
    for affirmative in (run, current, warned, order):
        assert not has_negation(affirmative), affirmative
    assert DEPTH.count("`up to date`") == 1 and DEPTH.count("`content changed`") == 1
    assert DEPTH.count("`WARN review.sync`") == 1 and DEPTH.count("`BLOCK review.sync`") == 1
    assert DEPTH.index(other) < DEPTH.index("loom_checker.py reviewer-count")
    assert DEPTH.index(order) < DEPTH.index("When a blind run is needed")
    # Build syncs first among its mechanical checks: before the adversary is
    # dispatched and before the suite, so merged content is checked there.
    assert _pinned_run(VERIFY, COMMAND, 4) == BUILD_SYNC_SENTENCES
    step = BUILD_SYNC_SENTENCES[0]
    assert not has_negation(step), step
    adversary = VERIFY.index("Dispatch the `loom-code:adversary` agent fresh-context")
    assert VERIFY.index(step) < adversary < VERIFY.index("Run the repository's complete package suite")
    assert VERIFY.count("sync-trunk") == 1
    assert "`sync-trunk` result" in HANDOFF
    assert "warning" in _sentence(HANDOFF, "`sync-trunk` result")


def test_no_op_sync_dispatches_without_rerun() -> None:
    current = _sentence(DEPTH, "reports `up to date`")
    assert "continue" in current, current
    for rerun in ("package suite", "adversarial", "Build", "re-run"):
        assert rerun not in current, current
    # Re-sync in later rounds is out of scope: the sync names Round 1 only.
    assert REVIEW_WORDS.count("sync-trunk") == 1
