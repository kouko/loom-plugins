"""The skill-and-gate recipe's own rules: `adversarial-skill-gate.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

Every assertion here pins text of the skill-and-gate recipe. It moved out
of `test_build_mechanical_checks.py`, where the same fragments were checked
against the whole procedure at once, so a skill-and-gate edit could turn a
test about another recipe red. The fragments and the assertion shape are
unchanged; only the document they are read against narrowed to the file
that owns the rules.

An edit to the skill-and-gate recipe turns this file red and names it; an
edit to the code recipe, to the spec recipe or to the shared protocol does
not.
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
RECIPE = REFERENCES / "adversarial-skill-gate.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


def _flat(path: Path) -> str:
    return " ".join(re.sub(r"^> ?", "", path.read_text(encoding="utf-8"), flags=re.M).split())


ADVERSARIAL_SKILL_GATE = _flat(RECIPE)
ADVERSARY_PROSE = _flat(ADVERSARY)


# --- One home for this recipe's rules: adversary.md repeats none of them ----

# Each fragment names one rule the skill-and-gate recipe owns; it lives in
# this file and nowhere in adversary.md.
PROCEDURE_FRAGMENTS = ("under time pressure", "prose temptations", "one character different")


def _procedure_fragments_in_both(agent: str, ref: str) -> list[str]:
    return [f for f in PROCEDURE_FRAGMENTS if f in agent and f in ref]


def test_procedure_fragments_helper_synthetic() -> None:
    ref = "Read the instruction as an agent under time pressure."
    assert _procedure_fragments_in_both("Read the reference first.", ref) == []
    duplicated = "Read it as an agent under time pressure would."
    assert _procedure_fragments_in_both(duplicated, ref) == ["under time pressure"]


def test_procedure_sentence_in_both_files_rejected() -> None:
    assert _procedure_fragments_in_both(ADVERSARY_PROSE, ADVERSARIAL_SKILL_GATE) == []
    assert [f for f in PROCEDURE_FRAGMENTS if f not in ADVERSARIAL_SKILL_GATE] == []
