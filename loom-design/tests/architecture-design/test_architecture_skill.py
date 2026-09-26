"""Structural grep-test guarding the architecture SKILL.md: the interview ->
ARCHITECTURE.md -> guards -> ratify -> commit tool shape, mirroring
interface/test_design_system_skill.py. Checks assert on load-bearing phrases.
"""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).parents[2] / "skills" / "architecture-design"
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
    assert re.findall(r"^name: (.+)$", fm, re.MULTILINE) == ["architecture-design"]
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
    plugin = ROOT.parents[1]
    for readme in (plugin.parent / "README.md", *sorted(plugin.glob("README*.md"))):
        text = readme.read_text(encoding="utf-8")
        assert "`architecture-design`" in text, readme
        assert "`architecture`" not in text, readme
        if readme.parent == plugin:
            assert "[`architecture-design`](skills/architecture-design/SKILL.md)" in text
        for target in re.findall(r"\]\((skills/[^)]+)\)", text):
            assert (readme.parent / target).is_file(), (readme, target)


def test_references_schema_validator_ratify_and_commit():
    text = _text()
    assert "references/architecture-md-schema.md" in text
    assert "scripts/architecture-design/validate_architecture_output.py" in text
    assert "ratified-by:" in text
    assert "docs(loom): ARCHITECTURE.md ratified" in text


def test_never_blocks_language_present():
    low = _text().lower()
    assert "never required" in low and "never blocks" in low


def test_skill_reads_code_and_proposes_two_options_per_choice():
    low = " ".join(_text().lower().split())
    for phrase in ("existing code", "at least two options", "trade-off", "recommendation",
                   "module split", "technology", "folder structure", "ci stages",
                   "references/design-know-how.md", "## decisions"):
        assert phrase in low, f"design step lacks {phrase!r}"


def test_single_answer_proposal_not_allowed():
    assert "never present a single answer" in " ".join(_text().lower().split())


def test_skill_states_redesign_updates_decisions_rules_guards():
    low = " ".join(_text().lower().split())
    assert "re-design" in low
    assert "decisions, rules and guards" in low
    assert "same commit" in low
    assert "re-ratify" in low


def test_guard_failure_message_fields_stated():
    low = SCHEMA.read_text(encoding="utf-8").lower()
    for field in ("rule id", "offending path", "conform", "change the rule and its guard"):
        assert field in low, f"missing guard failure-message field: {field!r}"
    assert "guard failure message" in _text().lower()


def test_skill_records_package_tests_when_absent_and_commits_edited_config():
    text = " ".join(_text().split())
    assert "- package-tests: <command> — <reason> (<date>)" in text
    step5 = text.split("## Step 5", 1)[1].split("## Downstream", 1)[0]
    assert "KICKOFF-DEFAULTS.md" in step5 and "Step 3 edited" in step5


def test_no_gate_marker():
    assert "<!-- gate:" not in _text()
    assert "<!-- gate:" not in SCHEMA.read_text(encoding="utf-8")


def test_body_under_word_cap():
    text = _text()
    body = text[text.index("---", 3) + 3:]
    words = len(body.split())
    assert words <= _MAX_BODY_WORDS, f"body is {words} words, cap is {_MAX_BODY_WORDS}"
