"""Direct main-branch Git mutation guard in the shared PreToolUse handler."""
# concern: direct main/master Git mutations can pass through the shared shell hook.
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest


CHECKER = Path(__file__).resolve().parents[1] / "scripts" / "loom_checker.py"


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True,
                   capture_output=True, text=True)


def _repo(tmp_path: Path, branch: str = "main") -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    _git(repo, "init", "-q", "-b", branch)
    _git(repo, "-c", "user.name=T", "-c", "user.email=t@example.com",
         "commit", "-q", "--allow-empty", "-m", "initial")
    return repo


def _hook(cwd: Path, command: str):
    return subprocess.run([sys.executable, str(CHECKER), "push", "--hook"],
                          input=json.dumps({"cwd": str(cwd), "tool_name": "Bash",
                                            "tool_input": {"command": command}}),
                          capture_output=True, text=True, cwd=cwd, timeout=30)


@pytest.mark.parametrize("branch", ["main", "master"])
@pytest.mark.parametrize("command", [
    "git merge feature", "git commit -m change", "git push origin HEAD",
    "git commit -m 'cost $5 | review'", "git commit -m change && echo done",
    "git push origin HEAD; echo done", "true; git commit -m change",
    "cd . && git push origin main",
])
def test_direct_git_mutation_denied_on_main_branches(tmp_path, branch, command):
    repo = _repo(tmp_path, branch)
    result = _hook(repo, command)
    assert result.returncode == 2
    assert "main/master" in result.stderr
    assert "feature branch or worktree" in result.stderr
    assert "protectMain=false" not in result.stderr
    assert result.stdout == ""


@pytest.mark.parametrize("command", ["git merge feature", "git commit -m change", "git push origin HEAD"])
def test_feature_branch_allows_git_mutation(tmp_path, command):
    repo = _repo(tmp_path)
    _git(repo, "switch", "-q", "-c", "feature")
    assert _hook(repo, command).returncode == 0


def _pair(tmp_path: Path) -> tuple[Path, Path]:
    """A repo on main and a linked worktree on `feature`; no native hooks."""
    repo = _repo(tmp_path)
    feature = tmp_path / "wt"
    _git(repo, "worktree", "add", "-q", "-b", "feature", str(feature))
    return repo, feature


@pytest.mark.parametrize("command", [
    "cd ../repo && git commit -m change",                 # cd-main-commit-denied
    "cd {repo} && FOO=1 git commit -m change",
    "git -C ../repo merge feature",                       # git-C-main-merge-denied
    "git -c core.pager=cat -C .. -C repo commit -m change",
    "git push origin HEAD:main",                          # feature-push-head-to-main-denied
    "git push origin +HEAD:refs/heads/master", "git push origin main",
    "git push origin --delete main", "echo ok; git push -u origin HEAD:master",
])
def test_main_spellings_from_feature_worktree_denied(tmp_path, command):
    repo, feature = _pair(tmp_path)
    assert not (repo / ".git" / "hooks" / "pre-commit").exists()  # no-native-hooks-repo-denies
    result = _hook(feature, command.format(repo=repo))
    assert result.returncode == 2, result.stderr
    assert "direct git merge, commit, or push on main/master is blocked" in result.stderr


@pytest.mark.parametrize("command", [
    "cd ../wt && git commit -m change",                   # cd-feature-commit-allowed
    "git -C ../wt commit -m change",                      # git-C-feature-commit-allowed
    "cd ../wt && git push origin HEAD:feature",           # feature-push-to-feature-allowed
    "cd ../wt && git push origin refs/tags/v1",
    "cd missing && git commit -m change",
])
def test_feature_targets_from_main_allowed(tmp_path, command):
    repo, _feature = _pair(tmp_path)
    assert _hook(repo, command).returncode == 0


def test_opt_out_allows_cd_main_commit(tmp_path):
    repo, feature = _pair(tmp_path)
    _git(repo, "config", "--local", "loom.protectMain", "false")
    assert _hook(feature, "cd ../repo && git commit -m change").returncode == 0


@pytest.mark.parametrize("command", ["bash -c 'git push origin main'",
                                     "sh -c 'cd ../repo && git commit -m change'"])
def test_shell_wrappers_stay_outside_guard(tmp_path, command):
    _main, feature = _pair(tmp_path)
    assert _hook(feature, command).returncode == 0


def test_non_git_and_detached_head_allow_ordinary_command(tmp_path):
    non_git = tmp_path / "plain"
    non_git.mkdir()
    assert _hook(non_git, "ls").returncode == 0
    repo = _repo(tmp_path)
    _git(repo, "checkout", "-q", "--detach")
    assert _hook(repo, "ls").returncode == 0


def test_repo_local_opt_out_allows_main_branch(tmp_path):
    repo = _repo(tmp_path)
    _git(repo, "config", "--local", "loom.protectMain", "false")
    assert _hook(repo, "git commit -m change").returncode == 0


def test_pr_merge_keeps_reminder_policy_on_main(tmp_path):
    repo = _repo(tmp_path)
    result = _hook(repo, "gh pr merge 12 --squash")
    assert result.returncode == 0
    assert "merging anyway." in result.stderr
