"""Graduated adversary probe for 2026-10-06-skill-prose-contradictions; guards against regression.
concern: a restated decision-point-1 rule outside the edited skills still merges every one-way door into ①, so contradiction 1 survives in a second copy.

The change narrowed the ① message to engineering one-way doors in
write-plan and capture-intent, but two other copies an agent reads still
put one-way doors into ① with no engineering qualifier:
`loom-code/contract/manifest.yaml` (action `restate-and-confirm`, the
charter the agents consult) and `AGENTS.md` (the loom 1.0 flow line Codex
loads as project instructions).
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]


def _manifest_restate_summary() -> str:
    text = (REPO / "loom-code/contract/manifest.yaml").read_text(encoding="utf-8")
    match = re.search(r"- name: restate-and-confirm\n(?:.*\n){0,3}?\s*summary: (.*)", text)
    assert match, "restate-and-confirm summary not found"
    return match.group(1)


def _agents_flow_line() -> str:
    for line in (REPO / "AGENTS.md").read_text(encoding="utf-8").splitlines():
        if "三個人類決策點" in line:
            return line
    raise AssertionError("AGENTS.md decision-point line not found")


def _agents_first_point(line: str) -> str:
    return line.split("①", 1)[1].split("②", 1)[0]


def _unqualified(text: str, door: str) -> bool:
    return door in text and "engineering" not in text


def test_detector_qualified_example_accepted() -> None:
    """A ① sentence naming engineering one-way doors passes."""
    assert not _unqualified("merge engineering one-way doors into ①", "one-way door")


def test_detector_unqualified_example_rejected() -> None:
    """A ① sentence merging every one-way door is caught."""
    assert _unqualified("merge one-way doors into ①", "one-way door")


def test_manifest_restate_and_confirm_limits_doors_to_engineering() -> None:
    """The manifest's decision-point-1 summary limits merged one-way doors to engineering changes."""
    summary = _manifest_restate_summary()
    assert not _unqualified(summary, "one-way door"), summary


def test_agents_md_first_decision_point_limits_doors_to_engineering() -> None:
    """AGENTS.md's ① entry limits one-way-door questions to engineering changes."""
    first = _agents_first_point(_agents_flow_line())
    assert not _unqualified(first, "單向門"), first
