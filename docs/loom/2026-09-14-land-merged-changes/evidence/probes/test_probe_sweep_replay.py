"""Adversarial probe: `land --sweep` token replay, same-commit copies, forged PR
rows and invocation from the main worktree. Reuses the real-git Repo from
test_land_sweep.py. Each case asserts the SAFE behaviour.
"""
from __future__ import annotations

import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from test_land_sweep import Repo, git, ref_exists, run, token_of  # noqa: E402


def test_sweepToken_newMergedPrAfterListing_removesNothing(tmp_path: Path, monkeypatch) -> None:
    """A token confirmed before another PR merged cannot authorize the grown list."""
    layout = Repo(tmp_path)
    _a, wt_a = layout.branch("feat/a", worktree="wt-a")
    _rc, out, _err, _calls = run(monkeypatch, layout, "--sweep")
    token = token_of(out)
    layout.branch("feat/c")  # merged after the maintainer saw the list

    rc, out, err, calls = run(monkeypatch, layout, "--sweep", "--confirm", token)

    assert rc == 1
    assert "the sweep list differs" in err
    assert layout.intact("feat/a", wt_a) and layout.intact("feat/c")
    assert not calls.argvs("update-ref") and not calls.argvs("push")


def test_sweep_sameCommitCopyBranch_untouched(tmp_path: Path, monkeypatch) -> None:
    """A copy branch at the merged head, with no PR of its own, keeps local and remote refs."""
    layout = Repo(tmp_path)
    tip, _ = layout.branch("feat/a")
    git(layout.repo, "branch", "feat/a-copy", tip)
    git(layout.repo, "push", "-q", "origin", "feat/a-copy")
    git(layout.repo, "branch", "feat/a.b", tip)

    _rc, out, _err, _calls = run(monkeypatch, layout, "--sweep")
    rc, out, err, _calls = run(monkeypatch, layout, "--sweep", "--confirm", token_of(out))

    assert rc == 0, err
    assert layout.gone("feat/a")
    assert layout.intact("feat/a-copy")
    assert ref_exists(layout.repo, "refs/heads/feat/a.b")


def test_sweep_prRowHeadOfOtherBranch_notListed(tmp_path: Path, monkeypatch) -> None:
    """A merged row naming feat/q but carrying feat/z's oid selects neither branch."""
    layout = Repo(tmp_path)
    z_tip, _ = layout.branch("feat/z", merged=False)
    layout.branch("feat/q", merged=False)
    layout.merged.append({"number": 9, "headRefName": "feat/q", "headRefOid": z_tip})

    rc, out, err, _calls = run(monkeypatch, layout, "--sweep")

    assert rc == 0, err
    assert not any(line.startswith("remove ") for line in out.splitlines()), out
    assert layout.intact("feat/q") and layout.intact("feat/z")


def test_sweep_fromMainOnMergedBranch_skipsIt(tmp_path: Path, monkeypatch) -> None:
    """Run from the main worktree while it has a merged branch checked out: that branch is skipped."""
    layout = Repo(tmp_path)
    layout.branch("feat/m")
    git(layout.repo, "switch", "-q", "feat/m")

    _rc, out, _err, _calls = run(monkeypatch, layout, "--sweep")

    assert "skip feat/m — current working directory" in out
    assert "confirm with" not in out
    assert git(layout.repo, "symbolic-ref", "--short", "HEAD") == "feat/m"
