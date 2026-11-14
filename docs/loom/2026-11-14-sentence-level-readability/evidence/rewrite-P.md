# Rewrites P

## EN1
The nightly job still reports success, because the retry code added in the last PR catches the timeout error and does not pass it on. That nightly job is the one the infra team moved to the new runner after two outages; the same team took over the queue in March. I will open a ticket for the fix. Tests cover 62% of the code that detects cache key collisions.

## EN2
The CLI rejects any config file over 2 MB; the config loader, which is the first thing the CLI calls, does the rejecting. The migration finished in 41 seconds. Three services share the orders table, and all three depend on that migration before the 14:00 deploy. Noisy alerts about failed token refreshes dropped from 30 a day to 4 a day.

## EN3
The linter reports problems in 12 files, and in 3 of those files the formatter and the linter give conflicting results. I will pause the import order rule until the update to the pinned parser version is merged. The report that the script generated lists 5 warnings.

## EN4
The hook treats every commit as a release. The check for tags created before version 3.0 never runs on forks. The maintainer who wrote the original guard added that check after the September incident. I approved PR 148.

## ZH1
那個夜間工作還是顯示通過，原因是上一個 PR 加進來的重試程式接住了逾時錯誤，沒有把它往外報。這個夜間工作是基礎設施團隊在兩次當機後搬到新執行機的；這個團隊是三月接手佇列的。快取鍵衝突偵測這部分程式，測試覆蓋率是 62%。部署延後了。遷移沒有跑完。

## ZH2
設定載入器會拒絕超過 2 MB 的檔案。那個遷移花了 41 秒完成；共用訂單資料表的三個服務，在 14:00 部署前都依賴這個遷移。權杖更新失敗的雜訊警示，從每天 30 則降到每天 4 則。警示變少了。門檻調高了。

## ZH3
檢查工具在 12 個檔案上回報了問題，其中 3 個檔案上，格式化工具和檢查工具的結果互相衝突。更新解析器鎖定版本的那個變更，合併流程還沒完成。報告列出 5 個警告。規則暫停了。

## ZH4
這個掛鉤把每個提交都當成發布來處理。針對 3.0 版之前建立的標籤的那個檢查，在分支副本上從來不會執行；這個檢查是寫原始防護的維護者在九月事故後加上的。產生發布說明的腳本，輸出格式是錯的。PR 148 沒有合併。
