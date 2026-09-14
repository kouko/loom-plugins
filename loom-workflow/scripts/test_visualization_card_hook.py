"""Tests for the loom-workflow SessionStart hook `hooks/visualization-card`.

Covers plan W2-05 acceptance 9 (A9) as unit tests:
  - positive `enabled-toolkit-prints-coexist-card`
  - boundary `disabled-or-other-project-prints-full-card`

Acceptance 8 (A8) cases `comparison-prompt-stream-shows-skill-call-and-table`
and `trivial-control-no-skill-call-no-diagram` are blind-run protocol (spec
design decision "Unprompted-use protocol"), not unit tests: they need a live
agent session and its event stream. Here only the card content they rely on
is checked (the full card names `loom-visualization` and its comparison and
flow triggers).

The hook runs as a subprocess via `python3 -I` with an isolated HOME,
config dir and project dir passed through the environment.
"""

import json
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
HOOK = PLUGIN_ROOT / "hooks" / "visualization-card"
HOOKS_JSON = PLUGIN_ROOT / "hooks" / "hooks.json"
ASSETS = PLUGIN_ROOT / "skills" / "loom-visualization" / "assets"
FULL_CARD = ASSETS / "trigger-card.md"
COEXIST_CARD = ASSETS / "trigger-card-coexist.md"
TOOLKIT_FIXTURE = Path(__file__).resolve().parent / "fixtures_ascii_graph_trigger_card.md"

KEY = "ascii-graph-toolkit@monkey-skills"

# Shape vocabulary used to read trigger phrases. Keys are shape names; values
# are patterns naming that shape. Non-toolkit shapes are included so the
# equality assertion on the toolkit card is not vacuous.
SHAPES = {
    "flow": r"\bflows?\b",
    "state machine": r"\bstate machines?\b",
    "architecture": r"\barchitectures?\b",
    "box-drawing/ASCII diagram": r"box-drawing|\bascii\b",
    "sequence": r"\bsequences?\b",
    "option comparison": r"\bcomparisons?\b",
    "branching decision": r"\bbranching\b",
    "reasoning chain": r"\breasoning chains?\b",
    "timeline": r"\btimelines?\b",
    "data model": r"\bdata models?\b",
}
TOOLKIT_SHAPES = {"flow", "state machine", "architecture", "box-drawing/ASCII diagram"}


# ---------- helpers ----------

def _sentences(text):
    body = "\n".join(l for l in text.splitlines() if not l.lstrip().startswith(("<!--", "#")))
    body = re.sub(r"\s+", " ", body)
    return [s for s in re.split(r"(?<=[.!?])\s+", body) if s.strip()]


def _trigger_phrases(text):
    """Sentences that instruct invoking a skill."""
    return [s for s in _sentences(text) if re.search(r"\binvo[kc]", s, re.I)]


def _shapes_named(sentences):
    found = set()
    for s in sentences:
        for name, pat in SHAPES.items():
            if re.search(pat, s, re.I):
                found.add(name)
    return found


