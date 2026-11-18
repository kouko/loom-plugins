# concern: missed violation - a write to a nested skill path gets no message from the plugin hook (Acceptance 2)
"""Every write to a nested skill path must report the violation at once."""
from __future__ import annotations

import json
import os
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
HOOK = REPO / "loom-workflow" / "scripts" / "validate-skill-folder-structure.sh"

pytestmark = pytest.mark.skipif(
    shutil.which("jq") is None and not os.environ.get("CI"),
    reason="hook reads stdin via jq",
)


def _write(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("x\n", encoding="utf-8")


def _run_hook(file_path: Path) -> subprocess.CompletedProcess:
    event = {"tool_name": "Write", "tool_input": {"file_path": str(file_path)}}
    return subprocess.run(
        ["bash", str(HOOK)], input=json.dumps(event),
        capture_output=True, text=True, cwd=REPO,
    )


def test_hook_nested_write_before_skill_md_reports_violation(tmp_path):
    """A new skill's first file can already be nested."""
    nested = tmp_path / "plugin" / "skills" / "new" / "assets" / "sub" / "f.md"
    _write(nested)

    result = _run_hook(nested)

    assert result.returncode == 2, result.stderr
    assert "Skill folder structure violation" in result.stderr


def test_hook_nested_folder_with_newline_reports_violation(tmp_path):
    """A line break in a nested folder name must not hide the skill root."""
    skill = tmp_path / "plugin" / "skills" / "x"
    _write(skill / "SKILL.md")
    nested = skill / "assets" / "sub\nfolder" / "f.md"
    _write(nested)

    result = _run_hook(nested)

    assert result.returncode == 2, result.stderr
    assert "Skill folder structure violation" in result.stderr


def test_hook_nested_folder_named_skills_reports_violation(tmp_path):
    """A nested folder called `skills` must not hide the real skill root."""
    skill = tmp_path / "plugin" / "skills" / "x"
    _write(skill / "SKILL.md")
    nested = skill / "references" / "skills" / "y" / "f.md"
    _write(nested)

    result = _run_hook(nested)

    assert result.returncode == 2, result.stderr
    assert "Skill folder structure violation" in result.stderr
