"""Build ends with a fresh adversary, the package suite and adversarial programs."""

import re
from pathlib import Path

import pytest

from prose_pin import has_negation, split_sentences as _sentences
# Sentences owned by the protocol file and by the recipes are pinned in those
# files' own test modules; the cross-document scans below read them from there
# rather than keeping a second copy that could drift. The protocol is named,
# because it is the one file of the set that every kind shares; the recipes
# are reached through `recipe_pins()`, which the routing table drives, so no
# one kind's test module is named here and retiring a kind takes its pins out
# of the scans instead of breaking this import.
from test_adversary_protocol import NO_DISCARD_UNDO
from test_adversary_routing import recipe_kind, recipe_pins, routed_recipe_files


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
# The attack procedure is one shared protocol file plus one recipe file per
# kind of artifact, all in the same skill reference folder. Each of those
# files has its own test module, which is where its rules are pinned:
# `test_adversary_protocol.py` for the protocol, and for each recipe a
# `test_adversary_recipe_<kind>.py` named after the kind it attacks, which
# the routing table lists. What stays here is the build station's own text,
# the adversary contract, and the scans that run across every one of those
# documents at once; a pin or scan below names the document it reads as `ref`
# the protocol and `ref-<kind>` that kind's recipe.
REFERENCES = ROOT / "loom-code/skills/closing-review/references"
ADVERSARIAL_REF = _flat(REFERENCES / "adversarial.md")
# Which recipe files there are is read from the routing table, not listed
# here: a kind given a recipe is scanned without an edit to this file, and a
# kind whose recipe is taken away leaves no path behind for the scans to open.
ADVERSARIAL_RECIPE_PATHS = routed_recipe_files()
# The rules those recipes pin in their own test modules, merged and looked up
# by pin name. A scan below exempts a recipe's own pinned sentence from what
# it flags; the exemption lives exactly as long as the recipe does.
RECIPE_PINS = recipe_pins()
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
    "adversary-reads-procedure-first": (
        "adversary", "read it first", "because it holds the whole attack procedure",
        ("`loom-code/skills/closing-review/references/adversarial.md`",),
        "Read `loom-code/skills/closing-review/references/adversarial.md` — read it first, because "
        "it holds the whole attack procedure.",
        ("Read `loom-code/skills/closing-review/references/adversarial.md` — never read it first, "
         "because it holds the whole attack procedure.",
         "Read `loom-code/skills/closing-review/references/adversarial.md` when convenient."),
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
}
REDISPATCH_UPDATE_NEW_COMMIT = "An update made on a Build re-dispatch is a new commit, never an amend."
DISCARD_LITERALS = (
    "git checkout --", "git restore", "git reset --hard", "git clean", "git worktree remove --force",
)
_PIN_DOCS = {
    "adversary": ADVERSARY_PROSE,
    "ref": ADVERSARIAL_REF,
    **{f"ref-{recipe_kind(p.name)}": _flat(p) for p in ADVERSARIAL_RECIPE_PATHS},
    "build": VERIFY,
}


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


# The pinned rules a sentence about an implementer and the floor is allowed
# to be. A name no routed recipe pins is simply not exempt, which makes the
# scan stricter rather than blinder, so a kind's retirement cannot let an
# added claim through.
_FLOOR_PINS = ("ref-branch-tests-excluded-from-floor",)


def _is_pinned_floor_sentence(sentence: str) -> bool:
    return any(_affirms(sentence, *RECIPE_PINS[p][1:3], *RECIPE_PINS[p][3])
               for p in _FLOOR_PINS if p in RECIPE_PINS)


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
    floor_claim = "An implementer's pin counts toward the floor."
    assert _implementer_floor_sentences(floor_claim) == [floor_claim]
    assert _implementer_floor_sentences("An implementer's pin never counts toward the floor.") == []
    for name in _FLOOR_PINS:
        if name not in RECIPE_PINS:  # its recipe is retired; nothing to exempt
            continue
        pin = RECIPE_PINS[name][4]
        assert _implementer_floor_sentences(pin) == []
        assert _implementer_floor_sentences(f"{pin} {floor_claim}") == [floor_claim]
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


# --- Dead pointers: the attack catalogue and the task trailer are retired ---

