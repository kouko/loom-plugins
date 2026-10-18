# concern: A conflict-free sync of a never-pushed branch must not be refused because an earlier branch commit tracked a file that is now ignored locally.
"""Replaying every own commit trips over a local ignored file that the merge path never touched.

A branch commits `local.cfg` by mistake, then untracks and ignores it while
the user keeps a local copy. Trunk moves on with an unrelated change. There
is no conflict and nothing collides between HEAD and the trunk tip, so the
sync must succeed (Acceptance 1 and 4) and the local file must survive.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/tests"))

from test_sync_trunk import commit_file, git, land_on_main, repos, sync  # noqa: E402


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
