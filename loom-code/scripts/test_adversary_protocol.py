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

# The readers and the two matchers are `prose_pin`'s, under this module's own
# names: every recipe's test module and `test_build_mechanical_checks.py`
# carried byte-identical copies of them.
from prose_pin import (
    affirms as _affirms,
    flat_prose as _flat,
    has_negation,
    pins_exact_sentence as _pins_exact_sentence,
    rule_prose as _rules,
    split_sentences,
)


ROOT = Path(__file__).resolve().parents[2]
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
PROTOCOL = REFERENCES / "adversarial.md"
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


# The raw protocol, for the assertions that cut it at a heading; the flattened
# protocol, for the sentence pins; and `_rules`, the same with its heading
# lines dropped -- a heading is structure, and `test_adversary_layout.py` owns
# it.
PROTOCOL_TEXT = PROTOCOL.read_text(encoding="utf-8")
ADVERSARIAL_REF = _flat(PROTOCOL)
ADVERSARY_PROSE = _flat(ADVERSARY)
RULES = _rules(PROTOCOL)


def _colon_sentences(text: str) -> list[str]:
    return split_sentences(text, ends=".:;")  # colon is a boundary here


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
    # The duty is narrowed to the programs that graduated into the re-run
    # suite (Acceptance 7): a program that is run twice and never again buys
    # no protection a mutation could measure. The verb therefore opens at the
    # condition, so a rewrite that widens the duty back to every update turns
    # this pin red.
    "ref-mutation-evidence": (
        "ref", "Every update to a program that was carried into the suite that runs on every "
        "later change carries mutation evidence run",
        "against the committed probe program itself",
        ("at least one mutation per kind of change the update touches",
         "an over-broad update would wrongly accept"),
        "Every update to a program that was carried into the suite that runs on every later "
        "change carries mutation evidence run against the committed probe program itself: "
        "at least one mutation per kind of change the update touches, plus one that an over-broad "
        "update would wrongly accept.",
        ("Every update to a program that was carried into the suite that runs on every later "
         "change carries mutation evidence run against the committed probe program itself: "
         "at least one mutation per kind of change the update touches, plus no one that an "
         "over-broad update would wrongly accept.",
         "Every update to a program that was carried into the suite that runs on every later "
         "change carries mutation evidence run against the committed probe program itself: "
         "one mutation overall.",
         # The duty widened back to every update, the rest untouched.
         "Every update carries mutation evidence run against the committed probe program itself: "
         "at least one mutation per kind of change the update touches, plus one that an "
         "over-broad update would wrongly accept."),
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


# --- What the protocol says outside the reuse-and-mutation passage ----------
#
# The pins above cover `Reuse first, update with evidence`, which is most of
# the protocol. These cover the rest: what the adversary is for, stated in the
# opening; which recipe to read and what giving or taking away a recipe costs,
# stated under `Which recipe to read`; and how a probe and a finding are
# recorded, stated under `Recording`. Same two shapes -- an affirmative verb
# before the pinned literal with a negation in the same sentence rejected, and
# an exact sentence where the rule's own wording carries the negation.
#
# Each verb starts where the rule's own sentence starts, and each pin's
# rejected list carries that sentence with its opening words exchanged. A pin
# whose verb opens mid-sentence leaves the words before it unwatched, and the
# change's own adversary reworded exactly those words in a recipe and saw
# nothing go red (FINDING unpinned-recipe); the rules of `Which recipe to
# read` and the two `Recording` rules below were unwatched the same way when
# that measurement was extended to every rule sentence of all four files.

# name: (verb, literal, extras, affirmative example, rejected examples)
RULE_PINS = {
    "protocol-the-job-is-to-make-the-change-fail": (
        "It is", "to make the change fail", (),
        "It is to make the change fail.",
        ("It is not to make the change fail.",
         "It is to report what looks risky."),
    ),
    "protocol-everything-run-is-committed-as-a-program": (
        "It runs at the end of Build", "everything it runs is committed as a program",
        ("Build re-runs those programs on every fix loop",
         "`finalize-review` executes them on committed content"),
        "It runs at the end of Build, and everything it runs is committed as a program: "
        "Build re-runs those programs on every fix loop, and `finalize-review` executes "
        "them on committed content.",
        ("It runs at the end of Build, and everything it runs is committed as a program, "
         "but `finalize-review` does not execute them on committed content and Build "
         "re-runs those programs on every fix loop.",
         "It runs at the end of Build, and everything it runs is committed as a program."),
    ),
    "protocol-artifact-type-comes-from-the-manifest": (
        "Every changed path has", "an artifact type",
        ("from the `artifact_types` list in `contract/manifest.yaml`",),
        "Every changed path has an artifact type, from the `artifact_types` list in "
        "`contract/manifest.yaml`.",
        ("Every changed path has an artifact type, but not from the `artifact_types` list "
         "in `contract/manifest.yaml`.",
         "Every path changed has an artifact type, from the `artifact_types` list in "
         "`contract/manifest.yaml`.",
         "Every changed path has an artifact type."),
    ),
    "protocol-protocol-plus-matching-recipes-is-the-whole-procedure": (
        "Read this protocol",
        "then the recipe file this table names for every artifact type among the changed paths",
        ("that protocol and those recipes are the whole procedure",),
        "Read this protocol, then the recipe file this table names for every artifact type "
        "among the changed paths: that protocol and those recipes are the whole procedure, "
        "and there is nothing else to find.",
        ("Read this protocol, then the recipe file this table names for every artifact type "
         "among the changed paths: that protocol and those recipes are not the whole "
         "procedure.",
         "Read protocol this, then the recipe file this table names for every artifact type "
         "among the changed paths: that protocol and those recipes are the whole procedure.",
         "Read this protocol, then the recipe file this table names for every artifact type "
         "among the changed paths."),
    ),
    "protocol-giving-a-type-a-recipe-is-one-file-and-one-row": (
        "Giving a type a recipe is", "one new file beside this one plus its own row here", (),
        "Giving a type a recipe is one new file beside this one plus its own row here.",
        ("Giving a type a recipe is not one new file beside this one plus its own row here.",
         "Giving type a a recipe is one new file beside this one plus its own row here.",
         "Giving a type a recipe is a new section in this file."),
    ),
    "protocol-taking-a-recipe-away-resets-the-row": (
        "Taking one away", "deletes its file",
        ("deletes the test module named after that kind where it has one",
         "puts its row back to `none`"),
        "Taking one away deletes its file, deletes the test module named after that kind "
        "where it has one, and puts its row back to `none`.",
        ("Taking one away never deletes its file, deletes the test module named after that "
         "kind where it has one, and puts its row back to `none`.",
         "Taking away one deletes its file, deletes the test module named after that kind "
         "where it has one, and puts its row back to `none`.",
         "Taking one away deletes its file and puts its row back to `none`.",
         "Taking one away deletes its file."),
    ),
    "protocol-reuse-is-checked-before-any-probe-is-written": (
        "Before writing any probe", "the adversary checks what already covers the target",
        ("this change's programs under `docs/loom/<change-id>/evidence/probes/`",
         "the repository's related tests"),
        "Before writing any probe, the adversary checks what already covers the target: "
        "this change's programs under `docs/loom/<change-id>/evidence/probes/` and the "
        "repository's related tests.",
        ("Before writing any probe, the adversary checks what already covers the target: "
         "this change's programs under `docs/loom/<change-id>/evidence/probes/` and not the "
         "repository's related tests.",
         "Before any writing probe, the adversary checks what already covers the target: "
         "this change's programs under `docs/loom/<change-id>/evidence/probes/` and the "
         "repository's related tests.",
         "Before writing any probe, the adversary checks what already covers the target."),
    ),
    "protocol-build-names-and-re-runs-every-committed-program": (
        "Build's hand-off names", "every committed program",
        ("Build re-runs each one on every fix loop",),
        "Build's hand-off names every committed program, and Build re-runs each one on "
        "every fix loop.",
        ("Build's hand-off names every committed program, and Build re-runs each one on "
         "every fix loop, though not on the last one.",
         "Build's names hand-off every committed program, and Build re-runs each one on "
         "every fix loop.",
         "Build's hand-off names every committed program."),
    ),
    "protocol-closing-review-supplies-the-programs-to-finalize-review": (
        "Closing review supplies", "them to `finalize-review`",
        ("executes each one and records the command, artifact, functional-content digest "
         "and observed result in the generated attestation",),
        "Closing review supplies them to `finalize-review`, which executes each one and "
        "records the command, artifact, functional-content digest and observed result in "
        "the generated attestation.",
        ("Closing review supplies them to `finalize-review`, which executes each one and "
         "records the command, artifact, functional-content digest and observed result in "
         "the generated attestation, and never runs them again.",
         "Closing supplies review them to `finalize-review`, which executes each one and "
         "records the command, artifact, functional-content digest and observed result in "
         "the generated attestation.",
         "Closing review supplies them to `finalize-review`."),
    ),
    "protocol-artifact-is-where-the-case-now-lives": (
        "`artifact` is", "where the case now lives", (),
        "- `artifact` is where the case now lives.",
        ("- `artifact` is not where the case now lives.",
         "- is `artifact` where the case now lives.",
         "- `artifact` is a label."),
    ),
    "protocol-every-failed-attempt-is-recorded": (
        "Record every attempt that failed to break anything", "for every artifact type",
        ("an eval rather than an anecdote",),
        "Record every attempt that failed to break anything, for every artifact type — "
        "that is what makes the attempts an eval rather than an anecdote.",
        ("Record no attempt that failed to break anything, for every artifact type — that "
         "is what makes the attempts an eval rather than an anecdote.",
         "Record every attempt that failed to break anything, for every artifact type."),
    ),
    "protocol-command-is-rerunnable-in-a-clean-tree": (
        "`command` must be", "re-runnable by someone else in a clean tree", (),
        "`command` must be re-runnable by someone else in a clean tree.",
        ("`command` must be re-runnable by someone else, but not in a clean tree.",
         "`command` must be recorded."),
    ),
    "protocol-probes-live-under-the-evidence-path": (
        "Put probes under", "`docs/loom/<change-id>/evidence/probes/`",
        ("that path is the `evidence` artifact type",),
        "Put probes under `docs/loom/<change-id>/evidence/probes/` — that path is the "
        "`evidence` artifact type.",
        ("Put probes under `docs/loom/<change-id>/evidence/probes/` — that path is not the "
         "`evidence` artifact type.",
         "Put probes under `docs/loom/<change-id>/evidence/probes/`."),
    ),
    "protocol-promotion-only-through-a-plan-task": (
        "Promote a probe into the repo's real test suite", "only through a plan task", (),
        "Promote a probe into the repo's real test suite only through a plan task.",
        ("Promote a probe into the repo's real test suite, not only through a plan task.",
         "Promote a probe into the repo's real test suite whenever it is stable."),
    ),
    "protocol-a-finding-carries-an-anchor-and-a-fix": (
        "Anything the adversary found that matters becomes",
        "a `finding` with an anchor and a fix", (),
        "Anything the adversary found that matters becomes a `finding` with an anchor and a fix.",
        ("Anything the adversary found that matters becomes a `finding` with an anchor and "
         "no fix.",
         "Anything the adversary found that matters becomes a note in the report."),
    ),
    "protocol-build-fixes-findings-before-hand-off": (
        "Build fixes every fatal or important finding", "before hand-off",
        ("lists any left unresolved in its hand-off",),
        "Build fixes every fatal or important finding before hand-off and lists any left "
        "unresolved in its hand-off.",
        ("Build fixes every fatal or important finding, though not before hand-off, and "
         "lists any left unresolved in its hand-off.",
         "Build fixes every fatal or important finding before hand-off."),
    ),
}

# name: (sentence, rewrites that must fail)
RULE_SENTENCE_PINS = {
    "protocol-a-type-with-no-recipe-is-attacked-with-the-protocol-alone": (
        "A type whose row says `none` has no recipe today — attack it with this protocol "
        "alone, and say in the report that it has none.",
        ("A type whose row says `none` has a recipe today — attack it with this protocol "
         "alone, and say in the report that it has none.",
         "A type whose row says `none` has no recipe today — attack it with this protocol "
         "alone.",
         "A whose type row says `none` has no recipe today — attack it with this protocol "
         "alone, and say in the report that it has none."),
    ),
    # The clause after the semicolon in `Giving a type a recipe is one new
    # file beside this one plus its own row here; no existing recipe file is
    # edited.` -- the semicolon makes it its own unit, and its own wording
    # carries the negation, so the affirmative matcher cannot hold it.
    "protocol-no-existing-recipe-is-edited": (
        "no existing recipe file is edited.",
        ("an existing recipe file is edited.",
         "no existing recipe file is edited unless the new kind needs it.",
         "no recipe file is edited."),
    ),
    "protocol-not-a-second-review": (
        "The adversary's job is not to find bugs the reviewers might also find.",
        ("The adversary's job is to find bugs the reviewers might also find.",
         "The adversary's job is not only to find bugs the reviewers might also find.",
         "The adversary's job is not to find bugs."),
    ),
}


@pytest.mark.parametrize("pin", sorted(RULE_PINS))
def test_rule_pin_helpers_synthetic(pin: str) -> None:
    verb, literal, extras, affirmative, rejected = RULE_PINS[pin]
    assert _affirms(affirmative, verb, literal, *extras), pin
    assert any(has_negation(r) for r in rejected), pin
    for example in rejected:
        assert not _affirms(example, verb, literal, *extras), example


@pytest.mark.parametrize("pin", sorted(RULE_PINS))
def test_protocol_affirms_the_rule(pin: str) -> None:
    verb, literal, extras, _affirmative, _rejected = RULE_PINS[pin]
    assert _affirms(RULES, verb, literal, *extras), (pin, verb, literal)


@pytest.mark.parametrize("pin", sorted(RULE_SENTENCE_PINS))
def test_rule_sentence_pin_helpers_synthetic(pin: str) -> None:
    sentence, rejected = RULE_SENTENCE_PINS[pin]
    assert _pins_exact_sentence(f"Read this first. {sentence}", sentence), pin
    for example in rejected:
        assert not _pins_exact_sentence(f"Read this first. {example}", sentence), example


@pytest.mark.parametrize("pin", sorted(RULE_SENTENCE_PINS))
def test_protocol_states_the_rule(pin: str) -> None:
    sentence, _rejected = RULE_SENTENCE_PINS[pin]
    assert _pins_exact_sentence(RULES, sentence), (pin, sentence)


# --- The protocol places the adversary at the end of Build ------------------

def test_protocol_opening_and_recording_name_build_and_finalize() -> None:
    opening = " ".join(PROTOCOL_TEXT.split("\n## ", 1)[0].split())
    assert "at the end of Build" in opening
    assert "a later round can re-run it" not in opening
    recording = " ".join(PROTOCOL_TEXT.split("## Recording", 1)[1].split())
    assert "Build re-runs" in recording
    assert "`finalize-review`" in recording


# --- The case count is a ceiling, stated here and nowhere else --------------
#
# Acceptance 8 and 9 of
# `docs/loom/intent/2026-09-23-adversarial-probes-earn-their-place.md`, as the
# intent reads after the floor was dropped. Two rules, and the scan below
# answers both:
#
# 1. No runtime file states a minimum number of cases at all. The floor is
#    what made the adversary produce volume: it set a number with no relevance
#    test. What it guarded against is answered by the `concern:` line every
#    program carries and by the reviewers who read the findings. So a floor is
#    a defect wherever it is written, the allowed restatements included.
# 2. How many cases a change may commit -- the ceiling -- is a rule of this
#    protocol and of no other runtime file. Four documents may restate it in
#    their own words: the agent contract's frontmatter, which is trigger text
#    a dispatcher reads, and the two translated READMEs, the English README
#    and the conventions file, which are indexes. Each is held to agreeing
#    with the source, so a ceiling that is not five contradicts it.
#
# The scan reads a bound and its number together ("at least three", "≥3",
# "3 つ以上", "至多五個") rather than a pinned sentence, because a restatement
# is free to reword everything except the number it states.

CAP = 5
FLOOR_BOUND, CAP_BOUND = "floor", "cap"

SKILLS = ROOT / "loom-code/skills"
AGENTS = ROOT / "loom-code/agents"
# Restatements the intent allows, each read whole except the agent contract,
# whose body is runtime prose like any other and whose frontmatter is the
# trigger text.
RESTATEMENTS = (
    ROOT / "loom-code/README.md",
    ROOT / "loom-code/README.ja.md",
    ROOT / "loom-code/README.zh-TW.md",
    ROOT / "AGENTS.md",
)

_NUMBERS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "一": 1, "二": 2, "三": 3, "四": 4, "五": 5,
    "六": 6, "七": 7, "八": 8, "九": 9, "十": 10,
}
_NUM = r"(?:\d+|one|two|three|four|five|six|seven|eight|nine|ten|[一二三四五六七八九十])"
_BOUND_BEFORE = {
    "at least": FLOOR_BOUND, "no fewer than": FLOOR_BOUND, "至少": FLOOR_BOUND,
    "≥": FLOOR_BOUND, "at most": CAP_BOUND, "no more than": CAP_BOUND,
    "up to": CAP_BOUND, "至多": CAP_BOUND, "最多": CAP_BOUND, "≤": CAP_BOUND,
}
_BOUND_AFTER = {"以上": FLOOR_BOUND, "以下": CAP_BOUND}
_COUNT_RE = re.compile(
    rf"(?P<pre>{'|'.join(_BOUND_BEFORE)})\s*\**\s*(?P<n1>{_NUM})"
    rf"|(?P<n2>{_NUM})\s*(?:つ|個|件|の)?\s*(?P<post>{'|'.join(_BOUND_AFTER)})",
    re.IGNORECASE,
)
# What the number has to be counting for the match to be this rule and not
# another one: an adversarial case, probe or program. It is looked for beside
# the number, not anywhere in the paragraph -- "at least one mutation per kind
# of change" sits in a paragraph about probe programs and counts mutations,
# and a table row's number belongs to its own row. The window reaches further
# forward than back because English and Chinese put the noun after the number
# ("at least three cases", "至少三個案例") and Japanese puts it before
# ("境界ケース 3 つ以上").
_CASE_NOUN = re.compile(r"\bcases?\b|\bprobes?\b|\bprograms?\b|ケース|案例", re.IGNORECASE)
_BACK, _FORWARD = 12, 60


