# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Drift-check tests (consolidated from test_checks_{seam,table,kink}.py)."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "skills" / "loom-visualization" / "scripts"))

from checks_seam import find_issues as seam_find_issues
from checks_table import find_issues as table_find_issues
from checks_kink import find_issues as kink_find_issues


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_checks_seam.py
# ---------------------------------------------------------------------------

# Inline fixtures (self-contained; no /tmp dependency, no nested fixtures/ dir).
# DRIFTED: boxes sized by char-count, so CJK content rows overflow their borders.
DRIFTED = """\
┌──────┐
│ 開始 │
└──┬───┘
   │
   ▼
┌────────┐
│ 驗證ユーザー │
└───┬────┘
    │
    ▼
┌──────────┐
│ 權限足夠? │
└──┬────┬──┘
 是 │    │ 否
   ▼    ▼
┌────────┐ ┌────────┐
│ 載入畫面 │ │ 顯示エラー │
└────────┘ └────────┘"""

# CLEAN: boxes sized by display-width; every vertical seam connects.
CLEAN = """\
     ┌──────┐
     │ 開始 │
     └───┬──┘
         │
         ▼
┌──────────────────┐
│ 驗證ユーザー身分 │
└─────────┬────────┘
          │
          ▼
   ┌────────────┐
   │ 權限足夠?  │
   └───┬────┬───┘
       │    │
      是    否
       ▼    ▼
┌────────────┐ ┌──────────────┐
│ 載入畫面   │ │ 顯示エラー   │
└────────────┘ └──────────────┘"""


def test_drifted_fixture_has_violations():
    issues = seam_find_issues(DRIFTED.splitlines())
    assert len(issues) >= 1


def test_clean_fixture_has_no_violations():
    issues = seam_find_issues(CLEAN.splitlines())
    assert issues == []


def test_seam_issue_tuple_shape():
    issues = seam_find_issues(DRIFTED.splitlines())
    ln, col, msg = issues[0]
    assert isinstance(ln, int) and ln >= 1
    assert isinstance(col, int) and col >= 0
    assert isinstance(msg, str) and msg


# Double-line box, width-correct (interior ' 中文 ' = 6 display cells -> 6 ═).
DOUBLE_CLEAN = """\
╔══════╗
║ 中文 ║
╚══════╝"""

# Same double box but the content row is sized by char-count (6 CJK+space chars
# vs 6-cell border) -> the right ║ lands at a column no border reaches.
DOUBLE_CORRUPTED = """\
╔══════╗
║ 中文字測試 ║
╚══════╝"""

# Rounded box, width-correct (interior ' 中文 ' = 6 display cells -> 6 ─).
ROUNDED_CLEAN = """\
╭──────╮
│ 中文 │
╰──────╯"""


def test_double_line_box_clean():
    assert seam_find_issues(DOUBLE_CLEAN.splitlines()) == []


def test_double_line_box_corrupted_caught():
    issues = seam_find_issues(DOUBLE_CORRUPTED.splitlines())
    assert len(issues) >= 1


def test_rounded_box_clean():
    assert seam_find_issues(ROUNDED_CLEAN.splitlines()) == []


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_checks_table.py
# Contract tests for the table-block equal-width check.
#
# A "table block" is a maximal run of consecutive lines that each start
# and end with a box vertical (│ as the first and last non-space glyph),
# optionally bracketed by ┌─┐ / ├─┤ / └─┘ border lines. find_issues flags
# any line in a block whose display_width differs from the block's
# modal/border display_width — the classic mistake of sizing a CJK table
# by character count instead of terminal-cell width.
# ---------------------------------------------------------------------------

