# 恢復 skill 資料夾檢查並清理 AGENTS.md
originator: kouko
kind: engineering
needs-design: no — 只改 repo 內部的測試與貢獻者文件，沒有新增使用者介面，也沒有多狀態行為
status: confirmed 2026-11-18
intent_confirmed_sha: 677a190e440cf609954a6d0fe2302deb4dac2262
publication: automatic — authorized 2026-11-18 by kouko

## Problem
`AGENTS.md` 規定 skill 資料夾必須扁平，並說違規會被 hook 擋下，但這個 repo 目前沒有任何檢查會執行：repo 內的 `.claude/hooks/validate-skill-folder-structure.sh` 沒有被註冊，loom-workflow 的 hook 又因為看到這支檔案而跳過。維護者和 agent 因此可能在沒有任何提示的情況下加入違規結構，直到安裝或使用時才發現。

同一份 `AGENTS.md` 還描述了不在這個 repo 的 plugin、已不存在的文件，以及過時的審查與版號規則。它每次 session 都會被載入，agent 可能依這些錯誤內容行動，或花時間尋找不存在的東西。

## Proposed outcome
這個 repo 的 skill 資料夾扁平規則有實際執行的檢查，而且 `AGENTS.md` 只陳述與 repo 現況相符的內容。

## Acceptance
1. 在任一 skill 的子資料夾內加入含檔案的巢狀資料夾後，不論是否已 commit，完整 package suite 都會失敗並指出該路徑；移除後恢復通過。
2. `AGENTS.md` 不再提及不在這個 repo 的 plugin，也不再指向不存在的檔案或測試。
3. `AGENTS.md` 對 skill 資料夾檢查、審查鏡頭與人數、版號及 changelog 的描述，都與 repo 現行的檢查和檔案一致。
4. `AGENTS.md` 仍保留 skill 資料夾扁平與版號 bump 的 MUST 規則，完整 package suite 通過。

## Constraints
- 不改變 loom-workflow hook 在其他 repo 的行為。
- 保留 repo 內未註冊的 `.claude/hooks/validate-skill-folder-structure.sh`，這個 repo 的 skill 資料夾規則由完整 package suite 檢查。
- 保留 `AGENTS.md` 的 Module Criteria、Test Location、Contract Citations 與 loom 1.0 flow 規則；既有測試依賴其中的文字。

## Out of scope
- 寫檔當下的違規提示，以及 loom-workflow hook 的誤報與漏報。
- 從 feature branch 推送或刪除遠端 `main` 的防護。
- 執行環境缺失時 hook 放行的問題。
- `closing-review` 的字數超限。
- 審查意見進入修復前的確認流程。
- 全面弱化 `AGENTS.md` 的強調語氣。

## Open questions
- none
