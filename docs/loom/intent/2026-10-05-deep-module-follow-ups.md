# 補上 deep module 改動留下的三個缺口
originator: kouko
kind: engineering
needs-design: no — reviewer lens prose, one prose-pin test and one example doc under loom-code/, which the manifest classifies as skill and doc artifact types, not an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [loom-code/skills/closing-review/references/lenses.md, loom-code/tests/test_write_plan_entry_definition.py, loom-code/docs/examples/swift-network-layer.md, docs/loom/intent/2026-10-05-deep-module-boundaries.md]
status: confirmed 2026-10-05
publication: automatic — authorized 2026-10-05 by kouko

## Problem
PR #83 讓 loom 要求計畫寫明模組入口、審查依入口判定測試，merge 時留下三個缺口：

| 缺口 | 後果 |
|---|---|
| 審查規則說「改非測試程式碼的 task 要標入口」，沒說設定檔、manifest、版號檔、文件算不算 | 只改版號或設定的 task 是否被要求標入口，因 reviewer 而異 |
| 釘住 write-plan 入口定義的測試，認不出 `cannot` 這種否定寫法 | 有人把入口定義改成反義（例如「入口不能是其他模組呼叫的地方」）時，測試仍會通過，漏掉這次本來要擋的退化 |
| 範例文件裡的審查示範，仍是「出現三次就抽出」 | 讀範例的 agent 會學到 PR #83 已經改掉的舊做法 |

## Proposed outcome
三處都和 PR #83 的規則一致：只有改到可被呼叫的程式行為的 task 才需要標入口；入口定義被改成否定寫法時測試會失敗；範例只在三處會因同一個理由一起改時才抽出。

## Acceptance
1. closing review 不會要求只改設定檔、manifest、版號字串或文件的 task 標入口，改到可被呼叫的程式行為的 task 仍會被要求；用範例 task 試，只 bump 版號的 task 不被要求標入口，改函式行為卻沒標入口的 task 仍被抓。
2. 釘住 write-plan 入口定義的測試，遇到用 `cannot`（及同類否定縮寫）把入口定義反過來的句子會失敗；對目前 write-plan 的正確文字仍然通過。
3. 範例文件中要求抽出共用程式的審查意見，理由改為那幾處會因同一個理由一起改，不再只憑出現次數。
4. 完整 package suite 全部通過；三份 manifest、README 的版號字串與 CHANGELOG 新區段一致。

## Constraints
- 不改 PR #83 已確認的規則內容與門檻（入口定義、從入口能觸及的判準、只轉手的定義、長度與三次只是提示）。
- 不新增使用者決策點、plan 欄位或 checker 規則。
- 對話用繁體中文；plan、verdict、commit body 等機器面 artifacts 用英文；PR 說明與驗收報告用使用者的語言。

## Out of scope
- write-plan Task size 段落的同一個「non-test code」用詞：規劃者多標一個入口不會造成錯判，而且該檔案離字數上限只剩 1 字。
- 其他範例文件裡可能存在的同類舊寫法。

## Open questions
- none
