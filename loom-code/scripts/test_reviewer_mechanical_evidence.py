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
    # lenses.md is the single source of these rules; reviewer.md points to it.
    text = _flat(LENSES_PATH)
    assert "the test files the change added or changed" in text
    flag = [
        s for s in _sentences(text)
        if "test files the change added or changed" in s
        and "skipped" in s
        and "never actually executes" in s
    ]
    assert flag, "lenses.md does not flag a skipped or non-executing changed test"
    assert "never run the complete package suite or the adversarial programs" in text
    assert "not grounds for `PASS_WITH_NOTES`" in text

    reviewer = _flat(REVIEWER_PATH)
    assert "`loom-code/skills/closing-review/references/lenses.md`" in reviewer
    # What still holds: citation reading, no probes, no edits.
    assert "Open every source you cite." in reviewer
    assert "you write no probes" in reviewer
    assert "**Do not modify**" in reviewer


LENSES_REF = "`loom-code/skills/closing-review/references/lenses.md`"


def test_reviewer_spells_the_lenses_path_one_way() -> None:
    """A4 negative (lenses-path-spelled-two-ways): reviewer.md sits at plugin
    level, so every citation resolves from the repository root."""
    reviewer = _flat(REVIEWER_PATH)
    assert "`skills/closing-review/references/lenses.md`" not in reviewer
    assert reviewer.count(LENSES_REF) == 4, reviewer.count(LENSES_REF)
    assert LENSES_PATH.is_file()


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
    rules = _run_rule_sentences(_flat(LENSES_PATH))
    assert len(rules) == 1, rules
    assert f"{RUN_RULE}, {PROBE_CARVE_OUT}" in rules[0], rules[0]
    assert _run_rule_sentences(_flat(REVIEWER_PATH)) == []
    assert not [s for s in _sentences("You run the test files the change added or changed.")
                if PROBE_CARVE_OUT in s]


def test_skipped_changed_test_stays_a_finding() -> None:
    (rule,) = _run_rule_sentences(_flat(LENSES_PATH))
    assert _skipped_test_is_finding(rule), rule
    assert "a green exit code does not show that it ran" in rule, rule


def test_skipped_test_names_the_file_the_reviewer_ran() -> None:
    (rule,) = _run_rule_sentences(_flat(LENSES_PATH))
    assert "a test in a changed test file the reviewer ran" in rule, rule
    assert not has_negation("a test in a changed test file the reviewer ran")


def test_shell_builtin_adversarial_artifact_scores_tests_needs_revision() -> None:
    lenses = _flat(LENSES_PATH)
    rule = [s for s in _sentences(lenses) if "shell builtin" in s]
    assert len(rule) == 1, rule
    assert (
        "exits 0 for unrelated reasons — score `tests` `NEEDS_REVISION` and raise "
        "a finding naming that artifact"
    ) in rule[0], rule[0]
    assert "shell builtin" not in _flat(REVIEWER_PATH)


def test_suite_ban_holds_in_every_round() -> None:
    lenses = _flat(LENSES_PATH)
    assert (
        "In every round, reviewers never run the complete package suite or the adversarial programs"
    ) in lenses
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
    lenses_nits = " ".join(_nit_sentences(_flat(LENSES_PATH)))
    assert "Ship may batch safe publication-only wording fixes" in lenses_nits
    assert "Ship may batch" not in _flat(REVIEWER_PATH)


# Severity and verdict rules: lenses.md states each exactly once, reviewer.md none.
_SEVERITY_RULES = {
    "consequence": r"Severity is decided by consequence",
    "fatal-level": r"\*\*fatal\*\* — ships a defect",
    "fatal-executor": r"an instruction that makes an executor do the wrong thing",
    "important-level": r"\*\*important\*\* — a reader following the text would act wrongly",
    "nit-level": r"\*\*nit\*\* — everything else",
    "any-fatal": r"Any fatal → `NEEDS_REVISION`",
    "two-important": r"Two or more important → `NEEDS_REVISION`",
    "one-important": r"One important → `PASS_WITH_NOTES`",
    "only-nits": r"Only nits, or nothing → ?`PASS`",
    "nits-no-round": r"Nits do not trigger another formal review",
    "opaque": r"is opaque and flips the whole verdict to `NEEDS_REVISION`",
    "suite-ban": r"never run the complete package suite or the adversarial programs",
    "not-grounds": r"not grounds for `PASS_WITH_NOTES`",
    "unchecked-claim": r"and did not, scores `PASS_WITH_NOTES`",
    "n-a": r"scores `N/A` with the reason",
    "leak-reverse": r"fires the other way",
    "whole-artifact": r"(?i:read the whole artifact), not only the delta",
}
# The reviewer.md wording these rules had before lenses.md became their only home.
_OLD_REVIEWER_FINGERPRINTS = (
    r"Severity is decided by consequence",
    r"Any `fatal` → `NEEDS_REVISION`",
    r"Two or more `important` → `NEEDS_REVISION`",
    r"One `important` → `PASS_WITH_NOTES`",
    r"`fatal` — a defect that ships",
    r"`nit`s never open a round",
    r"flips your whole verdict to `NEEDS_REVISION`",
    r"which is not a pass",
    r"also fires the other way",
    r"Read the artifact whole",
)


def _restated_severity_rules(text: str) -> list[str]:
    patterns = list(_SEVERITY_RULES.values()) + list(_OLD_REVIEWER_FINGERPRINTS)
    return [p for p in patterns if re.search(p, text)]


def test_severity_verdict_rules_once_in_lenses() -> None:
    lenses = _flat(LENSES_PATH)
    for name, pattern in _SEVERITY_RULES.items():
        hits = re.findall(pattern, lenses)
        assert len(hits) == 1, f"lenses.md states {name!r} {len(hits)} times"
    section = lenses.split("## Severity and verdict", 1)[1].split("## ", 1)[0]
    for sentence in _sentences(section):
        if re.search(r"→ `PASS", sentence):
            assert not has_negation(sentence), sentence
    reviewer = _flat(REVIEWER_PATH)
    assert "`loom-code/skills/closing-review/references/lenses.md`" in reviewer
    assert "<!-- gate: charter.plan-omission-narrow -->" in LENSES_PATH.read_text(encoding="utf-8")


def test_reviewer_md_restates_severity_table() -> None:
    old = (
        "Severity is decided by consequence, not by where the finding lands. "
        "Any `fatal` → `NEEDS_REVISION`. Two or more `important` → `NEEDS_REVISION`."
    )
    assert _restated_severity_rules(old)
    restated = _restated_severity_rules(_flat(REVIEWER_PATH))
    assert restated == [], f"reviewer.md restates lenses.md rules: {restated}"


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
