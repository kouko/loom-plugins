# Card replies C

## S1

Last night's nightly build failed because the sandbox API key expired on 2026-11-12, and the nightly will keep failing until PR 431 is merged. The fix is ready in that PR, but the PR is still open.

| When | What happened |
|---|---|
| 2026-10-30 | PR 412, an unrelated cleanup, removed the schedule entry of the job that rotates the key. The job has not run since then. |
| 2026-11-12 | The sandbox API key expired, because nothing had rotated it. |
| Last night, 02:10 | The nightly build failed at the integration tests step. 3 tests failed, and all 3 are in the payment module. |
| After the failure | I stored a new key and restored the schedule entry in PR 431. |

I reran the tests with the new key: the 3 payment tests pass, and the full suite shows 1,204 passed and 0 failed.

## S2

No, the full upgrade does not fit in this sprint: it needs 8 days and the sprint has 4 days of free capacity. The smaller first step, migrating invoice export only, needs 5 days, so it is also 1 day over.

The work is large because v5 removes the sync render API. We call that API in 14 places, and 9 of them are in invoice export. The estimate is 6 days of migration plus 2 days to retest invoice export.

| Option | Effort | Fits in 4 days? | What it means for you |
|---|---|---|---|
| Full upgrade this sprint | 8 days | No, 4 days short | Other sprint work has to move out. |
| Invoice export first, the rest next sprint (recommended) | 5 days now, the rest next sprint | No, 1 day short | 9 of the 14 call sites are done first. You need to free 1 more day, or let the work finish early next sprint. |
| Do nothing this sprint, upgrade later | 0 days now | Yes | We stay on v4.8. v4 security fixes end in 2027-03, so the upgrade has to happen before then. |

I recommend the second option, because it covers the largest part of the work and leaves the smallest overrun. If you cannot free 1 more day, the third option is workable, because the security deadline is 2027-03. The second option already combines "a smaller version" and "later", so there is no further combination to consider.

One point about the benefit: the vendor benchmark shows v5 rendering 30-40% faster, but we have not measured it on our own documents.

## S3

Five things changed on the search results page since Monday, and one of them is a new bug: a search with an empty query now returns 0 results instead of all items (ticket 908 is open for it).

| Area | Before | Now |
|---|---|---|
| Default sort | Relevance | Newest (changed on Tuesday, commit a3f9) |
| Results per page | 20 | 25 |
| Filter panel | No "price range" filter | "Price range" filter added |
| Empty query (bug) | Returned all items | Returns 0 results |
| Page load time (p95) | 820 ms | 870 ms |

The page load time went up after the change from 20 to 25 results per page. The "brand" filter did not change.

## S4

Yes, you can run it tonight, on two conditions: take a fresh backup first, and run it between 01:00 and 03:00, when traffic is low. One risk remains unmeasured: nobody has tested the migration against indexes of production size.

| Point | Status | Detail |
|---|---|---|
| Data correctness | Confirmed on staging | The dry run on the staging copy finished with 0 row mismatches. |
| Duration | Confirmed on staging only | The dry run took 38 minutes. Staging holds 60% of the production data, so the production duration is not measured. |
| Rollback | Confirmed once | The rollback script exists. It was tested once on staging and took 12 minutes. |
| Backup | Not current | The last production backup was taken at 06:00 today. The next scheduled one is at 06:00 tomorrow, after the migration. |
| Production-size indexes | Not confirmed | No dry run was done against them. |

What users see during the run: the migration moves 2.1 million order rows to the new partitioned table, and the orders table is read-only for the whole run. Nobody can write to orders during that time.

| Option | What it means |
|---|---|
| Tonight, 01:00-03:00, after a fresh backup (recommended) | The read-only period falls in the low-traffic window. The backup contains today's data if you need to restore. |
| Tonight, without a fresh backup | Not recommended. The only backup is from 06:00 today and does not contain the changes made since then. |
| Later, after a dry run against production-size data | This removes the unmeasured risk. The migration is delayed until that dry run is done. |

A smaller version, migrating only part of the rows, has not been prepared or tested, so I do not offer it. The recommended option already combines the fresh backup and the low-traffic window.

## S5

今天的數字 1,251,900 才是正確的；昨天的報表多算了 32,400，原因是報表在退款入帳之前就產出了，另外有 3 筆訂單的時區算錯。

