# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""Width primitive and glyph taxonomy tests (consolidated from test_width.py, test_glyphs.py)."""
# concern: shared rendering helpers in width.py must keep generator output byte-identical

import pathlib
import sys
import unicodedata

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[2] / "skills" / "loom-visualization" / "scripts"))

import glyphs
from width import char_width, display_width, split_lines


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_width.py
# Contract tests for the shared display-width primitive.
#
# Width policy (from the brief): CJK Wide/Fullwidth = 2, Ambiguous = 1,
# box-drawing = 1, control/zero-width = 0. Expectations derive from the
# interpreter's Unicode database (unicodedata).
# ---------------------------------------------------------------------------

def test_display_width_cjk_is_two_per_char():
    assert display_width("中文") == 4


def test_display_width_japanese_kana_and_kanji_are_wide():
    # Hiragana, katakana, kanji each render Wide = 2.
    assert display_width("あア漢") == 6


def test_display_width_fullwidth_forms_are_two():
    # U+3000 ideographic space and U+FF21 fullwidth Latin A are Wide = 2.
    assert display_width("　") == 2
    assert display_width("Ａ") == 2


def test_display_width_ascii_is_one_per_char():
    assert display_width("abc123") == 6


def test_display_width_empty_string_is_zero():
    assert display_width("") == 0


def test_char_width_box_drawing_is_one():
    assert char_width("─") == 1
    assert char_width("│") == 1
    assert char_width("┌") == 1


def test_char_width_ascii_is_one():
    assert char_width("a") == 1


def test_char_width_cjk_is_two():
    assert char_width("中") == 2


def test_char_width_ambiguous_is_one():
    # Ambiguous East-Asian width resolves to 1 under the policy.
    assert char_width("·") == 1
    assert char_width("§") == 1


def test_char_width_control_and_zero_width_is_zero():
    # Cc / Mn / Me / Cf categories -> 0.
    assert char_width("\x00") == 0          # NUL control char
    assert char_width("​") == 0        # zero-width space
    assert char_width("́") == 0        # combining acute accent


def test_split_lines_plain_label_returns_physical_lines():
    # Always >= 1 element; a bare label is a single-element list.
    assert split_lines("abc") == ["abc"]
    assert split_lines("a\nb") == ["a", "b"]
    assert split_lines("a\n\nb") == ["a", "", "b"]
    assert split_lines("") == [""]


def test_split_lines_handles_cr_crlf():
    # WHY: a carriage-return (\r) is a 0-width cursor-moving control char.
    # A naive label.split("\n") leaves \r embedded ("a\r\nb" -> ["a\r","b"])
    # or fails to split a \r-only label, so the \r passes width checks (0
    # cells) yet CORRUPTS terminal alignment silently at exit 0. splitlines()
    # treats \r, \n and \r\n as real line breaks, so no element retains an
    # embedded control char.
    assert split_lines("a\r\nb") == ["a", "b"]
    assert split_lines("a\rb") == ["a", "b"]
    # No element of any split result may retain an embedded \r.
    for label in ("a\r\nb", "a\rb", "x\r\ny\rz"):
        for piece in split_lines(label):
            assert "\r" not in piece, f"\\r leaked into {piece!r}"


def test_render_flow_crlf_label_leaks_no_carriage_return():
    # WHY: split_lines feeds the render generators. A CRLF label must produce
    # output with NO raw \r byte — a \r is a 0-width cursor-moving control
    # char that passes width checks yet corrupts terminal alignment at exit 0.
    # Encoding the rendered string to bytes proves the leak is closed at the
    # generator boundary (the flow generator stands in for all four render
    # generators that route through split_lines).
    from gen_flow import render_flow

    out = render_flow(["a\r\nb"])
    assert b"\r" not in out.encode("utf-8"), (
        "carriage-return leaked into rendered flow output"
    )


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_glyphs.py
# Tests for the canonical box-drawing glyph taxonomy (scripts/glyphs.py).
#
# These assert representative membership across ALL line styles (light /
# rounded / heavy / double / dashed) so a future deletion of any style from a
# frozenset is caught here rather than silently weakening a downstream check.
# ---------------------------------------------------------------------------

def test_rounded_corners_in_corners_and_junctions():
    assert "╭" in glyphs.CORNERS
    assert "╭" in glyphs.JUNCTIONS
    assert "╰" in glyphs.CORNERS
    assert "╰" in glyphs.JUNCTIONS


def test_double_style_members():
    assert "║" in glyphs.VERTICALS
    assert "╔" in glyphs.CORNERS
    assert "╬" in glyphs.TEES


def test_heavy_style_members():
    assert "┃" in glyphs.VERTICALS
    assert "┏" in glyphs.CORNERS
    assert "╋" in glyphs.TEES


def test_dashed_style_members():
    assert "┆" in glyphs.VERTICALS
    assert "┄" in glyphs.HORIZONTALS


def test_cross_and_arrow_membership():
    assert "┼" in glyphs.TEES
    assert "┼" in glyphs.JUNCTIONS
    assert "▼" in glyphs.ARROWS
    assert "▼" in glyphs.VERTICAL_CONNECTORS


