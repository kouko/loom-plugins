# 補齊 PR #86 留下的兩處小缺口：否定字檢查與「② 不重問」
originator: kouko
kind: engineering
needs-design: no — skill prose under loom-code/skills/ and loom-design/skills/ plus tests under loom-code/tests/, which the manifest classifies as skill and test artifacts, not an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [loom-code/tests/test_write_plan_shape_text.py, loom-code/tests/test_adversarial_product_one_way_door_without_spec.py, loom-code/scripts/prose_pin.py, loom-code/skills/write-plan/SKILL.md, loom-code/skills/write-plan/references/one-way-door.md, loom-code/skills/write-plan/references/confirm-intent.md, loom-design/skills/capture-intent/SKILL.md, loom-design/skills/write-spec/SKILL.md, loom-design/skills/write-spec/references/ui-flows.md]
status: confirmed 2026-10-07
publication: automatic — authorized 2026-10-07 by kouko

## Problem
PR #86 merge 時留下兩個已知缺口：

| 缺口 | 後果 |
|---|---|
| PR #86 新增的兩個文字檢查測試只認得 never、not、nothing、nor、n't 這幾個否定字，比 repo 共用的否定字清單少了 no、cannot、without、neither、nobody 等 | 有人把規則改成用這些字否定的句子時，測試仍會通過，守衛失效 |
| 「不寫 spec 的 product 改動，其無法回頭的選擇在 ① 問過後，之後若寫了 spec，② 不再重問」這條例外只寫在 ① 的說明裡；規定 ② 怎麼做的流程說明（write-plan、one-way-door 規則、write-spec 及其 UI 流程參考）只說要問這次改動的所有無法回頭選擇 | 照 ② 的說明走的 agent 會把 ① 已問過的選擇再問一次 |

## Proposed outcome
兩個測試用與 repo 其他文字檢查相同的否定字判斷；② 的說明也寫明 ① 已問過的 product 無法回頭選擇不再重問。

## Acceptance
1. 兩個測試遇到用 no、cannot、without、neither 或 nobody 否定的句子時會失敗，並各有對應的自我測試證明這一點。
2. 所有規定 ② 怎麼做、且說 ② 要問 product 無法回頭選擇的流程說明，都寫明 ① 已問過的不再重問，且與 ① 的說法一致。
3. 完整 package suite 通過，loom-code 與 loom-design 的版號字串與 CHANGELOG 新區段一致。

## Constraints
- 只改文字與測試，不改流程、不改 checker 規則、不新增決策點或欄位。
- 各 SKILL.md 不得超過字數上限（write-plan 只剩 1 字空間）。
- 對話用繁體中文；plan、verdict、commit body 等機器面 artifacts 用英文；PR 說明與驗收報告用使用者的語言。

## Out of scope
- PR #86 Follow-ups 中的另外兩項：① 與 ② 之間才發現的無法回頭選擇、一致性檢查的低信心疑點。
- 其他既有文字檢查測試的否定字判斷。
- 開場提示、manifest、AGENTS.md、各語言 README 與 test-prompts 等概要性說明裡的同一例外（user-decided 2026-10-07：只改流程說明）。

## Open questions
- none
