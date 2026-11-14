"""Public-entry checks for optional preparation JSON and legacy parity."""
# concern: JSON result contamination, selector ambiguity and exception notice loss.
# concern: Read-only JSON must reject malformed operands before domain reads and clear partial data on failure.
from __future__ import annotations

import io
import json
import runpy
from pathlib import Path

from test_loom_checker_cli import CHECKER, git, make_intent_state_repo, run_checker


def test_readonly_json_typed_observations_and_text_parity(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    for required, compatible in (("2.0", True), (" 2.00 ", True), ("02.0", False), ("2.99", False)):
        args = ("contract", "--require", "bad", "--require", required)
        text = run_checker(*args, cwd=tmp_path)
        result = run_checker(*args, "--json", cwd=tmp_path)
        payload = json.loads(result.stdout)
        assert result.returncode == text.returncode == (0 if compatible else 1)
        assert result.stderr == "" and result.stdout.endswith("\n")
        assert set(payload) == {"schema_version", "command", "status", "diagnostics", "notices", "error", "data", "suggested_next"}
        assert payload["suggested_next"] is None if compatible else payload["suggested_next"].strip()
        if not compatible:
            assert f"Suggested next step: {payload['suggested_next']}\n" in text.stderr
        assert payload["schema_version"] == 1 and payload["command"] == "contract"
        assert payload["data"] == {"contract_version": "2.3.1", "required_version": required, "compatible": compatible}
        assert payload["status"] == ("passed" if compatible else "blocked")
        assert payload["error"] is None and payload["notices"] == []
        assert bool(payload["diagnostics"]) is not compatible
        for diagnostic in payload["diagnostics"]:
            assert f"BLOCK {diagnostic['rule_id']}: {diagnostic['message']}\n" in text.stderr
    for floor in (2, 1):
        if floor == 1:
            (repo / "guide.md").write_text("Usage clarification.\n")
            git(repo, "add", "guide.md")
            git(repo, "commit", "-q", "-m", "clarify usage")
        result = run_checker("reviewer-count", " odd id ", "--json", cwd=repo)
        payload = json.loads(result.stdout)
        assert (result.returncode, result.stderr) == (0, "")
        assert payload["data"] == {"change_id": " odd id ", "reviewer_floor": floor}
        assert type(payload["data"]["reviewer_floor"]) is int
        assert payload["status"] == "passed" and payload["diagnostics"] == []
        assert payload["notices"] == [] and payload["error"] is None
        assert payload["suggested_next"] is None
        assert run_checker("reviewer-count", " odd id ", cwd=repo).stdout == f"{floor}\n"


def test_readonly_json_usage_and_selectors_before_domain_work(tmp_path: Path, monkeypatch) -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_readonly_entry")
    import loom_checker.command_handlers.contract as contract
    import loom_checker.command_handlers.reviewer_count as reviewer
    def forbidden(*args, **kwargs):
        raise AssertionError("invalid arguments performed domain work")
    monkeypatch.setattr(contract, "load_manifest", forbidden)
    monkeypatch.setattr(reviewer, "repo_root", forbidden)
    for command, operands in (("contract", ()), ("contract", ("--require",)),
                              ("contract", ("--require", "bad")), ("reviewer-count", ()),
                              ("reviewer-count", (" ",)), ("reviewer-count", ("id", "extra"))):
        for args in (operands, ("--help",), ("-h",), ("--json",)):
            out, err = io.StringIO(), io.StringIO()
            assert entry["main"]([command, *args, "--json"], out, err) == 2
            payload = json.loads(out.getvalue())
            assert err.getvalue() == "" and out.getvalue().endswith("\n")
            assert payload["status"] == "error" and payload["error"]["kind"] == "usage"
            assert "help" in payload["suggested_next"]
            assert payload["diagnostics"] == [] and all(value is None for value in payload["data"].values())


def test_readonly_json_repository_errors_and_late_failure_cleanup(tmp_path: Path, monkeypatch) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    (repo / "dirty").touch()
    for cwd in (tmp_path, repo):
        result = run_checker("reviewer-count", "id", "--json", cwd=cwd)
        payload = json.loads(result.stdout)
        assert (result.returncode, result.stderr) == (2, "")
        assert payload["error"]["kind"] == "usage" and payload["data"] == {"change_id": None, "reviewer_floor": None}
        assert "preserve" in payload["suggested_next"] and "repository" in payload["suggested_next"]
    entry = runpy.run_path(str(CHECKER), run_name="_readonly_entry")
    from loom_checker.helpers import UsageError
    for command, data in (("contract", {"contract_version": "2.0", "required_version": "2.0", "compatible": True}),
                          ("reviewer-count", {"change_id": "id", "reviewer_floor": 1})):
        for exception, kind in ((RuntimeError("late"), "internal"), (UsageError("late"), "usage")):
            calls = []
            def crash(args, out, err, *, result):
                calls.append(args)
                result["data"].update(data)
                out.write("partial stdout\n")
                err.write("partial stderr\n")
                raise exception
            monkeypatch.setitem(entry["COMMANDS"], command, crash)
            out, err = io.StringIO(), io.StringIO()
            assert entry["main"]([command, "operand", "--json"], out, err) == 2
            payload = json.loads(out.getvalue())
            assert calls == [["operand"]] and err.getvalue() == ""
            assert payload["error"]["kind"] == kind and payload["diagnostics"] == []
            assert ("Investigate" if kind == "internal" else "help") in payload["suggested_next"]
            assert all(value is None for value in payload["data"].values())


def test_preparation_json_passes_and_preserves_real_notices(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    plan = tmp_path / "plan.md"
    plan.write_text("")
    for args in (("plan", str(plan)), ("intake", "write-plan", "2026-09-09-example")):
        text = run_checker(*args, cwd=repo)
        result = run_checker(*args, "--json", cwd=repo)
        assert result.returncode == text.returncode == 0
        assert result.stderr == "" and result.stdout.endswith("\n")
        payload = json.loads(result.stdout)
        assert set(payload) == {"schema_version", "command", "status", "diagnostics", "notices", "error", "suggested_next"}
        assert payload["suggested_next"] is None
        assert payload["schema_version"] == 1 and payload["command"] == args[0]
        assert payload["status"] == "passed" and payload["diagnostics"] == [] and payload["error"] is None
        assert payload["notices"] == text.stdout.splitlines()
        assert text.stderr == ""


def test_preparation_json_blockers_usage_and_selector_boundaries(tmp_path: Path) -> None:
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    plan = repo / "docs/loom/2026-09-09-example/plan.md"
    plan.parent.mkdir(parents=True)
    plan.write_text("charter: 1.1\n")
    for args in (("plan", str(plan)), ("intake", "write-plan", "2026-09-09-example")):
        text = run_checker(*args, cwd=repo)
        result = run_checker(*args, "--json", cwd=repo)
        payload = json.loads(result.stdout)
        assert result.returncode == text.returncode == 1 and result.stderr == ""
        assert payload["status"] == "blocked" and payload["error"] is None
        assert payload["suggested_next"].strip()
        assert f"Suggested next step: {payload['suggested_next']}\n" in text.stderr
        assert payload["diagnostics"]
        for diagnostic in payload["diagnostics"]:
            assert f"BLOCK {diagnostic['rule_id']}: {diagnostic['message']}\n" in text.stderr
        assert payload["notices"] == text.stdout.splitlines()
    for args in (("plan",), ("plan", str(tmp_path / "absent")), ("intake",),
                 ("intake", "bad-station", "valid-id"), ("plan", "--json"),
                 ("intake", "write-plan", "id", "extra")):
        result = run_checker(*args, "--json", cwd=repo)
        payload = json.loads(result.stdout)
        assert result.returncode == 2 and result.stderr == ""
        assert payload["status"] == "error" and payload["error"]["kind"] == "usage"
        assert payload["suggested_next"].strip()
        if args != ("plan", "--json"):
            text = run_checker(*args, cwd=repo)
            assert f"Suggested next step: {payload['suggested_next']}\n" in text.stderr
        assert payload["diagnostics"] == []
    literal = repo / "--json"
    literal.write_text("")
    assert run_checker("plan", "./--json", "--json", cwd=repo).returncode == 0
    assert run_checker("plan", "--help", cwd=repo).stdout.startswith("plan —")
    assert "help only" not in run_checker("plan", "--help", "--json", cwd=repo).stdout


def test_preparation_json_checks_once_and_keeps_notices_on_internal_error(tmp_path: Path, monkeypatch) -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_json_entry")
    import loom_checker.command_handlers.intake as intake
    repo, _ = make_intent_state_repo(tmp_path, delivered=False)
    monkeypatch.chdir(repo)
    calls = []
    def crash(*args, **kwargs):
        calls.append(1)
        raise RuntimeError("after notice")
    monkeypatch.setattr(intake, "check_kind_recompute", crash)
    out, err = io.StringIO(), io.StringIO()
    assert entry["main"](["intake", "write-spec", "2026-09-09-example", "--json"], out, err) == 2
    payload = json.loads(out.getvalue())
    assert calls == [1] and err.getvalue() == ""
    assert payload["status"] == "error" and payload["diagnostics"] == []
    assert payload["notices"][0].startswith("interface-surfaces (")
    assert payload["error"] == {"kind": "internal", "message": "loom_checker internal error: RuntimeError: after notice"}
    assert "no reliable repair is known" in payload["suggested_next"]


def test_preparation_text_errors_hooks_and_other_commands_stay_unchanged(tmp_path: Path, monkeypatch) -> None:
    entry = runpy.run_path(str(CHECKER), run_name="_json_entry")
    for command in ("plan", "intake"):
        out, err = io.StringIO(), io.StringIO()
        assert entry["main"]([command], out, err) == 2
        assert out.getvalue() == "" and err.getvalue().count("Help:") == 1
    def hook_crash(args, out, err):
        raise RuntimeError("hook fixture")
    monkeypatch.setitem(entry["COMMANDS"], "push", hook_crash)
    out, err = io.StringIO(), io.StringIO()
    assert entry["main"](["push", "--hook"], out, err) == 0
    assert "allowing" in err.getvalue()
    result = run_checker("delivery", "--goal", "local", "--json", cwd=tmp_path)
    payload = json.loads(result.stdout)
    assert set(payload) == {"state", "reason", "next", "evidence", "complete", "suggested_next"}
    assert payload["suggested_next"] == payload["next"]
    assert "Suggested next step:" not in result.stderr
