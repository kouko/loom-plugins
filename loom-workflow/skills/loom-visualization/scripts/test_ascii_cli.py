# Ported from ascii-graph-toolkit v0.6.0 (monkey-skills e5b978e0), MIT.
"""CLI and end-to-end tests (consolidated from test_align_cli.py, test_generate_cli.py, test_e2e.py)."""

import ast
import io
import json
import os
import pathlib
import subprocess
import sys
from contextlib import redirect_stdout

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

import align
import generate
from generate import main, render
from width import display_width


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_align_cli.py
# ---------------------------------------------------------------------------

_SCRIPT = (
    pathlib.Path(__file__).resolve().parent / "align.py"
)

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

# CLEAN: boxes sized by display-width; seam connects, blocks equal-width,
# no kink. Verified to yield zero issues across all three checks.
CLEAN = """\
┌──────────┐
│ 開始處理 │
└────┬─────┘
     │
     ▼
┌──────────┐
│ 完成結束 │
└──────────┘"""


def test_analyze_drifted_has_issues():
    _report, issues = align.analyze(DRIFTED)
    assert len(issues) >= 1


def test_analyze_clean_has_no_issues():
    _report, issues = align.analyze(CLEAN)
    assert issues == []


def test_analyze_report_is_one_line_per_input_line():
    report, _issues = align.analyze(DRIFTED)
    assert len(report.splitlines()) == len(DRIFTED.splitlines())


def test_report_line_numbers_are_1_based_and_match_issue_numbering():
    # Regression for the dogfood F1 bug: the report numbered lines 0-based
    # while drift messages are 1-based, so "fix the flagged line" pointed one
    # line off. The report's first line must be index 1, and an issue's line
    # number must name the same row the report shows.
    report, issues = align.analyze(DRIFTED)
    first = report.splitlines()[0]
    assert first.split()[0] == "1", f"report not 1-based: {first!r}"
    ln = issues[0][0]
    # The issue's 1-based line number must appear as a report row label.
    labels = {line.split()[0] for line in report.splitlines()}
    assert str(ln) in labels


def test_main_drifted_returns_1(tmp_path):
    f = tmp_path / "drifted.txt"
    f.write_text(DRIFTED, encoding="utf-8")
    with redirect_stdout(io.StringIO()):
        rc = align.main([str(f)])
    assert rc == 1


def test_main_clean_returns_0(tmp_path):
    f = tmp_path / "clean.txt"
    f.write_text(CLEAN, encoding="utf-8")
    with redirect_stdout(io.StringIO()):
        rc = align.main([str(f)])
    assert rc == 0


def test_main_clean_prints_no_drift(tmp_path):
    f = tmp_path / "clean.txt"
    f.write_text(CLEAN, encoding="utf-8")
    buf = io.StringIO()
    with redirect_stdout(buf):
        align.main([str(f)])
    assert "no drift" in buf.getvalue()


def test_subprocess_stdin_drifted_exits_1():
    # Run from repo root; script's own dir is sys.path[0] so imports resolve.
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.run(
        [sys.executable, str(_SCRIPT)],
        input=DRIFTED,
        capture_output=True,
        text=True,
        env=env,
    )
    assert proc.returncode == 1, proc.stderr


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_generate_cli.py
# Contract tests for the generate.py dispatch CLI.
#
# render(shape, payload) is the testable seam (no subprocess); it routes
# to the matching generator and returns the rendered diagram. Each shape
# is exercised with a CJK/JP fixture so we prove the dispatch preserves
# the underlying generator's CJK behavior, not just that it returns text.
# ---------------------------------------------------------------------------

def test_table_dispatch_preserves_display_width_alignment():
    payload = {
        "headers": ["項目", "狀態", "數量"],
        "rows": [["使用者ログイン", "完了", "123"]],
    }
    out = render("table", payload)
    lines = out.splitlines()
    widths = {display_width(line) for line in lines}
    # WHY: a single shared display-width across every line is the only
    # observable proof that dispatch reached the real CJK-aware table
    # renderer (not a len-based stand-in that would skew wide cells).
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"


def test_flow_dispatch_contains_cjk_labels_and_is_multiline():
    payload = {"steps": ["収到訂單", "驗證ユーザー", "完了"]}
    out = render("flow", payload)
    assert out
    assert "収到訂單" in out and "驗證ユーザー" in out
    assert "\n" in out