def test_cjk_row_sized_by_char_count_is_flagged():
    # Borders + first row are display-width 12. The second content row was
    # sized to the SAME character count (4 interior chars) but those chars
    # are CJK (2 cells each) vs ASCII, so its display width is wider.
    #   "│中文ab│" -> 1 + 2 + 2 + 1 + 1 + 1 = 8 display cells
    #   "│中文中文│" -> 1 + 2 + 2 + 2 + 2 + 1 = 10 display cells
    # Both have 6 characters, so a naive char-count check sees them as
    # aligned; a display-width check catches the mismatch.
    lines = [
        "┌──────┐",     # top border, width 8
        "│中文ab│",     # width 8
        "│中文中文│",   # width 10 -- wider than the block
        "└──────┘",     # bottom border, width 8
    ]
    issues = table_find_issues(lines)
    assert len(issues) >= 1
    flagged_line_numbers = {ln for ln, _col, _msg in issues}
    assert 3 in flagged_line_numbers


def test_display_width_aligned_table_has_no_issues():
    # Every line is display-width 8: borders, an ASCII row, and a CJK row
    # whose two wide chars + spacing land on the same terminal width.
    #   "│ ab  │" -> 1+1+1+1+2+1 = wait, build explicitly below.
    # Interior is 6 cells wide on every line.
    lines = [
        "┌──────┐",     # 1 + 6 + 1 = 8
        "│ abcd │",     # 1 + 6 + 1 = 8
        "│ 中文 │",     # 1 + 1 + 2 + 2 + 1 + 1 = 8
        "└──────┘",     # 8
    ]
    assert table_find_issues(lines) == []


def test_branching_flowchart_is_not_a_table():
    # A decision box whose bottom border forks into two branch stubs.
    # The box content │ sit at display-cols 3 and 16; the branch stub
    # "│    │"'s │ sit at cols 7 and 12 -- a DIFFERENT left/right frame.
    # A flowchart is not a table, so the stub must not be flagged as a
    # too-narrow table row.
    lines = [
        "   ┌────────────┐",
        "   │ 權限足夠?  │",
        "   └───┬────┬───┘",
        "       │    │",
        "      是    否",
        "       ▼    ▼",
    ]
    assert table_find_issues(lines) == []


def test_lone_single_box_is_not_a_table():
    # One box: top border + one content row + bottom border. A single box
    # is not a table (no second data row sharing the frame), so nothing is
    # flagged even though this row's display width (10) exceeds the border
    # width (8) -- a single mislabelled box is a diagram element, not a
    # too-wide table row.
    lines = [
        "┌──────┐",     # width 8
        "│中文中文│",   # width 10 -- wider than the border
        "└──────┘",     # width 8
    ]
    assert table_find_issues(lines) == []


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_checks_kink.py
# ---------------------------------------------------------------------------

# --- Fixtures -------------------------------------------------------------
# Display columns are 0-based. Box-drawing glyphs are 1 cell wide (width.py).

# Off-by-one connector kink: the box's ┬ sits at col 9, but the trunk │
# directly below it drifts to col 10 with no junction glyph to justify it.
#                  0123456789012
KINK_SEAM = [
    "┌───────┐",        # box top
    "│  box  │",
    "└───┬───┘",        # ┬ at col 4 (exit point)
    "    │",            # │ at col 4 — straight so far
    "     │",           # │ drifts to col 5 — KINK, no junction
]

# Straight vertical seam: connector column is stable across the run.
STRAIGHT_SEAM = [
    "┌───────┐",
    "│  box  │",
    "└───┬───┘",        # ┬ at col 4
    "    │",            # │ at col 4
    "    │",            # │ at col 4
    "    ▼",            # ▼ at col 4
]

# Justified bend: the column shift is explained by a corner junction glyph,
# so it must NOT be flagged as a kink.
JUSTIFIED_BEND = [
    "    │",            # │ at col 4
    "    └──┐",         # └ at col 4 (junction justifies the turn)
    "       │",         # │ at col 7 — shift justified by the corner above
]

# Arrowhead landing inside the target box's horizontal span (cols 8..16).
ARROW_INTO_BOX = [
    "        │",        # │ at col 8
    "        ▼",        # ▼ at col 8
    "┌───────────────┐",  # box spans cols 0..16 — 8 is inside
    "│     target    │",
    "└───────────────┘",
]

