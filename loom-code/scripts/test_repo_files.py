"""Executable contract for `repo_files.repository_files` -- the one answer to
"which files belong to the repository at this root" that loom's gates share.

Every test builds a real temporary git repository rather than mocking git:
the behaviour under test IS git's, so a mock would only assert the mock.
"""
from __future__ import annotations

import subprocess
from pathlib import Path

from repo_files import nested_repositories, nested_worktrees, repository_files


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True)


def _init_repo(repo: Path) -> None:
    repo.mkdir(parents=True, exist_ok=True)
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")


def _write(repo: Path, rel: str, text: str = "x\n") -> Path:
    path = repo / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _commit(repo: Path, message: str = "c") -> None:
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", message)


def _rel(repo: Path, paths) -> set[str]:
    return {str(Path(p).relative_to(repo)) for p in paths}


def test_untracked_unignored_file_is_listed(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "tracked.py")
    _commit(repo)
    _write(repo, "untracked.py")

    assert _rel(repo, repository_files(repo)) == {"tracked.py", "untracked.py"}


def test_gitignored_file_is_absent(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, ".gitignore", "build/\nsecret.txt\n")
    _write(repo, "kept.py")
    _commit(repo)
    _write(repo, "build/out.py")
    _write(repo, "secret.txt")

    listed = _rel(repo, repository_files(repo))
    assert "kept.py" in listed
    assert "build/out.py" not in listed
    assert "secret.txt" not in listed


def test_fixed_ignore_list_components_are_dropped(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "kept.py")
    _write(repo, "__pycache__/kept.cpython.pyc")
    _write(repo, "node_modules/pkg/index.js")
    _write(repo, ".pytest_cache/CACHEDIR.TAG")
    _commit(repo)

    assert _rel(repo, repository_files(repo)) == {"kept.py"}


def test_subdirectory_root_scopes_the_listing(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "top.py")
    _write(repo, "sub/inside.py")
    _commit(repo)

    assert _rel(repo, repository_files(repo / "sub")) == {"sub/inside.py"}


def test_returns_absolute_paths(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "a.py")
    _commit(repo)

    assert all(Path(p).is_absolute() for p in repository_files(repo))


def test_nested_linked_worktree_contributes_nothing(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "kept.py")
    _commit(repo)
    _git(repo, "worktree", "add", "-q", "-b", "wt-branch", str(repo / "wt"))

    listed = _rel(repo, repository_files(repo))
    assert listed == {"kept.py"}, listed
    # The opaque `wt/` directory entry itself must not be returned either.
    assert not any(str(p).startswith(str(repo / "wt")) for p in
                   repository_files(repo))


def test_nested_worktrees_lists_the_nested_one_and_not_the_repository(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "kept.py")
    _commit(repo)
    _git(repo, "worktree", "add", "-q", "-b", "wt-branch", str(repo / "sub" / "wt"))

    assert nested_worktrees(repo) == [(repo / "sub" / "wt").resolve()]


def test_nested_worktrees_is_empty_without_a_nested_worktree(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "kept.py")
    _commit(repo)

    assert nested_worktrees(repo) == []


def test_nested_worktrees_is_empty_without_git(tmp_path: Path) -> None:
    plain = tmp_path / "plain"
    _write(plain, "a.py")

    assert nested_worktrees(plain) == []


def test_staged_but_deleted_path_is_not_returned(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "gone.py")
    _write(repo, "kept.py")
    _commit(repo)
    (repo / "gone.py").unlink()

    assert _rel(repo, repository_files(repo)) == {"kept.py"}


def test_walks_when_git_is_absent(tmp_path: Path) -> None:
    plain = tmp_path / "plain"
    _write(plain, "a.py")
    _write(plain, "sub/b.py")
    _write(plain, "__pycache__/c.pyc")
    _write(plain, ".gitignore", "a.py\n")

    listed = _rel(plain, repository_files(plain))
    # No .git means the .gitignore is not honoured -- ripgrep/fd/ruff default.
    assert listed == {"a.py", "sub/b.py", ".gitignore"}, listed


def test_archive_copy_listing_matches_git_checkout(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "a.py")
    _write(repo, "sub/b.py")
    _commit(repo)

    archive = tmp_path / "archive"
    archive.mkdir()
    tarball = tmp_path / "HEAD.tar"
    with tarball.open("wb") as handle:
        subprocess.run(["git", "-C", str(repo), "archive", "HEAD"],
                       check=True, stdout=handle)
    subprocess.run(["tar", "-xf", str(tarball), "-C", str(archive)], check=True)

    assert _rel(archive, repository_files(archive)) == _rel(
        repo, repository_files(repo))


def test_walk_drops_a_dot_git_that_is_a_file(tmp_path: Path) -> None:
    """A linked worktree and a submodule mark their directory with a `.git`
    FILE, so the no-git walk has to drop ignored names on every path
    component, not only on directories -- the git path already does."""
    plain = tmp_path / "plain"
    _write(plain, "sub/.git", "gitdir: /elsewhere\n")
    _write(plain, "sub/f.txt")

    assert _rel(plain, repository_files(plain)) == {"sub/f.txt"}


def test_bare_repository_lists_nothing(tmp_path: Path) -> None:
    """A bare repository has no work tree, so it owns no files. Walking it
    would return its object store (`HEAD`, `config`, `hooks/*.sample`)."""
    bare = tmp_path / "bare.git"
    subprocess.run(["git", "init", "-q", "--bare", str(bare)], check=True)

    assert repository_files(bare) == []


def test_nested_repositories_reports_a_plain_clone(tmp_path: Path) -> None:
    """The directories `repository_files` drops as "not ours" are nameable:
    a nested clone git collapses to one opaque entry, not only a worktree."""
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "kept.py")
    _commit(repo)
    inner = repo / "vendor"
    _init_repo(inner)
    _write(inner, "foreign.py")
    _commit(inner)

    assert _rel(repo, nested_repositories(repo)) == {"vendor"}
    assert "vendor/foreign.py" not in _rel(repo, repository_files(repo))


def test_nested_repositories_reports_a_submodule(tmp_path: Path) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "kept.py")
    _commit(repo)
    sub = tmp_path / "sub"
    _init_repo(sub)
    _write(sub, "foreign.py")
    _commit(sub)
    _git(repo, "-c", "protocol.file.allow=always", "submodule", "add", "-q",
         str(sub), "subm")
    _git(repo, "commit", "-q", "-m", "add sub")

    assert "subm" in _rel(repo, nested_repositories(repo))


def test_nested_repositories_is_empty_without_git(tmp_path: Path) -> None:
    plain = tmp_path / "plain"
    _write(plain, "a.py")

    assert nested_repositories(plain) == []


def test_nested_repositories_ignores_a_tracked_symlink_to_a_directory(
    tmp_path: Path,
) -> None:
    """A tracked symlink is one `--cached` entry that `is_dir` follows; it is
    not a collapsed foreign subtree, and naming it would make callers
    exclude the real directory it points at."""
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "real/sub/test_a.py")
    (repo / "link").symlink_to("real/sub", target_is_directory=True)
    _commit(repo)

    assert nested_repositories(repo) == []


def test_nested_worktrees_finds_a_worktree_whose_path_holds_a_newline(
    tmp_path: Path,
) -> None:
    repo = tmp_path / "repo"
    _init_repo(repo)
    _write(repo, "kept.py")
    _commit(repo)
    odd = repo / "odd\nname"
    _git(repo, "worktree", "add", "-q", "-b", "wt-branch", str(odd))

    assert nested_worktrees(repo) == [odd.resolve()]