IMPLEMENTER = ROOT / "loom-code/agents/implementer.md"
ADVERSARIAL_REF_PATH = REFERENCES / "adversarial.md"
_DEAD_POINTER = re.compile(r"attack[- ]catalogue|\bcatalogue\b|\btrailer\b", re.IGNORECASE)
BUILD_ADVERSARIAL_LINK = "[`adversarial.md`](../closing-review/references/adversarial.md)"
BUILD_LINK_VERB = "works from the recipes in"


def _dead_pointer_hits(text: str) -> list[str]:
    return _DEAD_POINTER.findall(text)


def test_dead_pointer_helpers_catalogue_link_reintroduced_fails() -> None:
    assert _dead_pointer_hits("Work the classes against the file, one attempt per class.") == []
    assert _dead_pointer_hits("Work the six classes in [`attack-catalogue.md`](attack-catalogue.md).")
    assert _dead_pointer_hits("they turn the catalogue into an eval")
    assert _dead_pointer_hits("failing test first, one commit carrying the task trailer.")
    assert _dead_pointer_hits("needs no separate task-accounting trailer.")
    affirmative = f"It {BUILD_LINK_VERB} {BUILD_ADVERSARIAL_LINK}."
    negated = f"It never {BUILD_LINK_VERB} {BUILD_ADVERSARIAL_LINK}."
    assert _affirms(affirmative, BUILD_LINK_VERB, BUILD_ADVERSARIAL_LINK)
    assert has_negation(negated)
    assert not _affirms(negated, BUILD_LINK_VERB, BUILD_ADVERSARIAL_LINK)


@pytest.mark.parametrize(
    "path",
    [ADVERSARY, ADVERSARIAL_REF_PATH, *ADVERSARIAL_RECIPE_PATHS, IMPLEMENTER],
    ids=lambda p: p.name,
)
def test_contract_no_attack_catalogue_or_task_trailer_reference(path: Path) -> None:
    assert _dead_pointer_hits(path.read_text(encoding="utf-8")) == [], path


def test_build_verify_step_links_adversarial_recipes_in_place() -> None:
    step = VERIFY.split("2. Dispatch the `loom-code:adversary` agent", 1)[1].split("3. Run the", 1)[0]
    assert _affirms(step, BUILD_LINK_VERB, BUILD_ADVERSARIAL_LINK), step
    target = (ROOT / "loom-code/skills/build" / "../closing-review/references/adversarial.md").resolve()
    assert target == ADVERSARIAL_REF_PATH and target.is_file()


def test_probes_field_helper_synthetic() -> None:
    good = 'probes: [{artifact: "<path>", status: reused | modified | new, reason: "<one line>"}]'
    assert PROBES_FIELD.search(good)
    assert not PROBES_FIELD.search('probes: [{artifact: "<path>", status: reused | modified | new}]')


# --- One home for the procedure: the adversarial reference files; adversary.md
# --- keeps role, inputs, return ---
#
# Each procedure rule is pinned in the test module of the file that owns it,
# where it is also checked against adversary.md: test_adversary_protocol.py for
# the protocol, and test_adversary_recipe_<kind>.py for each recipe the routing
# table lists. What adversary.md must keep is here.

def test_adversary_md_keeps_role_inputs_return_format() -> None:
    for pin in ("role-updates-own-programs", "redispatch-inputs", "adversary-reads-procedure-first"):
        _doc, verb, literal, extras, _a, _r = PROBE_MAINTENANCE_PINS[pin]
        assert _affirms(ADVERSARY_PROSE, verb, literal, *extras), pin
    assert "You own the negative in this flow" in ADVERSARY_PROSE
    assert _pins_exact_sentence(ADVERSARY_PROSE, REDISPATCH_UPDATE_NEW_COMMIT), ADVERSARY_PROSE
    assert "Use the host's edit tool (Edit/Write, `apply_patch` on Codex) -- never `sed -i`" in ADVERSARY_PROSE
    assert "## What you return" in ADVERSARY.read_text(encoding="utf-8")


def test_adversary_return_format_marks_probe_status() -> None:
    text = ADVERSARY.read_text(encoding="utf-8")
    block = text.split("## What you return", 1)[1].split("```", 2)[1]
    assert PROBES_FIELD.search(block), block
    assert re.search(r"^adversarial: \[\{command: ", block, re.M), block
    assert re.search(r"^findings: \[\{severity: ", block, re.M), block
