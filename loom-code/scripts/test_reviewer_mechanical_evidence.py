"""Acceptance 4 — reviewers leave the package suite and adversarial programs
to Build and finalization.

The complete package suite and the adversarial programs run mechanically at
the end of Build and again in `finalize-review`. The reviewer contract must
therefore not ask a reviewer to run them, and must not downgrade a dimension
to PASS_WITH_NOTES for not having run them. What a reviewer still runs is the
test files the change added or changed, and a skipped or never-executing test
in those files is a finding.
"""

import re
from pathlib import Path

from prose_pin import has_negation, split_sentences as _sentences


ROOT = Path(__file__).resolve().parents[2]
REVIEWER_PATH = ROOT / "loom-code/agents/reviewer.md"
LENSES_PATH = ROOT / "loom-code/skills/closing-review/references/lenses.md"


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def test_reviewer_text_runs_changed_test_files_and_flags_skips() -> None:
    for path in (REVIEWER_PATH, LENSES_PATH):
        text = _flat(path)
        assert "the test files the change added or changed" in text, path.name
        flag = [
            s for s in _sentences(text)
            if "test files the change added or changed" in s
            and "skipped" in s
            and "never actually executes" in s
        ]
        assert flag, f"{path.name} does not flag a skipped or non-executing changed test"
        assert "never run the complete package suite or the adversarial programs" in text, path.name
        assert "not grounds for `PASS_WITH_NOTES`" in text, path.name

    reviewer = _flat(REVIEWER_PATH)
    # What still holds: citation reading, no probes, no edits.
    assert "Open every source you cite." in reviewer
    assert "you write no probes" in reviewer
    assert "**Do not modify**" in reviewer


RUN_RULE = "test files the change added or changed"
PROBE_CARVE_OUT = (
    "except the adversarial programs under `docs/loom/<change-id>/evidence/probes/`"
)
# Negations the skipped-test sentence legitimately carries; any other negation
# inverts the finding ("is not a `tests` finding").
_ALLOWED_NEGATIONS = ("never actually executes", "does not show that it ran")
_FINDING = re.compile(r"\bis a (?:`tests` )?finding\b")
_ROUND_SCOPED = re.compile(
    r"\bRound \d\b|\b(?:first|final|last|later|early|some) rounds?\b", re.IGNORECASE
)


def _run_rule_sentences(text: str) -> list[str]:
    return [s for s in _sentences(text) if RUN_RULE in s]


def _skipped_test_is_finding(sentence: str) -> bool:
    rest = sentence
    for phrase in _ALLOWED_NEGATIONS:
        rest = rest.replace(phrase, "")
    return bool(_FINDING.search(sentence)) and not has_negation(rest)


def test_prose_pin_helpers_synthetic() -> None:
    assert _skipped_test_is_finding(
        "a test that is skipped, or that never actually executes, is a `tests` finding."
    )
    assert not _skipped_test_is_finding(
        "a test that is skipped, or that never actually executes, is not a `tests` finding."
    )
    assert not _ROUND_SCOPED.search("In every round, you never run the complete package suite.")
    assert _ROUND_SCOPED.search("In Round 1, you never run the complete package suite.")


def test_run_rule_excludes_adversarial_programs() -> None:
    for path in (REVIEWER_PATH, LENSES_PATH):
        rules = _run_rule_sentences(_flat(path))
        assert len(rules) == 1, f"{path.name}: {rules}"
        assert f"{RUN_RULE}, {PROBE_CARVE_OUT}" in rules[0], rules[0]
    assert not [s for s in _sentences("You run the test files the change added or changed.")
                if PROBE_CARVE_OUT in s]


def test_skipped_changed_test_stays_a_finding() -> None:
    for path in (REVIEWER_PATH, LENSES_PATH):
        (rule,) = _run_rule_sentences(_flat(path))
        assert _skipped_test_is_finding(rule), f"{path.name}: {rule}"


def test_skipped_test_names_the_file_the_reviewer_ran() -> None:
    for path, subject in ((REVIEWER_PATH, "you ran"), (LENSES_PATH, "the reviewer ran")):
        (rule,) = _run_rule_sentences(_flat(path))
        assert f"a test in a changed test file {subject}" in rule, f"{path.name}: {rule}"
        assert not has_negation(f"a test in a changed test file {subject}")


def test_suite_ban_holds_in_every_round() -> None:
    reviewer = _flat(REVIEWER_PATH)
    assert (
        "In every round, you never run the complete package suite or the adversarial programs"
    ) in reviewer
    for path in (REVIEWER_PATH, LENSES_PATH):
        for sentence in _sentences(_flat(path)):
            if _SUITE.search(sentence):
                assert not _ROUND_SCOPED.search(sentence), f"{path.name}: {sentence!r}"


_SUITE = re.compile(r"package suite|adversarial programs?\b", re.IGNORECASE)
_NEGATION = re.compile(r"\b(never|not|no)\b", re.IGNORECASE)
_DOWNGRADE_FOR_NOT_RUNNING = re.compile(
    r"(did not|could not|not) run\b|what was not run|evidence you did not run",
    re.IGNORECASE,
)


_SHIP_FOLDS_NITS = re.compile(
    r"\bship\b[^.]*\bfolds?\b[^.]*\bcommit\b|\bconfirm each fix\b", re.IGNORECASE
)


def _nit_sentences(text: str) -> list[str]:
    return [s for s in _sentences(text) if re.search(r"\bnits?\b", s)]


def test_ship_folds_nits_sentence_rejected() -> None:
    """Ship has no nit-folding step and publication-only edits never return to
    review, so the reviewer contract must not promise a folded nit commit that
    the reviewer confirms; it says what lenses.md says — Ship may batch."""
    old = (
        "`nit`s never open a round — `ship` folds them into one commit before "
        "push and you confirm each fix in one line, not a new round."
    )
    assert _SHIP_FOLDS_NITS.search(old)
    for path in (REVIEWER_PATH, LENSES_PATH):
        for sentence in _nit_sentences(_flat(path)):
            assert not _SHIP_FOLDS_NITS.search(sentence), f"{path.name}: {sentence!r}"
    reviewer_nits = " ".join(_nit_sentences(_flat(REVIEWER_PATH)))
    assert "Ship may batch safe publication-only wording fixes" in reviewer_nits


def test_no_reviewer_or_lens_text_requires_suite_run_or_downgrade() -> None:
    for path in (REVIEWER_PATH, LENSES_PATH):
        text = _flat(path)
        for phrase in (
            "evidence you did not run yourself",
            "an adversarial command supplied to finalization, scoring",
            "name what was not run",
            "Check anything checkable — a test result",
            "| the tests, run |",
            "Do not re-run adversarial programs",
        ):
            assert phrase not in text, f"{path.name} still says {phrase!r}"
        for sentence in _sentences(text):
            if _SUITE.search(sentence):
                assert _NEGATION.search(sentence), (
                    f"{path.name} mentions the suite or adversarial programs "
                    f"without keeping them out of the reviewer's hands: {sentence!r}"
                )
            if "PASS_WITH_NOTES" in sentence and _DOWNGRADE_FOR_NOT_RUNNING.search(sentence):
                assert "not grounds" in sentence, (
                    f"{path.name} downgrades for evidence not run: {sentence!r}"
                )
