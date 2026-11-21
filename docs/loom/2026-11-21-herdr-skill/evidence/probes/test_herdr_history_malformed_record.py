# concern: one malformed transcript record crashes the whole history search instead of degrading to unsearchable
"""Adversarial probe for herdr_search.py --history.

A JSONL record with no `cwd` and a non-object `payload` raises
AttributeError in `jsonl_texts`, which only OSError is caught around, so a
single bad local file aborts the search and loses every other hit.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-workflow" / "tests" / "loom-herdr"))

from test_herdr_search import SCRIPT, _claude, _herdr_env, _write_jsonl  # noqa: E402


def test_history_malformed_record_keeps_other_hits(tmp_path):
    """A malformed transcript does not stop hits from other transcripts."""
    home, env = _herdr_env(tmp_path, [])
    _claude(home, "good-session", "/a", "deploy notes")
    _write_jsonl(home / ".claude" / "projects" / "-p" / "bad-session.jsonl",
                 [{"type": "user", "payload": "not-an-object"}])
    proc = subprocess.run(
        [sys.executable, "-B", str(SCRIPT), "deploy", "--history", "--json"],
        env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)
    assert any("deploy notes" in r["snippet"] for r in rows)
