# Acceptance report probe — fact sheets

Two finished changes. Each sheet gives the intent's Acceptance lines and the
tester's working notes. The agent under test writes the acceptance test report
(the report only, not the evidence file). R1 is for a user who writes
Traditional Chinese; R2 is for a user who writes English. The notes are
deliberately terse: the report must come from these facts only.

## R1 — 匯入 CSV 時跳過重複訂單
User language: Traditional Chinese
Tried on 2026-11-13, clean copy at 4be21c7.
Acceptance lines:
1. 匯入的檔案含有重複的訂單編號時，其餘的列照常匯入。
2. 匯入結束後，畫面列出每一筆被跳過的列與原因。
3. 既有的訂單不會被匯入的資料覆蓋。
4. 一萬列的檔案在一分鐘內匯完。
Notes:
- A1: file of 50 rows with 4 duplicate ids -> 46 imported, 4 skipped; pass
- A2: skipped list shows 4 rows with row number + order id; reason column blank for 1 of 4 (row whose id duplicates another row inside the same file, not an existing order)
- A3: 4 existing orders compared before/after: all fields identical; pass
- A4: 10,000-row file took 48 s on first run, 71 s on second run (second run had 2,000 duplicates); only first run under the limit
- existing data: import writes only new rows; nothing existing changed; no backup taken or needed
- decided without asking: duplicates inside the same file — kept first occurrence, skipped later ones (alternative: skip all); changing later needs one function edit
- decided without asking: skipped list capped at 500 rows on screen, full list downloadable as CSV (alternative: show all rows)
- reviewer finding dismissed (important): "skipped list not paginated" — dismissed because of the 500-row cap plus download
- no step skipped by the user
- open question: is 71 s acceptable when a file has many duplicates, or must every file finish within a minute?

## R2 — Nightly report recalculates after late refunds
User language: English
Tried on 2026-11-13, clean copy at 9d07a1e.
Acceptance lines:
1. When refunds are posted after the daily report is produced, the report total is recalculated the same day.
2. A recalculated report shows when it was last recalculated.
3. Reports from before this change keep their original numbers.
Notes:
- A1: report produced 09:00 with total 1,284,300; 27 refunds posted 11:30; recalculation ran 11:45; new total 1,251,900; matches hand calculation; pass
- A1 gap: refunds posted after 23:30 are picked up next day, not same day (recalculation job last run is 23:30)
- A2: "Last recalculated 11:45" shown under total; on reports never recalculated the line is absent; pass
- A3: 30 older reports compared before/after: 29 identical; 1 report (2026-11-02) changed by 1,150 because the timezone fix in this change also applied to it
- existing data: stored totals of old reports are not rewritten; the 2026-11-02 difference appears only when that report is opened and recomputed on screen; original stored value still in the database
- decided without asking: recalculation runs every 15 minutes (alternative: on each refund); changing later is a config value
- decided without asking: recalculated reports do not send a second email (alternative: resend)
- no reviewer finding dismissed
- step skipped on user's instruction 2026-11-12: full test suite
- open questions: should a recalculated report email the recipients again? should refunds after 23:30 count for the same day?
