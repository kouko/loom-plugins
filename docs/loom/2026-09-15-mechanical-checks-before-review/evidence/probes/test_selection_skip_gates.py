"""Adversarial probe: expert-mode skips against the new Build and
closing-review gates.

`finalize-review` waives `package-tests` and `adversarial` independently
(finalize.py reads each from the bound selection). The new prose gates must
let an agent do the same without guessing:

* Build's hand-off gate ("does not hand off to Review until the complete
  package suite and every adversarial program pass") must carry the skip
  exception in the gate sentence itself; otherwise a `package-tests` skip
  either blocks hand-off forever or makes the agent run the suite anyway.
* closing review's reviewer-dispatch gate must name each skippable step;
  "or that `selection show` lists that step as skipped" has two antecedents,
  and the lazy reading lets one skip waive both checks.

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-mechanical-checks-before-review/evidence/probes/test_selection_skip_gates.py -q
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
BUILD = (REPO / "loom-code/skills/build/SKILL.md").read_text(encoding="utf-8")
REVIEW = (REPO / "loom-code/skills/closing-review/SKILL.md").read_text(encoding="utf-8")
VERIFY = " ".join(BUILD.split("## 3. Verify integration", 1)[1].split("## 4.", 1)[0].split())
DEPTH = " ".join(REVIEW.split("## 2. Compute review depth", 1)[1].split("\n## ", 1)[0].split())
SKIP_QUALIFIER = re.compile(r"\bskipped\b|\bunless\b", re.IGNORECASE)


def _sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.;])\s+", text) if s]


def _unqualified_handoff_gates(text: str) -> list[str]:
    return [
        s for s in _sentences(text)
        if "hand off" in s and "until" in s and "package suite" in s
        and not SKIP_QUALIFIER.search(s)
    ]


def _dispatch_gate_names_each_step(sentence: str) -> bool:
    return "`package-tests`" in sentence and "`adversarial`" in sentence


def test_handoffgate_qualifiedsentence_accepted() -> None:
    """Synthetic: a gate carrying its skip exception is accepted."""
    s = ("Build hands off to Review once the complete package suite and every "
         "adversarial program pass, unless `selection show` lists them as skipped.")
    s2 = "Build does not hand off to Review until the complete package suite passes."
    assert not _unqualified_handoff_gates(s)
    assert _unqualified_handoff_gates(s2)


def test_dispatchgate_singularantecedent_rejected() -> None:
    """Synthetic: 'that step' is rejected; naming both step ids is accepted."""
    assert not _dispatch_gate_names_each_step("or that `selection show` lists that step as skipped.")
    assert _dispatch_gate_names_each_step(
        "or that `selection show` lists `package-tests` or `adversarial` as skipped for that check.")


def test_buildskip_rulesorder_precedesrerun() -> None:
    """Recorded attack the text survives: the skip rules precede the fix-loop re-run."""
    skip = VERIFY.index("lists `adversarial` as skipped")
    rerun = VERIFY.index("repeat these end-of-Build checks")
    assert skip < rerun


def test_buildhandoffgate_packagetestsskipped_carriesskipexception() -> None:
    """A `package-tests` skip must not leave an unconditional hand-off gate."""
    assert not _unqualified_handoff_gates(VERIFY), _unqualified_handoff_gates(VERIFY)


def test_reviewdispatchgate_oneskipped_nameseachstep() -> None:
    """The reviewer-dispatch gate names `package-tests` and `adversarial` separately."""
    gate = next(s for s in _sentences(DEPTH) if s.startswith("Before dispatching reviewers in any round"))
    assert _dispatch_gate_names_each_step(gate), gate
