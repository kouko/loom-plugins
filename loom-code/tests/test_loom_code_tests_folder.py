"""loom-code's tests live in `loom-code/tests/`, apart from the code they test.

A pytest file left in `loom-code/scripts/` or anywhere under
`loom-code/skills/` is outside the folder the package suite discovers, so it
would either stop running or ship inside a skill as if it were runtime code.
"""
from __future__ import annotations

from pathlib import Path

PLUGIN = Path(__file__).resolve().parents[1]


def _stray_tests(plugin: Path) -> list[str]:
    """Pytest files under `scripts/` or `skills/` of a loom-code tree."""
    return sorted(
        path.relative_to(plugin).as_posix()
        for folder in (plugin / "scripts", plugin / "skills")
        for path in folder.rglob("test_*.py")
    )


def test_scripts_and_skills_hold_no_tests() -> None:
    assert _stray_tests(PLUGIN) == []


def test_probe_left_in_skill_is_detected(tmp_path: Path) -> None:
    probe = tmp_path / "skills" / "build" / "probes" / "test_recovery_rules.py"
    probe.parent.mkdir(parents=True)
    probe.write_text("")
    script_test = tmp_path / "scripts" / "test_stray.py"
    script_test.parent.mkdir(parents=True)
    script_test.write_text("")
    assert _stray_tests(tmp_path) == [
        "scripts/test_stray.py",
        "skills/build/probes/test_recovery_rules.py",
    ]
