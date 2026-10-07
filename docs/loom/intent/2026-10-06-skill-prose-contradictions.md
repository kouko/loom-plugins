# 修正 write-plan 與 closing-review 文件裡互相矛盾的四處規則
originator: kouko
kind: engineering
needs-design: no — skill prose under loom-code/skills/ and loom-design/skills/capture-intent/SKILL.md, which the manifest classifies as the skill artifact type, not an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [loom-code/skills/write-plan/SKILL.md, loom-code/skills/write-plan/references/one-way-door.md, loom-code/skills/write-plan/references/confirm-intent.md, loom-code/skills/write-plan/references/codex-first-contact.md, loom-design/skills/capture-intent/SKILL.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/skills/closing-review/references/adversarial-code.md, loom-code/skills/closing-review/references/lenses.md]
status: confirmed 2026-10-06
publication: automatic — authorized 2026-10-06 by kouko

## Problem
2026-10-06 的 skill 一致性檢查找到四處規則互相矛盾，Claude 與 Codex 各自回原檔核對後都確認存在。照字面逐條遵守的 agent 會做錯：

| 矛盾 | 後果 |
|---|---|
| product 改動中無法回頭的選擇：一份文件說在 ② 問，① 的訊息說明卻要求全部在 ① 問 | 規格還沒寫出來時就問使用者無法回頭的決定，使用者看不出後果 |
| Codex 的授權停頓被說成「每個 repo 第一次使用時」，但授權實際綁在已安裝的 plugin 上 | agent 會預告、甚至等待一個不存在的授權提示，或把 repo 自己的 hook 提示誤認成 loom 的 |
| adversary 的攻擊階段：一份說「不寫新程式」，另一份說「寫可執行的案例並執行」 | adversary 可能不敢先試跑，也可能在攻破前就提交程式 |
| 已轉正進測試資料夾的 probe：一條說 reviewer 不跑 adversarial 程式，另一條說 reviewer 要跑改過的測試檔 | reviewer 對同一個檔案收到相反指示 |

## Proposed outcome
四處都只剩一種讀法：product 的無法回頭選擇在 ② 問、engineering 的在 ① 問；Codex 授權停頓的說明符合實際觸發時機；adversary 先試跑、只提交攻破的程式；已轉正的 probe 被當作一般測試檔，由 reviewer 照跑。

## Acceptance
1. ① 的訊息說明與 one-way door 規則一致：product 改動的無法回頭選擇在 ② 問，engineering 的在 ① 問；loom-code 與 loom-design 兩邊說法相同。
2. 所有提到 Codex 授權停頓的地方，都說它在 plugin 新裝或更新時出現，不再說是每個 repo 第一次使用時。
3. adversary 的規則清楚區分攻擊時試跑的案例與最後提交的程式，兩份文件不再互相衝突。
4. reviewer 的規則對已轉正進測試資料夾的 probe 只給一種指示：當作改過的測試檔照跑。
5. 對這幾個 skill 重跑一致性檢查時，上述四點不再被列為矛盾；完整 package suite 通過，loom-code 與 loom-design 的版號字串與 CHANGELOG 新區段一致。

## Constraints
- 只改文字，不改流程、不改 checker 規則、不新增決策點或欄位。
- 各 SKILL.md 不得超過字數上限（write-plan 只剩 1 字空間）。
- 對話用繁體中文；plan、verdict、commit body 等機器面 artifacts 用英文；PR 說明與驗收報告用使用者的語言。

## Out of scope
- 一致性檢查列出的其他 12 個低信心疑點。
- write-plan 與 closing-review 之間的用詞差異（「non-test code」對「新增或改變函式行為」）。

## Open questions
- none
