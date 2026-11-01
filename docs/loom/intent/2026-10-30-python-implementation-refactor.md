# 整理 Decision Map 核心 Python 工具的模組邊界
originator: kouko
kind: engineering
needs-design: no — 保持既有指令、hook 與檔案格式的外部行為，只整理 Python 內部實作
status: confirmed 2026-10-30
publication: automatic — authorized 2026-10-30 by kouko

## Problem
Loom 的核心 Python 工具已有部分模組化，但 Decision Map 的讀取、驗證和交易程式仍透過相容入口呼叫其他模組的內部函式。維護者修改其中一項能力時，難以直接看出它的責任歸屬與影響範圍，也難以判斷哪些既有結構應保留。

## Proposed outcome
先整理 Decision Map 的現有 Python 實作，讓讀取、驗證及交易能力的責任歸屬、模組入口與相依方向更清楚，後續修改可在較小範圍完成。

## Acceptance
1. Decision Map 的讀取、驗證及交易能力各有可辨認的負責模組與入口；修改、加入或移除其中一項能力時，不必同步修改無關能力的實作。
2. 重構前後，Decision Map 工具對相同有效與無效輸入的結果、退出狀態及既有資料處理結果維持一致。
3. Decision Map 的既有測試與完整 Loom 套件測試通過，且沒有因重構而增加只轉手的模組或不必要的對外入口。

## Constraints
- 保留 Python 作為本次實作語言；本次不以 Go 重寫。
- 不改變現有插件對使用者提供的指令、hook 行為或資料格式。
- 不修改使用者現有資料。

## Out of scope
- Go 改寫及預編譯執行檔的交付。
- 新增插件功能或變更使用者可見行為。
- 這一批不整理其他插件的 Python 工具。

## Open questions
- none
