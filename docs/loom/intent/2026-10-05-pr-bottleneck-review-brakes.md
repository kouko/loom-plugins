# 讓審查點名會騙人的測試、讓 PR 風險一眼看懂
originator: kouko
kind: engineering
needs-design: no — station prose and one reviewer lens row under loom-code/skills/, which the manifest classifies as the `skill` artifact type, not an interface surface (`**/cli/**`, `**/api/**`, `**/commands/**`, `**/*.tsx`, `**/templates/**`)
evidence: [docs/loom/memory/a-test-can-be-correct-and-still-unable-to-fail.md, docs/loom/memory/fixtures-mirror-producer-shape.md, loom-code/skills/closing-review/references/lenses.md, loom-code/skills/ship/SKILL.md]
status: confirmed 2026-10-05
publication: automatic — authorized 2026-10-05 by kouko

## Problem
對照 Matt Pocock 的演講「Fixing the PR Bottleneck」（AI Engineer Paris 2026），並由 Claude、Codex 與一次獨立的複雜度檢驗分別比對 loom 現況後，剩下兩個缺口：

| 缺口 | 今天的後果 |
|---|---|
| 審查只要求測試「真的跑到改動的行為」，沒有點名會騙人的測試：把實作原樣再寫一遍的測試、讀原始碼文字判斷程式結構的測試、mock 掉自己聲稱要測的那一段的測試 | 這類測試全綠但沒有保護力；repo 的記憶裡已有兩次紀錄（測試不可能失敗、mock 造出不存在的資料形狀導致上線後崩潰） |
| PR 的「風險與回滾」段落沒有說要寫什麼 | 讀 PR 的人無法一眼看出這個改動能不能撤回、出事影響多大，只能讀完全文自己判斷 |

## Proposed outcome
審查會把三種會騙人的測試各自當成問題回報；ship 寫 PR 的「風險與回滾」段落時，固定寫出能否撤回、影響範圍與回滾方式。

## Acceptance
1. closing review 的審查會把三種會騙人的測試（把實作原樣再寫一遍、讀原始碼文字判斷程式結構、mock 掉自己聲稱要測的那一段）各自當成問題回報；用一個刻意寫壞的範例改動試，三種都會被抓到。
2. loom 自己用來釘住散文規則的測試，不會因為第 1 條被當成問題。
3. ship 產生的 PR 說明，「風險與回滾」段落寫明：能否撤回（one-way／two-way door）、出事的影響範圍、回滾方式。
4. 完整 package suite 全部通過，版號與 CHANGELOG 一致。

## Constraints
- 不新增使用者決策點、checker 規則、plan 欄位或 closing review 步驟。
- 審查者仍然只下判定、不改它審的東西（writer ≠ judge）。
- 對話用繁體中文；plan、spec、verdict、commit body 等 loom 機器面 artifacts 用英文；PR 說明與驗收報告用使用者的語言。

## Out of scope
- checker 檢查 PR 是否有合併風險那一行：checker 只能確認那行存在、不能確認內容是真的，而段落非空本來就有檢查。
- 「測試只能透過模組對外的介面」與 plan 的每個 task 寫明介面：併入之後的 deep module 討論；重新考慮的條件是，有紀錄顯示審查因為看不出介面而放過一個綁死內部結構的測試。
- closing review 收尾教訓改寫成測試、檢查或規範：現有段落已規定每次零到一個教訓；重新考慮的條件是，同一類審查發現在兩次以上的改動重複出現，中間卻沒有留下任何教訓、測試或檢查。
- 把風格與結構規範從寫 code 的 agent 那邊移走：已經是如此（函式長度、命名等規則只在審查的規則表，寫 code 的 agent 不讀）。
- 依可逆程度減少使用者最後要讀的驗收報告（③ 照舊每次都要）。

## Open questions
- none
