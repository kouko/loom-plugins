from __future__ import annotations

from loom_checker.helpers import artifact_path, read_text
from pathlib import Path
import re


# The intent's Acceptance list: `1. ...`, `2) ...` at line start.
ACCEPTANCE_ITEM = re.compile(r"^\s*(\d+)[.)]\s+\S")

# A report table data row, matched by its FIRST cell only. The header row and
# the `|---|` separator do not start with `| <digits> |`, and the verdict /
# "what happened" cells are written in the user's language, so the first cell
# is the one shape that does not depend on the report's language.
REPORT_ROW = re.compile(r"^\s*\|\s*(\d+)\s*\|")


def _get_intent_acceptance_numbers(intent_sections: dict[str, str]) -> set[int]:
    """The Acceptance numbers the intent carries."""
    body = intent_sections.get("Acceptance", "")
    return {
        int(match.group(1))
        for line in body.splitlines()
        if (match := ACCEPTANCE_ITEM.match(line))
    }


def _get_report_acceptance_numbers(report_text: str) -> set[int]:
    """The Acceptance numbers the report's table carries."""
    numbers: set[int] = set()
    for line in report_text.splitlines():
        match = REPORT_ROW.match(line)
        if match:
            numbers.add(int(match.group(1)))
    return numbers


def check_attestation_coverage(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str],
    attestation: dict,
) -> list[tuple[str, str]]:
    """Every intent Acceptance line has one row in the acceptance test report.

    The check is on the row identities, not the verdict cells: a complete
    report is one guarantee, acceptance passing is another. ``not_verified``
    is a legal row status and does not count as passing -- that judgement is
    the reviewer's, not this rule's.
    """
    rule = "intake.attestation-coverage"

    intent_numbers = _get_intent_acceptance_numbers(intent_sections)
    if not intent_numbers:
        return []

    report_path = artifact_path(manifest, "acceptance-test-report", change_id, repo)
    if not report_path.is_file():
        return [(rule, f"acceptance test report missing at {report_path.relative_to(repo)}")]

    report_numbers = _get_report_acceptance_numbers(read_text(report_path))
    failures: list[tuple[str, str]] = []
    missing = sorted(intent_numbers - report_numbers)
    extra = sorted(report_numbers - intent_numbers)
    if missing:
        failures.append((
            rule,
            "acceptance test report has no row for Acceptance lines: "
            f"{', '.join(map(str, missing))}",
        ))
    if extra:
        failures.append((
            rule,
            "acceptance test report carries rows for Acceptance lines the "
            f"intent does not have: {', '.join(map(str, extra))}",
        ))
    return failures