"""W1-01 — PRINCIPLES.md carries exactly one `ratified-by:` line and no
`pending-ratification:` line.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PRINCIPLES = REPO / "PRINCIPLES.md"


def _lines() -> list[str]:
    return PRINCIPLES.read_text(encoding="utf-8").splitlines()


def test_exactly_one_ratified_by_line() -> None:
    ratified = [line for line in _lines() if line.startswith("ratified-by:")]
    assert len(ratified) == 1


PENDING_RE = re.compile(r"^\s*pending[\s_-]*ratification\s*:", re.I | re.M)


def test_pending_ratification_line_absent() -> None:
    assert not PENDING_RE.search(PRINCIPLES.read_text(encoding="utf-8"))
