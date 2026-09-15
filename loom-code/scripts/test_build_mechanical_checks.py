"""Build ends with a fresh adversary, the package suite and adversarial programs."""

import re
from pathlib import Path

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
    "After a fix that leaves every adversarial program fitting the change, do not "
    "dispatch the adversary again."
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
        "Run checks. After a fix that leaves every adversarial program fitting the change, "
        "dispatch the adversary again.",
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


def test_no_other_role_edits_adversarial_program() -> None:
    assert _pins_exact_sentence(VERIFY, NO_OTHER_ROLE_EDITS_PROGRAM), VERIFY
    assert PROSE.count("edit an adversarial program") == 1


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
