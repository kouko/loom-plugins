"""Adversarial probes for the loom-visualization description A/B change.

Targets: the A/B runner's stream parser and decision rule (ab/run_ab.py), the
committed tested-hash guard (test_loom_visualization_description_ab.py), and the
description renderer shared with the budget guard
(scripts/test_loom_skill_description_catalog.py).

Probes that pass record attacks the change survived. Probes marked
``xfail(strict=True)`` record a real defect: they assert the behaviour that
should hold and currently fail; a fix turns them into an XPASS, which fails the
run so the marker gets removed.
"""

from __future__ import annotations

import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest


REPO_ROOT = Path(__file__).resolve().parents[2]
CHANGE_DIR = REPO_ROOT / "docs/loom/2026-09-14-loom-visualization-description-trigger"
RUN_AB = CHANGE_DIR / "ab/run_ab.py"
GUARD = Path(__file__).resolve().parent / "test_loom_visualization_description_ab.py"
CATALOG = REPO_ROOT / "scripts/test_loom_skill_description_catalog.py"
SKILL = REPO_ROOT / "loom-workflow/skills/loom-visualization/SKILL.md"


def _load(name: str, path: Path):
    if not path.exists():
        pytest.skip(f"{path} is absent")
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def run_ab():
    return _load("adversarial_run_ab", RUN_AB)


@pytest.fixture(scope="module")
def guard():
    return _load("adversarial_description_guard", GUARD)


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


@pytest.mark.xfail(strict=True, reason="malformed lines are skipped silently: undercount with error=False")
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


@pytest.mark.xfail(strict=True, reason="report() counts invocations from error sessions; decide() never sees them")
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


# --- tested-hash guard ----------------------------------------------------


def _results(tmp_path: Path, body: str) -> Path:
    path = tmp_path / "results.md"
    path.write_text(body, encoding="utf-8")
    return path


def _shipped_hash(guard) -> str:
    return guard.run_ab.sha256_text(guard._shipped())


def test_guard_missing_hash_line_fails_closed(guard, tmp_path: Path, monkeypatch) -> None:
    """results.md without the hash line fails the guard instead of passing vacuously."""
    monkeypatch.setattr(guard, "RESULTS", _results(tmp_path, "## Decision\n\n**SHIP**\n"))
    with pytest.raises(AssertionError):
        guard.test_description_shipped_text_equals_tested_hash()


def test_guard_uppercase_hash_fails_closed(guard, tmp_path: Path, monkeypatch) -> None:
    """An uppercase-hex hash line does not match and fails the guard."""
    line = f"B rendered description SHA-256: `{_shipped_hash(guard).upper()}`\n"
    monkeypatch.setattr(guard, "RESULTS", _results(tmp_path, "**SHIP**\n\n" + line))
    with pytest.raises(AssertionError):
        guard.test_description_shipped_text_equals_tested_hash()


@pytest.mark.xfail(strict=True, reason="HASH_LINE.search takes the first match; a conflicting second line is ignored")
def test_guard_duplicate_conflicting_hash_lines_fails_closed(guard, tmp_path: Path, monkeypatch) -> None:
    """Two hash lines that disagree make the tested text ambiguous, so the guard must fail."""
    good = f"B rendered description SHA-256: `{_shipped_hash(guard)}`\n"
    bad = f"B rendered description SHA-256: `{'0' * 64}`\n"
    monkeypatch.setattr(guard, "RESULTS", _results(tmp_path, "**SHIP**\n\n" + good + bad))
    with pytest.raises(AssertionError):
        guard.test_description_shipped_text_equals_tested_hash()


@pytest.mark.xfail(strict=True, reason="guard checks the hash only, never that the recorded decision is SHIP")
def test_guard_hold_decision_with_matching_hash_fails(guard, tmp_path: Path, monkeypatch) -> None:
    """Shipping B while results.md records HOLD (A/B lost) must fail the guard."""
    line = f"B rendered description SHA-256: `{_shipped_hash(guard)}`\n"
    monkeypatch.setattr(guard, "RESULTS", _results(tmp_path, "## Decision\n\n**HOLD**\n\n" + line))
    with pytest.raises(AssertionError):
        guard.test_description_shipped_text_equals_tested_hash()


# --- renderer shared by the hash guard and the budget guard ---------------


def test_render_description_trailing_whitespace_renders_identically(run_ab) -> None:
    """Trailing spaces on the scalar line render to the same text, so the hash is unchanged."""
    text = SKILL.read_text(encoding="utf-8")
    head, rest = text.split("\n---\n", 1)
    padded = head.replace(run_ab.DESCRIPTION_B, run_ab.DESCRIPTION_B + "   \t") + "\n---\n" + rest
    assert run_ab._render_description(padded) == run_ab.DESCRIPTION_B


def test_render_description_folded_scalar_fails_closed(run_ab) -> None:
    """A folded (>) or plain scalar is not silently rendered as an empty description."""
    for header in ("description: >\n", "description: "):
        text = f"---\nname: x\n{header}  {run_ab.DESCRIPTION_B}\n---\nbody\n"
        with pytest.raises(AssertionError):
            run_ab._render_description(text)


@pytest.mark.xfail(strict=True, reason="block-scalar regex stops at a blank line; later paragraphs are invisible")
def test_render_description_blank_line_paragraph_changes_hash(run_ab) -> None:
    """Text appended after a blank line inside the block scalar must change the rendered description."""
    text = SKILL.read_text(encoding="utf-8")
    edited = text.replace(run_ab.DESCRIPTION_B + "\n",
                          run_ab.DESCRIPTION_B + "\n\n  " + "untested extra words " * 200 + "\n", 1)
    assert edited != text
    assert run_ab.sha256_text(run_ab._render_description(edited)) != run_ab.DESCRIPTION_B_SHA256


# --- guard dependency on the A/B runner -----------------------------------


@pytest.mark.xfail(strict=True, reason="committed guard imports ab/run_ab.py; it cannot collect without the runner")
def test_guard_without_runner_script_still_collects(tmp_path: Path) -> None:
    """The committed guard needs only results.md and SKILL.md, not the A/B runner script."""
    for rel in ("loom-workflow/scripts/test_loom_visualization_description_ab.py",
                "loom-workflow/skills/loom-visualization/SKILL.md",
                "scripts/test_loom_skill_description_catalog.py",
                "docs/loom/2026-09-14-loom-visualization-description-trigger/ab/results.md"):
        (tmp_path / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy(REPO_ROOT / rel, tmp_path / rel)
    proc = subprocess.run(
        [sys.executable, "-m", "pytest", "-q", "-p", "no:cacheprovider",
         "loom-workflow/scripts/test_loom_visualization_description_ab.py"],
        cwd=tmp_path, capture_output=True, text=True, env={"PYTHONDONTWRITEBYTECODE": "1", "PATH": "/usr/bin:/bin"})
    assert proc.returncode == 0, proc.stdout[-800:]
