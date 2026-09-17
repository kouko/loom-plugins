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


def local_link_paths(text, base):
    """Resolved filesystem paths of every local inline or reference link."""
    raw = re.findall(r"\]\(\s*(<[^>]*>|[^)\s]+)", text)
    raw += re.findall(r"^ {0,3}\[[^\]]+\]:\s*(<[^>]*>|\S+)", text, re.MULTILINE)
    targets = [t[1:-1] if t.startswith("<") else t for t in raw]
    paths = []
    for target in targets:
        if "://" in target or target.startswith("#"):
            continue
        paths.append((target, (base / target.split("#")[0]).resolve()))
    return paths


def broken_links(text, base):
    return [t for t, p in local_link_paths(text, base) if not p.exists()]


def test_helper_catches_broken_reference_link(tmp_path):
    text = "See [x][ref].\n\n[ref]: missing/\n"
    assert broken_links(text, tmp_path) == ["missing/"]


def test_helper_accepts_angle_bracket_link_with_title(tmp_path):
    (tmp_path / "plans").mkdir()
    text = '[plans/](<plans/> "title")\n'
    assert broken_links(text, tmp_path) == []


def test_a2_all_links_resolve():
    assert broken_links(TEXT, README.parent) == []


def test_a2_maps_link_absent():
    maps = (README.parent / "maps").resolve()
    assert all(p != maps for _, p in local_link_paths(TEXT, README.parent))


def test_a3_maps_path_still_named_and_row_kept():
    rows = [l for l in TEXT.splitlines() if l.startswith("| `maps/`") or l.startswith("| [`maps/`]")]
    assert len(rows) == 1
    assert "Persistent decision maps" in rows[0]
