# concern: mixed-delta exemption - tasks with both docs and .py files incorrectly exempted
"""Adversarial probe demonstrating that tasks containing both documentation files
and behavior files (.py) under change/evidence stores are incorrectly exempted
from test case pair requirements.

Since the exemption logic exempts ALL files under change/evidence stores
regardless of type, a task with one exempt .md file and one non-exempt .py file
incorrectly passes the "ALL paths must be exempt" check.
"""

import sys
import tempfile
import subprocess
from pathlib import Path

def test_mixed_docs_and_py_requires_test_pairs():
    """A task with both .md and .py files under change store should NOT be exempt."""

    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Path(tmpdir)
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)

        (repo / "initial.txt").write_text("initial\n")
        subprocess.run(["git", "add", "initial.txt"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=repo, check=True)

        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=repo, check=True)
        subprocess.run(["git", "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main"], cwd=repo, check=True)
        subprocess.run(["git", "checkout", "-q", "-b", "work"], cwd=repo, check=True)

        change_id = "2026-09-27-prose-evidence-class"
        (repo / "docs" / "loom" / change_id).mkdir(parents=True)
        (repo / "docs" / "loom" / "intent").mkdir(parents=True, exist_ok=True)
        (repo / "docs" / "loom" / "intent" / f"{change_id}.md").write_text(f"""# Test intent
originator: tester
kind: engineering
needs-design: no
status: confirmed 2026-09-27

## Problem
Test problem

## Proposed outcome
Test outcome

## Acceptance
1. Test acceptance

## Constraints
- None

## Out of scope
- None

## Open questions
- none
""")

        # Create both a documentation file (should be exempt) and a behavior file (should NOT be exempt)
        (repo / "docs" / "loom" / change_id / "README.md").write_text("# Documentation\n")
        py_file = repo / "docs" / "loom" / change_id / "processor.py"
        py_file.write_text("# This processes data - a behavior change\n\
def process(items):\n\
    return [item.upper() for item in items]\n")

        # Create plan that incorrectly claims the mixed task is exempt
        plan_content = f"""# Test plan
intent: {change_id}@abc1234
charter: 1.1

## Task DAG
**W0-01 Mixed Task**  after: —  acceptance: 1
- Files: `docs/loom/{change_id}/README.md, docs/loom/{change_id}/processor.py`
- Test:
- Risk: agent-decided — should require test pair but claims exemption

## Questions asked
1 — what — none

## Risks
1. None.

## Simplicity check
- Reuse reviewers.py path sets for the exemption instead of a new classifier — taken
"""
        (repo / "docs" / "loom" / change_id / "plan.md").write_text(plan_content)

        checker_path = Path(__file__).resolve().parents[5] / "loom-code" / "scripts" / "loom_checker.py"
        result = subprocess.run([
            sys.executable, str(checker_path),
            "intake", "write-plan", change_id
        ], cwd=repo, capture_output=True, text=True)

        if result.returncode == 0:
            print(f"VULNERABILITY CONFIRMED: mixed docs+py task incorrectly exempted")
            print(f"The .py file's behavior change slips through due to over-broad exemption")
            return True
        else:
            if "intake.test-case-pair" in result.stderr:
                print(f"NO VULNERABILITY: mixed docs+py task correctly requires test pair")
                return False
            else:
                print(f"UNEXPECTED ERROR: {result.stderr}")
                return False

if __name__ == "__main__":
    vulnerable = test_mixed_docs_and_py_requires_test_pairs()
    exit(1 if vulnerable else 0)