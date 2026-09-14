"""Tests for detect_client.py (client check and Obsidian vault boundary)."""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import detect_client  # noqa: E402

SCRIPT = Path(__file__).resolve().parent / "detect_client.py"
KEYS = {"client", "mermaid", "remote_viewer", "obsidian_vault", "reason"}


def test_claude_code_cli_env_mermaid_false():
    result = detect_client.detect({"CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "cli"})
    assert result["client"] == "claude-code-cli"
    assert result["mermaid"] is False
    assert result["remote_viewer"] is False
    assert result["obsidian_vault"] is None


def test_claude_code_missing_entrypoint_is_unknown_suffix():
    result = detect_client.detect({"CLAUDECODE": "1"})
    assert result["client"] == "claude-code-unknown"
    assert result["mermaid"] is False


def test_unrecognised_env_falls_back_table_ascii():
    result = detect_client.detect({})
    assert result["client"] == "unknown"
    assert result["mermaid"] is False
    assert result["remote_viewer"] is False
    assert set(result) == KEYS


def test_codex_env_detected_by_each_marker():
    for var in ("CODEX_THREAD_ID", "CODEX_SANDBOX", "CODEX_CI"):
        result = detect_client.detect({var: "x"})
        assert result["client"] == "codex", var
        assert result["mermaid"] is False


def test_gemini_cli_env():
    result = detect_client.detect({"GEMINI_CLI": "1"})
    assert result["client"] == "gemini-cli"
    assert result["mermaid"] is False


def test_remote_viewer_from_bridge_session():
    env = {"CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "cli",
           "CLAUDE_CODE_BRIDGE_SESSION_ID": "abc"}
    result = detect_client.detect(env)
    assert result["remote_viewer"] is True
    assert result["mermaid"] is False


def test_remote_viewer_from_remote_entrypoint():
    result = detect_client.detect({"CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "remote_mobile"})
    assert result["client"] == "claude-code-remote_mobile"
    assert result["remote_viewer"] is True


def test_target_under_dot_obsidian_reports_vault(tmp_path):
    vault = tmp_path / "vault"
    (vault / ".obsidian").mkdir(parents=True)
    note_dir = vault / "notes" / "deep"
    note_dir.mkdir(parents=True)
    result = detect_client.detect({}, target=str(note_dir / "note.md"))
    assert result["obsidian_vault"] is True


def test_nonexistent_target_inside_vault_reports_vault(tmp_path):
    vault = tmp_path / "vault"
    (vault / ".obsidian").mkdir(parents=True)
    result = detect_client.detect({}, target=str(vault / "missing" / "dir" / "note.md"))
    assert result["obsidian_vault"] is True


def test_plain_repo_path_not_vault(tmp_path):
    repo = tmp_path / "repo"
    (repo / "docs").mkdir(parents=True)
    result = detect_client.detect({}, target=str(repo / "docs" / "out.md"))
    assert result["obsidian_vault"] is False


def test_obsidian_file_not_directory_is_not_vault(tmp_path):
    (tmp_path / ".obsidian").write_text("not a dir")
    result = detect_client.detect({}, target=str(tmp_path / "note.md"))
    assert result["obsidian_vault"] is False


def test_cli_prints_one_json_object(tmp_path):
    (tmp_path / ".obsidian").mkdir()
    env = {"PATH": "/usr/bin:/bin", "CLAUDECODE": "1", "CLAUDE_CODE_ENTRYPOINT": "cli"}
    proc = subprocess.run(
        [sys.executable, "-I", str(SCRIPT), "--target", str(tmp_path / "n.md")],
        capture_output=True, text=True, env=env, check=True,
    )
    data = json.loads(proc.stdout)
    assert set(data) == KEYS
    assert data["client"] == "claude-code-cli"
    assert data["mermaid"] is False
    assert data["obsidian_vault"] is True
    assert isinstance(data["reason"], str) and data["reason"]


def test_cli_without_target_reports_null_vault():
    proc = subprocess.run(
        [sys.executable, "-I", str(SCRIPT)],
        capture_output=True, text=True, env={"PATH": "/usr/bin:/bin"}, check=True,
    )
    data = json.loads(proc.stdout)
    assert data["client"] == "unknown"
    assert data["obsidian_vault"] is None