def _write(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(obj if isinstance(obj, str) else json.dumps(obj), encoding="utf-8")


def _install(config, entries):
    _write(config / "plugins" / "installed_plugins.json",
           {"version": 2, "plugins": {KEY: entries}})


@pytest.fixture
def env_dirs(tmp_path):
    home = tmp_path / "home"
    project = tmp_path / "project"
    (home / ".claude").mkdir(parents=True)
    project.mkdir()
    return home, home / ".claude", project


def _run(home, project=None, stdin=None, cwd=None, config_dir=None, extra_env=None):
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
    env["HOME"] = str(home)
    env["CLAUDE_PLUGIN_ROOT"] = str(PLUGIN_ROOT)
    if project is not None:
        env["CLAUDE_PROJECT_DIR"] = str(project)
    if config_dir is not None:
        env["CLAUDE_CONFIG_DIR"] = str(config_dir)
    if extra_env:
        env.update(extra_env)
    if stdin is None:
        stdin = json.dumps({"hook_event_name": "SessionStart", "session_id": "s1",
                            "cwd": str(cwd or project or home)})
    proc = subprocess.run([sys.executable, "-I", str(HOOK)], input=stdin, capture_output=True,
                          text=True, env=env, cwd=str(cwd or home), timeout=30)
    assert proc.returncode == 0, proc.stderr
    return proc


def _context(proc):
    data = json.loads(proc.stdout)
    ctx = data["hookSpecificOutput"]["additionalContext"]
    assert data["hookSpecificOutput"]["hookEventName"] == "SessionStart"
    assert data["additional_context"] == ctx
    assert data["additionalContext"] == ctx
    return ctx


def _is_full(ctx):
    return ctx.strip() == FULL_CARD.read_text(encoding="utf-8").strip()


def _is_coexist(ctx):
    return ctx.strip() == COEXIST_CARD.read_text(encoding="utf-8").strip()


# ---------- registration ----------

def test_hooks_json_registers_session_start_and_keeps_post_tool_use():
    hooks = json.loads(HOOKS_JSON.read_text(encoding="utf-8"))["hooks"]
    assert hooks["PostToolUse"] == [{
        "matcher": "Write|Edit",
        "hooks": [{"type": "command",
                   "command": "${CLAUDE_PLUGIN_ROOT}/scripts/validate-skill-folder-structure.sh"}],
    }]
    (entry,) = hooks["SessionStart"]
    assert entry["matcher"] == "startup|clear|compact"
    (h,) = entry["hooks"]
    assert h["type"] == "command"
    assert h["command"] == '"${CLAUDE_PLUGIN_ROOT}/hooks/visualization-card"'
    assert h["async"] is False


def test_hook_is_executable_python3_script():
    assert os.access(HOOK, os.X_OK)
    assert HOOK.read_text(encoding="utf-8").splitlines()[0] == "#!/usr/bin/env python3"


# ---------- A9 positive: enabled-toolkit-prints-coexist-card ----------

def test_enabled_toolkit_prints_coexist_card(env_dirs):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_coexist(_context(_run(home, project)))


def test_project_scope_detected_from_subdirectory_session(env_dirs):
    home, config, project = env_dirs
    sub = project / "pkg" / "deep"
    sub.mkdir(parents=True)
    _install(config, [{"scope": "project", "installPath": "/x", "version": "0.6.0",
                       "projectPath": str(project)}])
    _write(project / ".claude" / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_coexist(_context(_run(home, project, cwd=sub)))


def test_stdin_cwd_is_project_root_fallback(env_dirs):
    home, config, project = env_dirs
    _install(config, [{"scope": "local", "installPath": "/x", "version": "0.6.0",
                       "projectPath": str(project)}])
    _write(project / ".claude" / "settings.local.json", {"enabledPlugins": {KEY: True}})
    assert _is_coexist(_context(_run(home, None, cwd=project)))


def test_config_dir_override_is_used(env_dirs, tmp_path):
    home, _default_config, project = env_dirs
    override = tmp_path / "alt-config"
    _install(override, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(override / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_coexist(_context(_run(home, project, config_dir=override)))


def test_config_dir_override_ignores_default_dir(env_dirs, tmp_path):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    empty = tmp_path / "empty-config"
    empty.mkdir()
    assert _is_full(_context(_run(home, project, config_dir=empty)))


# ---------- A9 boundary: disabled-or-other-project-prints-full-card ----------

def test_disabled_prints_full_card(env_dirs):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    _write(project / ".claude" / "settings.local.json", {"enabledPlugins": {KEY: False}})
    assert _is_full(_context(_run(home, project)))


def test_other_project_scope_prints_full_card(env_dirs, tmp_path):
    home, config, project = env_dirs
    other = tmp_path / "other"
    other.mkdir()
    _install(config, [{"scope": "project", "installPath": "/x", "version": "0.6.0",
                       "projectPath": str(other)}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_full(_context(_run(home, project)))


def test_not_installed_prints_full_card(env_dirs):
    home, config, project = env_dirs
    _write(config / "plugins" / "installed_plugins.json", {"version": 2, "plugins": {}})
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _is_full(_context(_run(home, project)))


@pytest.mark.parametrize("target", ["installed", "settings"])
def test_malformed_json_prints_full_card(env_dirs, target):
    home, config, project = env_dirs
    _install(config, [{"scope": "user", "installPath": "/x", "version": "0.6.0"}])
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    bad = config / ("plugins/installed_plugins.json" if target == "installed" else "settings.json")
    _write(bad, "{not json")
    assert _is_full(_context(_run(home, project)))


@pytest.mark.parametrize("stdin", ["", "{not json", "[1, 2]"])
def test_empty_or_malformed_stdin_still_emits_json(env_dirs, stdin):
    home, _config, project = env_dirs
    assert _is_full(_context(_run(home, project, stdin=stdin)))


# ---------- card content ----------

@pytest.mark.parametrize("card", [FULL_CARD, COEXIST_CARD], ids=["full", "coexist"])
def test_cards_at_most_150_words(card):
    assert len(card.read_text(encoding="utf-8").split()) <= 150


def test_full_card_names_skill_and_comparison_and_flow_triggers():
    phrases = _trigger_phrases(FULL_CARD.read_text(encoding="utf-8"))
    assert any("loom-visualization" in s for s in phrases)
    named = _shapes_named(phrases)
    assert {"option comparison", "flow", "box-drawing/ASCII diagram"} <= named


def test_toolkit_card_trigger_shapes_are_the_expected_four():
    phrases = _trigger_phrases(TOOLKIT_FIXTURE.read_text(encoding="utf-8"))
    assert phrases
    assert _shapes_named(phrases) == TOOLKIT_SHAPES


def test_coexist_card_trigger_phrases_do_not_overlap_toolkit():
    text = COEXIST_CARD.read_text(encoding="utf-8")
    phrases = _trigger_phrases(text)
    assert any("loom-visualization" in s for s in phrases)
    named = _shapes_named(phrases)
    toolkit = _shapes_named(_trigger_phrases(TOOLKIT_FIXTURE.read_text(encoding="utf-8")))
    assert not (named & toolkit)
    assert {"option comparison", "branching decision", "reasoning chain",
            "timeline", "sequence", "data model"} <= named
    assert re.search(r"\bquantit", " ".join(phrases), re.I)
    assert re.search(r"reasoning pages?", " ".join(phrases), re.I)
    assert re.search(r"ascii-graph", text, re.I)


def test_coexist_card_picks_markdown_table_not_mermaid():
    """The hook host always has a shell, so the Mermaid gate never allows Mermaid there."""
    body = " ".join(_sentences(COEXIST_CARD.read_text(encoding="utf-8")))
    assert not re.search(r"mermaid", body, re.I)
    assert re.search(r"picks a markdown table, adding ASCII only when needed", body)


def test_coexist_card_box_drawing_split_between_skill_checks_and_toolkit_card():
    """Prescribed box drawing uses loom-visualization's align.py; the toolkit card keeps three shapes."""
    body = " ".join(_sentences(COEXIST_CARD.read_text(encoding="utf-8")))
    assert re.search(
        r"[Bb]ox-drawing diagrams prescribed by loom-visualization are drawn and verified "
        r"with loom-visualization's own `scripts/align\.py` and checks", body)
    assert re.search(r"the ascii-graph card covers flows, state machines and architecture;", body)
    assert not re.search(r"ascii-graph card covers[^.]*sequences", body)
