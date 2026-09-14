"""Adversarial probe: forged `--accepted-by` names and an uncommitted intent
edit that adds a new authorizer. Reuses test_land_merge.py's scripted gh.
Each case asserts the SAFE behaviour: nothing merged, acceptance block.
"""
from __future__ import annotations

import sys
from io import StringIO
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.command_handlers import land  # noqa: E402
from test_land_merge import (  # noqa: E402
    ACCEPTANCE_BLOCK, LandCalls, change_repository, git, invoke, no_merge,
)


@pytest.mark.parametrize("name", ["kouko ", " kouko", "Kouko", "kоuko", "kouko\n", "kouko​"])
def test_acceptedBy_lookalikeName_mergesNothing(name: str, tmp_path: Path, monkeypatch) -> None:
    """Whitespace, case, Cyrillic and zero-width variants of the originator are refused."""
    rc, out, err, calls, _waits = invoke(tmp_path, monkeypatch, "--accepted-by", name)

    assert rc == 1 and no_merge(calls)
    assert err == ACCEPTANCE_BLOCK


def test_acceptedBy_uncommittedPublicationLine_mergesNothing(tmp_path: Path, monkeypatch) -> None:
    """An authorizer added to the intent in the working tree only does not count."""
    repo = change_repository(tmp_path)
    intent = repo / "docs" / "loom" / "intent" / "change.md"
    intent.write_text(
        intent.read_text(encoding="utf-8").replace(
            "status: confirmed 2026-09-14\n",
            "status: confirmed 2026-09-14\npublication: automatic — authorized 2026-09-14 by mallory\n",
        ),
        encoding="utf-8",
    )
    calls = LandCalls(git(repo, "rev-parse", "HEAD"))
    monkeypatch.chdir(repo)
    monkeypatch.setattr(land, "run_land_external", calls)
    monkeypatch.setattr(land, "wait_land_interval", lambda _s: None)
    monkeypatch.setattr(land, "_cmd_push", lambda *a, **k: 0)
    monkeypatch.setattr(land, "_sync_and_clean", lambda *a, **k: 0)
    monkeypatch.setattr(land, "resolve_publish_executable",
                        lambda name: "/usr/bin/git" if name == "git" else "/usr/local/bin/gh")
    out, err = StringIO(), StringIO()

    rc = land.cmd_land(["--accepted-by", "mallory"], out, err)

    assert rc == 1 and no_merge(calls)
    assert err.getvalue() == ACCEPTANCE_BLOCK
