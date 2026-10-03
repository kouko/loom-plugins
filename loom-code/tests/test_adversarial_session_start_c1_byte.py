# concern: a non-UTF-8 control byte pasted into KICKOFF-DEFAULTS.md silences the whole session-start hook
"""Adversarial probe: a Latin-1 C1 control byte (0x85, NEL) in a defaults line.

Text pasted from a Latin-1 or Windows-1252 source carries C1 control bytes that
are not valid UTF-8. Under a UTF-8 locale `sed` aborts on them and `set -e`
kills the hook with no output; under the C locale the raw byte reaches the
JSON and makes it undecodable. Either way the session gets none of loom's
guidance, which is the failure the change set out to remove.
"""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
HOOK = REPO / "loom-code" / "hooks" / "session-start"


@pytest.mark.parametrize("locale", ["C", "en_US.UTF-8"])
def test_session_start_c1_control_byte_emits_valid_json(tmp_path, locale):
    """The hook exits 0 and prints strict UTF-8 JSON carrying the station order and the other defaults line."""
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    loom = tmp_path / "docs" / "loom"
    loom.mkdir(parents=True)
    (loom / "KICKOFF-DEFAULTS.md").write_bytes(
        b"# KICKOFF-DEFAULTS\n\n- second-vendor: codex\x85 pasted (2026-09-02)\n"
        b"- standing-docs: waived (2026-09-02)\n"
    )
    env = dict(os.environ, LC_ALL=locale, LANG=locale)
    proc = subprocess.run(["bash", str(HOOK)], cwd=tmp_path, env=env,
                          stdin=subprocess.DEVNULL, capture_output=True)
    assert proc.returncode == 0, proc.stderr.decode("utf-8", "replace")
    context = json.loads(proc.stdout.decode("utf-8"))["hookSpecificOutput"]["additionalContext"]
    assert "Station order:" in context
    assert "standing-docs: waived (2026-09-02)" in context
