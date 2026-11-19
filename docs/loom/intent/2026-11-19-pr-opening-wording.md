# 開 PR 這一步不再叫 publish
originator: kouko
kind: engineering
needs-design: yes — 變更 loom-code CLI 的命令名、印給使用者的訊息與各站對使用者的說法，目前沒有規格涵蓋這一步的命名與舊命令的處理
status: confirmed 2026-11-19
intent_confirmed_sha: 62f951f5f1ef45a62f7dee4405f24bf00de0b407
publication: automatic — authorized 2026-11-19 by kouko

## Problem
loom 在 closing-review 之後會推送變更分支、開啟（或沿用）PR 並等待 CI。這一步的命令叫 `publish`，在使用者看得到的地方也都叫 publish／發布：CLI 印出 `Published PR:`、`Publication target:`、`publish: CI ...`，推送提醒印出 `publishing anyway`，README 的站序寫成「Publish PR」，agent 在對話中也說「已發布」。

維護者發現使用者會把它讀成「已經發布版本」。實際上這一步只開了一個等待合併的 PR：合併要使用者另外接受，plugin 內容還要 bump 版號才會更新到已安裝的副本。誤讀會讓使用者以為工作已經交付，或沒意識到合併還要自己決定。

## Proposed outcome
這一步的命令改名為 `open-pr`，使用者在這一步看到的文字清楚表達「推送分支並開了一個等待合併的 PR」，不再出現 publish 字眼。舊命令名直接移除。

## Acceptance
1. `open-pr` 以原本 `publish` 的相同參數完成推送、開啟或沿用 PR、等待 CI。
2. 執行舊命令 `publish` 時，與任何不存在的命令一樣回報 unknown sub-command，不推送、不開 PR，以非零結束。
3. 開 PR 這一步（含等待 CI 與交付狀態回報）中，CLI 印給使用者的訊息、命令說明與錯誤建議，都把這一步描述為開啟或沿用 PR、等待合併，不再使用 publish／published／publication 字眼。
4. 推送提醒 hook 印給使用者的說明（目前的 `publishing anyway`）改用相同的說法。
5. Ship 站對使用者的回報（PR 結果與合併前的驗收提問）、Ship 指示 agent 執行的命令，以及確認 intent 時告知「答 yes 之後會推送並開 PR」的那句話，都用相同的說法與新命令名，並保留「合併是另外的決定」。
6. repo 的 README 中描述這一步的文字使用相同的說法與新命令名。
7. 已經安裝原生 git hook 的 repo 在更新後，仍能正常安裝與移除該 hook。
8. 照 Ship 指示操作的 agent 仍能完成開 PR、等待 CI 與合併，完整 package suite 通過。

## Constraints
- 舊命令名 `publish` 直接移除，不保留別名，也不保留專屬的改名提示（user-decided 2026-11-19：「直接移除，只回 unknown sub-command，不推送」）。
- 原生 git hook 腳本的內容逐字元不變，因為已安裝的 hook 是逐字元比對。
- 發 PR 前的授權機制維持原樣。

## Out of scope
- 移除或改變發 PR 前的授權機制。
- 機器讀的識別字：rule id（如 `publish.preconditions`）、交付狀態值（`published`）、intent 的 `publication:` 欄位、`publication_only_paths`、GitHub 上既有的 ruleset 名稱。
- `docs/loom/` 底下的歷史紀錄與 evidence。
- 程式內部的命名（檔名、類別名、函式名、變數名）。

## Open questions
- none
