# Codex 遵守 loom 的 main 保護 hook — 我試了什麼、結果如何

Tried on 2026-11-25, in a clean copy of the project at ffc47ad27. How I tried
each line and what came back: `docs/loom/2026-11-25-codex-hook-block-honored/evidence/acceptance-test-evidence.md`.

## 你要的東西，逐條

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | 在沒有原生 git hook 的測試 repo，真實 Codex session 在 main 上執行 `git commit`，main 的 HEAD 不變，且 agent 收到 loom 的擋下訊息。 | works | 第三種說法下 Codex 真的送出了 commit，loom 的 hook 擋下它，agent 收到並轉述了 loom 的擋下訊息，main 沒有多出任何 commit。 | re-tested |
| 2 | 同條件下，從 feature worktree 執行 `cd <main checkout> && git commit`，main 的 HEAD 不變。 | not verified | main 的 HEAD 沒變，但三種說法 Codex 的模型都拒絕執行，指令沒有送出，所以不是 hook 擋下的結果。 | re-tested |
| 3 | 同條件下，在 feature 分支上 `git commit` 照常成功。 | works | 這次三種說法模型都拒絕執行，沒能重測；採用上一輪的實測結果：真實 Codex session 在 feature 分支 commit 成功、hook 有觸發、main 不受影響。 | carried over — 上一輪之後只改了更新紀錄與計畫文件的文字，hook 與說明文件都沒動 |
| 4 | Claude Code、OpenCode、Antigravity 的 hook 行為不變（既有測試通過）。 | works | hook 與 checker 的程式和 main 完全相同，行為不可能改變；既有測試由自動化測試套件負責，它在變更被接受前執行、失敗就擋下。 | re-tested |
| 5 | 若原因出在 Codex 本身、loom 無法修正，交付一份記錄原因與證據的說明，並在 loom 的 Codex 文件寫明此限制。 | works | 英、日、繁中三份 README 的 Codex 段落都寫明更新後要用互動模式核准變更過的 hook，否則可能擋不住對 main 的操作；原因與證據記在這張 change 的計畫文件（現況證據的錯誤與資料兩項、風險第 1、2 條）。原因是推論，沒有實際重現。 | re-tested |

## 對你既有的資料做了什麼

Nothing — it only touched files this change created. 測試全部在一個新建、用完即丟的暫存 repo 裡進行；你的 Codex 設定與已安裝的 plugin 都沒有被修改。

## 我替你決定的事

- **試法的說法** — 模型拒絕時最多換兩次說法；第 1 條第三次成功，第 2 條三次都被拒就記成「未驗證」，沒有改用繞過模型的方式（例如手動餵 hook 輸入），因為那不是使用者實際會遇到的情況。
- **第 3 條沿用上一輪** — 這次重試被模型拒絕，但上一輪之後沒有任何會影響它的改動，所以保留上一輪的實測成功結果。
- **第 4 條判為 works** — 我沒有自己重跑整套測試，依據是 hook 與 checker 程式和 main 完全相同；整套測試由後續的自動化測試套件把關。

## 你叫我略過的步驟

Nothing — no step was skipped.

## 我不確定你要不要的事

- 第 2 條（從 feature worktree 跨到 main 做 commit）這次無法用真實 session 證明會被擋；你接受靠第 1 條的實測加上第 5 條的文件說明就算完成嗎？
- 計畫文件記著一筆「協調者自己看過 main 上兩種 commit 都被擋」的觀察，但沒有留下證據；跨 worktree 那一種在這次測試中沒有重現出來。
- 這次第 1 條能擋下，表示測試機上的 Codex hook 目前會被執行並生效；「更新後沒核准就擋不住」這個原因本身仍是推論，沒有重現。
