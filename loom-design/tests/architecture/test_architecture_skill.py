"""Structural grep-test guarding the architecture SKILL.md: the interview ->
ARCHITECTURE.md -> guards -> ratify -> commit tool shape, mirroring
interface/test_design_system_skill.py. Checks assert on load-bearing phrases.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parents[2] / "skills" / "architecture"
SKILL = ROOT / "SKILL.md"
SCHEMA = ROOT / "references" / "architecture-md-schema.md"

_MAX_BODY_WORDS = 1500
_MAX_DESC_CHARS = 400


def _text() -> str:
    assert SKILL.is_file(), f"SKILL.md is absent at {SKILL}"
    return SKILL.read_text(encoding="utf-8")


def _frontmatter() -> str:
    text = _text()
    assert text.startswith("---\n")
    return text.split("---\n", 2)[1]


def test_frontmatter_declares_name_and_version():
    fm = _frontmatter()
    assert "name: architecture" in fm
    assert "version: 1.0.0" in fm


def test_description_within_codex_limit_and_carries_triggers():
    fm = _frontmatter()
    desc_block = fm.split("description:", 1)[1].split("version:", 1)[0]
    desc = " ".join(line.strip() for line in desc_block.strip("|\n ").splitlines())
    assert len(desc) <= _MAX_DESC_CHARS, f"description is {len(desc)} chars"
    for trigger in ("架構規則", "アーキテクチャ"):
        assert trigger in desc


def test_referenced_relative_paths_exist():
    text = _text()
    for m in re.finditer(r"`(\.\./[\w./-]+|references/[\w./-]+)`", text):
        candidate = SKILL.parent / m.group(1)
        assert candidate.is_file(), f"SKILL.md references missing path: {m.group(1)}"


def test_references_schema_validator_ratify_and_commit():
    text = _text()
    assert "references/architecture-md-schema.md" in text
    assert "scripts/architecture/validate_architecture_output.py" in text
    assert "ratified-by:" in text
    assert "docs(loom): ARCHITECTURE.md ratified" in text


def test_never_blocks_language_present():
    low = _text().lower()
    assert "never required" in low and "never blocks" in low


def test_update_changes_rule_and_guard_together():
    low = _text().lower()
    assert "same commit" in low
    assert "re-ratify" in low


def test_guard_failure_message_fields_stated():
    for doc in (_text(), SCHEMA.read_text(encoding="utf-8")):
        low = doc.lower()
        for field in ("rule id", "offending path", "conform", "change the rule and its guard"):
            assert field in low, f"missing guard failure-message field: {field!r}"


def test_no_gate_marker():
    assert "<!-- gate:" not in _text()
    assert "<!-- gate:" not in SCHEMA.read_text(encoding="utf-8")


def test_body_under_word_cap():
    text = _text()
    body = text[text.index("---", 3) + 3:]
    words = len(body.split())
    assert words <= _MAX_BODY_WORDS, f"body is {words} words, cap is {_MAX_BODY_WORDS}"
