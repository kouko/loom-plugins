"""Adversary probe: the agent hook must not refuse ordinary feature-branch work.

Each command here starts in the main checkout but its commit or push runs on
a feature branch by the time Git executes it; the 3.89.0 guard allowed every
one of them (Acceptance 4: commit and push on a feature branch still pass).
"""
# concern: over-blocking — a commit or push that lands on a feature branch is refused because the guard judges the branch the agent started on.
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "loom-code" / "scripts" / "loom_checker.py"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _pair(tmp_path: Path) -> Path:
    """A repo on main with a linked worktree `wt` on `feature`; no native hooks."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "-c", "user.name=T", "-c", "user.email=t@example.com",
         "commit", "-q", "--allow-empty", "-m", "initial")
    _git(repo, "worktree", "add", "-q", "-b", "feature", str(tmp_path / "wt"))
    return repo


def _hook(cwd: Path, command: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECKER), "push", "--hook"],
                          input=json.dumps({"cwd": str(cwd), "tool_name": "Bash",
                                            "tool_input": {"command": command}}),
                          capture_output=True, text=True, cwd=cwd, timeout=30)


@pytest.mark.parametrize("command", [
    "git switch -c fix/x && git commit -am msg",
    "git checkout -b fix/x && git commit -am msg",
    "git checkout -b fix/x; git push -u origin HEAD",
])
def test_main_guard_branch_switched_before_commit_allowed(tmp_path, command):
    """Leaving main with switch/checkout -b and then committing is feature-branch work."""
    repo = _pair(tmp_path)
    result = _hook(repo, command)
    assert result.returncode == 0, result.stderr


def test_main_guard_subshell_cd_to_feature_allowed(tmp_path):
    """A subshell that enters the feature worktree commits on the feature branch."""
    repo = _pair(tmp_path)
    result = _hook(repo, "(cd ../wt && git commit -m change)")
    assert result.returncode == 0, result.stderr
