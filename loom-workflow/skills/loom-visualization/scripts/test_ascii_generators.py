# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Generator tests (consolidated from test_gen_{table,flow,tree,bar,arch,seq}.py)."""

import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from align import analyze
from width import display_width, split_lines

from gen_arch import render_arch
from gen_bar import render_bar
from gen_flow import render_flow
from gen_seq import render_seq
from gen_table import render_table
from gen_tree import render_tree


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_gen_table.py
# Contract tests for the CJK-aligned table generator.
#
# Alignment correctness is verified by display_width, not len: every
# rendered line MUST occupy the same number of terminal cells so that
# CJK/JP/EN-mixed cells line up in a monospace terminal.
# ---------------------------------------------------------------------------

_BOX_CHARS = set("┌┬┐│├┼┤└┴┘─")


def test_mixed_cjk_jp_en_table_lines_share_one_display_width():
    headers = ["項目", "狀態", "數量"]
    rows = [["使用者ログイン", "完了", "123"]]

    out = render_table(headers, rows)
    lines = out.splitlines()

    widths = {display_width(line) for line in lines}
    # WHY: a single shared cell-width across every line is the only
    # observable proof that CJK/JP cells were padded by display width
    # (not byte/char len) — len-based padding would make wide-char
    # lines come up short and the columns would skew.
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"


def test_gen_table_multiline_cell_stays_aligned():
    # One CJK cell spans 2 physical lines; its neighbor is single-line.
    headers = ["項目", "說明"]
    rows = [["使用者", "登入\n登出"]]

    out = render_table(headers, rows)
    lines = out.splitlines()

    # WHY: a 2-line cell must make its whole row 2 physical lines tall, so
    # both labels are visible — collapsing to 1 line would lose "登出".
    # Layout: top border, header (1 line), separator, data (2 lines),
    # bottom border = 6 lines.
    assert len(lines) == 6, f"expected 6 lines, got {len(lines)}: {lines}"

    data_lines = lines[3:5]
    # WHY: the short cell ("使用者") is top-aligned — its text sits on the
    # first physical line and the second physical line is blank-padded, so
    # the column stays rectangular instead of repeating the label.
    assert "使用者" in data_lines[0]
    assert "使用者" not in data_lines[1]
    assert "登入" in data_lines[0]
    assert "登出" in data_lines[1]

    # WHY: every output line sharing one display width is the only proof
    # that the multi-line row was padded by display width (not char len)
    # and that the blank-padded short cell kept the table rectangular.
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"


def test_ascii_only_output_has_no_box_drawing_chars():
    headers = ["項目", "狀態"]
    rows = [["使用者ログイン", "完了"]]

    out = render_table(headers, rows, ascii_only=True)

    offenders = _BOX_CHARS & set(out)
    assert not offenders, f"ascii_only output leaked box chars: {offenders}"
    assert "+" in out and "-" in out and "|" in out


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_gen_flow.py
# Contract tests for the linear-flow generator (render_flow).
#
# render_flow stacks each step as a box (┌─┐ │ label │ └─┘) on a common
# trunk column, joined by a centered down-arrow. The two invariants that
# make the diagram look right on a terminal are:
#
#   (a) every box-border line shares the same display_width -- so the
#       left/right borders line up vertically regardless of CJK/ASCII
#       label width;
#   (b) the connector │ and arrow ▼ sit at one constant display-column
#       across the whole output -- so the trunk is straight.
#
# Both are measured with width.display_width (terminal cells), never
# character count, because the labels mix CJK (2 cells) and ASCII (1).
# ---------------------------------------------------------------------------

def _display_col_of(line: str, glyph: str) -> int:
    """Display-column (0-based, in terminal cells) of glyph in line.

    Returns -1 if the glyph is absent. Uses display_width of the prefix
    so wide characters before the glyph advance the column by 2.
    """
    idx = line.find(glyph)
    if idx < 0:
        return -1
    return display_width(line[:idx])


def test_all_box_borders_share_one_display_width():
    out = render_flow(["收到訂單", "驗證ユーザー", "完了"])
    border_lines = [
        ln for ln in out.splitlines() if ln.lstrip().startswith(("┌", "└"))
    ]
    # Two borders per box, three boxes.
    assert len(border_lines) == 6
    widths = {display_width(ln) for ln in border_lines}
    assert len(widths) == 1, f"box borders differ in display width: {widths}"


def test_connector_and_arrow_share_one_trunk_column():
    out = render_flow(["收到訂單", "驗證ユーザー", "完了"])
    cols = []
    for ln in out.splitlines():
        for glyph in ("│", "▼"):
            if glyph in ln and ln.strip() in (glyph, "│", "▼"):
                cols.append(_display_col_of(ln, glyph))
    # Linear flow of 3 steps -> 2 connectors, each "│" then "▼".
    assert len(cols) >= 2, f"expected connector/arrow lines, got {cols}"
    assert len(set(cols)) == 1, f"trunk column not constant: {cols}"


