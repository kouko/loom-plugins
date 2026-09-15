"""Mutation probes: do the new station-text pins kill regressions of acceptance 1-3?

Run from the repo root:

    python3 -m pytest docs/loom/2026-09-15-station-gaps-after-dogfood/evidence/probes/test_probe_pin_mutants.py -q

Each probe copies loom-code into a temporary tree, applies one hostile edit to
the station text, and runs the change's own pin module there. A mutant the
pins let through is a surviving mutant: the probe FAILS on purpose and must
not be weakened. Mutants the pins kill PASS and stay recorded as attempts the
change survived. The unmutated control proves the copy is faithful.

Defect probes (expected to fail until the pins are strengthened):
DEFECT_PROBES below.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[5]
LOOM = REPO_ROOT / "loom-code"
BUILD_PIN = "test_build_mechanical_checks.py"
REVIEW_PIN = "test_review_convergence_contract.py"
BUILD = "loom-code/skills/build/SKILL.md"
REVIEW = "loom-code/skills/closing-review/SKILL.md"
REVIEWER = "loom-code/agents/reviewer.md"

DEFECT_PROBES = (
    "test_rerunpin_narrowedtrigger_killed",
    "test_suitepin_negatedsource_killed",
    "test_relookpin_standaloneround3relook_killed",
)


def _tree(tmp: Path) -> Path:
    root = tmp / "tree"
    shutil.copytree(
        LOOM, root / "loom-code",
        ignore=shutil.ignore_patterns("__pycache__", ".pytest_cache", "scripts"),
    )
    scripts = root / "loom-code" / "scripts"
    scripts.mkdir()
    for name in ("prose_pin.py", BUILD_PIN, REVIEW_PIN):
        shutil.copy2(LOOM / "scripts" / name, scripts / name)
    return root


def _mutate(root: Path, rel: str, old: str, new: str) -> None:
    path = root / rel
    text = path.read_text(encoding="utf-8")
    assert text.count(old) == 1, f"mutation anchor not unique in {rel}: {old!r}"
    path.write_text(text.replace(old, new), encoding="utf-8")


def _pins_pass(root: Path, pin: str) -> bool:
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    completed = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         str(root / "loom-code" / "scripts" / pin)],
        cwd=root, capture_output=True, text=True, env=env, timeout=300,
    )
    return completed.returncode == 0


def test_pincopy_unmutated_passes(tmp_path: Path) -> None:
    """The faithful copy passes both pin modules, so a failure below is the mutant's."""
    root = _tree(tmp_path)
    assert _pins_pass(root, BUILD_PIN)
    assert _pins_pass(root, REVIEW_PIN)


# --- acceptance 1: re-run after every fix ---------------------------------

def test_rerunpin_narrowedtrigger_killed(tmp_path: Path) -> None:
    """Narrowing 'after every fix' back to a returned change must fail the Build pins."""
    root = _tree(tmp_path)
    _mutate(root, BUILD, "after every fix: run", "after every fix that closing review returns: run")
    assert not _pins_pass(root, BUILD_PIN), "surviving mutant: re-run narrowed to returned changes"


def test_rerunpin_restoredoldtrigger_killed(tmp_path: Path) -> None:
    """Restoring the pre-change returned-change-only sentence must fail the Build pins."""
    root = _tree(tmp_path)
    _mutate(
        root, BUILD, "Repeat these end-of-Build checks after every fix:",
        "When closing review or a failed `finalize-review` returns the change to Build,\n"
        "repeat these end-of-Build checks after the fix:",
    )
    assert not _pins_pass(root, BUILD_PIN)


# --- acceptance 3: suite command source ------------------------------------

def test_suitepin_negatedsource_killed(tmp_path: Path) -> None:
    """Negating the suite-command sentence must fail the Build pins (prose-pin negation rule)."""
    root = _tree(tmp_path)
    _mutate(root, BUILD, "The suite command is the `package-tests:`", "The suite command is not the `package-tests:`")
    assert not _pins_pass(root, BUILD_PIN), "surviving mutant: negated suite-command source"


# --- acceptance 2: no re-look merely because the round is Round 3 ----------

def test_relookpin_standaloneround3relook_killed(tmp_path: Path) -> None:
    """A standalone 'before Round 3, re-look' paragraph outside the bullet must fail the pins."""
    root = _tree(tmp_path)
    _mutate(
        root, REVIEW, "never dispatch Round 4.\n\nTreat the episode",
        "never dispatch Round 4.\n\nBefore Round 3, always perform a technical design re-look.\n\n"
        "Treat the episode",
    )
    assert not _pins_pass(root, REVIEW_PIN), "surviving mutant: Round 3 re-look reintroduced outside the bullet"


def test_relookpin_bulletrelook_killed(tmp_path: Path) -> None:
    """Re-adding the re-look inside the Round 3 bullet must fail the pins."""
    root = _tree(tmp_path)
    _mutate(
        root, REVIEW, "- **Round 3 — terminal verification.** Review",
        "- **Round 3 — terminal verification.** First perform a technical design re-look. Review",
    )
    assert not _pins_pass(root, REVIEW_PIN)


def test_relookpin_droppedround2condition_killed(tmp_path: Path) -> None:
    """Dropping 'Round 2 still has blockers' from the stuck rule must fail the pins."""
    root = _tree(tmp_path)
    _mutate(root, REVIEW, "stuck when Round 2 still has blockers, the same", "stuck when the same")
    assert not _pins_pass(root, REVIEW_PIN)


def test_relookpin_reviewerround3relook_killed(tmp_path: Path) -> None:
    """Re-tying the reviewer contract's Round 3 to the technical design re-look must fail the pins."""
    root = _tree(tmp_path)
    _mutate(
        root, REVIEWER, "- Round 3 is terminal. If",
        "- Round 3 is terminal and occurs only after the technical design re-look. If",
    )
    assert not _pins_pass(root, REVIEW_PIN)
