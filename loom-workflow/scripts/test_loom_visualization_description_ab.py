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
CATALOG = REPO_ROOT / "scripts/test_loom_skill_description_catalog.py"

# Provenance: docs/loom/2026-09-14-loom-visualization-description-trigger/ab/results.md
# (variant B, SHIP) and ab/protocol.md (variant A, the pre-change description).
TESTED_SHA256 = "e98a3ed165415900bf405fe07209dde634cd465ff035fbea4ac2c73f57f6fd45"
VARIANT_A_SHA256 = "6c65729a01ccc3b9cc81d7387b163d4b61dd1d0a26386ea69a10cad8d370f64c"

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
