# concern: AGENTS.md SSOT claims diverge from scripts/sync_codex_manifests.py constants
"""Adversarial probe: the AGENTS.md SSOT line must match what the sync script actually does.

Pins each path named in AGENTS.md against the script's own constants (CLAUDE_MANIFEST,
CODEX_MANIFEST, AGY_MANIFEST) and runs `scripts/sync_codex_manifests.py --check --all`
against a clean tree so hand-drifted derived manifests fail here.

Mutation probe: hand-editing a derived manifest out of sync with the SSOT turns RED.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
SCRIPT = REPO / "scripts" / "sync_codex_manifests.py"


def test_ssot_paths_match_sync_script_constants() -> None:
    """Every manifest path AGENTS.md names must be produced from the script constants."""
    script = SCRIPT.read_text(encoding="utf-8")
    assert 'CLAUDE_MANIFEST = (".claude-plugin", "plugin.json")' in script, (
        "sync script CLAUDE_MANIFEST constant changed; AGENTS.md may now name stale paths"
    )
    assert 'CODEX_MANIFEST = (".codex-plugin", "plugin.json")' in script
    assert 'AGY_MANIFEST = ("plugin.json",)' in script

    agents = (REPO / "AGENTS.md").read_text(encoding="utf-8")
    assert "loom-code/.claude-plugin/plugin.json" in agents
    assert "loom-code/.codex-plugin/plugin.json" in agents
    assert "loom-code/plugin.json" in agents
    assert "loom-code/package.json" in agents


def test_sync_check_all_passes_on_clean_tree() -> None:
    """`scripts/sync_codex_manifests.py --check --all` must exit 0."""
    proc = subprocess.run(
        [sys.executable, str(SCRIPT), "--check", "--all"],
        cwd=REPO,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, (
        "manifest sync check failed:\n"
        f"stdout:\n{proc.stdout}\nstderr:\n{proc.stderr}"
    )
