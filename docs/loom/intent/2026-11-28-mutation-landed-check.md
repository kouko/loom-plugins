# 用改壞證明測試有效時，先確認改動真的生效
originator: kouko
kind: engineering
needs-design: no — rule text in loom-code's shared standard and station references only; no CLI, API, UI or user-facing file artifact changes
status: confirmed 2026-11-28
intent_confirmed_sha: c609d1bd2398fc8660d1cbecf41d7b651c486bad
publication: automatic — authorized 2026-11-28 by kouko

## Problem

loom 有幾處要求「故意把程式或測試資料改壞，看測試失敗，證明測試抓得到錯」：
implementer 補寫既有程式的測試時（`loom-code/references/engineering-baseline.md`
的 False-green diagnostic 與 Code-first backfill），以及 adversary 更新自己的
對抗程式時（`loom-code/skills/closing-review/references/adversarial.md`）。
這些規則只要求「看到失敗」，沒要求確認改動真的生效。

改動沒生效（搜尋字串沒對上、改到別的檔案、改到沒被執行的副本），測試卻因為
別的原因失敗時，寫的人和審的人都會以為「測試抓得到這個錯」，其實沒抓到。
目前 adversary 的對抗程式多半自己做了這個檢查（改動錨點必須剛好出現一次、
沒改的副本先跑一次要通過），但那是習慣，不是規則；換一個 agent 或手動做改壞
測試時就沒有東西擋著。沒有找到已發生的事故，這是預防性的補強。來源是
mattpocock/skills `diagnosing-bugs` Phase 5 第 2 步，評估見
`docs/loom/research/2026-11-28-mattpocock-skills.md` 第 3 項。

## Proposed outcome

寫測試的人與審測試的人共讀的測試標準寫明：用改壞來證明測試有效時，失敗只在
兩件事都確認過後才算數 —— 改動確實生效，以及沒改的版本會通過。baseline 與
adversary 的對抗程式更新規則都指向這條，不各寫一份。

## Acceptance

1. 共用的測試標準檔中有一條規則：用故意改壞讓測試失敗來證明測試有效時，必須先確認改動確實生效（與原始版本比對有差異，或要改的那段文字剛好比對到一次），也確認沒改的版本會通過；沒確認的失敗不能當作證據。
2. implementer 讀的 engineering baseline 中，False-green diagnostic 與 Code-first backfill 這兩處「改壞看失敗」的指示都指向這條規則，不另外重述。
3. adversary 更新對抗程式時要附的改壞證據規則指向同一條，並要求報告寫出確認改動生效的方式。
4. 把這條規則刪掉、或把「必須確認」改成「可以略過」時，package suite 會有測試失敗。
5. loom-code 發布新版號，CHANGELOG 寫明這條規則。

## Constraints

- 規則只寫在共用測試標準一處；其他檔案只放指向它的連結（沿用 PR #183 的「每條規則只寫在一處」）。
- 不新增 checker 規則、不新增流程步驟；只改文字與保護文字的測試。

## Out of scope

- 要求 adversary 的 mutation 工具（mutmut、stryker 等）額外做比對；那些工具本身就確認改動生效。
- 回頭修改既有 change 的對抗程式。
- 研究紀錄第 4 項（兩軸審查分工）。

## Open questions
- none
