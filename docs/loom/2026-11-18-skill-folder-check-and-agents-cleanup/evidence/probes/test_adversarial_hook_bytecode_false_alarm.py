# concern: false alarm - with the repo-level hook gone, the plugin hook reports ignored bytecode caches as skill violations here
"""A flat skill whose script was run must not be reported as nested."""
from __future__ import annotations

import json
import os
import py_compile
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


def test_hook_flat_edit_with_bytecode_cache_reports_nothing(tmp_path):
    """Editing SKILL.md stays silent when only `scripts/__pycache__` exists."""
    skill = tmp_path / "plugin" / "skills" / "x"
    script = skill / "scripts" / "tool.py"
    script.parent.mkdir(parents=True)
    script.write_text("VALUE = 1\n", encoding="utf-8")
    (skill / "SKILL.md").write_text("# x\n", encoding="utf-8")
    py_compile.compile(
        str(script), cfile=str(script.parent / "__pycache__" / "tool.pyc")
    )
    event = {"tool_name": "Edit", "tool_input": {"file_path": str(skill / "SKILL.md")}}

    result = subprocess.run(
        ["bash", str(HOOK)], input=json.dumps(event),
        capture_output=True, text=True, cwd=REPO,
    )

    assert result.returncode == 0, result.stderr
    assert result.stderr == ""
