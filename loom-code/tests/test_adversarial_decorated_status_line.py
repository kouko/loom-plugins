"""Adversarial probe: a misstated `Verification status:` line in ordinary
Markdown dress (list item, bold label, capitalised label) still publishes.
concern: publish lets a PR body misstate its verification status when the line is Markdown-decorated
Reuses test_loom_publish.py's real-flow helper; nothing is stubbed but the network.
"""
from __future__ import annotations

from pathlib import Path

import pytest

from test_loom_publish import disclosed_body, unattested_publication


@pytest.mark.parametrize("line", [
    "- Verification status: valid (skipped: reviewers)",
    "**Verification status:** valid (skipped: reviewers)",
    "Verification Status: valid (skipped: reviewers)",
])
def test_publish_decoratedMisstatedStatus_refusedBeforePush(
    line: str, tmp_path: Path, monkeypatch
) -> None:
    """The branch computes `absent`; a body claiming `valid` in any common
    Markdown form is refused before any outward call."""
    rc, _out, err, calls = unattested_publication(tmp_path, monkeypatch, disclosed_body([line]))

    assert rc == 1, err
    assert "Verification status: absent" in err
    assert calls.calls == []
