from __future__ import annotations

from loom_checker.helpers import artifact_path, git_maybe, read_text
from pathlib import Path, PurePosixPath
import re


RISK_LINE_RE = re.compile(r"^\d+\.\s+(.+)$")
BOUNDARY_TEST_REF = re.compile(r"(?:boundary|probe)\s+test\s+(?:in\s+)?(W\d+-\d+)", re.IGNORECASE)
PROGRAM_MARKER = re.compile(r"\b(?:boundary|probe)\s+test\b", re.IGNORECASE)


def _named_paths(line: str) -> set[str]:
    """Literal backticked file paths, optionally followed by a pytest node ID.

    Commands, task IDs, placeholders, directories and globs are not concrete
    filenames. Case is preserved so a misspelled extension cannot pass.
    """
    paths = set()
    for literal in re.findall(r"`([^`]+)`", line):
        name = literal.split("::", 1)[0]
        if (re.search(r"\s|[<>*?\[\]]", name) or name.endswith("/")
                or not re.search(r"[A-Za-z_]", name)
                or not ("/" in name or re.search(r"\.[A-Za-z]+$", name))):
            continue
        paths.add(name)
    return paths


def check_plan_boundary_tests(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str], 
    attestation: dict, *, require_files: bool = True, commit: str | None = None,
) -> list[tuple[str, str]]:
    """Check boundary-task references and concrete named test files.

    Planning intake sets require_files=False because implementation is still
    ahead. After Build, the default checks files too. A selected commit reads
    both the plan and its files from that tree, never from the checkout.
    Plans before charter 1.1 remain exempt.
    """
    rule = "intake.plan-boundary-tests"
    
    plan_path = artifact_path(manifest, "plan", change_id, repo)
    if commit is None:
        plan_text = read_text(plan_path) if plan_path.is_file() else None
    else:
        plan_text = git_maybe(repo, "show", f"{commit}:{plan_path.relative_to(repo).as_posix()}")
    if plan_text is None:
        return []
    
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
    named_files: set[str] = set()
    boundary_task = False
    for line in task_dag.splitlines():
        # Look for task headers with boundary test references
        # Pattern: **W1-01 Title** after: ... acceptance: ...
        task_header_match = re.match(r"^\s*\*\*(?P<id>W\d+-\d+)[^*]+\*\*\s*(?P<rest>.*)$", line)
        if task_header_match:
            task_id = task_header_match.group("id")
            # Check if this task is marked as a boundary test
            boundary_task = bool(PROGRAM_MARKER.search(line))
            if boundary_task:
                boundary_test_tasks.add(task_id)
        elif boundary_task and re.match(r"^\s*- (?:Files|Test):", line):
            named_files.update(_named_paths(line))
    
    # Also check if Risk lines explicitly reference boundary test tasks
    referenced_tasks = set()
    for risk in risk_lines:
        for match in BOUNDARY_TEST_REF.finditer(risk):
            referenced_tasks.add(match.group(1))
        if PROGRAM_MARKER.search(risk):
            named_files.update(_named_paths(risk))
    
    # If there are Risk lines that mention boundary tests, check they exist
    missing = referenced_tasks - boundary_test_tasks
    if missing:
        return [
            ("intake.plan-boundary-tests",
                f"Risk lines reference boundary test tasks that don't exist: {', '.join(sorted(missing))}")
        ]
    
    if require_files:
        # -t reports the committed object's type, so a tree is not a test file:
        # https://git-scm.com/docs/git-cat-file (verified 2026-11-02).
        missing_files = []
        for name in sorted(named_files):
            path = PurePosixPath(name)
            relative = not path.is_absolute() and ".." not in path.parts
            exists = relative and (
                (repo / name).is_file() if commit is None
                else git_maybe(repo, "cat-file", "-t", f"{commit}:{name}") == "blob"
            )
            if not exists:
                missing_files.append(name)
        if missing_files:
            return [(rule, "Named boundary/probe test files do not exist: "
                     + ", ".join(missing_files))]
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
