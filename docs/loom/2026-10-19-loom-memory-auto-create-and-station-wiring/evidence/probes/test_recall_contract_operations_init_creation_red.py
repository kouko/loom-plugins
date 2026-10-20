# concern: Acceptance 3 (Recall never creates a store) must hold for the
# whole shipped contract, not only SKILL.md's Recall section —
# references/operations.md carries the same operation and is not guarded, so
# a creation step can be added to Recall there with every contract test
# still green, violating "absent store is still a normal no-memory result".
"""Adversarial probe — the Recall no-creation contract is only pinned in
SKILL.md; operations.md's Recall can gain an `init` creation step and every
contract test stays green.

The regression guard `test_recall_absent_store_stays_normal_no_memory` reads
only the SKILL.md Recall section. This probe adds a store-creation step to
operations.md's Recall procedure, runs that real guard test against the
mutated tree, and requires the guard to go RED.

RED today: the guard reads only SKILL.md, never notices the operations.md
change, and stays green — the probe's assertion fails.
"""

from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[5]
OPERATIONS_REL = "loom-workflow/skills/loom-memory/references/operations.md"
GUARD_TEST = (
    "loom-workflow/tests/loom-memory/test_skill_contract.py"
    "::test_recall_absent_store_stays_normal_no_memory"
)

RECALL_ABSENT_SENTENCE = (
    "## Recall\n"
    "\n"
    "1. Locate the store. Its absence is a normal no-memory result — report it\n"
    "   and move on; never treat a missing store as an error to fix."
)
CREATION_LEAK = (
    "## Recall\n"
    "\n"
    "1. Locate the store. Its absence is a normal no-memory result — report it\n"
    "   and move on — creating it first with `init` when missing; never treat\n"
    "   a missing store as an error to fix."
)


def _extract_head(dest: pathlib.Path) -> None:
    archive = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "archive", "HEAD"],
        capture_output=True,
        check=True,
    ).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)


def test_recall_contract_operations_init_creation_red() -> None:
    """Recall contract: a store-creation step in operations.md's Recall must
    turn the no-creation guard red; the guard misses it today, so this probe
    is RED."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="loom-adv-c-"))
    try:
        _extract_head(tmp)
        ops = tmp / OPERATIONS_REL
        text = ops.read_text(encoding="utf-8")
        assert RECALL_ABSENT_SENTENCE in text, "probe precondition: Recall absent-store sentence not found"
        ops.write_text(text.replace(RECALL_ABSENT_SENTENCE, CREATION_LEAK), encoding="utf-8")
        assert "creating it first with `init` when missing" in ops.read_text(encoding="utf-8")

        result = subprocess.run(
            [sys.executable, "-m", "pytest", str(tmp / GUARD_TEST), "-q"],
            capture_output=True,
            text=True,
        )
        assert result.returncode == 1, (
            "the Recall no-creation guard stayed green while operations.md's "
            f"Recall gained an init step (pytest exit {result.returncode}, "
            f"stderr: {result.stderr[-500:]})"
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
