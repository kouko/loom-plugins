# 以普通專案規劃文件取代長期目標專用機制
originator: kouko
kind: engineering
needs-design: yes — 移除既有規劃文件契約與相關操作，並改變跨 session 規劃文件的使用約定；目前沒有涵蓋此替代方式的規格
evidence: [docs/loom/research/2026-11-16-roadmap-simplification.md, PRINCIPLES.md]
intent_confirmed_sha: bce53ed0eeff16abddbcd73475b0e3b4541ad68c
status: confirmed 2026-11-17
publication: automatic — authorized 2026-11-16 by kouko

## Problem
kouko 覺得長期規劃機制使用率低；目前要理解不同名稱、文件與操作，
才能保存跨多次 session 的目標和下一步。finance 專案已用普通 Markdown
保存這些資訊，但這種做法如何建立、讀取與持續更新尚未成為一致約定。
目前指引對階段拆分與排序只有基本原則；kouko 希望補強可直接運用的
規劃判斷，也能用於非軟體情境，同時避免把簡單工作擴成完整規劃流程。

## Proposed outcome
用簡單的專案規劃文件保存長期目標、完成條件、目前重點與未解問題，
讓後續 agent 可以接續工作；退休重疊的長期目標專用機制，降低維護負擔。
補強跨情境的階段規劃能力，讓複雜工作有依據地拆分、排序與調整，
而已確認的簡單工作仍能直接接續。

## Acceptance
1. 有跨 session 階段規劃需求的專案能選用根目錄的普通 ROADMAP.md 保存長期目標、完成條件、目前狀態、下一步及相關證據，而不依賴 decision-map 的檔案格式或執行程式。
2. agent 在使用者要求跨 session 的階段規劃、接續該工作或判斷下一步時，能依一致約定建立或讀取規劃文件，並在方向或已驗證成果改變時更新相關內容。
3. 新版不再提供 decision-map 操作與專案 PURPOSE 草擬模式；一般開發流程、研究、接續紀錄及單次 agent 執行目標仍可使用。
4. 原有規劃與歷史證據留在原處可讀；更新 plugin 不會刪除、改寫或轉換其他專案中的既有 map、purpose 或使用者資料。
5. 規劃文件不取代正式開發確認、驗證或驗收，也不把未驗證的工作描述為完成。
6. 對資訊足夠的複雜專案規劃，agent 能提出可獨立使用或驗證的階段，說明其目標、先後順序的依據及會改變後續投入的未知與條件。
7. 非軟體的分階段工作也能使用上述規劃判斷，不被要求套用軟體開發、部署或遷移流程。
8. 已確認的簡單工作與續作，不會因新增規劃知識而被要求額外訪談、填欄位、建立規劃文件或重開已確認的目標。

## Constraints
- 長期規劃使用可選的根目錄 ROADMAP.md，只保存當前摘要並連到詳細證據；不要求每個專案建立文件。
- 保留現有實作、獨立審查與驗收流程。
- 保留 goal-create 的 SESSION 功能；不得因移除 ARC 而刪除整個 skill。
- 遵循專案既有原則，不改寫、刪除或外傳使用者既有資料。
- 遵循現有 plugin 發版、測試及衍生 manifest 同步要求。
- 通用規劃判斷按情境需要使用；維持簡單文件與既有授權界線，不增加固定評分、必填清單或背景排程。

## Out of scope
- 自動執行整份 roadmap、背景排程或以規劃文件授權發布及合併。
- 其他 repository 的資料遷移、清理與歷史目標結案。
- 新的規劃 CLI、驗證器、ticket store 或通用轉換工具。

## Open questions
- none
