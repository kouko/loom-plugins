# concern: a failed keep-record write is swallowed, so the kept change later lands on a sweep remove line
"""Adversarial probe (REQ-1/REQ-2): when `git config` cannot write the keep
record (here a held `.git/config.lock`, as a concurrent git process leaves it),
the keep land must not report success silently. Either the record exists or the
failure is loud (non-zero exit or an error line).
"""
from __future__ import annotations

import subprocess
import sys
from io import StringIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))
sys.path.insert(0, str(ROOT / "loom-code" / "tests"))

from loom_checker.command_handlers import land  # noqa: E402
from test_land_sweep import GH, GIT, Repo  # noqa: E402


def test_keepLand_configLockHeld_failsLoudOrRecords(tmp_path: Path, monkeypatch) -> None:
    """A keep whose record write fails is reported, never a silent 'Kept worktree'."""
    layout = Repo(tmp_path)
    _tip, wt = layout.branch("feat/k", worktree="wt-k")
    monkeypatch.setattr(land, "sync_trunk", lambda target, out: None)
    target = land.LandTarget(wt, "", "feat/k", "main", "github.com/example/project", 1,
                             GIT, GH, None)
    lock = layout.repo / ".git" / "config.lock"
    lock.write_text("", encoding="utf-8")
    out, err = StringIO(), StringIO()
    try:
        rc = land._sync_and_clean(target, out, err, keep=True)
    finally:
        lock.unlink()
    recorded = subprocess.run(
        ["git", "-C", str(layout.repo), "config", "--get", "branch.feat/k.loomKept"],
        capture_output=True, text=True,
    ).stdout.strip()
    # Without the record a later sweep offers the kept change on a remove line,
    # so a silent success here is the defect this program pins.
    assert recorded or rc != 0 or err.getvalue(), out.getvalue()
