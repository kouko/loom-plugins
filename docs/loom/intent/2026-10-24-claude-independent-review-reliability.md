# 讓 Claude Code 獨立審查在完整變更上可靠完成
originator: kouko
kind: engineering
needs-design: yes — Claude 審查的失敗原因與恢復指引會呈現給使用者，現有設計文件未涵蓋這種錯誤；審查成功、執行失敗與未完成的結果也需要明確區分
status: confirmed 2026-10-24
publication: automatic — authorized 2026-10-24 by kouko

## Problem

使用者要求 Claude Code 獨立審查完整變更時，預檢可能成功，正式審查卻因反覆壓縮而中止。使用者拿不到審查結論，Loom 只回報未知錯誤，無法判斷是否值得重試或如何排除問題。目前只證明直接呼叫 Claude Code 可以在完整材料上完成審查，尚未證明 Loom 的審查入口可行。

## Proposed outcome

使用者透過 Loom 要求 Claude Code 獨立審查完整變更時，能取得可歸屬、可供既有審查流程使用的結果；若執行失敗，能辨識原因，且未完成的審查不會被當成通過。

## Acceptance

1. 已授權的 Claude Code 獨立審查透過 Loom 的正式入口，能對先前失敗的完整規模材料完成審查，並交回可供既有審查流程使用、具模型歸屬的結果。
2. 審查執行時只取得已授權且必要的材料，不修改被審查的工作樹；使用者既有 Claude Code 全域設定不因這次審查而改變。
3. 當 Claude Code 再次因反覆壓縮中止，Loom 明確回報未完成與可辨識的原因，且對外結果不含原始提示、審查內容或敏感錯誤輸出。
4. 既有授權檢查仍會阻止未授權的外部審查；其他審查執行器及一般成功、失敗路徑保持可用。

## Constraints

- 保留外部審查對供應商、模型、成本、資料外傳及本機檔案讀取的明確授權與揭露要求。
- 保留審查者唯讀、獨立判讀及原始審查材料不進入公開失敗結果的既有要求。

## Out of scope

- 更換審查供應商或模型。
- 自動重試失敗的外部審查，或把失敗當成審查通過。
- 修改 Claude Code 的全域使用者設定。
- 修正這次審查提出的其他程式碼問題。

## Open questions

- none
