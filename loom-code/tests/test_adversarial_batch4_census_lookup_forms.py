"""Adversarial probes: positional lookups and markdown holders the batch-4 census does not see (A1).

concern: a census that reports zero prose pins while a test still requires a skill sentence through a `.find()` presence check or a markdown body held on `self`, both forms the repository's own tests already use.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
_CLASSIFIER = REPO / "docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py"
if not _CLASSIFIER.exists():
    pytest.skip(
        "evidence classifier for 2026-09-27-prose-pin-stock-cleanup is gone",
        allow_module_level=True,
    )
_SPEC = importlib.util.spec_from_file_location("classify_test_files", _CLASSIFIER)
ctf = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(ctf)

_HEAD = 'from pathlib import Path\nSKILL = Path("skills/x/SKILL.md")\n'


def test_census_find_presence_lookup_flags_pin() -> None:
    """A sentence required through `.find(...) != -1` is a positional lookup, the same pin as `.index()`."""
    src = _HEAD + ('def test_x():\n    md = SKILL.read_text()\n'
                   '    idx = md.find("never mention ground truth")\n    assert idx != -1\n')
    lines = ctf.direct_pin_lines(src)
    assert lines and set(lines) <= {5, 6}, lines  # the lookup line or the assert line


def test_census_self_attribute_markdown_flags_pin() -> None:
    """A sentence asserted `in self.body`, where setup_method read SKILL.md into self.body, is a direct pin."""
    src = _HEAD + ('class TestSkill:\n    def setup_method(self):\n        self.body = SKILL.read_text()\n\n'
                   '    def test_x(self):\n        assert "never mention ground truth" in self.body\n')
    assert ctf.direct_pin_lines(src) == [8]
