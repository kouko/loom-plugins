# 修正反覆出現的停止檢查提醒
originator: kouko
kind: engineering
needs-design: yes — 現有停止檢查涵蓋未發布與再次停止，但未涵蓋本次回報的正常工作期間反覆提醒；需釐清主機事件與交付檢查的適用界線。
intent_confirmed_sha: d5c19cec3c6fed4458956ada49524dc36a40bf96
status: confirmed 2026-11-11
publication: automatic — authorized 2026-11-11 by kouko

## Problem
使用者在代理處理工作期間反覆看到「Stop hook error／Delivery incomplete」訊息，必須轉貼或詢問才能了解是否真的出錯，干擾原本工作的進行。

## Proposed outcome
停止檢查能提供符合當前工作情境的提醒，不反覆干擾正常進行或等待使用者決定的工作，同時保留對不實交付完成宣稱的檢查。

## Acceptance
1. 正常工作尚在進行或等待使用者決定時，不再因尚未發布而反覆產生要求恢復發布的錯誤提醒。
2. 有效的交付完成檢查仍能辨識未發布、未確認與已完成的交付，不把缺少證據視為成功。
3. 重現結果能區分程式故障、主動阻止停止與主機顯示方式；修正於實際受影響主機的結果與未驗證範圍明確記錄。

## Constraints
- 既有 PR #140 保持待驗收，不合併也不混入本次變更。
- 不以關閉全部交付檢查或自動合併來消除提醒。

## Out of scope
- 專案計數、對話去重及其他回顧工具功能。
- 與本次停止訊息無關的主機設定重整。

## Open questions
- none
