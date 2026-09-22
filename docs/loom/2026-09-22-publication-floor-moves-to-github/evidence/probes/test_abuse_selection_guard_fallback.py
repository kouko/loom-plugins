"""Adversarial probe: does a missing checker loosen the selection-store guard?

The Design decision "Host fallbacks allow too" turns the Codex stale-root
fallback (`hooks/hooks-codex.json`) and the agy adapter's failure path
(`hooks/agy_adapter.py`) from deny-everything into allow-publication, and
keeps denying only a command or file target naming `loom/selections`. The
intent Constraint is that `selection.guard` is not loosened. The attack:
writes into the record store that the running checker's guard refuses but
whose text does not contain the literal `loom/selections`.

Run from the repo root inside the package-tests uv environment:

    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest \
        docs/loom/2026-09-22-publication-floor-moves-to-github/evidence/probes/test_abuse_selection_guard_fallback.py -q

Attempts the change survives PASS; attempts that expose a defect FAIL on
purpose and must not be weakened.
"""
from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[5]
SCRIPTS = ROOT / "loom-code" / "scripts"
sys.path.insert(0, str(SCRIPTS))

from loom_checker.rule_checks.selection_guard import guard_reason

STORE = "loom/" + "selections"  # split so this file's own text is not a guard hit


def _repo(tmp_path: Path) -> Path:
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    (repo / ".git" / "loom" / "selections").mkdir(parents=True)
    return repo


def _bash(repo: Path, command: str) -> dict:
    return {"hook_event_name": "PreToolUse", "tool_name": "Bash",
            "tool_input": {"command": command}, "cwd": str(repo)}


def _write(repo: Path, file_path: str) -> dict:
    return {"hook_event_name": "PreToolUse", "tool_name": "Write",
            "tool_input": {"file_path": file_path, "content": "{}"}, "cwd": str(repo)}


def _codex_fallback(payload: dict, matcher: str, tmp_path: Path) -> subprocess.CompletedProcess:
    """Run the Codex PreToolUse command with PLUGIN_ROOT pointing at a
    directory that has no checker, i.e. the stale-root fallback."""
    hooks = json.loads((ROOT / "loom-code/hooks/hooks-codex.json").read_text(encoding="utf-8"))
    entry = next(e for e in hooks["hooks"]["PreToolUse"] if e["matcher"] == matcher)
    empty_root = tmp_path / "stale-root"
    empty_root.mkdir(exist_ok=True)
    return subprocess.run(["sh", "-c", entry["hooks"][0]["command"]],
                          input=json.dumps(payload), capture_output=True, text=True,
                          env={"PATH": "/usr/bin:/bin", "PLUGIN_ROOT": str(empty_root)},
                          cwd=payload["cwd"])


def _agy_missing_checker(command: str, cwd: Path, monkeypatch, capsys) -> dict:
    spec = importlib.util.spec_from_file_location(
        "agy_adapter_probe", ROOT / "loom-code/hooks/agy_adapter.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    monkeypatch.setattr(module, "CHECKER", cwd / "no-such-checker.py")
    module.push_gate({"toolCall": {"args": {"CommandLine": command, "Cwd": str(cwd)}},
                      "workspacePaths": [str(cwd)]})
    return json.loads(capsys.readouterr().out)


# Writes into the store whose text never spells the literal store path.
EVASIONS = [
    "cd .git/loom && printf x > selections/c.jsonl",
    "printf x > .git/loom//selections/c.jsonl",
    "printf x > .git/loom/./selections/c.jsonl",
]


@pytest.mark.parametrize("command", EVASIONS)
def test_checker_guard_store_write_denied(tmp_path: Path, command: str) -> None:
    """Control: with the checker running, each evasion is refused."""
    assert guard_reason(_bash(_repo(tmp_path), command)) is not None


@pytest.mark.parametrize("command", EVASIONS)
def test_codex_fallback_store_write_denied(tmp_path: Path, command: str) -> None:
    """Checker missing on Codex: the same write must still be refused (exit 2)."""
    result = _codex_fallback(_bash(_repo(tmp_path), command), "Bash", tmp_path)
    assert result.returncode == 2, (
        f"Codex stale-root fallback allows a selection-store write the checker "
        f"guard refuses: {command!r} -> exit {result.returncode}, {result.stderr.strip()!r}")


@pytest.mark.parametrize("command", EVASIONS)
def test_agy_fallback_store_write_denied(tmp_path: Path, monkeypatch, capsys, command: str) -> None:
    """Checker missing on agy: the same write must still be denied."""
    decision = _agy_missing_checker(command, _repo(tmp_path), monkeypatch, capsys)
    assert decision.get("decision") == "deny", (
        f"agy fallback allows a selection-store write the checker guard refuses: {decision}")


@pytest.mark.parametrize("relative", [
    ".git/loom/./selections/c.jsonl",
    ".git/loom//selections/c.jsonl",
])
def test_codex_fallback_store_file_write_denied(tmp_path: Path, relative: str) -> None:
    """A Write whose path spells the store unnormalised: the checker refuses
    it (realpath); the fallback must too."""
    repo = _repo(tmp_path)
    payload = _write(repo, f"{repo}/{relative}")  # a string: pathlib would normalise it
    assert f"{STORE}/" not in payload["tool_input"]["file_path"]
    assert guard_reason(payload) is not None  # control: checker running refuses
    result = _codex_fallback(payload, "apply_patch|Edit|Write", tmp_path)
    assert result.returncode == 2, (
        f"Codex fallback allows a file write into the store via {relative!r}")


def test_codex_fallback_literal_store_denied(tmp_path: Path) -> None:
    """Control: the literal store path is refused by the fallback."""
    result = _codex_fallback(_bash(_repo(tmp_path), f"printf x > .git/{STORE}/c.jsonl"),
                             "Bash", tmp_path)
    assert result.returncode == 2


def test_codex_fallback_push_allowed(tmp_path: Path) -> None:
    """Control (REQ-4): a push with the checker missing is allowed with the failure line."""
    result = _codex_fallback(_bash(_repo(tmp_path), "git push -u origin feat/x"), "Bash", tmp_path)
    assert result.returncode == 0
    assert "publication hook failed" in result.stderr
