# Prose changes stop producing mandatory executable tests — what I tried and what happened

Tried on 2026-09-27, in a clean copy of the project at 5f9a3228. How I tried each line and what came back: docs/loom/2026-09-27-prose-evidence-class/evidence/acceptance-test-evidence.md.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | 一個只改 skill 或 reference 散文的變更，其計畫中不再被要求為每個 task 附帶測試案例對；計畫能通過進場檢查並進入 Build。 | works | 既有計畫通過進場檢查，純文件任務免測試對規則經驗證有效 | — |
| 2 | 一個有行為變更的變更（改變 checker 規則、agent 行為或任何執行面），其驗收線仍被要求擁有正向加反向（或邊界）的測試案例對。 | works | 改變 .py/.sh/測試檔或受保護部件的任務仍需正向+反向測試案例對 | — |
| 3 | review 的 tests 面向文字承認散文變更的合格證據類別（checker 重算、fresh-context 審查、行為變更時的獨立驗收測試），且不再僅因散文變更未新增測試檔而開出 finding。 | works | 規則文件明確記載散文證據類別為語意審查+檢查重算+行為變更時驗收測試，純散文變更無需新增可執行測試 | — |
| 4 | 發版後，三份 plugin manifest 與 CHANGELOG 的版本同步由單一位置的重算檢查驗證；修改版號不再需要編輯多個寫死版號字串的測試檔。 | works | 三個 manifest 與 CHANGELOG 全部指向單一 CURRENT_VERSION 常數，修改該常數即可同步所有版本號 | — |
| 5 | 既有行為驗證不變：對抗探針上限、測試預算、計畫簡化檢查、獨立驗收測試各站照常運作。 | works | 對抗探針上限仍為 5，測試預算在 implementer 說明中，簡化檢查在 plan 欄位中，驗收測試站仍由 closing-review 呼叫 | — |

## 對你既有的資料做了什麼 (what this did to data you already had)

Nothing — it only touched files this change created. The change modifies loom-code internal mechanisms (rules, lenses, tests) and does not alter any existing user data or configuration files in user repositories.

## I decided for you

Nothing — every choice was either yours or forced. No additional decisions were made beyond what was specified in the intent, and no findings of severity important or worse were dismissed by the main agent during development.

## Things I am not sure you want

Nothing. All open questions in the intent were resolved during development.