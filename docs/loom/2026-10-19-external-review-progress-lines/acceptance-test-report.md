# 外部審查顯示「還在跑」— 我試了什麼、結果如何

2026-10-20 在專案的乾淨副本（949aca74）上試。每一條怎麼試、回來什麼：`docs/loom/2026-10-19-external-review-progress-lines/evidence/acceptance-test-evidence.md`。

全程用假的 Claude Code CLI 代替真的外部審查者，沒有任何審查內容送到廠商、沒有網路連線。進度間隔用出貨的 60 秒，沒有縮短；只有「逾時」那一案把審查上限從 30 分鐘縮成 70 秒，才不用等滿 30 分鐘。

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | While an outside review step runs longer than a minute, a progress line appears about once a minute stating the step, the elapsed time, and the time since the CLI last produced output. | works | 一個跑了 2 分 20 秒的審查，在第 1、2 分鐘各出現一行「review still running · 1m00s elapsed · last output 29s ago」這類進度；不到一分鐘就結束的步驟不印進度行。 | — |
| 2 | When a step ends — completed, failed or timed out — one closing line reports its total time and the longest silence observed. | works | 成功、失敗（exit 3）、審查逾時、preflight 逾時四種結束方式，各印剛好一行收尾，寫出總時間和最長安靜時間，數字和假 CLI 的實際節奏吻合（例如安靜 1m50s）。 | — |
| 3 | While the station waits for an outside review, the agent relays the progress lines to the maintainer instead of waiting silently. | partly | 外部審查的 skill 已寫明「背景執行、盯著錯誤輸出、把每行進度轉告使用者」，而兩個會發起外部審查的流程都經過這個 skill；我也確認指令在背景跑時，進度行一寫出就讀得到。但我沒有實際讓一個 agent 跑完一次審查、親眼看它轉告。 | — |
| 4 | The review result, its pass/fail status, the timeout behaviour and every existing outcome are unchanged, and the complete package suite passes. | works | 五種情境在改動前後各跑一次，回傳的結果、成敗、結束碼、逾時時間點完全相同，唯一差別是多了進度行；進度行裡找不到審查內容或 CLI 輸出的文字。這支程式自己的 129 個測試全過；完整 package suite 由驗收前的 automated test suite 執行，失敗就擋下這次變更。 | — |

## 對你既有的資料做了什麼 (what this did to data you already had)

沒有 — 這次變更只是讓外部審查在執行時多印幾行診斷訊息到錯誤輸出，不讀也不寫你既有的任何檔案或紀錄，回傳給流程的結果格式也沒變。

## I decided for you

- **進度行印在錯誤輸出，不放進結果** — 我選錯誤輸出，因為流程只解析標準輸出那一份結果；放進結果會改變它的格式。之後想把「最長安靜」存進結果，就要一併改讀結果的流程。
- **固定每 60 秒一行、只往下加、不覆寫同一行** — 依你把 30 秒改成 60 秒的決定；不做越來越久的間隔。之後想調整只需改一個數字。
- **「上次輸出」只算 CLI 寫完整的一行（標準輸出或錯誤輸出都算）** — 半行不算。Claude Code 和 Antigravity 通常到結束才輸出，所以它們的進度行多半是「no output yet」，這是預期，不是故障。
- **只有 preflight 和審查兩步會報進度，查模型清單那一步不報** — 因為它最多 15 秒。

沒有任何 important 以上的 finding 被駁回。

## Steps you told me to skip

Nothing — no step was skipped.

## Things I am not sure you want

- 第 3 條我只能從指令文字和背景執行的行為判斷，沒有親眼看到 agent 在真實審查中轉告進度。你要接受這個程度，還是要在下一次真實的外部審查時順便確認它真的有轉告？
- Claude Code 和 Antigravity 執行中幾乎不輸出，它們的「最長安靜」通常就等於整段審查時間。用這類資料決定未來的「多久沒輸出算卡住」門檻時，恐怕只有 Codex 的數字有參考價值 — 這符合你的預期嗎？
