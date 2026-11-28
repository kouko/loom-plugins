"""The tests standard is the one text writer and judge read for test rules.

`loom-code/references/tests-standard.md` holds every test-writing rule;
engineering-baseline.md and the closing-review `tests` lens row point to it
instead of restating it. Pins follow the prose-pin rule: an affirmative verb
before the pinned literal, no negation token in that sentence, and synthetic
self-tests for one affirmative and one negated example. A rule sentence or
reader pointer carrying its own negation is pinned whole instead.
"""
from __future__ import annotations

from pathlib import Path

from prose_pin import affirms, flat_prose, pins_exact_sentence, rule_prose

REPO = Path(__file__).resolve().parents[2]
STANDARD = REPO / "loom-code/references/tests-standard.md"
BASELINE = REPO / "loom-code/references/engineering-baseline.md"
LENSES = REPO / "loom-code/skills/closing-review/references/lenses.md"

# One literal per moved or added rule; each lives in the standard only.
MOVED_RULES = (
    "**Tests verify intent.** A test that cannot fail for the behaviour it names is a finding",
    "one restating a constant or the implementation",
    "a mock or stub replacing the very seam it claims to cover",
    "entry is what other modules call, never whatever its tests call",
    "a new or changed test that calls an internal (non-entry) function is a finding",
    "a test through the entry is never asked to add internal tests",
    "requires an affirmative verb before the pinned literal",
    "computed the same way the code computes it",
    "verifying through a side channel instead of the public interface",
    "what distinct defect, input, state, environment or oracle is new",
    "the retained case detects the old defect",
    "distinct boundary, integration and environment coverage",
    "harnesses and tests of tests are findings",
    "adds at most one test, extending an existing test first",
)
# Every rule sentence, pinned whole: a count-only pin lets "is a finding"
# flip to "is not a finding" unseen.
RULE_SENTENCES = (
    "**Tests verify intent.** A test that cannot fail for the behaviour it names is a finding — one restating a constant or the "
    "implementation, one reading source text to assert code structure (prose-pin tests that meet §5 of "
    "this file excepted), or a mock or stub replacing the very seam it claims to cover.",
    "A tautological assertion is a finding: its expected value is computed the same way the code "
    "computes it, so it passes by construction.",
    "Expected values must come from an independent source: a known-good literal, a worked example done "
    "by hand, or the spec.",
    "A test coupled to the implementation is a finding: one mocking an internal collaborator, one "
    "testing a private method, or one verifying through a side channel instead of the public interface.",
    "The tell: a behaviour-preserving refactor breaks the test.",
    "A module's entry is what other modules call, never whatever its tests call;",
    "a task adding or changing a function's behaviour whose plan Files line marks no entry is a finding;",
    "a new or changed test that calls an internal (non-entry) function is a finding when that behaviour "
    "is reachable from the module's entry, whether or not entry tests already cover it, and the fix "
    "moves the test to the entry, or deletes it when an entry test already covers that behaviour;",
    "a test through the entry is never asked to add internal tests, and logic the entry cannot reach "
    "that became its own module with its own entry, tested at that entry, is not a finding.",
    "A test that pins a sentence of prose requires an affirmative verb before the pinned literal, "
    "rejects any negation token in that same sentence, and carries synthetic self-tests validating one "
    "affirmative example and one rejected negated example.",
    "Compare tests for touched behaviour with existing cases: what distinct defect, input, state, "
    "environment or oracle is new? Ordinary consolidation or deletion requires evidence the retained "
    "case detects the old defect, not shared lines, text similarity or counts.",
    "Preserve distinct boundary, integration and environment coverage.",
    "Unnecessary helpers, harnesses and tests of tests are findings.",
    "The fix for any finding adds at most one test, extending an existing test first.",
)
BASELINE_POINTER = (
    "**Test rules live in [`tests-standard.md`](tests-standard.md).** Read it before writing a test: "
    "the reviewer judges every test against it."
)
LENS_POINTER = (
    "every rule in `../../../references/tests-standard.md` — tests that cannot fail for the behaviour "
    "they name, tautological assertions, tests coupled to the implementation, module entry versus "
    "internal-function tests, prose-pin tests, new tests against existing cases — is judged here, and a breach of it is a finding;"
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
    assert LENS_POINTER in tests_row


def test_moved_rules_stated_once_in_standard_only() -> None:
    """A2/A9: each rule is present once in the standard and absent from baseline and lenses."""
    standard = flat_prose(STANDARD)
    baseline, lenses = flat_prose(BASELINE), flat_prose(LENSES)
    for rule in MOVED_RULES:
        assert standard.count(rule) == 1, rule
        assert rule not in baseline, f"restated in baseline: {rule}"
        assert rule not in lenses, f"restated in lenses: {rule}"
    sentences = rule_prose(STANDARD)
    for sentence in RULE_SENTENCES:
        assert pins_exact_sentence(sentences, sentence), sentence
    assert pins_exact_sentence(rule_prose(BASELINE), BASELINE_POINTER)


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
