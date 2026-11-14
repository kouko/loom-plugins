# Card replies B

## S1

Last night's build failed because the test API key for the payment sandbox expired on 2026-11-12, and the nightly build will keep failing until PR 431 is merged.

What happened, in order:

| When | What happened |
|---|---|
| 2026-10-30 | PR 412, an unrelated cleanup, removed the schedule entry of the job that replaces the key. The job has not run since. |
| 2026-11-12 | The sandbox API key expired. |
| Last night, 02:10 | The nightly build failed at the integration test step. 3 tests failed, all in the payment module. |

What I did:

- I stored a new key and restored the schedule entry. Both changes are in PR 431, which is open and not merged.
- I reran the tests with the new key. The 3 payment tests pass, and the full suite shows 1,204 passed and 0 failed.

What you need to do: merge PR 431.

## S2

No, the full upgrade does not fit this sprint: it needs 8 days and the sprint has 4 free days. The smaller first step, migrating invoice export only, needs 5 days, so it also needs 1 more day than we have.

Why it takes this long: v5 removes the synchronous render call. We call it in 14 places, and 9 of them are in invoice export. The 8 days are 6 days of migration plus 2 days of retesting invoice export.

| Option | Work needed | Fits in 4 free days? | What you get | What you give up |
|---|---|---|---|---|
| A. Full upgrade this sprint | 8 days | No, 4 days short | All 14 places are on v5 | Other sprint work has to move out |
| B. Invoice export first, the other 5 places next sprint (recommended) | 5 days this sprint | No, 1 day short | The largest part, 9 of 14 places, is done first | You need to free 1 more day this sprint |
| C. Move the whole upgrade to next sprint | 0 days this sprint | Yes | No change to this sprint | Nothing is done on the upgrade this sprint |

I recommend B if you can free 1 more day, and C if you cannot.

- Waiting is safe for now: v4 keeps receiving security fixes until 2027-03.
- Doing nothing at all is ruled out, because after 2027-03 v4 gets no security fixes.
- A and B cannot be combined: B is the first part of A.
- The vendor's benchmark shows v5 rendering 30-40% faster. Nobody has measured it on our documents, so I would not count on that number yet.

Which option do you want?

## S3

Four things changed on the search results page since Monday, and one bug came in with them: a search with an empty query now returns 0 results instead of all items (ticket 908 is open for it).

| Item | Monday | Now |
|---|---|---|
| Default sort order | Relevance | Newest (commit a3f9, Tuesday) |
| Results per page | 20 | 25 |
| Filter panel | "Brand" filter | "Brand" filter, unchanged, plus a new "price range" filter |
| Page load time (95% of loads finish within) | 820 ms | 870 ms |
| Search with an empty query (bug) | Returns all items | Returns 0 results |

The page load time rose by 50 ms after the change from 20 to 25 results per page.

## S4

Yes, the migration can run tonight, on two conditions: take a fresh backup first, and run it between 01:00 and 03:00, when traffic is low. One thing is untested: how long it takes on the full production data.

What the migration does: it moves 2.1 million order rows to a new partitioned table. While it runs, nobody can write to the orders table; reading still works.

| Question | Status | Evidence |
|---|---|---|
| Does the data arrive intact? | Confirmed on staging | Dry run on the staging copy: 0 row mismatches |
| How long does it take? | Confirmed on staging only | 38 minutes on staging. Staging holds 60% of the production data, and no dry run used production-size indexes |
| Can we undo it? | Confirmed once | The rollback script ran once on staging and took 12 minutes |
| Is the backup recent enough? | Not yet | The last production backup is from 06:00 today. The next scheduled one is 06:00 tomorrow, after the migration |

| Option | What happens | Assessment |
|---|---|---|
| A. Tonight, 01:00-03:00, after a fresh backup | Orders are read-only during the run. If it fails, we roll back or restore from a backup taken just before | Recommended |
| B. Tonight, without a fresh backup | A restore would use the 06:00 backup, which lacks every order written after 06:00 today | Not recommended |
| C. Postpone, and first do a dry run on production-size data | We learn the real duration before the real run. The migration happens on a later night | Choose this if a read-only window of unknown length is not acceptable |

- Not running the migration at all is outside what you asked, so I did not assess it.
- A smaller run, moving only part of the rows, is ruled out: nobody has tested it.
- Option A already combines the two precautions, the fresh backup and the low-traffic window.

Plan for the run on production to take longer than 38 minutes. I have no measured figure for how much longer.

## S5

