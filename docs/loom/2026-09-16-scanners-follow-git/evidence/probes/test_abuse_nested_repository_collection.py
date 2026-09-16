"""Adversarial probes: what counts as "not this repository" for the runner.

`repo_files.repository_files` excludes every nested git repository -- a linked
worktree, a plain clone someone dropped in `vendor/`, a submodule -- because
`git ls-files --others` collapses each of them to one opaque directory entry
that the module then drops.

These probes ran the real pytest command `scripts/run_package_tests.py` builds
and asked what it collects. They found the runner excluding a NARROWER set than
the scanners: only the paths `git worktree list` reports. Commit 338bef0c closed
that gap -- `scripts/run_package_tests.py:73` now excludes the union of
`repo_files.nested_repositories` and `repo_files.nested_worktrees`, so a nested
clone and a submodule are excluded too. The assertions below pin the closed
behaviour.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))
sys.path.insert(0, str(REPO_ROOT / "scripts"))

from repo_files import repository_files  # noqa: E402
from run_package_tests import loom_family_commands  # noqa: E402


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def _seed(repo: Path) -> Path:
    (repo / "loom-code" / "scripts").mkdir(parents=True)
    (repo / "loom-code" / "scripts" / "test_seed.py").write_text(
        "def test_s():\n    pass\n", encoding="utf-8"
    )
    _git(repo, "init", "-q")
    _git(repo, "config", "user.email", "t@example.com")
    _git(repo, "config", "user.name", "T")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "c")
    return repo


def _collect(repo: Path) -> str:
    """Collect with exactly the exclusions the runner would pass.

    The code group names three directories; only `loom-code/scripts/` exists in
    these fixtures, so the command is rebuilt around that one target with the
    runner's own `--ignore` tokens carried over verbatim.
    """
    command = loom_family_commands(repo, "-q", only="code")[0]
    ignores = [token for token in command if token.startswith("--ignore=")]
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "loom-code/scripts/", "-q",
         "-p", "no:cacheprovider", "--collect-only", *ignores],
        cwd=repo, capture_output=True, text=True,
    )
    return result.stdout


def test_package_tests_nested_worktree_collects_nothing_from_it(
    tmp_path: Path,
) -> None:
    """The control: the case the change was written for holds end to end."""
    repo = _seed(tmp_path / "repo")
    nested = repo / "loom-code" / "scripts" / "wt"
    _git(repo, "worktree", "add", "-q", "-b", "wt-branch", str(nested))
    (nested / "loom-code" / "scripts" / "test_intruder.py").write_text(
        "def test_i():\n    assert False\n", encoding="utf-8"
    )

    assert "test_intruder" not in _collect(repo)


def test_package_tests_nested_clone_collects_nothing_from_it(
    tmp_path: Path,
) -> None:
    """A plain git repository nested in the tree was still collected.

    The scanners already agreed it is not ours: `repository_files` omits every
    file under it. The package-test command disagreed, because
    `git worktree list` never mentions it, so a foreign failing test failed this
    repository's suite. The runner now excludes `nested_repositories` as well,
    which is what names this clone.
    """
    repo = _seed(tmp_path / "repo")
    inner = repo / "loom-code" / "scripts" / "vendor"
    inner.mkdir(parents=True)
    (inner / "test_foreign.py").write_text(
        "def test_foreign():\n    assert False\n", encoding="utf-8"
    )
    _git(inner, "init", "-q")
    _git(inner, "config", "user.email", "t@example.com")
    _git(inner, "config", "user.name", "T")
    _git(inner, "add", "-A")
    _git(inner, "commit", "-q", "-m", "c")

    listed = [path.relative_to(repo).as_posix() for path in repository_files(repo)]
    assert "loom-code/scripts/vendor/test_foreign.py" not in listed

    assert "test_foreign" not in _collect(repo)


def test_package_tests_submodule_collects_nothing_from_it(tmp_path: Path) -> None:
    """A submodule's tests were collected as this repository's.

    The module documents that submodule contents are never listed, so the two
    definitions of "belongs to this repository" parted company here too. The
    same union fix closed it: git collapses a submodule to one directory entry,
    so `nested_repositories` names it and the runner passes `--ignore` for it.
    """
    repo = _seed(tmp_path / "repo")
    sub = _seed(tmp_path / "sub")
    (sub / "test_sub.py").write_text(
        "def test_sub():\n    assert False\n", encoding="utf-8"
    )
    _git(sub, "add", "-A")
    _git(sub, "commit", "-q", "-m", "c")
    _git(repo, "-c", "protocol.file.allow=always", "submodule", "add", "-q",
         str(sub), "loom-code/scripts/subm")
    _git(repo, "commit", "-q", "-m", "add sub")

    listed = [path.relative_to(repo).as_posix() for path in repository_files(repo)]
    assert "loom-code/scripts/subm/test_sub.py" not in listed

    assert "test_sub" not in _collect(repo)
