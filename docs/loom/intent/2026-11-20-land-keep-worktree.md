# 驗收合併時可以保留 worktree
originator: kouko
kind: engineering
needs-design: yes — 為 loom-code 的 land 命令新增「合併但不清理」的選項，改變 CLI 參數、說明文字與印出的訊息，目前沒有規格涵蓋這個形式
evidence: [loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/scripts/loom_checker.py, loom-code/skills/ship/SKILL.md]
status: confirmed 2026-11-20
intent_confirmed_sha: 071e271078c209413df6c88c506ba672682d9a24
publication: automatic — authorized 2026-11-20 by kouko

## Problem
維護者驗收一個變更後，有時想在合併後繼續留著這個變更的 worktree（例如合併後還要在裡面對正式環境跑驗證、查數字，或 worktree 由 herdr 之類的工具管理）。現在 loom 的合併步驟（`land --accepted-by`）合併後一定會刪掉 worktree 和本機、遠端分支，沒有保留的選項；而 ship 又禁止 agent 自己打 `gh pr merge`。

結果是：維護者說「接受，保留 worktree」時，agent 沒有任何合規的做法。2026-11-20 一個 dbt 專案的 session 裡，第一個 PR 只能在 land 執行中途把它停掉，第二個 PR 改用 `gh pr merge --squash` 繞過，跳過了 land 對 PR 內容的檢查與驗收紀錄。`land` 自己的說明文字還寫著「使用者要求保留 worktree 時不要清理」，但合併的形式一定會清理，兩邊互相矛盾。

## Proposed outcome
維護者在驗收時要求保留 worktree，loom 照常走完合併（同樣的檢查、同樣的驗收紀錄、同樣同步主幹），只是合併後不清理這個變更的 worktree、本機分支與遠端分支。之後要清理時，用 loom 既有的清理方式一次清掉。沒有要求保留時，行為和現在完全一樣。

## Acceptance
1. 維護者驗收時要求保留 worktree，合併完成後，該變更的 worktree 還在原來的位置，裡面的檔案與 checkout 的分支都沒有被動到，遠端分支也還在。
2. 要求保留的這次合併，仍然經過和一般合併相同的檢查與驗收紀錄，主幹也照常同步；任一檢查不過時，一樣拒絕合併。
3. 沒有要求保留時，合併後的結果和現在相同：worktree 與本機、遠端分支都被移除。
4. 保留下來的變更，之後用 loom 既有的清理方式可以把 worktree 與分支清掉。
5. 照 ship 的流程文字，維護者要求保留 worktree 時，agent 有一條不需要自己打 `gh pr merge` 的做法；`land` 的說明文字不再要求一件合併形式做不到的事。

## Constraints
- 合併前的檢查（PR 內容驗證、檢查項目、驗收者名字比對）一項都不能因為保留而放寬。
- 預設行為不變：沒有要求保留就照現在清理。
- user-decided — 保留時遠端分支也一起保留，不做部分清理（2026-11-20 kouko 選 A）。

## Out of scope
- 套件測試的時限（另一個待修項）。
- 對抗測試需要外部環境時的記錄方式（另一個待修項）。
- 驗收報告「Tried on」一行被翻譯的問題（下一個變更）。
- 改變 `land --cleanup` 與 `land --sweep` 現有的行為。

## Open questions
- none