def test_gen_flow_multiline_step_grows_box_taller():
    """A \\n label renders one centered body line per physical line.

    The box grows taller (one body line per label line); a single-line
    sibling still renders exactly one body line; and every box line --
    borders, multi-line body, single-line body -- shares one display_width
    so the diagram stays rectangular (the bare trunk │/▼ line is padding +
    glyph, narrower by design, and is covered by the trunk-column test).
    """
    multi = "驗證使用者\n身份確認"
    single = "完了"
    out = render_flow([multi, single])
    lines = out.splitlines()

    # Box lines are the borders (┌/└) and the bordered body lines; the
    # bare trunk │/▼ is excluded (it is padding + a single glyph).
    box_lines = [
        ln for ln in lines
        if ln.startswith(("┌", "└")) or (ln.startswith("│") and ln.endswith("│"))
    ]

    # (2) every box line shares one display_width.
    widths = {display_width(ln) for ln in box_lines}
    assert len(widths) == 1, f"box lines differ in display width: {widths}"

    # (1) the multi-line box has one body line per label line. Body lines
    # are bordered with "│" on both ends but are not the bare trunk.
    body_lines = [
        ln for ln in lines
        if ln.startswith("│") and ln.endswith("│") and ln.strip() != "│"
    ]
    multi_bodies = [
        ln for ln in body_lines if any(part in ln for part in split_lines(multi))
    ]
    assert len(multi_bodies) == len(split_lines(multi)) == 2, (
        f"multi-line box body lines: {multi_bodies}"
    )

    # (3) the single-line sibling still renders exactly one body line.
    single_bodies = [ln for ln in body_lines if single in ln]
    assert len(single_bodies) == 1, f"single-line box body lines: {single_bodies}"


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_gen_tree.py
# Contract tests for the Unicode tree/hierarchy generator.
#
# Branch glyphs (├─ └─ │) precede the labels, so the columns at which
# those glyphs appear are constant regardless of CJK label width — that
# column-stability is the observable proof the tree was rendered with a
# correct per-ancestor continuation prefix.
# ---------------------------------------------------------------------------

def _tree():
    return {
        "label": "訂單系統",
        "children": [
            {"label": "訂單服務"},
            {"label": "庫存サービス", "children": [{"label": "預扣"}]},
        ],
    }


def test_root_label_is_first_line():
    out = render_tree(_tree())
    lines = out.splitlines()
    assert lines[0] == "訂單系統"


def test_branch_glyphs_at_expected_columns():
    out = render_tree(_tree())
    lines = out.splitlines()

    # WHY: branch glyphs precede the CJK labels, so their columns are
    # constant. A first-level child's connector must start at column 0;
    # if continuation prefixes were computed with len()-vs-display-width
    # confusion or off-by-one indentation, these columns would drift.
    first_child = lines[1]
    assert first_child.startswith("├─ "), first_child
    assert first_child[3:] == "訂單服務"

    last_top_child = lines[2]
    # WHY: the LAST top-level child must use └─, not ├─ — proves the
    # renderer distinguishes last-sibling from the rest.
    assert last_top_child.startswith("└─ "), last_top_child
    assert last_top_child[3:] == "庫存サービス"


def test_grandchild_under_last_sibling_uses_space_continuation():
    out = render_tree(_tree())
    lines = out.splitlines()

    # The grandchild "預扣" sits under the LAST top-level child, so its
    # ancestor continuation column is spaces ("   "), not "│  ".
    grandchild = lines[3]
    # WHY: under a last-sibling the vertical bar must NOT be drawn;
    # leaking "│" here is the classic continuation-prefix bug.
    assert grandchild.startswith("   └─ "), repr(grandchild)
    assert grandchild[6:] == "預扣"
    assert "│" not in grandchild


def test_grandchild_under_non_last_sibling_uses_bar_continuation():
    tree = {
        "label": "root",
        "children": [
            {"label": "first", "children": [{"label": "deep"}]},
            {"label": "second"},
        ],
    }
    out = render_tree(tree)
    lines = out.splitlines()

    # "deep" sits under "first", which is NOT the last sibling, so the
    # ancestor continuation column must keep the vertical bar "│  ".
    grandchild = lines[2]
    assert grandchild.startswith("│  └─ "), repr(grandchild)
    assert grandchild[6:] == "deep"


