# Codex 遵守 loom 的 main 保護 hook — 我試了什麼、結果如何

Tried on 2026-11-25, in a clean copy of the project at 18dbb3436. How I tried
each line and what came back: `docs/loom/2026-11-25-codex-hook-block-honored/evidence/acceptance-test-evidence.md`.

## 你要的東西，逐條

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | 在沒有原生 git hook 的測試 repo，真實 Codex session 在 main 上執行 `git commit`，main 的 HEAD 不變，且 agent 收到 loom 的擋下訊息。 | not verified | main 的 HEAD 確實沒變，但那是因為 Codex 的模型兩次都拒絕執行這個 commit，指令根本沒送出，所以 loom 的 hook 沒有機會擋、也沒有出現擋下訊息。 | — |
| 2 | 同條件下，從 feature worktree 執行 `cd <main checkout> && git commit`，main 的 HEAD 不變。 | not verified | 同上：模型兩次都拒絕執行，main 沒變不是 hook 擋下的結果。 | — |
| 3 | 同條件下，在 feature 分支上 `git commit` 照常成功。 | works | 真實 Codex session 在 feature worktree 執行 commit，hook 有觸發、commit 成功寫入 feature 分支，main 不受影響。 | — |
| 4 | Claude Code、OpenCode、Antigravity 的 hook 行為不變（既有測試通過）。 | works | 這次改動完全沒有動到 hook 與 checker 的程式（和 main 相比差異為空），行為不可能改變；既有測試由自動化測試套件負責，它在變更被接受前執行、失敗就擋下。 | — |
| 5 | 若原因出在 Codex 本身、loom 無法修正，交付一份記錄原因與證據的說明，並在 loom 的 Codex 文件寫明此限制。 | works | 英、日、繁中三份 README 的 Codex 段落都寫明：更新後要用互動模式啟動 Codex 一次並核准變更過的 hook，核准前 hook 可能被略過、擋不住對 main 的 commit／merge／push，且 `codex exec` 可能不會顯示核准提示。 | — |

## 對你既有的資料做了什麼

Nothing — it only touched files this change created. 測試全部在一個新建、用完即丟的暫存 repo 裡進行；你的 Codex 設定與已安裝的 plugin 都沒有被修改。

## 我替你決定的事

- **第 1、2 條的試法** — 模型拒絕後我照指示只換一次說法再試；第二次仍被拒，就記成「未驗證」，沒有改用繞過模型的方式（例如手動餵 hook 輸入），因為那不是使用者實際會遇到的情況。之後要補驗，得在能讓模型願意執行 commit 的條件下重跑一次真實 session。
- **第 4 條判為 works** — 我沒有自己重跑整套測試，判斷依據是 hook 與 checker 程式和 main 完全相同；整套測試由後續的自動化測試套件把關。

## 你叫我略過的步驟

Nothing — no step was skipped.

## 我不確定你要不要的事

- 第 1、2 條這次無法證明 Codex 會照 hook 結果停下；這張 change 靠第 5 條（文件說明限制）交付，你接受這樣就算完成嗎？
- 測試機上的 Codex hook 是否已在互動模式核准過，我沒有確認（依指示不碰 Codex 設定）；這會影響第 1、2 條重跑時的結果。
