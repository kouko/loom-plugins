# concern: evidence store exemption - non-test .py files under evidence store incorrectly exempted
"""Adversarial probe demonstrating that .py files under docs/loom/evidence/ that
don't match test naming patterns are incorrectly exempted from test case pair
requirements.

Files like docs/loom/evidence/my_util.py should NOT be exempt because they
represent behavior changes, not prose evidence.
"""

import sys
import tempfile
import subprocess
from pathlib import Path

def test_non_test_py_under_evidence_store_requires_test_pairs():
    """A non-test .py file under docs/loom/evidence/ should NOT be exempt."""

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
        (repo / "docs" / "loom" / "evidence").mkdir(parents=True)
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

        # Create a .py file under evidence store that DOESN'T match test naming pattern
        # This should NOT be exempt because it's not a test file
        py_file = repo / "docs" / "loom" / "evidence" / "data_processor.py"
        py_file.write_text("# Processes data for tests - behavior change\n\
def process_test_data(raw_data):\n\
    cleaned = [x.strip() for x in raw_data if x]\n\
    return [int(x) for x in cleaned if x.isdigit()]\n")

        # Create plan that incorrectly claims this .py file is exempt
        plan_content = f"""# Test plan
intent: {change_id}@abc1234
charter: 1.1

## Task DAG
**W0-01 Data Processor**  after: —  acceptance: 1
- Files: `docs/loom/evidence/data_processor.py`
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

        # Debug: let's see what happened
        if result.returncode == 0:
            print(f"VULNERABILITY CONFIRMED: non-test .py file under evidence store incorrectly exempted")
            return True
        else:
            print(f"Task incorrectly requires test pair - this might be correct or might indicate another issue")
            print(f"Return code: {result.returncode}")
            if result.stderr:
                print(f"STDERR: {result.stderr}")
            if "intake.test-case-pair" in result.stderr:
                print(f"This suggests the system correctly identified it needs test pairs")
            return False

if __name__ == "__main__":
    vulnerable = test_non_test_py_under_evidence_store_requires_test_pairs()
    exit(1 if vulnerable else 0)