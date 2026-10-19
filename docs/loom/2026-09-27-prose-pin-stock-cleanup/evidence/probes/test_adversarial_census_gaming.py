"""Adversarial probes against the census classifier (A1, A4).

concern: a census class decided by a comment token instead of by what the file asserts, and a documented CLI flag that crashes.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_SPEC = importlib.util.spec_from_file_location("classify_test_files", _HERE / "classify-test-files.py")
ctf = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ctf)

TRIGGER = "# prose_pin matcher self-test"
RECIPE_MODULES = ("code", "shape", "skill_gate", "spec")


def test_census_class_comment_token_planted_is_unchanged(tmp_path: Path) -> None:
    """Adding a comment that asserts nothing must not change a file's census class."""
    flipped = []
    for name in RECIPE_MODULES:
        path = ctf.REPO / f"loom-code/tests/test_adversary_recipe_{name}.py"
        copy = tmp_path / path.name
        copy.write_text(path.read_text(encoding="utf-8") + f"\n{TRIGGER}\n", encoding="utf-8")
        before, after = ctf.classify(path)[0], ctf.classify(copy)[0]
        if before != after:
            flipped.append((path.name, before, after))
    assert flipped == [], f"class depends on a comment token: {flipped}"


def test_census_roots_flag_given_is_accepted() -> None:
    """The docstring's `--roots` usage runs instead of raising."""
    run = subprocess.run(
        [sys.executable, str(_HERE / "classify-test-files.py"), "--roots", "loom-code/tests"],
        capture_output=True, text=True,
    )
    assert run.returncode == 0, run.stderr[-400:]
