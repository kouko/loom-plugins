"""Validate the two published read-only checker observations."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from loom_checker.cli_advice import write_suggestion


HELP = """checked-readonly — validate read-only checker JSON
Usage: loom-python --repair --script checked_readonly.py contract --require <version>
       loom-python --ready --script checked_readonly.py reviewer-count <change-id>
Do not supply --json; this consumer adds it. Exact --help or -h runs no checker.
Validates schema version, command, required fields/types, request identity and
exit/status agreement; preserves compatible extra fields. Passed/blocked/error
JSON retains exits 0/1/2. Invalid results exit 2 with no stdout; startup exit 86
is preserved. The checker subprocess has a configured 30-second timeout.
The outer launcher owns readiness and repair. No writes, retries, text fallback
or change to checker policy, authorization or host trust is introduced.
Optional suggested_next is advisory: missing or unusable advice does not change
validation. Accepted JSON is preserved; advice grants no execution authority.
Local faults append Suggested next step: on stderr, generated locally.
"""


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "duplicate JSON key")
        result[key] = value
    return result


def _constant(value):
    raise ValueError("non-JSON numeric constant")


def _validate(raw, command, operands, code):
    value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant)
    _require(isinstance(value, dict), "expected one JSON object")
    _require(type(value.get("schema_version")) is int and value["schema_version"] == 1,
             "unsupported schema_version")
    _require(value.get("command") == command, "command mismatch")
    status = value.get("status")
    _require(status in ("passed", "blocked", "error"), "invalid status")
    _require(code == {"passed": 0, "blocked": 1, "error": 2}[status], "exit/status mismatch")
    diagnostics, notices = value.get("diagnostics"), value.get("notices")
    _require(isinstance(diagnostics, list), "invalid diagnostics")
    for item in diagnostics:
        _require(isinstance(item, dict) and isinstance(item.get("rule_id"), str)
                 and bool(item["rule_id"].strip()) and isinstance(item.get("message"), str),
                 "invalid diagnostic fields")
    _require(isinstance(notices, list) and all(isinstance(item, str) for item in notices),
             "invalid notices")
    _require("error" in value, "missing error")
    error, data = value["error"], value.get("data")
    _require(isinstance(data, dict), "invalid data")
    fields = (("contract_version", "required_version", "compatible") if command == "contract"
              else ("change_id", "reviewer_floor"))
    _require(all(key in data for key in fields), "missing command data")
    if status == "error":
        _require(not diagnostics and isinstance(error, dict)
                 and error.get("kind") in ("usage", "internal")
                 and isinstance(error.get("message"), str), "invalid error state")
        _require(all(data[key] is None for key in fields), "error contains domain data")
        return value
    _require(error is None and bool(diagnostics) == (status == "blocked"),
             "contradictory diagnostics/error state")
    if command == "contract":
        _require(all(isinstance(data[key], str) and data[key].strip() for key in fields[:2]),
                 "invalid contract versions")
        requirements = [operands[i + 1] for i, item in enumerate(operands[:-1]) if item == "--require"]
        _require(bool(requirements) and data["required_version"] == requirements[-1],
                 "required_version mismatch")
        _require(type(data["compatible"]) is bool and data["compatible"] == (status == "passed"),
                 "compatibility/status mismatch")
    else:
        _require(status == "passed" and operands and data["change_id"] == operands[0],
                 "reviewer request/status mismatch")
        _require(type(data["reviewer_floor"]) is int and data["reviewer_floor"] > 0,
                 "invalid reviewer_floor")
    return value


def main(argv=None, out=None, err=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    out, err = (sys.stdout if out is None else out), (sys.stderr if err is None else err)
    if argv in (["--help"], ["-h"]):
        out.write(HELP)
        return 0
    advice = "Inspect --help and correct the command input before deliberately rerunning."
    try:
        _require(argv and argv[0] in ("contract", "reviewer-count"),
                 "choose contract or reviewer-count; use --help")
        _require("--json" not in argv, "omit --json; the consumer adds it")
        advice = "Investigate the checker runtime and preserve outstanding work before deliberate re-execution; the outer launcher owns readiness and repair."
        child = subprocess.run([sys.executable, "-E", "-s", str(Path(__file__).with_name("loom_checker.py")),
                                *argv, "--json"], text=True, capture_output=True, timeout=30)
        if child.returncode == 86:
            err.write("checked-readonly: " + (child.stderr.strip() or "checker runtime unavailable") + "\n")
            write_suggestion(advice, err)
            return 86
        advice = "Investigate the checker output contract and original diagnostic; preserve outstanding work and do not act on unvalidated output."
        _require(not child.stderr, "unexpected checker stderr")
        _validate(child.stdout, argv[0], argv[1:], child.returncode)
    except subprocess.TimeoutExpired:
        err.write("checked-readonly: checker timed out after 30 seconds; investigate before rerunning\n")
        write_suggestion("Investigate the checker runtime and preserve outstanding work before deliberate re-execution.", err)
        return 2
    except (ValueError, OSError, UnicodeError, RecursionError) as exc:
        err.write(f"checked-readonly: {exc}\n")
        write_suggestion(advice, err)
        return 2
    out.write(child.stdout.strip() + "\n")
    return child.returncode


if __name__ == "__main__":
    raise SystemExit(main())
