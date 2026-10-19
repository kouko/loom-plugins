"""Adversarial probes against the census classifier (A1, A4).

concern: a census class decided by a comment token instead of by what the file asserts, a documented CLI flag that crashes, and a phrase pin in loop form reported as pin-free.
"""
from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_EVIDENCE = REPO / "docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes"
_CLASSIFIER = _EVIDENCE / "classify-test-files.py"
if not _CLASSIFIER.exists():
    pytest.skip(
        "evidence classifier for 2026-09-27-prose-pin-stock-cleanup is gone",
        allow_module_level=True,
    )
_SPEC = importlib.util.spec_from_file_location("classify_test_files", _CLASSIFIER)
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
        [sys.executable, str(_CLASSIFIER), "--roots", "loom-code/tests"],
        capture_output=True, text=True,
    )
    assert run.returncode == 0, run.stderr[-400:]


def test_census_loop_phrase_pin_is_pinned(tmp_path: Path) -> None:
    """`for p in ("<phrase>", ...): assert p in TEXT` is a pin, even beside a structure signal."""
    f = tmp_path / "test_probe.py"
    f.write_text(
        'from prose_pin import flat_prose\nTEXT = flat_prose("SKILL.md")\n\n'
        'def test_heading():\n    assert TEXT.startswith("# Title")\n\n'
        'def test_x():\n    for phrase in ("the rule is stated here", "a second clause here"):\n'
        "        assert phrase in TEXT\n",
        encoding="utf-8",
    )
    cls, secondary = ctf.classify(f)
    assert cls == "sentence-pin" or secondary.get("has_pins") == "yes", (cls, secondary)
