"""loom-design's tests live in `loom-design/tests/`, apart from the code they test.

A pytest file left in `loom-design/scripts/` or anywhere under
`loom-design/skills/` is outside the folder the package suite discovers, so it
would either stop running or ship inside a skill as if it were runtime code.
"""
from __future__ import annotations

from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]


def _stray_tests(plugin: Path) -> list[str]:
    """Pytest files under `scripts/` or `skills/` of a loom-design tree."""
    return sorted(
        path.relative_to(plugin).as_posix()
        for folder in (plugin / "scripts", plugin / "skills")
        for path in folder.rglob("test_*.py")
    )


def test_scripts_and_skills_hold_no_tests() -> None:
    assert _stray_tests(PLUGIN) == []


def test_stray_design_test_is_detected(tmp_path: Path) -> None:
    station_test = tmp_path / "scripts" / "interface" / "test_stray.py"
    station_test.parent.mkdir(parents=True)
    station_test.write_text("")
    skill_test = tmp_path / "skills" / "write-spec" / "test_stray.py"
    skill_test.parent.mkdir(parents=True)
    skill_test.write_text("")
    assert _stray_tests(tmp_path) == [
        "scripts/interface/test_stray.py",
        "skills/write-spec/test_stray.py",
    ]
