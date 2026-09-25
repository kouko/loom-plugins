"""Tests for validate_architecture_output.py — the ARCHITECTURE.md structure
check (ratified line, the four rule sections and nothing else, the rule-line
grammar, unique ids, and every `check:` guard path existing).
"""

from pathlib import Path

from validate_architecture_output import validate

_VALID = """\
# Architecture
ratified-by: Alex Rivera 2026-09-25

## Decisions
- D-1 — layer-first folders — options: layer-first, feature-first — reason: one small app

## Module boundaries
- MB-1 — ui/ never imports db/ — check: tests/arch/test_boundaries.py

## File placement
- FP-1 — tests live under tests/, apart from the code they test — check: review

## File size
- FS-1 — no source file over 400 lines — check: review

## CI stages
- CI-1 — lint runs before the test suite — check: review
"""


def _write(tmp_path: Path, text: str, guard: bool = True) -> Path:
    if guard:
        (tmp_path / "tests" / "arch").mkdir(parents=True)
        (tmp_path / "tests" / "arch" / "test_boundaries.py").write_text("", encoding="utf-8")
    path = tmp_path / "ARCHITECTURE.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_decisions_section_valid(tmp_path):
    ok, problems = validate(_write(tmp_path, _VALID))
    assert ok, problems


def test_decisions_section_missing_rejected(tmp_path):
    text = _VALID.replace(
        "## Decisions\n- D-1 — layer-first folders — options: layer-first, feature-first "
        "— reason: one small app\n\n", "")
    ok, problems = validate(_write(tmp_path, text))
    assert not ok
    assert any("Decisions" in p for p in problems)


def test_overview_section_rejected(tmp_path):
    text = _VALID.replace("## Module boundaries", "## Overview\nA layered app.\n\n## Module boundaries")
    ok, problems = validate(_write(tmp_path, text))
    assert not ok
    assert any("Overview" in p for p in problems)


def test_rule_with_existing_guard_valid(tmp_path):
    ok, problems = validate(_write(tmp_path, _VALID))
    assert ok, problems


def test_missing_guard_path_rejected(tmp_path):
    ok, problems = validate(_write(tmp_path, _VALID, guard=False))
    assert not ok
    assert any("tests/arch/test_boundaries.py" in p for p in problems)


def test_review_only_rule_needs_no_guard(tmp_path):
    text = _VALID.replace("check: tests/arch/test_boundaries.py", "check: review")
    ok, problems = validate(_write(tmp_path, text, guard=False))
    assert ok, problems


def test_unratified_file_rejected(tmp_path):
    text = _VALID.replace("ratified-by: Alex Rivera 2026-09-25\n", "")
    path = _write(tmp_path, text)
    ok, problems = validate(path)
    assert not ok
    assert any("ratified-by" in p for p in problems)
    ok, problems = validate(path, draft=True)
    assert ok, problems


def test_missing_section_bad_grammar_and_duplicate_ids_rejected(tmp_path):
    text = _VALID.replace("## CI stages\n- CI-1 — lint runs before the test suite — check: review\n", "")
    text = text.replace("FS-1", "FP-1").replace("## File size\n", "## File size\n- files stay small\n")
    ok, problems = validate(_write(tmp_path, text))
    assert not ok
    joined = "\n".join(problems)
    assert "CI stages" in joined
    assert "files stay small" in joined
    assert "FP-1" in joined and "unique" in joined
