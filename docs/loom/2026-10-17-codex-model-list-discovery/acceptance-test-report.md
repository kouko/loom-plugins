# Codex review 能列出帳號可用的模型 — 我試了什麼、結果如何

2026-10-17 在專案的乾淨副本（01ac4bf7）上試過。每一條怎麼試、回來什麼：`docs/loom/2026-10-17-codex-model-list-discovery/evidence/acceptance-test-evidence.md`。

## 你要的，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | With a working Codex login, loom's Codex candidate listing returns the account's current models (a non-empty list) instead of a "response missing" failure. | works | 用你這台機器上真實登入的 Codex 列模型，回來 7 個模型名稱；同樣的指令在修改前的版本仍回報「response missing」。 | — |
| 2 | When Codex is reachable but never answers, the listing still ends within its time limit and reports a timeout or failure reason rather than hanging. | works | 換成一個永遠不回話、還多開一個子程序佔住輸出的假 Codex，列表在 15 秒準時結束並回報 timeout，事後沒有殘留程序。 | — |
| 3 | Candidate listing for Claude Code and Antigravity behaves as before, and the complete package suite passes. | works | Claude Code 與 Antigravity 列表那段程式完全沒被改動，涵蓋它們的 38 個測試全部通過；完整測試套件則由正式驗收前一定會跑、失敗就擋下這次變更的自動化測試把關。 | — |

## 對你既有的資料做了什麼

沒有 — 只碰了這次變更自己建立的檔案。測試用的同意紀錄和空資料夾都放在專案外的暫存區，沒有修改你的 Codex 設定，也沒有送出任何程式碼給 Codex，只問了一次模型清單。

## 我替你決定的事

- **假 Codex 的寫法** — 我讓它除了不回話之外，還多開一個子程序佔住輸出，因為這是最容易讓列表卡住或留下殘留程序的情況。如果你在意的是別種「不回話」（例如網路斷線），那種情況這次沒有另外試。

## 你要我跳過的步驟

沒有 — 沒有跳過任何步驟。

## 我不確定你要不要的

沒有。
