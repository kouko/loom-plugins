"""Adversarial probe: `land --accepted-by` when gh or git misbehave (empty,
malformed, non-list output; failing fetch before verification). Reuses the
scripted-gh fixture from test_land_merge.py. Each case asserts the SAFE
behaviour: nothing merged, or a merged PR that stops before sync and cleanup.
"""
from __future__ import annotations

import subprocess
import sys
from io import StringIO
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.command_handlers import land  # noqa: E402
from test_land_merge import LandCalls, change_repository, git, invoke, no_merge  # noqa: E402


def test_checksLookup_emptyStdoutExitZero_mergesNothing(tmp_path: Path, monkeypatch) -> None:
    """gh exiting 0 with no output at all is an unobserved check state, not 'no checks'."""
    def configure(calls: LandCalls) -> None:
        calls.checks = [""]

    rc, out, err, calls, _waits = invoke(tmp_path, monkeypatch, "--accepted-by", "kouko",
                                         configure=configure)

    assert no_merge(calls), (rc, out, err)
    assert rc == 1


def test_checksLookup_jsonObjectNotList_mergesNothing(tmp_path: Path, monkeypatch) -> None:
    """A JSON object where a list of checks is expected blocks the merge."""
    def configure(calls: LandCalls) -> None:
        calls.checks = ['{"name": "gate", "bucket": "pass"}']

    rc, out, err, calls, _waits = invoke(tmp_path, monkeypatch, "--accepted-by", "kouko",
                                         configure=configure)

    assert rc == 1 and no_merge(calls)
    assert "BLOCK land.merge" in err


def test_mergeStateLookup_nullPayload_mergesNothing(tmp_path: Path, monkeypatch) -> None:
    """`null` from the merge-state read blocks instead of raising."""
    def configure(calls: LandCalls) -> None:
        calls.merge_states = [None]

    rc, out, err, calls, _waits = invoke(tmp_path, monkeypatch, "--accepted-by", "kouko",
                                         configure=configure)

    assert rc == 1 and no_merge(calls)


def test_mergeReread_mergedWithoutOid_blocks(tmp_path: Path, monkeypatch) -> None:
    """A failed merge whose re-read says MERGED with a null mergeCommit is not a success."""
    def configure(calls: LandCalls) -> None:
        calls.merge_outcome = (1, "boom")
        calls.pr_states = [{"state": "MERGED", "mergeCommit": None}]

    rc, out, err, calls, _waits = invoke(tmp_path, monkeypatch, "--accepted-by", "kouko",
                                         configure=configure)

    assert rc == 1
    assert "Merged PR" not in out
    assert "merge not performed" in err


class FetchFails(LandCalls):
    def __call__(self, argv, timeout, **kwargs):
        if [str(a) for a in argv][1:2] == ["fetch"]:
            self.calls.append([str(a) for a in argv])
            return subprocess.CompletedProcess(argv, 128, "", "fatal: unable to access")
        return super().__call__(argv, timeout, **kwargs)


def test_verifyFetch_gitFetchFails_noSyncOrCleanup(tmp_path: Path, monkeypatch) -> None:
    """A failing fetch before verification exits 1 and never reaches trunk sync or cleanup."""
    repo = change_repository(tmp_path)
    calls = FetchFails(git(repo, "rev-parse", "HEAD"))
    reached: list[bool] = []
    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", calls)
    monkeypatch.setattr(land, "wait_land_interval", lambda _s: None)
    monkeypatch.setattr(land, "_cmd_push", lambda *a, **k: 0)
    monkeypatch.setattr(land, "_sync_and_clean", lambda *a, **k: reached.append(True) or 0)
    monkeypatch.setattr(land, "resolve_publish_executable",
                        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh")
    out, err = StringIO(), StringIO()

    rc = land.cmd_land(["--accepted-by", "kouko"], out, err)

    assert rc == 1
    assert not reached
    assert "BLOCK land.verify: cannot fetch origin main" in err.getvalue()
