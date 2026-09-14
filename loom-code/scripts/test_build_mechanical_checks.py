"""Build ends with a fresh adversary, the package suite and adversarial programs."""

from pathlib import Path

from prose_pin import has_negation


ROOT = Path(__file__).resolve().parents[2]
BUILD = (ROOT / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
PROSE = " ".join(BUILD.split())
VERIFY = " ".join(BUILD.split("## 3. Verify integration", 1)[1].split("## 4.", 1)[0].split())
HANDOFF = " ".join(BUILD.split("## 4. Hand off to Review", 1)[1].split())
ADVERSARY = ROOT / "loom-code/agents/adversary.md"


def _sentence(text: str, fragment: str) -> str:
    return next(s for s in text.split(". ") if fragment in s)


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
    assert "Give it only paths: the intent, the plan, and the changed paths" in VERIFY
    assert "never pass an implementer's explanation of its own code" in VERIFY
    for leak in ("implementer's report", "implementer's summary", "self_review"):
        assert leak not in VERIFY


def test_build_allows_complete_suite_at_end() -> None:
    assert (
        "Build does not hand off to Review until the complete package suite and every "
        "adversarial program pass."
    ) in VERIFY
    assert "`finalize-review` still executes both once more on committed content." in VERIFY
    assert "complete package suite command and its result" in HANDOFF
    assert "each adversarial program's path and command" in HANDOFF


def test_no_speculative_preflight_ban_remains() -> None:
    assert "speculative push preflight" not in PROSE
    assert "owns its one content-bound execution" not in PROSE
    for sentence in PROSE.split(". "):
        if "complete package suite" in sentence and has_negation(sentence):
            assert "does not hand off" in sentence or "skipped" in sentence, sentence


def test_fix_return_reruns_existing_programs() -> None:
    sentence = _sentence(
        VERIFY, "When closing review or a failed `finalize-review` returns the change to Build"
    )
    assert "repeat these end-of-Build checks" in sentence
    assert "re-run the existing adversarial programs" in sentence
    assert "Do not dispatch the adversary again." in VERIFY


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
