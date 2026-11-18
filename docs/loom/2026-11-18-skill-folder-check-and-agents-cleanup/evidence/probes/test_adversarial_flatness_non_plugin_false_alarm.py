# concern: false alarm - top-level folders that are not plugins fail the flatness check
"""Only plugin skill folders are subject to the flat-folder rule."""
from __future__ import annotations

import importlib.util
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]


def _flatness_module():
    spec = importlib.util.spec_from_file_location(
        "skill_folder_flatness_under_attack",
        REPO / "tests" / "test_skill_folder_flatness.py",
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("top_level", ["tests", "docs", "scripts"])
def test_flatness_non_plugin_skills_folder_passes(tmp_path, top_level):
    """A fixture or record under a non-plugin folder is not a skill."""
    subprocess.run(["git", "-C", str(tmp_path), "init", "-q"], check=True)
    fixture = tmp_path / top_level / "skills" / "x" / "assets" / "sub" / "f.md"
    fixture.parent.mkdir(parents=True)
    fixture.write_text("x\n", encoding="utf-8")

    _flatness_module().assert_skill_folders_flat(tmp_path)
