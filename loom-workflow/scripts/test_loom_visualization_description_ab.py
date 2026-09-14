"""The shipped loom-visualization description is the exact A/B-tested text.

A behavioural A/B validates only the text that ran, so the rendered
description must hash to the value recorded in the change's A/B results.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
SKILL_PATH = REPO_ROOT / "loom-workflow/skills/loom-visualization/SKILL.md"
AB_DIR = REPO_ROOT / "docs/loom/2026-09-14-loom-visualization-description-trigger/ab"
RESULTS = AB_DIR / "results.md"
HASH_LINE = re.compile(r"^B rendered description SHA-256: `(?P<sha>[0-9a-f]{64})`$", re.MULTILINE)

sys.path.insert(0, str(AB_DIR))
import run_ab  # noqa: E402  (brings the catalog renderer and the hash helper)


def _tested_hash() -> str:
    match = HASH_LINE.search(RESULTS.read_text(encoding="utf-8"))
    assert match, "results.md records no B description hash"
    return match["sha"]


def _shipped() -> str:
    return run_ab._render_description(SKILL_PATH.read_text(encoding="utf-8"))


def test_description_shipped_text_equals_tested_hash() -> None:
    assert run_ab.sha256_text(_shipped()) == _tested_hash()


def test_description_edited_text_fails_hash_check() -> None:
    shipped = _shipped()
    edited = shipped[:-1] + ("," if shipped[-1] != "," else ".")
    assert run_ab.sha256_text(edited) != _tested_hash()


def test_description_names_station_reports_contains_phrase() -> None:
    assert "Loom station reports to the user" in _shipped()
