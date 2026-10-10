# 外部審查須遵守使用者最後的選擇
originator: kouko
kind: engineering
needs-design: no — 既有外部審查規格已涵蓋授權與直接請求，此次修正其判定
status: confirmed 2026-10-10

## Problem
使用者明確排除某個 coding agent，或改口選擇另一個時，外部審查仍可能把被排除的 agent 視為已授權，造成不該發生的外部資料傳送。另一方面，明確的請求若被誤判，使用者可能被要求重複確認。

## Proposed outcome
Loom 能依使用者實際選擇啟動指定的外部 coding agent，拒絕與改選不會授權被排除者，明確請求也不需要第二次確認。

## Acceptance
1. 使用者明確拒絕或改選其他 coding agent 時，被排除的 agent 不會進行外部審查或任何需對外連線的準備動作。
2. 使用者明確要求某個 coding agent 審查時，Loom 能使用該 agent 執行原本的審查任務，而不再要求同一選擇的第二次確認。
3. 未能確認實際授權對象或審查範圍時，外部執行不會開始；授權成功時，現有的資料傳送告知、模型與 effort 約束仍然適用。

## Constraints
- 修正只留在本機；不推送或建立 PR。
- 不把程式碼或審查內容傳給外部 coding agent，除非有針對具體資料傳送的明確授權。
- 保留已確認的直接請求免重複確認規則。

## Out of scope
- 更改外部供應商帳戶額度或自動切換模型。
- 擴大外部 CLI 的檔案讀取權限。

## Open questions
- none