def _number(token: str) -> int:
    return int(token) if token.isdigit() else _NUMBERS[token.lower()]


def _units(text: str) -> list[str]:
    """The text in the units a rule is stated in: paragraphs, and each table
    row on its own, so that no window below reaches out of one row into the
    next."""
    units: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        lines = paragraph.splitlines()
        units += [ln for ln in lines if ln.lstrip().startswith("|")]
        units.append(" ".join(ln for ln in lines if not ln.lstrip().startswith("|")))
    return [" ".join(unit.split()) for unit in units if unit.strip()]


def case_counts(text: str) -> set[tuple[str, int]]:
    """Every (bound, number) pair the text states about cases, `floor` or `cap`."""
    found: set[tuple[str, int]] = set()
    for unit in _units(text):
        for match in _COUNT_RE.finditer(unit):
            window = unit[max(0, match.start() - _BACK):match.end() + _FORWARD]
            if not _CASE_NOUN.search(window):
                continue
            if match.group("pre"):
                found.add((_BOUND_BEFORE[match.group("pre").lower()], _number(match.group("n1"))))
            else:
                found.add((_BOUND_AFTER[match.group("post")], _number(match.group("n2"))))
    return found


def _body(path: Path) -> str:
    """The file without a YAML frontmatter block, which is trigger text."""
    text = path.read_text(encoding="utf-8")
    if text.startswith("---\n") and "\n---\n" in text[4:]:
        return text[4:].split("\n---\n", 1)[1]
    return text


