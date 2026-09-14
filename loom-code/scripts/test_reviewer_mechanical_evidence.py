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


ROOT = Path(__file__).resolve().parents[2]
REVIEWER_PATH = ROOT / "loom-code/agents/reviewer.md"
LENSES_PATH = ROOT / "loom-code/skills/closing-review/references/lenses.md"


def _flat(path: Path) -> str:
    return " ".join(path.read_text(encoding="utf-8").split())


def _sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;])\s+", text) if s]


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


_SUITE = re.compile(r"package suite|adversarial programs?\b", re.IGNORECASE)
_NEGATION = re.compile(r"\b(never|not|no)\b", re.IGNORECASE)
_DOWNGRADE_FOR_NOT_RUNNING = re.compile(
    r"(did not|could not|not) run\b|what was not run|evidence you did not run",
    re.IGNORECASE,
)


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
