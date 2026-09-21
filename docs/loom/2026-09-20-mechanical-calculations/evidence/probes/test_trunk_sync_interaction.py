"""Adversarial probe: narrow-delta auto-skip across a trunk sync.

`sync-trunk` merges the remote trunk tip into the change branch, moving the
merge base. The attack surface: after the sync the committed delta must be
recomputed against the NEW base — trunk content merged in must not count as
this change's delta, a selection bound before the sync must lapse (the merge
base it recorded no longer applies), and a fast-forward that leaves the
branch with no commits of its own must keep the full ritual (empty delta).

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-20-mechanical-calculations/evidence/probes/test_trunk_sync_interaction.py -q

Every probe is an attempt to make the change fail. Attempts the change
survives PASS; attempts that expose a defect FAIL on purpose and must not be
weakened.
"""
from __future__ import annotations

import hashlib
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker import selection
from loom_checker.reviewers import committed_branch_paths, required_reviewer_count
from loom_checker.selection import _auto_skip

CHANGE = "2026-09-20-mechanical-calculations"
AUTO_SKIP = {"spec", "plan", "blind-run"}
NARROW_FILES = ("docs/guide.md", "test_feature.py")
TRUNK_PRODUCTION = ("src.py", "newmod.py")
HOST_ENV = ("CLAUDE_CODE_SESSION_ID", "CLAUDE_CODE_SESSION_ATTENDED", "CLAUDE_CODE_ENTRYPOINT")


