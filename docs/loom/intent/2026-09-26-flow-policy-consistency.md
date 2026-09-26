# 修正三項流程判斷落差
originator: kouko
kind: engineering
needs-design: no — restores existing reviewer, test-discovery and explicit-selection contracts; no new interface or uncovered behavior
status: confirmed 2026-09-26

## Problem
Loom 使用者目前可能在修改架構規則時得到過少的驗證，使用合法測試命名卻沒有執行測試，或明確保留驗證後仍取得缺少該驗證的有效證明。

## Proposed outcome
架構規則、測試探索與明確保留的驗證都受到既有流程一致處理，使用者能信任驗證結果所代表的工作。

## Acceptance
1. 架構規則文件的變更得到與其他受保護規則文件一致的審查及自動略過判斷。
2. 宣告支援的兩種 Python 測試檔名都會被執行；失敗能反映在套件結果，原有分組及排除範圍保持有效。
3. 已確認選擇所保留的驗證不會被自動略過；產生與驗證審查證明採相同要求，未綁定選擇時仍保有既有自動略過行為。

## Constraints
- 使用現有複雜度控制，採最小修正與既有測試資源。
- 同步直接相關的流程敘述及版本資訊，揭露既有審查證明重新驗證的影響。

## Out of scope
- 略過規格或計畫後的文件依賴問題。
- 計畫階段對小改動的判斷，以及未確認架構草稿是否生效。
- 發布及合併。

## Open questions
- none
