# 清理散文斷言測試存量（第二批）
originator: kouko
kind: engineering
needs-design: no — 純內部測試與證據清理，不觸及任何介面表面（manifest globs 之外）
evidence: [docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md]
status: confirmed 2026-09-28
publication: automatic — authorized 2026-09-28 by kouko

## Problem
第一批清理（2026-09-27-prose-pin-stock-cleanup，PR #64）後，仍有 26 個測試檔夾帶逐字比對散文句子的斷言：15 個會執行程式的行為類檔、7 個被 `docs/loom/evidence/mechanisms.yaml` 登記為 gate eval 的檔案、4 個文法不變量檔裡的句子斷言。只要潤稿落在這些檔案檢查的 skill／reference 上，測試照樣失敗、照樣要修，所以「改散文幾乎不用動測試」這個目標還沒達成。

## Proposed outcome
這 26 個檔案內的句子釘住斷言全部移除或換掉；檔案裡的行為檢查、結構檢查與文法檢查照舊保留。每個被移除的釘住所防守的缺陷類別，對應到一個具名替代（checker 重算規則、結構測試、review lens 面向，或已登記的 cold-read 證據）。原本以釘住當執行證據的 gate，改為指向那個替代。清理後，全 repo 的字面感應測試只剩文法級不變量一類。

另外修好 loom-visualization 描述的 A/B 重跑腳本，讓第一批決定的「描述證據＝語意審查＋結果重跑」真的能重跑出結果。

## Acceptance
1. 用第一批的普查腳本在乾淨副本重跑：句子釘住類為零，而且沒有任何檔案仍帶句子比對斷言（`has_pins=yes`），除非報告中逐檔寫明理由；分類結果可用腳本重算。
2. 這 26 個檔案裡的行為、結構與文法檢查仍在，清理後完整 package suite 全綠。
3. 每個被移除的釘住，其防守的缺陷類別對應到一個具名替代，對應表存於變更 evidence；acceptance testing 抽查可驗證該替代存在。
4. 原本以被移除的釘住作為執行證據的每個 gate，在 `docs/loom/evidence/mechanisms.yaml` 中改指向一個存在的替代證據，機制普查檢查通過。
5. 清理不刪除任何行為測試：清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。
6. loom-visualization 描述的 A/B 重跑腳本在乾淨副本照其說明能從頭跑完，對目前的描述產出新的一份結果，結果存於變更 evidence。

## Constraints
- 沿用 2026-09-27-prose-evidence-class 已確認的證據政策與收回條款，以及第一批確立的做法：分類忽略註解、`other` 桶非零即失敗、人工覆寫必須寫明理由。
- gate eval 檔內的釘住斷言也一併替換（2026-09-28 kouko 決定）；關卡文字被改錯時改由審查與 cold-read 紀錄發現。
- A/B 重跑腳本修復併入本變更（2026-09-28 kouko 決定）。
- 只動測試、證據檔、A/B 重跑腳本與 `mechanisms.yaml` 的 eval 指向；不修改任何 production 散文（skill／agent／reference）內容。
- 不新增 checker 規則；機制總數不增加。
- 刪除前列出將刪斷言清單供 review（沿用「Delete tests of removed behaviour」慣例）。

## Out of scope
- 修改任何 skill／agent／reference 散文內容本身。
- 為散文引入 LLM 評審或 golden-set 行為評估。
- 變更 PR #61 已確立的證據政策。
- 第一批列為文法級不變量而保留的文法檢查本身。

## Open questions
- none
