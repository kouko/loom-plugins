from __future__ import annotations

from loom_checker.helpers import artifact_path, is_real_date, read_text
from loom_checker.intent_state import STATUS
from loom_checker.parsing import LIST_ITEM
from pathlib import Path


def _get_intent_acceptance_numbers(intent_sections: dict[str, str]) -> set[int]:
    """Extract Acceptance line numbers from intent sections."""
    body = intent_sections.get("Acceptance", "")
    numbers = set()
    for line in body.splitlines():
        if (match := LIST_ITEM.match(line)):
            try:
                numbers.add(int(match.group(1)))
            except ValueError:
                pass
    return numbers


def _get_report_acceptance_rows(report_text: str) -> dict[int, str]:
    """Parse acceptance test report and return mapping of acceptance number to status."""
    # Parse the markdown table
    lines = report_text.splitlines()
    in_table = False
    header_found = False
    acceptance_map = {}
    
    for line in lines:
        if not in_table and "| # |" in line and "What you asked for" in line:
            in_table = True
            continue
        if in_table and "|---|" in line:
            header_found = True
            continue
        if in_table and header_found and line.strip().startswith("|"):
            # Parse table row
            parts = [part.strip() for part in line.strip("|").split("|")]
            if len(parts) >= 4:
                try:
                    acc_num = int(parts[0])
                    status = parts[2]  # Verdict column
                    if status in {"works", "partly", "not_verified", "fails"}:
                        acceptance_map[acc_num] = status
                except (ValueError, IndexError):
                    pass
        elif in_table and line.strip() and not line.strip().startswith("|"):
            # End of table
            break
            
    return acceptance_map


def check_attestation_coverage(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str], 
    attestation: dict
) -> list[tuple[str, str]]:
    """Check that acceptance test report covers all intent Acceptance lines."""
    rule = "intake.attestation-coverage"
    
    # Get intent acceptance numbers
    intent_numbers = _get_intent_acceptance_numbers(intent_sections)
    if not intent_numbers:
        # No acceptance lines in intent - nothing to check
        return []
    
    # Get attestation from the change directory if possible, otherwise check if it's in the manifest
    attestation_path = artifact_path(manifest, "attestation", change_id, repo)
    if not attestation_path.is_file():
        # Fallback: check if attestation is passed in (during finalize-review)
        # For now, we'll rely on the attestation parameter passed to this function
        pass
    
    # Parse the acceptance test report
    report_path = artifact_path(manifest, "acceptance-test-report", change_id, repo)
    if not report_path.is_file():
        # If no report exists, this is a failure unless acceptance-test was skipped
        # We'll check for skip via the attestation's selection or other means
        # For simplicity, we'll require the report to exist
        return [(rule, f"acceptance test report missing at {report_path.relative_to(repo)}")]
    
    report_text = read_text(report_path)
    report_rows = _get_report_acceptance_rows(report_text)
    
    # Check for missing or extra rows
    missing = sorted(intent_numbers - set(report_rows.keys()))
    extra = sorted(set(report_rows.keys()) - intent_numbers)
    
    if missing:
        return [(rule, f"acceptance test report missing rows for Acceptance lines: {', '.join(map(str, missing))}")]
    
    if extra:
        return [(rule, f"acceptance test report has extra rows for Acceptance lines: {', '.join(map(str, extra))}")]
    
    # Check that each row has a valid status (already done in parsing)
    # All good
    return []


def acceptance_count(intent_sections: dict[str, str]) -> int:
    """How many things the user said "done means this" about."""
    body = intent_sections.get("Acceptance", "")
    return sum(1 for line in body.splitlines() if LIST_ITEM.match(line))