def test_gen_tree_multiline_node_keeps_branch_prefixes():
    # A NON-last child and a LAST child each carry a CJK two-line label;
    # the last child also has a grandchild under it.
    tree = {
        "label": "訂單系統",
        "children": [
            {"label": "訂單服務\n下單"},
            {
                "label": "庫存サービス\n在庫",
                "children": [{"label": "預扣"}],
            },
        ],
    }
    out = render_tree(tree)
    lines = out.splitlines()

    # Line 0: root. Line 1: first child's connector line. Line 2: its
    # continuation line. Line 3: last child's connector line. Line 4:
    # its continuation line. Line 5: grandchild under the last child.
    assert lines[0] == "訂單系統"

    # First child is NON-last: connector on line 1, continuation on
    # line 2. WHY: the continuation prefix under a non-last sibling
    # must keep the vertical bar "│  " so the bar runs past the wrapped
    # label, and the continuation text must align under the label (col 3).
    assert lines[1] == "├─ 訂單服務", repr(lines[1])
    assert lines[2] == "│  下單", repr(lines[2])
    assert lines[2][3:] == "下單"

    # Last child: connector on line 3, continuation on line 4. WHY:
    # under a last sibling the continuation column is spaces "   ", not
    # "│  " — leaking "│" here is the multi-line continuation-prefix bug.
    assert lines[3] == "└─ 庫存サービス", repr(lines[3])
    assert lines[4] == "   在庫", repr(lines[4])
    assert "│" not in lines[4]
    assert lines[4][3:] == "在庫"

    # Grandchild renders AFTER all of the last child's label lines, with
    # the last-sibling space continuation.
    assert lines[5] == "   └─ 預扣", repr(lines[5])
    assert lines[5][6:] == "預扣"


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_gen_bar.py
# Contract tests for the CJK-aligned horizontal bar chart generator.
#
# Label-column alignment is verified by display_width, not len: every
# row's label segment MUST occupy the same number of terminal cells so
# that CJK/JP/EN-mixed labels line up before the bar starts. Bar lengths
# are verified to scale proportionally to the values.
# ---------------------------------------------------------------------------

def _label_segment(line: str) -> str:
    # WHY: the label column ends at the first bar/space boundary. The
    # label is right-padded with spaces then a single space separator,
    # so the label segment is everything up to (but not including) the
    # first '█'. Measuring this substring by display_width is the only
    # observable proof the padding used cell-width, not char-len.
    bar_start = line.index("█")
    return line[:bar_start]


def test_label_column_shares_one_display_width_across_rows():
    pairs = [("使用者", 120), ("注文", 80), ("AirPods", 40)]

    out = render_bar(pairs)
    lines = out.splitlines()

    widths = {display_width(_label_segment(line)) for line in lines}
    # WHY: a single shared label-segment cell-width across every row is
    # the only observable proof CJK/JP labels were padded by display
    # width — len-based padding would make the wide-char rows come up
    # short and the bars would not start at a common column.
    assert len(widths) == 1, f"label column misaligned: {sorted(widths)}"


def test_bar_lengths_are_proportional_to_values():
    pairs = [("使用者", 120), ("注文", 80), ("AirPods", 40)]
    width = 20

    out = render_bar(pairs, width=width)
    lines = out.splitlines()

    bar_runs = [line.count("█") for line in lines]

    # WHY: encodes the scaling intent — the max value maps to `width`
    # cells, and a half-value row maps to ~half. Without proportional
    # scaling these asserts cannot hold.
    assert bar_runs[0] == width, f"max row should fill width: {bar_runs[0]}"
    assert bar_runs[0] == max(bar_runs), "max-value row must have longest bar"
    # 40 is one-third of 120 -> ~width/3; 80 is two-thirds -> ~2*width/3.
    assert bar_runs[2] == round(40 / 120 * width)
    assert bar_runs[1] == round(80 / 120 * width)


def test_empty_input_returns_empty_string():
    # WHY: empty input must not crash (max() on an empty sequence raises).
    # Parity with gen_flow's empty-steps guard.
    assert render_bar([]) == ""


def test_bar_newline_in_label_rejected():
    # WHY: a bar row is inherently one line. A label containing '\n'
    # would silently split one row into two and corrupt the chart
    # alignment, so it must fail loud (ValueError) rather than render.
    import pytest

    with pytest.raises(ValueError):
        render_bar([("a\nb", 10)])

    # A normal bar still renders — the guard must not block valid input.
    assert render_bar([("ok", 10)]) != ""


def test_bar_carriage_return_in_label_rejected():
    # WHY: a carriage-return (\r) is a 0-width cursor-moving control char that
    # passes display-width checks yet silently corrupts the chart's terminal
    # alignment. The guard previously tested only for "\n", letting a \r-only
    # label through; it must reject ANY line break (\r, \n, \r\n).
    import pytest

    with pytest.raises(ValueError):
        render_bar([("a\rb", 10)])

    with pytest.raises(ValueError):
        render_bar([("a\r\nb", 10)])


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_gen_arch.py
# Contract tests for the layered-architecture diagram generator.
#
# render_arch stacks one INDEPENDENT box per layer, all sharing one outer
# interior width. Correctness is verified by display_width, not len: every
# rendered line MUST occupy the same number of terminal cells, and the two
# layer boxes MUST share one outer width, so the diagram reads as a clean
# vertical stack in a monospace terminal.
# ---------------------------------------------------------------------------

