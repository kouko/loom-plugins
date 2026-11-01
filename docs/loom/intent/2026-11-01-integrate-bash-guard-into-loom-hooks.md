# 將 bash-guard 併入 Loom 的執行前保護

originator: kouko
kind: engineering
needs-design: no — changes to hook and gate internals; no declared user interface surface
evidence: [loom-code/hooks/hooks.json, loom-code/hooks/hooks-codex.json, loom-code/hooks/hooks-opencode.json, /Users/kouko/dotfiles/claude/.claude/hooks/executable_bash-guard.sh, /Users/kouko/dotfiles/claude/settings.template.json]
status: confirmed 2026-11-01
publication: automatic — authorized 2026-11-01 by kouko

## Problem

目前 Git 操作的本機保護由 dotfiles 的使用者層級 bash-guard 負責，Loom 另有自己的執行前檢查。兩套機制分開維護，讓保護規則與 Loom 流程無法一起演進；先前嘗試擴充 bash-guard 的指令解析也未能收斂。

## Proposed outcome

由 Loom 的 hooks 負責簡單、明確的主分支 Git 操作保護。只要 loom-code 外掛在支援的宿主中啟用，該保護就對其執行的專案生效，不要求專案正在走 Loom 流程；dotfiles 不再以獨立 hook 重複執行同一組規則。

## Acceptance

1. loom-code 外掛啟用時，不論專案是否正在走 Loom 流程，執行前檢查都能阻止 main/master 上直接執行的 `git merge`、`git commit` 與 `git push`，並讓功能分支上的正常工作繼續；不宣稱能阻止複合指令、腳本或其他方式更新主分支。
2. 在非 Git 目錄與 detached HEAD，`ls` 等一般 Bash 指令可照常執行；既有的破壞性指令檢查仍各自運作。
3. Loom 原有的發佈提醒與其他執行前行為仍可正常運作。
4. 切換到已安裝的新版本後，同一個 Git 保護規則只執行一次；dotfiles 不再註冊獨立的 bash-guard。
5. 相關測試與 Loom 完整套件測試通過，並能在乾淨環境重現保護與放行結果。
6. dotfiles 與個人 Obsidian vault 仍能在主分支工作，且這兩個例外不會套用到其他使用者的專案。

## Constraints

- 先前已選定精簡版 B 的保護行為作為遷移基準；不恢復先前未收斂的複雜指令解析。
- 在非 Git 目錄與 detached HEAD，普通 Bash 指令不得因無法判定分支而一律被拒絕。
- 保留目前 dotfiles 與個人 Obsidian vault 可以在主分支工作的結果；不得把這兩個個人路徑設成所有 Loom 使用者的固定例外。
- 保留目前其他使用者層級 hooks 與 statusline 的作用。
- dotfiles 工作樹已有與本變更無關的未提交內容，必須保留。
- `gh pr merge`／`gh pr close` 遵循 Loom 現行的提醒政策，不遷移舊 bash-guard 的拒絕規則。

## Out of scope

- 重寫 Loom 的完整發佈與合併流程。
- 變更 dcg、session-title、delegation-authority 或 statusline 的功能。
- 恢復先前放棄的 bash-guard 指令解析器。
- 安裝 Git hooks 或保證本機 main/master 分支指標無法透過其他入口更新。

## Open questions

- none
