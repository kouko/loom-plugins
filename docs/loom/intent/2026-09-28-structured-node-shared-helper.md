# 抽出 loom-visualization 產生器共用的結構化節點渲染 helper
originator: kouko
kind: engineering
needs-design: no — 純內部 refactor：只動 `scripts/gen_flow.py` 與 `scripts/gen_arch.py` 的內部實作，不觸及 interface-surface globs（`**/cli/`、`**/api/`、`**/commands/`、`**/*.tsx`、`**/templates/**`），無使用者可見行為變更
status: open

## Problem
前一個變更（#62，統一框狀節點文字結構）把「標題／分隔線／內文」的三段式渲染寫進了 `scripts/gen_flow.py` 與 `scripts/gen_arch.py`，但同一段邏輯在兩檔各重複了兩份（字串 `\n` 分支一份、dict 分支一份），共 4 份近乎相同的程式碼。未來任何節點樣式調整（分隔線記號、內距、換行預算）都必須同步改 4 處；漏改一處就讓流程圖與架構圖的行為悄然分歧。

## Proposed outcome
`scripts/width.py`（或其他共用模組）提供一個渲染「標題列／分隔線／寬度感知換行之內文列」的 helper；`gen_flow.py` 與 `gen_arch.py` 的 4 份內嵌重複區塊全部替換為對該 helper 的呼叫；兩產生器的輸出與現在逐位元組相同。

## Acceptance
1. `gen_flow.py` 與 `gen_arch.py` 內不再含有重複的結構化節點渲染區塊——4 個重複位置全部由對同一個共用 helper 的呼叫取代。
2. 兩產生器的輸出逐位元組不變：既有 generator 測試（含 CJK 樣本與 `scripts/align.py` 檢查）全數通過，且 refactor 前後對相同輸入的輸出完全一致。
3. 套件測試全數通過。

## Constraints
- 產生器維持僅用 Python 標準庫。
- 這是純 refactor：任何節點渲染行為（樣式、對齊、寬度計算、錯誤訊息）都不變。
- 未抽取的檔案（`gen_tree.py`、`gen_seq.py`、`gen_bar.py`、`gen_table.py`）保持原狀。
- skill 資料夾扁平、SKILL.md token 上限等 repo 慣例照舊。

## Out of scope
- 節點樣式的任何行為變更（含上一個變更的 follow-up 之外的新樣式決策）。
- 其他產生器的重構。
- 上一個變更遺留的其他 follow-up（無）。

## Open questions
- none
