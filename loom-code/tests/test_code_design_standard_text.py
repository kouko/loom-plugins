"""The code-design standard is the one text writer, planner and judge read.

`loom-code/references/code-design-standard.md` holds the code-design rules;
engineering-baseline.md, the closing-review code-lens rows and write-plan's
Task size paragraph point to it instead of restating it. Pins follow the
prose-pin rule: an affirmative verb before the pinned literal, no negation
token in that sentence, and synthetic self-tests for one affirmative and one
negated example.
"""
from __future__ import annotations

import re
from pathlib import Path

from prose_pin import affirms, flat_prose, rule_prose

REPO = Path(__file__).resolve().parents[2]
STANDARD = REPO / "loom-code/references/code-design-standard.md"
BASELINE = REPO / "loom-code/references/engineering-baseline.md"
LENSES = REPO / "loom-code/skills/closing-review/references/lenses.md"
WRITE_PLAN = REPO / "loom-code/skills/write-plan/SKILL.md"
LENS_CITE = "`../../../references/code-design-standard.md`"

# One literal per moved rule; each lives in the standard only.
MOVED_RULES = (
    "past 20 lines, and again past 50, is a prompt to look",
    "two concrete users now, an explicit request, or a visible motivation",
    "A finding must name the smaller shape that does the same job",
    "resource-boundary handling and policy choice",
    "a package `__init__`, a TS `index` barrel",
    "extracted only when the three change for the same reason",
    "wanting to test it alone is no reason for a new entry",
    "annotated with its ceiling and its upgrade path",
)
SINGLE_USE_BANS = ("abstraction for a single use", "premature abstraction", "speculative generality")


def _owned_by_standard(rule: str, standard: str, *others: str) -> bool:
    return standard.count(rule) == 1 and all(rule not in other for other in others)


def _one_threshold(standard: str, *readers: str) -> bool:
    stated = affirms(
        standard, "justifies itself with", "two concrete users now", "an explicit request", "a visible motivation"
    )
    return stated and not any(ban in text for text in (standard, *readers) for ban in SINGLE_USE_BANS)


def _shallow_and_deletion_test(text: str) -> bool:
    return (
        affirms(text, "gives its callers", "little", "interface is nearly as complex as what it does")
        and affirms(text, "Prefer", "small interface", "hides substantial behaviour")
        and affirms(text, "imagine deleting it", "pass-through", "complexity vanishes")
        and affirms(text, "reappears across its callers", "earns its place")
    )


def _testability(text: str) -> bool:
    return affirms(text, "Accept", "dependency from outside", "rather than creating it inside") and affirms(
        text, "return a result", "rather than producing a side effect"
    )


def _task_size_points(paragraph: str) -> bool:
    return affirms(paragraph, "Read", "../../references/code-design-standard.md", "module boundary")


def _task_size() -> str:
    text = WRITE_PLAN.read_text(encoding="utf-8")
    start = text.index("**Task size.**")
    return " ".join(text[start:text.index("\n\n", start)].split())


def _lens_row(name: str) -> str:
    rows = [l for l in LENSES.read_text(encoding="utf-8").splitlines() if l.startswith(f"| {name} |")]
    return rows[0]


def test_standard_exists_and_code_lens_rows_cite_it() -> None:
    """A1 positive (file-exists): the standard exists; each moved row cites it."""
    assert STANDARD.is_file()
    for name in ("naming", "refactoring", "deliberate-simplification", "deletion-first", "architecture"):
        assert LENS_CITE in _lens_row(name), name
    assert "SOLID (Martin)" in _lens_row("architecture")


def test_moved_rules_stated_once_in_standard_only() -> None:
    """A2 positive (refactoring-rule-once) and A9: each moved rule lives in the standard alone."""
    standard, baseline, lenses = flat_prose(STANDARD), flat_prose(BASELINE), flat_prose(LENSES)
    for rule in MOVED_RULES:
        assert _owned_by_standard(rule, standard, baseline, lenses), rule
    assert "(code-design-standard.md)" in baseline


