"""Adversarial probes: hostile and absent input to `repository_files`.

Filenames come out of `git ls-files -z` and are then stat-ed. Everything here
attacks that seam: names git would quote without `-z`, entries whose stat
answer is not "an existing regular file", and roots that are not a repository
at all. Most of these attempts fail to break anything -- that is the point of
recording them.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from repo_files import repository_files  # noqa: E402


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _init(repo: Path) -> Path:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    return repo


def _relative(root: Path) -> set[str]:
    return {path.relative_to(root).as_posix() for path in repository_files(root)}


HOSTILE_NAMES = [
    "newline\nname.md",
    'double"quote.md',
    "single'quote.md",
    "back\\slash.md",
    " leading-space.md",
    "trailing-space .md",
    "日本語.md",
    "tab\tname.md",
]


def test_repository_files_hostile_names_returns_every_one(tmp_path: Path) -> None:
    """Names git quotes without `-z`, read back under `core.quotePath=true`."""
    repo = _init(tmp_path / "repo")
    created = []
    for name in HOSTILE_NAMES:
        (repo / name).write_text("x\n", encoding="utf-8")
        created.append(name)
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")
    _git(repo, "config", "core.quotePath", "true")

    listed = _relative(repo)
    assert {Path(name).as_posix() for name in created} <= listed


def test_repository_files_symlinks_keeps_only_the_resolvable_file(
    tmp_path: Path,
) -> None:
    """A broken symlink and a symlink to a directory are not regular files."""
    repo = _init(tmp_path / "repo")
    (repo / "real.md").write_text("x\n", encoding="utf-8")
    (repo / "dir").mkdir()
    (repo / "dir" / "inner.md").write_text("x\n", encoding="utf-8")
    (repo / "to-file.md").symlink_to(repo / "real.md")
    (repo / "broken.md").symlink_to(repo / "absent.md")
    (repo / "to-dir").symlink_to(repo / "dir")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")

    listed = _relative(repo)
    assert "real.md" in listed
    assert "to-file.md" in listed
    assert "broken.md" not in listed
    assert "to-dir" not in listed


def test_repository_files_deleted_after_commit_drops_the_missing_path(
    tmp_path: Path,
) -> None:
    """`--cached` still names a path removed from the work tree."""
    repo = _init(tmp_path / "repo")
    (repo / "gone.md").write_text("x\n", encoding="utf-8")
    (repo / "stays.md").write_text("x\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")
    (repo / "gone.md").unlink()

    assert _relative(repo) == {"stays.md"}


def test_repository_files_absent_root_returns_no_files(tmp_path: Path) -> None:
    """A root that does not exist answers "no files" instead of failing.

    This pins the observed behaviour rather than claiming it is wrong: the
    walks it replaced were silent in the same way. It is recorded because every
    consumer reads an empty list as "nothing to report", so a gate handed a
    wrong root passes vacuously. A root that is a regular file behaves the same.
    """
    missing = tmp_path / "does-not-exist"
    a_file = tmp_path / "plain.txt"
    a_file.write_text("x\n", encoding="utf-8")

    assert repository_files(missing) == []
    assert repository_files(a_file) == []


def test_repository_files_empty_repository_returns_no_files(
    tmp_path: Path,
) -> None:
    """An initialised repository with no commit and no files: zero, not a crash."""
    repo = _init(tmp_path / "repo")

    assert repository_files(repo) == []
