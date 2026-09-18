"""The shared attack protocol's own rules: `adversarial.md`.

Acceptance 3 and 6 of `docs/loom/intent/2026-09-18-modular-adversary-recipes.md`.

Every assertion here pins a sentence of the protocol file that every recipe
is read together with. Each one moved out of
`test_build_mechanical_checks.py` or `test_review_convergence_contract.py`
with its pinned text and its assertion shape unchanged: a pin that pins a
sentence still names the affirmative verb before the literal and still
rejects a negation of it.

What this file therefore is: the one place a protocol edit turns red, and
the one place a protocol rule is pinned. A recipe file cannot turn it red,
and it holds no rule a recipe owns.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
PROTOCOL = REFERENCES / "adversarial.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


def _flat(path: Path) -> str:
    return " ".join(re.sub(r"^> ?", "", path.read_text(encoding="utf-8"), flags=re.M).split())


# The raw protocol, for the assertions that cut it at a heading, and the
# flattened protocol, for the sentence pins.
PROTOCOL_TEXT = PROTOCOL.read_text(encoding="utf-8")
ADVERSARIAL_REF = _flat(PROTOCOL)
ADVERSARY_PROSE = _flat(ADVERSARY)


def _sentences(text: str) -> list[str]:
    return split_sentences(text)


def _colon_sentences(text: str) -> list[str]:
    return split_sentences(text, ends=".:;")  # colon is a boundary here


def _affirms(text: str, verb: str, literal: str, *extras: str) -> bool:
    """Some sentence carries `verb` before `literal`, every extra, and no negation."""
    for s in _sentences(text):
        v, lit = s.find(verb), s.find(literal)
        if 0 <= v < lit and all(e in s for e in extras) and not has_negation(s):
            return True
    return False


def _pins_exact_sentence(section: str, sentence: str) -> bool:
    return _sentences(section).count(sentence) == 1


# --- The probe-maintenance rules the protocol owns --------------------------
#
# (doc, verb, literal, extras, affirmative example, rejected examples)

PROTOCOL_PINS = {
    "ref-commit-before-copy": (
        "ref", "The adversary commits the updated probe", "before it makes a copy",
        ("because `git worktree add` and `git archive` hold only committed content",
         "an uncommitted update takes the edit-tool route in the working tree"),
        "The adversary commits the updated probe before it makes a copy, because `git worktree "
        "add` and `git archive` hold only committed content, and an uncommitted update takes the "
        "edit-tool route in the working tree.",
        ("The adversary commits the updated probe not before it makes a copy, because `git "
         "worktree add` and `git archive` hold only committed content, and an uncommitted update "
         "takes the edit-tool route in the working tree.",
         "The adversary commits the updated probe before it makes a copy."),
    ),
    "ref-undo-before-worktree-remove": (
        "ref", "The adversary undoes each mutation in a worktree copy with the host's edit tool",
        "before `git worktree remove` removes that copy",
        ("prefers a `git archive` extract when the copy will be left behind",),
        "The adversary undoes each mutation in a worktree copy with the host's edit tool before "
        "`git worktree remove` removes that copy, and prefers a `git archive` extract when the "
        "copy will be left behind in a temp directory.",
        ("The adversary undoes each mutation in a worktree copy with the host's edit tool before "
         "`git worktree remove` removes that copy, and never prefers a `git archive` extract when "
         "the copy will be left behind in a temp directory.",
         "The adversary undoes each mutation in a worktree copy with the host's edit tool before "
         "`git worktree remove` removes that copy."),
    ),
    "ref-mutation-red-then-reverted": (
        "ref", "Each mutation must", "turn the probe RED and is then reverted", (),
        "Each mutation must turn the probe RED and is then reverted, and the report gives each "
        "one's command and observed result.",
        ("Each mutation must not turn the probe RED and is then reverted, and the report gives "
         "each one's command and observed result.",),
    ),
    "ref-mutation-reported": (
        "ref", "the report gives", "each one's command and observed result", (),
        "Each mutation must turn the probe RED and is then reverted, and the report gives each "
        "one's command and observed result.",
        ("Each mutation must turn the probe RED and is then reverted, and the report never gives "
         "each one's command and observed result.",),
    ),
    "ref-mutation-copy-of-logic-proves-nothing": (
        "ref", "A copy of the probe's logic proves", "nothing about that program", (),
        "A copy of the probe's logic proves nothing about that program.",
        ("A copy of the probe's logic proves nothing about that program, unless it is not a copy.",
         "A copy of the probe's logic is enough evidence."),
    ),
    "ref-permanent-test-is-reuse": (
        "ref", "counts as reuse", "the adversary names it in `reason`",
        ("A permanent repository test that already covers a case", "leaves the test as it is"),
        "A permanent repository test that already covers a case counts as reuse: the adversary "
        "names it in `reason` and leaves the test as it is.",
        ("A permanent repository test that already covers a case never counts as reuse: the "
         "adversary names it in `reason` and leaves the test as it is.",),
    ),
    "ref-reuse-checks-existing-first": (
        "ref", "the adversary checks what already covers the target",
        "this change's programs under `docs/loom/<change-id>/evidence/probes/`",
        ("the repository's related tests",),
        "Before writing any probe, the adversary checks what already covers the target: this "
        "change's programs under `docs/loom/<change-id>/evidence/probes/` and the repository's related tests.",
        ("Before writing any probe, the adversary checks what already covers the target, not "
         "this change's programs under `docs/loom/<change-id>/evidence/probes/` and the repository's related tests.",),
    ),
    "ref-status-with-reason-for-new": (
        "ref", "marks each probe", "`reused`, `modified` or `new`",
        ("a one-line reason for every new one",),
        "Its report marks each probe `reused`, `modified` or `new`, with a one-line reason for every new one.",
        ("Its report marks each probe `reused`, `modified` or `new`, with no one-line reason for every new one.",
         "Its report marks each probe `reused`, `modified` or `new`."),
    ),
    "ref-update-own-programs": (
        "ref",
        "When Build re-dispatches it for a widened scope or for trunk content brought in by `sync-trunk`,",
        "the adversary updates only its own programs", ("fixes nothing in the product",),
        "When Build re-dispatches it for a widened scope or for trunk content brought in by "
        "`sync-trunk`, the adversary updates only its own programs and fixes nothing in the product.",
        ("When Build re-dispatches it for a widened scope or for trunk content brought in by "
         "`sync-trunk`, the adversary never updates only its own programs and fixes nothing in the "
         "product.",),
    ),
    "ref-defect-kept-and-reported": (
        "ref", "When a failing program caught a product defect,",
        "the adversary keeps that program unchanged and returns a finding",
        ("Build then fixes the product",),
        "When a failing program caught a product defect, the adversary keeps that program unchanged "
        "and returns a finding, and Build then fixes the product.",
        ("When a failing program caught a product defect, the adversary never keeps that program "
         "unchanged and returns a finding, and Build then fixes the product.",),
    ),
    "ref-mutation-restores-original-rejection": (
        "ref", "One mutation restores", "the original behaviour the stale program rejected",
        ("the updated probe must turn RED on it",),
        "One mutation restores the original behaviour the stale program rejected, and the updated "
        "probe must turn RED on it.",
        ("One mutation restores the original behaviour the stale program rejected, and the updated "
         "probe need not turn RED on it.",
         "One mutation restores the original behaviour the stale program rejected."),
    ),
    "ref-reuse-modify-then-new": (
        "ref", "It reuses a program that covers a case",
        "writes a new probe only when nothing covers the case",
        ("modifies one when a small change covers it",),
        "It reuses a program that covers a case, modifies one when a small change covers it, and "
        "writes a new probe only when nothing covers the case.",
        ("It never reuses a program that covers a case, modifies one when a small change covers it, "
         "and writes a new probe only when nothing covers the case.",
         "It may write new probes freely, modifies one when a small change covers it, and writes a "
         "new probe only when nothing covers the case."),
    ),
    "ref-mutation-evidence": (
        "ref", "Every update carries mutation evidence run",
        "against the committed probe program itself",
        ("at least one mutation per kind of change the update touches",
         "an over-broad update would wrongly accept"),
        "Every update carries mutation evidence run against the committed probe program itself: "
        "at least one mutation per kind of change the update touches, plus one that an over-broad "
        "update would wrongly accept.",
        ("Every update carries mutation evidence run against the committed probe program itself: "
         "at least one mutation per kind of change the update touches, plus no one that an "
         "over-broad update would wrongly accept.",
         "Every update carries mutation evidence run against the committed probe program itself: "
         "one mutation overall."),
    ),
    "ref-mutation-in-throwaway-copy-or-edit-tool": (
        "ref", "The adversary applies each mutation in", "a throwaway copy of the working tree",
        ("runs the committed probe program there unchanged",
         "applies and undoes the mutation with the host's edit tool"),
        "The adversary applies each mutation in a throwaway copy of the working tree, such as a "
        "temporary `git worktree add` or a `git archive` extract, and runs the committed probe "
        "program there unchanged, or applies and undoes the mutation with the host's edit tool.",
        ("The adversary applies each mutation in a throwaway copy of the working tree and runs the "
         "committed probe program there unchanged, or never applies and undoes the mutation with "
         "the host's edit tool.",
         "The adversary applies each mutation in the working tree and runs the committed probe "
         "program there unchanged."),
    ),
    "ref-copy-still-runs-own-assertion": (
        "ref", "Running the unchanged probe inside a copy of the tree",
        "still exercises its own assertion", ("unlike a copy of its logic",),
        "Running the unchanged probe inside a copy of the tree still exercises its own assertion, "
        "unlike a copy of its logic.",
        ("Running the unchanged probe inside a copy of the tree does not exercise its own "
         "assertion, unlike a copy of its logic.",),
    ),
    "ref-rewritten-case-counts-modified": (
        "ref", "A stale case that is rewritten or flipped to its positive form",
        "counts as `modified`", (),
        "A stale case that is rewritten or flipped to its positive form counts as `modified`.",
        ("A stale case that is rewritten or flipped to its positive form does not count as `modified`.",
         "A stale case that is rewritten or flipped to its positive form counts as `new`."),
    ),
}
UPDATE_NO_WEAKENING = "An update never deletes, skips or xfails a case to make it pass."
CODE_CHANGE_NOT_A_CASE = "If a case needs the code changed to fail, it is not a case."
NO_DISCARD_UNDO = (
    "Discard commands (`git checkout --`, `git restore`, `git reset --hard`, `git clean`, "
    "`git worktree remove --force`) are never used to undo a mutation, because host guards "
    "refuse them and they can destroy uncommitted work."
)
_PIN_DOCS = {"ref": ADVERSARIAL_REF}


@pytest.mark.parametrize("pin", sorted(PROTOCOL_PINS))
def test_probe_maintenance_pin_helpers_synthetic(pin: str) -> None:
    _doc, verb, literal, extras, affirmative, rejected = PROTOCOL_PINS[pin]
    assert _affirms(affirmative, verb, literal, *extras)
    assert any(has_negation(r) for r in rejected), pin
    for example in rejected:
        assert not _affirms(example, verb, literal, *extras), example


@pytest.mark.parametrize("pin", sorted(PROTOCOL_PINS))
def test_adversary_probe_maintenance_rule_stated(pin: str) -> None:
    doc, verb, literal, extras, _affirmative, _rejected = PROTOCOL_PINS[pin]
    assert _affirms(_PIN_DOCS[doc], verb, literal, *extras), (pin, verb, literal)


def test_update_no_weakening_helpers_synthetic() -> None:
    assert _pins_exact_sentence(f"Keep every case. {UPDATE_NO_WEAKENING}", UPDATE_NO_WEAKENING)
    assert not _pins_exact_sentence(
        "Keep every case. An update may delete, skip or xfail a case to make it pass.",
        UPDATE_NO_WEAKENING,
    )


def test_adversary_update_never_weakens_a_case() -> None:
    assert _pins_exact_sentence(ADVERSARIAL_REF, UPDATE_NO_WEAKENING), ADVERSARIAL_REF
    assert _pins_exact_sentence(ADVERSARIAL_REF, CODE_CHANGE_NOT_A_CASE), ADVERSARIAL_REF


def test_no_discard_undo_helpers_synthetic() -> None:
    assert _pins_exact_sentence(f"Undo in a copy. {NO_DISCARD_UNDO}", NO_DISCARD_UNDO)
    assert not _pins_exact_sentence(
        "Undo in a copy. Discard commands (`git checkout --`, `git restore`, `git reset --hard`, "
        "`git clean`) may be used to undo a mutation, because host guards refuse them and they "
        "can destroy uncommitted work.",
        NO_DISCARD_UNDO,
    )
    assert not _pins_exact_sentence(
        "Undo in a copy. Discard commands (`git checkout --`, `git restore`) are never used to "
        "undo a mutation.",
        NO_DISCARD_UNDO,
    )


def test_adversary_mutation_undo_uses_no_discard_command() -> None:
    assert _pins_exact_sentence(ADVERSARIAL_REF, NO_DISCARD_UNDO), ADVERSARIAL_REF


# --- One home for the protocol's rules: adversary.md repeats none of them ---

# Each fragment names one rule the protocol owns; it lives in this file and
# nowhere in adversary.md.
PROCEDURE_FRAGMENTS = (
    "already covers the target", "counts as reuse",
    "marks each probe", "counts as `modified`", "nothing in the product", "that program unchanged",
    "mutation evidence", "an over-broad update would wrongly accept",
    "the original behaviour the stale program rejected", "hold only committed content",
    "a throwaway copy of the working tree", "still exercises its own assertion", "removes that copy",
    "Discard commands", UPDATE_NO_WEAKENING,
    "an anecdote", "must be re-runnable", "needs the code changed to fail",
)


def _procedure_fragments_in_both(agent: str, ref: str) -> list[str]:
    return [f for f in PROCEDURE_FRAGMENTS if f in agent and f in ref]


def test_procedure_fragments_helper_synthetic() -> None:
    ref = "Before writing any probe, the adversary checks what already covers the target."
    assert _procedure_fragments_in_both("Read the reference first.", ref) == []
    duplicated = "Before you write any probe, check what already covers the target."
    assert _procedure_fragments_in_both(duplicated, ref) == ["already covers the target"]


def test_procedure_sentence_in_both_files_rejected() -> None:
    assert _procedure_fragments_in_both(ADVERSARY_PROSE, ADVERSARIAL_REF) == []
    assert [f for f in PROCEDURE_FRAGMENTS if f not in ADVERSARIAL_REF] == []


# --- The protocol places the adversary at the end of Build ------------------

def test_protocol_opening_and_recording_name_build_and_finalize() -> None:
    opening = " ".join(PROTOCOL_TEXT.split("\n## ", 1)[0].split())
    assert "at the end of Build" in opening
    assert "a later round can re-run it" not in opening
    recording = " ".join(PROTOCOL_TEXT.split("## Recording", 1)[1].split())
    assert "Build re-runs" in recording
    assert "`finalize-review`" in recording


def test_protocol_recording_sends_findings_to_the_finalize_input() -> None:
    recording = " ".join(PROTOCOL_TEXT.split("## Recording", 1)[1].split())
    destination = next(
        s for s in _colon_sentences(recording) if "`findings` input of `finalize-review`" in s
    )
    assert "closing review passes" in destination, destination
    assert not has_negation(destination), destination
