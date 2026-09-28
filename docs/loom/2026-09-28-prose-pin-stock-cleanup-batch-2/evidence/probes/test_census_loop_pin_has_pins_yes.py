"""Adversary probe: the census classifier misses a phrase pin written as a loop.

`assert "phrase" in TEXT` sets has_pins=yes. The same pin written as
`for phrase in ("...", ...): assert phrase in TEXT` does not, so a file that
also carries a structure signal is reported clean. Real files in the test
roots use this form today and the A1 census reports them has_pins=no.

concern: the A1 census instrument reports a file as pin-free while it asserts multi-word prose phrases present in loop form.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

CLASSIFIER = Path(__file__).resolve().parents[3] / (
    "2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py"
)
_SPEC = importlib.util.spec_from_file_location("classify_test_files_probe", CLASSIFIER)
ctf = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ctf)

HEADER = 'from prose_pin import flat_prose\nTEXT = flat_prose("SKILL.md")\n\n'
STRUCTURE = 'def test_heading():\n    assert TEXT.startswith("# Title")\n\n'


def _pinned(tmp_path: Path, body: str) -> bool:
    f = tmp_path / "test_probe.py"
    f.write_text(HEADER + STRUCTURE + body, encoding="utf-8")
    cls, secondary = ctf.classify(f)
    return cls == "sentence-pin" or secondary.get("has_pins") == "yes"


def test_census_direct_phrase_pin_is_pinned(tmp_path: Path) -> None:
    """Control: the direct form is seen as a pin."""
    assert _pinned(tmp_path, 'def test_x():\n    assert "the rule is stated here" in TEXT\n')


def test_census_loop_phrase_pin_is_pinned(tmp_path: Path) -> None:
    """The loop form of the same pin is seen as a pin too."""
    body = ('def test_x():\n    for phrase in ("the rule is stated here", "a second clause here"):\n'
            '        assert phrase in TEXT\n')
    assert _pinned(tmp_path, body)
