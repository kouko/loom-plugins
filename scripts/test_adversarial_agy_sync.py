"""Adversarial probes for the Antigravity (agy) root-manifest half of
``scripts/sync_codex_manifests.py`` and its edit-time drift hook
``.claude/hooks/check-codex-manifest-drift.sh``.

Fixtures are self-contained plugin dirs under tmp_path; no committed manifest
is touched. A failing probe is a finding; a passing one records a survived attack.
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCRIPT = REPO_ROOT / "scripts" / "sync_codex_manifests.py"
HOOK = REPO_ROOT / ".claude" / "hooks" / "check-codex-manifest-drift.sh"

CLAUDE = {"name": "loom-code", "version": "9.9.9", "description": "d", "author": {"name": "k"},
          "license": "MIT", "keywords": ["x"]}


def _cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True)


def _plugin(root: Path, name: str = "loom-code") -> Path:
    plugin = root / name
    (plugin / ".claude-plugin").mkdir(parents=True)
    claude = dict(CLAUDE, name=name)
    (plugin / ".claude-plugin" / "plugin.json").write_text(json.dumps(claude), encoding="utf-8")
    assert _cli("--scaffold", str(plugin)).returncode == 0
    assert _cli(str(plugin)).returncode == 0
    return plugin


def test_syncagy_generated_root_manifest_carries_only_agy_fields(tmp_path):
    """The generated root manifest holds name/version/description and nothing else."""
    plugin = _plugin(tmp_path)
    root = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
    assert list(root) == ["name", "version", "description"]


def test_syncagy_extra_key_single_plugin_check_fails(tmp_path):
    """A hand-added key (e.g. host wiring) in the root manifest is drift for --check."""
    plugin = _plugin(tmp_path)
    data = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
    data["hooks"] = "./hooks.json"
    (plugin / "plugin.json").write_text(json.dumps(data), encoding="utf-8")
    assert _cli("--check", str(plugin)).returncode == 1


def test_syncagy_reordered_keys_check_passes(tmp_path):
    """Reordering keys is not a semantic change; --check stays clean (survived attempt)."""
    plugin = _plugin(tmp_path)
    data = json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))
    (plugin / "plugin.json").write_text(json.dumps(dict(reversed(list(data.items())))), encoding="utf-8")
    assert _cli("--check", str(plugin)).returncode == 0


def test_syncagy_type_changed_version_check_fails(tmp_path):
    """A version written as a number instead of a string is drift."""
    plugin = _plugin(tmp_path)
    (plugin / "plugin.json").write_text(
        json.dumps({"name": "loom-code", "version": 999, "description": "d"}), encoding="utf-8")
    assert _cli("--check", str(plugin)).returncode == 1


def test_syncagy_invalid_json_root_check_reports_drift_without_traceback(tmp_path):
    """A corrupt root manifest fails --check with a DRIFT line, not a Python traceback."""
    plugin = _plugin(tmp_path)
    (plugin / "plugin.json").write_text("{not json", encoding="utf-8")
    result = _cli("--check", str(plugin))
    assert result.returncode == 1
    assert "Traceback" not in result.stderr, result.stderr


def test_syncagy_invalid_json_root_sync_regenerates(tmp_path):
    """Plain sync repairs a corrupt root manifest instead of crashing on it."""
    plugin = _plugin(tmp_path)
    (plugin / "plugin.json").write_text("{not json", encoding="utf-8")
    result = _cli(str(plugin))
    assert result.returncode == 0, result.stderr
    assert json.loads((plugin / "plugin.json").read_text(encoding="utf-8"))["name"] == "loom-code"


def test_syncagy_missing_root_all_check_fails_single_plugin_passes(tmp_path):
    """--all --check requires the root manifest; single-plugin --check tolerates its absence."""
    for name in ("loom-code", "loom-design", "loom-workflow"):
        _plugin(tmp_path, name)
    (tmp_path / "loom-design" / "plugin.json").unlink()
    all_check = _cli("--all", "--check", "--repo-root", str(tmp_path))
    single = _cli("--check", str(tmp_path / "loom-design"))
    assert all_check.returncode == 1 and "MISSING" in all_check.stderr
    assert single.returncode == 0


def test_syncagy_root_manifest_as_directory_check_fails(tmp_path):
    """A directory squatting at <plugin>/plugin.json fails --check without a traceback."""
    plugin = _plugin(tmp_path)
    (plugin / "plugin.json").unlink()
    (plugin / "plugin.json").mkdir()
    result = _cli("--check", str(plugin))
    assert result.returncode != 0
    assert "Traceback" not in result.stderr, result.stderr


def _hook(file_path: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(["bash", str(HOOK)], input=json.dumps({"tool_input": {"file_path": str(file_path)}}),
                          capture_output=True, text=True)


def test_drifthook_root_manifest_hand_edit_blocks(tmp_path):
    """Editing the agy root manifest itself into drift is caught at edit time,
    as the hook message now promises for ``<plugin>/plugin.json``."""
    (tmp_path / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp_path / "scripts" / "sync_codex_manifests.py")
    plugin = _plugin(tmp_path, "myplugin")
    (plugin / "plugin.json").write_text(
        json.dumps({"name": "myplugin", "version": "0.0.1", "description": "d"}), encoding="utf-8")
    result = _hook(plugin / "plugin.json")
    assert result.returncode == 2, (result.returncode, result.stderr)


def test_drifthook_claude_side_edit_with_root_drift_blocks(tmp_path):
    """A Claude-manifest edit while the root manifest drifted blocks (survived attempt)."""
    (tmp_path / "scripts").mkdir()
    shutil.copy(SCRIPT, tmp_path / "scripts" / "sync_codex_manifests.py")
    plugin = _plugin(tmp_path, "myplugin")
    (plugin / "plugin.json").write_text(
        json.dumps({"name": "myplugin", "version": "0.0.1", "description": "d"}), encoding="utf-8")
    assert _hook(plugin / ".claude-plugin" / "plugin.json").returncode == 2
