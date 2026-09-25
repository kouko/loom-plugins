"""Regression eval for the PostToolUse:Write|Edit validate-skill-folder-structure.sh
hook: a flat skill passes (exit 0), a nested subfolder is blocked (exit 2)."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "validate-skill-folder-structure.sh"

# A local checkout without jq skips; under CI a missing jq runs and fails.
pytestmark = pytest.mark.skipif(
    shutil.which("jq") is None and not os.environ.get("CI"),
    reason="hook reads stdin via jq",
)


def _make_skill(tmp_path: Path) -> Path:
    skill = tmp_path / "skills" / "x"
    (skill / "assets").mkdir(parents=True)
    (skill / "SKILL.md").write_text("# x\n")
    (skill / "assets" / "f.md").write_text("flat\n")
    return skill


def _run(tmp_path: Path, file_path: Path) -> subprocess.CompletedProcess:
    event = {"tool_name": "Write", "tool_input": {"file_path": str(file_path)}}
    # cwd outside any git repo, so the repo-level dedup skip cannot fire.
    return subprocess.run(
        ["bash", str(SCRIPT)], input=json.dumps(event),
        capture_output=True, text=True, cwd=tmp_path,
    )


def test_flat_skill_passes(tmp_path):
    skill = _make_skill(tmp_path)
    result = _run(tmp_path, skill / "assets" / "f.md")
    assert result.returncode == 0, result.stderr
    assert result.stderr == ""


def test_nested_subfolder_is_blocked(tmp_path):
    skill = _make_skill(tmp_path)
    nested = skill / "assets" / "sub" / "f.md"
    nested.parent.mkdir()
    nested.write_text("nested\n")
    result = _run(tmp_path, nested)
    assert result.returncode == 2
    assert "Skill folder structure violation" in result.stderr
    assert "assets/sub" in result.stderr
