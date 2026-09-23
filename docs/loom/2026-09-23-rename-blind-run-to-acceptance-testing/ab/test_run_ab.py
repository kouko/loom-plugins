"""Focused tests for run_ab.py's pure parts: decision rule, hash, parsing, argv."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_ab  # noqa: E402


def test_decision_rule_keeps_b_when_its_valid_rate_is_at_least_a() -> None:
    assert run_ab.decide(a_inv=17, a_valid=18, b_inv=17, b_valid=18) == "KEEP B"
    assert run_ab.decide(a_inv=17, a_valid=18, b_inv=18, b_valid=18) == "KEEP B"
    assert run_ab.decide(a_inv=18, a_valid=18, b_inv=17, b_valid=18) == "STOP"
    # rates, not counts: 16/16 beats 17/18 even though 16 < 17
    assert run_ab.decide(a_inv=17, a_valid=18, b_inv=16, b_valid=16) == "KEEP B"
    assert run_ab.decide(a_inv=16, a_valid=16, b_inv=17, b_valid=18) == "STOP"


def test_decision_rule_error_or_empty_variant_is_incomplete() -> None:
    assert run_ab.decide(a_inv=3, a_valid=4, b_inv=4, b_valid=4, errors=1) == "INCOMPLETE"
    assert run_ab.decide(a_inv=0, a_valid=0, b_inv=4, b_valid=4) == "INCOMPLETE"
    assert run_ab.decide(a_inv=4, a_valid=4, b_inv=0, b_valid=0) == "INCOMPLETE"


def _init(skills=("loom-workflow:loom-visualization",), source="loom-workflow@inline") -> dict:
    return {"type": "system", "subtype": "init", "skills": list(skills),
            "plugins": [{"name": "loom-workflow", "source": source}]}


def test_report_error_session_not_counted_and_not_ship(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(run_ab, "EVIDENCE", tmp_path / "evidence")
    monkeypatch.setattr(run_ab, "CHANGE_DIR", tmp_path)
    monkeypatch.setattr(run_ab, "RESULTS", tmp_path / "results.md")
    final = json.dumps({"type": "result", "result": "prose"})
    ids = [pid for pid, _ in run_ab.prompts()]
    for variant in ("A", "B"):
        (tmp_path / "evidence" / f"ab-{variant}").mkdir(parents=True)
        for pid in ids:
            (tmp_path / "evidence" / f"ab-{variant}" / f"{pid}-run1.jsonl").write_text(
                json.dumps(_init()) + "\n" + final + "\n")
    (tmp_path / "evidence/ab-B" / f"{ids[0]}-run1.jsonl").write_text("\n".join([
        json.dumps(_init()),
        json.dumps(_tool("Skill", {"skill": "loom-visualization"})),
        json.dumps({"type": "result", "is_error": True, "api_error_status": 429, "result": "limit"}),
    ]) + "\n")
    run_ab.report(runs=1)
    text = (tmp_path / "results.md").read_text(encoding="utf-8")
    assert "**INCOMPLETE**" in text and "**KEEP B**" not in text
    assert "| B | 8 | 0 |" in text  # the errored session is neither valid nor counted


def test_report_excludes_and_counts_runs_where_the_skill_did_not_load(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(run_ab, "EVIDENCE", tmp_path / "evidence")
    monkeypatch.setattr(run_ab, "CHANGE_DIR", tmp_path)
    monkeypatch.setattr(run_ab, "RESULTS", tmp_path / "results.md")
    invoked = "\n".join([json.dumps(_init()),
                         json.dumps(_tool("Skill", {"skill": "loom-visualization"})),
                         json.dumps({"type": "result", "result": "prose"})]) + "\n"
    ids = [pid for pid, _ in run_ab.prompts()]
    for variant in ("A", "B"):
        (tmp_path / "evidence" / f"ab-{variant}").mkdir(parents=True)
        for pid in ids:
            (tmp_path / "evidence" / f"ab-{variant}" / f"{pid}-run1.jsonl").write_text(invoked)
    # B's first run never loaded the skill: invalid, not a failure
    (tmp_path / "evidence/ab-B" / f"{ids[0]}-run1.jsonl").write_text("\n".join([
        json.dumps(_init(skills=())), json.dumps({"type": "result", "result": "prose"})]) + "\n")
    run_ab.report(runs=1)
    text = (tmp_path / "results.md").read_text(encoding="utf-8")
    assert "| A | 9 | 9 | 100% | 0 |" in text
    assert "| B | 8 | 8 | 100% | 1 |" in text
    assert "**KEEP B**" in text


def test_parse_loaded_requires_the_inline_plugin_skill_in_init() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        final = {"type": "result", "result": "ok"}
        assert run_ab.parse_stream(_stream(tmp, [_init(), final]))["loaded"] is True
        assert run_ab.parse_stream(_stream(tmp, [_init(skills=()), final]))["loaded"] is False
        installed = _init(source="loom-workflow@loom")  # the installed copy, not the variant's
        assert run_ab.parse_stream(_stream(tmp, [installed, final]))["loaded"] is False
        assert run_ab.parse_stream(_stream(tmp, [final]))["loaded"] is False


def test_parse_undecodable_nonempty_line_marks_error() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        path = tmp / "s.jsonl"
        final = json.dumps({"type": "result", "result": "ok"})
        path.write_text('{"type": "assist\n' + final + "\n", encoding="utf-8")
        assert run_ab.parse_stream(path)["error"] is True
        path.write_text("\n   \n" + final + "\n", encoding="utf-8")
        assert run_ab.parse_stream(path)["error"] is False  # blank lines are not corrupt


def test_scratch_default_is_under_system_temp_not_a_session_path() -> None:
    assert run_ab.scratch_dir({}) == Path(tempfile.gettempdir()) / "loom-ab-rename"
    assert run_ab.scratch_dir({"AB_SCRATCH": "/x/y"}) == Path("/x/y")
    assert "claude-501" not in run_ab.Path(run_ab.__file__).read_text(encoding="utf-8")


def test_candidate_hash_recorded_and_mismatch_detected() -> None:
    assert run_ab.sha256_text(run_ab.DESCRIPTION_B) == run_ab.DESCRIPTION_B_SHA256
    run_ab.check_hash(run_ab.DESCRIPTION_B)
    with pytest.raises(ValueError):
        run_ab.check_hash(run_ab.DESCRIPTION_B + " ")


def test_variants_differ_only_in_the_renamed_phrase() -> None:
    assert "blind-run results" in run_ab.DESCRIPTION_A
    assert run_ab.DESCRIPTION_B == run_ab.DESCRIPTION_A.replace(
        "blind-run results", "acceptance test results")


def _stream(tmp: Path, events: list[dict]) -> Path:
    path = tmp / "s.jsonl"
    path.write_text("\n".join(json.dumps(e) for e in events) + "\n", encoding="utf-8")
    return path


def _tool(name: str, inp: dict) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": name, "input": inp}]}}


def test_parse_counts_prefixed_and_bare_skill_names_only() -> None:
    with tempfile.TemporaryDirectory() as d:
        tmp = Path(d)
        final = {"type": "result", "result": "| a | b |\n|---|---|\n| 1 | 2 |"}
        for skill in ("loom-workflow:loom-visualization", "loom-visualization"):
            got = run_ab.parse_stream(_stream(tmp, [_tool("Skill", {"skill": skill}), final]))
            assert got["invoked"] is True and got["table"] is True
        other = run_ab.parse_stream(_stream(tmp, [
            _tool("Skill", {"skill": "loom-design:capture-intent"}),
            _tool("Bash", {"command": "echo loom-visualization"}),
            {"type": "result", "result": "┌──┐\n│x │\n└──┘"},
        ]))
        assert other["invoked"] is False and other["table"] is False and other["diagram"] is True
        assert other["error"] is False
        limited = run_ab.parse_stream(_stream(tmp, [{
            "type": "result", "is_error": True, "api_error_status": 429,
            "result": "You've hit your session limit"}]))
        assert limited["error"] is True  # a rate-limited session is not a measured session


def test_argv_loads_three_variant_plugins_isolated_with_slash_commands_on() -> None:
    argv = run_ab.build_argv("hi", Path("/v/B"), '{"enabledPlugins": {}}')
    assert argv[:3] == ["claude", "-p", "hi"]
    assert [argv[i + 1] for i, a in enumerate(argv) if a == "--plugin-dir"] == [
        "/v/B/loom-code", "/v/B/loom-design", "/v/B/loom-workflow"]
    assert "--bare" not in argv
    assert argv[argv.index("--output-format") + 1] == "stream-json" and "--verbose" in argv
    assert argv[argv.index("--setting-sources") + 1] == "project"
    assert "--strict-mcp-config" in argv
    assert "--disable-slash-commands" not in argv  # it would also disable skills


def test_trial_env_disables_claude_mds_and_drops_nesting_marker() -> None:
    env = run_ab.trial_env({"CLAUDECODE": "1", "PATH": "/bin"})
    assert env == {"PATH": "/bin", "CLAUDE_CODE_DISABLE_CLAUDE_MDS": "1"}


def test_pending_jobs_skips_complete_streams_and_caps_count() -> None:
    with tempfile.TemporaryDirectory() as d:
        ev = Path(d)
        (ev / "ab-A").mkdir()
        (ev / "ab-A/p1-run1.jsonl").write_text(json.dumps({"type": "result", "result": "ok"}) + "\n")
        (ev / "ab-B").mkdir()
        (ev / "ab-B/p1-run1.jsonl").write_text("{}\n")  # interrupted: no result event
        jobs = [(v, pid, "t", 1) for pid in ("p1", "p2") for v in ("A", "B")]
        assert run_ab.pending_jobs(jobs, ev, limit=None) == jobs[1:]
        assert run_ab.pending_jobs(jobs, ev, limit=2) == jobs[1:3]


def test_disabled_plugins_settings_turns_every_key_off() -> None:
    settings = json.loads(run_ab.disabled_plugins_settings(
        {"enabledPlugins": {"x@m": True, "loom-code@loom": True}, "apiKeyHelper": "secret"}))
    assert settings == {"enabledPlugins": {"x@m": False, "loom-code@loom": False}}


def test_copies_differing_beyond_description_are_rejected() -> None:
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d, "A"), Path(d, "B")
        for root in (a, b):
            (root / "loom-workflow/skills/loom-visualization").mkdir(parents=True)
            (root / "loom-code").mkdir()
            (root / "loom-code/x.md").write_text("same\n", encoding="utf-8")
        skill = "---\nname: loom-visualization\ndescription: |\n  {}\n---\nbody\n"
        rel = run_ab.SKILL_REL
        (a / rel).write_text(skill.format(run_ab.DESCRIPTION_A), encoding="utf-8")
        (b / rel).write_text(skill.format(run_ab.DESCRIPTION_B), encoding="utf-8")
        run_ab.verify_copies(a, b)
        (a / "loom-code/__pycache__").mkdir()
        (a / "loom-code/__pycache__/hook.cpython-312.pyc").write_bytes(b"\0")
        (b / "loom-code/stray.pyc").write_bytes(b"\0")
        run_ab.verify_copies(a, b)  # hook bytecode from a session is not a copy difference
        (b / "loom-code/x.md").write_text("changed\n", encoding="utf-8")
        with pytest.raises(ValueError):
            run_ab.verify_copies(a, b)
