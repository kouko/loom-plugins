"""Adversarial probe: the frozen-store list keeps every store that still exists.

Guards against over-deletion: docs/loom/plans/ must stay listed, and any
store from the pre-change list that exists on disk must still be linked.
Run from the repository root: python3 <this file>. Exit 1 on failure.
"""
import sys
from pathlib import Path

ROOT = Path.cwd()
BASE = ROOT / "docs/loom"
ORIGINAL_ENTRIES = ["plans/", "specs/", "backlog/", "BACKLOG.md", "design/", "archive/",
                    "2026-07-12-us-sec-primary-source-layer/",
                    "2026-07-19-8k-prose-kpi-intake/"]


def frozen_section():
    text = (BASE / "README.md").read_text(encoding="utf-8")
    start = text.index("These are the pre-1.0 stores.")
    return text[start:text.index("\n## ", start)]


def test_frozen_store_list_existing_stores_still_listed():
    """plans/ and every original entry that exists on disk remain linked."""
    section = frozen_section()
    missing = [e for e in ORIGINAL_ENTRIES
               if (BASE / e).exists() and f"]({e})" not in section]
    if f"](plans/)" not in section:
        missing.append("plans/ (required)")
    assert not missing, missing


if __name__ == "__main__":
    try:
        test_frozen_store_list_existing_stores_still_listed()
    except AssertionError as exc:
        print("RED unlisted existing stores:", exc)
        sys.exit(1)
    print("GREEN")
