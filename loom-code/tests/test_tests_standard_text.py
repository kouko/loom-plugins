"""The tests standard is the one text writer and judge read for test rules.

`loom-code/references/tests-standard.md` holds every test-writing rule;
engineering-baseline.md and the closing-review `tests` lens row point to it
instead of restating it. Pins follow the prose-pin rule: an affirmative verb
before the pinned literal, no negation token in that sentence, and synthetic
self-tests for one affirmative and one negated example.
"""
from __future__ import annotations

from pathlib import Path

from prose_pin import affirms, flat_prose, rule_prose

REPO = Path(__file__).resolve().parents[2]
STANDARD = REPO / "loom-code/references/tests-standard.md"
BASELINE = REPO / "loom-code/references/engineering-baseline.md"
LENSES = REPO / "loom-code/skills/closing-review/references/lenses.md"

# One literal per moved or added rule; each lives in the standard only.
MOVED_RULES = (
    "A test that cannot fail when the logic changes is not a test.",
    "one restating a constant or the implementation",
    "a mock or stub replacing the very seam it claims to cover",
    "entry is what other modules call, never whatever its tests call",
    "a new or changed test that calls an internal (non-entry) function is a finding",
    "a test through the entry is never asked to add internal tests",
    "requires an affirmative verb before the pinned literal",
    "computed the same way the code computes it",
    "verifying through a side channel instead of the public interface",
)


def _tautology_ban(text: str) -> bool:
    return affirms(text, "is a finding", "computed the same way the code computes it") and affirms(
        text, "must come from", "independent source", "known-good literal", "worked example", "spec"
    )


def _impl_coupled_ban(text: str) -> bool:
    return affirms(
        text, "is a finding", "mocking an internal collaborator", "private method", "side channel"
    ) and affirms(text, "behaviour-preserving refactor", "breaks the test")


def test_standard_exists_and_lens_row_cites_it() -> None:
    """A1: the standard exists; the lens `tests` row cites it by relative path."""
    assert STANDARD.is_file()
    tests_row = next(l for l in LENSES.read_text(encoding="utf-8").splitlines() if l.startswith("| tests |"))
    assert "`../../../references/tests-standard.md`" in tests_row


def test_moved_rules_stated_once_in_standard_only() -> None:
    """A2/A9: each rule is present once in the standard and absent from baseline and lenses."""
    standard = flat_prose(STANDARD)
    baseline, lenses = flat_prose(BASELINE), flat_prose(LENSES)
    for rule in MOVED_RULES:
        assert standard.count(rule) == 1, rule
        assert rule not in baseline, f"restated in baseline: {rule}"
        assert rule not in lenses, f"restated in lenses: {rule}"
    assert "`tests-standard.md`" in baseline or "(tests-standard.md)" in baseline


def test_tautology_and_impl_coupled_bans_affirmative() -> None:
    """A4/A6 positive: both bans are stated affirmatively in the standard."""
    text = rule_prose(STANDARD)
    assert _tautology_ban(text)
    assert _impl_coupled_ban(text)


def test_bans_matcher_rejects_negated_synthetic() -> None:
    """A4/A6 negative: the matchers accept an affirmative example and reject its negation."""
    tautology = (
        "A tautological assertion is a finding: its expected value is computed the same way "
        "the code computes it. Expected values must come from an independent source: a "
        "known-good literal, a worked example, or the spec."
    )
    assert _tautology_ban(tautology)
    assert not _tautology_ban(tautology.replace("is a finding", "is never a finding"))
    coupled = (
        "A test coupled to the implementation is a finding: one mocking an internal "
        "collaborator, one testing a private method, or one verifying through a side channel. "
        "The tell: a behaviour-preserving refactor breaks the test."
    )
    assert _impl_coupled_ban(coupled)
    assert not _impl_coupled_ban(coupled.replace("is a finding", "is not a finding"))


def test_red_green_refactor_loop_unchanged() -> None:
    """A9 boundary: the baseline keeps the red → green → refactor loop."""
    baseline = flat_prose(BASELINE)
    assert "## 2. Red → green → refactor" in BASELINE.read_text(encoding="utf-8")
    assert (
        "**REFACTOR** — with every test green, improve the internal structure without "
        "changing behaviour."
    ) in baseline
