# concern: a living document still presents a retired or moved skill (complexity-critique, loom-workflow skill-refactor/skill-tuning, requesting-docs-review) as something that ships or acts today
"""Adversary probe for Acceptance 1 and 2 of 2026-11-20-stale-doc-references.

Each case names one sentence in a living document (not per-change history)
that states a retired skill as current. Under the renewed Acceptance 2 a
historical record keeps its original wording, so a case is stale only while
the sentence stands AND no separate dated note in the same file
("Note YYYY-MM-DD: ...") names the retired skill to label it as history.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[5]

DATED_NOTE = r"Note \d{4}-\d{2}-\d{2}:"

CASES = [
    # (file, regex for the present-tense claim, retired skill a dated note must name)
    ("loom-workflow/docs/skill-evolution-architecture.md",
     r"loom-workflow currently ships:(?:\n- [^\n]*)*\n- `complexity-critique`",
     "complexity-critique"),
    ("loom-workflow/docs/skill-evolution-architecture.md",
     r"`loom-workflow/skills/skill-(?:refactor|tuning)/SKILL\.md`",
     "loom-workflow/skills/skill-"),
    ("loom-workflow/docs/quarterly-audit-runbook.md",
     r"Skills with NOTICE files[^\n]*\n(?:- [^\n]*\n)*- (?:complexity-critique|skill-refactor|skill-tuning) ",
     "skill-tuning"),
    ("docs/loom/memory/same-reviewer-delta-confirmation-dies-at-a-context-compaction.md",
     r"`requesting-docs-review`'s Directive 2\s+encodes it",
     "requesting-docs-review"),
    ("docs/loom/memory/docs-review-dogfood-must-probe-the-evidence-class-trap.md",
     r"On every future change to docs-review contracts\s+\(requesting-docs-review",
     "requesting-docs-review"),
]


def _dated_note_names(text, name):
    for m in re.finditer(DATED_NOTE, text):
        window = text[m.start():m.start() + 800]
        if name in window:
            return True
    return False


def _stale_hits(cases=CASES, read=lambda rel: (ROOT / rel).read_text(encoding="utf-8")):
    hits = []
    for rel, pattern, name in cases:
        text = read(rel)
        if re.search(pattern, text) and not _dated_note_names(text, name):
            hits.append(f"{rel}: /{pattern}/")
    return hits


def test_living_docs_retired_skill_names_absent_as_current():
    """No living document states a retired skill as current without a dated history note."""
    hits = _stale_hits()
    assert not hits, "retired skill presented as current:\n" + "\n".join(hits)


def test_stale_hits_unlabelled_claim_flagged():
    """Synthetic: a claim with no dated note is reported; one with a note naming it is not."""
    case = [("x.md", r"ships `complexity-critique`", "complexity-critique")]
    assert _stale_hits(case, read=lambda _: "It ships `complexity-critique`.\n")
    labelled = "It ships `complexity-critique`.\n(Note 2026-11-21: complexity-critique retired.)\n"
    assert not _stale_hits(case, read=lambda _: labelled)
