"""Adversarial probe: does anything still refuse a publication command, or
remind where REQ-12 wants silence?

REQ-4: on every host the publication hook allows any Bash command that
pushes or opens a pull request, including when the checker is missing or
crashes; only the literal first-command shape earns one reminder line.
REQ-12: a command that only mentions the merge words is silent. The attack
runs the real hook commands as each host runs them, as subprocesses, with a
fixture repository and no network.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-22-publication-floor-moves-to-github/evidence/probes/test_abuse_hook_never_refuses.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
CHECKER = ROOT / "loom-code" / "scripts" / "loom_checker.py"
CHANGE = "2026-09-22-example"
PUSH = "git " + "push"            # split so no host hook reads this file as a push
MERGE = "gh pr " + "merge"
CREATE = "gh pr " + "create"


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo), *args], check=True,
                          capture_output=True, text=True).stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "src.py").write_text("V = 1\n", encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "initial")
    git(repo, "switch", "-q", "-c", f"feat/{CHANGE}")
    intent = repo / "docs" / "loom" / "intent" / f"{CHANGE}.md"
    intent.parent.mkdir(parents=True)
    intent.write_text("# Example\n\noriginator: kouko\nstatus: confirmed 2026-09-22\n",
                      encoding="utf-8")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "intent")
    return repo


def hook(repo: Path, command: str) -> subprocess.CompletedProcess:
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": command}, "cwd": str(repo)}
    return subprocess.run([sys.executable, str(CHECKER), "push", "--hook"],
                          input=json.dumps(payload), capture_output=True, text=True,
                          cwd=str(repo))


def claude_code_hook_command() -> str:
    hooks = json.loads((ROOT / "loom-code/hooks/hooks.json").read_text(encoding="utf-8"))
    entry = next(e for e in hooks["hooks"]["PreToolUse"] if "Bash" in e["matcher"])
    return entry["hooks"][0]["command"]


# --- REQ-4: allow ------------------------------------------------------------


def test_hook_direct_push_allowed_with_reminder(repo: Path) -> None:
    result = hook(repo, f"{PUSH} -u origin feat/{CHANGE}")
    assert result.returncode == 0, result.stderr
    assert "loom: verification absent" in result.stderr


@pytest.mark.parametrize("command", [
    f"{CREATE} --title t --body 'selection records live in .git/loom per the spec'",
    f"{PUSH} origin HEAD && {CREATE} --fill --body 'see .git/loom for records'",
])
def test_hook_pr_open_mentioning_store_allowed(repo: Path, command: str) -> None:
    """REQ-4 says any command that opens a pull request is allowed. A PR
    body that merely mentions where loom keeps its records is not a write."""
    result = hook(repo, command)
    assert result.returncode == 0, (
        f"the hook refuses a PR-open command that only mentions the record "
        f"directory: exit {result.returncode}, {result.stderr.strip()!r}")


def test_claude_code_hook_checker_missing_allowed(repo: Path, tmp_path: Path) -> None:
    """REQ-4 on Claude Code with the checker missing (a stale plugin root):
    Claude Code refuses a PreToolUse command that exits 2. The hook command
    must not exit 2 for a push."""
    empty_root = tmp_path / "stale-root"
    empty_root.mkdir()
    payload = {"hook_event_name": "PreToolUse", "tool_name": "Bash",
               "tool_input": {"command": f"{PUSH} -u origin feat/{CHANGE}"}, "cwd": str(repo)}
    env = dict(os.environ, CLAUDE_PLUGIN_ROOT=str(empty_root))
    result = subprocess.run(["sh", "-c", claude_code_hook_command()],
                            input=json.dumps(payload), capture_output=True, text=True,
                            cwd=str(repo), env=env)
    assert result.returncode != 2, (
        f"Claude Code hook with the checker missing exits 2 (refuses the push): "
        f"{result.stderr.strip()!r}")


def test_hook_reminder_crash_allowed(tmp_path: Path) -> None:
    """A reminder that cannot be computed (cwd not a repository) allows."""
    outside = tmp_path / "not-a-repo"
    outside.mkdir()
    result = hook(outside, f"{PUSH} origin main")
    assert result.returncode == 0
    assert "publication hook failed" in result.stderr


# --- REQ-12: silence ----------------------------------------------------------


@pytest.mark.parametrize("command", [
    f'grep -rn "{MERGE}" .',
    f'echo "{MERGE} 12"',
    f'git commit --allow-empty -m "{MERGE} after review"',
    f'git log --grep="{PUSH}"',
    f'# {MERGE}',
    f'true; {MERGE} 12',
    f"bash -c '{PUSH} origin x'",
    f"echo \"$(date) {MERGE}\"",
    f"cat <<EOF\n{MERGE}\nEOF",
])
def test_hook_mention_only_silent(repo: Path, command: str) -> None:
    result = hook(repo, command)
    assert result.returncode == 0, result.stderr
    assert result.stdout == "" and result.stderr == "", (command, result.stdout, result.stderr)
