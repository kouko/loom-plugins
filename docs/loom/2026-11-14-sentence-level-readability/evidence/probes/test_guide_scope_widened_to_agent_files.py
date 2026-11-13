# concern: an acceptance line with no executable guard — Acceptance 5 (the
# guide covers chat text only, never files written for an agent) is held
# only by a check that a "Scope" heading exists, so a guide whose Scope
# body is rewritten to cover agent-read files still passes its own tests.
"""Adversarial probe: the plain-language guide's tests never read the Scope body.

The plan says the existing rules-and-steps test holds the scope-kept and
agent-docs-excluded cases. This probe copies the working-tree guide and its
test module into a temp tree, rewrites the Scope sentence so the guide also
covers files the agent writes, runs the real test module there, and
requires that run to fail.

RED today: the test module asserts only that a "Scope" section exists, so
it still passes on the widened scope.
"""

from __future__ import annotations

import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

REPO_ROOT = pathlib.Path(__file__).resolve().parents[5]
SKILL_REL = "loom-workflow/skills/loom-visualization"
GUIDE_REL = SKILL_REL + "/references/plain-language.md"
TESTS_REL = "loom-workflow/tests/loom-visualization/test_references.py"


def _run_guide_tests(pattern: str, replacement: str) -> int:
    """Run the guide's test module on a temp copy of the skill, before and after one mutation.

    Returns the exit code of the mutated run; the unmutated run must pass first,
    so a failing mutated run comes from the mutation alone.
    """
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="loom-adv-scope-"))
    try:
        shutil.copytree(REPO_ROOT / SKILL_REL, tmp / SKILL_REL)
        (tmp / TESTS_REL).parent.mkdir(parents=True)
        shutil.copyfile(REPO_ROOT / TESTS_REL, tmp / TESTS_REL)
        command = [sys.executable, "-m", "pytest", "-p", "no:cacheprovider", str(tmp / TESTS_REL)]
        control = subprocess.run(command, cwd=tmp, capture_output=True, text=True)
        assert control.returncode == 0, "probe precondition: unmutated copy fails\n" + control.stdout
        guide = tmp / GUIDE_REL
        text, count = re.subn(pattern, replacement, guide.read_text(encoding="utf-8"))
        assert count == 1, f"probe precondition: {pattern!r} matched {count} times"
        guide.write_text(text, encoding="utf-8")
        return subprocess.run(command, cwd=tmp, capture_output=True, text=True).returncode
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def test_guide_scope_widened_to_agent_files_rejected() -> None:
    """Acceptance 5: a Scope that also covers files the agent writes must fail the tests."""
    code = _run_guide_tests(
        r"It never covers files you write:",
        "It also covers files you write:",
    )
    assert code == 1, "the guide's tests passed a Scope that covers intents, specs, plans and code comments"
