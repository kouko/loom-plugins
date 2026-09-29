"""loom-design's copies of loom-code's contract templates stay identical.

loom-design skills read local copies instead of loom-code's files, so a copy
and its original must change together; this test fails when one side moves.
"""
from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

REPO = Path(__file__).resolve().parents[1]
TEMPLATES = REPO / "loom-code" / "contract" / "templates"
DESIGN = REPO / "loom-design" / "skills"
PAIRS = [
    (DESIGN / "capture-intent" / "templates" / name, TEMPLATES / name)
    for name in ("intent.md", "PRINCIPLES-interview.md", "KICKOFF-DEFAULTS.md")
] + [(DESIGN / "write-spec" / "templates" / "spec-minimal.md", TEMPLATES / "spec-minimal.md")]


@pytest.mark.parametrize("copy, original", PAIRS, ids=lambda p: str(p.relative_to(REPO)))
def test_copy_matches_original(copy: Path, original: Path) -> None:
    assert copy.read_bytes() == original.read_bytes()


def test_inlined_requirement_grammar_matches_manifest() -> None:
    manifest = yaml.safe_load((REPO / "loom-code" / "contract" / "manifest.yaml").read_text(encoding="utf-8"))
    fields = manifest["artifacts"]["spec"]["fields"]
    expected = next(f["grammar"] for f in fields if f["name"] == "Requirements")
    forms = (DESIGN / "write-spec" / "references" / "spec-forms.md").read_text(encoding="utf-8")
    inlined = re.search(r"^Grammar: `([^`]+)`$", forms, re.MULTILINE)
    assert inlined is not None and inlined.group(1) == expected
