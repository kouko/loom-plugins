# agent 的回報寫進檔案，盲跑排在內容凍結之後

originator: kouko
kind: engineering
needs-design: no — agent contracts and one station's prose under loom-code/agents/ and loom-code/skills/, which the manifest classifies as the `skill` artifact type, not an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [loom-code/agents/adversary.md, loom-code/agents/reviewer.md, loom-code/agents/implementer.md, loom-code/agents/blind-runner.md, loom-code/skills/closing-review/SKILL.md]
status: withdrawn — 兩位獨立審查員在第一輪指出，兩個半邊各自是協定的重新設計而非散文修改：排序規則在實際管轄該步驟的那一句底下三個條件自動成立因而無效，在同一站另一句較鬆的敘述底下則會生效但與前者矛盾；回報寫檔案的規則沒有任何已提交的文字要求派工端指定路徑，安全分支只靠習慣維持。教訓寫入 docs/loom/memory/an-ordering-rule-that-is-vacuous-at-its-own-trigger-changes-nothing.md

## Problem

兩件在 2026-09-20 這天實測到的浪費，都不是判斷錯誤，是流程形狀造成的。

**一、agent 的回報被截斷。** agent 把結果當成訊息回傳，長的回報在送達前被切斷，協調者必須再問一次。這天發生約八次，每次都是一個來回。被切掉的往往是最後面的部分 —— 也就是結論、未解決事項、以及對自己工作的保留。

**二、盲跑報告被迫重走三次。** 盲跑報告是使用者用來驗收的文件，但它在功能內容還會變動的時候就先做了。這天每一次修補落地，報告裡逐字引用的輸出就跟程式對不上，於是重走。第一次重走還讓使用者差點收到一份把「已經修好的問題」寫成「已知限制」的驗收文件。

## Proposed outcome

agent 的回報落在檔案裡，訊息只帶路徑，所以長度不再造成資訊遺失。盲跑排在功能內容不再變動之後，所以報告產出一次就有效。

## Acceptance

1. 四個 agent 契約都說明回報寫進檔案、訊息只回路徑。
2. 結案審查站說明盲跑在功能內容凍結後才做，並說明「凍結」是什麼意思。
3. 沒有任何閘門、規則或檢查被放寬；既有測試全部通過。

## Constraints

- 只改散文，不改檢查器程式。
- 不改變任何 agent 的職責界線（誰能改什麼、誰產出判定）。
- 機器面輸出維持英文。

## Out of scope

- 把儀式規模改成機械計算（小改動不寫規格／計畫／盲跑）—— 那是更大的變更，另案。
- 對抗測試數量的精簡 —— 已登記在 memory 紀錄裡。
- 其他三道守門員（dcg、CC Safety Net、權限拒絕清單）造成的打字。

## Open questions

- none
