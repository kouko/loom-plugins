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

from prose_pin import split_sentences as _sentences


ROOT = Path(__file__).resolve().parents[2]
REVIEWER_PATH = ROOT / "loom-code/agents/reviewer.md"
LENSES_PATH = ROOT / "loom-code/skills/closing-review/references/lenses.md"


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


LENSES_REF = "`loom-code/skills/closing-review/references/lenses.md`"


def test_reviewer_spells_the_lenses_path_one_way() -> None:
    """A4 negative (lenses-path-spelled-two-ways): reviewer.md sits at plugin
    level, so every citation resolves from the repository root."""
    reviewer = _flat(REVIEWER_PATH)
    assert "`skills/closing-review/references/lenses.md`" not in reviewer
    assert reviewer.count(LENSES_REF) == 4, reviewer.count(LENSES_REF)
    assert LENSES_PATH.is_file()


_ROUND_SCOPED = re.compile(
    r"\bRound \d\b|\b(?:first|final|last|later|early|some) rounds?\b", re.IGNORECASE
)


def test_prose_pin_helpers_synthetic() -> None:
    assert not _ROUND_SCOPED.search("In every round, you never run the complete package suite.")
    assert _ROUND_SCOPED.search("In Round 1, you never run the complete package suite.")


def test_suite_ban_holds_in_every_round() -> None:
    for path in (REVIEWER_PATH, LENSES_PATH):
        for sentence in _sentences(_flat(path)):
            if _SUITE.search(sentence):
                assert not _ROUND_SCOPED.search(sentence), f"{path.name}: {sentence!r}"


def test_prose_does_not_eliminate_behavior_evidence() -> None:
    """A3 negative: behaviour-changes-still-require-executable-evidence"""
    lenses_text = _flat(LENSES_PATH)
    # The lens must not say prose needs no behavior evidence at all
    assert "prose needs no behavior evidence" not in lenses_text
    assert "prose-only change needs no behavior evidence" not in lenses_text


_SUITE = re.compile(r"package suite|adversarial programs?\b", re.IGNORECASE)
_NEGATION = re.compile(r"\b(never|not|no)\b", re.IGNORECASE)


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
