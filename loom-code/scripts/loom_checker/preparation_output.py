"""Bounded result rendering for preparation and read-only JSON pilots."""
from __future__ import annotations

import json

from loom_checker.helpers import report


def new_result(command: str) -> dict:
    result = {"schema_version": 1, "command": command, "status": "passed",
              "diagnostics": [], "notices": [], "error": None}
    if command == "contract":
        result["data"] = dict(contract_version=None, required_version=None, compatible=None)
    elif command == "reviewer-count":
        result["data"] = dict(change_id=None, reviewer_floor=None)
    return result


def report_result(failures: list[tuple[str, str]], err, result: dict | None) -> int:
    if result is None:
        return report(failures, err)
    result["status"] = "blocked" if failures else "passed"
    result["diagnostics"] = [{"rule_id": rule, "message": reason} for rule, reason in failures]
    return 1 if failures else 0


def error_result(result: dict, kind: str, message: str) -> None:
    result.update(status="error", diagnostics=[], error={"kind": kind, "message": message})
    if "data" in result:
        result["data"] = dict.fromkeys(result["data"])


def write_result(result: dict, out) -> None:
    out.write(json.dumps(result, ensure_ascii=True) + "\n")
