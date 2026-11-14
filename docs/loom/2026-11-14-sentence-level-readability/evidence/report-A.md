# Reports A

## R1

### 匯入 CSV 時跳過重複訂單 — 我試了什麼、結果如何

2026-11-13 在專案的一份乾淨副本（4be21c7）上試的。每一條怎麼試、得到什麼：`docs/loom/2026-11-10-example/evidence/acceptance-test-evidence.md`。

#### 你要求的事，一條一條看

| # | 你要求的事 | 結論 | 實際發生的事 | 重跑 |
|---|---|---|---|---|
| 1 | 匯入的檔案含有重複的訂單編號時，其餘的列照常匯入。 | 正常 | 一個 50 列、其中 4 列訂單編號重複的檔案，匯入了 46 列，跳過 4 列。 | — |
| 2 | 匯入結束後，畫面列出每一筆被跳過的列與原因。 | 部分正常 | 畫面列出 4 筆被跳過的列，都有列號和訂單編號，但其中 1 筆的原因是空白的：那一列重複的是同一個檔案裡的另一列，不是既有的訂單。 | — |
| 3 | 既有的訂單不會被匯入的資料覆蓋。 | 正常 | 比對了 4 筆既有訂單匯入前後的內容，所有欄位都一樣。 | — |
| 4 | 一萬列的檔案在一分鐘內匯完。 | 部分正常 | 第一次匯入一萬列花了 48 秒；第二次的檔案有 2,000 列重複，花了 71 秒，超過一分鐘。 | — |

#### 對你既有的資料做了什麼

既有的資料沒有任何改變。匯入只會新增列，不會改動原本就在的訂單。這次沒有做備份，也不需要備份。

#### 我替你決定的事

- **同一個檔案裡出現重複的訂單編號時怎麼處理** — 我選了保留第一次出現的那一列、跳過後面的，另一個做法是全部跳過。之後要改的話，要改一個 function。
- **畫面上最多顯示多少筆被跳過的列** — 我選了畫面上最多顯示 500 筆，完整清單可以下載成 CSV，另一個做法是全部顯示在畫面上。之後要改的代價我沒有評估過。
- **「被跳過的清單沒有分頁」這項意見沒有採納** — 審查的人提出這項意見，嚴重程度是「重要」；沒有採納，是因為畫面已經限制在 500 筆，而且完整清單可以下載。如果這個理由不成立，問題會出現在被跳過的列超過 500 筆的時候：畫面上看不到全部，只能靠下載。

#### 你叫我跳過的步驟

沒有 — 沒有任何步驟被跳過。

#### 我不確定你要不要的事

- 檔案裡有很多重複訂單時，匯入花了 71 秒。這樣可以接受嗎？還是每一個檔案都必須在一分鐘內匯完？

## R2

### Nightly report recalculates after late refunds — what I tried and what happened

Tried on 2026-11-13, in a clean copy of the project at 9d07a1e. How I tried
each line and what came back: `docs/loom/2026-11-10-example/evidence/acceptance-test-evidence.md`.

#### What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | When refunds are posted after the daily report is produced, the report total is recalculated the same day. | partly | A report produced at 09:00 with a total of 1,284,300 was recalculated at 11:45, after 27 refunds were posted at 11:30, and the new total of 1,251,900 matches my hand calculation; but refunds posted after 23:30 are picked up the next day, not the same day. | — |
| 2 | A recalculated report shows when it was last recalculated. | works | "Last recalculated 11:45" appears under the total, and a report that was never recalculated does not show the line. | — |
| 3 | Reports from before this change keep their original numbers. | partly | Of 30 older reports compared before and after, 29 are identical; the report for 2026-11-02 differs by 1,150, because the timezone fix in this change also applied to it. | — |

#### What this did to data you already had

The stored totals of your old reports were not rewritten. The one difference, on the 2026-11-02 report, appears only when that report is opened and recomputed on screen; its original stored value is still in the database, so the old number can still be read. I did not record a separate backup.

#### I decided for you

- **How often the recalculation runs** — I picked every 15 minutes rather than on each refund. Changing it later means changing one config value.
- **Whether a recalculated report is emailed again** — I picked no second email rather than resending. I did not assess what changing it later would cost.

No finding of severity important or worse was dismissed.

#### Steps you told me to skip

- The full test suite — skipped on your instruction, 2026-11-12.

#### Things I am not sure you want

- Should a recalculated report email the recipients again?
- Should refunds posted after 23:30 count for the same day?
