"""The one answer to "which files belong to the repository at this root".

git is asked, not reimplemented: `git ls-files --cached --others
--exclude-standard -z`, run through `git_exec.run_git` with `-C <root>`, so a
root that is a subdirectory scopes the listing to that subtree. `-z` is
mandatory -- without it a path containing a newline comes back shell-quoted
(git-config(1), core.quotePath). Encoding/argv rationale lives in
`git_exec.run_git`'s docstring and is not restated here.

When there is no git the filesystem is walked instead, and a `.gitignore` that
happens to be present is NOT honoured. ripgrep, fd and ruff all behave that way
by default, and it keeps a `git archive` copy working. A BARE repository is git
even though `git rev-parse --show-toplevel` prints nothing there; it owns no
work tree, so it owns no files, and the walk must not be reached.

Both paths then drop any path with a component in IGNORED_DIRECTORY_NAMES, and
drop every entry that is not an existing regular file: `--others` emits a
nested repository or linked worktree as one opaque directory entry such as
`wt/` rather than its files -- that entry is how the worktree's contents stay
out of the listing, so it is dropped, never expanded -- and `--cached` still
lists a staged-but-deleted path. Paths returned are absolute; every caller
derives its own relative form.

Submodule contents are never listed: `--recurse-submodules` is documented as
incompatible with `--others` (git-ls-files(1)).

`nested_worktrees` and `nested_repositories` answer the neighbouring git
question -- where the foreign subtrees inside this root are -- for the callers
that must exclude those paths rather than list files themselves, so that no
second git invocation grows outside this module. They are not the same set:
`nested_repositories` names the opaque directory entries git collapsed, which
covers a clone and a submodule but misses a gitignored worktree;
`nested_worktrees` names what `git worktree list` reports, which covers the
gitignored worktree but nothing else. A caller that must exclude everything
foreign takes the union.

Sibling-module import (no `__init__.py`), following `git_exec`'s own
precedent in this directory.
"""
from __future__ import annotations

import os
from pathlib import Path

from git_exec import run_git

IGNORED_DIRECTORY_NAMES = frozenset(
    {".git", ".pytest_cache", "__pycache__", "node_modules"}
)


def repository_files(root: Path | str) -> list[Path]:
    """Absolute paths of the files belonging to the repository at `root`."""
    root = Path(root)
    entries = _git_entries(root)
    if entries is None:
        entries = _walk_entries(root)
    return [path for path in entries if path.is_file()]


def nested_worktrees(root: Path | str) -> list[Path]:
    """Absolute paths of the git worktrees that live inside `root`.

    `git worktree list --porcelain` lists every worktree of the repository,
    including the one `root` itself is in; only the ones strictly below `root`
    are returned, so the repository's own worktree is never one of them. The
    paths git prints are already resolved, so `root` is resolved before the
    comparison. No git, or a `root` outside any repository, is an empty list,
    not an error -- the callers have nothing to exclude in that case.
    """
    root = Path(root).resolve()
    listing = run_git(root, "worktree", "list", "--porcelain")
    if listing is None:
        return []
    paths = [
        Path(line[len("worktree "):])
        for line in listing.splitlines()
        if line.startswith("worktree ")
    ]
    return sorted(path for path in paths if path != root and root in path.parents)


def nested_repositories(root: Path | str) -> list[Path]:
    """Absolute paths of the git repositories nested inside `root`.

    These are exactly the entries `repository_files` drops as "not a file":
    git collapses a nested repository -- a linked worktree, a plain clone
    dropped in `vendor/`, a submodule's gitlink -- to one opaque directory
    entry instead of listing its contents. Naming them lets a caller that
    must EXCLUDE those subtrees (rather than list files) use the same answer
    the scanners use. No git here is an empty list, not an error.
    """
    root = Path(root)
    entries = _git_entries(root)
    if entries is None:
        return []
    return sorted({path for path in entries if path.is_dir()})


def _git_entries(root: Path) -> list[Path] | None:
    """Paths git lists under `root`, or None when there is no git here.

    A bare repository is git, but owns no work tree: `--show-toplevel` has
    nothing to print there, so absence of git is decided by
    `--is-bare-repository` FIRST -- otherwise the walk fallback would return
    the object store itself (`HEAD`, `config`, `hooks/*.sample`), whose
    directory is named `foo.git` and so prunes nothing.
    """
    if run_git(root, "rev-parse", "--is-bare-repository") == "true":
        return []
    if not run_git(root, "rev-parse", "--show-toplevel"):
        return None
    listing = run_git(
        root, "ls-files", "--cached", "--others", "--exclude-standard", "-z",
        strip=False,
    )
    if listing is None:
        return None
    return [
        root / entry
        for entry in listing.split("\0")
        if entry and not _is_ignored(Path(entry).parts)
    ]


def _walk_entries(root: Path) -> list[Path]:
    """Every file under `root`, minus the ignored names.

    Pruning `subdirectories` is the cheap half -- it keeps the walk out of
    the subtree. The filename is filtered too, because an ignored name is
    not always a directory: a linked worktree and a submodule both mark
    their directory with a `.git` FILE. Filtering only directories is what
    made this path disagree with the git path on the same tree.
    """
    paths: list[Path] = []
    for directory, subdirectories, filenames in os.walk(root):
        subdirectories[:] = [
            name for name in subdirectories
            if name not in IGNORED_DIRECTORY_NAMES
        ]
        paths.extend(
            Path(directory) / name for name in filenames
            if name not in IGNORED_DIRECTORY_NAMES
        )
    return paths


def _is_ignored(parts) -> bool:
    return any(part in IGNORED_DIRECTORY_NAMES for part in parts)
