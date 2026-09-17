"""A1-A3 checks for change 2026-09-17-loom-readme-small-fixes."""
import re
from pathlib import Path

README = Path(__file__).resolve().parents[2] / "README.md"
TEXT = README.read_text(encoding="utf-8")
FLAT = re.sub(r"\s+", " ", TEXT)


def test_a1_plans_named_as_subject():
    after = FLAT.split("survive only in git history.", 1)[1].lstrip()
    assert after.startswith("The old plans stay in")


def test_a1_bare_they_absent():
    assert "They stay in" not in FLAT


def test_a2_all_links_resolve():
    for target in re.findall(r"\]\(([^)]+)\)", TEXT):
        if "://" in target or target.startswith("#"):
            continue
        path = (README.parent / target.split("#")[0]).resolve()
        assert path.exists(), target


def test_a2_maps_link_absent():
    assert "](maps/)" not in TEXT


def test_a3_maps_path_still_named_and_row_kept():
    rows = [l for l in TEXT.splitlines() if l.startswith("| `maps/`") or l.startswith("| [`maps/`]")]
    assert len(rows) == 1
    assert "Persistent decision maps" in rows[0]
