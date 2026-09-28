"""Adversarial probes for the loom-visualization description A/B runner.

Targets: the A/B runner's stream parser and decision rule (ab/run_ab.py). The
runner imports the description renderer from
tests/test_loom_skill_description_catalog.py, so the fixture puts that folder
on the import path.

The probes are ordinary tests: each asserts the behaviour that should hold, and
a passing probe records an attack the change survived. The probes skip when
docs/ is absent.
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[3]
CHANGE_DIR = REPO_ROOT / "docs/loom/2026-09-14-loom-visualization-description-trigger"
RUN_AB = CHANGE_DIR / "ab/run_ab.py"
CATALOG = REPO_ROOT / "tests/test_loom_skill_description_catalog.py"


def _load(name: str, path: Path):
    if not path.exists():
        pytest.skip(f"{path} is absent")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def run_ab():
    # run_ab.py imports the catalog renderer by bare name from the folder it
    # was written beside; the catalog test now lives in the root tests/ folder.
    sys.path.insert(0, str(CATALOG.parent))
    return _load("adversarial_run_ab", RUN_AB)


def _tool(name: str, inp: object) -> dict:
    return {"type": "assistant", "message": {"content": [
        {"type": "tool_use", "name": name, "input": inp}]}}


FINAL = {"type": "result", "result": "plain prose answer"}


def _write(path: Path, lines: list[str]) -> Path:
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


# --- parser ---------------------------------------------------------------


def test_parse_stream_near_miss_skill_names_not_counted(run_ab, tmp_path: Path) -> None:
    """A Skill call naming a look-alike skill, or prose that mentions it, is not an invocation."""
    events = [
        _tool("Skill", {"skill": "loom-visualization-extra"}),
        _tool("Skill", {"skill": "Loom-Visualization"}),
        _tool("Skill", {"skill": " loom-visualization"}),
        _tool("Skill", {"skill": "other:loom-visualization"}),
        _tool("Skillx", {"skill": "loom-visualization"}),
        {"type": "assistant", "message": {"content": [
            {"type": "text", "text": "I will use loom-visualization now"}]}},
        {"type": "user", "message": {"content": [
            {"type": "tool_use", "name": "Skill", "input": {"skill": "loom-visualization"}}]}},
        {"type": "result", "result": "Skill loom-visualization invoked"},
    ]
    got = run_ab.parse_stream(_write(tmp_path / "s.jsonl", [json.dumps(e) for e in events]))
    assert got["invoked"] is False and got["error"] is False


def test_parse_stream_truncated_before_result_reports_error(run_ab, tmp_path: Path) -> None:
    """A stream cut before its result event (half a JSON line at the end) is incomplete."""
    whole = json.dumps(_tool("Skill", {"skill": "loom-visualization"}))
    got = run_ab.parse_stream(_write(tmp_path / "s.jsonl", [whole, json.dumps(FINAL)[:20]]))
    assert got["error"] is True


def test_parse_stream_empty_file_reports_error(run_ab, tmp_path: Path) -> None:
    """An empty stream file is an unmeasured session, not a measured no-invoke."""
    path = tmp_path / "s.jsonl"
    path.write_text("", encoding="utf-8")
    assert run_ab.parse_stream(path)["error"] is True


def test_parse_stream_malformed_invocation_line_reports_error(run_ab, tmp_path: Path) -> None:
    """A corrupted line mid-stream must make the session incomplete, not a silent no-invoke."""
    corrupted = json.dumps(_tool("Skill", {"skill": "loom-visualization"}))[:-3]
    got = run_ab.parse_stream(_write(tmp_path / "s.jsonl", [corrupted, json.dumps(FINAL)]))
    assert got["error"] is True or got["invoked"] is True


def test_parse_stream_wrong_type_input_not_silent_invoke(run_ab, tmp_path: Path) -> None:
    """A Skill input of the wrong JSON type is either rejected loudly or not counted."""
    path = _write(tmp_path / "s.jsonl", [
        json.dumps(_tool("Skill", "loom-visualization")), json.dumps(FINAL)])
    try:
        got = run_ab.parse_stream(path)
    except (AttributeError, TypeError):
        return
    assert got["invoked"] is False


# --- decision rule --------------------------------------------------------


def test_decide_equal_and_zero_counts_hold(run_ab) -> None:
    """Equal counts, including zero against zero, never ship."""
    assert run_ab.decide(0, 0) == "HOLD"
    assert run_ab.decide(18, 18) == "HOLD"
    assert run_ab.decide(18, 17) == "HOLD"


def test_report_errored_b_session_holds(run_ab, tmp_path: Path, monkeypatch) -> None:
    """A B win that rests on an errored (unmeasured) session must not be reported as SHIP."""
    monkeypatch.setattr(run_ab, "EVIDENCE", tmp_path / "evidence")
    monkeypatch.setattr(run_ab, "CHANGE_DIR", tmp_path)
    monkeypatch.setattr(run_ab, "RESULTS", tmp_path / "results.md")
    ids = [pid for pid, _ in run_ab.prompts()]
    for variant in ("A", "B"):
        (tmp_path / "evidence" / f"ab-{variant}").mkdir(parents=True)
        for pid in ids:
            _write(tmp_path / "evidence" / f"ab-{variant}" / f"{pid}-run1.jsonl", [json.dumps(FINAL)])
    _write(tmp_path / "evidence/ab-B" / f"{ids[0]}-run1.jsonl", [
        json.dumps(_tool("Skill", {"skill": "loom-visualization"})),
        json.dumps({"type": "result", "is_error": True, "api_error_status": 429, "result": "limit"})])
    run_ab.report(runs=1)
    assert "**SHIP**" not in (tmp_path / "results.md").read_text(encoding="utf-8")
