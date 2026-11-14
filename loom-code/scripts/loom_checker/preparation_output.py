"""Bounded result rendering for preparation and read-only JSON pilots."""
from __future__ import annotations

import json

from loom_checker.helpers import report


def suggested_next(command: str, category: str) -> str | None:
    if command not in {"contract", "reviewer-count"} or category == "passed":
        return None
    if category == "blocked":
        return "Update the plugin identified by the contract diagnostic, then recheck supported requirements."
    if category == "usage":
        if command == "reviewer-count":
            return "Inspect the diagnostic and command help; select the intended repository, preserve outstanding work and establish a clean completed change before deliberately rerunning."
        return "Inspect the reported operand or manifest issue and command help; correct it before deliberately rerunning."
    return "Investigate the reported failure and preserve outstanding work; no reliable repair is known."


def new_result(command: str) -> dict:
    result = {"schema_version": 1, "command": command, "status": "passed",
              "diagnostics": [], "notices": [], "error": None}
    if command == "contract":
        result["data"] = dict(contract_version=None, required_version=None, compatible=None)
    elif command == "reviewer-count":
        result["data"] = dict(change_id=None, reviewer_floor=None)
    if "data" in result:
        result["suggested_next"] = None
    return result


def report_result(failures: list[tuple[str, str]], err, result: dict | None) -> int:
    if result is None:
        return report(failures, err)
    result["status"] = "blocked" if failures else "passed"
    result["diagnostics"] = [{"rule_id": rule, "message": reason} for rule, reason in failures]
    if "suggested_next" in result:
        result["suggested_next"] = suggested_next(result["command"], result["status"])
    return 1 if failures else 0


def error_result(result: dict, kind: str, message: str) -> None:
    result.update(status="error", diagnostics=[], error={"kind": kind, "message": message})
    if "data" in result:
        result["data"] = dict.fromkeys(result["data"])
        result["suggested_next"] = suggested_next(result["command"], kind)


def write_result(result: dict, out) -> None:
    out.write(json.dumps(result, ensure_ascii=True) + "\n")
