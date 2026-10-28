# concern: branch rule tells the agent to create a change branch that already exists, so `git switch -c` fails and the near-miss `git switch -C` discards its commits
"""Adversary probe: the change branch already exists while HEAD is on the trunk.

capture-intent now creates `<type>/<change-id>` before the intent commit. A
later station (write-spec, or write-plan at Step 3 for an already-confirmed
intent) that starts on the trunk -- a new session, a handoff resume -- reads
"on the trunk, create it", runs `git switch -c <type>/<change-id>`, and git
refuses: `fatal: a branch named '...' already exists`. The rule names no
route for that state; the nearest command that "works", `git switch -C`,
resets the existing branch and drops the confirmed intent commit.

Each station that owns the branch rule must say, in an affirmative sentence,
that an existing change branch is switched to with
`git switch <type>/<change-id>` (no `-c`).

Run from the repo root:
    python3 -m pytest docs/loom/2026-10-29-change-branch-before-intent/evidence/probes/test_probe_existing_change_branch.py
"""
from __future__ import annotations

import sys
from pathlib import Path


def _repo_root(start: Path) -> Path:
    for parent in [start, *start.parents]:
        if (parent / "loom-code" / "scripts" / "prose_pin.py").is_file():
            return parent
    raise RuntimeError("repo root not found")


ROOT = _repo_root(Path(__file__).resolve().parent)
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))
from prose_pin import affirms, rule_prose  # noqa: E402

LITERAL = "`git switch <type>/<change-id>`"
VERBS = ("switch", "reuse", "run")
STATE = "already exists"


def _states_existing_branch_route(text: str) -> bool:
    return any(affirms(text, verb, LITERAL, STATE) for verb in VERBS)


def test_probe_affirmative_route_accepted() -> None:
    """Self-test: an affirmative sentence naming the existing-branch route passes."""
    text = ("If `<type>/<change-id>` already exists, switch to it with "
            "`git switch <type>/<change-id>`.")
    assert _states_existing_branch_route(text)


def test_probe_negated_route_rejected() -> None:
    """Self-test: the same route in a negated sentence does not count."""
    text = ("If `<type>/<change-id>` already exists, never switch to it with "
            "`git switch <type>/<change-id>`.")
    assert not _states_existing_branch_route(text)


def test_write_plan_branch_exists_switches_to_it() -> None:
    """write-plan's branch rule routes an existing change branch to a plain switch."""
    text = rule_prose(ROOT / "loom-code" / "skills" / "write-plan" / "SKILL.md")
    assert _states_existing_branch_route(text), (
        "write-plan: 'on the trunk, create it' fails when the change branch already exists"
    )


def test_capture_intent_branch_exists_switches_to_it() -> None:
    """capture-intent's branch rule (which write-spec defers to) routes an existing change branch to a plain switch."""
    text = rule_prose(ROOT / "loom-design" / "skills" / "capture-intent" / "SKILL.md")
    assert _states_existing_branch_route(text), (
        "capture-intent: 'on the trunk, create it' fails when the change branch already exists"
    )
