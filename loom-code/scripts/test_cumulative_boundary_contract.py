"""Contract checks for Write Plan's cumulative-boundary reassessment."""

from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
WRITE_PLAN = ROOT / "loom-code/skills/write-plan/SKILL.md"
REFERENCE = (
    ROOT
    / "loom-code/skills/write-plan/references/cumulative-boundary-reassessment.md"
)
SCREEN_START = "<!-- BEGIN cumulative-boundary-screen -->"
SCREEN_END = "<!-- END cumulative-boundary-screen -->"
NEGATION = re.compile(r"\b(?:not|never|no|without|skip|omit)\b", re.I)


def _words(text: str) -> list[str]:
    return re.findall(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)*", text)


def _marked_screen(text: str) -> str:
    assert text.count(SCREEN_START) == 1
    assert text.count(SCREEN_END) == 1
    return text.split(SCREEN_START, 1)[1].split(SCREEN_END, 1)[0].strip()


def _affirmative_sentence(text: str, literal: str) -> str:
    sentence = next(
        (part.strip() for part in re.split(r"(?<=[.!?])\s+", text) if literal in part),
        "",
    )
    assert sentence, f"missing affirmative contract for {literal!r}"
    assert not NEGATION.search(sentence), f"negated contract for {literal!r}: {sentence}"
    return sentence


def test_affirmative_sentence_guard_rejects_negated_contract() -> None:
    assert "Run the screen" in _affirmative_sentence(
        "Run the screen for every code change.", "Run the screen"
    )
    try:
        _affirmative_sentence(
            "Do not run the screen for every code change.", "run the screen"
        )
    except AssertionError as error:
        assert "negated contract" in str(error)
    else:
        raise AssertionError("negated prose unexpectedly passed")


def test_entrypoint_has_bounded_always_run_screen_and_conditional_load() -> None:
    screen = _marked_screen(WRITE_PLAN.read_text())
    collapsed = " ".join(screen.split())
    assert 60 <= len(_words(screen)) <= 90
    _affirmative_sentence(screen, "Run this screen for every code change")
    for evidence in (
        "current boundary",
        "direct callers",
        "state owner",
        "focused tests",
    ):
        assert evidence in collapsed
    assert "at most 20 unique commits across the target set" in collapsed
    assert "metadata only" in collapsed
    assert "Do not read raw diffs" in collapsed
    assert "concrete dependency, state, test, or relevant-context warning" in collapsed
    assert "references/cumulative-boundary-reassessment.md" in collapsed
    assert "only then" in collapsed


def test_detailed_reference_filters_noise_and_requires_both_causes() -> None:
    text = REFERENCE.read_text()
    assert 250 <= len(_words(text)) <= 400
    for noise in (
        "renames",
        "formatting",
        "generated updates",
        "dependency bumps",
        "mass updates",
    ):
        assert noise in text
    assert "at most three target-only diffs" in text
    assert "distinct responsibility" in text
    assert "observable locality failure" in text
    _affirmative_sentence(text, "Extract only when both")
    _affirmative_sentence(text, "Preserve the current boundary")


def test_decision_uses_existing_plan_carriers_and_rejects_proxy_splits() -> None:
    text = REFERENCE.read_text()
    for carrier in ("Current State Evidence", "task", "Risk"):
        assert carrier in text
    assert "characterization" in text
    assert "behavior-preserving extraction" in text
    assert "before the feature" in text
    for proxy in (
        "file length",
        "token count",
        "commit count",
        "churn",
        "physical file split",
    ):
        assert proxy in text
    assert "warnings, never extraction verdicts" in text
