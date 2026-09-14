"""Adversarial probe: `land --accepted-by` cleanup against worktree states whose
uncommitted work is invisible to plain `git status`, and against neighbours
with similar names. Reuses the real-git Layout from test_land_cleanup.py.

Each case asserts the SAFE behaviour: the user's bytes survive.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from test_land_cleanup import Layout, git, ref_exists, run_land  # noqa: E402


def test_cleanup_skipWorktreeEdit_preservesEdit(tmp_path: Path, monkeypatch) -> None:
    """A tracked file edited and hidden with --skip-worktree is uncommitted work (Acceptance #7)."""
    layout = Layout(tmp_path)
    (layout.wt / "feature.txt").write_text("local secret edit\n", encoding="utf-8")
    git(layout.wt, "update-index", "--skip-worktree", "feature.txt")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert (layout.wt / "feature.txt").is_file(), (rc, out, err)
    assert (layout.wt / "feature.txt").read_text(encoding="utf-8") == "local secret edit\n"
    assert rc == 1 and "BLOCK land.cleanup" in err


def test_cleanup_assumeUnchangedEdit_preservesEdit(tmp_path: Path, monkeypatch) -> None:
    """A tracked file edited under --assume-unchanged is uncommitted work (Acceptance #7)."""
    layout = Layout(tmp_path)
    (layout.wt / "feature.txt").write_text("local edit\n", encoding="utf-8")
    git(layout.wt, "update-index", "--assume-unchanged", "feature.txt")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert (layout.wt / "feature.txt").is_file(), (rc, out, err)
    assert rc == 1 and "BLOCK land.cleanup" in err


def test_cleanup_untrackedHiddenByConfig_refuses(tmp_path: Path, monkeypatch) -> None:
    """status.showUntrackedFiles=no must not hide an untracked file from the guard."""
    layout = Layout(tmp_path)
    git(layout.repo, "config", "status.showUntrackedFiles", "no")
    (layout.wt / "notes.txt").write_text("draft\n", encoding="utf-8")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert (layout.wt / "notes.txt").is_file(), (rc, out, err)
    assert rc == 1 and "BLOCK land.cleanup" in err


def test_cleanup_envInsideCacheDir_preservesEnv(tmp_path: Path, monkeypatch) -> None:
    """A non-regenerable .env nested inside an ignored __pycache__/ directory survives."""
    layout = Layout(tmp_path)
    (layout.wt / "__pycache__").mkdir()
    (layout.wt / "__pycache__" / ".env").write_text("TOKEN=secret\n", encoding="utf-8")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert (layout.wt / "__pycache__" / ".env").is_file(), (rc, out, err)


def test_cleanup_similarNeighbours_untouched(tmp_path: Path, monkeypatch) -> None:
    """Prefix, suffix, dot and detached neighbours with dirty files are untouched (Acceptance #8)."""
    layout = Layout(tmp_path)
    neighbours = {
        "feat/x-2": layout.root / "wt-x-2",
        "feat/x.y": layout.root / "wt-x.y",
        "feat/xx": layout.root / "wt-x-old",
        "x": layout.root / "wt-x" "x",
    }
    for branch, path in neighbours.items():
        layout.add_worktree(path, branch)
        (path / "draft.txt").write_text(branch + "\n", encoding="utf-8")
    detached = layout.root / "wt-detached"
    git(layout.repo, "worktree", "add", "-q", "--detach", str(detached), "feat/x")
    (detached / "draft.txt").write_text("detached\n", encoding="utf-8")

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 0, err
    assert not layout.wt.exists()
    for branch, path in neighbours.items():
        assert ref_exists(layout.repo, f"refs/heads/{branch}"), branch
        assert (path / "draft.txt").is_file(), branch
    assert (detached / "draft.txt").is_file()
    [remove] = calls.git_calls("worktree", "remove")
    assert remove[-1] == str(layout.wt)


def test_cleanup_lockedWorktree_keepsBranches(tmp_path: Path, monkeypatch) -> None:
    """A locked worktree is not force-removed and both branch refs stay."""
    layout = Layout(tmp_path)
    git(layout.repo, "worktree", "lock", str(layout.wt))

    rc, out, err, calls = run_land(monkeypatch, layout)

    assert rc == 1
    assert layout.wt.is_dir()
    assert ref_exists(layout.repo, "refs/heads/feat/x")
    assert layout.remote_has("feat/x")
