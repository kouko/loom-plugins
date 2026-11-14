# Reports B

## R1

### 匯入 CSV 時跳過重複訂單 — 我試了什麼、結果如何

我在 2026-11-13 試的，用的是專案在 4be21c7 的一份乾淨副本。每一條我怎麼試、得到什麼結果，都記在：`docs/loom/2026-11-10-example/evidence/acceptance-test-evidence.md`。

#### 你要求的事，一條一條看

| # | 你要求的事 | 判定 | 實際發生的事 | 重跑 |
|---|---|---|---|---|
| 1 | 匯入的檔案含有重複的訂單編號時，其餘的列照常匯入。 | 可用 | 我匯入一個 50 列、其中 4 列訂單編號重複的檔案，結果 46 列匯入、4 列被跳過。 | — |
| 2 | 匯入結束後，畫面列出每一筆被跳過的列與原因。 | 部分可用 | 畫面列出了 4 筆被跳過的列，每筆都有列號和訂單編號，但其中 1 筆的原因是空白的；那一筆的編號是和同一個檔案裡的另一列重複，而不是和既有的訂單重複。 | — |
| 3 | 既有的訂單不會被匯入的資料覆蓋。 | 可用 | 我比對了 4 筆既有訂單在匯入前和匯入後的內容，所有欄位都一模一樣。 | — |
| 4 | 一萬列的檔案在一分鐘內匯完。 | 部分可用 | 一萬列的檔案第一次匯入花了 48 秒，但第二次花了 71 秒，因為第二次的檔案裡有 2,000 列重複；只有第一次在一分鐘內。 | — |

#### 對你既有的資料做了什麼

匯入只會寫入新的列，你既有的資料沒有任何一筆被改動。我沒有做備份，這次也不需要備份。

#### 我替你做的決定

- **同一個檔案裡有重複的訂單編號時要留哪一筆** — 我選了保留第一次出現的那一列、跳過後面重複的列，而不是把重複的列全部跳過。我的紀錄裡沒有寫下選這個做法的理由。之後要改的話，需要修改一個 function。
- **畫面上最多顯示幾筆被跳過的列** — 我選了畫面上最多顯示 500 筆，完整的清單可以下載成 CSV，而不是在畫面上顯示全部的列。我的紀錄裡沒有寫下選這個做法的理由，也沒有評估之後要改的代價。
- **「被跳過的清單沒有分頁」這個意見被駁回了** — reviewer 提出被跳過的清單沒有分頁，嚴重程度是 important；這個意見被駁回，因為畫面上最多只顯示 500 筆，而且完整的清單可以下載。如果這個理由不成立，問題就會出現在這份清單上。

#### 你叫我跳過的步驟

沒有 — 沒有任何步驟被跳過。

#### 我不確定你要不要的事

- 檔案裡有很多重複的列時，匯入花了 71 秒。這樣可以接受嗎？還是每一個檔案都必須在一分鐘內匯完？

## R2

### Nightly report recalculates after late refunds — what I tried and what happened

Tried on 2026-11-13, in a clean copy of the project at 9d07a1e. How I tried
each line and what came back: `docs/loom/2026-11-10-example/evidence/acceptance-test-evidence.md`.

#### What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | When refunds are posted after the daily report is produced, the report total is recalculated the same day. | partly | A report produced at 09:00 with a total of 1,284,300 was recalculated at 11:45 after 27 refunds were posted at 11:30, and the new total of 1,251,900 matches my hand calculation; but refunds posted after 23:30 are picked up the next day, because the last recalculation of the day runs at 23:30. | — |
| 2 | A recalculated report shows when it was last recalculated. | works | The report showed "Last recalculated 11:45" under the total, and a report that was never recalculated does not show that line. | — |
| 3 | Reports from before this change keep their original numbers. | partly | I compared 30 older reports before and after the change: 29 are identical, but the report for 2026-11-02 changed by 1,150, because the timezone fix in this change also applied to it. | — |

#### What this did to data you already had

The change does not rewrite the stored totals of your old reports. The one difference is the report for 2026-11-02: when you open it, the screen recomputes the total and shows a number that differs by 1,150 from the stored one. The original stored value is still in the database, so the old number can still be read. My notes record no separate backup.

#### I decided for you

- **How often the recalculation runs** — I picked every 15 minutes rather than once for each refund. My notes do not record the reason. Changing it later means changing one config value.
- **Whether a recalculated report is emailed again** — I picked no second email rather than resending the report. My notes record neither the reason nor the cost of changing it later.

No finding of severity important or worse was dismissed.

#### Steps you told me to skip

- The full test suite — skipped on your instruction, 2026-11-12.

#### Things I am not sure you want

- Should a recalculated report email the recipients again?
- Should refunds posted after 23:30 count for the same day?
