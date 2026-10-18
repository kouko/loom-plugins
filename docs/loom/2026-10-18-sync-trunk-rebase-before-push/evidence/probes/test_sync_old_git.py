# concern: A git that lacks a rebase flag (git before 2.38 has no --no-update-refs) must not turn every conflict-free sync of a never-pushed branch into a refusal.
"""The merge path already tolerates git before 2.38 (merge-tree falls back);
the rebase path hard-requires `--no-update-refs`, which git 2.38 introduced.

The repository's own tests model an older git by making one subcommand
answer with a usage error (see `test_merge_tree_unavailable_falls_back_to_merge_then_abort`);
this probe does the same for the rebase flag.
"""
from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/scripts"))
sys.path.insert(0, str(REPO / "loom-code/tests"))

from loom_checker.command_handlers import sync as sync_handler  # noqa: E402
from test_sync_trunk import commit_file, git, land_on_main, repos  # noqa: E402


def test_sync_oldgit_succeeds(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """A conflict-free behind branch still syncs when git rejects --no-update-refs."""
    _origin, change, teammate = repos(tmp_path)
    commit_file(change, "feature.txt", "feature\n", "feature work")
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")
    real_git = sync_handler._git

    def old_git(git_exe, repo, *args, **kwargs):
        if args and args[0] == "rebase" and "--no-update-refs" in args:
            return 129, "", "error: unknown option `no-update-refs'"
        return real_git(git_exe, repo, *args, **kwargs)

    monkeypatch.setattr(sync_handler, "_git", old_git)
    monkeypatch.chdir(change)
    out, err = StringIO(), StringIO()

    code = sync_handler.cmd_sync_trunk([], out=out, err=err)

    assert code == 0, out.getvalue() + err.getvalue()
    assert "content changed" in out.getvalue()
    assert git(change, "merge-base", "--is-ancestor", trunk_tip, "HEAD") == ""