# Arrowhead pointing OUTSIDE the target box's horizontal span.
ARROW_MISSES_BOX = [
    "                      │",   # │ at col 22
    "                      ▼",   # ▼ at col 22 — to the right of the box
    "┌───────────────┐",         # box spans cols 0..16 — 22 is outside
    "│     target    │",
    "└───────────────┘",
]

# Display-width-aligned nested box: the outer │ at each side terminates at a
# corner on the line below, and inner boxes sit fully inside. No connector
# bends, so there must be no kink flagged.
NESTED_BOX = [
    "┌────────────────────┐",
    "│  データ層          │",
    "│  ┌────┐  ┌────┐    │",
    "│  │ PG │  │RDS │    │",
    "│  └────┘  └────┘    │",
    "└────────────────────┘",
]

# Two boxes side by side on one row: each │ terminates at a corner directly
# below it. No seam bends, so there must be no kink flagged.
TWO_SIDE_BY_SIDE_BOXES = [
    "┌──┐ ┌──┐",
    "│a │ │b │",
    "└──┘ └──┘",
]

# Correctly-aligned ROUNDED box. ╭╮╰╯ are corners (junctions): each │ side
# terminates at a rounded corner directly below. No bend, no kink flagged.
ROUNDED_BOX = [
    "╭──────╮",
    "│ 中文 │",
    "╰──────╯",
]

# Correctly-aligned HEAVY box. ┏┓┗┛ are corners; ┃ is a vertical connector.
# Width-correct, so each ┃ side terminates at a heavy corner directly below.
HEAVY_BOX = [
    "┏━━━━┓",
    "┃ 中 ┃",
    "┗━━━━┛",
]

# Corrupted DOUBLE-line box: a double-line trunk ║ exits via a ╦ tee, runs
# straight one line, then drifts one column with no junction to justify it —
# the off-by-one kink mirror of KINK_SEAM but built from double-line glyphs.
# Proves ║ is now actually checked as a vertical connector (it was skipped —
# silently clean — before the glyphs.py taxonomy refactor).
DOUBLE_BOX_CORRUPTED = [
    "╔═══╗",
    "║ X ║",
    "╚═╦═╝",            # ╦ tee at col 2 (exit point)
    "  ║",              # ║ at col 2 — straight so far
    "   ║",             # ║ drifts to col 3 — KINK, no junction
]


# --- Seam-straightness tests ---------------------------------------------


def test_off_by_one_kink_flagged():
    issues = kink_find_issues(KINK_SEAM)
    assert len(issues) >= 1


def test_straight_seam_clean():
    assert kink_find_issues(STRAIGHT_SEAM) == []


def test_justified_bend_not_flagged():
    assert kink_find_issues(JUSTIFIED_BEND) == []


def test_nested_box_no_false_kink():
    assert kink_find_issues(NESTED_BOX) == []


def test_two_side_by_side_boxes_no_false_kink():
    assert kink_find_issues(TWO_SIDE_BY_SIDE_BOXES) == []


def test_rounded_box_no_false_kink():
    assert kink_find_issues(ROUNDED_BOX) == []


def test_heavy_box_no_false_kink():
    assert kink_find_issues(HEAVY_BOX) == []


def test_double_box_corrupted_is_caught():
    assert kink_find_issues(DOUBLE_BOX_CORRUPTED) != []


# --- Arrowhead-into-box tests --------------------------------------------


def test_arrow_into_box_clean():
    assert kink_find_issues(ARROW_INTO_BOX) == []


def test_arrow_missing_box_flagged():
    issues = kink_find_issues(ARROW_MISSES_BOX)
    assert len(issues) >= 1


# --- Contract shape ------------------------------------------------------


def test_kink_issue_tuple_shape():
    issues = kink_find_issues(KINK_SEAM)
    ln, col, msg = issues[0]
    assert isinstance(ln, int) and ln >= 1
    assert isinstance(col, int) and col >= 0
    assert isinstance(msg, str) and msg
