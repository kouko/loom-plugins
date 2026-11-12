"""Bounded result rendering for the plan/intake JSON pilot."""
from __future__ import annotations

import json

from loom_checker.helpers import report


def new_result(command: str) -> dict:
    return {"schema_version": 1, "command": command, "status": "passed",
            "diagnostics": [], "notices": [], "error": None}


def report_result(failures: list[tuple[str, str]], err, result: dict | None) -> int:
    if result is None:
        return report(failures, err)
    result["status"] = "blocked" if failures else "passed"
    result["diagnostics"] = [{"rule_id": rule, "message": reason} for rule, reason in failures]
    return 1 if failures else 0


def error_result(result: dict, kind: str, message: str) -> None:
    result.update(status="error", diagnostics=[], error={"kind": kind, "message": message})


def write_result(result: dict, out) -> None:
    out.write(json.dumps(result, ensure_ascii=True) + "\n")
