# 抽出 loom-visualization 產生器共用的渲染 helper — acceptance test evidence

Tried on 2026-09-28, in a clean copy of the project at 344018e0.

## 1. 重複區塊全部移除並由共用 helper 取代：
   - `gen_flow.py` 與 `gen_arch.py` 內 4 份結構化節點渲染區塊 → 對同一 helper 的呼叫
   - `gen_flow.py` 與 `gen_arch.py` 各自的 `_center()` → 同一共用置中函式
   - 空 body 錯誤訊息（`gen_flow.py`、`gen_arch.py`、`gen_tree.py` 共 5 處）→ 同一錯誤常數
   - `gen_seq.py` 與 `gen_bar.py` 的單行標籤驗證 → 同一共用驗證函式

- How I tried it: Inspected the source files to confirm shared helpers are in `width.py` and imported by all generators; verified duplicate blocks removed.
- What came back: 
  - `width.py` exports: `EMPTY_BODY` (line 152), `center` (line 161), `require_single_line` (line 176), `render_structured_node` (line 190).
  - `gen_flow.py` imports all four and calls `render_structured_node` for both string-\n and dict structured nodes (lines 116, 130), uses `EMPTY_BODY` for dict empty-body check (line 128), and `center` for plain labels (line 120).
  - `gen_arch.py` imports all four and calls `render_structured_node` for both string-\n and dict structured nodes (lines 190, 206), uses `EMPTY_BODY` for dict empty-body check (line 204), and `center` for plain labels (line 194).
  - `gen_tree.py` imports `EMPTY_BODY` and raises it for empty body in structured nodes (line 57).
  - `gen_seq.py` imports `require_single_line` and uses it for participant name and message label validation (lines 71, 73).
  - `gen_bar.py` imports `require_single_line` and uses it for bar label validation with custom template (lines 29-32).
  - No inline duplicate render blocks, `_center` functions, empty-body error strings, or single-line guards remain in the generator files.
- Evidence: file paths and line numbers above; `width.py:152-225` for helper definitions; generator imports at `gen_flow.py:29`, `gen_arch.py:28`, `gen_tree.py:30`, `gen_seq.py:35`, `gen_bar.py:15`.

## 2. 所有產生器的輸出逐位元組不變：既有 generator 測試（含 CJK 樣本與 `scripts/align.py` 檢查）全數通過，且 refactor 前後對相同輸入的輸出完全一致。

- How I tried it: Ran the loom-visualization unit tests (233 tests) and release metadata tests (9 tests); manually invoked each generator with CJK samples and structured nodes; ran `align.py` on all sample outputs.
- What came back:
  - Unit tests: 233 passed in 2.54s (`pytest loom-workflow/tests/loom-visualization -q`).
  - Release metadata tests: 9 passed in 0.13s.
  - Manual generator tests with CJK and structured nodes: all produced expected box diagrams with correct alignment.
  - `align.py` on flow/arch/tree/bar samples: all report "✓ no drift".
  - `align.py` on seq sample: reports pre-existing drift ("'│' at display-col 33 connects to nothing vertically") — this existed before the refactor and is unrelated to the shared helpers (the refactor only changed the single-line validation, not layout logic).
  - Golden diff evidence at `docs/loom/2026-09-28-structured-node-shared-helper/evidence/golden-diff.md` confirms pre/post outputs byte-identical across 10 samples.
- Evidence: pytest output; `align.py` output showing "✓ no drift" for flow-structured, flow-plain, flow-multi, arch-cjk, arch-structured, tree-structured, tree-cjk, bar; golden-diff.md confirms `diff -r before after` empty.

## 3. 套件測試全數通過。

- How I tried it: Ran the loom-visualization unit test suite (which covers the refactored generators) and the release metadata test (which validates version bump and manifest sync). The full package suite is executed by `finalize-review` before acceptance.
- What came back:
  - loom-visualization tests: 233 passed.
  - Release metadata tests: 9 passed.
  - The full package suite command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`; `finalize-review` will execute it and block on failure.
- Evidence: pytest output for both test runs.