"""Adversary probe: in-scope spellings that still reach main past the agent hook.

Each command is a plain shell spelling of Acceptance 1 or 3 (no `sh -c`,
`eval`, script, function or alias) run from a feature worktree, in a
repository with no native git hooks.
"""
# concern: under-blocking — a cd/subshell or push-refspec spelling commits or pushes to main without the refusal.
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
CHECKER = ROOT / "loom-code" / "scripts" / "loom_checker.py"
REFUSAL = "direct git merge, commit, or push on main/master is blocked"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True, text=True)


def _pair(tmp_path: Path) -> tuple[Path, Path]:
    """A repo on main with a linked worktree `wt` on `feature`; no native hooks."""
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", "main")
    _git(repo, "-c", "user.name=T", "-c", "user.email=t@example.com",
         "commit", "-q", "--allow-empty", "-m", "initial")
    _git(repo, "worktree", "add", "-q", "-b", "feature", str(tmp_path / "wt"))
    return repo, tmp_path / "wt"


def _hook(cwd: Path, command: str) -> subprocess.CompletedProcess:
    return subprocess.run([sys.executable, str(CHECKER), "push", "--hook"],
                          input=json.dumps({"cwd": str(cwd), "tool_name": "Bash",
                                            "tool_input": {"command": command}}),
                          capture_output=True, text=True, cwd=cwd, timeout=30)


@pytest.mark.parametrize("command", [
    "(cd ../repo && git commit -m change)",
    "(cd {repo} && git merge feature)",
])
def test_main_guard_subshell_cd_to_main_denied(tmp_path, command):
    """A subshell that enters the main checkout commits or merges on main."""
    repo, feature = _pair(tmp_path)
    result = _hook(feature, command.format(repo=repo))
    assert result.returncode == 2 and REFUSAL in result.stderr, result.stderr


@pytest.mark.parametrize("command", [
    "cd missing; cd {repo} && git commit -m change",
    "cd -; cd {repo} && git commit -m change",
])
def test_main_guard_absolute_cd_after_unresolved_cd_denied(tmp_path, command):
    """An absolute `cd <main checkout>` resolves on its own, whatever came before it."""
    repo, feature = _pair(tmp_path)
    result = _hook(feature, command.format(repo=repo))
    assert result.returncode == 2 and REFUSAL in result.stderr, result.stderr


def test_main_guard_push_dwim_heads_main_denied(tmp_path):
    """Git resolves the destination `heads/main` to refs/heads/main on the remote."""
    _repo, feature = _pair(tmp_path)
    result = _hook(feature, "git push origin HEAD:heads/main")
    assert result.returncode == 2 and REFUSAL in result.stderr, result.stderr
