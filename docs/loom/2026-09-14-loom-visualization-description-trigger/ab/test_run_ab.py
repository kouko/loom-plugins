"""Focused tests for run_ab.py's pure parts: decision rule, hash, parsing, argv."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent))
import run_ab  # noqa: E402


def test_decision_rule_ships_only_on_strictly_greater() -> None:
    assert run_ab.decide(a_count=3, b_count=4) == "SHIP"
    assert run_ab.decide(a_count=4, b_count=4) == "HOLD"
    assert run_ab.decide(a_count=5, b_count=4) == "HOLD"


def test_candidate_hash_recorded_and_mismatch_detected() -> None:
    assert run_ab.sha256_text(run_ab.DESCRIPTION_B) == run_ab.DESCRIPTION_B_SHA256
    run_ab.check_hash(run_ab.DESCRIPTION_B)
    with pytest.raises(ValueError):
        run_ab.check_hash(run_ab.DESCRIPTION_B + " ")


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


def test_argv_loads_three_variant_plugins_without_bare() -> None:
    argv = run_ab.build_argv("hi", Path("/v/B"), '{"enabledPlugins": {}}')
    assert argv[:3] == ["claude", "-p", "hi"]
    assert [argv[i + 1] for i, a in enumerate(argv) if a == "--plugin-dir"] == [
        "/v/B/loom-code", "/v/B/loom-design", "/v/B/loom-workflow"]
    assert "--bare" not in argv
    assert argv[argv.index("--output-format") + 1] == "stream-json" and "--verbose" in argv


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