def _frontmatter(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    return text[4:].split("\n---\n", 1)[0] if text.startswith("---\n") else ""


def runtime_prose_files() -> list[Path]:
    """Every runtime prose file of loom-code that is not the source."""
    return sorted(
        p for p in list(SKILLS.rglob("*.md")) + list(AGENTS.glob("*.md"))
        if p != PROTOCOL
    )


def test_case_counts_reads_every_wording_synthetic() -> None:
    assert case_counts("write at least three cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("write **at least three** cases") == {(FLOOR_BOUND, 3)}
    assert case_counts("実行可能な境界ケース 3 つ以上を書く") == {(FLOOR_BOUND, 3)}
    assert case_counts("至少三個可執行的邊界案例") == {(FLOOR_BOUND, 3)}
    assert case_counts("≥3 個可執行的邊界案例") == {(FLOOR_BOUND, 3)}
    assert case_counts("a change commits at most five probe programs") == {(CAP_BOUND, 5)}
    assert case_counts("at most four cases") == {(CAP_BOUND, 4)}


def test_case_counts_ignores_a_count_of_something_else_synthetic() -> None:
    """A number beside another noun is not a count of cases."""
    assert case_counts("when it reports `up to date`, continue") == set()
    assert case_counts("the episode admits at most three distinct digests") == set()
    assert case_counts(
        "mutation evidence run against the committed probe program itself: at least "
        "one mutation per kind of change the update touches"
    ) == set()
    # A table row's number belongs to its own row, not to the row above it.
    table = "| **read** | ≥2 fresh-context reviewers | verdict |\n| **attack** | cases |\n"
    assert case_counts(table) == set()


def test_body_and_frontmatter_helpers_synthetic() -> None:
    path = ADVERSARY
    assert _frontmatter(path).startswith("name: adversary"), _frontmatter(path)[:40]
    assert "name: adversary" not in _body(path)
    assert _body(path).lstrip().startswith("# adversary subagent")


def test_protocol_states_the_ceiling_and_no_floor() -> None:
    assert case_counts(PROTOCOL_TEXT) == {(CAP_BOUND, CAP)}


def test_no_runtime_prose_states_a_minimum_case_count() -> None:
    """Rule 1: a floor is a defect wherever it is written.

    Every runtime prose file, the protocol and the four allowed restatements
    included, because a restatement may keep its own words but not reintroduce
    the number the intent removed.
    """
    read = {PROTOCOL: PROTOCOL_TEXT, ADVERSARY: ADVERSARY.read_text(encoding="utf-8")}
    read |= {path: path.read_text(encoding="utf-8") for path in RESTATEMENTS}
    read |= {path: path.read_text(encoding="utf-8") for path in runtime_prose_files()}
    floors = {
        str(path.relative_to(ROOT)): sorted(n for bound, n in case_counts(text) if bound == FLOOR_BOUND)
        for path, text in read.items()
        if any(bound == FLOOR_BOUND for bound, _ in case_counts(text))
    }
    assert floors == {}, floors


def test_no_second_statement_of_the_case_count_in_runtime_prose() -> None:
    """Rule 2: the ceiling is stated in the protocol and in no other runtime
    file. A recipe, a station or an agent body that states a number of cases
    again is a second place to keep right."""
    second = {
        str(path.relative_to(ROOT)): sorted(case_counts(_body(path)))
        for path in runtime_prose_files()
        if case_counts(_body(path))
    }
    assert second == {}, second


def test_no_restatement_contradicts_the_source() -> None:
    allowed = {(CAP_BOUND, CAP)}
    sources = {str(p.relative_to(ROOT)): p.read_text(encoding="utf-8") for p in RESTATEMENTS}
    sources["loom-code/agents/adversary.md frontmatter"] = _frontmatter(ADVERSARY)
    contradicting = {
        name: sorted(case_counts(text) - allowed)
        for name, text in sources.items()
        if case_counts(text) - allowed
    }
    assert contradicting == {}, contradicting


def test_protocol_recording_sends_findings_to_the_finalize_input() -> None:
    recording = " ".join(PROTOCOL_TEXT.split("## Recording", 1)[1].split())
    destination = next(
        s for s in _colon_sentences(recording) if "`findings` input of `finalize-review`" in s
    )
    assert "closing review passes" in destination, destination
    assert not has_negation(destination), destination
