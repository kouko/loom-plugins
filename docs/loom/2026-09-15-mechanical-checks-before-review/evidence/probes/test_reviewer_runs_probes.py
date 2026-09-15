"""Adversarial probe: the reviewer's "run the changed test files" rule
selects the adversarial programs themselves.

Adversarial programs are committed as pytest files (`test_*.py`) under
`docs/loom/<change-id>/evidence/probes/`, and closing review hands each
reviewer the changed paths. A reviewer following reviewer.md or lenses.md
literally runs "the test files the change added or changed" -- which
includes those probes -- although the same contract says it never runs the
adversarial programs. The run instruction must itself carve the probes out.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-mechanical-checks-before-review/evidence/probes/test_reviewer_runs_probes.py -q
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
PROBES_DIR = Path(__file__).resolve().parent
RUN_RULE = "test files the change added or changed"
CARVE_OUT = re.compile(
    r"\b(?:except|excluding|other than|apart from|never|not|no)\b[^.;]*"
    r"(?:evidence/probes|adversarial programs?\b|probes?\b)",
    re.IGNORECASE,
)


def _sentences(path: Path) -> list[str]:
    flat = " ".join(path.read_text(encoding="utf-8").split())
    return [s for s in re.split(r"(?<=[.;])\s+", flat) if s]


def _run_rule_selects_probes(sentence: str) -> bool:
    """True when a sentence tells the reader to run changed test files
    without excluding the adversarial programs in that same sentence."""
    return RUN_RULE in sentence and not CARVE_OUT.search(sentence)


def test_carveout_affirmativeexclusion_accepted() -> None:
    """Synthetic: a run rule that names the probes as excluded passes."""
    sentence = (
        "You run the test files the change added or changed, except the "
        "adversarial programs under evidence/probes."
    )
    assert not _run_rule_selects_probes(sentence)


def test_carveout_bareruninstruction_rejected() -> None:
    """Synthetic: a run rule with no exclusion is flagged."""
    sentence = "You run the test files the change added or changed."
    assert _run_rule_selects_probes(sentence)


def test_changeprobes_committedaspytest_aretestfiles() -> None:
    """Boundary fact: this change's adversarial programs are test_*.py files."""
    probes = sorted(p.name for p in PROBES_DIR.glob("test_*.py"))
    assert probes, "no adversarial program shaped as a test file"


def test_reviewerrunrule_addedprobefile_excludesprobe() -> None:
    """Every reviewer-facing run rule must exclude the adversarial programs."""
    offending = []
    for rel in ("loom-code/agents/reviewer.md",
                "loom-code/skills/closing-review/references/lenses.md"):
        for sentence in _sentences(REPO / rel):
            if _run_rule_selects_probes(sentence):
                offending.append(f"{rel}: {sentence[:160]}")
    assert not offending, (
        "run rule selects this change's probes "
        f"{sorted(p.name for p in PROBES_DIR.glob('test_*.py'))}: {offending}"
    )
