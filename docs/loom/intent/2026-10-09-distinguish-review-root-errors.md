# 區分審查目錄與外部 CLI 缺失
originator: kouko
kind: engineering
needs-design: no — 既有外部審查規格已涵蓋失敗狀態，此次只修正錯誤原因分類
status: confirmed 2026-10-10

## Problem
外部審查開始時，若指定的本機審查目錄不存在，使用者會看到「外部 CLI 未安裝」，因此可能檢查錯誤的地方，無法判斷審查為何沒有完成。

## Proposed outcome
外部審查失敗時，Loom 能把審查目錄不存在與外部 CLI 不存在區分開，並保留失敗狀態。

## Acceptance
1. 指定的審查目錄不存在時，使用者能看到指向目錄的明確原因，且該次審查不會算完成。
2. 外部 CLI 不存在時，使用者仍能看到指向 CLI 的明確原因。
3. 兩種失敗都不會洩露原始錯誤文字或與原因無關的資料；有效目錄與 CLI 的現有結果維持可用。

## Constraints
- 保留目前的授權、資料傳送、明確模型與 effort 選擇規則。
- 修正只留在本機；不推送或建立 PR。

## Out of scope
- 改變外部供應商帳戶額度或自動切換模型。
- 擴大外部 CLI 的檔案讀取權限。

## Open questions
- none
