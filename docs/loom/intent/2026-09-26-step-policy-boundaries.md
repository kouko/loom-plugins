# 修正略過步驟與架構規則的生效邊界
originator: kouko
kind: engineering
needs-design: no — restores existing optional-step and architecture-ratification contracts; internal station/checker behavior is already defined
status: confirmed 2026-09-26

## Problem
Loom 使用者允許略過步驟後仍可能被缺少文件阻擋；尚未完成的工作可能被過早簡化；未確認的架構草稿也可能成為強制要求。

## Proposed outcome
略過選擇與後續文件需求一致，未完成工作不被過早簡化，架構規則只在確認後生效。

## Acceptance
1. 使用者可直接用自然語言要求略過步驟，不必新增確認碼或額外操作；未略過的要求仍有效。
2. 略過規格或計畫後可以繼續工作，不再被該文件或其衍生要求阻擋。
3. 實作前不因目前只有需求或計畫提交而自動略過必要步驟；完成後的簡化仍以實際內容判斷。
4. 未確認的架構草稿不約束規劃、審查或日常測試；已確認規則仍有效。
5. 修正沿用既有資料與流程，沒有新增持久狀態、確認流程或重複的判斷系統。

## Constraints
- 三項一起修正，採最小必要改動，保留目前使用者指示 agent 跳過步驟的能力。
- 不降低未略過驗證的要求，不把缺少驗證冒稱為通過。

## Out of scope
- 新的流程平台、儲存格式或權限系統。

## Open questions
- none
