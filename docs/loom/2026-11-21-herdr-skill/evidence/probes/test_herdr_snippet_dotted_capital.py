# concern: case-insensitive snippet offsets computed on lowered text drift when lowering changes string length
"""Adversarial probe for herdr_search.py snippet extraction.

`str.lower()` turns U+0130 (Turkish dotted capital I) into two code points,
so an index found in the lowered text points past the match in the original
text. With enough such characters before the match, the reported snippet no
longer contains the query at all.
"""

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(REPO / "loom-workflow" / "tests" / "loom-herdr"))

from test_herdr_search import SCRIPT, _claude, _herdr_env, _pane  # noqa: E402


def test_snippet_dotted_capital_prefix_contains_query(tmp_path):
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
