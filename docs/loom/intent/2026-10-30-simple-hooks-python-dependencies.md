# 讓簡單 hook 不受 Loom 檢查器套件需求影響
originator: kouko
kind: engineering
needs-design: no — 只調整既有 hook 的執行環境選擇，保留其事件、輸出格式與使用者可見行為
status: confirmed 2026-10-30
publication: automatic — authorized 2026-10-30 by kouko

## Problem
部分只使用 Python 內建功能的 Loom hook 仍先經過檢查器專用環境的依賴檢查。當該環境尚未建立或缺少套件時，hook 會收到不適用的缺依賴訊息，維護者也難以判斷實際需要修復的是哪一項功能。

## Proposed outcome
簡單 hook 可以在可用的系統 Python 上執行，不受檢查器專用套件是否安裝影響；需要完整檢查器的 hook 繼續遵守原有環境檢查及失敗處理。

## Acceptance
1. 在未建立 Loom 專用 Python 環境、但有可用系統 Python 的乾淨環境，僅使用內建功能的既有 hook 仍產生原有結果，且不顯示檢查器套件缺失訊息。
2. 需要 Loom 檢查器的發布 hook 仍在缺少必要環境時依原有規則回報並處理，不因簡單 hook 的調整而略過檢查。
3. 各主機既有 hook 的事件、輸出格式、退出狀態及完整 Loom 套件測試維持原有結果。

## Constraints
- 本次保留 Python；不移除檢查器實際需要的 `tomllib` 與 `PyYAML`。
- 不修改使用者專案資料。

## Out of scope
- 改寫 Loom 檢查器的 YAML 或 TOML 格式與解析方式。
- 變更發布政策或新增 hook 功能。

## Open questions
- none
