"""The shipped loom-visualization description is the exact A/B-tested text.

A behavioural A/B validates only the text that ran, so the rendered
description must hash to the value the A/B recorded. The hashes are pinned
here as literals so this guard does not depend on the per-change record.
"""

from __future__ import annotations

import hashlib
import importlib.util
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/loom-visualization/SKILL.md"
CATALOG = REPO_ROOT / "tests/test_loom_skill_description_catalog.py"

# Provenance: the ab/results.md (variant B, KEEP B) and ab/protocol.md (variant A,
# the description it renamed) of the 2026-09-23 change that renamed the step to
# acceptance testing.
TESTED_SHA256 = "b901f3528a8b1adbaaa412c1eb75034c973a0dac9e88def516f9ea147650c556"
VARIANT_A_SHA256 = "e98a3ed165415900bf405fe07209dde634cd465ff035fbea4ac2c73f57f6fd45"

_spec = importlib.util.spec_from_file_location("loom_skill_description_catalog", CATALOG)
_catalog = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_catalog)
_render_description = _catalog._render_description


def _shipped() -> str:
    return _render_description(SKILL_PATH.read_text(encoding="utf-8"))


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def test_description_shipped_text_equals_tested_hash() -> None:
    assert _sha256(_shipped()) == TESTED_SHA256


def test_description_shipped_text_is_not_variant_a() -> None:
    assert _sha256(_shipped()) != VARIANT_A_SHA256


def test_description_names_station_reports_contains_phrase() -> None:
    assert "Loom station reports to the user" in _shipped()
