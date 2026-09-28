"""Adversarial probes against guards left behind by the prune (W1-01).

concern: a kept test that no longer reads what its name says it checks.

The reword-guard case was retired once the guard's docstrings were narrowed
to what it checks (only the longest sentence is disturbed).
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]


def test_case_class_check_recipe_row_dropped_goes_red(tmp_path: Path) -> None:
    """Dropping a case class row from the code recipe must redden the test named for it."""
    shutil.copytree(REPO / "loom-code", tmp_path / "loom-code", ignore=shutil.ignore_patterns("__pycache__"))
    recipe = tmp_path / "loom-code/skills/closing-review/references/adversarial-code.md"
    text = recipe.read_text(encoding="utf-8")
    row = next(line for line in text.splitlines() if line.startswith("| Boundary |"))
    recipe.write_text(text.replace(row + "\n", ""), encoding="utf-8")
    run = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "loom-code/tests/test_adversary_recipe_code.py::test_recipe_names_every_class_to_draw_cases_from"],
        cwd=tmp_path, capture_output=True, text=True,
    )
    assert run.returncode != 0, "recipe lost a case class and the test named for it stayed green"