| 項目 | 昨日報表 | 今日重算 | 差額 |
|---|---|---|---|
| 營收 | 1,284,300 | 1,251,900 | 32,400 |

| 原因 | 筆數 | 金額 | 現況 |
|---|---|---|---|
| 昨日報表在 09:00 產出，退款批次到 11:30 才入帳 | 27 筆退款 | 31,250（差額 32,400 扣掉時區的 1,150 推算） | 還會再發生：退款入帳後，報表不會自動重算，這個功能尚未做 |
| 訂單時間的時區換算錯誤，系統把 UTC 時間當成台北時間 | 3 筆訂單 | 1,150 | 已修正（PR 388，已合併） |

所以在自動重算做好之前，只要報表產出的時間早於當天的退款入帳時間，隔天重算的數字就會比報表低。

## S6

登入頁改版趕不上原訂的 11/21 上線，依目前狀況最快 11/26；5 個工作項目中 2 項完成、1 項進行中、1 項卡住、1 項未開始。

| 工作項目 | 狀態 | 說明 |
|---|---|---|
| 表單樣式 | 完成 | |
| 錯誤訊息文案 | 完成 | |
| 第三方登入按鈕 | 進行中 | Google 已完成。Apple 在等對方審核，送出後已過 4 天。 |
| 行動版排版 | 卡住 | 設計稿缺少 320px 寬度的版本。我已在週二向設計提出，目前還沒拿到。 |
| 無障礙檢查 | 未開始 | 排在行動版排版之後，所以行動版排版沒完成就不能開始。 |

目前有兩件事在等別人：Apple 的審核，以及設計補上 320px 的設計稿。

## S7

我建議採用作法 A：匯入時跳過重複的訂單編號，其餘的列照常匯入，結束後列出被跳過的列。這樣一筆重複不會再讓整批失敗，也不會動到既有訂單，修改量是 1 個函式，約半天。

現況是系統遇到第一筆重複就中止，並把整批資料還原。上週 12 次匯入失敗中，有 9 次是這個原因。

| 作法 | 使用者看到的結果 | 工作量 | 風險或限制 |
|---|---|---|---|
| A：跳過重複列，其餘照匯（建議） | 匯入成功，結束後看到被跳過的列的清單 | 改 1 個函式，約半天 | 被跳過的列需要使用者自己處理 |
| B：重複時用新資料覆蓋舊資料 | 匯入成功，既有訂單被新資料取代 | 未估算 | 會改到既有訂單；客服曾要求不可自動覆蓋，所以不建議 |
| C：維持整批失敗，但錯誤訊息列出所有重複列 | 匯入仍然失敗，但一次看到全部重複列（目前只列第一筆） | 約 2 小時 | 使用者仍須修正檔案後重新匯入 |
| 不處理或延後 | 與現在相同 | 0 | 這類失敗會繼續發生，上週佔 12 次中的 9 次 |

C 是工作量較小的版本，如果這週只有 2 小時可用，可以先做 C。A 和 C 不需要合併，因為 A 結束時已經列出所有被跳過的重複列。資料表有唯一鍵限制，所以三種作法都不會產生重複資料。

## S8

已經查到記憶體是在處理 GIF 時洩漏的，但還不確定問題出在我們的程式還是函式庫；目前服務靠提早重啟和定時重啟維持運作。

出問題的是圖片縮圖服務：記憶體每小時約增加 180 MB，約 9 小時後被系統重啟。

| 項目 | 狀態 | 內容 |
|---|---|---|
| 洩漏發生的情況 | 已確認 | 處理 GIF 時記憶體會增加；處理 JPEG、PNG 時不會增加。 |
| 洩漏的位置 | 已確認 | GIF 每一格解碼後的緩衝區沒有被釋放。 |
| 是誰沒有釋放 | 未確認 | 可能是我們的程式沒有呼叫釋放，也可能是函式庫 3.2 版本身的問題。 |
| 升級能否解決 | 未確認 | 函式庫 3.3 版的更新紀錄提到修正了 GIF 記憶體問題，但還沒有測試。 |

暫時措施已經上線：我把重啟門檻從 2 GB 調到 1.5 GB，並讓服務每 6 小時定時重啟一次。

下一步是在測試環境把函式庫升到 3.3 版，跑 500 張 GIF，觀察記憶體是否還會增加。
