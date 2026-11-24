# 刻意保留的 worktree 要留下紀錄，批次清理不會刪到它
originator: kouko
kind: engineering
needs-design: yes — 改變 loom-code 的 land 命令（--keep-worktree、--sweep、--cleanup）印出的訊息與清單分組，並新增一筆跨 session 的保留紀錄，目前沒有規格涵蓋
evidence: [loom-code/scripts/loom_checker/command_handlers/land.py, loom-code/skills/ship/SKILL.md, loom-code/scripts/loom_checker.py]
status: confirmed 2026-11-23
intent_confirmed_sha: 6561d19dd9e6e5f78760d5c05d47cd8292b1df63
publication: automatic — authorized 2026-11-23 by kouko

## Problem
loom-code 3.88.0 讓維護者在驗收時可以要求保留 worktree（`land --accepted-by <name> --keep-worktree`）。但 loom 沒有把「這個變更是刻意保留的」記下來，只在合併當下印一行訊息。

結果：
- 換一個 session 的 agent 看到一個已合併、worktree 還在的變更，分不出它是維護者要求保留的，還是之前清理失敗留下的。ship 的流程文字要 agent「保留的除外」，但 agent 沒有資訊可以照做。
- `land --sweep` 列出的可清理清單會包含保留的變更，而且沒有任何標示。維護者在不知情的情況下對清單說「好」，保留的 worktree 和分支就會被刪掉。

受影響的是所有在合併後保留 worktree 的 loom 使用者，以及之後在同一個 repo 工作的 agent。

## Proposed outcome
用 `--keep-worktree` 合併的變更，會留下一筆之後的 session 讀得到的保留紀錄。批次清理把保留的變更分開列出、而且永遠不刪；要刪只能由維護者明確要求清理那一個變更。agent 遇到已合併、還留著 worktree 的變更時，有保留紀錄就不動它；分不出來時，先問維護者再清理。

## Acceptance
1. 用 `--keep-worktree` 合併後，在一個完全不知道先前對話的新 session 裡，loom 能指出這個變更是被刻意保留的。
2. 批次清理的清單會把保留的變更另外列出並標明是保留的；確認批次清理後，保留的變更（worktree、本機分支、遠端分支）都還在。
3. 維護者明確要求清理某個保留的變更時，用 loom 既有的清理方式可以把它清掉，而且清完之後不再留有它的保留紀錄。
4. 沒有用 `--keep-worktree` 合併的變更，批次清理和清理的行為與現在相同。
5. 照 ship 的流程文字，agent 只清理沒有保留紀錄的已合併變更；分不出是否保留時，先問維護者，不會自行清理。

## Constraints
- 保留紀錄不能寫進 worktree 的工作目錄、也不能被 commit 或推到遠端：維護者保留的 worktree 內容要維持原樣。
- `--keep-worktree` 合併前的所有檢查不變。
- user-decided — 批次清理把保留的變更另外列出、標明保留、永遠不刪，而不是完全不列出（2026-11-23 kouko 選建議做法）。

## Out of scope
- 3.88.0 時期已經保留、沒有紀錄的 worktree 不做補登；這類情況由 Acceptance 5 的「分不出來就先問」處理。
- 驗收報告「Tried on」一行被翻譯的問題（另一個待修項）。
- 套件測試時限、對抗測試的外部環境記錄、PyYAML 底層 Python、偶發逾時測試（其他待修項）。

## Open questions
- none
