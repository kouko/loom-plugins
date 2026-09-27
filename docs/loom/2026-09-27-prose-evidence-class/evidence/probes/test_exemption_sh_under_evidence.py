# concern: evidence store exemption - .sh files under evidence store incorrectly exempted
"""Adversarial probe demonstrating that .sh files under docs/loom/evidence/ are
incorrectly exempted from test case pair requirements.

Shell scripts under evidence store that don't match test naming patterns
should NOT be exempt as they represent behavior changes.
"""

import sys
import tempfile
import subprocess
from pathlib import Path

def test_sh_under_evidence_store_requires_test_pairs():
    """A .sh file under docs/loom/evidence/ should NOT be exempt from test pairs."""

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

        # Create a .sh file under evidence store that DOESN'T match test naming pattern
        # This should NOT be exempt because it's not a test file
        sh_file = repo / "docs" / "loom" / "evidence" / "setup_test_env.sh"
        sh_file.write_text("#!/bin/bash\n\
# Sets up test environment - behavior change\n\
export TEST_DATA_DIR=/tmp/test_data\n\
mkdir -p $TEST_DATA_DIR\n\
echo \"Test environment ready\"\n")

        # Create plan that incorrectly claims this .sh file is exempt
        plan_content = f"""# Test plan
intent: {change_id}@abc1234
charter: 1.1

## Task DAG
**W0-01 Setup Script**  after: —  acceptance: 1
- Files: `docs/loom/evidence/setup_test_env.sh`
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
            print(f"VULNERABILITY CONFIRMED: .sh file under evidence store incorrectly exempted")
            return True
        else:
            if "intake.test-case-pair" in result.stderr:
                print(f"NO VULNERABILITY: .sh file under evidence store correctly requires test pair")
                return False
            else:
                print(f"UNEXPECTED ERROR: {result.stderr}")
                return False

if __name__ == "__main__":
    vulnerable = test_sh_under_evidence_store_requires_test_pairs()
    exit(1 if vulnerable else 0)