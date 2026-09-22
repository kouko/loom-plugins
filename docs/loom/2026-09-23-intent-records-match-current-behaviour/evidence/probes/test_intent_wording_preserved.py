"""Adversarial probe: the edited intents keep their confirmed wording.

The change intent's first Constraint says the existing wording of each intent
stays as it was confirmed; the only allowed edits are added notes plus the one
status line in Acceptance 1 (2026-09-19-expert-mode-skip-friction). This probe
diffs every edited intent against the trunk commit the branch started from
(b568ba1a, PR #43) and fails on any existing line that was rewritten or
removed. Added lines anywhere pass.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-23-intent-records-match-current-behaviour/evidence/probes/test_intent_wording_preserved.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import difflib
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
BASE = "b568ba1a"
INTENTS = [
    "2026-09-14-antigravity-cli-compatibility",
    "2026-09-14-expert-mode-step-selection",
    "2026-09-14-land-merged-changes",
    "2026-09-18-blocked-publish-names-the-legal-routes",
    "2026-09-19-expert-mode-skip-friction",
    "2026-09-19-publication-hook-false-positives",
    "2026-09-20-mechanical-calculations",
]
# (intent, old line, required prefix of the new line): the one allowed rewrite.
ALLOWED_REWRITES = {
    ("2026-09-19-expert-mode-skip-friction", "status: open"): "status: closed",
}


def base_lines(change_id: str) -> list[str]:
    text = subprocess.run(
        ["git", "-C", str(REPO), "show", f"{BASE}:docs/loom/intent/{change_id}.md"],
        check=True, capture_output=True, text=True,
    ).stdout
    return text.splitlines()


def rewritten_lines(change_id: str, old: list[str], new: list[str]) -> list[str]:
    """Every base line that the new text rewrote or removed, minus the allowed one."""
    faults: list[str] = []
    matcher = difflib.SequenceMatcher(a=old, b=new, autojunk=False)
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag in ("equal", "insert"):
            continue
        replaced = new[j1:j2]
        for line in old[i1:i2]:
            prefix = ALLOWED_REWRITES.get((change_id, line.strip()))
            if prefix and any(r.strip().startswith(prefix) for r in replaced):
                continue
            faults.append(f"{tag}: {line!r} -> {replaced!r}")
    return faults


def test_wordingcheck_syntheticrewrite_detected() -> None:
    """A rewritten existing line is reported; a pure insertion is not."""
    old = ["kind: engineering", "needs-design: no", "## Open questions"]
    inserted = ["kind: engineering", "needs-design: no", "## Later changes", "- x", "## Open questions"]
    rewritten = ["kind: engineering", "needs-design: no — reason", "## Open questions"]
    assert rewritten_lines("synthetic", old, inserted) == []
    assert rewritten_lines("synthetic", old, rewritten) != []


def test_wordingcheck_allowedstatus_accepted() -> None:
    """The one status line Acceptance 1 allows passes; a different rewrite of it fails."""
    old = ["status: open", "## Problem"]
    good = ["status: closed 2026-09-23 — PR #43", "## Problem"]
    bad = ["status: withdrawn", "## Problem"]
    assert rewritten_lines("2026-09-19-expert-mode-skip-friction", old, good) == []
    assert rewritten_lines("2026-09-19-expert-mode-skip-friction", old, bad) != []


@pytest.mark.parametrize("change_id", INTENTS)
def test_editedintent_existingwording_unchanged(change_id: str) -> None:
    """No confirmed line of an edited intent is rewritten or removed."""
    new = (REPO / "docs/loom/intent" / f"{change_id}.md").read_text(encoding="utf-8").splitlines()
    faults = rewritten_lines(change_id, base_lines(change_id), new)
    assert not faults, f"{change_id} rewrote confirmed wording:\n" + "\n".join(faults)
