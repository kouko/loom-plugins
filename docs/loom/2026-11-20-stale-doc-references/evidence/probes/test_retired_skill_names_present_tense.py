# concern: a living document still presents a retired or moved skill (complexity-critique, loom-workflow skill-refactor/skill-tuning, requesting-docs-review) as something that ships or acts today
"""Adversary probe for Acceptance 2 of 2026-11-20-stale-doc-references.

Each case names one sentence in a living document (not per-change history)
that states a retired skill as current. The probe fails while that sentence
still stands; it passes once the sentence is corrected or marked as history.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]

CASES = [
    # (file, regex that matches the present-tense stale claim)
    ("loom-workflow/docs/skill-evolution-architecture.md",
     r"loom-workflow currently ships:(?:\n- [^\n]*)*\n- `complexity-critique`"),
    ("loom-workflow/docs/skill-evolution-architecture.md",
     r"`loom-workflow/skills/skill-(?:refactor|tuning)/SKILL\.md`"),
    ("loom-workflow/docs/quarterly-audit-runbook.md",
     r"Skills with NOTICE files[^\n]*\n(?:- [^\n]*\n)*- (?:complexity-critique|skill-refactor|skill-tuning) "),
    ("docs/loom/memory/same-reviewer-delta-confirmation-dies-at-a-context-compaction.md",
     r"`requesting-docs-review`'s Directive 2\s+encodes it"),
    ("docs/loom/memory/docs-review-dogfood-must-probe-the-evidence-class-trap.md",
     r"On every future change to docs-review contracts\s+\(requesting-docs-review"),
]


def _stale_hits():
    hits = []
    for rel, pattern in CASES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if re.search(pattern, text):
            hits.append(f"{rel}: /{pattern}/")
    return hits


def test_living_docs_retired_skill_names_absent_as_current():
    """No living document states a retired skill as currently shipping or acting."""
    hits = _stale_hits()
    assert not hits, "retired skill presented as current:\n" + "\n".join(hits)
