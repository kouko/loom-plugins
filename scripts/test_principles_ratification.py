"""W1-01 — PRINCIPLES.md records kouko's 2026-09-15 signature of the
non-negotiable 2 user-skipped-steps amendment, and no longer carries a
`pending-ratification:` line.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PRINCIPLES = REPO / "PRINCIPLES.md"

AMENDMENT = "non-negotiable 2 user-skipped-steps amendment ratified by kouko 2026-09-15"


def _lines() -> list[str]:
    return PRINCIPLES.read_text(encoding="utf-8").splitlines()


def test_ratified_by_names_2026_09_15_non_negotiable_2_amendment() -> None:
    ratified = [line for line in _lines() if line.startswith("ratified-by:")]
    assert len(ratified) == 1
    assert ratified[0].endswith("; " + AMENDMENT)


PENDING_RE = re.compile(r"^\s*pending[\s_-]*ratification\s*:", re.I | re.M)


def test_pending_ratification_line_absent() -> None:
    assert not PENDING_RE.search(PRINCIPLES.read_text(encoding="utf-8"))
