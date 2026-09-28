# 清理散文斷言測試存量
originator: kouko
kind: engineering
needs-design: no — 純內部測試清理，不觸及任何介面表面（manifest globs 之外）
status: confirmed 2026-09-27
publication: automatic — authorized 2026-09-27 by kouko

## Problem
上一個變更（2026-09-27-prose-evidence-class，PR #61）已讓機制不再強迫「新的」散文變更附帶字面感應測試，但既有存量原封不動：目前 main 上約 40 個測試檔仍在釘住散文句子（其中 12 個是純釘住、不含任何可執行行為），`prose_pin` 系檔案內有約 432 個測試函式、多為混合用途。每次潤稿這些測試照樣碎、照樣要修，維護成本持續發生，只是不再新增。受影響的是本 repo 的所有後續變更：散文相關 PR 的測試修補噪音沒有隨機制修正消失。

## Proposed outcome
既有句子釘住測試分批清理：純釘住檔案刪除；混合檔案只保留行為與結構部分；文法級不變量（`prose_pin` matcher 及其自測、negation matcher、gate marker 文法）依已確認政策保留。每個被刪除釘住所防守的缺陷類別對應到替代證據（checker 重算、結構測試或 review lens），對應表存於變更 evidence。清理後，字面感應測試只剩文法級不變量一類。

## Acceptance
1. 一份普查報告存在於變更 evidence：每個讀散文的測試檔被分類為行為／結構／句子釘住／文法不變量四類之一，分類方法可用腳本重算。
2. 純句子釘住檔案（零可執行行為）全數刪除；普查歸為句子釘住類的混合檔案只保留行為與結構部分；清理後完整 package suite 全綠。
3. 每個被刪除的釘住測試，其防守的缺陷類別對應到一個具名替代（checker 重算規則、結構測試或 review lens 面向），對應表存於 evidence，acceptance testing 抽查可驗。
4. 清理後普查報告證明句子釘住類為零：字面感應檔案只剩文法級不變量類，以及被 `docs/loom/evidence/mechanisms.yaml` 登記為 gate eval 的檔案（該 gate 的執行證據，本批保留並在報告中單獨列類）。
5. 清理不刪除任何行為測試：清理前後，「會執行程式（subprocess／checker 呼叫）」的測試函式數量不減少，重算可證。

## Constraints
- 沿用 2026-09-27-prose-evidence-class intent 已確認的證據政策與收回條款；本變更不新增 checker 規則，普查以變更 evidence 內的腳本呈現。
- 分批進行：每批一個可審查的大小，批次切分由 plan 決定。
- 只動測試與證據檔；不修改任何 production 散文（skill／agent／reference）內容。
- 每批刪除前列出將刪檔案清單供 review（延用既有「Delete tests of removed behaviour」慣例）。

## Out of scope
- 修改任何 skill／agent／reference 散文內容本身。
- 為散文引入 LLM 評審或 golden-set 行為評估。
- 變更 PR #61 已確立的證據政策（tests lens 散文條款、intake 豁免、單一版本常數）。
- docs/loom 工作文件（本來就無測試）。
- 第二批（2026-09-28 kouko 決定分批）：普查歸為行為類、但檔內仍夾帶句子釘住斷言的 15 個檔案，以及 gate eval 檔案內的釘住斷言替換；另開變更處理，清單見本變更 census-report。
- 修復 loom-visualization 描述的 A/B 重跑腳本（`docs/loom/2026-09-14-loom-visualization-description-trigger/ab/run_ab.py`：import 路徑已失效、寫死舊描述）；2026-09-28 kouko 決定描述證據改為語意審查＋結果重跑後，結果重跑須待此修復，另開變更。

## Open questions
- none
