"""Build ends with a fresh adversary, the package suite and adversarial programs."""

import re
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences as _sentences


ROOT = Path(__file__).resolve().parents[2]
BUILD = (ROOT / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
PROSE = " ".join(BUILD.split())
VERIFY = " ".join(BUILD.split("## 3. Verify integration", 1)[1].split("## 4.", 1)[0].split())
HANDOFF = " ".join(BUILD.split("## 4. Hand off to closing-review", 1)[1].split())
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


def _sentence(text: str, fragment: str) -> str:
    return next(s for s in _sentences(text) if fragment in s)


def test_build_dispatches_fresh_adversary_then_suite_after_tasks() -> None:
    tasks_land = VERIFY.index("After all tasks land")
    dispatch = VERIFY.index("Dispatch the `loom-code:adversary` agent fresh-context")
    suite = VERIFY.index("Run the repository's complete package suite, then each committed adversarial program")
    assert tasks_land < dispatch < suite
    sentence = _sentence(VERIFY, "Dispatch the `loom-code:adversary` agent fresh-context")
    assert "§2 requires before every host-native dispatch" in sentence
    assert not has_negation(sentence), sentence
    assert "Never dispatch an agent that implemented any part of the change." in VERIFY
    assert "The adversary writes and commits its adversarial programs." in VERIFY
    description = ADVERSARY.read_text(encoding="utf-8").split("\n", 3)[2]
    assert "by the build station" in description
    assert "review station" not in description


def test_adversary_prompt_carries_no_implementer_explanation() -> None:
    assert (
        "Give it only the change id, `HEAD`, and paths: the intent, the plan, and the "
        "changed paths with their artifact types"
    ) in VERIFY
    assert "never pass an implementer's explanation of its own code" in VERIFY
    for leak in ("implementer's report", "implementer's summary", "self_review"):
        assert leak not in VERIFY


GATE = (
    "Build does not hand off to `closing-review` until the complete package suite has passed or "
    "`selection show` lists `package-tests` as skipped, and until every adversarial "
    "program has passed or it lists `adversarial` as skipped, each skip waiving only "
    "its own check."
)
ADVERSARY_FINDINGS = (
    "Every fatal or important finding the adversary returns is fixed inside Build like "
    "a failing check before hand-off, and any finding left unresolved is listed in the "
    "§4 hand-off."
)
_HANDOFF = re.compile(r"\bhand(?:s|ed|ing)?[ -]off\b", re.IGNORECASE)
_OPTIONAL = re.compile(
    r"\b(?:optional(?:ly)?|may|might|if (?:needed|time permits)|at (?:your|its) discretion)\b",
    re.IGNORECASE,
)


def _extra_handoff_sentences(section: str) -> list[str]:
    """Sentences about handing off to closing-review other than the pinned gate pair."""
    return [
        s for s in _sentences(section)
        if _HANDOFF.search(s) and s not in (GATE, ADVERSARY_FINDINGS)
    ]


def _optional_sentences(section: str) -> list[str]:
    return [s for s in _sentences(section) if _OPTIONAL.search(s)]


def test_handoff_helpers_synthetic() -> None:
    assert _extra_handoff_sentences(f"{GATE} {ADVERSARY_FINDINGS}") == []
    escape = "When the diff is small, hand off to `closing-review` while the suite is still running."
    assert _extra_handoff_sentences(f"{GATE} {escape}") == [escape]
    assert _optional_sentences("Run the complete package suite.") == []
    assert _optional_sentences("Optionally run the complete package suite.")


def test_build_allows_complete_suite_at_end() -> None:
    assert VERIFY.count(GATE) == 1
    assert _extra_handoff_sentences(VERIFY) == []
    assert _optional_sentences(VERIFY) == []
    assert "`finalize-review` still executes both once more on committed content." in VERIFY
    assert "complete package suite command and its result" in HANDOFF
    assert "each adversarial program's path and command" in HANDOFF


def test_adversary_findings_fixed_or_handed_off() -> None:
    assert VERIFY.count(ADVERSARY_FINDINGS) == 1
    assert not has_negation(ADVERSARY_FINDINGS), ADVERSARY_FINDINGS
    assert not _OPTIONAL.search(ADVERSARY_FINDINGS), ADVERSARY_FINDINGS
    assert "every unresolved adversary finding" in HANDOFF


def test_no_speculative_preflight_ban_remains() -> None:
    assert "speculative push preflight" not in PROSE
    assert "owns its one content-bound execution" not in PROSE
    for sentence in _sentences(PROSE):
        if "complete package suite" in sentence and has_negation(sentence):
            assert "does not hand off" in sentence or "skipped" in sentence, sentence


def test_rerun_trigger_covers_every_fix() -> None:
    assert VERIFY.count("Repeat these end-of-Build checks after every fix:") == 1
    sentence = _sentence(VERIFY, "Repeat these end-of-Build checks after every fix")
    assert "run the complete package suite and re-run the existing adversarial programs" in sentence
    assert not has_negation(sentence), sentence
    assert not _OPTIONAL.search(sentence), sentence
    assert "Do not dispatch the adversary again." not in VERIFY
    assert VERIFY.count(ORDINARY_FIX_NO_REDISPATCH) == 1, VERIFY


ORDINARY_FIX_NO_REDISPATCH = (
    "After a fix where every adversarial program still passes, or fails only for a "
    "product defect, do not dispatch the adversary again."
)
NO_OTHER_ROLE_EDITS_PROGRAM = (
    "Implementers and the orchestrator never edit an adversarial program."
)


def _names_stale_program_redispatch(section: str) -> bool:
    """One affirmative sentence re-dispatches the adversary to update its own
    programs when a widened scope makes one stale."""
    return any(
        "widens or changes what the change covers" in s
        and "Build dispatches the `loom-code:adversary` agent fresh-context again "
        "to update its own programs" in s
        and not has_negation(s)
        for s in _sentences(section)
    )


def _pins_exact_sentence(section: str, sentence: str) -> bool:
    return _sentences(section).count(sentence) == 1


def test_stale_program_redispatch_helpers_synthetic() -> None:
    affirmative = (
        "When a fix widens or changes what the change covers and a committed adversarial "
        "program fails for that reason, Build dispatches the `loom-code:adversary` agent "
        "fresh-context again to update its own programs."
    )
    negated = affirmative.replace("When a fix", "Never, when a fix")
    assert _names_stale_program_redispatch(affirmative)
    assert not _names_stale_program_redispatch(negated)
    assert _pins_exact_sentence(f"Run checks. {NO_OTHER_ROLE_EDITS_PROGRAM}", NO_OTHER_ROLE_EDITS_PROGRAM)
    assert not _pins_exact_sentence(
        "Run checks. Implementers and the orchestrator may edit an adversarial program.",
        NO_OTHER_ROLE_EDITS_PROGRAM,
    )
    assert _pins_exact_sentence(f"Run checks. {ORDINARY_FIX_NO_REDISPATCH}", ORDINARY_FIX_NO_REDISPATCH)
    assert not _pins_exact_sentence(
        "Run checks. After a fix where every adversarial program still passes, or fails only "
        "for a product defect, dispatch the adversary again.",
        ORDINARY_FIX_NO_REDISPATCH,
    )


def test_build_redispatches_adversary_for_stale_programs() -> None:
    assert _names_stale_program_redispatch(VERIFY), VERIFY
    inputs = _sentence(VERIFY, "the widened changed paths")
    assert "the failing program's output" in inputs
    assert not has_negation(inputs), inputs
    assert _sentence(VERIFY, "The adversary updates only its own programs") == (
        "The adversary updates only its own programs."
    )
    assert "each adversary re-dispatch with its reason" in HANDOFF
    assert "the adversary never fixes what it breaks" in VERIFY


_OTHER_ROLE = re.compile(r"\b(?:implementers?|orchestrators?)\b", re.IGNORECASE)
_EDIT_VERB = re.compile(r"\b(?:edit|modif|rewrit|update)", re.IGNORECASE)


def _other_role_program_edit_sentences(text: str) -> list[str]:
    """Sentences, other than the pinned prohibition, naming another role editing a program."""
    return [
        s for s in _sentences(text)
        if s != NO_OTHER_ROLE_EDITS_PROGRAM
        and _OTHER_ROLE.search(s)
        and _EDIT_VERB.search(s)
        and "adversarial program" in s
    ]


def test_other_role_program_edit_helper_synthetic() -> None:
    legit = f"The adversary updates only its own programs. {NO_OTHER_ROLE_EDITS_PROGRAM}"
    assert _other_role_program_edit_sentences(legit) == []
    override = "When time is short, the orchestrator rewrites a stale adversarial program itself."
    assert _other_role_program_edit_sentences(f"{legit} {override}") == [override]


def test_no_other_role_edits_adversarial_program() -> None:
    assert _pins_exact_sentence(VERIFY, NO_OTHER_ROLE_EDITS_PROGRAM), VERIFY
    assert PROSE.count("edit an adversarial program") == 1
    for text in (VERIFY, ADVERSARY_PROSE, ADVERSARIAL_REF):
        assert _other_role_program_edit_sentences(text) == []


def test_ordinary_fix_reruns_programs_without_redispatch() -> None:
    assert _pins_exact_sentence(VERIFY, ORDINARY_FIX_NO_REDISPATCH), VERIFY
    rerun = VERIFY.index("Repeat these end-of-Build checks after every fix:")
    assert rerun < VERIFY.index(ORDINARY_FIX_NO_REDISPATCH)


def test_returned_change_only_trigger_absent() -> None:
    assert (
        "When closing review or a failed `finalize-review` returns the change to Build"
        not in VERIFY
    )


STEP_3 = VERIFY.split("3. Run the repository's complete package suite", 1)[1].split(
    "When a check fails", 1
)[0]


SUITE_NONE = "when it is `none`, `selection show` must list `package-tests` as skipped."


def _names_suite_command(step: str) -> bool:
    """The suite-command sentence names the declared value and the absent fallback, affirmatively."""
    sentence = next(
        (s for s in _sentences(step)
         if "`package-tests:`" in s and "`docs/loom/KICKOFF-DEFAULTS.md`" in s),
        None,
    )
    return (
        sentence is not None
        and sentence.startswith("The suite command is")
        and "`package-tests:` value in" in sentence
        and "when absent, the command detected from build markers" in sentence
        and not has_negation(sentence)
    )


def test_suite_command_names_package_tests_declaration() -> None:
    assert _names_suite_command(STEP_3), STEP_3
    assert STEP_3.count(SUITE_NONE) == 1, STEP_3
    assert not has_negation(SUITE_NONE)
    assert not _OPTIONAL.search(SUITE_NONE)


def test_suite_step_without_command_source_fails() -> None:
    accepted = (
        "Run the repository's complete package suite, then each committed adversarial "
        "program. The suite command is the `package-tests:` value in "
        "`docs/loom/KICKOFF-DEFAULTS.md`, or, when absent, the command detected from "
        "build markers; " + SUITE_NONE
    )
    rejected = "Run the repository's complete package suite, then each committed adversarial program."
    negated = accepted.replace("The suite command is the", "The suite command is not the")
    assert _names_suite_command(accepted)
    assert not _names_suite_command(rejected)
    assert not _names_suite_command(negated)


def test_skipped_selection_step_omits_that_check() -> None:
    read = (
        "run `loom_checker.py selection show <change-id>` and omit only the steps it lists "
        "as skipped (spec, plan, implementer, tdd, adversarial, package-tests, blind-run)"
    )
    assert PROSE.count(read) == 1
    assert (
        "When `selection show` lists `adversarial` as skipped, dispatch no adversary and "
        "run no adversarial program."
    ) in VERIFY
    assert (
        "When it lists `package-tests` as skipped, run no complete package suite."
    ) in VERIFY


# --- The adversary updates its own programs with evidence and reuses first ---

def _flat(path: Path) -> str:
    return " ".join(re.sub(r"^> ?", "", path.read_text(encoding="utf-8"), flags=re.M).split())


ADVERSARY_PROSE = _flat(ADVERSARY)
ADVERSARIAL_REF = _flat(ROOT / "loom-code/skills/closing-review/references/adversarial.md")
UPDATE_NO_WEAKENING = "An update never deletes, skips or xfails a case to make it pass."
PROBES_FIELD = re.compile(
    r"^probes: \[\{artifact: .+, status: reused \| modified \| new, reason: .+\}\]$", re.M
)


def _affirms(text: str, verb: str, literal: str, *extras: str) -> bool:
    """Some sentence carries `verb` before `literal`, every extra, and no negation."""
    for s in _sentences(text):
        v, lit = s.find(verb), s.find(literal)
        if 0 <= v < lit and all(e in s for e in extras) and not has_negation(s):
            return True
    return False


# (doc, verb, literal, extras, affirmative example, rejected examples)
PROBE_MAINTENANCE_PINS = {
    "role-updates-own-programs": (
        "adversary", "You fix nothing you attack, and you",
        "update only your own programs when Build re-dispatches you", (),
        "You fix nothing you attack, and you update only your own programs when Build re-dispatches you.",
        ("You fix nothing you attack, and you never update only your own programs when Build re-dispatches you.",),
    ),
    "update-scope": (
        "adversary",
        "When Build re-dispatches you for a widened scope or for trunk content brought in by `sync-trunk`,",
        "update only the programs you committed for this change", ("fix nothing in the product",),
        "When Build re-dispatches you for a widened scope or for trunk content brought in by "
        "`sync-trunk`, update only the programs you committed for this change, and still fix "
        "nothing in the product.",
        ("When Build re-dispatches you for a widened scope or for trunk content brought in by "
         "`sync-trunk`, do not update only the programs you committed for this change, and still "
         "fix nothing in the product.",),
    ),
    "defect-kept-and-reported": (
        "adversary", "When a failing program caught a product defect,",
        "keep that program unchanged and return a finding", ("Build then fixes the product",),
        "When a failing program caught a product defect, keep that program unchanged and return a "
        "finding, and Build then fixes the product.",
        ("When a failing program caught a product defect, do not keep that program unchanged and "
         "return a finding, and Build then fixes the product.",),
    ),
    "mutation-restores-original-rejection": (
        "adversary", "Include one mutation that restores",
        "the original behaviour the stale program rejected",
        ("the updated probe must turn RED on it",),
        "Include one mutation that restores the original behaviour the stale program rejected, and "
        "the updated probe must turn RED on it.",
        ("Include one mutation that restores the original behaviour the stale program rejected, and "
         "the updated probe need not turn RED on it.",
         "Include one mutation that restores the original behaviour the stale program rejected."),
    ),
    "branch-tests-excluded-from-floor": (
        "adversary", "Reuse toward the three-case floor counts",
        "(a) the programs you committed for this change",
        ("(b) tests that exist unchanged outside this change's branch",),
        "Reuse toward the three-case floor counts only (a) the programs you committed for this "
        "change and (b) tests that exist unchanged outside this change's branch.",
        ("Reuse toward the three-case floor counts not only (a) the programs you committed for "
         "this change and (b) tests that exist unchanged outside this change's branch.",
         "Reuse toward the three-case floor counts (a) the programs you committed for this change "
         "and (b) any test on this change's branch."),
    ),
    "branch-tests-named-related-coverage": (
        "adversary", "Name any other test added or changed on the branch",
        "as related coverage only", ("such as an implementer's pin",),
        "Name any other test added or changed on the branch, such as an implementer's pin, as "
        "related coverage only.",
        ("Name any other test added or changed on the branch, such as an implementer's pin, not "
         "as related coverage only.",
         "Name any other test added or changed on the branch, such as an implementer's pin, as "
         "floor coverage."),
    ),
    "commit-before-copy": (
        "adversary", "Commit the updated probe", "before you make a copy",
        ("because `git worktree add` and `git archive` hold only committed content",
         "an uncommitted update takes the edit-tool route in the working tree"),
        "Commit the updated probe before you make a copy, because `git worktree add` and "
        "`git archive` hold only committed content, and an uncommitted update takes the "
        "edit-tool route in the working tree.",
        ("Commit the updated probe not before you make a copy, because `git worktree add` and "
         "`git archive` hold only committed content, and an uncommitted update takes the "
         "edit-tool route in the working tree.",
         "Commit the updated probe before you make a copy."),
    ),
    "undo-before-worktree-remove": (
        "adversary", "Undo each mutation in a worktree copy with the host's edit tool",
        "before `git worktree remove` removes that copy",
        ("prefer a `git archive` extract when the copy will be left behind",),
        "Undo each mutation in a worktree copy with the host's edit tool before `git worktree "
        "remove` removes that copy, and prefer a `git archive` extract when the copy will be left "
        "behind in a temp directory.",
        ("Undo each mutation in a worktree copy with the host's edit tool before `git worktree "
         "remove` removes that copy, and never prefer a `git archive` extract when the copy will "
         "be left behind in a temp directory.",
         "Undo each mutation in a worktree copy with the host's edit tool before `git worktree "
         "remove` removes that copy."),
    ),
    "redispatch-inputs": (
        "adversary", "On a re-dispatch, you also receive", "the widened changed paths",
        ("or the trunk paths a sync brought in", "and the failing program's output"),
        "On a re-dispatch, you also receive the widened changed paths, or the trunk paths a sync "
        "brought in, and the failing program's output.",
        ("On a re-dispatch, you also receive no widened changed paths, or the trunk paths a sync "
         "brought in, and the failing program's output.",
         "On a re-dispatch, you also receive the widened changed paths."),
    ),
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
    "mutation-on-committed-probe": (
        "adversary", "Back every update with mutation evidence",
        "against the committed probe program itself", (),
        "Back every update with mutation evidence run against the committed probe program itself;",
        ("Back every update with mutation evidence run against a copy of its logic, not against "
         "the committed probe program itself;",
         "Back every update with mutation evidence run against a copy of its logic;"),
    ),
    "mutation-per-kind-and-over-broad": (
        "adversary", "Use", "at least one mutation per kind of change the update touches",
        ("an over-broad update would wrongly accept",),
        "Use at least one mutation per kind of change the update touches, and include one that "
        "an over-broad update would wrongly accept.",
        ("Use at least one mutation per kind of change the update touches, and never include one "
         "that an over-broad update would wrongly accept.",
         "Use one mutation for the update, and include one that an over-broad update would wrongly accept."),
    ),
    "mutation-red-then-reverted": (
        "adversary", "Each mutation must", "turn the probe RED and is then reverted", (),
        "Each mutation must turn the probe RED and is then reverted;",
        ("Each mutation must not turn the probe RED and is then reverted;",),
    ),
    "mutation-reported": (
        "adversary", "report each one with", "its command and observed result", (),
        "report each one with its command and observed result.",
        ("never report each one with its command and observed result.",),
    ),
    "reuse-checks-existing-first": (
        "adversary", "check what already covers the target",
        "this change's programs under `docs/loom/<change-id>/evidence/probes/`",
        ("the repository's related tests",),
        "Before you write any probe, check what already covers the target: this change's programs "
        "under `docs/loom/<change-id>/evidence/probes/` and the repository's related tests.",
        ("Before you write any probe, you need not check what already covers the target: this "
         "change's programs under `docs/loom/<change-id>/evidence/probes/` and the repository's related tests.",),
    ),
    "reuse-modify-then-new": (
        "adversary", "Reuse a program that already covers a case",
        "write a new probe only when nothing covers the case",
        ("modify a program when a small change makes it cover the case",),
        "Reuse a program that already covers a case and write nothing new for it, modify a program "
        "when a small change makes it cover the case, and write a new probe only when nothing covers the case.",
        ("Reuse a program that already covers a case or do not, modify a program when a small change "
         "makes it cover the case, and write a new probe only when nothing covers the case.",),
    ),
    "permanent-test-is-reuse": (
        "adversary", "counts as reuse", "name it in `reason`",
        ("A permanent repository test that already covers a case", "leave the test as it is"),
        "A permanent repository test that already covers a case counts as reuse: name it in "
        "`reason` and leave the test as it is.",
        ("A permanent repository test that already covers a case never counts as reuse: name it in "
         "`reason` and leave the test as it is.",),
    ),
    "status-with-reason-for-new": (
        "adversary", "marks each probe", "as `reused`, `modified` or `new`",
        ("every `new` one carries a one-line `reason`",),
        "`probes` marks each probe as `reused`, `modified` or `new`, and every `new` one carries a one-line `reason`.",
        ("`probes` never marks each probe as `reused`, `modified` or `new`, and every `new` one "
         "carries a one-line `reason`.",
         "`probes` marks each probe as `reused`, `modified` or `new`."),
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
    "ref-branch-tests-excluded-from-floor": (
        "ref", "Reuse toward the floor counts",
        "(a) the programs the adversary committed for this change",
        ("(b) tests that exist unchanged outside this change's branch",),
        "Reuse toward the floor counts only (a) the programs the adversary committed for this "
        "change and (b) tests that exist unchanged outside this change's branch.",
        ("Reuse toward the floor counts not only (a) the programs the adversary committed for "
         "this change and (b) tests that exist unchanged outside this change's branch.",
         "Reuse toward the floor counts (a) the programs the adversary committed for this change "
         "and (b) any test on this change's branch."),
    ),
    "ref-branch-tests-named-related-coverage": (
        "ref", "Any other test added or changed on the branch",
        "is named as related coverage only", ("such as an implementer's pin",),
        "Any other test added or changed on the branch, such as an implementer's pin, is named "
        "as related coverage only.",
        ("Any other test added or changed on the branch, such as an implementer's pin, is not "
         "named as related coverage only.",
         "Any other test added or changed on the branch, such as an implementer's pin, counts "
         "toward the floor."),
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
    "build-trigger-excludes-caught-defect": (
        "build", "Build dispatches",
        "rather than for a product defect it correctly caught",
        ("`loom-code:adversary` agent fresh-context again to update its own programs",
         "or trunk content brought in by a trunk sync changes it",
         "fails, or is unable to run, for that reason"),
        "Build dispatches the `loom-code:adversary` agent fresh-context again to update its own "
        "programs when a fix widens or changes what the change covers, or trunk content brought in "
        "by a trunk sync changes it, and a committed adversarial program fails, or is unable to "
        "run, for that reason, rather than for a product defect it correctly caught.",
        ("Build dispatches the `loom-code:adversary` agent fresh-context again to update its own "
         "programs when a fix widens or changes what the change covers, or trunk content brought "
         "in by a trunk sync changes it, and a committed adversarial program fails, or is unable "
         "to run, for that reason, not rather than for a product defect it correctly caught.",
         "Build dispatches the `loom-code:adversary` agent fresh-context again to update its own "
         "programs when a fix widens or changes what the change covers and a committed adversarial "
         "program fails for any reason."),
    ),
    "build-passing-program-keeps-content": (
        "build", "A program that still passes", "keeps its content", (),
        "A program that still passes keeps its content.",
        ("A program that still passes does not keep its content.",
         "A program that still passes is rewritten."),
    ),
    "build-decides-and-fixes-defect": (
        "build", "Build decides which case applies",
        "fixes a product defect in the product", (),
        "Build decides which case applies from the program's failure, and fixes a product defect "
        "in the product as above.",
        ("Build decides which case applies from the program's failure, and never fixes a product "
         "defect in the product as above.",
         "Give the adversary the failing program's output."),
    ),
    "build-reruns-after-update": (
        "build", "After the update, Build repeats", "these end-of-Build checks", (),
        "After the update, Build repeats these end-of-Build checks.",
        ("After the update, Build does not repeat these end-of-Build checks.",
         "After the update, Build hands off."),
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
    "ref-floor-counts-reuse": (
        "ref", "Reused and modified cases count", "toward the floor", (),
        "Reused and modified cases count toward the floor.",
        ("Reused and modified cases do not count toward the floor.",),
    ),
    "mutation-in-throwaway-copy-or-edit-tool": (
        "adversary", "Apply each mutation in", "a throwaway copy of the working tree",
        ("run the committed probe program there unchanged",
         "apply and undo the mutation with the host's edit tool"),
        "Apply each mutation in a throwaway copy of the working tree, such as a temporary `git "
        "worktree add` or a `git archive` extract, and run the committed probe program there "
        "unchanged, or apply and undo the mutation with the host's edit tool.",
        ("Apply each mutation in a throwaway copy of the working tree and run the committed probe "
         "program there unchanged, or do not apply and undo the mutation with the host's edit tool.",
         "Apply each mutation in the working tree and run the committed probe program there unchanged."),
    ),
    "copy-still-runs-own-assertion": (
        "adversary", "Running the unchanged probe inside a copy of the tree",
        "still exercises its own assertion", ("unlike a copy of its logic",),
        "Running the unchanged probe inside a copy of the tree still exercises its own assertion, "
        "unlike a copy of its logic.",
        ("Running the unchanged probe inside a copy of the tree no longer exercises its own "
         "assertion, unlike a copy of its logic.",),
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
    "rewritten-case-counts-modified": (
        "adversary", "A stale case that is rewritten or flipped to its positive form",
        "counts as `modified`", (),
        "A stale case that is rewritten or flipped to its positive form counts as `modified`.",
        ("A stale case that is rewritten or flipped to its positive form never counts as `modified`.",
         "A stale case that is rewritten or flipped to its positive form counts as `new`."),
    ),
    "ref-rewritten-case-counts-modified": (
        "ref", "A stale case that is rewritten or flipped to its positive form",
        "counts as `modified`", (),
        "A stale case that is rewritten or flipped to its positive form counts as `modified`.",
        ("A stale case that is rewritten or flipped to its positive form does not count as `modified`.",
         "A stale case that is rewritten or flipped to its positive form counts as `new`."),
    ),
}
NO_DISCARD_UNDO = (
    "Discard commands (`git checkout --`, `git restore`, `git reset --hard`, `git clean`, "
    "`git worktree remove --force`) are never used to undo a mutation, because host guards "
    "refuse them and they can destroy uncommitted work."
)
REDISPATCH_UPDATE_NEW_COMMIT = "An update made on a Build re-dispatch is a new commit, never an amend."
DISCARD_LITERALS = (
    "git checkout --", "git restore", "git reset --hard", "git clean", "git worktree remove --force",
)
_PIN_DOCS = {"adversary": ADVERSARY_PROSE, "ref": ADVERSARIAL_REF, "build": VERIFY}


@pytest.mark.parametrize("pin", sorted(PROBE_MAINTENANCE_PINS))
def test_probe_maintenance_pin_helpers_synthetic(pin: str) -> None:
    _doc, verb, literal, extras, affirmative, rejected = PROBE_MAINTENANCE_PINS[pin]
    assert _affirms(affirmative, verb, literal, *extras)
    assert any(has_negation(r) for r in rejected), pin
    for example in rejected:
        assert not _affirms(example, verb, literal, *extras), example


@pytest.mark.parametrize("pin", sorted(PROBE_MAINTENANCE_PINS))
def test_adversary_probe_maintenance_rule_stated(pin: str) -> None:
    doc, verb, literal, extras, _affirmative, _rejected = PROBE_MAINTENANCE_PINS[pin]
    assert _affirms(_PIN_DOCS[doc], verb, literal, *extras), (pin, verb, literal)


def test_update_no_weakening_helpers_synthetic() -> None:
    assert _pins_exact_sentence(f"Keep every case. {UPDATE_NO_WEAKENING}", UPDATE_NO_WEAKENING)
    assert not _pins_exact_sentence(
        "Keep every case. An update may delete, skip or xfail a case to make it pass.",
        UPDATE_NO_WEAKENING,
    )


def test_adversary_update_never_weakens_a_case() -> None:
    assert _pins_exact_sentence(ADVERSARY_PROSE, UPDATE_NO_WEAKENING), ADVERSARY_PROSE
    assert _pins_exact_sentence(ADVERSARIAL_REF, UPDATE_NO_WEAKENING), ADVERSARIAL_REF
    assert "**at least three**" in ADVERSARIAL_REF
    assert "**at least three**" in ADVERSARY_PROSE


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
    assert _pins_exact_sentence(ADVERSARY_PROSE, NO_DISCARD_UNDO), ADVERSARY_PROSE
    assert _pins_exact_sentence(ADVERSARIAL_REF, NO_DISCARD_UNDO), ADVERSARIAL_REF


def test_redispatch_update_new_commit_helpers_synthetic() -> None:
    assert _pins_exact_sentence(f"Commit it. {REDISPATCH_UPDATE_NEW_COMMIT}", REDISPATCH_UPDATE_NEW_COMMIT)
    assert not _pins_exact_sentence(
        "Commit it. An update made on a Build re-dispatch may be amended into the original commit.",
        REDISPATCH_UPDATE_NEW_COMMIT,
    )


def test_adversary_redispatch_update_is_new_commit() -> None:
    assert _pins_exact_sentence(ADVERSARY_PROSE, REDISPATCH_UPDATE_NEW_COMMIT), ADVERSARY_PROSE


# --- Added-sentence scans: an extra sentence cannot override a pinned rule ---

def _discard_literals_outside_rule(text: str) -> list[str]:
    return [
        s for s in _sentences(text)
        if s != NO_DISCARD_UNDO and any(lit in s for lit in DISCARD_LITERALS)
    ]


_FLOOR_PINS = ("branch-tests-excluded-from-floor", "ref-branch-tests-excluded-from-floor")


def _is_pinned_floor_sentence(sentence: str) -> bool:
    return any(_affirms(sentence, *PROBE_MAINTENANCE_PINS[p][1:3], *PROBE_MAINTENANCE_PINS[p][3])
               for p in _FLOOR_PINS)


def _implementer_floor_sentences(text: str) -> list[str]:
    return [
        s for s in _sentences(text)
        if re.search(r"\bimplementer", s, re.IGNORECASE) and "floor" in s
        and not has_negation(s) and not _is_pinned_floor_sentence(s)
    ]


_DISPATCH = re.compile(r"\b(?:re-)?dispatch", re.IGNORECASE)


def _redispatch_for_caught_defect_sentences(text: str) -> list[str]:
    return [
        s for s in _sentences(text)
        if _DISPATCH.search(s) and "product defect" in s
        and "rather than for a product defect" not in s and not has_negation(s)
    ]


_EVERY_FAILURE_STALE = re.compile(
    r"\b(?:every|any|all)\b[^.;]*\bfail(?:ure|ures|ing)?\b[^.;]*\bstale\b", re.IGNORECASE
)


def _every_failure_stale_sentences(text: str) -> list[str]:
    return [s for s in _sentences(text) if _EVERY_FAILURE_STALE.search(s) and not has_negation(s)]


def test_added_sentence_scans_synthetic() -> None:
    added = "Clean up with `git reset --hard` when the copy is dirty."
    assert _discard_literals_outside_rule(f"Undo it. {NO_DISCARD_UNDO}") == []
    assert _discard_literals_outside_rule(f"{NO_DISCARD_UNDO} {added}") == [added]
    pin = PROBE_MAINTENANCE_PINS["branch-tests-excluded-from-floor"][4]
    floor_claim = "An implementer's pin counts toward the floor."
    assert _implementer_floor_sentences(pin) == []
    assert _implementer_floor_sentences(f"{pin} {floor_claim}") == [floor_claim]
    assert _implementer_floor_sentences("An implementer's pin never counts toward the floor.") == []
    trigger = PROBE_MAINTENANCE_PINS["build-trigger-excludes-caught-defect"][4]
    defect = "Build re-dispatches the adversary for a program that caught a product defect."
    assert _redispatch_for_caught_defect_sentences(f"{trigger} {ORDINARY_FIX_NO_REDISPATCH}") == []
    assert _redispatch_for_caught_defect_sentences(f"{trigger} {defect}") == [defect]
    stale = "Build treats every failure as stale and re-dispatches the adversary."
    assert _every_failure_stale_sentences("A stale case that is rewritten counts as `modified`.") == []
    assert _every_failure_stale_sentences(stale) == [stale]


@pytest.mark.parametrize("doc", sorted(_PIN_DOCS))
def test_no_added_sentence_overrides_pinned_rules(doc: str) -> None:
    text = _PIN_DOCS[doc]
    assert _discard_literals_outside_rule(text) == []
    assert _implementer_floor_sentences(text) == []
    assert _redispatch_for_caught_defect_sentences(text) == []
    assert _every_failure_stale_sentences(text) == []


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
