"""Guard: living docs must not present the retired skills as current.

Each case names one sentence in a living document (not per-change history)
that once stated a retired or moved skill (complexity-critique,
loom-workflow skill-refactor/skill-tuning, requesting-docs-review) as
something that ships or acts today. The test fails if such a sentence returns.

A historical section may keep an old name verbatim when a dated
current-name note labels it (intent Acceptance 1 and 2). Cases that carry a
note pattern fail only when the old-name text appears without that note.
"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[1]

ARCH_NOTE = (r"Note 2026-11-21: the planning doc below is kept verbatim"
             r"[\s\S]*?retired in favour of `critique`")

CASES = [
    # (file, regex that matches the stale claim,
    #  regex of the dated note that labels it as history, or None)
    ("loom-workflow/docs/skill-evolution-architecture.md",
     r"loom-workflow currently ships:(?:\n- [^\n]*)*\n- `complexity-critique`",
     ARCH_NOTE),
    ("loom-workflow/docs/skill-evolution-architecture.md",
     r"`loom-workflow/skills/skill-(?:refactor|tuning)/SKILL\.md`",
     ARCH_NOTE),
    ("loom-workflow/docs/quarterly-audit-runbook.md",
     r"Skills with NOTICE files[^\n]*\n(?:- [^\n]*\n)*- (?:complexity-critique|skill-refactor|skill-tuning) ",
     r"Note 2026-11-21: the list above is as of v1\.7\.0\.[\s\S]*\bcritique\b"),
    ("docs/loom/memory/same-reviewer-delta-confirmation-dies-at-a-context-compaction.md",
     r"`requesting-docs-review`'s Directive 2\s+encodes it",
     None),
    ("docs/loom/memory/docs-review-dogfood-must-probe-the-evidence-class-trap.md",
     r"On every future change to docs-review contracts\s+\(requesting-docs-review",
     None),
]


def _is_stale(text, pattern, note):
    return bool(re.search(pattern, text)) and not (note and re.search(note, text))


def _stale_hits():
    hits = []
    for rel, pattern, note in CASES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        if _is_stale(text, pattern, note):
            hits.append(f"{rel}: /{pattern}/")
    return hits


def test_living_docs_retired_skill_names_absent_as_current():
    """No living document states a retired skill as currently shipping or acting."""
    hits = _stale_hits()
    assert not hits, "retired skill presented as current:\n" + "\n".join(hits)


def test_old_name_without_dated_note_is_flagged():
    """Removing the dated note from a historical file exposes the old name."""
    for rel, pattern, note in CASES[:3]:
        text = re.sub(note, "", (ROOT / rel).read_text(encoding="utf-8"))
        assert _is_stale(text, pattern, note), rel
