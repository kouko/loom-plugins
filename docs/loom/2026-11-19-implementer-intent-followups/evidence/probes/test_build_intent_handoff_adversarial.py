# concern: A weakened or skip-scoped rewrite of Build's intent-path hand-off must be rejected by its pin.
"""Adversarial probes for Build's intent-path hand-off (Acceptance 1)."""
from __future__ import annotations

import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
BUILD = ROOT / "loom-code/skills/build/SKILL.md"
PIN_TEST = "loom-code/tests/test_build_mechanical_checks.py"
NEGATION_RE = re.compile(
    r"\b(?:not|never|no|cannot|without|neither|nobody|nor)\b|n't|\boptional", re.IGNORECASE
)
PLANNED = "Hand each agent the confirmed intent path, the retained artifact paths and the omitted steps;"
MUTATIONS = {
    "optional-prefix": ("Hand each agent the\nconfirmed intent path",
                        "Optionally, when it helps: Hand each agent the\nconfirmed intent path"),
    "negate-planned": ("Hand each agent the\nconfirmed intent path",
                       "Never Hand each agent the\nconfirmed intent path"),
    "negate-skipped": ("and hand the implementer the intent\npath",
                       "and do not hand the implementer the intent\npath"),
}


def _clauses(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;])\s+", " ".join(text.split())) if s]


def _affirmed_unconditionally(paragraph: str, clause: str) -> bool:
    """The clause is stated affirmatively, and the paragraph does not open on a skip condition."""
    clauses = _clauses(paragraph)
    if clauses.count(clause) != 1 or NEGATION_RE.search(clause):
        return False
    lead = clauses[: clauses.index(clause)]
    return not any("skipped" in c for c in lead)


def _paragraph_with(text: str, needle: str) -> str:
    for para in re.split(r"\n\s*\n", text):
        if needle in " ".join(para.split()):
            return para
    return ""


def test_intent_handoff_helper_affirmative_example_accepted() -> None:
    assert _affirmed_unconditionally(f"Every dispatch carries paths. {PLANNED}", PLANNED)


def test_intent_handoff_helper_negated_example_rejected() -> None:
    negated = PLANNED.replace("Hand", "Never hand")
    assert not _affirmed_unconditionally(negated, negated)


def test_build_planned_path_handoff_not_scoped_to_skip() -> None:
    """The planned-path intent hand-off must not sit under a 'when skipped' lead sentence."""
    text = BUILD.read_text(encoding="utf-8")
    para = _paragraph_with(text, "confirmed intent path")
    assert _affirmed_unconditionally(para, PLANNED), para


@pytest.mark.parametrize("name", sorted(MUTATIONS))
def test_build_handoff_pin_weakened_rewrite_fails(name: str, tmp_path: Path) -> None:
    """The repository pin must turn RED on a weakened rewrite, not only on deletion."""
    old, new = MUTATIONS[name]
    copy = tmp_path / "tree"
    copy.mkdir()
    archive = subprocess.run(["git", "-C", str(ROOT), "archive", "HEAD", "loom-code"],
                             capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(copy)], input=archive, check=True)
    env = {k: v for k, v in os.environ.items() if k not in ("FORCE_COLOR", "CLAUDE_CODE_SESSION_ID")}

    def pin() -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider", PIN_TEST,
             "-k", "intent or handoff"],
            cwd=copy, env=env, capture_output=True, text=True,
        )

    control = pin()
    assert control.returncode == 0, f"control copy fails before mutation:\n{control.stdout[-600:]}"
    target = copy / "loom-code/skills/build/SKILL.md"
    text = target.read_text(encoding="utf-8")
    assert old in text
    target.write_text(text.replace(old, new, 1), encoding="utf-8")
    result = pin()
    assert result.returncode != 0, f"{name} survived the pin:\n{result.stdout[-400:]}"
