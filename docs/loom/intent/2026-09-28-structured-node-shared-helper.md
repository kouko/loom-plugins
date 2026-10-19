# 抽出 loom-visualization 產生器共用的渲染 helper
originator: kouko
kind: engineering
needs-design: no — 純內部 refactor：只動 `scripts/` 下產生器與檢查器的內部實作（不觸及 `**/templates/**`、`**/cli/`、`**/api/` 等 interface-surface globs），無使用者可見行為變更
status: confirmed 2026-09-28

## Problem
前一個變更（#62，統一框狀節點文字結構）把「標題／分隔線／內文」的三段式渲染寫進了 `scripts/gen_flow.py` 與 `scripts/gen_arch.py`，但同一段邏輯在兩檔各重複了兩份（字串 `\n` 分支一份、dict 分支一份），共 4 份近乎相同的程式碼。同樣的重複也散布在其他產生器與檢查器之間：`_center()` 置中函式在兩檔重複、空 body 錯誤訊息在 3 檔出現 5 次、單行標籤驗證在 seq 與 bar 重複。未來任何節點樣式或渲染行為調整都必須在多處同步修改；漏改一處就讓不同圖形產生器的行為悄然分歧。

## Proposed outcome
`scripts/width.py`（既有共用模組）集中提供產出器共用的渲染與驗證 helper：結構化節點（標題列／分隔線／寬度感知換行之內文列）渲染、置中、空 body 錯誤常數、單行標籤驗證。`gen_flow.py`、`gen_arch.py`、`gen_tree.py`、`gen_seq.py`、`gen_bar.py` 的重複區塊全部替換為對這些 helper 的呼叫；所有產生器的輸出與現在逐位元組相同。

## Acceptance
1. 重複區塊全部移除並由共用 helper 取代：
   - `gen_flow.py` 與 `gen_arch.py` 內 4 份結構化節點渲染區塊 → 對同一 helper 的呼叫
   - `gen_flow.py` 與 `gen_arch.py` 各自的 `_center()` → 同一共用置中函式
   - 空 body 錯誤訊息（`gen_flow.py`、`gen_arch.py`、`gen_tree.py` 共 5 處）→ 同一錯誤常數
   - `gen_seq.py` 與 `gen_bar.py` 的單行標籤驗證 → 同一共用驗證函式
2. 所有產生器的輸出逐位元組不變：既有 generator 測試（含 CJK 樣本與 `scripts/align.py` 檢查）全數通過，且 refactor 前後對相同輸入的輸出完全一致。
3. 套件測試全數通過。

## Constraints
- 產生器維持僅用 Python 標準庫。
- 這是純 refactor：任何節點渲染行為（樣式、對齊、寬度計算、錯誤訊息）都不變。
- `gen_table.py`、`align.py` 等未被識別為重複的檔案保持原狀（除非共用 helper 的引入自然涉及它們，則僅限 import 取代、不改行為）。
- skill 資料夾扁平、SKILL.md token 上限等 repo 慣例照舊。

## Out of scope
- 節點樣式的任何行為變更（含上一個變更的 follow-up 之外的新樣式決策）。
- 非重複程式碼的重構（如 `gen_arch.py` 內部的 `_pad_line`、`gen_table.py` 的 `_pad`——兩者語意不同，不合併）。
- 上一個變更遺留的其他 follow-up（無）。

## Open questions
- none
