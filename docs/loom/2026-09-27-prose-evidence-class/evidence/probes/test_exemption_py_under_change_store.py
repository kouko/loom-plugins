# concern: exemption loophole - .py files under change store incorrectly exempted from test case pairs
"""Adversarial probe demonstrating that .py files under docs/loom/<change-id>/ are
incorrectly exempted from test case pair requirements, allowing behavior changes
to slip through without required tests.

The exemption logic in _is_task_exempt_from_test_pairs() incorrectly exempts
ALL files under change/evidence stores regardless of type, when only low-risk
doc extensions (.md/.mdx/.rst/.txt) should be exempt for prose evidence.
"""

import sys
import tempfile
import subprocess
from pathlib import Path

def test_py_under_change_store_requires_test_pairs():
    """A .py file under docs/loom/<change-id>/ should NOT be exempt from test pairs."""

    with tempfile.TemporaryDirectory() as tmpdir:
        repo = Path(tmpdir)
        # Initialize git repo with proper remote tracking
        subprocess.run(["git", "init", "-q"], cwd=repo, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=repo, check=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=repo, check=True)

        (repo / "initial.txt").write_text("initial\n")
        subprocess.run(["git", "add", "initial.txt"], cwd=repo, check=True)
        subprocess.run(["git", "commit", "-q", "-m", "initial"], cwd=repo, check=True)

        # Set up remote tracking branches
        subprocess.run(["git", "update-ref", "refs/remotes/origin/main", "HEAD"], cwd=repo, check=True)
        subprocess.run(["git", "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/main"], cwd=repo, check=True)
        subprocess.run(["git", "checkout", "-q", "-b", "work"], cwd=repo, check=True)

        change_id = "2026-09-27-prose-evidence-class"
        (repo / "docs" / "loom" / change_id).mkdir(parents=True)
        (repo / "docs" / "loom" / "intent").mkdir(parents=True, exist_ok=True)

        # Create intent file
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

        # Create a .py file under the change store - this represents a behavior change
        # and should NOT be exempt from test case pair requirements
        py_file = repo / "docs" / "loom" / change_id / "behavior_change.py"
        py_file.write_text("# This is a behavior change that modifies system behavior\n\
def process_data(input_data):\n\
    return transform(input_data)\n\
\ndef transform(data):\n\
    return [x * 2 for x in data]\n")

        # Create plan that incorrectly claims this .py file is exempt
        plan_content = f"""# Test plan
intent: {change_id}@abc1234
charter: 1.1

## Task DAG
**W0-01 Behavior Change**  after: —  acceptance: 1
- Files: `docs/loom/{change_id}/behavior_change.py`
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

        # Run the intake checker
        checker_path = Path(__file__).resolve().parents[5] / "loom-code" / "scripts" / "loom_checker.py"
        result = subprocess.run([
            sys.executable, str(checker_path),
            "intake", "write-plan", change_id
        ], cwd=repo, capture_output=True, text=True)

        # If the change incorrectly passes (returncode 0), the vulnerability exists
        # If it correctly fails with intake.test-case-pair, the vulnerability is fixed
        if result.returncode == 0:
            print(f"VULNERABILITY CONFIRMED: .py file under change store was incorrectly exempted")
            print(f"This allows behavior changes to slip through without required tests")
            return True  # Attack succeeded - vulnerability exists
        else:
            if "intake.test-case-pair" in result.stderr:
                print(f"NO VULNERABILITY: .py file under change store correctly requires test pair")
                return False  # Attack failed - no vulnerability
            else:
                print(f"UNEXPECTED ERROR: intake failed for other reason")
                print(f"STDERR: {result.stderr}")
                return False

if __name__ == "__main__":
    # Return code 0 means no vulnerability (system works correctly)
    # Return code 1 means vulnerability exists (defect exposed)
    vulnerable = test_py_under_change_store_requires_test_pairs()
    exit(1 if vulnerable else 0)