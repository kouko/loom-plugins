"""The spec recipe's own rules: `adversarial-spec.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

One kind of assertion, against the working tree: the one-home check that
moved out of `test_build_mechanical_checks.py`, where the same fragment was
checked against the whole procedure at once, so a spec-recipe edit could
turn a test about the code recipe red.

Nothing here is frozen. The recipe stays free to be edited -- reworded,
extended, reordered -- and no sentence of it is pinned. What the split did,
once, is `test_adversary_layout.py`'s business and is read from git there,
not from these files.
"""
from __future__ import annotations

from pathlib import Path

# The reader is `prose_pin`'s, under this module's own name: the protocol's
# test module, every other recipe's and `test_build_mechanical_checks.py`
# carried byte-identical copies of it.
from prose_pin import flat_prose as _flat


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
RECIPE = REFERENCES / "adversarial-spec.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


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
