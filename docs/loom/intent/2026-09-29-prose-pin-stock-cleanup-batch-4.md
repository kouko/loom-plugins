# 清理散文斷言測試存量（第四批）：短語與藏起來的比對
originator: kouko
kind: engineering
needs-design: no — 純內部測試、證據與版號清理，不觸及任何介面表面（manifest globs 之外）
evidence: [docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-3/evidence/census-report.md]
status: confirmed 2026-09-29
publication: automatic — authorized 2026-09-29 by kouko

## Problem
第三批清理（PR #66）後，普查腳本報「句子比對 = 0」，但這只代表腳本看得到的寫法：兩個字的短語或單一詞、寫在檢查小工具裡的句子、用位置查找（`.index()`）或正規表示式比對的句子，腳本都看不到（第三批 census-report「Known limits」）。潤稿碰到這些字眼時測試仍會變紅，而且沒有人知道還剩多少。

## Proposed outcome
第三批看不到的幾種寫法變得可以被找出來並重算；找到的散文比對移除或換掉，行為、結構與文法檢查保留；每個移除的比對都對應到一個具名替代。三個 plugin 升 patch 版號。

## Acceptance
1. 普查在乾淨副本中重算，涵蓋第三批看不到的寫法（兩個字的短語、檢查小工具內的字串、位置查找與正規表示式比對），回報比對 skill／reference 散文的測試檔為零，除非報告中逐檔寫明理由；比對 checker／CLI 輸出的斷言不被算成散文比對。
2. 被清理的檔裡的行為、結構與文法檢查仍在，清理後完整 package suite 全綠。
3. 每個被移除的比對，其防守的缺陷類別對應到一個具名替代，對應表存於變更 evidence；acceptance testing 抽查可驗證該替代存在。
4. 若有 gate 以被移除的比對作為執行證據，`docs/loom/evidence/mechanisms.yaml` 改指向存在的替代，機制普查檢查通過。
5. 清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。
6. 三個 plugin 的版號各升一個 patch，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

## Constraints
- 沿用 2026-09-27-prose-evidence-class 的證據政策，以及第一到三批的做法：分類忽略註解、人工覆寫必須寫明理由、刪除前列出將刪斷言清單供 review、被刪減的測試改名為它實際還在檢查的事。
- 只動測試、證據檔、`mechanisms.yaml` 的 eval 指向、普查腳本與版號相關檔；不修改任何 production 散文（skill／agent／reference）內容。
- 不新增 checker 規則；機制總數不增加。
- 標題、gate 標記、欄位名等結構字串的檢查屬於結構檢查，保留。
- 版號必須在 closing review 的 finalize 之前 commit。
- 找法（user-decided 2026-09-29，選項 A）：擴大普查腳本，列出第三批看不到的寫法的所有候選，逐一移除或寫明理由，結果可重算。

## Out of scope
- 修改任何 skill／agent／reference 散文內容本身。
- 比對程式輸出訊息的斷言。
- 第三批刻意保留的 3 個 gate 方向檢查，以及 decision-map 的 Codex `defaultPrompt` 字串。
- 第三批改由人工審查接手的 50 類缺陷是否恢復自動檢查。

## Open questions
- none
