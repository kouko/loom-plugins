"""Behavioral tests for loom-workflow's host memory reminder hook.

`hooks/memory-mirror-reminder` reads a Claude Code PostToolUse payload and,
when a Write or Edit landed on a host auto-memory note, prints one JSON
reminder to classify it with loom-memory. Path-only: it never reads the note.
"""
# concern: path-matching boundary and fail-open defects in the host memory reminder hook
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN = Path(__file__).resolve().parents[2]
REPO = PLUGIN.parent
HOOK = PLUGIN / "hooks" / "memory-mirror-reminder"
NOTE_DIR = "/home/u/.claude/projects/-home-u-repo/memory"


def run(stdin: str, env_extra: dict | None = None) -> subprocess.CompletedProcess[str]:
    env = {k: v for k, v in os.environ.items() if k != "CLAUDE_CONFIG_DIR"}
    env.update(env_extra or {})
    return subprocess.run([sys.executable, str(HOOK)], input=stdin,
                          capture_output=True, text=True, env=env)


def payload(path: str, tool: str = "Write") -> str:
    return json.dumps({"hook_event_name": "PostToolUse", "tool_name": tool,
                       "tool_input": {"file_path": path}})


def reminder(proc) -> str:
    assert proc.returncode == 0
    out = json.loads(proc.stdout)
    spec = out["hookSpecificOutput"]
    assert spec["hookEventName"] == "PostToolUse"
    return spec["additionalContext"]


@pytest.mark.parametrize("body", [
    "---\ntype: feedback\n---\nx", "---\ntype: project\n---\nx",
    "---\ntype: user\n---\nx", "no frontmatter at all",
])
def test_any_note_type_reminds(tmp_path, body):
    d = tmp_path / ".claude" / "projects" / "-x-repo" / "memory"
    d.mkdir(parents=True)
    note = d / "note.md"
    note.write_text(body, encoding="utf-8")
    assert "loom-memory" in reminder(run(payload(str(note))))


@pytest.mark.parametrize("stdin", [
    "", "not json", "[]", "{}", json.dumps({"tool_input": {}}),
    json.dumps({"tool_input": "x"}), json.dumps({"tool_input": {"file_path": 3}}),
    payload("/repo/README.md"), payload(NOTE_DIR + "/note.txt"),
    payload("/home/u/.claude/projects/-r/memory/sub/note.md"),
    payload("/home/u/docs/loom/memory/note.md"),
])
def test_non_memory_or_malformed_silent(stdin):
    proc = run(stdin)
    assert (proc.returncode, proc.stdout) == (0, "")


def _post_tool_commands(path: Path) -> list[str]:
    hooks = json.loads(path.read_text(encoding="utf-8")).get("hooks", {})
    return [h.get("command", "") for entry in hooks.get("PostToolUse", [])
            if entry.get("matcher") == "Write|Edit" for h in entry.get("hooks", [])]


def test_claude_hooks_wired():
    cmds = _post_tool_commands(PLUGIN / "hooks" / "hooks.json")
    assert '"${CLAUDE_PLUGIN_ROOT}/hooks/memory-mirror-reminder"' in cmds
    assert any("validate-skill-folder-structure.sh" in c for c in cmds)
    assert os.access(HOOK, os.X_OK)


def test_codex_hooks_unwired():
    for rel in ("hooks/hooks-codex.json", "hooks/hooks-opencode.json", "hooks.json"):
        p = PLUGIN / rel
        if p.exists():
            assert "memory-mirror-reminder" not in p.read_text(encoding="utf-8"), rel


def test_reminder_names_finalize_deferral():
    text = reminder(run(payload(NOTE_DIR + "/a.md")))
    assert "finalize-review" in text and "attestation" in text
    assert "next change" in text
    assert "docs/" not in text


def test_index_write_silent():
    proc = run(payload(NOTE_DIR + "/MEMORY.md"))
    assert (proc.returncode, proc.stdout) == (0, "")


def test_orphan_files_absent():
    assert not (REPO / ".claude/hooks/remind-memory-mirror.sh").exists()
    assert not (REPO / "tests/hooks/test_remind_memory_mirror.py").exists()
    files = subprocess.run(["git", "grep", "-l", "-e", "remind-memory-mirror",
                            "-e", "remind_memory_mirror"], cwd=REPO,
                           capture_output=True, text=True).stdout.split()
    stray = [f for f in files if not f.startswith("docs/")
             and not f.endswith("CHANGELOG.md") and f != Path(__file__).relative_to(REPO).as_posix()]
    assert stray == []


def test_fixture_neutral_name():
    text = (REPO / "tests/test_tests_folder_convention.py").read_text(encoding="utf-8")
    assert "remind_memory_mirror" not in text


def test_removed_test_coverage_widened(tmp_path):
    config = tmp_path / "cfg"
    assert reminder(run(payload(str(config / "projects/-r/memory/n.md")),
                        {"CLAUDE_CONFIG_DIR": str(config)}))
    assert reminder(run(payload(NOTE_DIR + "/n.md", tool="Edit")))
    # Nonexistent note: path-only, still reminds without crashing.
    assert reminder(run(payload(NOTE_DIR + "/missing.md")))
    unreadable = tmp_path / ".claude/projects/-r/memory/locked.md"
    unreadable.parent.mkdir(parents=True)
    unreadable.write_text("x", encoding="utf-8")
    unreadable.chmod(0)
    try:
        assert reminder(run(payload(str(unreadable))))
    finally:
        unreadable.chmod(0o600)
