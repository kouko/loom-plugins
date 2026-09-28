"""Adversarial probes against guards left behind by the prune (W1-01, W2-02).

concern: a kept test that no longer reads what its name says it checks, and a guard that claims to catch any reintroduced prose pin but can disturb only one sentence.
"""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
TESTS = REPO / "loom-code/tests"
sys.path[:0] = [str(TESTS), str(REPO / "loom-code/scripts")]

import test_adversary_routing as routing  # noqa: E402


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


def test_reword_guard_pin_on_shorter_sentence_is_disturbed(tmp_path: Path) -> None:
    """The reword guard must disturb a pin on any recipe sentence, not only the longest."""
    refs = tmp_path / routing.REFERENCES.relative_to(routing.ROOT)
    refs.mkdir(parents=True)
    pinned = "Record every attempt."
    (refs / "adversarial-synthetic.md").write_text(
        f"# Adversarial — synthetic\n\n{pinned} This much longer sentence is the only one the guard rewords.\n",
        encoding="utf-8",
    )
    routing._reword_a_recipe_in(tmp_path, "adversarial-synthetic.md")
    after = (refs / "adversarial-synthetic.md").read_text(encoding="utf-8")
    assert pinned not in after, "a pin on this sentence survives the reword, so the guard stays green"
