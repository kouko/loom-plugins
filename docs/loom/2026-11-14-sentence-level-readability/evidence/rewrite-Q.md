# Rewrites Q

## EN1
The nightly job still reports a pass, because when a timeout happens, the retry code that the last PR added reports no error [retry wrapper]. The infra team moved that job to the new runner after two outages. That team took over the queue in March. I will open a ticket for the fix. Test coverage of the code that detects cache key collisions is at 62%.

## EN2
The config loader does not accept any file over 2 MB. The CLI calls this loader first. The migration finished in 41 seconds. Three services share the orders table, and they depend on this migration before the 14:00 deploy. The noisy alerts about failures of the token refresh dropped from 30 a day to 4 a day.

## EN3
The linter reports problems in 12 files, and in 3 of them the formatter and the linter conflict. I will pause the rule about the order of imports until the update to the pinned version of the parser is merged. The report that the script generated lists 5 warnings.

## EN4
The hook treats every commit as a release. One check never runs on forks. The maintainer who wrote the original guard added that check after the September incident, and it covers tags that were created before version 3.0. I approved PR 148.

## ZH1
那個夜間工作還是顯示通過，因為逾時發生時，上一個 PR 加進來的重試程式不回報錯誤〔重試包裝〕。那個夜間工作是基礎設施團隊在兩次當機後搬到新執行機的；這個團隊在三月接手佇列。偵測快取鍵衝突的那段程式，測試覆蓋率是 62%。部署延後，因為遷移沒跑完。

## ZH2
設定載入器不接受超過 2 MB 的檔案。那個遷移花了 41 秒完成；共用訂單資料表的三個服務在 14:00 部署前都依賴它。權杖更新失敗的雜訊警示從每天 30 則降到每天 4 則。警示變少，因為門檻調高了。

## ZH3
檢查工具回報 12 個檔案有問題，而且格式化工具和檢查工具在 3 個檔案上的要求互相衝突。更新解析器鎖定版本的那個合併流程還沒完成。報告列出 5 個警告，所以規則暫停。

## ZH4
這個掛鉤把每個提交都當成發布來處理。有一個檢查在分支副本上從來不會執行。這個檢查是寫原始防護的維護者在九月事故後加上的，對象是 3.0 版之前建立的標籤。產生發布說明的腳本輸出格式錯了，所以 PR 148 沒合併。
