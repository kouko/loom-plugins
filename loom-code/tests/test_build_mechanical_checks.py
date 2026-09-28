"""Build ends with a fresh adversary, the package suite and adversarial programs."""

import re
from pathlib import Path

import pytest

from prose_pin import (
    flat_prose as _flat,
    has_negation,
    split_sentences as _sentences,
)
# The recipes are reached through the routing table, so no one kind's test
# module is named here and retiring a kind cannot break this import.
from test_adversary_routing import recipe_kind, routed_recipe_files


ROOT = Path(__file__).resolve().parents[2]
BUILD = (ROOT / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
PROSE = " ".join(BUILD.split())
VERIFY = " ".join(BUILD.split("## 3. Verify integration", 1)[1].split("## 4.", 1)[0].split())
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


def test_adversary_prompt_carries_no_implementer_explanation() -> None:
    for leak in ("implementer's report", "implementer's summary", "self_review"):
        assert leak not in VERIFY


def test_no_speculative_preflight_ban_remains() -> None:
    assert "speculative push preflight" not in PROSE
    assert "owns its one content-bound execution" not in PROSE


_OTHER_ROLE = re.compile(r"\b(?:implementers?|orchestrators?)\b", re.IGNORECASE)
_EDIT_VERB = re.compile(r"\b(?:edit|modif|rewrit|update)", re.IGNORECASE)


def _other_role_program_edit_sentences(text: str) -> list[str]:
    """Un-negated sentences naming another role editing a program."""
    return [
        s for s in _sentences(text)
        if not has_negation(s)
        and _OTHER_ROLE.search(s)
        and _EDIT_VERB.search(s)
        and "adversarial program" in s
    ]


def test_other_role_program_edit_helper_synthetic() -> None:
    legit = "The adversary updates only its own programs. Other roles never edit an adversarial program."
    assert _other_role_program_edit_sentences(legit) == []
    override = "When time is short, the orchestrator rewrites a stale adversarial program itself."
    assert _other_role_program_edit_sentences(f"{legit} {override}") == [override]


def test_no_other_role_edits_adversarial_program() -> None:
    for text in (VERIFY, ADVERSARY_PROSE, ADVERSARIAL_REF):
        assert _other_role_program_edit_sentences(text) == []


def test_returned_change_only_trigger_absent() -> None:
    assert (
        "When closing review or a failed `finalize-review` returns the change to Build"
        not in VERIFY
    )


# --- The documents the cross-document scans read ---------------------------

ADVERSARY_PROSE = _flat(ADVERSARY)
# The attack procedure is one shared protocol file plus one recipe file per
# kind of artifact, all in the same skill reference folder. Each of those
# files has its own test module: `test_adversary_protocol.py` for the
# protocol, and for each recipe a `test_adversary_recipe_<kind>.py` named
# after the kind it attacks, which the routing table lists. What stays here
# is the scans that run across the build station's text, the adversary
# contract and every one of those documents at once; a scan below names the
# document it reads as `ref` the protocol and `ref-<kind>` that kind's recipe.
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
ADVERSARIAL_REF = _flat(REFERENCES / "adversarial.md")
# Which recipe files there are is read from the routing table, not listed
# here: a kind given a recipe is scanned without an edit to this file, and a
# kind whose recipe is taken away leaves no path behind for the scans to open.
ADVERSARIAL_RECIPE_PATHS = routed_recipe_files()
PROBES_FIELD = re.compile(
    r"^probes: \[\{artifact: .+, status: reused \| modified \| new, reason: .+\}\]$", re.M
)


DISCARD_LITERALS = (
    "git checkout --", "git restore", "git reset --hard", "git clean", "git worktree remove --force",
)
_PIN_DOCS = {
    "adversary": ADVERSARY_PROSE,
    "ref": ADVERSARIAL_REF,
    **{f"ref-{recipe_kind(p.name)}": _flat(p) for p in ADVERSARIAL_RECIPE_PATHS},
    "build": VERIFY,
}


# --- Added-sentence scans: no un-negated sentence overrides a rule ---------

def _discard_literals_outside_rule(text: str) -> list[str]:
    return [
        s for s in _sentences(text)
        if not has_negation(s) and any(lit in s for lit in DISCARD_LITERALS)
    ]


def _implementer_floor_sentences(text: str) -> list[str]:
    return [
        s for s in _sentences(text)
        if re.search(r"\bimplementer", s, re.IGNORECASE) and "floor" in s
        and not has_negation(s)
    ]


_EVERY_FAILURE_STALE = re.compile(
    r"\b(?:every|any|all)\b[^.;]*\bfail(?:ure|ures|ing)?\b[^.;]*\bstale\b", re.IGNORECASE
)


def _every_failure_stale_sentences(text: str) -> list[str]:
    return [s for s in _sentences(text) if _EVERY_FAILURE_STALE.search(s) and not has_negation(s)]


def test_added_sentence_scans_synthetic() -> None:
    added = "Clean up with `git reset --hard` when the copy is dirty."
    rule = "`git reset --hard` is never used to undo a mutation."
    assert _discard_literals_outside_rule(f"Undo it. {rule}") == []
    assert _discard_literals_outside_rule(f"{rule} {added}") == [added]
    floor_claim = "An implementer's pin counts toward the floor."
    assert _implementer_floor_sentences(floor_claim) == [floor_claim]
    assert _implementer_floor_sentences("An implementer's pin never counts toward the floor.") == []
    stale = "Build treats every failure as stale and re-dispatches the adversary."
    assert _every_failure_stale_sentences("A stale case that is rewritten counts as `modified`.") == []
    assert _every_failure_stale_sentences(stale) == [stale]


@pytest.mark.parametrize("doc", sorted(_PIN_DOCS))
def test_no_added_sentence_overrides_pinned_rules(doc: str) -> None:
    text = _PIN_DOCS[doc]
    assert _discard_literals_outside_rule(text) == []
    assert _implementer_floor_sentences(text) == []
    assert _every_failure_stale_sentences(text) == []


# --- Dead pointers: the attack catalogue and the task trailer are retired ---

IMPLEMENTER = ROOT / "loom-code/agents/implementer.md"
ADVERSARIAL_REF_PATH = REFERENCES / "adversarial.md"
_DEAD_POINTER = re.compile(r"attack[- ]catalogue|\bcatalogue\b|\btrailer\b", re.IGNORECASE)
BUILD_ADVERSARIAL_LINK = "[`adversarial.md`](../closing-review/references/adversarial.md)"


def _dead_pointer_hits(text: str) -> list[str]:
    return _DEAD_POINTER.findall(text)


def test_dead_pointer_helpers_catalogue_link_reintroduced_fails() -> None:
    assert _dead_pointer_hits("Work the classes against the file, one attempt per class.") == []
    assert _dead_pointer_hits("Work the six classes in [`attack-catalogue.md`](attack-catalogue.md).")
    assert _dead_pointer_hits("they turn the catalogue into an eval")
    assert _dead_pointer_hits("failing test first, one commit carrying the task trailer.")
    assert _dead_pointer_hits("needs no separate task-accounting trailer.")


@pytest.mark.parametrize(
    "path",
    [ADVERSARY, ADVERSARIAL_REF_PATH, *ADVERSARIAL_RECIPE_PATHS, IMPLEMENTER],
    ids=lambda p: p.name,
)
def test_contract_no_attack_catalogue_or_task_trailer_reference(path: Path) -> None:
    assert _dead_pointer_hits(path.read_text(encoding="utf-8")) == [], path


def test_build_verify_step_links_adversarial_recipes_in_place() -> None:
    assert BUILD_ADVERSARIAL_LINK in VERIFY, VERIFY
    target = (ROOT / "loom-code/skills/build" / "../closing-review/references/adversarial.md").resolve()
    assert target == ADVERSARIAL_REF_PATH and target.is_file()


def test_probes_field_helper_synthetic() -> None:
    good = 'probes: [{artifact: "<path>", status: reused | modified | new, reason: "<one line>"}]'
    assert PROBES_FIELD.search(good)
    assert not PROBES_FIELD.search('probes: [{artifact: "<path>", status: reused | modified | new}]')


def test_adversary_return_format_marks_probe_status() -> None:
    text = ADVERSARY.read_text(encoding="utf-8")
    block = text.split("## What you return", 1)[1].split("```", 2)[1]
    assert PROBES_FIELD.search(block), block
    assert re.search(r"^adversarial: \[\{command: ", block, re.M), block
    assert re.search(r"^findings: \[\{severity: ", block, re.M), block