def test_two_layers_share_outer_width():
    layers = [
        {
            "name": "Presentation",
            "components": ["Web App", "Mobile App", "Desktop"],
        },
        {
            "name": "Business Logic",
            "components": ["OrderService", "InventoryService"],
        },
    ]

    out = render_arch(layers)
    lines = out.splitlines()

    # Locate each box's top border (the first line of every box starts
    # with "┌"). There are exactly two layers, hence two top borders.
    top_borders = [ln for ln in lines if ln.startswith("┌")]
    assert len(top_borders) == 2, f"expected 2 boxes, got {len(top_borders)}"

    # 1. Both boxes share ONE outer width — the only observable proof that
    #    every layer was sized to the shared max interior, not to its own
    #    natural component-row width.
    w0, w1 = display_width(top_borders[0]), display_width(top_borders[1])
    assert w0 == w1, f"layer boxes differ in outer width: {w0} vs {w1}"

    # 2. EVERY line shares that one display width — len-based padding would
    #    leave some lines short and skew the stack; a single shared cell
    #    width is the rectangularity guarantee.
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"

    # 3. Each box's separator junctions (┬) land at the SAME display-columns
    #    as the component-row seams (│). This is the file's central claim
    #    ("legitimate junctions keep align.py's kink check happy") and its
    #    most intricate logic — a one-column junction shift keeps every line
    #    width equal (passing assertion 2 silently), so seam alignment needs
    #    its own assertion. We check the first box: rows are
    #    [top, name, separator, row, bottom] repeating every 5 lines.
    def seam_columns(line: str, seam_char: str) -> list[int]:
        return [
            display_width(line[:i])
            for i, ch in enumerate(line)
            if ch == seam_char
        ]

    separator, row_line = lines[2], lines[3]
    sep_junctions = seam_columns(separator, "┬")
    row_seams = seam_columns(row_line, "│")
    # The row's │ includes the two outer borders; the inner seams are the
    # ones that must coincide with the separator's ┬.
    inner_row_seams = row_seams[1:-1]
    assert sep_junctions == inner_row_seams, (
        f"separator ┬ columns {sep_junctions} do not align with "
        f"row │ seams {inner_row_seams}"
    )
    assert sep_junctions, "expected at least one inter-cell junction"


def _seam_columns(line: str, seam_char: str) -> list[int]:
    """Display-columns (not char indices) of every `seam_char` on the line."""
    return [
        display_width(line[:i]) for i, ch in enumerate(line) if ch == seam_char
    ]


def test_cjk_layers_align_and_pass_oracle():
    """Mixed 中/英/日 labels stay rectangular AND clear the alignment oracle.

    Wide (2-cell) labels are the case where a char-count layout silently
    drifts: a separator ┬ computed by list-index instead of display-column
    lands one cell off under CJK, and the seam check (checks_seam) flags the
    orphaned vertical. We assert BOTH observable consequences:

      1. every rendered line has the SAME display width (rectangularity), and
      2. analyze() — the seam + table + kink oracle — finds zero issues,

    so junctions must be placed in DISPLAY cells, not character positions.
    """
    layers = [
        {
            "name": "展示層 Presentation",
            "components": ["網頁 Web", "モバイル App", "Desktop"],
        },
        {
            "name": "ビジネス Logic",
            "components": ["訂單 Service", "Inventory"],
        },
    ]

    out = render_arch(layers)
    lines = out.splitlines()

    # 1. Rectangular: one shared display width across every line.
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"CJK lines misaligned: {sorted(widths)}"

    # 2. The oracle is clean — no seam drift, no table-width drift, no kink.
    _report, issues = analyze(out)
    assert issues == [], f"oracle found drift under CJK: {issues}"

    # 3. Every box's separator ┬ still lands under the row │ in DISPLAY cells.
    #    A list-index junction would shift under the wide chars while keeping
    #    widths equal, so seam alignment needs its own CJK assertion.
    for box_start in range(0, len(lines), 5):
        separator, row_line = lines[box_start + 2], lines[box_start + 3]
        sep_junctions = _seam_columns(separator, "┬")
        inner_row_seams = _seam_columns(row_line, "│")[1:-1]
        assert sep_junctions == inner_row_seams, (
            f"box at line {box_start + 1}: separator ┬ {sep_junctions} "
            f"misaligned with row │ {inner_row_seams} under CJK"
        )


