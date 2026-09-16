"""Adversarial probes: what the smaller citation candidate set now reports.

`check_doc_citations.list_repo_files` used to hand the resolver every file on
disk; it now hands it what git says belongs to the repository. The change's own
docstring argues the direction is intended: citations that were silently
UNCHECKED because an ignored copy made them ambiguous are now checked.

These probes ask the other question -- what the smaller set makes the resolver
say about a file that is really there.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from check_doc_citations import check_citation, list_repo_files  # noqa: E402


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _init(repo: Path) -> Path:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    return repo


def test_check_citation_ignored_target_reports_no_finding(tmp_path: Path) -> None:
    """A citation whose target exists but is gitignored is called missing.

    `resolve_cited_path` tries the literal repo-root-relative path first, so a
    citation written from the root still resolves. One written as a suffix --
    `build/generated.md` under `docs/` -- falls through to the repo-wide suffix
    search, finds nothing now that the candidate set is git's, and is reported
    as "file not found" for a file that is on disk and readable.
    """
    repo = _init(tmp_path / "repo")
    (repo / ".gitignore").write_text("build/\n", encoding="utf-8")
    (repo / "docs" / "build").mkdir(parents=True)
    (repo / "docs" / "build" / "generated.md").write_text("hello\n", encoding="utf-8")
    (repo / "docs" / "note.md").write_text("see it\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")

    files = list_repo_files(repo)
    checked, reason = check_citation(repo, "build/generated.md", 1, None, files)

    assert (checked, reason) != (True, "file not found")


def test_check_citation_untracked_target_resolves_cleanly(tmp_path: Path) -> None:
    """The control: an untracked, unignored target is still a candidate."""
    repo = _init(tmp_path / "repo")
    (repo / "docs" / "sub").mkdir(parents=True)
    (repo / "docs" / "sub" / "fresh.md").write_text("hello\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")
    (repo / "docs" / "sub" / "newer.md").write_text("hello\n", encoding="utf-8")

    files = list_repo_files(repo)
    checked, reason = check_citation(repo, "sub/newer.md", 1, None, files)

    assert reason is None


def test_list_repo_files_worktree_copy_excludes_the_duplicate(
    tmp_path: Path,
) -> None:
    """The intended win, pinned: a nested worktree no longer doubles every path."""
    repo = _init(tmp_path / "repo")
    (repo / "docs" / "sub").mkdir(parents=True)
    (repo / "docs" / "sub" / "one.md").write_text("hello\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")
    _git(repo, "worktree", "add", "-q", "-b", "side", str(repo / "wt"))

    files = list_repo_files(repo)

    assert files == [".gitignore"] or all(not f.startswith("wt/") for f in files)
    assert "docs/sub/one.md" in files
