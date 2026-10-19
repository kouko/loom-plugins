# 讓入口定義測試回到整句判斷
originator: kouko
kind: engineering
needs-design: no — one prose-pin test and one wording change in write-plan SKILL.md under loom-code/, which the manifest classifies as test and skill artifact types, not an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [loom-code/tests/test_write_plan_entry_definition.py, loom-code/skills/write-plan/SKILL.md, loom-code/references/engineering-baseline.md, docs/loom/intent/2026-10-05-deep-module-follow-ups.md]
status: confirmed 2026-10-06
publication: automatic — authorized 2026-10-06 by kouko

## Problem
PR #84 讓釘住 write-plan 入口定義的測試把句子按分號切開、逐段判斷，因為那一句裡有一個合法的否定詞。後果有兩個：

| 後果 | 影響 |
|---|---|
| 有人在入口定義那一句用分號接上一段否定、把定義推翻時，測試仍通過 | PR #83 要擋的退化（入口被定義成測試呼叫的地方）可能漏過去 |
| 測試比 repo 自己的規範寬鬆：規範要求同一句出現任何否定詞就拒絕 | 測試與它依據的規範不一致，下一位讀者會以為逐段判斷是被允許的 |

## Proposed outcome
測試回到整句判斷，與 repo 規範一致；write-plan 那一句換一個不含否定詞的說法，意思不變；測試註明它只是便宜的固定檢查，不保證語意。

## Acceptance
1. 在入口定義那一句裡，用分號接上一段否定把它推翻，測試會失敗。
2. write-plan 目前的入口定義文字經改寫後仍讓測試通過，意思與原本相同，字數不增加。
3. 測試本身說明它只是固定檢查，抓不到所有反義寫法。
4. 完整 package suite 全部通過；三份 manifest、README 的版號字串與 CHANGELOG 新區段一致。

## Constraints
- 不改 PR #83 已確認的入口定義、判準與門檻。
- write-plan SKILL.md 的字數不得超過上限（目前只剩 1 字空間）。
- 不新增使用者決策點、plan 欄位或 checker 規則。
- 對話用繁體中文；plan、verdict、commit body 等機器面 artifacts 用英文；PR 說明與驗收報告用使用者的語言。

## Out of scope
- 「rather than」「instead of」「neither … nor」等反義寫法的偵測：業界經驗顯示關鍵字清單補不完，這類語意交給 closing review 的 reviewer。
- write-plan Task size 段落的「non-test code」用詞（同 2026-10-05-deep-module-follow-ups 的理由）。
- 其他 prose-pin 測試。

## Open questions
- none
