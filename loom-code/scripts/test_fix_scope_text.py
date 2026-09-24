"""Every fix is scoped to its defect's class before hand-off (plan W0-01;
intent 2026-09-24-fix-the-whole-class Acceptance 1, 2 and 4).

concern: false-green prose pin — a bare-substring pin passed a rule that was
negated or handed to the wrong actor, so each rule sentence is pinned with
`affirms` (actor before literal, no negation); graduated adversary probe.

The rule lives in Build §2 only; closing-review and Ship carry one-sentence
pointers, and the implementer contract accepts a multi-file fix hand-off.
"""
from __future__ import annotations

import re
from pathlib import Path

from prose_pin import affirms, flat_prose, pins_exact_sentence, split_sentences

ROOT = Path(__file__).resolve().parents[2]
CODE = ROOT / "loom-code"
BUILD_TEXT = (CODE / "skills/build/SKILL.md").read_text(encoding="utf-8")
REVIEW = flat_prose(CODE / "skills/closing-review/SKILL.md")
SHIP = flat_prose(CODE / "skills/ship/SKILL.md")
IMPLEMENTER = flat_prose(CODE / "agents/implementer.md")
SECTION_2 = BUILD_TEXT.split("## 2. Implement test first", 1)[1].split("## 3.", 1)[0]
RULE = " ".join(("Before any fix" + SECTION_2.partition("Before any fix")[2]).split("\n\n", 1)[0].split())

SEARCH_PIN = (
    "the main agent names", "the defect's class",
    "Before any fix is handed to an implementer or made by the main agent itself",
    "the adversary, acceptance testing, a reviewer or a failing check",
    "searches the whole content of every file the change touches",
    "(`git diff --name-only <base>...HEAD`, where `<base>` is the branch base §1 reads)",
    "every surface named by the Acceptance line the finding maps to",
)
BOUND_PIN = ("The search is bounded by", "those files and those surfaces")
RECORD_PIN = (
    "The fix hand-off lists", "every instance found, the flagged one included",
    "the hand-off and the fix's commit message each state the class and the places searched",
    "even when the flagged instance is the only one found",
)
WEAKENED = (
    ("lists every instance found", "never lists every instance found"),
    ("even when the flagged", "but not even when the flagged"),
    ("the main agent names", "the implementer names"),
)


def test_rule_names_class_search_and_acceptance_surfaces() -> None:
    assert affirms(RULE, *SEARCH_PIN)
    assert affirms(RULE, *BOUND_PIN)


def test_record_states_class_and_places_searched_even_when_none_found() -> None:
    assert affirms(RULE, *RECORD_PIN)


def test_weakened_rule_fails_the_pins() -> None:
    for old, new in WEAKENED:
        weakened = RULE.replace(old, new, 1)
        assert weakened != RULE, old
        assert not (affirms(weakened, *SEARCH_PIN) and affirms(weakened, *RECORD_PIN)), new


def test_pointers_reach_every_fix_path() -> None:
    for phrase in ("names the defect's class", "--name-only", "the places searched"):
        assert phrase not in REVIEW and phrase not in SHIP, phrase
    pointers = [s for s in split_sentences(REVIEW) if "class" in s and "Build §2" in s]
    assert len(pointers) == 1 and "the main agent" in pointers[0], pointers
    assert affirms(SHIP, "The minimum fix covers", "every instance of the defect's class", "Build §2")
    assert affirms(IMPLEMENTER, "In a fix hand-off", "the task's scope", "the instances it lists and their files")
    assert "never silently widen the work" in IMPLEMENTER


ONE_CLASS_ONE_TASK = (
    "A fix hand-off that lists several instances of one defect class is one task, "
    "a single assertion about that class."
)


def test_one_class_many_instances_is_one_task() -> None:
    assert pins_exact_sentence(IMPLEMENTER, ONE_CLASS_ONE_TASK)


def test_blocked_for_instances_rewrite_fails_the_pin() -> None:
    weakened = IMPLEMENTER.replace(
        ONE_CLASS_ONE_TASK,
        "A fix hand-off that lists several instances of one defect class returns `BLOCKED`.",
    )
    assert not pins_exact_sentence(weakened, ONE_CLASS_ONE_TASK)


CHECKER_TESTS = {"test_loom_checker_cli.py", "test_loom_checker_modules.py", "test_probes_language_policy.py"}
LIST_RULES_RE = re.compile(r"--list-rules|list_rules")
LEN_EQ_RE = re.compile(r"len\(.*\)\s*==\s*\d+")
RULE_LIST_EQ_RE = re.compile(r"len\(\s*(?:RULES|RULE_IDS|rule_ids)\s*\)\s*==\s*\d+")


def literal_rule_counts(text: str) -> list[str]:
    """Lines that pin the checker's rule count as a literal integer.

    Recognition-based and partial: it flags `len(RULES|RULE_IDS|rule_ids) == <int>`
    anywhere, and `len(...) == <int>` within six lines after a `--list-rules`
    or `list_rules` mention. A count held in a variable, computed, or compared
    further away passes unseen.
    """
    lines = text.splitlines()
    return [
        line.strip() for i, line in enumerate(lines)
        if RULE_LIST_EQ_RE.search(line)
        or (LEN_EQ_RE.search(line) and any(LIST_RULES_RE.search(x) for x in lines[max(0, i - 6):i + 1]))
    ]


def test_no_literal_rule_count_outside_checker_tests() -> None:
    files = sorted((CODE / "scripts").glob("test_*.py")) + sorted((CODE / "skills").rglob("test_*.py"))
    hits = {p.name: found for p in files if p.name not in CHECKER_TESTS
            if (found := literal_rule_counts(p.read_text(encoding="utf-8")))}
    assert hits == {}


def test_literal_rule_count_reintroduced_fails() -> None:
    eq = "=="  # kept off the sample lines so this file does not flag itself
    sample = (
        'def test_count() -> None:\n'
        '    out = run([CHECKER, "--list-rules"]).stdout\n'
        f'    assert len(out.splitlines()) {eq} 26\n'
        f'assert len(RULES) {eq} 26\n'
    )
    assert literal_rule_counts(sample) == [line.strip() for line in sample.splitlines()[2:]]


def test_no_gate_marker_or_dispatch_wording() -> None:
    assert "<!-- gate" not in SECTION_2
    for word in ("dispatch", "subagent", "new step", "extra step"):
        assert word not in RULE, word
