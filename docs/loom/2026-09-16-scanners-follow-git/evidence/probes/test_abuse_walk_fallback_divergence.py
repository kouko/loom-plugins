"""Adversarial probes: the two code paths of `repo_files.repository_files`.

`loom-code/scripts/repo_files.py` promises one answer to "which files belong
to the repository at this root", computed either by asking git or, when there
is no git, by walking the filesystem. Its module docstring states the shared
post-condition: "Both paths then drop any path with a component in
IGNORED_DIRECTORY_NAMES". The spec records the same decision (user-decided,
`docs/loom/2026-09-16-scanners-follow-git/spec.md`), and
`loom-workflow/scripts/test_no_live_cot_explain_references.py` deleted four of
its five `SKIPPED_DIRS` names on the strength of it.

These probes hold the two paths against each other on the same tree.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from repo_files import IGNORED_DIRECTORY_NAMES, repository_files  # noqa: E402


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _init(repo: Path) -> Path:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    return repo


def _relative(root: Path) -> list[str]:
    return sorted(path.relative_to(root).as_posix() for path in repository_files(root))


def test_repository_files_gitfile_without_git_drops_the_dot_git_component(
    tmp_path: Path,
) -> None:
    """A `.git` that is a FILE used to survive the no-git walk.

    A linked worktree and a submodule both mark their directory with a `.git`
    *file*, not a directory. `_walk_entries` pruned directories by name only, so
    the file came back as one of the repository's own files -- while the git
    path drops any path carrying a `.git` component. Same tree, two answers.
    `repo_files.py:146-148` closed it by filtering filenames against
    IGNORED_DIRECTORY_NAMES too.
    """
    root = tmp_path / "nogit"
    (root / "sub").mkdir(parents=True)
    (root / "sub" / ".git").write_text("gitdir: /elsewhere\n", encoding="utf-8")
    (root / "sub" / "f.txt").write_text("x\n", encoding="utf-8")

    assert ".git" in IGNORED_DIRECTORY_NAMES
    assert "sub/.git" not in _relative(root)


def test_repository_files_gitfile_with_git_drops_the_dot_git_component(
    tmp_path: Path,
) -> None:
    """The control: with git present the same tree loses `sub/.git`.

    This is the half that holds, and it is what makes the failure above a
    divergence between the two paths rather than a missing feature.
    """
    root = _init(tmp_path / "withgit")
    (root / "sub").mkdir()
    (root / "sub" / ".git").write_text("gitdir: /elsewhere\n", encoding="utf-8")
    (root / "sub" / "f.txt").write_text("x\n", encoding="utf-8")

    assert "sub/.git" not in _relative(root)
    assert "sub/f.txt" in _relative(root)


def test_repository_files_bare_repository_lists_no_git_internals(
    tmp_path: Path,
) -> None:
    """A bare repository was not "no git", but was treated as such.

    `git rev-parse --show-toplevel` has no work tree to print in a bare
    repository, so the module concluded there was no git here and walked. The
    directory it then walked IS the object store: `HEAD`, `config`, every
    `hooks/*.sample`, and every loose object -- in a module that ships in a
    plugin run inside other people's repositories. `repo_files.py:114-115`
    closed it by asking `--is-bare-repository` first and short-circuiting to an
    empty listing.
    """
    bare = tmp_path / "bare.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)

    assert repository_files(bare) == []
