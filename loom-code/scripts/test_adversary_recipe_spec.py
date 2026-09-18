"""The spec recipe's own rules: `adversarial-spec.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

Every assertion here pins text of the spec recipe. It moved out of
`test_build_mechanical_checks.py`, where the same fragment was checked
against the whole procedure at once, so a spec-recipe edit could turn a
test about the code recipe red. The fragment and the assertion shape are
unchanged; only the document it is read against narrowed to the file that
owns the rule.

An edit to the spec recipe turns this file red and names it; an edit to the
code recipe, to the skill-and-gate recipe or to the shared protocol does
not.
"""
from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
RECIPE = REFERENCES / "adversarial-spec.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


def _flat(path: Path) -> str:
    return " ".join(re.sub(r"^> ?", "", path.read_text(encoding="utf-8"), flags=re.M).split())


ADVERSARIAL_SPEC = _flat(RECIPE)
ADVERSARY_PROSE = _flat(ADVERSARY)


# --- One home for the spec recipe's rules: adversary.md repeats none of them -

# Each fragment names one rule the spec recipe owns; it lives in this file
# and nowhere in adversary.md.
PROCEDURE_FRAGMENTS = ("did not want",)


def _procedure_fragments_in_both(agent: str, ref: str) -> list[str]:
    return [f for f in PROCEDURE_FRAGMENTS if f in agent and f in ref]


def test_procedure_fragments_helper_synthetic() -> None:
    ref = "Name a behaviour the requirement permits that the author clearly did not want."
    assert _procedure_fragments_in_both("Read the reference first.", ref) == []
    duplicated = "Name what the author did not want."
    assert _procedure_fragments_in_both(duplicated, ref) == ["did not want"]


def test_procedure_sentence_in_both_files_rejected() -> None:
    assert _procedure_fragments_in_both(ADVERSARY_PROSE, ADVERSARIAL_SPEC) == []
    assert [f for f in PROCEDURE_FRAGMENTS if f not in ADVERSARIAL_SPEC] == []
