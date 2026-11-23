# concern: a later session working inside a kept worktree cannot see that its change was kept
"""Adversarial probe (REQ-1, Acceptance 1): a `land --sweep` listing run from any
worktree of the repository marks a kept change as kept. Ship tells the agent to
stay in the kept worktree, so the kept worktree itself is the likeliest place a
later session runs sweep from. Reuses the real-git Repo from test_land_sweep.py.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))
sys.path.insert(0, str(ROOT / "loom-code" / "tests"))

from test_land_sweep import Repo, git, run  # noqa: E402


def test_sweep_invokedInsideKeptWorktree_marksChangeKept(tmp_path: Path, monkeypatch) -> None:
    """Sweep run from the kept linked worktree shows its branch on a kept line."""
    layout = Repo(tmp_path)
    _tip, wt = layout.branch("feat/k", worktree="wt-k")
    git(layout.repo, "config", "branch.feat/k.loomKept", "2026-11-23")

    rc, out, err, _calls = run(monkeypatch, layout, "--sweep", cwd=wt)

    assert rc == 0, err
    assert any(line.startswith("kept feat/k ") for line in out.splitlines()), out


def test_sweep_keptBranchCheckedOutInMain_marksChangeKept(tmp_path: Path, monkeypatch) -> None:
    """Keep landed from the main checkout: sweep there shows the branch on a kept line."""
    layout = Repo(tmp_path)
    layout.branch("feat/k")
    git(layout.repo, "switch", "-q", "feat/k")
    git(layout.repo, "config", "branch.feat/k.loomKept", "2026-11-23")

    rc, out, err, _calls = run(monkeypatch, layout, "--sweep")

    assert rc == 0, err
    assert any(line.startswith("kept feat/k ") for line in out.splitlines()), out