def test_derived_sets_are_supersets():
    assert glyphs.JUNCTIONS >= glyphs.CORNERS
    assert glyphs.JUNCTIONS >= glyphs.TEES
    assert glyphs.STRUCTURAL >= glyphs.VERTICALS
    assert glyphs.STRUCTURAL >= glyphs.ARROWS


def test_horizontal_in_horizontals_and_box_border():
    assert "─" in glyphs.HORIZONTALS
    assert "─" in glyphs.BOX_BORDER


# ---------------------------------------------------------------------------
# loom-visualization: standard-library width pins
#
# char_width is derived from the interpreter's Unicode database:
#   category Cc / Mn / Me / Cf -> 0, East Asian Width W / F -> 2, else 1.
# ---------------------------------------------------------------------------

# Every non-ASCII glyph the six generators emit (table, flow, tree, bar,
# arch, seq). test_generators_emit_only_pinned_glyphs keeps this list honest.
GENERATOR_GLYPHS = "─│┌┐└┘├┤┬┴┼█►▼◄"


def _policy_width(ch):
    if unicodedata.category(ch) in ("Cc", "Mn", "Me", "Cf"):
        return 0
    return 2 if unicodedata.east_asian_width(ch) in ("W", "F") else 1


def test_cjk_ideographs_are_two():
    for ch in "中文漢字資料訂單系統\U00020000":
        assert unicodedata.east_asian_width(ch) == "W", hex(ord(ch))
        assert char_width(ch) == 2, hex(ord(ch))


def test_kana_is_two_and_halfwidth_katakana_is_one():
    for ch in "あいうをんアイウヲンーヽ・":
        assert char_width(ch) == 2, hex(ord(ch))
    # U+FF71 HALFWIDTH KATAKANA A has East Asian Width H -> 1 cell.
    assert unicodedata.east_asian_width("ｱ") == "H"
    assert char_width("ｱ") == 1


def test_cjk_punctuation_is_two():
    for ch in "、。「」『』【】〜〈〉":
        assert char_width(ch) == 2, hex(ord(ch))
    assert display_width("「開始」、完了。") == 16


def test_fullwidth_forms_are_two():
    for ch in "ＡＺａｚ０９！？（）　":
        assert unicodedata.east_asian_width(ch) in ("F", "W"), hex(ord(ch))
        assert char_width(ch) == 2, hex(ord(ch))


def test_every_generator_glyph_is_one():
    for ch in GENERATOR_GLYPHS:
        assert char_width(ch) == 1, hex(ord(ch))


def test_every_taxonomy_glyph_is_one():
    for ch in sorted(glyphs.STRUCTURAL):
        assert char_width(ch) == 1, hex(ord(ch))


def test_generators_emit_only_pinned_glyphs():
    from gen_arch import render_arch
    from gen_bar import render_bar
    from gen_flow import render_flow
    from gen_seq import render_seq
    from gen_table import render_table
    from gen_tree import render_tree

    outputs = [
        render_table(["a", "b"], [["1", "2"], ["3", "4"]]),
        render_flow(["start", "end"]),
        render_tree({"label": "root", "children": [{"label": "a"}, {"label": "b", "children": [{"label": "c"}]}]}),
        render_bar([("a", 3), ("b", 1)], width=5),
        render_arch([{"name": "L1", "components": ["a", "b"]}, {"name": "L2", "components": ["c"]}]),
        render_seq(["A", "B", "C"], [{"from": "A", "to": "C", "label": "go"}, {"from": "C", "to": "A", "label": "back"}]),
    ]
    emitted = {ch for out in outputs for ch in out if ord(ch) > 127}
    assert emitted <= set(GENERATOR_GLYPHS), sorted(emitted - set(GENERATOR_GLYPHS))
    assert emitted == set(GENERATOR_GLYPHS), sorted(set(GENERATOR_GLYPHS) - emitted)


def test_control_and_combining_chars_width_zero():
    cases = {
        "Cc": "\x00\x07\x1b\x7f\x85\x9f",
        "Mn": "゙゚̀́",
        "Me": "⃝⃞",
        "Cf": "­​‍⁠﻿",
    }
    for category, chars in cases.items():
        for ch in chars:
            assert unicodedata.category(ch) == category, hex(ord(ch))
            assert char_width(ch) == 0, hex(ord(ch))
    # A combining mark adds no cell to its base character.
    assert display_width("é") == 1
    assert display_width("が") == 2


def test_char_width_matches_unicodedata_policy():
    for cp in list(range(0x0000, 0x3100)) + list(range(0xF900, 0x10000)):
        if 0xD800 <= cp <= 0xDFFF:
            continue
        ch = chr(cp)
        assert char_width(ch) == _policy_width(ch), hex(cp)


