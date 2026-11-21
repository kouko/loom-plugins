# concern: an out-of-range --limit is accepted and the overflow notice reports more hits than exist
"""Adversarial probe for herdr_search.py --limit.

`--limit -1` shows no hits and then prints "(2 more hits)" for a search that
has one hit, because the notice subtracts the raw negative limit.
"""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-workflow" / "tests" / "loom-herdr"))

from test_herdr_search import SCRIPT, _claude, _herdr_env, _pane  # noqa: E402


def test_limit_negative_rejected_or_counted(tmp_path):
    """A negative limit is rejected, or the overflow notice counts real hits."""
    home, env = _herdr_env(tmp_path, [_pane("w1:p1", "claude", "cid-1", "/a")])
    _claude(home, "cid-1", "/a", "deploy once")
    proc = subprocess.run(
        [sys.executable, "-B", str(SCRIPT), "deploy", "--limit", "-1"],
        env=env, capture_output=True, text=True,
    )
    if proc.returncode == 0:
        assert "(2 more hits" not in proc.stdout, proc.stdout
    else:
        assert "limit" in proc.stderr.lower(), proc.stderr