@pytest.fixture(autouse=True)
def no_host_session(monkeypatch):
    for name in HOST_ENV:
        monkeypatch.delenv(name, raising=False)


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def git_ok(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def base_repo(tmp_path: Path, narrow: bool) -> Path:
    """A repo on `main` with the remote-tracking ref origin/main already at
    the base commit, so `branch_base` resolves through origin/main both before
    and after the simulated fetch moves it."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "base.py").write_text("VALUE = 1\n", encoding="utf-8")
    git_ok(repo, "add", "base.py")
    git_ok(repo, "commit", "-q", "-m", "initial")
    git_ok(repo, "update-ref", "refs/remotes/origin/main", git(repo, "rev-parse", "HEAD"))
    git_ok(repo, "switch", "-q", "-c", "feature")
    if narrow:
        (repo / "docs").mkdir()
        (repo / "docs" / "guide.md").write_text("guide\n", encoding="utf-8")
        (repo / "test_feature.py").write_text("pass\n", encoding="utf-8")
        git_ok(repo, "add", *NARROW_FILES)
        git_ok(repo, "commit", "-q", "-m", "narrow files")
    return repo


def advance_trunk(repo: Path) -> None:
    """The trunk gains production code (a modified file and a new module),
    then the simulated fetch moves origin/main to the new tip."""
    git_ok(repo, "switch", "-q", "main")
    (repo / "src.py").write_text("def api():\n    return 2\n", encoding="utf-8")
    (repo / "newmod.py").write_text("def lib():\n    return 3\n", encoding="utf-8")
    git_ok(repo, "add", *TRUNK_PRODUCTION)
    git_ok(repo, "commit", "-q", "-m", "trunk production code")
    tip = git(repo, "rev-parse", "HEAD")
    git_ok(repo, "switch", "-q", "feature")
    git_ok(repo, "update-ref", "refs/remotes/origin/main", tip)


def record_bound(repo: Path, skip: list[str]) -> None:
    """An in-scope proposal plus a valid confirmation, recorded BEFORE the
    sync moves the merge base."""
    names = [s["name"] for s in selection.step_vocabulary()]
    run = [name for name in names if name not in skip]
    branch, merge_base = selection.current_scope(repo)
    code = selection.selection_code(CHANGE, run, skip)
    proposal_id = uuid.uuid4().hex
    selection.append_event(repo, CHANGE, {
        "event": "proposal", "id": proposal_id, "code": code, "origin": "user",
        "run": run, "skip": skip, "branch": branch, "merge_base": merge_base,
        "session_id": None, "created_at": selection.now(),
    })
    prompt = f"/loom-code:expert-mode OK {code}"
    selection.append_event(repo, CHANGE, {
        "event": "confirmation", "proposal_id": proposal_id, "code": code,
        "source": "user-typed", "session_id": None, "prompt_ref": "probe",
        "prompt_text": prompt,
        "prompt_sha256": hashlib.sha256(prompt.encode("utf-8")).hexdigest(),
        "branch": branch, "merge_base": merge_base, "at": selection.now(),
    })


def names() -> list[str]:
    return [s["name"] for s in selection.step_vocabulary()]


def test_trunksync_mergein_trunkexcluded(tmp_path: Path) -> None:
    """A clean sync merges the advanced trunk into the branch: the trunk's
    production code must NOT count as this change's delta afterwards — the
    delta is recomputed against the new base, so the narrow auto-skip still
    applies and the reviewer floor stays 1."""
    repo = base_repo(tmp_path, narrow=True)
    assert set(_auto_skip(repo, CHANGE, names())) == AUTO_SKIP
    advance_trunk(repo)
    git_ok(repo, "merge", "--ff", "--no-edit", "-m", "Merge origin/main into feature",
           git(repo, "rev-parse", "refs/remotes/origin/main"))
    paths = committed_branch_paths(repo, CHANGE)
    assert paths == set(NARROW_FILES), (
        f"trunk content leaked into the branch delta: {sorted(paths)}")
    assert paths.isdisjoint(TRUNK_PRODUCTION), paths
    assert set(_auto_skip(repo, CHANGE, names())) == AUTO_SKIP, (
        "auto-skip must survive a clean trunk sync of a narrow delta")
    assert required_reviewer_count(repo, CHANGE) == 1


def test_trunksync_lapsed_recomputes(tmp_path: Path) -> None:
    """A selection bound BEFORE the sync lapses once the merge base moves:
    no user selection is bound afterwards, and the still-narrow delta falls
    back to the mechanical auto-skip."""
    repo = base_repo(tmp_path, narrow=True)
    record_bound(repo, skip=["adversarial"])
    state = selection.effective_selection(repo, CHANGE)
    assert state["bound"] is True and state["skip"] == ["adversarial"], state
    advance_trunk(repo)
    git_ok(repo, "merge", "--ff", "--no-edit", "-m", "Merge origin/main into feature",
           git(repo, "rev-parse", "refs/remotes/origin/main"))
    state = selection.effective_selection(repo, CHANGE)
    assert state["bound"] is False, (
        f"a pre-sync selection survived the merge-base move: {state}")
    assert set(state["skip"]) == AUTO_SKIP, state


def test_trunksync_fastforward_empty_failclosed(tmp_path: Path) -> None:
    """A branch with no commits of its own fast-forwards to the trunk tip:
    the committed delta is empty afterwards and acceptance 3 keeps the full
    ritual — no automatic skips, reviewer floor 2."""
    repo = base_repo(tmp_path, narrow=False)
    advance_trunk(repo)
    git_ok(repo, "merge", "--ff", "--no-edit", "-m", "Merge origin/main into feature",
           git(repo, "rev-parse", "refs/remotes/origin/main"))
    assert committed_branch_paths(repo, CHANGE) == set()
    assert _auto_skip(repo, CHANGE, names()) == [], (
        "an empty post-sync delta must not auto-skip anything")
    assert required_reviewer_count(repo, CHANGE) == 2


def test_trunksync_conflictproduction_failclosed(tmp_path: Path) -> None:
    """When the branch's own delta touches production code, a sync whose
    conflict resolution keeps the feature's production change must keep the
    full ritual: the production path is still in the recomputed delta."""
    repo = base_repo(tmp_path, narrow=True)
    (repo / "src.py").write_text("def api():\n    return 9\n", encoding="utf-8")
    git_ok(repo, "add", "src.py")
    git_ok(repo, "commit", "-q", "-m", "feature touches production code")
    advance_trunk(repo)
    git_ok(repo, "merge", "--no-edit", "-m", "Merge origin/main into feature",
           git(repo, "rev-parse", "refs/remotes/origin/main"),
           "-X", "ours")
    paths = committed_branch_paths(repo, CHANGE)
    assert "src.py" in paths, (
        f"the production path vanished from the post-sync delta: {sorted(paths)}")
    assert _auto_skip(repo, CHANGE, names()) == [], (
        "a production path in the delta must keep the full ritual after a sync")
    assert required_reviewer_count(repo, CHANGE) == 2


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
