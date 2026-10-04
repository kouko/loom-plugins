# 先改程式、再補回 loom 流程的做法說明
originator: kouko
kind: engineering
needs-design: no — guidance text in an existing engineering reference; no new field, rule, step, command or file artifact
evidence: [loom-code/references/engineering-baseline.md, /Users/kouko/XcodeProjects/komado-Viewfinder/docs/loom/2026-10-01-video-drop-frame-diagnostics/plan.md]
status: confirmed 2026-10-04
publication: automatic — authorized 2026-10-04 by kouko

## Problem
使用者有時會刻意先略過 loom 直接改程式，之後再補回流程。loom 已經能記錄「使用者指示跳過 tdd」並在 PR 揭露，但沒有說明這種情況該怎麼補測試、要記下什麼，agent 只能自己發明做法。

| 現況 | 後果（以 komado-Viewfinder PR #45 為例） |
|---|---|
| engineering-baseline 的「Legacy backfill」只涵蓋 task 層級的舊程式碼 | 沒有適用於「整個變更的程式先寫好」的做法 |
| 同一段寫「有機會先寫測試卻跳過」算違規，沒提使用者指示的情況 | agent 不確定這樣做算不算違規，只好在 plan 用散文標「反向補寫」 |
| 沒說事後補的測試要證明什麼 | 以「接口還不存在、編譯不過」當紅燈，測試是否抓得到問題沒有證據 |
| 沒說要記下哪些程式碼先寫好 | reviewer 只能從散文猜程式碼的來源 |

## Proposed outcome
使用者先略過 loom 改好程式後，用現有的「跳過 tdd」指示就能把變更補回 loom；agent 照一份明確做法補測試、記錄範圍；補紀錄不增加新步驟的成本。

## Acceptance
1. engineering-baseline 說明：使用者以一般語言指示跳過 tdd、程式在流程開始前就寫好時，補回流程要先寫測試釘住既有行為（bug 一起釘）再修改，並在 plan 記下先寫好的程式碼範圍。
2. 同一份說明寫明三個界線：沒有使用者指示而跳過先寫測試仍算違規；流程開始後新寫的程式碼照常先寫測試；編譯失敗不能當成測試抓得到問題的證據。
3. 不新增 intent 欄位、checker 規則或流程步驟；紀錄由現有的跳過紀錄與 PR 揭露承載；沒有這種指示的變更，行為完全不變。
4. 完整 package suite 全部通過，版號一致。

## Constraints
- 不改變三個決策點、站序、現有 checker 規則與 intent 格式。
- 使用者 2026-10-04 依複雜度檢驗選擇最小做法，放棄機器驗證程式與測試的先後順序。出現以下任一情況時，再另開 intent 做機器檢查版本：
  - agent 未經使用者指示，把自己新寫的程式碼當成先寫好的；
  - 再有兩次補回時，reviewer 沒看出程式碼的來源。
- loom-plugins 是公開 repo，不複製 komado-Viewfinder 的實際內容；komado-Viewfinder 不修改。
- 對話用繁體中文；plan、spec、verdict、commit body 等 loom 機器面 artifacts 用英文。

## Out of scope
- 新的 intent 欄位、checker 規則、失敗證明或新舊行為判斷步驟。
- 修改 komado-Viewfinder 或任何其他 repo。
- 改變 loom 何時被觸發（略過 loom 由使用者自己說）。

## Open questions
- none
