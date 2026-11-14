# Card replies A

## S1

Last night's build failed because the test key for the payment sandbox expired on 2026-11-12, and the nightly build will keep failing until PR 431 is merged.

The build failed at 02:10 in the integration test step. Three tests failed, all in the payment module.

| Date | What happened |
|---|---|
| 2026-10-30 | PR 412, an unrelated cleanup, removed the schedule entry of the job that renews the key. The job has not run since. |
| 2026-11-12 | The sandbox API key expired. |
| Last night, 02:10 | The three payment tests failed and the build failed with them. |

I have stored a new key and restored the schedule entry in PR 431. That PR is open and not merged. With the fix in place I reran the tests: the three payment tests pass, and the full suite shows 1,204 passed and 0 failed.

## S2

Not the whole upgrade: it needs 8 days and the sprint has 4 free. I recommend starting it next sprint.

The work is 6 days of migration plus 2 days of retesting invoice export. Version 5 removes the synchronous render call, which we use in 14 places, 9 of them in invoice export.

| Option | Work | Fits in the 4 free days? | What it means for you |
|---|---|---|---|
| A. Full upgrade this sprint | 8 days | No, 4 days over | Other sprint work has to be dropped to make room. |
| B. Invoice export only this sprint, the rest next sprint | 5 days now | No, 1 day over | Possible only if you free one more day. Two library versions are in use until the rest is done. |
| C. Start the upgrade next sprint (recommended) | 8 days, planned in advance | Nothing needed this sprint | No gain this sprint. Version 4 keeps receiving security fixes until 2027-03. |

Why C: nothing forces the upgrade this sprint. The security deadline is March 2027. The speed gain is 30-40% in the vendor's benchmark, and nobody has measured it on our documents.

Other choices I considered:

- Not upgrading at all is ruled out, because security fixes for version 4 end in 2027-03.
- Option B is the smaller version. Choose it if you can free the fifth day.
- Combining A and B gives nothing new: B followed by the remaining work next sprint is the full upgrade.

## S3

Five things changed on the search results page since Monday, and one of them is a bug: a search with an empty query now returns no results.

| What | Before | Now |
|---|---|---|
| Default sort order | By relevance | Newest first (changed Tuesday, commit a3f9) |
| Results per page | 20 | 25 |
| Filter panel | No price filter | "Price range" filter added |
| Empty query | Returned all items | Returns 0 results. This is a bug; ticket 908 is open. |
| Page load time (p95: 95% of loads finish within this time) | 820 ms | 870 ms, measured after the change to 25 results per page |

The "brand" filter did not change.

## S4

Yes, with two conditions: take a fresh backup first, and run it between 01:00 and 03:00. One thing has not been tested, which is how long the migration takes on the full production data.

The migration moves 2.1 million order rows to a new partitioned table. While it runs, nobody can create or change orders; orders can only be read.

| Question | Status | Evidence |
|---|---|---|
| Does the data arrive intact? | Confirmed on staging | Dry run on a staging copy: 0 row mismatches. |
| How long does it take? | Confirmed on staging only | 38 minutes on staging, which holds 60% of the production data. |
| How long does it take on production? | Not confirmed | No dry run has been done against indexes of production size. |
| Can we undo it? | Confirmed once | The rollback script was tested once on staging and took 12 minutes. |
| Is there a current backup? | No | The last backup is from 06:00 today. The next scheduled one is 06:00 tomorrow, after the migration. |

| Option | What it means for you |
|---|---|
| A. Run tonight, 01:00-03:00, after a fresh backup (recommended) | Orders are read-only during the hours with the least traffic. If something goes wrong, the backup holds everything up to the start. |
| B. Run tonight without a fresh backup | If you have to restore, every order change made after 06:00 today is lost. |
| C. Postpone until a dry run at production size is done | The duration is known before the real run. The migration moves to a later night. |

Why A: the fresh backup removes the largest risk, and the low-traffic window limits how many users meet the read-only period. If the production run time is what worries you most, choose C. I have not looked at migrating only part of the rows, so I do not offer that as an option.

## S5

今天的數字 1,251,900 是正確的；昨天的 1,284,300 多算了 32,400，原因有兩個。

