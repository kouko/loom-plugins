"""W1-01 — RED/GREEN evidence: `deletion-first` reaches the docs and skill
lenses, plus the cap-bump-candidate rule.

Before this task, `deletion-first` was a code-only dimension
(`lenses.md`'s "Code — eleven dimensions" table): only a program's new
abstractions were asked to justify themselves against a smaller shape.
Station text and agent contracts — the artifacts the `docs` and `skill`
lenses actually score — could grow a new paragraph, mechanism, reserved
task, or fallback path with nobody asking whether it replaced something or
prevented an observed failure. This file pins that the docs table and the
skill lens paragraph each name `deletion-first`, that the shared definition
they both point to carries an affirmative sentence requiring the smaller
shape, that a second sentence names a deletion candidate for a file whose
`*_CAP` was raised in two consecutive changes, and that `reviewer.md`'s
`docs` and `skill` lens rows end with `deletion-first`.

Never `wc` for word counts — BSD/GNU disagree; `len(str.split())` only.
"""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
REVIEWER = REPO / "loom-code/agents/reviewer.md"


def test_reviewer_docs_row_ends_with_deletion_first() -> None:
    text = REVIEWER.read_text(encoding="utf-8")
    row = next(
        (line for line in text.splitlines() if line.strip().startswith("| `docs`")),
        None,
    )
    assert row is not None, "reviewer.md has no `| `docs` |` lens row."
    assert row.rstrip().rstrip("|").rstrip().endswith("deletion-first"), (
        f"reviewer.md's docs lens row does not end with `deletion-first`: {row!r}"
    )


def test_reviewer_skill_row_ends_with_deletion_first() -> None:
    text = REVIEWER.read_text(encoding="utf-8")
    row = next(
        (line for line in text.splitlines() if line.strip().startswith("| `skill`")),
        None,
    )
    assert row is not None, "reviewer.md has no `| `skill` |` lens row."
    assert row.rstrip().rstrip("|").rstrip().endswith("deletion-first"), (
        f"reviewer.md's skill lens row does not end with `deletion-first`: {row!r}"
    )
