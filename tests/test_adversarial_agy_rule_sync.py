"""Adversarial probes for the agy plugin rule generation in
`sync_codex_manifests.py` (`AGY_RULE_SOURCES` -> `<plugin>/rules/AGENTS.md`).

Fixtures are built under tmp_path; the committed tree is never written.
Probes that expose a defect FAIL; the rest stay as regressions.
"""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

import sync_codex_manifests as m

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sync_codex_manifests.py"
REPO_ROOT = Path(__file__).resolve().parents[1]
CARD_REL = ("skills", "loom-visualization", "assets", "trigger-card.md")
CARD_TEXT = "# Card (probe)\nInvoke `loom-visualization` FIRST.\n"


def _plugin(tmp_path: Path, name: str = "loom-workflow") -> Path:
    """A plugin dir copied from the committed manifests plus a fixture card."""
    src = REPO_ROOT / "loom-workflow"
    plugin = tmp_path / name
    for sub in (".claude-plugin", ".codex-plugin"):
        shutil.copytree(src / sub, plugin / sub)
    card = plugin.joinpath(*CARD_REL)
    card.parent.mkdir(parents=True)
    card.write_text(CARD_TEXT, encoding="utf-8")
    return plugin


def _run(argv, cwd=None):
    return subprocess.run(
        [sys.executable, str(SCRIPT), *argv], capture_output=True, text=True, cwd=cwd
    )


def _rule(plugin: Path) -> Path:
    return plugin / "rules" / "AGENTS.md"


@pytest.mark.parametrize(
    "mutate",
    [
        lambda t: t.replace("<!-- Generated", "<!-- generated", 1),
        lambda t: t.rstrip("\n"),
        lambda t: t + "\n",
        lambda t: t.split("\n", 1)[1],
        lambda t: "﻿" + t,
    ],
    ids=["header-case", "no-final-nl", "extra-nl", "no-header", "bom"],
)
def test_agy_rule_check_mutated_rule_reports_drift(tmp_path, mutate):
    plugin = _plugin(tmp_path)
    assert _run([str(plugin)]).returncode == 0
    rule = _rule(plugin)
    rule.write_text(mutate(rule.read_text(encoding="utf-8")), encoding="utf-8")
    proc = _run(["--check", str(plugin)])
    assert proc.returncode != 0 and "DRIFT" in proc.stderr, proc.stderr


def test_agy_rule_sync_second_run_idempotent(tmp_path):
    plugin = _plugin(tmp_path)
    assert _run([str(plugin)]).returncode == 0
    first = _rule(plugin).stat().st_mtime_ns
    body = _rule(plugin).read_bytes()
    assert _run([str(plugin)]).returncode == 0
    assert _rule(plugin).stat().st_mtime_ns == first
    assert _rule(plugin).read_bytes() == body
    assert _run(["--check", str(plugin)]).returncode == 0


def test_agy_rule_crlf_card_generates_stable_rule(tmp_path):
    """A CRLF card (Windows checkout) reads back normalised; sync then check is
    clean and a rerun does not flap."""
    plugin = _plugin(tmp_path)
    plugin.joinpath(*CARD_REL).write_bytes(CARD_TEXT.replace("\n", "\r\n").encode())
    assert _run([str(plugin)]).returncode == 0
    assert _run(["--check", str(plugin)]).returncode == 0
    assert _run([str(plugin)]).returncode == 0
    assert _run(["--check", str(plugin)]).returncode == 0


def test_agy_rule_non_utf8_rule_reports_drift_then_sync_repairs(tmp_path):
    plugin = _plugin(tmp_path)
    _rule(plugin).parent.mkdir()
    _rule(plugin).write_bytes(b"\xff\xfe\x00garbage")
    proc = _run(["--check", str(plugin)])
    assert proc.returncode != 0 and "Traceback" not in proc.stderr, proc.stderr
    assert _run([str(plugin)]).returncode == 0
    assert _run(["--check", str(plugin)]).returncode == 0


def test_agy_rule_orphan_rule_sync_then_check_clean(tmp_path):
    """The DRIFT message for a leftover rule (card deleted) tells the user to
    run the sync command; running it must clear the drift, or the CI gate
    stays red with a remediation that does nothing."""
    plugin = _plugin(tmp_path)
    assert _run([str(plugin)]).returncode == 0
    plugin.joinpath(*CARD_REL).unlink()
    drift = _run(["--check", str(plugin)])
    assert drift.returncode != 0 and "Run: python3" in drift.stderr, drift.stderr
    assert _run([str(plugin)]).returncode == 0
    after = _run(["--check", str(plugin)])
    assert after.returncode == 0, after.stderr


def test_agy_rule_rule_path_is_directory_fails_cleanly(tmp_path):
    """`rules/AGENTS.md` is a directory: check reports it, sync fails without
    a traceback (the engine's own tests hold MISSING paths to that bar)."""
    plugin = _plugin(tmp_path)
    _rule(plugin).mkdir(parents=True)
    check = _run(["--check", str(plugin)])
    assert check.returncode != 0 and "Traceback" not in check.stderr, check.stderr
    sync = _run([str(plugin)])
    assert "Traceback" not in sync.stderr, sync.stderr


def test_agy_rule_all_check_and_single_check_agree_on_drift(tmp_path):
    for name in m.CODEX_ELIGIBLE:
        src = REPO_ROOT / name
        for sub in (".claude-plugin", ".codex-plugin"):
            shutil.copytree(src / sub, tmp_path / name / sub)
        if (src / "plugin.json").exists():
            shutil.copy(src / "plugin.json", tmp_path / name / "plugin.json")
    card = (tmp_path / "loom-workflow").joinpath(*CARD_REL)
    card.parent.mkdir(parents=True)
    card.write_text(CARD_TEXT, encoding="utf-8")
    assert _run(["--all", "--repo-root", str(tmp_path)]).returncode == 0
    assert _run(["--all", "--check", "--repo-root", str(tmp_path)]).returncode == 0
    _rule(tmp_path / "loom-workflow").write_text("tampered\n", encoding="utf-8")
    single = _run(["--check", str(tmp_path / "loom-workflow")])
    every = _run(["--all", "--check", "--repo-root", str(tmp_path)])
    assert single.returncode != 0 and every.returncode != 0
    assert "DRIFT" in single.stderr and "DRIFT" in every.stderr


def test_agy_rule_relative_plugin_arg_from_plugin_cwd_resolves(tmp_path):
    """`.` as the plugin, run from inside the plugin, still maps to the rule."""
    plugin = _plugin(tmp_path)
    assert _run(["."], cwd=plugin).returncode == 0
    assert _rule(plugin).is_file()
    _rule(plugin).write_text("tampered\n", encoding="utf-8")
    assert _run(["--check", "."], cwd=plugin).returncode != 0


def test_agy_rule_sync_preserves_codex_hooks_key(tmp_path):
    """Sync with a stale shared field keeps the Codex-only `hooks` pointer."""
    plugin = _plugin(tmp_path)
    codex_path = plugin / ".codex-plugin" / "plugin.json"
    codex = json.loads(codex_path.read_text(encoding="utf-8"))
    assert codex["hooks"] == "./hooks/hooks-codex.json"
    codex["version"] = "0.0.0-stale"
    codex_path.write_text(json.dumps(codex), encoding="utf-8")
    assert _run([str(plugin)]).returncode == 0
    synced = json.loads(codex_path.read_text(encoding="utf-8"))
    assert synced["hooks"] == "./hooks/hooks-codex.json"
    assert synced["version"] != "0.0.0-stale"
    assert _run(["--check", str(plugin)]).returncode == 0
