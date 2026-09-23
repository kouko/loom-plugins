"""Adversarial probe: the tester returns the same verdicts the report template lets it write.

The template now allows four verdicts -- works / partly / not verified / fails.
The tester's contract still returns `works | partly | not-yet` to the station
and says a line it could not try is `not-yet`. A tester following both writes
"not verified" in the report and `not-yet` in its return, and has no return
value at all for a row the report marks "fails".

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-23-lighter-acceptance-testing/evidence/probes/test_verdict_vocabulary_contract_matches_template.py -q

concern: vocabulary drift -- the tester's returned verdict set differs from the report template's verdict set, so a failing or untried line is named two ways
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
TESTER = REPO / "loom-code" / "agents" / "acceptance-tester.md"
TEMPLATE = REPO / "loom-code" / "skills" / "closing-review" / "references" / "acceptance-test-report.md"


def _norm(word: str) -> str:
    return word.strip().replace("-", " ").lower()


def _template_verdicts() -> set[str]:
    text = " ".join(TEMPLATE.read_text(encoding="utf-8").split())
    match = re.search(r"Verdict is one of ([a-z /-]+?)\.", text)
    assert match, "template no longer lists its verdicts"
    return {_norm(w) for w in match.group(1).split("/")}


def _returned_verdicts() -> set[str]:
    text = TESTER.read_text(encoding="utf-8")
    match = re.search(r"result: ([a-z |-]+?),", text)
    assert match, "tester contract no longer lists its returned results"
    return {_norm(w) for w in match.group(1).split("|")}


def test_verdictvocabulary_returnedset_equalstemplateset():
    """Every verdict the report may carry has the same name in the tester's return, and no other."""
    assert _returned_verdicts() == _template_verdicts(), (
        f"returned {sorted(_returned_verdicts())} vs template {sorted(_template_verdicts())}"
    )


def test_verdictvocabulary_untriedline_usestemplateword():
    """The contract's word for a line it could not try is one of the template's verdicts."""
    text = " ".join(TESTER.read_text(encoding="utf-8").split())
    match = re.search(r"An Acceptance line you could not try is `([^`]+)`", text)
    assert match, "tester contract no longer names the untried-line verdict"
    assert _norm(match.group(1)) in _template_verdicts(), match.group(1)
