"""loom-workflow's tests live in `loom-workflow/tests/`, apart from the code they test.

A pytest file left under `loom-workflow/skills/`, `loom-workflow/scripts/` or
`loom-workflow/.claude-plugin/` is outside the folder the package suite
discovers, so it would either stop running or ship inside a skill as if it were
runtime code.
"""
from __future__ import annotations

from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]


def _stray_tests(plugin: Path) -> list[str]:
    """Pytest files under `skills/`, `scripts/` or `.claude-plugin/` of a loom-workflow tree."""
    return sorted(
        path.relative_to(plugin).as_posix()
        for folder in (plugin / "skills", plugin / "scripts", plugin / ".claude-plugin")
        for path in folder.rglob("test_*.py")
    )


def test_skills_scripts_and_manifest_folder_hold_no_tests() -> None:
    assert _stray_tests(PLUGIN) == []


def test_stray_workflow_test_is_detected(tmp_path: Path) -> None:
    strays = [
        tmp_path / "skills" / "handoff" / "scripts" / "test_stray.py",
        tmp_path / "scripts" / "test_stray.py",
        tmp_path / ".claude-plugin" / "test_stray.py",
    ]
    for stray in strays:
        stray.parent.mkdir(parents=True, exist_ok=True)
        stray.write_text("")
    assert _stray_tests(tmp_path) == [
        ".claude-plugin/test_stray.py",
        "scripts/test_stray.py",
        "skills/handoff/scripts/test_stray.py",
    ]
