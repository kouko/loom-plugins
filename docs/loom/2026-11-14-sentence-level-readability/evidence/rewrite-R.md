# Rewrites R

## EN1
The nightly job still reports green, because the retry wrapper that the last PR added does not report a timeout when one happens. The infra team took over the queue in March, and they moved this nightly job to the new runner after two outages. I will open a ticket for the fix. Test coverage of the code that detects cache key collisions is at 62%.

## EN2
The config loader will not load any file over 2 MB. The CLI calls this loader first. The migration finished in 41 seconds. Three services share the orders table, and they depend on that migration before the 14:00 deploy. The number of noisy alerts about failed token refreshes dropped from 30 a day to 4 a day.

## EN3
The linter reports problems in 12 files, and on 3 of those files the formatter and the linter conflict. I will leave the rule about import order out until the update to the pinned parser version is merged. The report that the script generated lists 5 warnings.

## EN4
The hook treats every commit as a release. One check never runs on forks. The maintainer who wrote the original guard added that check after the September incident, and it covers tags that were created before version 3.0. I approved PR 148.

## ZH1
那個夜間工作還是顯示通過。發生逾時的時候，上一個 PR 加進來的重試包裝不回報這個錯誤。這個夜間工作，是三月接手佇列的基礎設施團隊在兩次當機後搬到新執行機的。偵測快取鍵衝突的那段程式，測試覆蓋率是 62%。部署延後了。遷移沒跑完。

## ZH2
設定載入器不接受超過 2 MB 的檔案。那個遷移花了 41 秒完成；共用訂單資料表的三個服務，在 14:00 部署前都依賴它。權杖更新失敗的警示裡屬於雜訊的，從每天 30 則降到 4 則。警示變少了。門檻調高了。

## ZH3
檢查工具在 12 個檔案回報了問題。格式化工具和檢查工具在 3 個檔案上的要求互相衝突。更新解析器鎖定版本的那個變更，合併流程還沒完成。報告列出 5 個警告。規則暫停了。

## ZH4
這個掛鉤把每個提交都當成發布來處理。有一個檢查在分支副本上從來不會執行；它是寫原始防護的維護者在九月事故後，為 3.0 版之前建立的標籤加上的。產生發布說明的腳本，輸出格式錯了。PR 148 沒合併。
