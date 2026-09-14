"""PreToolUse guard over the selection record store (plan W2-02; Acceptance 2).

Spec decisions 3 and 17 of 2026-09-14-expert-mode-step-selection: the
PreToolUse hook on both hosts denies a Bash command that names the capture
command or the record store, or names a git-dir or bare `selections/` path
together with a recognised write form, and denies a file-writing tool call
whose target resolves under `<git common dir>/loom/`. Everything else passes.
Disguised commands are outside the local guarantee (intent Constraints).
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from loom_checker.rule_checks import selection_guard

SCRIPTS = Path(__file__).resolve().parent
PLUGIN_ROOT = SCRIPTS.parent
CHECKER = SCRIPTS / "loom_checker.py"
HOOKS = PLUGIN_ROOT / "hooks"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(cwd), *args], capture_output=True, text=True, check=True
    ).stdout.strip()


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    git(repo, "init", "-q", "-b", "main")
    git(repo, "config", "user.email", "t@example.com")
    git(repo, "config", "user.name", "T")
    (repo / "base.txt").write_text("base", encoding="utf-8")
    git(repo, "add", "base.txt")
    git(repo, "commit", "-q", "-m", "base")
    return repo


# --- Bash text rule --------------------------------------------------------

DENIED_COMMANDS = [
    # the capture command and the store itself, whatever the verb
    "python3 loom-code/scripts/loom_checker.py selection capture --hook < p.json",
    "echo '{}' >> .git/loom/selections/c.jsonl",
    "ls .git/loom",
    'cat x >> "$(git rev-parse --git-common-dir)/loom/selections/c.jsonl"',
    # relative-path record writes
    'cd "$(git rev-parse --git-common-dir)/loom" && echo x >> selections/c.jsonl',
    "cd ../../loom && tee -a selections/c.jsonl < ev.json",
    # a bare selections/ write counts only next to a loom or .git name
    "cd ../../loom && mv /tmp/forged.jsonl selections/c.jsonl",
    "cd ../../loom && cp forged.jsonl ./selections/c.jsonl",
    "cd ../../loom && dd if=forged of=selections/c.jsonl",
    "cd ../../loom && install -m 644 forged selections/c.jsonl",
    "cd ../../loom && sed -i '$d' selections/c.jsonl",
    "cd ../../loom && perl -pi -e 's/a/b/' selections/c.jsonl",
    "cd .git && cd loom && echo x >> selections/a.jsonl",
    # rev-parse / git-dir record writes
    'd=$(git rev-parse --git-common-dir); printf x > "$d/loom/s/c.jsonl"',
    'git rev-parse --git-dir | xargs -I{} cp forged {}/loom/x',
    'GIT_DIR=$(pwd)/.git; tee "$GIT_DIR/loom/x" < ev',
    "python3 -c \"import subprocess; subprocess.run(['git','rev-parse','--git-common-dir'])\"",
    "uv run python -c 'import os' --git-dir",
    'node -e "require(\'fs\').appendFileSync(process.env.GIT_DIR)"',
    "ruby -e 'File.write(ENV[\"GIT_DIR\"], 1)'",
    "sed -i.bak s/a/b/ $(git rev-parse --git-common-dir)/loom/x",
    "bash -c 'cd ../loom && cp forged selections/c.jsonl'",
    # the capture command run by the checker program, however it is launched
    "python3 -m loom_checker selection capture --hook",
    "bash -c 'python3 x/loom_checker.py selection capture --hook < p'",
    # a nested host session whose prompt would fire the capture hook
    'claude -p "/loom-code:expert-mode K7Q2"',
    'codex exec "$expert-mode K7Q2"',
    "env FOO=1 claude -p '/expert-mode K7Q2'",
    "exec claude -p '$loom-code:expert-mode K7Q2'",
    "echo '/expert-mode K7Q2' | xargs claude -p",
    "bash -c 'claude -p \"/expert-mode K7Q2\"'",
    "/usr/local/bin/codex exec '/loom-code:expert-mode K7Q2'",
]


@pytest.mark.parametrize("command", DENIED_COMMANDS)
def test_recognised_record_writes_are_denied(command):
    assert selection_guard.bash_guard_reason(command), command


ALLOWED_COMMANDS = [
    "ls models/selections/",
    "pytest tests/selections/",
    "pytest tests/selections/ -k install",
    "cat selections/readme.md",
    "python3 loom-code/scripts/loom_checker.py selection cancel 2026-09-14-x",
    "python3 loom-code/scripts/loom_checker.py selection show 2026-09-14-x",
    "python3 loom-code/scripts/loom_checker.py selection propose c --origin user --skip reviewers",
    "python3 loom-code/scripts/loom_checker.py selection record-failure c --step review --rule r",
    "git rev-parse --git-common-dir",
    "git rev-parse --git-dir 2>/dev/null",
    "git rev-parse --git-dir >/dev/null 2>&1",
    "echo hi > out.txt",
    "git status --short",
    "git push origin HEAD",
    # an application directory that merely ends in selections/
    "echo cfg > app/selections/config.json",
    "cp defaults.json app/selections/config.json",
    # the capture words read or written as text, not run by the checker
    'rg "selection capture" loom-code',
    'git commit -m "fix selection capture race"',
    # a host program with no entry-point token, or the token with no host
    "claude --version",
    "codex --help",
    "rg expert-mode loom-code",
    'git commit -m "expert-mode docs"',
]


@pytest.mark.parametrize("command", ALLOWED_COMMANDS)
def test_ordinary_commands_pass(command):
    assert selection_guard.bash_guard_reason(command) is None, command


# --- Bash working directory ------------------------------------------------

def bash_payload(cwd: Path, command: str) -> dict:
    return {"tool_name": "Bash", "cwd": str(cwd), "tool_input": {"command": command}}


def test_write_from_cwd_inside_loom_dir_is_denied(repo: Path):
    """The Bash tool keeps its cwd: an earlier `cd` into the store must not
    let a later relative write pass."""
    loom = repo / ".git" / "loom"
    (loom / "selections").mkdir(parents=True)
    assert selection_guard.guard_reason(bash_payload(loom, "mv x selections/c.jsonl"))
    assert selection_guard.guard_reason(bash_payload(loom / "selections", "cp x c.jsonl"))


def test_read_from_cwd_inside_loom_dir_passes(repo: Path):
    loom = repo / ".git" / "loom"
    (loom / "selections").mkdir(parents=True)
    assert selection_guard.guard_reason(bash_payload(loom, "ls selections/")) is None


def test_write_from_ordinary_repo_cwd_passes(repo: Path):
    assert selection_guard.guard_reason(bash_payload(repo, "mv x app/selections/c.json")) is None


# --- file-writing tools ----------------------------------------------------

def test_relative_write_under_common_dir_loom_is_denied(repo: Path):
    payload = {"tool_name": "Write", "cwd": str(repo),
               "tool_input": {"file_path": ".git/loom/selections/c.jsonl", "content": "{}"}}
    assert selection_guard.guard_reason(payload)


@pytest.mark.parametrize("tool, key", [
    ("Write", "file_path"), ("Edit", "file_path"),
    ("MultiEdit", "file_path"), ("NotebookEdit", "notebook_path"),
])
def test_every_claude_file_tool_is_guarded(repo: Path, tool: str, key: str):
    target = repo / ".git" / "loom" / "selections" / "c.jsonl"
    payload = {"tool_name": tool, "cwd": str(repo), "tool_input": {key: str(target)}}
    assert selection_guard.guard_reason(payload)


def test_write_resolved_through_separate_git_dir_is_denied(tmp_path: Path):
    """The target names no `.git/loom` text: only resolving the common dir
    catches it."""
    work, gitdir = tmp_path / "work", tmp_path / "store"
    subprocess.run(["git", "init", "-q", f"--separate-git-dir={gitdir}", str(work)],
                   check=True, capture_output=True)
    payload = {"tool_name": "Edit", "cwd": str(work),
               "tool_input": {"file_path": str(gitdir / "loom" / "x.jsonl")}}
    assert selection_guard.guard_reason(payload)


def test_worktree_write_to_main_common_dir_is_denied(repo: Path, tmp_path: Path):
    worktree = tmp_path / "wt"
    git(repo, "worktree", "add", "-q", "-b", "feature", str(worktree))
    relative = os.path.relpath(repo / ".git" / "loom" / "selections" / "c.jsonl", worktree)
    payload = {"tool_name": "Write", "cwd": str(worktree), "tool_input": {"file_path": relative}}
    assert selection_guard.guard_reason(payload)


def test_codex_apply_patch_headers_are_guarded(repo: Path):
    for header in ("Add File", "Update File", "Delete File"):
        patch = f"*** Begin Patch\n*** {header}: .git/loom/selections/c.jsonl\n+{{}}\n*** End Patch\n"
        payload = {"tool_name": "apply_patch", "cwd": str(repo), "tool_input": {"command": patch}}
        assert selection_guard.guard_reason(payload), header


def test_ordinary_file_writes_pass(repo: Path):
    patch = "*** Begin Patch\n*** Add File: models/selections/x.sql\n+select 1\n*** End Patch\n"
    for payload in (
        {"tool_name": "apply_patch", "cwd": str(repo), "tool_input": {"command": patch}},
        {"tool_name": "Write", "cwd": str(repo), "tool_input": {"file_path": "src/app.py"}},
        {"tool_name": "Edit", "cwd": str(repo), "tool_input": {"file_path": str(repo / ".git" / "config")}},
    ):
        assert selection_guard.guard_reason(payload) is None, payload


# --- hook wiring -----------------------------------------------------------

def run_hook(payload: dict, cwd: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(CHECKER), "push", "--hook"],
        input=json.dumps(payload), capture_output=True, text=True, cwd=str(cwd),
    )


def test_push_hook_denies_with_one_block_line(repo: Path):
    result = run_hook({"hook_event_name": "PreToolUse", "tool_name": "Bash", "cwd": str(repo),
                       "tool_input": {"command": "echo x >> .git/loom/selections/c.jsonl"}}, repo)
    assert result.returncode == 2
    lines = result.stderr.strip().splitlines()
    assert len(lines) == 1 and lines[0].startswith("BLOCK selection.guard: ")


def test_push_hook_denies_file_tool_write(repo: Path):
    result = run_hook({"hook_event_name": "PreToolUse", "tool_name": "Write", "cwd": str(repo),
                       "tool_input": {"file_path": ".git/loom/selections/c.jsonl"}}, repo)
    assert result.returncode == 2
    assert result.stderr.startswith("BLOCK selection.guard: ")


@pytest.mark.parametrize("payload", [
    {"tool_name": "Bash", "tool_input": {"command": "ls models/selections/"}},
    {"tool_name": "Bash", "tool_input": {"command": "python3 x/loom_checker.py selection cancel c"}},
    {"tool_name": "Write", "tool_input": {"file_path": "src/app.py", "content": "git push"}},
    {"tool_name": "apply_patch", "tool_input": {"command": "*** Update File: a.py\n+git push origin HEAD\n"}},
])
def test_push_hook_passes_unguarded_non_push_calls(repo: Path, payload: dict):
    result = run_hook({"hook_event_name": "PreToolUse", "cwd": str(repo), **payload}, repo)
    assert result.returncode == 0, result.stderr


def test_claude_matcher_covers_bash_and_file_tools():
    hooks = json.loads((HOOKS / "hooks.json").read_text(encoding="utf-8"))["hooks"]
    (entry,) = hooks["PreToolUse"]
    assert entry["matcher"] == "Bash|Write|Edit|MultiEdit|NotebookEdit"


def codex_file_tool_entry() -> dict:
    hooks = json.loads((HOOKS / "hooks-codex.json").read_text(encoding="utf-8"))["hooks"]
    assert hooks["PreToolUse"][0]["matcher"] == "Bash"
    (entry,) = [e for e in hooks["PreToolUse"] if e["matcher"] != "Bash"]
    return entry


def test_codex_matcher_covers_apply_patch():
    assert set(codex_file_tool_entry()["matcher"].split("|")) == {"apply_patch", "Edit", "Write"}


def test_codex_file_tool_hook_delegates_to_checker_and_passes_when_missing(tmp_path: Path):
    (hook,) = codex_file_tool_entry()["hooks"]
    payload = json.dumps({"tool_name": "apply_patch",
                          "tool_input": {"command": "*** Add File: .git/loom/x\n"}})
    installed = tmp_path / "installed" / "scripts"
    installed.mkdir(parents=True)
    (installed / "loom_checker.py").write_text(
        "import sys\nsys.stdin.read()\nprint(sys.argv[1:])\nraise SystemExit(2)\n", encoding="utf-8")
    delegated = subprocess.run(hook["command"], shell=True, input=payload, text=True,
                               capture_output=True,
                               env=dict(os.environ, PLUGIN_ROOT=str(installed.parent)))
    assert delegated.returncode == 2 and "'push', '--hook'" in delegated.stdout
    missing = subprocess.run(hook["command"], shell=True, input=payload, text=True,
                             capture_output=True,
                             env=dict(os.environ, PLUGIN_ROOT=str(tmp_path / "gone")))
    assert missing.returncode == 0