def test_tree_dispatch_contains_cjk_labels_and_is_multiline():
    payload = {
        "node": {
            "label": "訂單系統",
            "children": [{"label": "庫存サービス"}],
        }
    }
    out = render("tree", payload)
    assert out
    assert "訂單系統" in out and "庫存サービス" in out
    assert "\n" in out


def test_bar_dispatch_contains_cjk_labels_and_renders_bars():
    payload = {"pairs": [["売上", 100], ["成本", 40]], "width": 20}
    out = render("bar", payload)
    assert out
    assert "売上" in out and "成本" in out
    assert "█" in out


def test_arch_shape_routes():
    payload = {
        "layers": [
            {"name": "Presentation", "components": ["Web App", "モバイル"]},
            {"name": "資料層", "components": ["DB"]},
        ]
    }
    out = render("arch", payload)
    lines = out.splitlines()
    assert out
    assert "\n" in out
    # WHY: a single shared display-width across every line is the only
    # observable proof that dispatch reached the real CJK-aware arch
    # renderer (boxes stack to one shared interior width).
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"
    assert "モバイル" in out and "資料層" in out


def test_seq_shape_routes():
    payload = {"participants": ["User", "API サービス", "DB"], "messages": []}
    out = render("seq", payload)
    lines = out.splitlines()
    assert out
    assert "\n" in out
    # WHY: a shared display-width across the lifeline rows is the only
    # observable proof that dispatch reached the real CJK-aware seq
    # renderer (lifelines align under display-centered participant boxes,
    # not character-centered ones).
    assert "API サービス" in out and "User" in out and "DB" in out
    widths = {display_width(line) for line in lines}
    assert len(widths) == 1, f"lines misaligned: {sorted(widths)}"


def test_main_seq_returns_0(monkeypatch, capsys):
    payload = '{"participants":["A","B"],"messages":[]}'
    monkeypatch.setattr("sys.stdin", io.StringIO(payload))
    assert main(["seq"]) == 0
    out = capsys.readouterr().out
    assert out.strip()


def test_main_arch_returns_0(monkeypatch, capsys):
    payload = '{"layers":[{"name":"L1","components":["a","b"]}]}'
    monkeypatch.setattr("sys.stdin", io.StringIO(payload))
    assert main(["arch"]) == 0
    out = capsys.readouterr().out
    assert out.strip()


def test_unknown_shape_raises():
    try:
        render("bogus", {})
    except (ValueError, KeyError):
        return
    raise AssertionError("render did not reject an unknown shape")


def test_main_unknown_shape_returns_2():
    # WHY: the CLI contract promises a clean exit code 2 (not a crash)
    # for an unknown shape so callers can branch on the status.
    assert main(["bogus"]) == 2


# ---------------------------------------------------------------------------
# From ascii-graph tests/test_e2e.py
# End-to-end dogfood: oracle + generators wired together on mixed 中/日 input.
#
# These are integration smoke tests for the whole ascii-graph loop:
#
#   1. A real, display-width-aligned branching flowchart (mixed Traditional
#      Chinese / Japanese) passes the oracle end-to-end with ZERO drift —
#      the diagram below was converged by actually running it through
#      align.analyze and tuning the spacing until clean.
#   2. Corrupting one box (padding a CJK label by character count so it
#      overflows its border) makes the oracle flag drift AND makes the CLI
#      exit 1 — proving the detect direction of the loop, not just the
#      happy path.
#   3. Each generator shape renders an aligned diagram for a 中/日 payload.
#
# Integration tests of an already-wired system pass on first write; the
# load-bearing guarantee is that the CONVERGED fixture stays clean while a
# DRIFTED one is caught (test 2 is the negative control that would fail if
# the oracle stopped detecting).
# ---------------------------------------------------------------------------

# A mixed 中/日 branching flowchart, converged through align.analyze until
# every box border, seam, branch, and arrowhead lands on its display column.
# (開始受付処理 / 権限ありますか? / 画面表示 / 拒否します — start → decision →
# two leaf outcomes.) Do not "tidy" the spacing: it is display-width-exact.
CONVERGED_FLOWCHART = """\
┌─────────────────┐
│  開始受付処理   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ 権限ありますか? │
└──┬───────────┬──┘
   │           │
   ▼           ▼
┌──────────┐  ┌────────────┐
│ 画面表示 │  │ 拒否します │
└──────────┘  └────────────┘"""


def test_converged_flowchart_passes_oracle():
    """The hand-converged mixed 中/日 flowchart has zero drift end-to-end."""
    _report, issues = align.analyze(CONVERGED_FLOWCHART)
    assert issues == []


