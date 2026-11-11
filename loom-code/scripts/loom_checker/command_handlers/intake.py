from __future__ import annotations

from loom_checker.helpers import UsageError
from loom_checker.helpers import artifact_path
from loom_checker.helpers import load_manifest
from loom_checker.helpers import read_text
from loom_checker.helpers import repo_root
from loom_checker.helpers import report
from loom_checker.intent_state import CHANGE_ID
from loom_checker.intent_state import INTAKE_STATIONS
from loom_checker.parsing import parse_document
from loom_checker.rule_checks.intake import check_confirmed
from loom_checker.rule_checks.intake import check_confirmed_behavior
from loom_checker.rule_checks.intake import check_plan_field_caps_at
from loom_checker.rule_checks.intake import check_req_grammar
from loom_checker.rule_checks.intake import check_spec_ready
from loom_checker.rule_checks.intake import check_test_case_pairs
from loom_checker.rule_checks.intake import check_ui_flows_recompute
from loom_checker.rule_checks.intake import prose_lines
from loom_checker.rule_checks.intent import check_kind_recompute
from loom_checker.rule_checks.intent import touched_interface_surfaces
from loom_checker.rule_checks.plan_boundary_tests import check_plan_boundary_tests
from pathlib import Path
from io import StringIO
import json
import re
import sys


def cmd_intake(args: list[str], out=sys.stdout, err=sys.stderr) -> int:
    json_mode = "--json" in args
    if json_mode:
        args = args.copy()
        args.remove("--json")
    diagnostics = StringIO()
    try:
        station, change_id = _parse_args(args)
        failures, complete = _evaluate_intake(
            station, change_id,
            diagnostics if json_mode else out,
            diagnostics if json_mode else err,
        )
    except (UsageError, OSError) as exc:
        if not json_mode:
            raise
        payload = {
            "station": args[0] if args else None,
            "change_id": args[1] if len(args) > 1 else None,
            "state": "unconfirmed", "checks_complete": False,
            "failures": [], "diagnostics": diagnostics.getvalue(), "error": str(exc),
        }
        out.write(json.dumps(payload) + "\n")
        return 2
    if not json_mode:
        return report(failures, err)
    out.write(json.dumps({
        "station": station, "change_id": change_id,
        "state": "blocked" if failures else "passed", "checks_complete": complete,
        "failures": [{"rule": rule, "reason": reason} for rule, reason in failures],
        "diagnostics": diagnostics.getvalue(), "error": None,
    }) + "\n")
    return 1 if failures else 0


def _parse_args(args: list[str]) -> tuple[str, str]:
    if len(args) < 2:
        raise UsageError("intake needs a station and a change-id.")
    station, change_id = args[0], args[1]
    if not CHANGE_ID.fullmatch(change_id):
        raise UsageError(
            f"{change_id!r} is not a change-id; expected [A-Za-z0-9._-]+ "
            "(the id is spliced into a path, so nothing else is accepted)."
        )
    if len(args) > 2:
        raise UsageError(f"unexpected argument {args[2]!r}.")
    if station not in INTAKE_STATIONS:
        raise UsageError(
            f"unknown station {station!r}; intake covers {' and '.join(INTAKE_STATIONS)}."
        )
    return station, change_id


def _evaluate_intake(station: str, change_id: str, out, err) -> tuple[list[tuple[str, str]], bool]:
    manifest = load_manifest()
    repo = repo_root(Path.cwd())
    failures = check_confirmed(manifest, repo, change_id, station)
    if failures:
        return failures, False
    intent_path = artifact_path(manifest, "intent", change_id, repo)
    front, sections = parse_document(read_text(intent_path))
    skipped: set[str] = set()
    # Dated instruction records waive artifact dependencies only; they never
    # waive verification evidence.
    for artifact, section in (("intent", "Constraints"), ("plan", "Risks")):
        path = artifact_path(manifest, artifact, change_id, repo)
        if path.is_file():
            # Filter before parsing so example headings cannot become carriers.
            _, record_sections = parse_document("\n".join(prose_lines(read_text(path))))
            skipped.update(re.findall(
                r"^skipped-by-instruction: (spec|plan) \d{4}-\d{2}-\d{2}$",
                record_sections.get(section, ""), re.MULTILINE,
            ))

    failures: list[tuple[str, str]] = []
    if station == "write-plan" and "plan" not in skipped:
        failures += check_test_case_pairs(manifest, repo, change_id, sections)
        failures += check_plan_field_caps_at(manifest, repo, change_id)

    kind = front.get("kind", "").strip()
    needs_design = front.get("needs-design", "").strip().split()[:1]
    yes_at_write_plan = station == "write-plan" and needs_design == ["yes"] and "spec" not in skipped

    touched: list[str] = []
    if kind == "engineering" or yes_at_write_plan:
        touched = touched_interface_surfaces(repo, manifest, out)
    if kind == "engineering":
        failures += check_kind_recompute(touched)

    if "spec" not in skipped:
        failures += check_req_grammar(manifest, repo, change_id, sections)

    if yes_at_write_plan:
        failures += check_spec_ready(manifest, repo, change_id)
        failures += check_ui_flows_recompute(manifest, repo, change_id, touched)
    if station == "write-plan" and kind == "product" and "spec" not in skipped:
        # "A product spec needs confirmed-behavior before it becomes a plan"
        # does not depend on needs-design: under `no`, a carried-details list
        # forces a spec and write-plan runs decision point 2 on it. With no
        # spec there is nothing to confirm and the rule returns nothing.
        failures += check_confirmed_behavior(manifest, repo, change_id, err)
    
    # New evidence drift guard checks at write-plan intake
    if station == "write-plan" and "plan" not in skipped:
        # Planned task references must resolve; files may be written in Build.
        failures += check_plan_boundary_tests(
            manifest, repo, change_id, sections, {}, require_files=False,
        )
        # Note: attestation-based checks (coverage, commit-identity, intent-version)
        # are deferred to finalize-review since attestation doesn't exist at intake time

    return failures, True
