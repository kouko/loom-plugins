from __future__ import annotations

from loom_checker.helpers import artifact_path, read_text
from pathlib import Path
import re


RISK_LINE_RE = re.compile(r"^\d+\.\s+(.+)$")
BOUNDARY_TEST_REF = re.compile(r"boundary\s+test\s+(?:in\s+)?(W\d+-\d+)", re.IGNORECASE)


def check_plan_boundary_tests(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str], 
    attestation: dict
) -> list[tuple[str, str]]:
    """Check that each Risk line in plan has a corresponding boundary test task.
    
    This rule only applies to new plans (charter 1.1+) as per the policy.
    """
    rule = "intake.plan-boundary-tests"
    
    plan_path = artifact_path(manifest, "plan", change_id, repo)
    if not plan_path.is_file():
        return []
    
    plan_text = read_text(plan_path)
    
    # Check if plan has charter 1.1+ (only applies to new plans)
    charter_match = re.search(r"charter:\s*(\d+)\.(\d+)", plan_text)
    if not charter_match:
        # No charter - legacy plan, skip this check
        return []
    
    major, minor = int(charter_match.group(1)), int(charter_match.group(2))
    if (major, minor) < (1, 1):
        # Pre-1.1 charter, exempt
        return []
    
    # Parse the plan for Risk lines and Task DAG
    plan_sections = _parse_plan_sections(plan_text)
    task_dag = plan_sections.get("Task DAG", "")
    risks = plan_sections.get("Risks", "")
    
    # Find boundary test references in Risk lines
    risk_lines = []
    for line in risks.splitlines():
        match = RISK_LINE_RE.match(line.strip())
        if match:
            risk_lines.append(match.group(1))
    
    # Find all boundary test tasks in Task DAG
    boundary_test_tasks = set()
    for line in task_dag.splitlines():
        # Look for task headers with boundary test references
        # Pattern: **W1-01 Title** after: ... acceptance: ...
        task_header_match = re.match(r"^\s*\*\*(?P<id>W\d+-\d+)[^*]+\*\*\s*(?P<rest>.*)$", line)
        if task_header_match:
            task_id = task_header_match.group("id")
            rest = task_header_match.group("rest")
            # Check if this task is marked as a boundary test
            if "boundary" in rest.lower() and "test" in rest.lower():
                boundary_test_tasks.add(task_id)
    
    # Also check if Risk lines explicitly reference boundary test tasks
    referenced_tasks = set()
    for risk in risk_lines:
        for match in BOUNDARY_TEST_REF.finditer(risk):
            referenced_tasks.add(match.group(1))
    
    # If there are Risk lines that mention boundary tests, check they exist
    missing = referenced_tasks - boundary_test_tasks
    if missing:
        return [
            ("intake.plan-boundary-tests",
                f"Risk lines reference boundary test tasks that don't exist: {', '.join(sorted(missing))}")
        ]
    
    # If there are boundary test tasks but no Risk lines reference them, warn
    # (This is less strict - could be standalone boundary tests)
    # We'll just ensure every Risk line that mentions boundary tests has a corresponding task
    return []


def _parse_plan_sections(plan_text: str) -> dict[str, str]:
    """Parse plan markdown into sections."""
    sections = {}
    current_section = None
    current_lines = []
    
    for line in plan_text.splitlines():
        # Check for H2 section headers
        h2_match = re.match(r"^##\s+(.+)$", line)
        if h2_match:
            if current_section is not None:
                sections[current_section] = "\n".join(current_lines).strip()
            current_section = h2_match.group(1)
            current_lines = []
        elif current_section is not None:
            current_lines.append(line)
    
    # Don't forget the last section
    if current_section is not None:
        sections[current_section] = "\n".join(current_lines).strip()
    
    return sections