# concern: stale failure - a nested folder already deleted from disk keeps the flatness check failing (Acceptance 1)
"""Removing the nested folder must restore a passing check."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
NESTED = "loom-code/skills/x/assets/sub"


def _flatness_module():
    spec = importlib.util.spec_from_file_location(
        "skill_folder_flatness_under_attack",
        REPO / "tests" / "test_skill_folder_flatness.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _git(root: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-C", str(root), "-c", "user.name=probe",
         "-c", "user.email=probe@example.invalid", *args],
        check=True, capture_output=True,
    )


@pytest.mark.parametrize("committed", [True, False], ids=["committed", "staged"])
def test_flatness_removed_nested_folder_passes(tmp_path, committed):
    """The folder fails while present and passes once it is gone from disk."""
    module = _flatness_module()
    _git(tmp_path, "init", "-q")
    nested = tmp_path / NESTED
    nested.mkdir(parents=True)
    (nested / "f.md").write_text("x\n", encoding="utf-8")
    _git(tmp_path, "add", ".")
    if committed:
        _git(tmp_path, "commit", "-q", "-m", "fixture")
    with pytest.raises(AssertionError):
        module.assert_skill_folders_flat(tmp_path)

    shutil.rmtree(nested)

    module.assert_skill_folders_flat(tmp_path)
