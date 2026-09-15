"""Adversarial probes for the UserPromptSubmit hook `hooks/visualization-card`.

Each probe feeds hostile config or stdin and requires: exit 0, exactly one
stdout line, valid JSON with the three context keys equal, and the expected
card.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

PLUGIN_ROOT = Path(__file__).resolve().parents[1]
HOOK = PLUGIN_ROOT / "hooks" / "visualization-card"
ASSETS = PLUGIN_ROOT / "skills" / "loom-visualization" / "assets"
FULL = (ASSETS / "trigger-card.md").read_text(encoding="utf-8").strip()
COEXIST = (ASSETS / "trigger-card-coexist.md").read_text(encoding="utf-8").strip()
KEY = "ascii-graph-toolkit@monkey-skills"


def _dirs(tmp_path):
    config = tmp_path / "home" / ".claude"
    (config / "plugins").mkdir(parents=True)
    project = tmp_path / "project"
    project.mkdir()
    return config, project


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text if isinstance(text, str) else json.dumps(text), encoding="utf-8")


def _run(config, project, stdin="{}", hook=HOOK, plugin_root=PLUGIN_ROOT):
    env = {k: v for k, v in os.environ.items()
           if k not in ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT")}
    env.update(HOME=str(config.parent), CLAUDE_CONFIG_DIR=str(config),
               CLAUDE_PROJECT_DIR=str(project))
    if plugin_root is not None:
        env["CLAUDE_PLUGIN_ROOT"] = str(plugin_root)
    proc = subprocess.run([sys.executable, "-I", str(hook)], input=stdin, capture_output=True,
                          text=True, env=env, cwd=str(project), timeout=60)
    assert proc.returncode == 0, proc.stderr
    lines = proc.stdout.splitlines()
    assert len(lines) == 1, proc.stdout[:200]
    data = json.loads(lines[0])
    ctx = data["hookSpecificOutput"]["additionalContext"]
    assert data["additional_context"] == ctx == data["additionalContext"]
    return ctx.strip()


def _enable(config, value=True, scope_entry=None):
    _write(config / "plugins" / "installed_plugins.json",
           {"version": 2, "plugins": {KEY: [scope_entry or {"scope": "user"}]}})
    _write(config / "settings.json", {"enabledPlugins": {KEY: value}})


def test_visualization_card_deeply_nested_installed_json_prints_full_card(tmp_path):
    """A 100000-deep nested installed_plugins.json falls back to the full card."""
    config, project = _dirs(tmp_path)
    n = 100000
    _write(config / "plugins" / "installed_plugins.json", '{"plugins":' + "[" * n + "]" * n + "}")
    assert _run(config, project) == FULL


def test_visualization_card_huge_installed_json_prints_full_card(tmp_path):
    """A ~20 MB installed_plugins.json without the toolkit yields the full card."""
    config, project = _dirs(tmp_path)
    plugins = {f"p{i}@m": [{"scope": "user", "pad": "x" * 200}] for i in range(90000)}
    _write(config / "plugins" / "installed_plugins.json", {"plugins": plugins})
    assert _run(config, project) == FULL


@pytest.mark.parametrize("plugins", [[KEY], "ascii-graph-toolkit@x", None, 7])
def test_visualization_card_non_dict_plugins_prints_full_card(tmp_path, plugins):
    """A non-object `plugins` value yields the full card."""
    config, project = _dirs(tmp_path)
    _write(config / "plugins" / "installed_plugins.json", {"plugins": plugins})
    _write(config / "settings.json", {"enabledPlugins": {KEY: True}})
    assert _run(config, project) == FULL


@pytest.mark.parametrize("value", ["true", 1, "True", [True]])
def test_visualization_card_truthy_non_boolean_enabled_prints_full_card(tmp_path, value):
    """Only the JSON boolean true enables the toolkit; string "true" or 1 does not."""
    config, project = _dirs(tmp_path)
    _enable(config, value)
    assert _run(config, project) == FULL


def test_visualization_card_project_path_trailing_slash_prints_coexist(tmp_path):
    """A project-scoped projectPath with a trailing slash still matches the root."""
    config, project = _dirs(tmp_path)
    _enable(config, True, {"scope": "project", "projectPath": str(project) + "/"})
    assert _run(config, project) == COEXIST


def test_visualization_card_project_path_symlink_prints_coexist(tmp_path):
    """A projectPath that is a symlink to the project root still matches."""
    config, project = _dirs(tmp_path)
    link = tmp_path / "link"
    os.symlink(project, link)
    _enable(config, True, {"scope": "local", "projectPath": str(link)})
    assert _run(config, project) == COEXIST


def test_visualization_card_project_path_traversal_other_project_prints_full(tmp_path):
    """A projectPath resolving to another directory via .. does not match."""
    config, project = _dirs(tmp_path)
    (tmp_path / "other").mkdir()
    _enable(config, True, {"scope": "project", "projectPath": str(project / ".." / "other")})
    assert _run(config, project) == FULL


@pytest.mark.skipif(hasattr(os, "geteuid") and os.geteuid() == 0, reason="root reads mode 000")
def test_visualization_card_unreadable_settings_prints_full_card(tmp_path):
    """An unreadable settings.json falls back to the full card without a traceback."""
    config, project = _dirs(tmp_path)
    _enable(config, True)
    settings = config / "settings.json"
    settings.chmod(0)
    try:
        assert _run(config, project) == FULL
    finally:
        settings.chmod(0o644)


def test_visualization_card_settings_is_directory_prints_full_card(tmp_path):
    """A directory where the project settings.local.json should be yields the full card."""
    config, project = _dirs(tmp_path)
    _enable(config, True)
    (project / ".claude" / "settings.local.json").mkdir(parents=True)
    assert _run(config, project) == FULL


@pytest.mark.parametrize("stdin", ["[1,2]", "garbage", '{"cwd": 123}', "", "\x00\xff"])
def test_visualization_card_hostile_stdin_prints_one_card(tmp_path, stdin):
    """Non-object, non-JSON or wrongly typed stdin still yields exactly one card."""
    config, project = _dirs(tmp_path)
    assert _run(config, project, stdin=stdin) == FULL


def test_visualization_card_missing_assets_exits_zero_valid_json(tmp_path):
    """A hook copy with no assets anywhere still exits 0 with one valid JSON line."""
    config, project = _dirs(tmp_path)
    bare = tmp_path / "bare" / "hooks"
    bare.mkdir(parents=True)
    shutil.copy(HOOK, bare / "visualization-card")
    assert _run(config, project, hook=bare / "visualization-card", plugin_root=None) == ""