| 原因 | 筆數 | 金額 | 現況 |
|---|---|---|---|
| 昨天報表在 09:00 產出，退款到 11:30 才入帳，所以報表沒有扣掉這些退款 | 27 筆退款 | 31,250 | 尚未處理。退款入帳後報表不會自動重算，之後還會發生。 |
| 訂單時間換算錯誤：系統把 UTC 時間當成台北時間 | 3 筆訂單 | 1,150 | 已修正（PR 388，已合併）。 |
| 合計 | | 32,400 | |

之後只要退款在報表產出後才入帳，當天的報表數字就會偏高，要到重算之後才正確。「退款入帳後自動重算」這個功能還沒做。

## S6

登入頁改版趕不上原訂的 11/21，依目前狀況最快 11/26 上線。5 個項目完成 2 個，1 個進行中，1 個卡住，1 個還沒開始。

| 項目 | 狀態 | 說明 |
|---|---|---|
| 表單樣式 | 完成 | |
| 錯誤訊息文案 | 完成 | |
| 第三方登入按鈕 | 進行中 | Google 已完成。Apple 在等對方審核，送出已 4 天。 |
| 行動版排版 | 卡住 | 設計稿缺 320px 寬度的版本，週二已向設計提出。 |
| 無障礙檢查 | 未開始 | 排在行動版排版之後，要等行動版完成才能開始。 |

目前有兩件事在等別人：Apple 的審核，以及設計補上 320px 的設計稿。

## S7

我建議採用作法 A：遇到重複的訂單編號就跳過那一列，其餘照常匯入，結束後列出被跳過的列。這樣一筆重複不會再讓整批失敗，約半天可以完成。

現況是遇到第一筆重複就中止，整批資料都不匯入。上週 12 次匯入失敗裡有 9 次是這個原因。

| 作法 | 使用者會看到什麼 | 工作量 | 風險 |
|---|---|---|---|
| A. 跳過重複列，其餘照匯（建議） | 匯入成功，並看到一份被跳過的列的清單 | 改 1 個函式，約半天 | 既有訂單不會被改動 |
| B. 用新資料覆蓋舊資料 | 匯入成功，重複的訂單變成新內容 | 未估算 | 會改到既有訂單。客服曾要求不可自動覆蓋。 |
| C. 維持整批失敗，但錯誤訊息列出所有重複列 | 匯入仍然失敗，但一次看到全部重複列（目前只列第一筆） | 約 2 小時 | 使用者仍要自己刪掉重複列再重新匯入 |

三種作法都不會產生重複資料，因為資料表本身有唯一鍵限制。

其他選擇：

- 不處理：不建議。上週 12 次失敗中的 9 次會繼續發生。
- 較小的版本：就是作法 C。如果這週排不出半天，可以先做 C。
- 合併兩種作法：不需要。A 已經會列出被跳過的列，包含了 C 提供的資訊。
- 作法 B：排除，因為違反客服的要求。

## S8

已經找到記憶體是在哪裡漏掉的：縮圖服務處理 GIF 時，每一格解碼後的緩衝區沒有釋放。還不知道的是，問題出在我們的程式還是函式庫本身，所以目前還沒有修好，服務靠定時重啟維持運作。

症狀是圖片縮圖服務的記憶體每小時約增加 180 MB，約 9 小時後被系統重啟。

| 項目 | 狀態 |
|---|---|
| 洩漏發生在處理 GIF 時；處理 JPEG、PNG 不會增加記憶體 | 已確認 |
| GIF 每一格解碼後的緩衝區沒有釋放 | 已確認 |
| 是我們的程式沒有呼叫釋放，還是函式庫 3.2 版本身的問題 | 未確認 |
| 函式庫 3.3 版能不能解決（它的更新紀錄提到修正 GIF 記憶體問題） | 未確認，尚未測試 |

暫時措施已經上線：重啟門檻從 2 GB 調到 1.5 GB，並且每 6 小時定時重啟一次。

下一步是在測試環境把函式庫升到 3.3 版，跑 500 張 GIF，觀察記憶體是否還會增加。
