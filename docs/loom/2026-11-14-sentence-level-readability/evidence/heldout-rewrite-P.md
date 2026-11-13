# Held-out rewrites P

## EN1
A join drops 214 rows, because the orders model that the dashboard reads cannot handle orders with no store id. The analyst who rebuilt the weekly revenue report in October rewrote that join after the audit so that it uses the new calendar table. I will not fix the handling of empty store ids now; I will put it on the list of work to do later. The check on whether the daily revenue snapshot is up to date has a delay of 9 minutes.

## EN2
The importer relies on a date parser that cannot read two-digit years. The finance team, which owns the tax ledger, asked for an export before the quarter close on the 28th; that export ran in 3 minutes. The rate at which vendor invoices are matched as duplicates fell from 7% to 2%.

## EN3
After a restart, the scheduler no longer has its jobs, and the queue gives the 4 slow workers no work. I will turn off the old cron bridge after the change to the worker pool size limit is released. The log that the agent attached shows 17 timeouts.

## EN4
The cache keeps using out-of-date prices for 15 minutes. The alert for refunds larger than 500 dollars never fires at night; the on-call engineer who inherited the pricing service set it up after the August outage. I approved ticket 3172 without checking it.

## ZH1
有一個關聯查詢少了 214 筆資料，原因是儀表板讀取的訂單模型無法處理門市編號是空的訂單。這個關聯查詢是十月重做每週營收報表的那位分析師在稽核後重寫的，目的是改用新的日曆表。檢查「每日營收快照是不是最新」的那項檢查，延遲是 9 分鐘。報表比較晚產出。排程重新執行了。

## ZH2
匯入程式依賴的日期解析器無法讀取兩位數的年份。負責稅務帳本的財務團隊在 28 日季結前要求了一份匯出，那份匯出執行了 3 分鐘。廠商發票被比對為重複的比率從 7% 降到 2%。比對變快了。索引重建了。

## ZH3
排程器重啟後，原本的工作不見了，而且佇列沒有把工作分給 4 個慢速工作程序。調整工作程序池大小上限的那項變更，上線流程還沒完成。記錄檔顯示有 17 次逾時。舊的橋接停用。

## ZH4
快取會繼續使用過期的價格，長達 15 分鐘。針對超過 500 元退款的那個警示，在夜間從來不會觸發；這個警示是八月當機後接手定價服務的值班工程師設定的。退款通知的寄送範本裡，欄位對應錯了。工單 3172 沒有關閉。
