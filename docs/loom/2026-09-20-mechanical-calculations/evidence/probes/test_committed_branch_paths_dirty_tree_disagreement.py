"""Adversarial probe: committed_branch_paths excludes working-tree edits.

The function must return only committed paths between the branch and its base.
Working-tree edits (staged, unstaged, and untracked) must not appear in the
result, or the auto-skip and reviewer floor will disagree with what reviewers
and finalize-review actually see.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from loom_checker.reviewers import committed_branch_paths


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    """Create a repository with one committed feature-branch path."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "src.py")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "switch", "-q", "-c", "feature")
    (repo / "feature.txt").write_text("committed\n", encoding="utf-8")
    git(repo, "add", "feature.txt")
    git(repo, "commit", "-q", "-m", "add feature")
    return repo


def test_committedpaths_unstaged_excluded(tmp_path: Path) -> None:
    """Unstaged changes are absent from committed_branch_paths."""
    repo = make_repo(tmp_path)
    (repo / "src.py").write_text("VALUE = 999\n", encoding="utf-8")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths == {"feature.txt"}, f"Expected only feature.txt, got {paths}"


def test_committedpaths_staged_excluded(tmp_path: Path) -> None:
    """Staged changes are absent from committed_branch_paths."""
    repo = make_repo(tmp_path)
    (repo / "src.py").write_text("VALUE = 888\n", encoding="utf-8")
    git(repo, "add", "src.py")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths == {"feature.txt"}, f"Expected only feature.txt, got {paths}"


def test_committedpaths_untracked_excluded(tmp_path: Path) -> None:
    """Untracked changes are absent from committed_branch_paths."""
    repo = make_repo(tmp_path)
    (repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths == {"feature.txt"}, f"Expected only feature.txt, got {paths}"


def test_committedpaths_codexplumbing_excluded(tmp_path: Path) -> None:
    """Codex scaffold hook plumbing is absent from committed_branch_paths."""
    repo = make_repo(tmp_path)
    plumbing = repo / ".codex" / "hooks" / "loom-checker"
    plumbing.parent.mkdir(parents=True, exist_ok=True)
    plumbing.write_text("# scaffold hook\n", encoding="utf-8")
    git(repo, "add", ".codex/hooks/loom-checker")
    git(repo, "commit", "-q", "-m", "add plumbing")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert ".codex/hooks/loom-checker" not in paths
    assert paths == {"feature.txt"}, f"Expected only feature.txt, got {paths}"


def test_committedpaths_hostplumbing_excluded(tmp_path: Path) -> None:
    """Host plumbing paths are absent from committed_branch_paths."""
    repo = make_repo(tmp_path)
    plumbing_paths = [
        ".herdr/cache/state.bin",
        "node_modules/pkg/index.js",
        "__pycache__/mod.pyc",
        "package.lock",
        "events.jsonl",
    ]
    for relative in plumbing_paths:
        path = repo / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(relative, encoding="utf-8")
    git(repo, "add", "-f", *plumbing_paths)
    git(repo, "commit", "-q", "-m", "add host plumbing")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths.isdisjoint(plumbing_paths), (
        f"Host plumbing leaked into committed paths: {sorted(paths)}"
    )


def test_committedpaths_empty_returnsempty(tmp_path: Path) -> None:
    """A branch with no commits over its base returns an empty path set."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "src.py")
    git(repo, "commit", "-q", "-m", "initial")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths == set(), f"Expected an empty set, got {paths}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])