"""Public-entry checks for optional preparation JSON and legacy parity."""
# concern: JSON result contamination, selector ambiguity and exception notice loss.
from __future__ import annotations

import io
import json
import runpy
from pathlib import Path

from test_loom_checker_cli import CHECKER, make_intent_state_repo, run_checker


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
        assert set(payload) == {"schema_version", "command", "status", "diagnostics", "notices", "error"}
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
    assert set(json.loads(result.stdout)) == {"state", "reason", "next", "evidence", "complete"}
