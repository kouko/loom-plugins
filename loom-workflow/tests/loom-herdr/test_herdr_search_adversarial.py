# concern: herdr_search.py breaks on hostile input — snippet offsets drift after length-changing lowercase, one malformed transcript aborts history search, a negative --limit miscounts hits
"""Adversarial tests for herdr_search.py, graduated from the build's probes.

Each case caught a defect at 01e24486a and keeps guarding it:
- snippet extraction: `str.lower()` turns U+0130 into two code points, so an
  index found in lowered text drifted past the match in the original;
- --history: a record with no `cwd` and a non-object `payload` raised
  AttributeError and aborted the whole search;
- --limit: `-1` showed no hits then printed "(2 more hits)" for one hit.
"""

import json
import subprocess
import sys

from test_herdr_search import SCRIPT, _claude, _herdr_env, _pane, _write_jsonl


def test_snippet_dotted_capital(tmp_path):
    """A hit's snippet contains the matched query even after Turkish capitals."""
    home, env = _herdr_env(tmp_path, [_pane("w1:p1", "claude", "cid-1", "/a")])
    _claude(home, "cid-1", "/a", "İ" * 60 + " please deploy the widget")
    proc = subprocess.run(
        [sys.executable, "-B", str(SCRIPT), "deploy", "--json"],
        env=env, capture_output=True, text=True,
    )
    assert proc.returncode == 0, proc.stderr
    rows = json.loads(proc.stdout)
    assert len(rows) == 1
    assert "deploy" in rows[0]["snippet"].lower(), rows[0]["snippet"]


def test_history_malformed_record_unsearchable(tmp_path):
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


def test_limit_negative_rejected(tmp_path):
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
