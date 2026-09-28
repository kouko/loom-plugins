"""`deletion-first` reaches the docs and skill lenses.

What stays here is structural: `reviewer.md`'s `docs` and `skill` lens
table rows each end with the `deletion-first` dimension token. The
wording of the deletion-first rule in `lenses.md` is review-only.
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
