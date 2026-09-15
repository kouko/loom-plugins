"""Hostile-reading and constraint probes for closing-review re-look, word budget, checker code.

Run from the repo root (needs the branch base 9906c79c in the clone):

    python3 -m pytest docs/loom/2026-09-15-station-gaps-after-dogfood/evidence/probes/test_probe_relook_and_budget.py -q

Every probe here is an attempt the change is expected to survive; a failure
is a real regression. A missing base commit fails loudly rather than skipping,
because a skipped probe would read as a pass in finalize-review.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO_ROOT / "loom-code" / "scripts"))

from prose_pin import has_negation, split_sentences  # noqa: E402

BASE = "9906c79c"
BUILD = "loom-code/skills/build/SKILL.md"
REVIEW = "loom-code/skills/closing-review/SKILL.md"
REVIEW_TEXT = (REPO_ROOT / REVIEW).read_text(encoding="utf-8")
REVIEW_WORDS = " ".join(REVIEW_TEXT.split())
FINALIZE = " ".join(REVIEW_TEXT.split("## 5. Finalize", 1)[1].split("## Handoff", 1)[0].split())
NO_RELOOK = "No technical design re-look precedes that round unless the episode is stuck."


def _git(*args: str) -> str:
    completed = subprocess.run(["git", "-C", str(REPO_ROOT), *args], capture_output=True, text=True)
    assert completed.returncode == 0, f"git {' '.join(args)} failed: {completed.stderr}"
    return completed.stdout


def _stuck_trigger() -> str:
    stuck = next(s for s in split_sentences(REVIEW_WORDS, ends=".") if s.startswith("Treat the episode as stuck"))
    return stuck.partition(";")[0]


def test_stuckrule_finalizefailure_nottrigger() -> None:
    """Hostile reading: no stuck-rule condition names a finalize failure, so S7-a cannot enter it by text."""
    trigger = _stuck_trigger()
    assert "finalize" not in trigger, trigger
    assert "Round 3" not in trigger, trigger


def test_finalizesection_norelook_followsfailure() -> None:
    """The no-re-look sentence sits after the finalize failure return, in the same paragraph."""
    fail = FINALIZE.index("When `finalize-review` fails")
    at = FINALIZE.index(NO_RELOOK)
    assert fail < at
    assert "Handoff" not in FINALIZE[fail:at]


def test_round3bullet_relookword_absent() -> None:
    """Time-pressure reading: nothing in the Round 3 bullet invites a re-look step."""
    start = REVIEW_TEXT.index("- **Round 3")
    bullet = " ".join(REVIEW_TEXT[start:].split("\n\n", 1)[0].split())
    for word in ("re-look", "re-plan", "redesign", "first"):
        assert word not in bullet.lower(), bullet


def test_stuckrule_round2blockers_relookaffirmed() -> None:
    """Constraint: Round 2 blockers still lead to the technical design re-look before Round 3."""
    stuck = next(s for s in split_sentences(REVIEW_WORDS, ends=".") if s.startswith("Treat the episode as stuck"))
    trigger, _, action = stuck.partition(";")
    assert "Round 2 still has blockers" in trigger
    assert "only after the technical design re-look" in action
    assert not has_negation(action), action


def test_wordbudget_buildplusreview_notabovebase() -> None:
    """Acceptance 5 recounted with str.split against the base commit, not a remembered number."""
    base = sum(len(_git("show", f"{BASE}:{p}").split()) for p in (BUILD, REVIEW))
    head = sum(len((REPO_ROOT / p).read_text(encoding="utf-8").split()) for p in (BUILD, REVIEW))
    assert head <= base, (head, base)


def test_checkercode_diffsincebase_empty() -> None:
    """Acceptance 6: no checker code, attestation or push validation changed since the base."""
    changed = _git("diff", "--name-only", BASE, "HEAD", "--",
                   "loom-code/scripts/loom_checker", "loom-code/scripts/loom_checker.py").split()
    assert changed == [], changed
