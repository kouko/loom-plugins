"""Adversary probes: the visualization-card hook now runs on every prompt
(UserPromptSubmit), so any stall or silent empty card costs every turn.

Each probe runs the committed hook as a subprocess with an isolated HOME,
config dir and project dir. A probe that fails is a break, not a flake.

Run:
    uv run --isolated --with-requirements requirements-package-tests.lock \
        python -m pytest -q -p no:cacheprovider \
        docs/loom/2026-09-16-plain-language-replies/evidence/probes/test_probe_card_hook_boundaries.py
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pytest


def _find_repo_root(start: Path) -> Path:
    """Walk upward until a directory holding docs/loom and loom-workflow is found."""
    for candidate in [start.resolve(), *start.resolve().parents]:
        if (candidate / "docs" / "loom").is_dir() and (candidate / "loom-workflow").is_dir():
            return candidate
    raise RuntimeError(f"repo root not found above {start}")


ROOT = _find_repo_root(Path(__file__).parent)
PLUGIN = ROOT / "loom-workflow"
HOOK = PLUGIN / "hooks" / "visualization-card"
FULL = (PLUGIN / "skills/loom-visualization/assets/trigger-card.md").read_text(encoding="utf-8")
KEY = "ascii-graph-toolkit@monkey-skills"


@pytest.fixture
def dirs(tmp_path):
    home = tmp_path / "home"
    config = home / ".claude"
    project = tmp_path / "project"
    config.mkdir(parents=True)
    project.mkdir()
    return home, config, project


def _env(home, project, plugin_root=PLUGIN):
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
    env.update(HOME=str(home), CLAUDE_PROJECT_DIR=str(project), CLAUDE_PLUGIN_ROOT=str(plugin_root))
    return env


def _run(env, stdin: bytes, args=(), timeout=30, stdout=subprocess.PIPE):
    return subprocess.run([sys.executable, "-I", str(HOOK), *args], input=stdin,
                          stdout=stdout, stderr=subprocess.PIPE, env=env, timeout=timeout)


def _context(stdout: bytes) -> str:
    return json.loads(stdout)["hookSpecificOutput"]["additionalContext"]


@pytest.mark.parametrize("args", [(), ("--host=codex",)], ids=["claude", "codex"])
def test_cardHook_hugeCjkPrompt_emitsCardUnderTwoSeconds(dirs, args):
    """A 30 MB pasted prompt with CJK text and a lone surrogate still yields the card quickly."""
    home, _config, project = dirs
    payload = json.dumps({"hook_event_name": "UserPromptSubmit", "cwd": str(project),
                          "prompt": "中" * 5_000_000 + "\ud800"}).encode()
    start = time.monotonic()
    proc = _run(_env(home, project), payload, args)
    elapsed = time.monotonic() - start
    assert proc.returncode == 0, proc.stderr
    assert _context(proc.stdout).strip() == FULL.strip()
    assert elapsed < 2.0, elapsed


def test_cardHook_nonUtf8Stdin_emitsFullCard(dirs):
    """Invalid UTF-8 on stdin is malformed input: exit 0 with the full card."""
    home, _config, project = dirs
    proc = _run(_env(home, project), b"\xff\xfe{\"prompt\": \"\x80\"}")
    assert proc.returncode == 0, proc.stderr
    assert _context(proc.stdout).strip() == FULL.strip()


def test_cardHook_twentyConcurrentTurns_emitIdenticalOutput(dirs):
    """Two sessions submitting at once share no state: every run prints the same bytes."""
    home, _config, project = dirs
    env = _env(home, project)
    payload = json.dumps({"hook_event_name": "UserPromptSubmit", "prompt": "hi"}).encode()
    with ThreadPoolExecutor(max_workers=20) as pool:
        procs = list(pool.map(lambda _: _run(env, payload), range(20)))
    assert {p.returncode for p in procs} == {0}
    assert len({p.stdout for p in procs}) == 1


def test_cardHook_closedStdout_neverExitsWithBlockingCode(dirs):
    """Exit code 2 blocks the user's prompt on UserPromptSubmit; a closed stdout must not produce it."""
    home, _config, project = dirs
    proc = _run(_env(home, project), b"{}", stdout=subprocess.DEVNULL)
    assert proc.returncode != 2
    r, w = os.pipe()
    os.close(r)
    try:
        proc = subprocess.run([sys.executable, "-I", str(HOOK)], input=b"{}", stdout=w,
                              stderr=subprocess.PIPE, env=_env(home, project), timeout=30)
    finally:
        os.close(w)
    assert proc.returncode != 2, proc.stderr


def test_cardHook_hungSettingsFile_finishesWithinFiveSeconds(dirs):
    """A settings file that never returns data (FIFO, hung network mount) must not stall every prompt."""
    home, config, project = dirs
    (config / "plugins").mkdir()
    (config / "plugins" / "installed_plugins.json").write_text(
        json.dumps({"version": 2, "plugins": {KEY: [{"scope": "user"}]}}), encoding="utf-8")
    os.mkfifo(config / "settings.json")
    try:
        proc = _run(_env(home, project), b"{}", timeout=5)
    except subprocess.TimeoutExpired:
        pytest.fail("hook blocked >5s on an unreadable settings file; hooks.json sets no timeout, "
                    "so the host default applies to every prompt")
    assert proc.returncode == 0


def test_cardHook_undecodablePluginRootCard_fallsBackToBundledCard(dirs, tmp_path):
    """A non-UTF-8 card under CLAUDE_PLUGIN_ROOT should fall through to the bundled card, not an empty one."""
    home, _config, project = dirs
    fake = tmp_path / "fake-root"
    card = fake / "skills" / "loom-visualization" / "assets" / "trigger-card.md"
    card.parent.mkdir(parents=True)
    card.write_bytes(b"\xff\xfe\x00 not utf-8")
    proc = _run(_env(home, project, plugin_root=fake), b"{}")
    assert proc.returncode == 0, proc.stderr
    assert _context(proc.stdout).strip() == FULL.strip()