今天的數字 1,251,900 是正確的；昨天的報表多算了 32,400，原因有兩個，其中一個已修好，另一個之後還會再發生。

| 原因 | 筆數 | 影響金額 | 現況 |
|---|---|---|---|
| 昨天報表在 09:00 產出，退款在 11:30 才入帳，報表沒有扣到這些退款 | 27 筆退款 | 31,250（差額 32,400 減去下一列的 1,150，是我推算的） | 尚未解決 |
| 訂單的時間換算錯誤：系統把 UTC 時間當成台北時間 | 3 筆訂單 | 1,150 | 已修正（PR 388，已合併） |
| 合計 | | 32,400 | |

對你的影響：

- 退款入帳之後，報表不會自動重算。這個自動重算的功能還沒做。
- 所以只要退款在報表產出之後才入帳，當天的報表就會比實際營收高，要重算一次才會正確。

## S6

登入頁改版趕不上原訂的 11/21 上線，依目前狀況最快 11/26；5 個工作項目完成 2 項，1 項進行中，1 項受阻，1 項還沒開始。

| 工作項目 | 狀態 | 說明 |
|---|---|---|
| 表單樣式 | 完成 | |
| 錯誤訊息文案 | 完成 | |
| 第三方登入按鈕 | 進行中 | Google 已完成。Apple 在等對方審核，我們已送出 4 天 |
| 行動版排版 | 受阻 | 設計稿缺少 320px 寬度的版本。我們在週二已向設計提出 |
| 無障礙檢查 | 未開始 | 排在行動版排版之後才做 |

目前有兩件事在等別人：Apple 的審核，以及設計補上 320px 的設計稿。無障礙檢查要等行動版排版做完才能開始。

## S7

我建議採用作法 A：匯入時跳過重複的列，其餘的列照常匯入，結束後列出被跳過的列。這樣一筆重複不會再讓整批失敗，也不會改到既有的訂單。

現況：匯入時遇到第一筆重複的訂單編號就中止，整批資料都不匯入。上週 12 次匯入失敗，其中 9 次是這個原因。

| 作法 | 使用者看到什麼 | 工作量 | 缺點 | 評估 |
|---|---|---|---|---|
| A. 跳過重複的列，其餘照常匯入 | 匯入成功，結束後看到被跳過的列的清單 | 改 1 個函式，約半天 | 使用者要自己處理被跳過的列 | 建議 |
| B. 重複時用新資料覆蓋舊資料 | 匯入成功，既有訂單被改成新資料 | 我沒有估算 | 會改到既有訂單，客服曾要求不可自動覆蓋 | 不建議 |
| C. 維持整批失敗，但錯誤訊息列出所有重複的列 | 匯入仍然失敗，但一次看到全部重複的列（目前只看到第一筆） | 約 2 小時 | 使用者仍要修改檔案後重新匯入 | 可行，是比 A 小的版本 |

- 三種作法都不會產生重複資料，因為資料表本身有唯一鍵限制。
- 不處理或延後處理：我不建議，因為這個原因上週造成 12 次失敗中的 9 次。
- A 和 C 不能合併：A 讓匯入繼續，C 讓匯入整批失敗。A 結束後的清單已經提供 C 想給的資訊。
- 如果這週只能花 2 小時，可以先做 C，之後再改成 A。

你要採用哪一個？

## S8

問題的位置已經找到：圖片縮圖服務在處理 GIF 時，每一格解碼後的緩衝區沒有釋放，所以記憶體一直增加。還沒查清楚的是，這是我們的程式沒有呼叫釋放，還是函式庫 3.2 版本身的問題。服務目前靠定時重啟維持運作。

症狀：記憶體每小時約增加 180 MB，約 9 小時後服務被系統重啟。

| 項目 | 狀態 |
|---|---|
| 洩漏發生在處理 GIF 時；處理 JPEG、PNG 時記憶體不會增加 | 已確認 |
| GIF 每一格解碼後的緩衝區沒有釋放 | 已確認 |
| 原因是我們的程式沒有呼叫釋放，還是函式庫 3.2 版本身的問題 | 未確認 |
| 函式庫 3.3 版能不能解決（它的更新紀錄提到修正 GIF 記憶體問題） | 未確認，還沒測試 |

暫時措施（已完成）：

- 我把重啟門檻從 2 GB 調低到 1.5 GB。
- 我設定服務每 6 小時定時重啟一次。

下一步：我會在測試環境把函式庫升到 3.3 版，處理 500 張 GIF，觀察記憶體是否還會增加。
