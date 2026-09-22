"""Adversarial probe: the edited intents keep their confirmed wording.

The change intent's first Constraint says the existing wording of each intent
stays as it was confirmed; the only allowed edits are added notes plus the one
status line in Acceptance 1 (2026-09-19-expert-mode-skip-friction). A second
Constraint (user-decided 2026-09-23) lets
2026-09-19-publication-hook-false-positives append a reason to its
`needs-design: no` line and nothing more; its added `originator:` line and
`## Out of scope` section are insertions, which always pass. This probe
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
import re
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
# (intent, exact old line) -> pattern the whole new line must match. The status
# line is Acceptance 1's; the needs-design line is the Constraints exception
# user-decided 2026-09-23 (cf97c369): the line keeps `needs-design: no` and only
# gains a non-empty reason after the checker's ` — ` separator.
ALLOWED_REWRITES = {
    ("2026-09-19-expert-mode-skip-friction", "status: open"):
        re.compile(r"status: closed\b.*"),
    ("2026-09-19-publication-hook-false-positives", "needs-design: no"):
        re.compile(r"needs-design: no — \S.*"),
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
            allowed = ALLOWED_REWRITES.get((change_id, line))
            if allowed and any(allowed.fullmatch(r) for r in replaced):
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


def test_wordingcheck_needsdesignreason_appendonly() -> None:
    """The needs-design exception accepts only an appended reason, only in its own intent."""
    hook = "2026-09-19-publication-hook-false-positives"
    old = ["kind: engineering", "needs-design: no", "## Problem"]

    def with_line(line: str) -> list[str]:
        return ["kind: engineering", line, "## Problem"]

    assert rewritten_lines(hook, old, with_line("needs-design: no — hook recognition only")) == []
    for bad in ("needs-design: yes — a reason", "needs-design: no —", "needs-design: no — ",
                "needs-design: No — a reason", "needs-design: no - a reason",
                "needs-design: no, a reason", "needs-design: none — a reason"):
        assert rewritten_lines(hook, old, with_line(bad)) != [], bad
    assert rewritten_lines("2026-09-14-land-merged-changes", old,
                           with_line("needs-design: no — a reason")) != []
    assert rewritten_lines(hook, old, ["kind: Engineering", "needs-design: no — a reason",
                                       "## Problem"]) != []


@pytest.mark.parametrize("change_id", INTENTS)
def test_editedintent_existingwording_unchanged(change_id: str) -> None:
    """No confirmed line of an edited intent is rewritten or removed."""
    new = (REPO / "docs/loom/intent" / f"{change_id}.md").read_text(encoding="utf-8").splitlines()
    faults = rewritten_lines(change_id, base_lines(change_id), new)
    assert not faults, f"{change_id} rewrote confirmed wording:\n" + "\n".join(faults)
