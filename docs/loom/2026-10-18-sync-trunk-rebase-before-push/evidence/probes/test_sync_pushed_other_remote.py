# concern: Commits already pushed to a remote other than origin must never be rewritten by sync, or the next plain push to that remote is rejected.
"""The pushed-check asks only `origin` (ls-remote origin, --remotes=origin).

A branch pushed with `-u` to a second remote (a fork, a backup remote) is
pushed history all the same; the intent's constraint is to never rewrite a
commit that exists on a remote, and Acceptance 2 requires the next non-forced
publish to be accepted.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/tests"))

from test_sync_trunk import commit_file, git, land_on_main, repos, sync  # noqa: E402


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
