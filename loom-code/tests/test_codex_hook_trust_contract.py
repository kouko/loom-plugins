"""Gate-marker presence for installed Loom hook trust versus repository hooks."""

from __future__ import annotations

from pathlib import Path


PLUGIN = Path(__file__).resolve().parents[1]
FIRST_CONTACT = PLUGIN / "skills" / "write-plan" / "references" / "codex-first-contact.md"


def test_first_contact_new_worktree_does_not_create_loom_trust_work() -> None:
    """Gate-marker presence only; the paragraph's wording is review-only."""
    text = FIRST_CONTACT.read_text(encoding="utf-8")

    assert text.count("<!-- gate: write-plan.codex-installed-hook-trust-boundary -->") == 1
