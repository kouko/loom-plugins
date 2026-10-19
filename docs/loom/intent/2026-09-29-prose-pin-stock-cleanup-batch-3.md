# 清理散文斷言測試存量（第三批）並補發版號
originator: kouko
kind: engineering
needs-design: no — 純內部測試、證據與版號清理，不觸及任何介面表面（manifest globs 之外）
evidence: [docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/census-report.md]
status: confirmed 2026-09-29
publication: automatic — authorized 2026-09-29 by kouko

## Problem
第二批清理（PR #65）後，普查腳本報「句子釘住 = 0」，但它看不到「直接把整句寫死在測試裡比對」的寫法；已知仍有 7 個測試檔這樣做（清單在 evidence 的 Batch-3 段）。潤稿落在這些檔檢查的 skill／reference 上，測試照樣變紅，「改散文幾乎不用動測試」的目標還沒達成。另外第二批沒有升版號，已安裝的副本拿不到第一批之後的測試變更。

## Proposed outcome
普查腳本看得到「直接把 skill／reference 整句寫死在測試裡比對」的寫法（比對程式輸出的不算），已知的 7 個檔加上擴大後新找到的檔，其中的句子比對斷言移除或換掉，行為、結構與文法檢查保留；每個移除的比對都對應到一個具名替代。loom-code、loom-design、loom-workflow 三個 plugin 升 patch 版號，已安裝副本能透過更新拿到第二、三批的變更。

## Acceptance
1. 擴大後的普查腳本在乾淨副本中重算，回報逐字比對 skill／reference 句子的測試檔為零（已知 7 個檔與新找到的檔都算），除非報告中逐檔寫明理由；比對 checker／CLI 輸出的斷言不被算成散文比對。
2. 被清理的檔裡的行為、結構與文法檢查仍在，清理後完整 package suite 全綠。
3. 每個被移除的比對，其防守的缺陷類別對應到一個具名替代，對應表存於變更 evidence；acceptance testing 抽查可驗證該替代存在。
4. 若有 gate 以被移除的比對作為執行證據，`docs/loom/evidence/mechanisms.yaml` 改指向存在的替代，機制普查檢查通過。
5. 清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。
6. 三個 plugin 的版號各升一個 patch，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

## Constraints
- 沿用 2026-09-27-prose-evidence-class 的證據政策，以及第一、二批的做法：分類忽略註解、人工覆寫必須寫明理由、刪除前列出將刪斷言清單供 review。
- 只動測試、證據檔、`mechanisms.yaml` 的 eval 指向、普查腳本與版號相關檔；不修改任何 production 散文（skill／agent／reference）內容。
- 不新增 checker 規則；機制總數不增加。
- 範圍（user-decided 2026-09-29，選項 B）：擴大普查腳本讓它看得到直接寫死句子的比對，只抓比對 skill／reference 內容的，程式輸出不算；新找到的檔在這批一起清。
- 版號必須在 closing review 的 finalize 之前 commit，讓 attestation 涵蓋它。

## Out of scope
- 修改任何 skill／agent／reference 散文內容本身。
- 比對程式輸出訊息（checker／CLI 印出的字串）的斷言：那是行為檢查，不是散文比對。
- 變更 PR #61 已確立的證據政策。

## Open questions
- none
