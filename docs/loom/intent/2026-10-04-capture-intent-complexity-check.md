# capture-intent 在確認前先檢驗範圍值不值得
originator: kouko
kind: engineering
needs-design: no — guidance text in an existing station; no new field, rule, command, decision point or file artifact
evidence: [loom-design/skills/capture-intent/SKILL.md, docs/loom/intent/2026-10-04-code-first-backfill-guidance.md]
status: confirmed 2026-10-04
publication: automatic — authorized 2026-10-04 by kouko

## Problem
使用者在 capture-intent 提出或考慮一個成本明顯的範圍（整套新機制、新欄位、新規則、新步驟）時，沒有任何一站在確認 intent 之前問「這個範圍值不值得它的成本」。簡化檢查要等到 plan 或程式碼已經存在才會發生。

| 發生日期 | 變更 | 後果 |
|---|---|---|
| 2026-10-01 | 2026-10-01-remove-expert-mode | 臨時另派一個 agent 做檢驗 |
| 2026-10-04 | 2026-10-04-code-first-backfill-guidance | intent 重寫兩輪、外部審查兩次後，使用者手動要求複雜度檢驗才判定 RESHAPE，範圍縮成一段說明 |

## Proposed outcome
範圍成本明顯時，capture-intent 在確認前自動做一次複雜度檢驗，把結果和較小的替代做法放進同一則確認訊息，讓使用者一次決定；使用者不必自己記得要求檢驗。

## Acceptance
1. capture-intent 說明：當使用者的要求或討論中的選項會新增機制、欄位、規則或步驟時，確認前先執行一次複雜度檢驗（loom-workflow 的 critique，complexity 模式）。
2. 檢驗的判定與較小的替代做法，出現在決策點 ① 的同一則訊息裡；不新增停點，最後仍由使用者選擇。
3. 修 bug、改措辭這類不增加成本的要求，不觸發檢驗。
4. 沒有安裝 loom-workflow 時，capture-intent 的行為跟現在完全一樣。
5. 完整 package suite 全部通過，版號一致。

## Constraints
- 不新增 loom-design skill（會與 critique 重複）、決策點、intent 欄位或 checker 規則。
- 只用公開的 skill 名稱引用 loom-workflow，不引用它的內部檔案（plugin 邊界）。
- 對話用繁體中文；plan、spec、verdict、commit body 等 loom 機器面 artifacts 用英文。

## Out of scope
- loom-design 未安裝時由 write-plan 代跑的確認流程。
- 改變 critique 本身的判斷方式。
- write-spec、write-plan、closing-review 既有的簡化檢查。

## Open questions
- none