def test_owned_matcher_rejects_duplicate_and_missing() -> None:
    """A1 negative (missing) and A2 negative (duplicated), on synthetic text."""
    rule = MOVED_RULES[5]
    assert _owned_by_standard(rule, f"Rule: {rule}.", "baseline text")
    assert not _owned_by_standard(rule, f"Rule: {rule}.", f"lens restates {rule}")
    assert not _owned_by_standard(rule, "", "baseline text")


def test_one_abstraction_threshold() -> None:
    """A3 positive (one-abstraction-threshold): standard states it; baseline and lenses only point."""
    standard, baseline, lenses = rule_prose(STANDARD), flat_prose(BASELINE), flat_prose(LENSES)
    assert _one_threshold(standard, baseline, lenses)
    assert "two concrete users" not in baseline and "two concrete users" not in lenses


def test_threshold_matcher_rejects_single_use_ban() -> None:
    """A3 negative (single-use-ban-remains): a reader keeping the single-use ban fails."""
    standard = (
        "Every new abstraction, flag, config or extension point justifies itself with two concrete "
        "users now, an explicit request, or a visible motivation."
    )
    assert _one_threshold(standard, "Simplicity first. Read the standard.")
    assert not _one_threshold(standard, "Simplicity first. Nothing speculative, no abstraction for a single use.")
    assert not _one_threshold(standard.replace("justifies itself", "never justifies itself"))


def test_shallow_module_and_deletion_test_present() -> None:
    """A5 positive (shallow-and-deletion-test-present)."""
    assert _shallow_and_deletion_test(rule_prose(STANDARD))


def test_shallow_matcher_rejects_negated() -> None:
    """A5 negative (shallow-negated), on synthetic text."""
    text = (
        "A module whose interface is nearly as complex as what it does gives its callers little. "
        "Prefer a small interface that hides substantial behaviour. "
        "To judge a module, imagine deleting it: if the complexity vanishes with it, it was a pass-through; "
        "if the complexity reappears across its callers, the module earns its place."
    )
    assert _shallow_and_deletion_test(text)
    assert not _shallow_and_deletion_test(text.replace("Prefer a small", "Do not prefer a small"))


def test_testability_present() -> None:
    """A7 positive (testability-present)."""
    assert _testability(rule_prose(STANDARD))


def test_testability_matcher_rejects_negated() -> None:
    """A7 negative (testability-negated), on synthetic text."""
    text = (
        "Accept a dependency from outside rather than creating it inside. "
        "Where the behaviour allows, return a result rather than producing a side effect."
    )
    assert _testability(text)
    assert not _testability(text.replace("Accept a", "Never accept a"))


def test_task_size_cites_standard() -> None:
    """A8 positive (task-size-cites-standard)."""
    assert _task_size_points(_task_size())


def test_task_size_matcher_rejects_missing_pointer() -> None:
    """A8 negative (task-size-no-pointer), on synthetic text."""
    pointer = "Read `../../references/code-design-standard.md` when choosing each task's module boundary."
    assert _task_size_points(pointer)
    assert not _task_size_points("Each task owns one module boundary.")
    assert not _task_size_points(pointer.replace("Read", "Do not read"))


def test_forward_only_finding_kept() -> None:
    """A9 positive (forward-only-finding-kept): forwarding modules stay a finding."""
    assert affirms(rule_prose(STANDARD), "only forwards", "is a finding", "just a call elsewhere returning its result")


def test_barrel_exemption_kept() -> None:
    """A9 boundary (barrel-exemption-kept): a re-export declaring the entry stays outside the rule."""
    text = rule_prose(STANDARD)
    assert affirms(text, "hiding any of those", "outside this rule", "re-export that declares the module's entry")
    assert re.search(r"package `__init__`, a TS `index` barrel", text)
