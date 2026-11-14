# concern: a substring prose pin cannot see negation — the sentence-shape
# check looks for "concise" + "connect", for "human reading experiment" and
# for "sentence shapes" + "rule 3" anywhere in the text, so a guide rewritten
# to say the opposite of Acceptance 2, 3 or 6 still passes its own tests.
"""Adversarial probe: the plain-language guide's tests accept inverted guidance.

Each case copies the working-tree guide and its test module into a temp
tree, rewrites one sentence of the guide into its opposite, runs the real
test module there, and requires that run to fail.

RED today: every inverted sentence keeps the substrings the check greps
for, so the test module still passes on the mutated guide.
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
    tmp = pathlib.Path(tempfile.mkdtemp(prefix="loom-adv-shape-"))
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


def test_rule7_concise_sentence_inverted_rejected() -> None:
    """Acceptance 2: a rule 7 that says concise means dropping connecting words must fail the tests."""
    code = _run_guide_tests(
        r"It\s+never means dropping the words that connect a sentence: keep",
        "It also means dropping the words that connect a sentence: drop",
    )
    assert code == 1, "the guide's tests passed a rule 7 that tells the agent to drop connecting words"


def test_rewrite_step5_shape_check_inverted_rejected() -> None:
    """Acceptance 3: a last rewrite step that excludes the sentence shapes must fail the tests."""
    code = _run_guide_tests(
        r"and for the five sentence shapes of rule 3 before sending",
        "but never for the five sentence shapes of rule 3 before sending",
    )
    assert code == 1, "the guide's tests passed a rewrite step that never checks the sentence shapes"


def test_study_limit_reading_experiment_inverted_rejected() -> None:
    """Acceptance 6: a guide claiming the study ran a human reading experiment must fail the tests."""
    code = _run_guide_tests(
        r"it ran no human reading\s+experiment",
        "it ran a human reading experiment",
    )
    assert code == 1, "the guide's tests passed a study limit rewritten into the opposite claim"
