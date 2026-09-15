"""Adversarial probes for `hooks/visualization-card --host=codex` and the Codex
hook wiring (`hooks/hooks-codex.json`, `.codex-plugin/plugin.json`).

Codex marks a hook failed when its JSON carries keys beside
`hookSpecificOutput`, so on Codex the output must be exactly that one key.
The Claude path must stay byte-identical to the base commit.
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
FULL = (ASSETS / "trigger-card.md").read_text(encoding="utf-8")
COEXIST = (ASSETS / "trigger-card-coexist.md").read_text(encoding="utf-8")
KEY = "ascii-graph-toolkit@monkey-skills"
BASE = "80dbc465"
STRIP = ("CLAUDE_CONFIG_DIR", "CLAUDE_PROJECT_DIR", "CLAUDE_PLUGIN_ROOT", "PLUGIN_ROOT")


def _env(tmp_path, toolkit_active=False, **extra):
    config = tmp_path / "home" / ".claude"
    (config / "plugins").mkdir(parents=True, exist_ok=True)
    project = tmp_path / "project"
    project.mkdir(exist_ok=True)
    if toolkit_active:
        (config / "plugins" / "installed_plugins.json").write_text(
            json.dumps({"plugins": {KEY: [{"scope": "user"}]}}), encoding="utf-8")
        (config / "settings.json").write_text(
            json.dumps({"enabledPlugins": {KEY: True}}), encoding="utf-8")
    env = {k: v for k, v in os.environ.items() if k not in STRIP}
    env.update(CLAUDE_CONFIG_DIR=str(config), CLAUDE_PROJECT_DIR=str(project))
    env.update(extra)
    return env


def _run(args, env, stdin=b"{}", hook=HOOK, cwd=None):
    return subprocess.run([sys.executable, str(hook), *args], input=stdin,
                          capture_output=True, env=env, cwd=cwd)


def _codex_payload(proc):
    assert proc.returncode == 0, proc.stderr
    lines = proc.stdout.decode("utf-8").splitlines()
    assert len(lines) == 1, lines
    data = json.loads(lines[0])
    assert list(data) == ["hookSpecificOutput"], data.keys()
    assert set(data["hookSpecificOutput"]) == {"hookEventName", "additionalContext"}
    assert data["hookSpecificOutput"]["hookEventName"] == "UserPromptSubmit"
    return data["hookSpecificOutput"]["additionalContext"]


def test_visualization_card_codex_toolkit_active_full_card_only_key(tmp_path):
    """Claude config says the toolkit is active; Codex still gets the full card
    and nothing but `hookSpecificOutput`."""
    env = _env(tmp_path, toolkit_active=True)
    assert json.loads(_run([], env).stdout)["additionalContext"] == COEXIST
    assert _codex_payload(_run(["--host=codex"], env)) == FULL


@pytest.mark.parametrize(
    "stdin",
    [b"", b"not json", b"[1,2]", b"\xff\xfe\x00", b'{"cwd": 7}', b"{" * 100000],
    ids=["empty", "text", "array", "binary", "bad-cwd", "deep"],
)
def test_visualization_card_codex_malformed_stdin_single_key(tmp_path, stdin):
    assert _codex_payload(_run(["--host=codex"], _env(tmp_path), stdin=stdin)) == FULL


@pytest.mark.parametrize(
    "args",
    [["--host=codex", "--extra"], ["--verbose", "--host=codex"], ["--host=codex"] * 2],
    ids=["trailing-arg", "leading-arg", "repeated"],
)
def test_visualization_card_codex_extra_args_single_key(tmp_path, args):
    assert _codex_payload(_run(args, _env(tmp_path))) == FULL


@pytest.mark.parametrize(
    "args",
    [["--host", "codex"], ["--host=Codex"], ["--host=claude"], ["--bogus"]],
    ids=["space-form", "capitalised", "other-host", "bogus"],
)
def test_visualization_card_unrecognised_host_form_claude_shape_exit0(tmp_path, args):
    """Only the exact `--host=codex` token selects Codex; any other spelling
    falls back to the Claude three-key shape without crashing (the committed
    Codex hook uses the exact token)."""
    proc = _run(args, _env(tmp_path))
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert set(data) == {"hookSpecificOutput", "additional_context", "additionalContext"}


def test_visualization_card_codex_assets_missing_empty_context_exit0(tmp_path):
    """A hook copied away from its assets with no plugin-root env still exits 0
    with the single Codex key (empty context, never a traceback)."""
    lonely = tmp_path / "plugin" / "hooks" / "visualization-card"
    lonely.parent.mkdir(parents=True)
    shutil.copy(HOOK, lonely)
    proc = _run(["--host=codex"], _env(tmp_path), hook=lonely)
    assert _codex_payload(proc) == ""
    assert proc.stderr == b""


def _base_hook(tmp_path):
    shown = subprocess.run(["git", "-C", str(PLUGIN_ROOT), "show",
                            f"{BASE}:loom-workflow/hooks/visualization-card"],
                           capture_output=True)
    if shown.returncode != 0:
        pytest.skip(f"base commit {BASE} not available in this clone")
    base = tmp_path / "base" / "hooks" / "visualization-card"
    base.parent.mkdir(parents=True)
    base.write_bytes(shown.stdout)
    return base


@pytest.mark.parametrize("active", [False, True], ids=["full", "coexist"])
@pytest.mark.parametrize("stdin", [b"{}", b"garbage"], ids=["json", "garbage"])
def test_visualization_card_claude_default_matches_base_bytes(tmp_path, active, stdin):
    base = _base_hook(tmp_path)
    env = _env(tmp_path, toolkit_active=active, CLAUDE_PLUGIN_ROOT=str(PLUGIN_ROOT))
    old = _run([], env, stdin=stdin, hook=base)
    new = _run([], env, stdin=stdin)
    assert old.returncode == new.returncode == 0
    # Only the event name moved (SessionStart -> UserPromptSubmit).
    assert new.stdout == old.stdout.replace(b'"SessionStart"', b'"UserPromptSubmit"')
    assert b'"SessionStart"' not in new.stdout


def test_visualization_card_codex_hooks_json_command_uses_plugin_root(tmp_path):
    """The Codex hook command names PLUGIN_ROOT only, and run through `sh -c`
    from an unrelated cwd with a space in the plugin path it delivers the
    single-key full card."""
    hooks = json.loads((PLUGIN_ROOT / "hooks" / "hooks-codex.json").read_text(encoding="utf-8"))
    assert set(hooks["hooks"]) == {"UserPromptSubmit"}
    groups = hooks["hooks"]["UserPromptSubmit"]
    commands = [h["command"] for g in groups for h in g["hooks"]]
    assert len(commands) == 1
    command = commands[0]
    assert "${PLUGIN_ROOT}" in command and "CLAUDE_PLUGIN_ROOT" not in command

    installed = tmp_path / "with space" / "loom-workflow"
    shutil.copytree(PLUGIN_ROOT / "hooks", installed / "hooks")
    shutil.copytree(ASSETS, installed / "skills" / "loom-visualization" / "assets")
    env = _env(tmp_path, toolkit_active=True, PLUGIN_ROOT=str(installed))
    proc = subprocess.run(["sh", "-c", command], input=b"{}", capture_output=True,
                          env=env, cwd=tmp_path / "project")
    assert _codex_payload(proc) == FULL


def test_visualization_card_codex_manifest_hooks_path_resolves():
    manifest = json.loads((PLUGIN_ROOT / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    target = (PLUGIN_ROOT / manifest["hooks"]).resolve()
    assert target == (PLUGIN_ROOT / "hooks" / "hooks-codex.json").resolve()
    assert target.is_file()
    claude = json.loads((PLUGIN_ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    assert "--host=codex" not in json.dumps(claude)