def test_slack_distributed_evenly():
    """Extra outer width is shared across a layer's cells, not dumped on one.

    When a layer's natural component-row is narrower than the shared outer
    interior, the leftover cells are spread EVENLY (remainder, then last cell)
    so the box reads as proportioned columns — not three skinny cells beside
    one bloated tail. We measure each cell's display width between the row's │
    seams; the max and min interior-cell widths must differ by at most one
    cell (the integer remainder).
    """
    layers = [
        # A long layer name forces ~26 cells of slack onto the 3-cell layer.
        {
            "name": "WideLayerNameForcesLotsOfSlackHere",
            "components": ["a", "b", "c"],
        },
        {"name": "x", "components": ["q"]},
    ]

    out = render_arch(layers)
    lines = out.splitlines()
    row_line = lines[3]  # the a/b/c component row of the first box

    # Split the interior (between the outer │…│) on the inner │ seams to get
    # each cell's rendered text, and measure its display width.
    interior_text = row_line[1:-1]
    cell_widths = [display_width(cell) for cell in interior_text.split("│")]
    assert len(cell_widths) == 3, f"expected 3 cells, got {cell_widths}"

    spread = max(cell_widths) - min(cell_widths)
    assert spread <= 1, (
        f"slack not distributed evenly across cells: widths {cell_widths} "
        f"(spread {spread} > 1 cell)"
    )


def test_single_layer_single_component():
    """A single-layer, single-component diagram is a clean rectangular box.

    Degenerate inputs (one component, one layer) must still render a box with
    a top, name, separator, row, and bottom — all the same display width — and
    pass the alignment oracle. With one component there are no inner seams, so
    the separator is a plain ├──┤ rule.
    """
    out = render_arch([{"name": "Only", "components": ["Solo"]}])
    lines = out.splitlines()

    assert len(lines) == 5, f"expected a 5-line single box, got {len(lines)}"
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"degenerate box not rectangular: {sorted(widths)}"

    _report, issues = analyze(out)
    assert issues == [], f"oracle found drift in degenerate box: {issues}"

    # No inner component seam: the separator has no ┬ junctions.
    assert "┬" not in lines[2], "single-component separator should have no ┬"


def test_gen_arch_multiline_component_grows_band_taller():
    """A layer with a `\n` component and a `\n` layer name grows taller.

    The band's row height = max line-count among its component cells, and a
    multi-line layer NAME renders as multiple centered name lines. Cells
    TOP-align: the taller cell's text fills the upper rows, with blank padding
    below for shorter cells. The shared outer width still spans all bands, and
    every output line keeps one equal display width.
    """
    layers = [
        {
            "name": "資料層\nData Layer",  # two name lines
            "components": ["快取\nCache", "DB"],  # 2-line CJK cell + 1-line cell
        },
        {
            "name": "Single",
            "components": ["Plain"],
        },
    ]

    out = render_arch(layers)
    lines = out.splitlines()

    # 1. Rectangular: one shared display width across every line.
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"multiline lines misaligned: {sorted(widths)}"

    # 2. The first band gains extra rows. Single-line band = 5 lines
    #    [top, name, separator, row, bottom]. The first band has a 2-line name
    #    (+1 name line) and a 2-line tallest cell (+1 row line), so it is
    #    5 + 1 + 1 = 7 lines. Total = 7 + 5 = 12 lines.
    assert len(lines) == 12, f"expected 12 lines (7 + 5), got {len(lines)}"

    # 3. The multi-line NAME renders across two centered lines. Both name
    #    fragments must appear as their own lines.
    name_lines = [ln for ln in lines[:7] if "資料層" in ln or "Data Layer" in ln]
    assert any("資料層" in ln for ln in name_lines), "first name line missing"
    assert any("Data Layer" in ln for ln in name_lines), "second name line missing"
    # They are on distinct lines (not concatenated onto one).
    assert not any(
        "資料層" in ln and "Data Layer" in ln for ln in name_lines
    ), "name lines should not be concatenated"

    # 4. The multi-line CELL top-aligns: "快取" appears on the first row line,
    #    "Cache" on the second; the single-line "DB" sits beside "快取" on the
    #    first row line and the blank below it on the second.
    #    Band layout: [top, name0, name1, separator, row0, row1, bottom].
    row0, row1 = lines[4], lines[5]
    assert "快取" in row0 and "DB" in row0, f"row0 missing top cell text: {row0!r}"
    assert "Cache" in row1, f"row1 missing continuation text: {row1!r}"
    assert "DB" not in row1, f"single-line DB should not repeat on row1: {row1!r}"

    # 5. The oracle stays clean under the taller band.
    _report, issues = analyze(out)
    assert issues == [], f"oracle found drift in multiline band: {issues}"


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_gen_seq.py
# Contract tests for the sequence-diagram generator (participant skeleton).
#
# render_seq lays participant boxes side by side across the top, each with a
# lifeline stub `┬` centered under its box and vertical lifelines `│` running
# below. Task 1 renders ONLY the participants-only skeleton (messages are
# accepted but not yet drawn). Correctness is verified by display_width, not
# len: every rendered line MUST occupy the same number of terminal cells, and
# each lifeline MUST sit at its participant box's TRUE display-center column so
# CJK (2-cell) names stay aligned in a monospace terminal.
# ---------------------------------------------------------------------------

