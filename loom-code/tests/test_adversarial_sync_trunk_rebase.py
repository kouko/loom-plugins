"""Adversarial programs for `sync-trunk` rebasing a never-pushed branch.

Graduated from the 2026-10-18-sync-trunk-rebase-before-push change store:
a replayed history that trips over a now-ignored local file, a git without
`--no-update-refs`, and a branch pushed only to a non-origin remote.
"""
from __future__ import annotations

import subprocess
from io import StringIO
from pathlib import Path

import pytest

from loom_checker.command_handlers import sync as sync_handler
from test_sync_trunk import commit_file, git, land_on_main, repos, sync


def test_sync_ignoredhistory_succeeds(tmp_path: Path) -> None:
    """A never-pushed branch that once tracked a now-ignored local file syncs and keeps that file."""
    _origin, change, teammate = repos(tmp_path)
    commit_file(change, "local.cfg", "OLD=committed\n", "commit local config by mistake")
    git(change, "rm", "-q", "--cached", "local.cfg")
    (change / ".gitignore").write_text("local.cfg\n", encoding="utf-8")
    git(change, "add", ".gitignore")
    git(change, "commit", "-q", "-m", "untrack and ignore local config")
    (change / "local.cfg").write_text("LOCAL=keep-me\n", encoding="utf-8")
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stdout + result.stderr
    assert "content changed" in result.stdout
    assert git(change, "merge-base", "--is-ancestor", trunk_tip, "HEAD") == ""
    assert (change / "local.cfg").read_text(encoding="utf-8") == "LOCAL=keep-me\n"


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


def test_sync_otherremote_keepscommits(tmp_path: Path) -> None:
    """A branch pushed only to a non-origin remote keeps its pushed commit and pushes without force."""
    _origin, change, teammate = repos(tmp_path)
    fork = tmp_path / "fork.git"
    subprocess.run(["git", "init", "-q", "--bare", str(fork)], check=True)
    git(change, "remote", "add", "fork", str(fork))
    own = commit_file(change, "feature.txt", "feature\n", "feature work")
    git(change, "push", "-q", "-u", "fork", "feature")
    trunk_tip = land_on_main(teammate, "other.txt", "other\n")

    result = sync(change)

    assert result.returncode == 0, result.stdout + result.stderr
    ancestor = subprocess.run(
        ["git", "-C", str(change), "merge-base", "--is-ancestor", own, "HEAD"], capture_output=True
    )
    assert ancestor.returncode == 0, "the commit pushed to the fork was rewritten"
    assert git(change, "merge-base", "--is-ancestor", trunk_tip, "HEAD") == ""
    pushed = subprocess.run(
        ["git", "-C", str(change), "push", "-q", "fork", "feature"], capture_output=True, text=True
    )
    assert pushed.returncode == 0, pushed.stderr
