"""Fix-scope rule-count guard (plan W0-01; intent 2026-09-24-fix-the-whole-class).

concern: a test outside the checker's own tests still pins the checker's rule
count as a literal integer; only `test_loom_checker_*.py` is exempt and the
look-ahead spans twenty lines; graduated adversary probe.

The fix-scope rule's wording in Build §2 and its pointers are review-only; this
file keeps the rule-count guard and the no-gate-marker check on Build §2.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "loom-code"
BUILD_TEXT = (CODE / "skills/build/SKILL.md").read_text(encoding="utf-8")
SECTION_2 = BUILD_TEXT.split("## 2. Implement test first", 1)[1].split("## 3.", 1)[0]


TREES = ("loom-code", "loom-design", "loom-workflow")
WINDOW = 20
LIST_RULES_RE = re.compile(r"--list-rules|list_rules|\bRULE_IDS\b|\brule_ids\b")
LEN_EQ_RE = re.compile(r"len\(.*\)\s*==\s*\d+")
RULE_LIST_EQ_RE = re.compile(r"len\(\s*(?:RULE_IDS|rule_ids)\s*\)\s*==\s*\d+")


def is_checker_own_test(path: Path) -> bool:
    return path.name.startswith("test_loom_checker_")


def literal_rule_counts(text: str) -> list[str]:
    """Lines that pin the checker's rule count as a literal integer.

    Recognition-based and partial: it flags `len(RULE_IDS|rule_ids) == <int>`
    anywhere, and `len(...) == <int>` within twenty lines after a `--list-rules`,
    `list_rules`, `RULE_IDS` or `rule_ids` mention. A bare `RULES` name is left
    out: recipe tests use it for their own lists. A count held in a variable,
    computed, or compared further away passes unseen.
    """
    lines = text.splitlines()
    return [
        line.strip() for i, line in enumerate(lines)
        if RULE_LIST_EQ_RE.search(line)
        or (LEN_EQ_RE.search(line) and any(LIST_RULES_RE.search(x) for x in lines[max(0, i - WINDOW):i + 1]))
    ]


def test_no_literal_rule_count_outside_checker_tests() -> None:
    files = [p for tree in TREES for p in sorted((ROOT / tree).rglob("test_*.py"))
             if "__pycache__" not in p.parts and not is_checker_own_test(p)]
    hits = {str(p.relative_to(ROOT)): found for p in files
            if (found := literal_rule_counts(p.read_text(encoding="utf-8")))}
    assert hits == {}, hits


def test_literal_rule_count_reintroduced_fails() -> None:
    eq = "=="  # kept off the sample lines so this file does not flag itself
    sample = (
        'def test_count() -> None:\n'
        '    out = run([CHECKER, "--list-rules"]).stdout\n'
        f'    assert len(out.splitlines()) {eq} 26\n'
        f'assert len(RULE_IDS) {eq} 26\n'
    )
    assert literal_rule_counts(sample) == [line.strip() for line in sample.splitlines()[2:]]


def test_far_literal_rule_count_fails() -> None:
    eq = "=="
    sample = 'run([CHECKER, "--list-rules"])\n' + "x = 1\n" * 15 + f"assert len(lines) {eq} 26\n"
    assert literal_rule_counts(sample) == [f"assert len(lines) {eq} 26"]


def test_unrelated_rules_constant_is_not_flagged() -> None:
    eq = "=="
    sample = f"RULES = _rules(RECIPE)\nassert len(RULES) {eq} 5\n"
    assert literal_rule_counts(sample) == []


def test_rule_list_test_without_literal_count_passes() -> None:
    sample = 'ids = run([CHECKER, "--list-rules"]).stdout.splitlines()\nassert ids == sorted(ids)\n'
    assert literal_rule_counts(sample) == []


def test_only_the_checkers_own_tests_are_exempt() -> None:
    assert is_checker_own_test(Path("test_loom_checker_cli.py"))
    assert not is_checker_own_test(Path("test_probes_language_policy.py"))


def test_no_gate_marker_or_dispatch_wording() -> None:
    assert "<!-- gate" not in SECTION_2