def _col_of_char(line: str, target: str) -> list[int]:
    """Display-columns (not char indices) of every `target` on the line."""
    return [
        display_width(line[:i]) for i, ch in enumerate(line) if ch == target
    ]


def test_participants_render_boxes_and_lifelines():
    """3 participants (incl. CJK) render boxes + display-centered lifelines.

    A char-count layout silently drifts under a wide (2-cell) name: the
    lifeline `│` computed by string index instead of display-column lands one
    cell off. We assert three observable consequences:

      1. each participant name appears inside a box,
      2. EVERY rendered line shares one display width (rectangularity), and
      3. each lifeline `│` on the lifeline rows sits at its box's TRUE
         display-center column — computed independently here, not read back.
    """
    participants = ["User", "API サービス", "DB"]
    messages = []  # Task 1: skeleton only, messages not yet rendered.

    out = render_seq(participants, messages)
    lines = out.splitlines()

    # 1. Each participant name appears in the output (inside its box).
    for name in participants:
        assert name in out, f"participant {name!r} missing from output"

    # 2. Rectangular: one shared display width across every line. len-based
    #    padding would leave CJK lines short and skew the lifelines.
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"

    # Independently compute each box's expected center display-column.
    # Box interior = name display width + 2 (one pad space each side); the
    # left border "│" occupies the box's first column, so the interior center
    # sits at box_start + 1 + interior // 2. Boxes are laid out left to right
    # with a fixed gap; the gap is whatever separates the first two box top
    # corners "┌". We derive box_start from the actual "┌" positions so the
    # test does not hard-code the gap width (only that centers are consistent).
    top = lines[0]
    box_starts = _col_of_char(top, "┌")
    assert len(box_starts) == len(participants), (
        f"expected {len(participants)} box tops, got {len(box_starts)}"
    )
    expected_centers = [
        start + 1 + (display_width(name) + 2) // 2
        for start, name in zip(box_starts, participants)
    ]

    # 3. The lifeline-stub row (the box's "└──┬─┘" line) carries one ┬ per box,
    #    each at its expected center column.
    stub_row = next(ln for ln in lines if "┬" in ln)
    stub_cols = _col_of_char(stub_row, "┬")
    assert stub_cols == expected_centers, (
        f"lifeline stubs {stub_cols} not at box centers {expected_centers}"
    )

    # ...and the vertical-lifeline rows below carry one │ per box at the SAME
    # columns (and nothing else but spaces).
    lifeline_rows = [
        ln for ln in lines if set(ln) <= {"│", " "} and "│" in ln
    ]
    assert lifeline_rows, "expected at least one vertical-lifeline row"
    for row in lifeline_rows:
        assert _col_of_char(row, "│") == expected_centers, (
            f"lifeline │ columns {_col_of_char(row, '│')} "
            f"not at box centers {expected_centers}"
        )


def _box_centers(top_line: str, participants: list[str]) -> list[int]:
    """Independently recompute each box's lifeline display-center column.

    Mirrors the test-1 derivation: interior = name width + 2 pads, the left
    border occupies the box's first column, so the center sits at
    box_start + 1 + interior // 2. box_start is read from actual "┌" columns.
    """
    box_starts = _col_of_char(top_line, "┌")
    return [
        start + 1 + (display_width(name) + 2) // 2
        for start, name in zip(box_starts, participants)
    ]


