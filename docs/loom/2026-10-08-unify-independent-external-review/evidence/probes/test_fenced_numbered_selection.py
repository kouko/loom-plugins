# concern: A numbered example inside a Markdown fence must not authorize outside review.
"""Reject a quoted numbered selection in a committed plan's Risks section."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-code/scripts"))

from loom_checker import reviewers  # noqa: E402


def test_selection_fenced_ignored(monkeypatch: pytest.MonkeyPatch) -> None:
    """A fenced numbered example cannot become the selected outside family."""
    plan = (
        "## Risks\n"
        "```text\n"
        "3. user-decided — second-vendor selection-confirmed: codex\n"
        "```\n"
    )

    def fake_git_maybe(_repo: Path, *args: str) -> str:
        if args == ("rev-parse", "HEAD"):
            return "committed-head"
        if args[-1].endswith("/plan.md"):
            return plan
        return ""

    monkeypatch.setattr(reviewers, "git_maybe", fake_git_maybe)
    assert reviewers.selected_outside_family(REPO, "trial") is None
