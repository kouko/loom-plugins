# concern: Malformed, contradictory, or wrong-request checker observations must not become usable results.
"""Exercise checked observations through the public entry and real producers."""
from __future__ import annotations

import copy
import io
import json
import runpy
import subprocess
import sys
from pathlib import Path

from test_loom_checker_cli import CHECKER, git, make_intent_state_repo, run_checker

CONSUMER = CHECKER.with_name("checked_readonly.py")


def test_real_observations_and_direct_parity(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    for floor in (2, 1):
        if floor == 1:
            (repo / "guide.md").write_text("Usage clarification.\n")
            git(repo, "add", "guide.md")
            git(repo, "commit", "-q", "-m", "clarify usage")
        for args in (("contract", "--require", "bad", "--require", " 2.00 "),
                     ("contract", "--require", "2.99"), ("contract",),
                     ("reviewer-count", " odd id ")):
            direct = run_checker(*args, "--json", cwd=repo)
            checked = subprocess.run([sys.executable, str(CONSUMER), *args], cwd=repo,
                                     text=True, capture_output=True)
            assert (checked.returncode, checked.stderr) == (direct.returncode, "")
            assert json.loads(checked.stdout) == json.loads(direct.stdout)
            if args[0] == "reviewer-count":
                assert json.loads(checked.stdout)["data"]["reviewer_floor"] == floor


def test_entry_validation_and_execution_boundary(monkeypatch) -> None:
    entry = runpy.run_path(str(CONSUMER), run_name="_checked_test")
    calls = []
    response = subprocess.CompletedProcess([], 0, "", "")
    def child(args, **kwargs):
        calls.append((args, kwargs))
        if isinstance(response, Exception):
            raise response
        return response
    monkeypatch.setattr(entry["subprocess"], "run", child)
    def invoke(args):
        out, err = io.StringIO(), io.StringIO()
        calls.clear()
        code = entry["main"](args, out, err)
        return code, out.getvalue(), err.getvalue()
    for args in (["--help"], ["-h"], [], ["plan"], ["contract", "--json"]):
        code, out, err = invoke(args)
        assert code == (0 if args in (["--help"], ["-h"]) else 2)
        assert not calls
        assert "30" in out if code == 0 else err.startswith("checked-readonly:")
    for command, operands, data in (
        ("contract", ["--require", "bad", "--require", " 2.00 "],
         {"contract_version": "2.3.1", "required_version": " 2.00 ", "compatible": True}),
        ("reviewer-count", [" odd id "], {"change_id": " odd id ", "reviewer_floor": 3}),
    ):
        payload = dict(schema_version=1, command=command, status="passed", diagnostics=[],
                       notices=["unchanged"], error=None, data=data, extra={"future": [1]})
        payload["data"]["extra"] = {"future": True}
        numeric_extra = json.dumps(payload).replace('"future": [1]', '"future": [1e999, 1.234567890123456789]')
        response = subprocess.CompletedProcess([], 0, " \n" + numeric_extra + " \n", "")
        assert invoke([command, *operands]) == (0, numeric_extra + "\n", "")
        accepted = [(0, payload)]
        error = copy.deepcopy(payload)
        error.update(status="error", error={"kind": "usage", "message": "bad", "extra": 1})
        error["data"] = {key: None for key in data if key != "extra"}
        accepted.append((2, error))
        if command == "contract":
            blocked = copy.deepcopy(payload)
            blocked.update(status="blocked", diagnostics=[{"rule_id": "contract.requires", "message": "no", "extra": 1}])
            blocked["data"]["compatible"] = False
            accepted.append((1, blocked))
        for code, value in accepted:
            response = subprocess.CompletedProcess([], code, json.dumps(value), "")
            actual, out, err = invoke([command, *operands])
            assert (actual, err, json.loads(out)) == (code, "", value)
            assert len(calls) == 1
            assert calls[0] == ([sys.executable, "-E", "-s", str(CHECKER), command, *operands, "--json"],
                                {"text": True, "capture_output": True, "timeout": 30})
            if code:
                broken = copy.deepcopy(value)
                if code == 2:
                    broken["data"][next(iter(data))] = "partial observation"
                else:
                    broken["diagnostics"][0]["rule_id"] = " "
                response = subprocess.CompletedProcess([], code, json.dumps(broken), "")
                actual, out, err = invoke([command, *operands])
                assert (actual, out) == (2, "") and err.startswith("checked-readonly:")
        invalid = ["", "[]", "{}", json.dumps(payload) + " {}",
                   json.dumps(payload).replace('"schema_version": 1', '"schema_version": 1, "schema_version": 1'),
                   json.dumps(payload).replace('"future": [1]', '"future": NaN'),
                   json.dumps(payload).replace('"future": true', '"future": true, "future": true')]
        mutations = [("schema_version", True), ("command", "plan"), ("status", "unknown"),
                     ("diagnostics", [{"rule_id": "x", "message": "no"}]), ("notices", [1]),
                     ("error", {}), ("data", []), ("diagnostics", ["bad"])]
        for key, value in mutations:
            changed = copy.deepcopy(payload)
            changed[key] = value
            invalid.append(json.dumps(changed))
        for key in payload:
            if key != "extra":
                changed = copy.deepcopy(payload)
                del changed[key]
                invalid.append(json.dumps(changed))
        for key in data:
            if key != "extra":
                for value in (None, " " if key == "contract_version" else "wrong", False):
                    changed = copy.deepcopy(payload)
                    changed["data"][key] = value
                    invalid.append(json.dumps(changed))
        for raw in invalid:
            response = subprocess.CompletedProcess([], 0, raw, "")
            code, out, err = invoke([command, *operands])
            assert (code, out) == (2, ""), raw
            assert err.startswith("checked-readonly:") and len(calls) == 1
        for response in (subprocess.CompletedProcess([], 1, json.dumps(payload), ""),
                         subprocess.CompletedProcess([], 0, json.dumps(payload), "warning"),
                         OSError("cannot start"), subprocess.TimeoutExpired("checker", 30)):
            code, out, err = invoke([command, *operands])
            assert (code, out) == (2, "") and err.startswith("checked-readonly:")
            assert len(calls) == 1
    response = subprocess.CompletedProcess([], 86, "", "runtime unavailable")
    assert invoke(["contract", "--require", "2.0"]) == (86, "", "checked-readonly: runtime unavailable\n")
