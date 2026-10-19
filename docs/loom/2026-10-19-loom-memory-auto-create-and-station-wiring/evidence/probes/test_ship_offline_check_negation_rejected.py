# concern: the ship offline routing check must reject a negated routing
# sentence ("Never use loom-workflow:loom-memory to route a qualifying
# durable repository lesson") — a substring grep for
# "loom-workflow:loom-memory" + "durable repository lesson" cannot tell
# the sentence is inverted, so a rewrite that forbids the routing the
# change promises still passes the guard.
"""Adversarial probe — ship's offline loom-memory routing check accepts an
inverted routing sentence.

Check 2 of `loom-code/tests/local/test-git-memory-delegation.sh` passes when
the ship SKILL.md text contains both "loom-workflow:loom-memory" and
"durable repository lesson" anywhere. This probe rewrites the routing
sentence into its exact negation, runs the real offline script against the
mutated tree, and requires the routing check to FAIL.

RED today: the negated sentence still contains both substrings, so the
script prints the routing PASS line — the probe's assertion fails.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[5]
SHIP_SKILL_REL = "loom-code/skills/ship/SKILL.md"
OFFLINE_CHECK_REL = "loom-code/tests/local/test-git-memory-delegation.sh"
ROUTING_PASS_LINE = (
    "PASS — ship routes a qualifying durable repository lesson to "
    "loom-workflow:loom-memory"
)

AFFIRMATIVE = "Use `loom-workflow:loom-memory` to route a qualifying durable repository lesson"
NEGATED = "Never use `loom-workflow:loom-memory` to route a qualifying durable repository lesson"


def _extract_head(dest: pathlib.Path) -> None:
    archive = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "archive", "HEAD"],
        capture_output=True,
        check=True,
    ).stdout
    subprocess.run(["tar", "-x", "-C", str(dest)], input=archive, check=True)


def test_ship_offline_check_negation_rejected() -> None:
    """Ship routing guard: a negated routing sentence must fail the offline
    routing check; the check passes it today, so this probe is RED."""
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="loom-adv-b-"))
    try:
        _extract_head(tmp)
        skill = tmp / SHIP_SKILL_REL
        text = skill.read_text(encoding="utf-8")
        assert AFFIRMATIVE in text, "probe precondition: routing sentence not found verbatim"
        text = text.replace(AFFIRMATIVE, NEGATED)
        # the sentence itself must now forbid the routing
        assert re.search(r"Never use `loom-workflow:loom-memory`", text)
        skill.write_text(text, encoding="utf-8")

        result = subprocess.run(
            ["bash", str(tmp / OFFLINE_CHECK_REL)],
            cwd=tmp,
            capture_output=True,
            text=True,
        )
        assert ROUTING_PASS_LINE not in result.stdout, (
            "the offline routing check passed an inverted routing sentence — "
            "grep for two substrings cannot see the negation:\n"
            + "\n".join(
                line for line in result.stdout.splitlines() if "loom-memory" in line
            )
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
