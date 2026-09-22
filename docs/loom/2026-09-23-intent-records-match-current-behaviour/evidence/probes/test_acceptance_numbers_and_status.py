"""Adversarial probe: the Acceptance numbers the notes name exist, and no intent is open.

Attacks Acceptance 1, 2 and 4 of the change intent: every "Acceptance N" a
"## Later changes" note names must be a numbered line of that intent's own
Acceptance list; each of the five intents names PR #43 in a sentence that
affirms it replaced lines; no intent in the store reads `status: open`, in
any spelling; and the closed intent is reported closed by the checker.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-23-intent-records-match-current-behaviour/evidence/probes/test_acceptance_numbers_and_status.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[5]
INTENT_DIR = REPO / "docs" / "loom" / "intent"
EDITED = [
    "2026-09-14-antigravity-cli-compatibility",
    "2026-09-14-expert-mode-step-selection",
    "2026-09-14-land-merged-changes",
    "2026-09-18-blocked-publish-names-the-legal-routes",
    "2026-09-19-expert-mode-skip-friction",
    "2026-09-19-publication-hook-false-positives",
    "2026-09-20-mechanical-calculations",
]
FIVE = [
    "2026-09-14-expert-mode-step-selection",
    "2026-09-14-land-merged-changes",
    "2026-09-14-antigravity-cli-compatibility",
    "2026-09-18-blocked-publish-names-the-legal-routes",
    "2026-09-19-publication-hook-false-positives",
]
AFFIRMATIVE_VERBS = ("replaced", "replaces", "shipped", "carries", "holds", "rest")
NEGATIONS = re.compile(r"\b(?:no|not|never|nor|without|none)\b|n't", re.I)
NUMBER_LIST = re.compile(r"Acceptance ((?:\d+)(?:(?:, | and )\d+)*)")


def sentences(text: str) -> list[str]:
    """Split on a full stop, colon or semicolon followed by whitespace."""
    return [s.strip() for s in re.split(r"(?<=[.:;])\s+", " ".join(text.split())) if s.strip()]


def affirms(text: str, literal: str) -> bool:
    """True when a sentence carries an affirmative verb before `literal` and no negation."""
    for sentence in sentences(text):
        index = sentence.find(literal)
        if index < 0:
            continue
        head = sentence[:index].lower()
        if any(re.search(rf"\b{verb}\b", head) for verb in AFFIRMATIVE_VERBS) \
                and not NEGATIONS.search(sentence):
            return True
    return False


def later_changes(change_id: str) -> str:
    text = (INTENT_DIR / f"{change_id}.md").read_text(encoding="utf-8")
    match = re.search(r"^## Later changes\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    assert match, f"{change_id} has no Later changes section"
    return match.group(1)


def acceptance_numbers(change_id: str) -> set[int]:
    text = (INTENT_DIR / f"{change_id}.md").read_text(encoding="utf-8")
    section = re.search(r"^## Acceptance\n(.*?)(?=^## )", text, re.S | re.M).group(1)
    return {int(n) for n in re.findall(r"^(\d+)\. ", section, re.M)}


def test_affirms_affirmativesentence_accepted() -> None:
    """Synthetic: an affirmative sentence naming the literal is accepted."""
    assert affirms("- PR #43 replaced Acceptance 11: a merge is allowed.", "Acceptance 11")


def test_affirms_negatedsentence_rejected() -> None:
    """Synthetic: the same literal inside a negated sentence is rejected."""
    assert not affirms("- PR #43 never replaced Acceptance 11.", "Acceptance 11")
    assert not affirms("- It replaced nothing, not Acceptance 11.", "Acceptance 11")


@pytest.mark.parametrize("change_id", EDITED)
def test_laterchanges_acceptancenumbers_exist(change_id: str) -> None:
    """Every Acceptance number a note names is a line of that intent's Acceptance list."""
    known = acceptance_numbers(change_id)
    for group in NUMBER_LIST.findall(later_changes(change_id)):
        for number in re.findall(r"\d+", group):
            assert int(number) in known, f"{change_id}: Acceptance {number} not in {sorted(known)}"


@pytest.mark.parametrize("change_id", FIVE)
def test_fiveintents_pr43replacement_affirmed(change_id: str) -> None:
    """Each of the five intents affirms PR #43 replaced named Acceptance lines."""
    note = later_changes(change_id)
    assert affirms(note, "Acceptance"), f"{change_id} does not affirm a replaced Acceptance line"
    assert "PR #43" in note


def test_intentstore_statusopen_absent() -> None:
    """No intent reads `status: open`, whatever its case, spacing or frontmatter form."""
    pattern = re.compile(r"^\W*status\W*:\s*open\b", re.I | re.M)
    offenders = [p.name for p in INTENT_DIR.glob("*.md") if pattern.search(p.read_text(encoding="utf-8"))]
    assert offenders == []


def test_skipfriction_status_closedpr43() -> None:
    """The shipped intent reads closed with PR #43, and the checker reports it closed."""
    text = (INTENT_DIR / "2026-09-19-expert-mode-skip-friction.md").read_text(encoding="utf-8")
    status = re.search(r"^status:\s*(.+)$", text, re.M).group(1)
    assert status.startswith("closed") and "PR #43" in status
    result = subprocess.run(
        [sys.executable, str(REPO / "loom-code/scripts/loom_checker.py"), "intents",
         "2026-09-19-expert-mode-skip-friction"],
        capture_output=True, text=True, cwd=str(REPO), timeout=60,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == ["2026-09-19-expert-mode-skip-friction", "closed"]