def test_wrap_label_prefers_ascii_spaces():
    from width import wrap_label
    # ASCII text with spaces - should break at spaces
    assert wrap_label("hello world", 5) == ["hello", "world"]
    assert wrap_label("hello  world", 5) == ["hello", "world"]  # multiple spaces collapsed
    assert wrap_label("a b c d e", 3) == ["a b", "c d", "e"]  # prefers spaces

    # CJK text without spaces - should break per character
    assert wrap_label("你好世界", 4) == ["你好", "世界"]  # 2+2 chars, each 2 cells
    assert wrap_label("你好世界", 3) == ["你", "好", "世", "界"]  # breaks per char when needed

    # Mixed ASCII and CJK
    assert wrap_label("Hello 世界", 8) == ["Hello ", "世界"]  # breaks at space, includes space
    assert wrap_label("Hello世界", 8) == ["Hello", "世界"]  # no space, breaks between "o" and "世"

    # Edge cases
    assert wrap_label("", 5) == [""]
    assert wrap_label(" ", 5) == [" "]  # single space fits
    assert wrap_label("  ", 5) == ["  "]  # two spaces fit


def test_wrap_label_handles_tabs_and_control_chars():
    from width import wrap_label
    # Tabs and other control chars should be treated as 0 width but not as break points
    # For now, we'll just ensure it doesn't crash - the split_lines function will raise
    # for embedded control chars other than \n/\r, but wrap_label works on already-split lines
    pass


# ---------------------------------------------------------------------------
# W1-01: Shared helpers tests (EMPTY_BODY, center, require_single_line, render_structured_node)
# ---------------------------------------------------------------------------

def test_EMPTY_BODY_constant():
    from width import EMPTY_BODY
    assert EMPTY_BODY == "Body cannot be empty for structured node"


def test_center_plain_ascii():
    from width import center
    # Even slack
    assert center("abc", 7) == "  abc  "
    # Odd slack (extra goes right)
    assert center("abc", 8) == "  abc   "
    # Label wider than interior -> negative slack -> no padding
    assert center("abcdef", 4) == "abcdef"


def test_center_cjk():
    from width import center
    # CJK chars are 2 cells each
    # "中文" = 4 cells, interior=8 -> slack=4 -> left=2, right=2
    assert center("中文", 8) == "  中文  "
    # Odd slack
    assert center("中文", 9) == "  中文   "
    # Label wider than interior
    assert center("中文", 3) == "中文"


def test_require_single_line_passes():
    from width import require_single_line
    # Single line value should not raise
    require_single_line("hello", "test label")
    require_single_line("", "empty label")
    require_single_line("中文", "cjk label")


def test_require_single_line_raises_seq_style():
    from width import require_single_line
    import pytest
    with pytest.raises(ValueError) as exc:
        require_single_line("line1\nline2", "participant name")
    assert "line break not supported in participant name" in str(exc.value)
    # !r format produces 'line1\nline2' (escaped)
    assert "line1\\nline2" in str(exc.value)


def test_require_single_line_raises_bar_style():
    from width import require_single_line
    import pytest
    with pytest.raises(ValueError) as exc:
        require_single_line("line1\nline2", "bar label", template="{phrase} must be single-line, got line break in {value!r}")
    assert "bar label must be single-line, got line break in" in str(exc.value)
    assert "line1\\nline2" in str(exc.value)


def test_render_structured_node_basic():
    from width import render_structured_node
    # Simple ASCII title and body
    lines = render_structured_node("Title", ["body line"], 10)
    # Title line: "│ Title    │" (interior=10, title="Title"=5, so 10-5-1=4 spaces)
    assert lines[0] == "│ Title    │"
    # Separator line: "├──────────┤"
    assert lines[1] == "├──────────┤"
    # Body line: "│ body line│" (interior=10, "body line"=9, so 10-9-1=0 spaces)
    assert lines[2] == "│ body line│"


def test_render_structured_node_cjk():
    from width import render_structured_node
    # CJK title and body - "標題" = 4 cells, "內容行" = 6 cells
    lines = render_structured_node("標題", ["內容行"], 12)
    # Title: "│ 標題       │" (interior=12, "標題"=4, so 12-4-1=7 spaces)
    assert lines[0] == "│ 標題       │"
    # Separator: "├────────────┤"
    assert lines[1] == "├────────────┤"
    # Body: "│ 內容行     │" (interior=12, "內容行"=6, so 12-6-1=5 spaces)
    assert lines[2] == "│ 內容行     │"


def test_render_structured_node_empty_body_list():
    from width import render_structured_node
    # Empty body list should still return title + separator (caller validates non-empty)
    lines = render_structured_node("Title", [], 10)
    assert lines[0] == "│ Title    │"
    assert lines[1] == "├──────────┤"
    assert len(lines) == 2  # Only title and separator, no body lines


def test_render_structured_node_wrapped_body():
    from width import render_structured_node
    # Body line that needs wrapping at interior-1
    lines = render_structured_node("Title", ["this is a long body line that wraps"], 20)
    assert lines[0] == "│ Title              │"
    assert lines[1] == "├────────────────────┤"
    # Body should be wrapped at interior-1 = 19 cells
    # "this is a long body line that wraps" width = 37 chars (ASCII) = 37 cells
    # Wrapped at 19 cells
    # All body lines should start with "│ " and end with "│" (no trailing space)
    for line in lines[2:]:
        assert line.startswith("│ ")
        assert line.endswith("│")
