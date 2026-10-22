# 修復 Claude Code 獨立審查失敗與錯誤診斷
originator: kouko
kind: engineering
needs-design: yes — 審查失敗時呈現給使用者的診斷會改變，目前沒有涵蓋這個輸出的設計文件
status: confirmed 2026-10-22
publication: automatic — authorized 2026-10-22 by kouko

## Problem
使用者要求 Claude Code 做獨立審查時，短暫預檢可能成功，正式審查卻失敗且沒有審查結論。Loom 只回報「unknown error」，使使用者與維護者無法判斷失敗原因，也無法可靠地決定如何恢復審查。

## Proposed outcome
在 Claude Code 可正常執行時，Loom 能完成獨立審查；執行失敗時，Loom 提供足以定位問題且不洩漏審查內容的診斷，並清楚區分失敗與已完成的審查。

## Acceptance
1. 在已授權且 Claude Code 可正常執行的環境中，正式審查能在預檢後完成，並交回可歸屬的審查內容。
2. 正式審查失敗時，使用者或維護者能取得足以區分可辨識故障與未知故障的安全診斷及下一步；原始審查材料不會出現在對外結果中。
3. 沒有完成的 Claude Code 審查不會被記成成功的審查或審查結論；既有授權範圍與其他執行器的行為仍有效。

## Constraints
- 保留外部審查的明確授權與資料外傳揭露要求。
- 不將原始提示、審查內容或可能含敏感資訊的完整錯誤輸出寫入公開結果。
- 這是 PR #105 之後的獨立變更，不修改已合併的 Python 環境修復。

## Out of scope
- 改用其他審查供應商來代替 Claude Code。
- 把審查失敗視為已通過，或自動略過必要的審查。
- Go 重寫或降低 Python 版本需求。

## Open questions
- none
