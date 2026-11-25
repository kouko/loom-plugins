# Codex 遵守 loom 的 main 保護 hook
originator: kouko
kind: engineering
needs-design: no — internal hook wiring for one host; no user-facing surface changes
evidence: [loom-code/hooks-codex.json, loom-code/scripts/loom_checker/command_handlers/push.py]
status: confirmed 2026-11-25
intent_confirmed_sha: 08809d4
publication: automatic — authorized 2026-11-25 by kouko

## Problem
2026-11-25 實測（loom-code 3.90.1，`codex exec -s danger-full-access`）：Codex 有觸發 loom 的 PreToolUse hook，但 agent 在 main 上直接 `git commit`、以及 `cd <main> && git commit` 都成功寫進 main。把同一份 hook 輸入手動送給 checker 會得到 exit 2 與擋下訊息，所以 checker 判斷正確，是 Codex 沒有照結果停下。用 Codex 的使用者以為 main 有保護，實際上沒有；只剩 opt-in 的原生 git hook 和 GitHub 規則兜底。

## Proposed outcome
在 Codex 裡，loom 判定要擋的 git 指令真的不會執行，agent 看到跟 Claude Code 相同的擋下訊息；feature 分支上的正常操作不受影響。

## Acceptance
1. 在沒有原生 git hook 的測試 repo，真實 Codex session 在 main 上執行 `git commit`，main 的 HEAD 不變，且 agent 收到 loom 的擋下訊息。
2. 同條件下，從 feature worktree 執行 `cd <main checkout> && git commit`，main 的 HEAD 不變。
3. 同條件下，在 feature 分支上 `git commit` 照常成功。
4. Claude Code、OpenCode、Antigravity 的 hook 行為不變（既有測試通過）。
5. 若原因出在 Codex 本身、loom 無法修正，交付一份記錄原因與證據的說明，並在 loom 的 Codex 文件寫明此限制。

## Constraints
- 擋下訊息、exit code 語意、`loom.protectMain false` 退出機制維持不變。
- 只用 Codex 已公開支援的 hook 介面。

## Out of scope
- 修改 Codex 本身。
- 擴大擋下的指令寫法（已由 3.90.1 處理）。
- OpenCode、Antigravity 的實測（另行處理）。

## Open questions
- none
