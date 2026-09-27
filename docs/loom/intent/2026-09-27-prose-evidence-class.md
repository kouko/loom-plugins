# Prose changes stop producing mandatory executable tests
originator: kouko
kind: engineering
needs-design: no — review-lens text, plan intake rule text and test placement in loom-code; skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-27
publication: automatic — authorized 2026-09-27 by kouko

## Problem
Loom 強迫每一種變更（包括純散文變更）都附帶可執行測試：review 的 tests 面向只承認「先失敗後通過」的可執行證據，而計畫的每個 task 又都必須各帶一對測試案例。採用 loom 的 repo 產品本身是散文（skill 指令檔），散文沒有執行結果可比對，唯一能滿足要求的方式就是寫出斷言句子字面的測試。這類測試每次潤稿都碎、抓不到真實回歸，數量持續累積（本 repo 225 個測試檔中有 166 個在斷言散文）；另外每個發版 PR 都還要額外修改一個寫死版號的測試檔。受影響的是所有採用 loom 的 repo 與其使用者：測試維護成本被機制放大，測試庫裡大量測試不對應任何可執行行為。

## Proposed outcome
執行型散文（skill 指令、agent 契約、規則 reference）的合格證據從「字面感應測試」改為既有的語意層與行為層：fresh-context 語意審查（既有 closing-review reviewer，非新增 LLM 呼叫）、行為有變時的獨立驗收測試（既有 AT 站）、checker 結構重算（既有規則）；字面感應測試只保留給 checker 表達不了的文法級不變量。說明型散文與 docs/loom 工作文件維持現狀（本來就無測試，靠 schema 重算與審查）。計畫的測試案例對要求從「每個 task 各一對」改為「每條驗收線在整個變更內被某個 task 擁有一對」，純文件／發版類 task 免附測試對、其證據指向既有檢查站。版本同步檢查合併到單一位置的重算檢查，發版 PR 不再編輯多個寫死版號字串的測試檔。

## Acceptance
1. 一個只改 skill 或 reference 散文的變更，其計畫中不再被要求為每個 task 附帶測試案例對；計畫能通過進場檢查並進入 Build。
2. 一個有行為變更的變更（改變 checker 規則、agent 行為或任何執行面），其驗收線仍被要求擁有正向加反向（或邊界）的測試案例對。
3. review 的 tests 面向文字承認散文變更的合格證據類別（checker 重算、fresh-context 審查、行為變更時的獨立驗收測試），且不再僅因散文變更未新增測試檔而開出 finding。
4. 發版後，三份 plugin manifest 與 CHANGELOG 的版本同步由單一位置的重算檢查驗證；修改版號不再需要編輯多個寫死版號字串的測試檔。
5. 既有行為驗證不變：對抗探針上限、測試預算、計畫簡化檢查、獨立驗收測試各站照常運作。

## Constraints
- 不新增 checker 規則、不新增參考文件檔、不新增 LLM 呼叫；只用現有機制重新定位。
- lens 的 dimension 定義行由 reviewer 執行、checker 不重算，此既有定位需在文字上明示（明確化而非新增豁免）。
- 可逆條件（收回條款）：散文變更合併後，若發生「某缺陷本可被移除前的字面感應層擋下」且在後續使用中被發現，即把 tests lens 的散文證據條款還原。
- 存量散斷言測試的逐檔清理不屬於本次變更。
- 檔案分類沿用既有 reviewer-floor 的路徑分類器。

## Out of scope
- 清理既有的散文斷言測試存量。
- 為散文引入 LLM 評審或 golden-set 行為評估。
- 變更對抗探針、測試預算或簡化檢查的現行機制。

## Open questions
- none