def test_message_arrow_direction_and_landing():
    """Each message renders a centered label row + a directional arrow row.

    Three messages exercise the geometry that a naive char-index layout gets
    wrong:

      1. a LEFT→RIGHT message: the arrowhead ► must land EXACTLY on the
         target lifeline's display-center column, shaft is ─;
      2. a RIGHT→LEFT message: the arrowhead ◄ must land EXACTLY on the
         target (leftward) column;
      3. a NON-ADJACENT span (skips a middle participant): on the arrow row
         the shaft CROSSES the intermediate lifeline column (that cell is a
         shaft glyph, not the preserved │);

    plus the two invariants the whole diagram must keep: every line shares one
    display width, and each label is centered over its arrow's span.
    """
    participants = ["A", "B", "C"]
    messages = [
        {"from": "A", "to": "B", "label": "go"},   # left -> right, adjacent
        {"from": "B", "to": "A", "label": "ok"},   # right -> left, adjacent
        {"from": "A", "to": "C", "label": "skip"},  # left -> right, non-adjacent
    ]

    out = render_seq(participants, messages)
    lines = out.splitlines()

    # Shared display width across every line (rectangularity).
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"

    centers = _box_centers(lines[0], participants)
    col_a, col_b, col_c = centers

    # Arrow rows are the lines carrying a horizontal arrowhead glyph.
    arrow_rows = [ln for ln in lines if "►" in ln or "◄" in ln]
    assert len(arrow_rows) == len(messages), (
        f"expected {len(messages)} arrow rows, got {len(arrow_rows)}"
    )
    row_go, row_ok, row_skip = arrow_rows

    # 1. A -> B : single ► head landing on B's column; rightward shaft.
    assert _col_of_char(row_go, "►") == [col_b], (
        f"L->R head at {_col_of_char(row_go, '►')}, expected B col {col_b}"
    )
    assert "◄" not in row_go
    # Shaft cell immediately right of the source is a horizontal glyph.
    assert row_go[col_a + 1] == "─", "L->R shaft should start with ─"

    # 2. B -> A : single ◄ head landing on A's (leftward) column.
    assert _col_of_char(row_ok, "◄") == [col_a], (
        f"R->L head at {_col_of_char(row_ok, '◄')}, expected A col {col_a}"
    )
    assert "►" not in row_ok

    # 3. A -> C : head on C; the intermediate lifeline column B is CROSSED by
    #    the shaft on this row (a horizontal glyph, NOT the preserved │).
    assert _col_of_char(row_skip, "►") == [col_c], (
        f"non-adjacent head at {_col_of_char(row_skip, '►')}, expected C col {col_c}"
    )
    crossing_cell = row_skip[col_b]
    assert crossing_cell != "│", (
        f"intermediate lifeline at col {col_b} should be crossed, got {crossing_cell!r}"
    )
    assert crossing_cell == "─", (
        f"crossing cell should be shaft ─, got {crossing_cell!r}"
    )

    # Label rows: the line directly ABOVE each arrow row carries its label,
    # centered over the arrow's [min, max] column span.
    for arrow_row, msg in zip(arrow_rows, messages):
        idx = lines.index(arrow_row)
        label_row = lines[idx - 1]
        label = msg["label"]
        assert label in label_row, f"label {label!r} missing above its arrow"
        # Centered: the label's midpoint sits within 1 cell of the span midpoint.
        start_col = display_width(label_row[: label_row.index(label)])
        label_mid = start_col + display_width(label) / 2
        lo = min(centers[participants.index(msg["from"])],
                 centers[participants.index(msg["to"])])
        hi = max(centers[participants.index(msg["from"])],
                 centers[participants.index(msg["to"])])
        span_mid = (lo + hi) / 2
        assert abs(label_mid - span_mid) <= 1, (
            f"label {label!r} mid {label_mid} not centered over span "
            f"mid {span_mid}"
        )


def test_long_cjk_label_widens_gap():
    """A CJK label wider than the default lifeline gap widens its span.

    Two adjacent participants (`A`, `B`) carry a message whose CJK label is
    far wider than the default box-to-box gap. Before column-widening, the
    label would clamp/overflow past the target lifeline and shear the
    rectangle. We assert three things a correct widening keeps true:

      1. the FULL label appears on its label row, fitting WITHIN its arrow's
         [src, dst] span — it does not overflow past the target lifeline
         column and is not truncated;
      2. EVERY rendered line shares one display width (rectangularity);
      3. each lifeline `│` sits at consistent display-columns across every
         lifeline row (lifelines stay vertical after the widening shift).
    """
    participants = ["A", "B"]
    # 6 CJK glyphs = 12 display cells, far wider than the default _GAP (3) plus
    # the two 1-cell box interiors: the gap MUST widen to fit this label.
    label = "送信処理開始要"
    messages = [{"from": "A", "to": "B", "label": label}]

    out = render_seq(participants, messages)
    lines = out.splitlines()

    # 2. Rectangular: one shared display width across every line.
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"

    centers = _box_centers(lines[0], participants)
    col_a, col_b = centers
    lo, hi = min(col_a, col_b), max(col_a, col_b)

    # Locate the arrow row and its label row (line directly above).
    arrow_rows = [ln for ln in lines if "►" in ln or "◄" in ln]
    assert len(arrow_rows) == 1, f"expected 1 arrow row, got {len(arrow_rows)}"
    arrow_row = arrow_rows[0]
    # Arrowhead lands exactly on B's lifeline column.
    assert _col_of_char(arrow_row, "►") == [col_b], (
        f"arrowhead at {_col_of_char(arrow_row, '►')}, expected B col {col_b}"
    )
    label_row = lines[lines.index(arrow_row) - 1]

    # 1. Full label present and fitting WITHIN the [lo, hi] arrow span.
    assert label in label_row, f"label {label!r} missing / truncated"
    start_col = display_width(label_row[: label_row.index(label)])
    end_col = start_col + display_width(label)
    assert start_col >= lo, (
        f"label starts at col {start_col}, overflows left past span start {lo}"
    )
    assert end_col <= hi + 1, (
        f"label ends at col {end_col}, overflows past target lifeline {hi}"
    )

    # 3. Lifelines vertical: every lifeline row carries │ at the same columns.
    lifeline_rows = [
        ln for ln in lines if set(ln) <= {"│", " "} and "│" in ln
    ]
    assert lifeline_rows, "expected at least one vertical-lifeline row"
    for row in lifeline_rows:
        assert _col_of_char(row, "│") == centers, (
            f"lifeline │ columns {_col_of_char(row, '│')} "
            f"drifted from box centers {centers}"
        )