def test_oracle_catches_drift_end_to_end(tmp_path):
    """Padding one CJK box by char-count overflows it; the oracle catches it.

    This is the negative control: it proves the loop still DETECTS drift,
    so test 1's clean result is meaningful and not a dead assertion.
    """
    # Pad the decision label by character count (insert が・change ? to ？),
    # the canonical model error — char-count looks balanced but the row's
    # display width now overflows its border, so the right '│' connects to
    # nothing.
    corrupted = CONVERGED_FLOWCHART.replace(
        "│ 権限ありますか? │",
        "│ 権限がありますか？ │",
    )
    assert corrupted != CONVERGED_FLOWCHART  # the corruption actually applied

    _report, issues = align.analyze(corrupted)
    assert issues != []

    f = tmp_path / "drifted.txt"
    f.write_text(corrupted, encoding="utf-8")
    with redirect_stdout(io.StringIO()):
        rc = align.main([str(f)])
    assert rc == 1


def test_all_generator_shapes_render_aligned():
    """Each generator shape renders an aligned diagram for a 中/日 payload."""
    # table — every line must share one display width (CJK-aware columns).
    table = generate.render(
        "table",
        {
            "headers": ["項目", "状態"],
            "rows": [["注文", "完了"], ["配送", "準備中"]],
        },
    )
    table_lines = table.splitlines()
    assert len(table_lines) >= 2
    widths = {display_width(line) for line in table_lines}
    assert len(widths) == 1, f"table lines have unequal display widths: {widths}"

    # flow — multi-line, and every step label appears.
    flow = generate.render("flow", {"steps": ["受注", "検証ユーザー", "完了"]})
    assert len(flow.splitlines()) > 1
    for step in ("受注", "検証ユーザー", "完了"):
        assert step in flow

    # tree — node labels present, with branch glyphs.
    tree = generate.render(
        "tree",
        {
            "node": {
                "label": "訂單系統",
                "children": [
                    {"label": "訂單服務"},
                    {"label": "庫存サービス", "children": [{"label": "預扣"}]},
                ],
            }
        },
    )
    for label in ("訂單系統", "訂單服務", "庫存サービス", "預扣"):
        assert label in tree
    assert "├─" in tree
    assert "└─" in tree

    # bar — labels present, with the █ bar glyph.
    bar = generate.render("bar", {"pairs": [["売上", 100], ["費用", 60]], "width": 10})
    assert "売上" in bar
    assert "費用" in bar
    assert "█" in bar


# ---------------------------------------------------------------------------
# loom-visualization: standard-library-only run time
# ---------------------------------------------------------------------------

_HERE = pathlib.Path(__file__).resolve().parent

PORTED_MODULES = (
    "width", "glyphs", "align", "generate",
    "checks_seam", "checks_table", "checks_kink",
    "gen_table", "gen_flow", "gen_tree", "gen_bar", "gen_arch", "gen_seq",
)


def test_cjk_labelled_flow_passes_checks_under_python_I(tmp_path):
    # Isolated mode (-I) drops the script directory, user site-packages and
    # PYTHON* variables from the import path, so the scripts must resolve
    # their siblings themselves and need nothing beyond the standard library.
    steps = ["收到訂單", "驗證ユーザー", "在庫を確認する", "完成"]
    payload = json.dumps({"steps": steps}, ensure_ascii=False)
    gen = subprocess.run(
        [sys.executable, "-I", str(_HERE / "generate.py"), "flow"],
        input=payload, capture_output=True, text=True, encoding="utf-8", cwd=tmp_path,
    )
    assert gen.returncode == 0, gen.stderr
    for step in steps:
        assert step in gen.stdout

    check = subprocess.run(
        [sys.executable, "-I", str(_HERE / "align.py"), "-"],
        input=gen.stdout, capture_output=True, text=True, encoding="utf-8", cwd=tmp_path,
    )
    assert check.returncode == 0, check.stdout + check.stderr
    assert "no drift" in check.stdout


def test_ported_scripts_import_only_stdlib_and_siblings():
    for name in PORTED_MODULES:
        tree = ast.parse((_HERE / f"{name}.py").read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                modules = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and not node.level:
                modules = [node.module]
            else:
                continue
            for module in modules:
                top = module.split(".")[0]
                assert top in sys.stdlib_module_names or top in PORTED_MODULES, (
                    f"{name}.py imports non-stdlib module {module!r}"
                )
