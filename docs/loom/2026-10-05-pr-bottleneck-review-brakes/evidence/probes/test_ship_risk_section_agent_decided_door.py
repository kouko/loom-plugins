# concern: PR risk section misses a one-way door recorded as agent-decided after decision point one
"""Adversarial probe: the ship PR `## Risks and rollback` placeholder must send
the writer to agent-decided door answers too, not only user-decided lines.

write-plan records a one-way door that surfaces after decision point one as
`agent-decided` (task Risk lines, acceptance test report), never as a
user-decided line. A placeholder that cites only user-decided lines lets the
PR call such a change a two-way door.
"""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
SHIP = ROOT / "loom-code" / "skills" / "ship" / "SKILL.md"

AFFIRMATIVE = re.compile(r"\b(cit(e|es|ing)|nam(e|es|ing)|includ(e|es|ing)|stat(e|es|ing)|list(s|ing)?)\b", re.I)
NEGATION = re.compile(r"\b(not|never|no|without|except|omit|skip|ignore)\b|n't", re.I)


def _risk_placeholder(text: str) -> str:
    match = re.search(r"^## Risks and rollback\n(.*?)^## ", text, re.M | re.S)
    assert match, "ship SKILL.md has no `## Risks and rollback` block"
    return match.group(1)


def _affirms(block: str, literal: str) -> bool:
    for sentence in re.split(r"(?<=[.;])\s+", " ".join(block.split())):
        index = sentence.find(literal)
        if index < 0 or NEGATION.search(sentence):
            continue
        if AFFIRMATIVE.search(sentence[:index]):
            return True
    return False


def test_affirms_selftest_affirmative_example_accepted() -> None:
    """A sentence citing agent-decided door answers is accepted."""
    assert _affirms("<door, citing user-decided and agent-decided door lines>", "agent-decided")


def test_affirms_selftest_negated_example_rejected() -> None:
    """A sentence that cites agent-decided answers under a negation is rejected."""
    assert not _affirms("<door, citing user-decided lines, not agent-decided ones>", "agent-decided")


def test_ship_risk_placeholder_cites_agent_decided_doors() -> None:
    """The PR risk placeholder affirmatively cites agent-decided door answers."""
    block = _risk_placeholder(SHIP.read_text(encoding="utf-8"))
    assert _affirms(block, "agent-decided"), block
