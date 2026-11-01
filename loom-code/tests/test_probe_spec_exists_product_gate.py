# concern: unreachable rule - a resumed run without loom-design whose existing product spec lacks confirmed-behavior never reaches the product-spec gate text
"""Adversarial probe for `2026-10-29-write-plan-conditional-references`.

Before this change the `write-plan.product-spec-needs-confirmed-behavior`
gate sat in SKILL.md's always-read body. It now lives only in
`references/self-written-spec.md`, and SKILL.md points there from two
branches: the `no` branch's spec condition and `yes, spec missing,
loom-design not installed`.

A run without loom-design that wrote its product spec in an earlier
session and stopped before decision point 2 resumes on the branch
`yes, and spec.md already exists` and goes straight to the intake check.
`intake.confirmed-behavior` blocks with "decision point 2 has not
happened", but neither that branch nor the intake check sends the run to
the file that says how to run decision point 2 (plain words, nothing from
`## Design decision` down, the `git hash-object` pin). This probe is RED
while that route is missing.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))

from prose_pin import has_negation, split_sentences  # noqa: E402

WRITE_PLAN = ROOT / "loom-code/skills/write-plan/SKILL.md"
GATE_ID = "write-plan.product-spec-needs-confirmed-behavior"
POINTER = "self-written-spec.md"
AFFIRMATIVE = re.compile(r"\b(?:read|follow|apply|run)\b", re.IGNORECASE)

SPEC_EXISTS = "**`yes`, and `docs/loom/<change-id>/spec.md` already exists**"
INSTALLED = "**`yes`, spec missing, `loom-design` installed**"
INTAKE = "### The intake check"


def _resume_route(text: str) -> str:
    """The text a run on the spec-exists branch reads before Step 5."""
    step4 = text.split("## Step 4", 1)[1].split("\n## Step 5", 1)[0]
    branch = step4.split(SPEC_EXISTS, 1)[1].split(INSTALLED, 1)[0]
    intake = step4.split(INTAKE, 1)[1]
    return " ".join((branch + "\n" + intake).split())


def _routes_to_gate(route: str) -> bool:
    if GATE_ID in route:
        return True
    return any(
        POINTER in s and AFFIRMATIVE.search(s) and not has_negation(s)
        for s in split_sentences(route)
    )


def test_routeDetector_affirmativePointer_accepted() -> None:
    """Synthetic: an affirmative pointer sentence counts as a route."""
    assert _routes_to_gate(
        "For a `kind: product` spec missing its `confirmed-behavior:` line, "
        "read `references/self-written-spec.md` and follow its gate."
    )


def test_routeDetector_negatedPointer_rejected() -> None:
    """Synthetic: a negated pointer sentence is not a route."""
    assert not _routes_to_gate(
        "Do not read `references/self-written-spec.md` on this branch."
    )


def test_specExistsBranch_loomDesignAbsentResume_reachesProductGate() -> None:
    """The always-read body holds the gate, or the spec-exists branch or its
    intake check routes to it."""
    text = WRITE_PLAN.read_text(encoding="utf-8")
    assert GATE_ID in text or _routes_to_gate(_resume_route(text)), (
        "a resumed run on `yes, spec exists` without loom-design is never "
        f"sent to {POINTER} or {GATE_ID}"
    )
