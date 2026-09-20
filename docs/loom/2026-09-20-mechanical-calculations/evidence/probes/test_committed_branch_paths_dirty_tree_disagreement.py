"""Adversarial probe: committed_branch_paths excludes working-tree edits.

The function must return ONLY committed paths between the branch and its base.
Working-tree edits (staged, unstaged, untracked) must NOT appear in the result,
or the auto-skip and reviewer floor will disagree with what reviewers/finalize-review
actually see.
"""
from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path

import pytest

from loom_checker.reviewers import committed_branch_paths


def git(repo: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(repo), *args], check=True, capture_output=True, text=True
    ).stdout.strip()


def make_repo(tmp_path: Path) -> Path:
    """Create a repo with base commit and a feature branch with one committed change."""
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "src.py")
    git(repo, "commit", "-q", "-m", "initial")
    # Create feature branch
    git(repo, "switch", "-q", "-c", "feature")
    (repo / "feature.txt").write_text("committed\n", encoding="utf-8")
    git(repo, "add", "feature.txt")
    git(repo, "commit", "-q", "-m", "add feature")
    return repo


def test_committed_branch_paths_excludes_unstaged_edits(tmp_path: Path) -> None:
    """Unstaged changes must not appear in committed_branch_paths."""
    repo = make_repo(tmp_path)
    # Unstaged edit to tracked file
    (repo / "src.py").write_text("VALUE = 999\n", encoding="utf-8")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    # Only the committed feature.txt should appear
    assert paths == {"feature.txt"}, f"Expected {{'feature.txt'}}, got {paths}"


def test_committed_branch_paths_excludes_staged_edits(tmp_path: Path) -> None:
    """Staged (cached) changes must not appear in committed_branch_paths."""
    repo = make_repo(tmp_path)
    # Staged edit to tracked file
    (repo / "src.py").write_text("VALUE = 888\n", encoding="utf-8")
    git(repo, "add", "src.py")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths == {"feature.txt"}, f"Expected {{'feature.txt'}}, got {paths}"


def test_committed_branch_paths_excludes_untracked_files(tmp_path: Path) -> None:
    """Untracked files must not appear in committed_branch_paths."""
    repo = make_repo(tmp_path)
    (repo / "untracked.txt").write_text("untracked\n", encoding="utf-8")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths == {"feature.txt"}, f"Expected {{'feature.txt'}}, got {paths}"


def test_committed_branch_paths_excludes_host_plumbing(tmp_path: Path) -> None:
    """Host plumbing (.codex/hooks/...) must be excluded from committed paths."""
    repo = make_repo(tmp_path)
    plumbing = repo / ".codex" / "hooks" / "loom-checker"
    plumbing.parent.mkdir(parents=True, exist_ok=True)
    plumbing.write_text("# scaffold hook\n", encoding="utf-8")
    git(repo, "add", ".codex/hooks/loom-checker")
    git(repo, "commit", "-q", "-m", "add plumbing")
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert ".codex/hooks/loom-checker" not in paths, f"Plumbing leaked: {paths}"
    assert paths == {"feature.txt"}, f"Expected {{'feature.txt'}}, got {paths}"


def test_committed_branch_paths_handles_empty_delta(tmp_path: Path) -> None:
    """When branch has no commits over base, result is empty set, not error."""
    repo = Path(tempfile.mkdtemp()) / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "test@example.com")
    git(repo, "config", "user.name", "Test")
    (repo / "src.py").write_text("VALUE = 1\n", encoding="utf-8")
    git(repo, "add", "src.py")
    git(repo, "commit", "-q", "-m", "initial")
    # No feature branch commits — diff is empty
    paths = committed_branch_paths(repo, "2026-09-20-mechanical-calculations")
    assert paths == set(), f"Expected empty set, got {paths}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])