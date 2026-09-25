"""Adversarial probe: a test left where the old suite ran it now vanishes silently.
concern: a test written into a location the package suite used to collect is
neither run by the discovered inventory nor refused by any guard, so it goes
dark with a green suite.

Before the move, `scripts/run_package_tests.py --loom-family` handed pytest the
repository-root `scripts/` and `.claude/hooks/` folders, so a new
`scripts/test_x.py` ran. After the move the inventory discovers only the
`tests/` folders, and the guards that keep tests out of old homes cover
`loom-code/{scripts,skills}`, `loom-design/{scripts,skills}` and
`loom-workflow/{skills,scripts,.claude-plugin}` -- not the repository root.
AGENTS.md states the rule for root `scripts/` (tests must not sit beside
production code) and the intent's Acceptance 1 says no test remains beside
production code, but nothing recomputes it there.

Each case copies the working tree (tracked plus untracked, non-ignored files)
into a temporary git repository, plants a failing pytest file at one of those
old homes, and requires that EITHER the inventory's pytest sessions collect it
OR one of the tests-folder guard modules fails on the planted tree.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


def _repo_root(start: Path) -> Path:
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "scripts" / "run_package_tests.py").is_file() and (
            candidate / "loom-code"
        ).is_dir():
            return candidate
    raise RuntimeError(f"could not locate the repository root above {start}")


REPO = _repo_root(Path(__file__).parent)

GUARDS = [
    "tests/test_tests_folder_convention.py",
    "loom-code/tests/test_loom_code_tests_folder.py",
    "loom-design/tests/test_loom_design_tests_folder.py",
    "loom-workflow/tests/test_loom_workflow_tests_folder.py",
]

STRAY_BODY = "def test_planted_stray_probe():\n    assert False\n"

LIST_COMMANDS = (
    "import json, sys, importlib.util\n"
    "from pathlib import Path\n"
    "spec = importlib.util.spec_from_file_location('rpt', 'scripts/run_package_tests.py')\n"
    "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)\n"
    "print(json.dumps(m.loom_family_commands(Path.cwd(), '-q')))\n"
)


def _copy_tree(dest: Path) -> None:
    listed = subprocess.run(
        ["git", "ls-files", "-z", "-co", "--exclude-standard"],
        cwd=REPO, capture_output=True, check=True,
    ).stdout.decode("utf-8").split("\0")
    for rel in filter(None, listed):
        src = REPO / rel
        if not src.is_file():
            continue
        target = dest / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, target)
    git = ["git", "-c", "user.name=probe", "-c", "user.email=probe@example.invalid"]
    subprocess.run([*git, "init", "-q"], cwd=dest, check=True)
    subprocess.run([*git, "add", "-A"], cwd=dest, check=True)
    subprocess.run([*git, "commit", "-q", "-m", "copy"], cwd=dest, check=True)


def _collected_by_inventory(copy: Path, stray: str) -> bool:
    commands = json.loads(subprocess.run(
        [sys.executable, "-c", LIST_COMMANDS], cwd=copy,
        capture_output=True, text=True, check=True,
    ).stdout)
    for command in commands:
        if command[1:3] != ["-m", "pytest"]:
            continue
        args = [a for a in command[3:] if a not in ("-n", "auto", "-q", "-v")]
        out = subprocess.run(
            [sys.executable, "-m", "pytest", *args, "--collect-only", "-q",
             "-p", "no:cacheprovider"],
            cwd=copy, capture_output=True, text=True,
        ).stdout
        if "test_planted_stray_probe" in out and Path(stray).name in out:
            return True
    return False


def _flagged_by_a_guard(copy: Path) -> bool:
    guards = [g for g in GUARDS if (copy / g).is_file()]
    for guard in guards:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", guard, "-q", "-p", "no:cacheprovider"],
            cwd=copy, capture_output=True, text=True,
        )
        if result.returncode != 0:
            return True
    return False


def test_inventory_stray_test_in_root_tests_folder_is_collected(tmp_path: Path) -> None:
    """Control case: the same planted file under the root `tests/` folder is
    collected, so a red result above is the location, not the harness."""
    copy = tmp_path / "copy"
    copy.mkdir()
    _copy_tree(copy)
    stray = "tests/test_zz_planted_stray.py"
    (copy / stray).write_text(STRAY_BODY, encoding="utf-8")
    assert _collected_by_inventory(copy, stray)


@pytest.mark.parametrize(
    "stray",
    ["scripts/test_zz_planted_stray.py", ".claude/hooks/test_zz_planted_stray.py"],
)
def test_inventory_stray_test_in_a_formerly_collected_root_folder_is_run_or_refused(
    tmp_path: Path, stray: str
) -> None:
    """A pytest file planted in the repository-root `scripts/` or
    `.claude/hooks/` -- folders the suite collected before the move -- must
    either be collected by the discovered inventory or make a tests-folder
    guard fail; a planted file that does neither goes dark silently."""
    copy = tmp_path / "copy"
    copy.mkdir()
    _copy_tree(copy)
    planted = copy / stray
    planted.parent.mkdir(parents=True, exist_ok=True)
    planted.write_text(STRAY_BODY, encoding="utf-8")

    collected = _collected_by_inventory(copy, stray)
    flagged = _flagged_by_a_guard(copy)
    assert collected or flagged, (
        f"{stray} is neither collected by run_package_tests.py --loom-family "
        f"nor refused by any of {GUARDS}"
    )
