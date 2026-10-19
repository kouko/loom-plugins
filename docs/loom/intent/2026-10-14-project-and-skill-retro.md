# Separate project and installed-skill retrospectives
originator: kouko
kind: engineering
needs-design: yes — the review target expands across skill instructions and plugin integration, with multi-object proposal output not covered by an existing spec
status: confirmed 2026-10-15
publication: automatic — authorized 2026-10-15 by kouko

## Problem
目前兩個回顧工具的名稱沒有清楚指出各自要改善的對象。單次回顧偏向專案開發環境；跨次分析雖能發現 skill 問題，修改提案卻只針對 SKILL.md。當已安裝 skill 的問題來自 plugin 的註冊、載入或其他整合環節時，使用者難以從現有工具得到歸屬清楚、可交給後續實作的建議。跨次工具還能在批准後直接改寫 skill，兩種回顧的交付邊界不一致。

## Proposed outcome
使用者可以分別要求一次紀錄的專案開發回顧，以及多次紀錄的已安裝 skill 回顧。兩者提供有來源、可供後續實作的具體改善方案；後者能將與目標 skill 相關的 plugin 整合問題列入分析。回顧本身不套用修改。

## Acceptance
1. 使用者可以用 project-retro 回顧目前或指定的一次開發紀錄，得到指向該專案實作方式、文件、檢查工具或專案層級 agent 指示的有來源改善方案；跨專案可重用工具的問題另列為候選。
2. 使用者可以用 skill-retro 分析多次開發紀錄，取得針對已安裝 skill 行為的可審閱方案，並能區分 skill 指示與相關 plugin 註冊、載入、hook、腳本或相依 connector 的問題；單次證據不足時不宣稱反覆缺陷。
3. 兩種回顧都不直接修改被回顧的專案實作或目標 skill／plugin；需要變更時，方案能交給獨立的實作流程處理。
4. 使用者能以兩個新名稱呼叫相應工具，普通請求能依改善對象分流；舊名稱的遷移方式清楚可見。

## Constraints
- 兩種回顧都留在 loom-workflow，不新增 plugin 或 Loom 開發站。
- project-retro 使用一次紀錄；skill-retro 使用多次紀錄判斷反覆問題。
- 現有紀錄的隱私界線與外送前的同意要求繼續適用。
- 舊名稱不保留為可呼叫入口；提供遷移說明。

## Out of scope
- 與任何已安裝 skill 無關的通用 plugin 或 connector 稽核。
- 從單次紀錄直接判定 skill 的反覆缺陷，或自動套用回顧建議。
- 在這次變更新增其他宿主的 session 紀錄匯入能力。

## Open questions
- none
