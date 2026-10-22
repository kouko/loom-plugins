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

# The report template pins the Verdict cell to these four words; the
# attestation's vocabulary spells `not verified` with an underscore. Both
# spellings are accepted, case-insensitively, so a report that follows the
# template parses and anything else records as unreadable.
VERDICTS = {
    "works": "works",
    "partly": "partly",
    "not verified": "not_verified",
    "not_verified": "not_verified",
    "fails": "fails",
}


def _get_intent_acceptance_numbers(intent_sections: dict[str, str]) -> set[int]:
    """The Acceptance numbers the intent carries."""
    body = intent_sections.get("Acceptance", "")
    return {
        int(match.group(1))
        for line in body.splitlines()
        if (match := ACCEPTANCE_ITEM.match(line))
    }


def _report_rows(report_text: str) -> list[tuple[int, str]]:
    """(Acceptance number, raw Verdict cell) for each table data row.

    The Verdict cell is the fourth pipe-separated field of the template's
    `| # | asked | verdict | happened | re-run |` row -- the position the
    report template fixes, one shape that does not depend on the report's
    language. Counting rows rather than collecting them into a set is what
    lets the check see a duplicated line the set would collapse.
    """
    rows: list[tuple[int, str]] = []
    for line in report_text.splitlines():
        match = REPORT_ROW.match(line)
        if not match:
            continue
        cells = line.split("|")
        verdict = cells[3].strip() if len(cells) > 3 else ""
        rows.append((int(match.group(1)), verdict))
    return rows


def _normalise_verdict(cell: str) -> str | None:
    """The attestation status for a Verdict cell, or None when the cell is
    not one of the four words the report template pins."""
    key = " ".join(cell.lower().replace("_", " ").split())
    return VERDICTS.get(key)


def acceptance_coverage(
    intent_sections: dict[str, str], report_text: str,
) -> list[dict]:
    """The per-line coverage snapshot the attestation's `acceptance_status`
    field holds: one entry per intent Acceptance number, carrying the status
    the report's Verdict cell states. A row the report does not carry, or
    whose Verdict cell is unreadable, records `not_verified` -- the
    conservative status; the coverage check fails on the missing row and on
    the unreadable cell separately."""
    intent_numbers = sorted(_get_intent_acceptance_numbers(intent_sections))
    statuses: dict[int, str] = {}
    for number, cell in _report_rows(report_text):
        statuses[number] = _normalise_verdict(cell) or "not_verified"
    return [
        {"acceptance": number, "status": statuses.get(number, "not_verified")}
        for number in intent_numbers
    ]


def check_attestation_coverage(
    manifest, repo: Path, change_id: str, intent_sections: dict[str, str],
    attestation: dict,
) -> list[tuple[str, str]]:
    """Every intent Acceptance line has exactly one report row, and that row
    states a Verdict the template allows.

    The check is on the row identities and the Verdict vocabulary, not on
    whether acceptance passed: `not verified` and `fails` are legal row
    statuses and do not block here -- that judgement is the reviewer's and
    the user's, not this rule's.
    """
    rule = "intake.attestation-coverage"

    intent_numbers = _get_intent_acceptance_numbers(intent_sections)
    if not intent_numbers:
        return []

    report_path = artifact_path(manifest, "acceptance-test-report", change_id, repo)
    if not report_path.is_file():
        return [(rule, f"acceptance test report missing at {report_path.relative_to(repo)}")]

    rows = _report_rows(read_text(report_path))
    counts: dict[int, int] = {}
    for number, _cell in rows:
        counts[number] = counts.get(number, 0) + 1

    failures: list[tuple[str, str]] = []
    missing = sorted(intent_numbers - set(counts))
    if missing:
        failures.append((
            rule,
            "acceptance test report has no row for Acceptance lines: "
            f"{', '.join(map(str, missing))}",
        ))
    duplicate = sorted(number for number, count in counts.items() if count > 1)
    if duplicate:
        failures.append((
            rule,
            "acceptance test report carries duplicate rows for Acceptance "
            f"lines: {', '.join(map(str, duplicate))}",
        ))
    extra = sorted(set(counts) - intent_numbers)
    if extra:
        failures.append((
            rule,
            "acceptance test report carries rows for Acceptance lines the "
            f"intent does not have: {', '.join(map(str, extra))}",
        ))
    unreadable = sorted({
        number for number, cell in rows if _normalise_verdict(cell) is None
    })
    if unreadable:
        failures.append((
            rule,
            "acceptance test report states no Verdict in (works / partly / "
            "not verified / fails) for Acceptance lines: "
            f"{', '.join(map(str, unreadable))}",
        ))
    return failures
