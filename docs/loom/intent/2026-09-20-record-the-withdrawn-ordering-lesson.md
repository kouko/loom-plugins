# 把一次未收斂變更的教訓與撤回紀錄放進主線

originator: kouko
kind: engineering
needs-design: no — two records under docs/loom/, no code and no station prose; the manifest classifies neither path as an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [docs/loom/memory/an-ordering-rule-that-is-vacuous-at-its-own-trigger-changes-nothing.md, docs/loom/intent/2026-09-20-cheaper-agent-returns-and-blind-run-order.md]
status: confirmed 2026-09-20
publication: automatic — authorized 2026-09-20 by kouko

## Problem

2026-09-20 有一次變更在終局審查輪被判未收斂，流程因此終止。它產出的兩份紀錄只存在於那條分支上，主線沒有：一份是兩個缺陷形狀的教訓，一份是那次嘗試本身的撤回紀錄（試了什麼、為什麼撤）。

維護者要移除那條分支。分支一旦刪除，這兩份紀錄就永久消失 —— 包括「有人試過這件事」這個事實本身。

流程本身給的出路是「搭下一個變更的順風車」，但這個 repo 目前沒有正在進行、又適合夾帶的變更，而那兩份紀錄的價值不該取決於下一個變更什麼時候發生。

## Proposed outcome

那兩份紀錄進入主線，成為任何人日後查得到的內容；那條未收斂的分支可以安全刪除。

## Acceptance

1. 主線上存在那則教訓紀錄，內容與被審查過的版本一致。
2. 主線上存在那份撤回的需求紀錄，狀態仍是撤回，理由仍在。
3. 記憶庫的索引與內容一致，既有測試全部通過。

## Constraints

- 只新增紀錄，不改任何程式、站說明或 agent 契約。
- 那則教訓紀錄的內容不再修改 —— 它已經過三輪審查，最後一版是審查員逐條要求下改出來的強度。
- 機器面輸出維持英文。

## Out of scope

- 重做被撤回的那兩個改動（排序規則、回報寫檔案）—— 它們是協定的重新設計，要各自的需求。
- 對「終局輪判不過就終止」這條規則本身的任何修改。

## Open questions

- none