def test_label_fitting_default_span_does_not_widen():
    """A label that EXACTLY fits the default span must NOT widen the gap.

    Column-widening must add only the deficit between the label width and the
    TRUE inclusive lifeline span (center[dst] - center[src] + 1). If the span
    primitive miscounts (off-by-one), a label that already fits gets a
    spuriously wider gap — the diagram is wider than necessary. We pin this by
    comparing against the messages-less skeleton: a label whose display width
    equals the true default span produces a diagram of the SAME total width as
    the participants-only skeleton (no widening).
    """
    participants = ["A", "B"]

    # Baseline width with no messages = the un-widened skeleton.
    skeleton = render_seq(participants, [])
    base_width = display_width(skeleton.splitlines()[0])

    # True default inclusive span between A's and B's lifelines, computed from
    # the skeleton's own header (independent of render_seq internals).
    centers = _box_centers(skeleton.splitlines()[0], participants)
    default_span = centers[1] - centers[0] + 1

    # A label exactly as wide as that span fits without any widening.
    label = "x" * default_span
    out = render_seq(participants, [{"from": "A", "to": "B", "label": label}])
    out_width = display_width(out.splitlines()[0])

    assert out_width == base_width, (
        f"label of width {default_span} (== true span) over-widened: diagram "
        f"width {out_width} vs minimal {base_width}"
    )
    # And the full label still fits within the (unchanged) span.
    label_row = next(ln for ln in out.splitlines() if label in ln)
    start_col = display_width(label_row[: label_row.index(label)])
    assert start_col >= centers[0] and start_col + default_span <= centers[1] + 1, (
        f"label not within span [{centers[0]}, {centers[1]}]"
    )


def test_self_message_rejected():
    """A message with from == to (self-message) is rejected with ValueError."""
    import pytest

    participants = ["A", "B"]
    messages = [{"from": "A", "to": "A", "label": "loop"}]
    with pytest.raises(ValueError):
        render_seq(participants, messages)


def test_seq_newline_in_label_rejected():
    """A `\\n` in a participant name OR a message label is rejected loudly.

    Multi-line sequence diagrams are DEFERRED. A newline embedded in a
    participant name or a message label would silently corrupt the diagram
    (a row would split across lines, shearing the rectangle and lifelines).
    The check must fire EARLY — before any layout — so the failure is a clear
    ValueError, not a downstream mis-render. A normal seq still renders fine.
    """
    import pytest

    # 1. Newline in a participant name -> ValueError.
    with pytest.raises(ValueError):
        render_seq(["A\nB", "C"], [])

    # 2. Newline in a message label -> ValueError.
    with pytest.raises(ValueError):
        render_seq(["A", "B"], [{"from": "A", "to": "B", "label": "go\nstop"}])

    # 3. A normal seq (no newlines anywhere) still renders without error.
    out = render_seq(["A", "B"], [{"from": "A", "to": "B", "label": "go"}])
    assert "go" in out
    assert "►" in out


def test_seq_carriage_return_in_label_rejected():
    """A bare \\r (no \\n) in a name OR message label is rejected loudly.

    A carriage-return is a 0-width cursor-moving control char: it passes the
    display-width checks yet silently corrupts the rendered diagram's terminal
    alignment. The reject guard that only tested for "\\n" let a \\r-only label
    through; the guard must reject ANY line break (\\r, \\n, \\r\\n).
    """
    import pytest

    # 1. Bare \r in a participant name -> ValueError.
    with pytest.raises(ValueError):
        render_seq(["A\rB", "C"], [])

    # 2. Bare \r in a message label -> ValueError.
    with pytest.raises(ValueError):
        render_seq(["A", "B"], [{"from": "A", "to": "B", "label": "go\rstop"}])

    # 3. CRLF in a message label -> ValueError.
    with pytest.raises(ValueError):
        render_seq(["A", "B"], [{"from": "A", "to": "B", "label": "go\r\nstop"}])
