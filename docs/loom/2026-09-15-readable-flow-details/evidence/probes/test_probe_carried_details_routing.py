"""Adversary probes: states the carried-details rules never mention.

1. A `kind: product` change with `needs-design: no`. capture-intent's
   decision point ① shows carried details for engineering only and says "A
   product change shows them at `write-spec`'s decision point ② instead". But
   `needs-design: no` routes to write-plan, never to write-spec, and
   write-plan's intake runs `intake.confirmed-behavior` only on `yes`. So a
   product change's carried details can reach a plan with no user stop
   showing them.
2. A product change's carried detail that is not visible. write-spec and
   write-plan both record it "on the matching Requirement or Design decision
   line", while decision point ② shows "nothing from `## Design decision`
   down". A detail recorded on a Design decision line never reaches the user.

Prose pins follow the baseline: an affirmative verb before the pinned
literal, no negation token in that sentence, synthetic self-tests.

Run from the repo root:
    python3 -m pytest docs/loom/2026-09-15-readable-flow-details/evidence/probes/test_probe_carried_details_routing.py -q -p no:cacheprovider
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def _find_repo_root(start: Path) -> Path:
    """Walk upward until a directory holding docs/loom is found."""
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs" / "loom").is_dir() and (candidate / "loom-code").is_dir():
            return candidate
    raise RuntimeError(f"repo root not found above {start}")


ROOT = _find_repo_root(Path(__file__).parent)
sys.path.insert(0, str(ROOT / "loom-code" / "scripts"))

from prose_pin import has_negation, split_sentences  # noqa: E402

CAPTURE = ROOT / "loom-design/skills/capture-intent/SKILL.md"
WRITE_SPEC = ROOT / "loom-design/skills/write-spec/SKILL.md"
WRITE_PLAN = ROOT / "loom-code/skills/write-plan/SKILL.md"
CHECKER = ROOT / "loom-code/scripts/loom_checker.py"


def _flat(text: str) -> str:
    return " ".join(text.split())


def _section(text: str, heading: str) -> str:
    match = re.search(rf"^{re.escape(heading)}$.*?(?=^## |\Z)", text, re.M | re.S)
    assert match, f"section {heading!r} missing"
    return match.group(0)


def affirmative_pin(text: str, verb: str, literal: str) -> bool:
    """True when some sentence holds `verb` before `literal` and no negation token."""
    for sentence in split_sentences(_flat(text), ".;"):
        v = re.search(rf"\b{verb}\b", sentence)
        at = sentence.find(literal)
        if v and at > v.start() and not has_negation(sentence):
            return True
    return False


# --- synthetic self-tests for the pin ---


def test_affirmativePin_syntheticAffirmativeSentence_accepted() -> None:
    """An affirmative sentence with the verb before the literal is accepted."""
    assert affirmative_pin("A product change shows them at write-plan's decision point.", "shows", "write-plan")


def test_affirmativePin_syntheticNegatedSentence_rejected() -> None:
    """The same sentence carrying a negation token is rejected."""
    assert not affirmative_pin(
        "A product change never shows them at write-plan's decision point.", "shows", "write-plan"
    )


# --- 1. product change with needs-design: no ---


def test_captureIntentProductRouting_needsDesignNo_namesWritePlanConfirmation() -> None:
    """Decision point ① names where a product change without a spec station shows its carried details."""
    item = _section(CAPTURE.read_text(encoding="utf-8"), "## Step 4 — Decision point ①: restate and confirm")
    item = item.split("5. **The carried details", 1)[1].split("Questions may only ask", 1)[0]
    assert affirmative_pin(item, "shows", "write-plan"), (
        "the only routing for a product change names write-spec, which a needs-design: no change never reaches"
    )


def _git(repo: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=repo, check=True, capture_output=True, text=True)


INTENT = """# Export my tasks
originator: kouko
kind: product
needs-design: no — no new surface, same export command gains a question
status: confirmed 2026-09-15

## Problem
Backing up tasks overwrites the last copy without asking.

## Proposed outcome
The user keeps the last copy unless they agree to replace it.

## Value case
kouko; lost a backup last week; GO.

## Acceptance
1. The user keeps the last copy unless they agree to replace it.

## Constraints
- none

## Out of scope
- syncing

## Open questions
- none
"""

SPEC_WITHOUT_CONFIRMATION = """# Export my tasks — spec
intent: probe-product-no-design@0000000
pre-build-review: not-required — small

## Requirements
REQ-1 — Ask before replacing
  WHEN the export file exists, the command shall ask before replacing it → Acceptance #1

