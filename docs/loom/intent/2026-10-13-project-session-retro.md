# Review one coding session for project development improvements
originator: kouko
kind: engineering
needs-design: no — a new on-demand skill contract, with no GUI, CLI, API, template, or multi-state interface
status: confirmed 2026-10-13
publication: automatic — authorized 2026-10-13 by kouko

## Problem
在一次專案開發結束後，使用者缺少一個專門回看該次紀錄、找出專案文件、檢查工具或 agent 工作環境改善點的 Loom 工具。現有的 distill-sessions 針對多次紀錄改善既有 skill，不能直接承接這個目的；兩種回顧若混用，建議的對象和證據門檻會不清楚。

## Proposed outcome
使用者可以在 loom-workflow 主動要求回顧目前或指定的單次開發紀錄，得到有原始證據的專案開發環境改善建議，同時保留 distill-sessions 對多次紀錄與 skill 修改的職責。

## Acceptance
1. 使用者可以呼叫 loom-workflow 的 retro 回顧目前或指定的一次開發紀錄，取得依影響排序、可追溯到該次紀錄的改善建議。
2. 回顧結果能分辨專案層級的改善建議與僅憑單次紀錄發現的 skill 問題候選，不會直接修改任何檔案。
3. 現有 distill-sessions 的名稱、觸發範圍和多次紀錄改善 skill 的行為仍可使用；一般回顧請求能找到 retro，skill 改善紀錄挖掘請求仍能找到 distill-sessions。

## Constraints
- 新 skill 位於 loom-workflow，與 distill-sessions 共存。
- retro 是使用者主動呼叫的獨立工具，不成為 Loom 開發站或品質閘。
- 對話使用繁體中文；儲存庫產物遵循既有語言慣例。

## Out of scope
- 更名或重作 distill-sessions。
- 自動套用 retro 建議，或從單次紀錄直接修改 skill。
- 新增另一個 plugin 或 Loom 站。

## Open questions
- none
