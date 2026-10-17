"""Adversary probe for 2026-10-17-codex-model-list-discovery.

concern: a discovery timeout that never fires when the codex app-server
leaves a descendant process holding its stdout pipe open.
"""
from __future__ import annotations

import os
import stat
import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parents[5] / "loom-code" / "scripts"

DRIVER = """
import os, subprocess, sys
sys.path.insert(0, sys.argv[1])
import external_review as er
er.CODEX_DISCOVERY_TIMEOUT = 2
try:
    er._codex_candidates(subprocess.run, os.getcwd())
except subprocess.TimeoutExpired:
    print("timeout-raised")
"""


def test_codex_app_server_descendant_holds_stdout_times_out(tmp_path):
    """A codex whose child keeps stdout open must still time out promptly."""
    fake = tmp_path / "bin" / "codex"
    fake.parent.mkdir()
    fake.write_text("#!/bin/sh\nsleep 30 &\nsleep 30\n")
    fake.chmod(fake.stat().st_mode | stat.S_IEXEC)
    env = dict(os.environ, PATH=f"{fake.parent}{os.pathsep}{os.environ['PATH']}")
    try:
        out = subprocess.run([sys.executable, "-c", DRIVER, str(SCRIPTS)],
                             env=env, cwd=tmp_path, capture_output=True,
                             text=True, timeout=10)
    except subprocess.TimeoutExpired:
        raise AssertionError("discovery hung past its 2s timeout")
    assert "timeout-raised" in out.stdout