## Design decision
- carried detail from the conversation: the question defaults to no. agent-decided

## Alternatives considered
- always overwrite: loses data

## Current state evidence
- Forward: N/A — probe fixture

## UI flows
todo export with an existing file → the question replace todo-export? [y/N]
"""


NO_DESIGN_LINE = "needs-design: no — no new surface, same export command gains a question"


def _intake(tmp_path: Path, needs_design_line: str) -> subprocess.CompletedProcess:
    """Build a repo with an origin remote, confirmed product intent and unconfirmed spec; run intake."""
    change_id = "probe-product-no-design"
    work = tmp_path / "work"
    intent = work / "docs/loom/intent" / f"{change_id}.md"
    spec = work / "docs/loom" / change_id / "spec.md"
    intent.parent.mkdir(parents=True)
    spec.parent.mkdir(parents=True)
    intent.write_text(INTENT.replace(NO_DESIGN_LINE, needs_design_line), encoding="utf-8")
    spec.write_text(SPEC_WITHOUT_CONFIRMATION, encoding="utf-8")
    who = ["-c", "user.name=probe", "-c", "user.email=probe@example.invalid"]
    _git(work, "init", "-q", "-b", "main")
    _git(work, *who, "add", ".")
    _git(work, *who, "commit", "-q", "-m", f"docs(loom): intent probe confirmed\n\n{needs_design_line}")
    _git(tmp_path, "init", "-q", "--bare", str(tmp_path / "origin.git"))
    _git(work, "remote", "add", "origin", str(tmp_path / "origin.git"))
    _git(work, "push", "-q", "origin", "main")
    _git(work, "fetch", "-q", "origin")
    _git(work, "remote", "set-head", "origin", "main")
    _git(work, "switch", "-q", "-c", f"feat/{change_id}")
    return subprocess.run(
        [sys.executable, str(CHECKER), "intake", "write-plan", change_id],
        cwd=work, capture_output=True, text=True,
    )


def test_writePlanIntake_productNeedsDesignYesUnconfirmed_blocksOnConfirmedBehavior(tmp_path: Path) -> None:
    """Control: the same unconfirmed product spec under needs-design: yes blocks on confirmed-behavior."""
    result = _intake(tmp_path, NO_DESIGN_LINE.replace("needs-design: no", "needs-design: yes"))
    assert result.returncode != 0
    assert "intake.confirmed-behavior" in result.stdout + result.stderr, result.stdout + result.stderr


def test_writePlanIntake_productNoDesignSpecUnconfirmed_blocksOnConfirmedBehavior(tmp_path: Path) -> None:
    """write-plan intake blocks a product spec holding carried details that no user stop confirmed."""
    result = _intake(tmp_path, NO_DESIGN_LINE)
    output = result.stdout + result.stderr
    assert "Traceback" not in output, output
    assert "intake.confirmed-behavior" in output, (
        "intake write-plan does not check confirmed-behavior for a kind: product spec because "
        f"needs-design is no; exit={result.returncode} output={output!r}"
    )


# --- 2. a product change's non-visible carried detail ---


def _design_decision_sentences(text: str) -> list[str]:
    return [s for s in split_sentences(_flat(text), ".;") if "Design decision line" in s]


def test_writeSpecCarriedDetail_productNonVisible_recordedWhereShown() -> None:
    """write-spec routes a product change's carried detail only to lines decision point ② shows."""
    step2 = _section(WRITE_SPEC.read_text(encoding="utf-8"), "## Step 2 — Write the spec")
    carried = step2.split("**Carried details.**", 1)[1].split("Forms:", 1)[0]
    routing = _design_decision_sentences(carried)
    assert routing, "carried-details routing sentence missing"
    assert all("engineering" in s for s in routing), (
        "a product change's carried detail may land on a Design decision line, which ② never shows: "
        + routing[0]
    )


def test_writePlanCarriedDetail_productNonVisible_recordedWhereShown() -> None:
    """write-plan routes a product change's carried detail only to lines decision point ② shows."""
    step4 = _section(WRITE_PLAN.read_text(encoding="utf-8"), "## Step 4 — Does this need a spec?")
    bullet = step4.split("- Record each carried detail", 1)[1].split("\n\n", 1)[0]
    routing = _design_decision_sentences("Record each carried detail" + bullet)
    assert routing, "carried-details routing sentence missing"
    assert all("engineering" in s for s in routing), (
        "a product change's carried detail may land on a Design decision line, which ② never shows: "
        + routing[0]
    )
