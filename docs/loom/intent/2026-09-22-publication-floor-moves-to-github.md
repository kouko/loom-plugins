# 合併底線移到 GitHub，loom 在本機只擋自己的指令、其他只提醒

originator: kouko
kind: engineering
needs-design: yes — 新增一份使用者複製進自己 repo、由 GitHub 執行的 CI 設定範本（外部系統依賴的檔案產物），且 ship 站對 GitHub 規則有「已設定／未設定／讀不到」三種狀態的新行為，沒有既有 spec 涵蓋
evidence: [loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/scripts/loom_checker/rule_checks/push.py, loom-code/scripts/loom_checker/rule_checks/publish.py, loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/hooks/hooks.json, loom-code/skills/ship/SKILL.md, PRINCIPLES.md]
status: confirmed 2026-09-22
publication: automatic — authorized 2026-09-22 by kouko

## Problem

loom 的發佈閘門在 agent 執行 Bash 前讀整串指令文字、猜它會不會推送或合併，猜到就擋。這帶來兩個方向相反的問題：

| 問題 | 後果 |
|---|---|
| 擋錯 | 分支還沒有驗證紀錄時 agent 被擋，使用者只好在自己的終端打同一行指令送出（2026-09-18 在 dotfiles 一天內 5 次以上）；指令文字裡只是提到合併也會被擋 |
| 漏看 | 用 `if … then`、`( … )`、`xargs`、`cat <<EOF \| bash`、前面加一段 `true;` 等寫法包起來的推送，完全不經檢查；GitHub 網頁上的合併按鈕、使用者自己的終端也看不到 |

使用者真正要守的底線只有一條：**合併回 main 之前，一定要有一個記錄實作內容與脈絡的 PR**。現在的閘門為了擋住操作寫了約 1,360 行 shell 解析，卻守不住這條底線。

前一版 intent（2026-09-19-publication-gate-warns-instead-of-blocking）試著在同一套解析上把部分阻擋改成提醒，實作後出現三個繞過回歸與 23 項測試失敗，由本 intent 取代。

## Proposed outcome

- 「合併進 main 前必須有合格 PR」這條底線由 GitHub 執行：main 只接受透過 PR 合併，PR 內文必須通過九章節檢查才能合併。
- loom 在本機只在自己的指令裡擋：ship 站開 PR、loom 自己的合併指令，送出前檢查 PR 內文。
- 其他所有推送、開 PR、合併操作，loom 在本機只提醒、不擋；認不出來的寫法就不提醒。
- ship 站會檢查目前 repo 的 GitHub 規則有沒有設好，沒設時告訴使用者缺什麼，並給一個可以直接執行的設定指令；只有使用者同意才會改 GitHub 設定。
- plugin 附一份 CI 設定範本，其他專案複製進去就能在 GitHub 上跑 PR 內文檢查。
- 預設仍跑完整 loom 流程；使用者用口語就能指示 agent 跳過任何步驟，不再需要輸入機器產生的通行碼。
- 跳過步驟時，使用者會看到提醒，但流程繼續執行、不被擋下。
- PR 上的驗證狀態由 loom 重新計算，不採信 agent 的說法：有效／沒有驗證紀錄／驗證紀錄與目前內容不符；三種都可以合併，後兩種在 PR 上寫明。
- PRINCIPLES.md 第 2 條配合修改：跳過驗證不再需要打字確認，改為必須在 PR 揭露。

## Acceptance

1. 在 main 已設定「必須透過 PR」且啟用內文檢查的 repo：PR 內文缺了九章節中任何一節、或任一節沒有實質內容時，GitHub 上無法合併，檢查結果指名是哪一節。
2. 同一個 repo：直接推送到 main 被 GitHub 拒絕。
3. 同一個 repo：九章節齊全、但分支沒有驗證紀錄的 PR 可以合併，且 PR 上看得到「沒有驗證紀錄」的揭露；驗證紀錄存在但與目前內容不符時，PR 上看得到「不符」的揭露；兩種揭露都由 loom 重新計算，手動改寫 PR 上的狀態文字不會讓檢查結果改變。
4. 在沒有驗證紀錄的分支上，agent 用任何 shell 寫法推送或開 PR，都不會被 loom 擋下；最常見的直接寫法會在終端出現一行提醒。
5. 用 ship 站開 PR 時，內文缺章節或有空章節會在 PR 送出前被擋下，並指名是哪一節。
6. 用 loom 自己的合併指令合併一個內文缺章節的 PR 會被擋下並指名是哪一節；內文齊全、沒有驗證紀錄的 PR 會合併，終端出現提醒。
7. 在 main 沒有設定規則的 repo 執行 ship 站：ship 站說出缺了哪一項，並顯示一個設定指令；使用者沒同意前，GitHub 上的設定沒有任何改變。
8. 在讀不到 GitHub 規則的 repo（權限不足或不是 GitHub）執行 ship 站：ship 站說「無法確認」並繼續，不擋下。
9. 把 plugin 附的 CI 範本複製進一個新的 GitHub repo 並開 PR，內文檢查會執行，結果與第 1、3 條一致。
10. 使用者口語指示跳過步驟後，agent 繼續完成推送與開 PR，過程中沒有要求使用者輸入任何通行碼；推送、開 PR、合併時終端都出現提醒，列出哪些驗證紀錄不存在。
11. PRINCIPLES.md 第 2 條寫明「跳過驗證必須在 PR 揭露」且不再要求打字確認，並帶有使用者的簽署（ratified-by）。
12. 只是在文字裡提到合併指令的操作（搜尋那串字、印出那串字、當作 commit 訊息），指令正常執行，沒有提醒也沒有阻擋。
13. 既有測試全部通過。

## Constraints

- PR 內文維持現行九章節規則，判斷條件不放寬（使用者 2026-09-22 決定）。
- 不得以補產一份驗證紀錄的方式讓任何檢查通過。
- 保留 loom 對跳站紀錄目錄的防護（`selection.guard`），不放寬。
- 未經使用者同意，不得改動任何 repo 的 GitHub 設定。
- 機器面輸出（訊息文字、測試、commit、CI 範本）維持英文。

## Out of scope

- 自動替其他 repo 套用 GitHub 規則或 CI 範本。
- GitHub 以外的程式碼託管平台、GitHub 免費方案下無法設定保護規則的私有 repo（這些 repo 只剩本機提醒與 loom 自己指令的檢查）。
- 以 REST API 形式送出的合併（`gh api …/merge`）在本機的辨識。
- 用 git pre-push hook 擋直接推送到 main。
- `~/dotfiles` 的自訂腳本變更。
- 刪除 `loom-gate-warn` 分支；它保留原狀。

## Open questions

- none
