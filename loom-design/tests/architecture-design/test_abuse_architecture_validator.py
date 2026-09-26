# concern: the ARCHITECTURE.md validator reports OK for files the schema forbids
"""Adversary probes for validate_architecture_output.py.

The schema (architecture-md-schema.md) says guard paths are relative to the
repository root, the four rule sections come in a fixed order after
`## Decisions`, and the validator checks all of that. Each case feeds a file
that breaks one of those promises and expects the validator to reject it.
"""
from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "loom-design" / "scripts" / "architecture-design"))

from validate_architecture_output import validate  # noqa: E402

_HEAD = "# Architecture\nratified-by: Alex Rivera 2026-09-25\n\n"
_BODY = """\
## Decisions
- D-1 — layer-first folders — options: layer-first, feature-first — reason: small app

## Module boundaries
- MB-1 — ui/ never imports db/ — check: {guard}

## File placement
- FP-1 — tests live under tests/ — check: review

## File size
- FS-1 — no source file over 400 lines — check: review

## CI stages
- CI-1 — lint runs before the test suite — check: review
"""


def _write(root: Path, text: str) -> Path:
    repo = root / "repo"
    repo.mkdir()
    path = repo / "ARCHITECTURE.md"
    path.write_text(text, encoding="utf-8")
    return path


def test_guardpath_outsiderepo_rejected(tmp_path):
    """A guard outside the repository (absolute or ../) is not a repo-relative guard."""
    for name in ("absolute", "dotdot"):
        root = tmp_path / name
        root.mkdir()
        outside = root / "outside_guard.py"
        outside.write_text("", encoding="utf-8")
        guard = str(outside) if name == "absolute" else "../outside_guard.py"
        ok, problems = validate(_write(root, _HEAD + _BODY.format(guard=guard)))
        assert not ok, f"guard {guard!r} outside the repository was accepted"


def test_rulesection_duplicated_rejected(tmp_path):
    """A second copy of a rule section must not hide the first copy's broken lines."""
    text = _HEAD + _BODY.format(guard="review") + (
        "\n## File size\n- FS-2 — modules stay small — check: review\n"
    )
    text = text.replace("- FS-1 — no source file over 400 lines — check: review",
                        "- files stay small")
    ok, problems = validate(_write(tmp_path, text))
    assert not ok, "a malformed rule line in a duplicated section was accepted"


def test_sections_outoforder_rejected(tmp_path):
    """The schema fixes Decisions first, then the four rule sections in order."""
    body = _BODY.format(guard="review")
    decisions, rules = body.split("\n\n## Module boundaries", 1)
    text = _HEAD + "## Module boundaries" + rules + "\n" + decisions + "\n"
    ok, problems = validate(_write(tmp_path, text))
    assert not ok, "Decisions after the rule sections was accepted"
