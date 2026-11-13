# Dogfood samples

Eight chat replies an agent might send to a user. Each contains several of the
five sentence shapes under test and several checkable facts (numbers, names,
outcomes). The samples were written for this probe and reuse none of the
guide's own example sentences.

## EN1
The retry wrapper the last PR added eats the timeout, so the nightly job that the infra team who took over the queue in March moved to the new runner after two outages still reports green. I'll ticket the fix. Cache key collision detection test coverage is at 62%.

## EN2
The config loader the CLI calls first refuses any file over 2 MB. The migration that the three services which share the orders table depend on before the 14:00 deploy finished in 41 seconds. Token refresh failure alert noise dropped from 30 to 4 a day.

## EN3
The linter complains about 12 files and the formatter fights it on 3 of them. I'll shelve the import order rule until the parser version pin update lands. The report the script generated lists 5 warnings.

## EN4
The hook thinks every commit is a release. The check that the maintainer who wrote the original guard added for tags created before version 3.0 after the September incident never runs on forks. I greenlit PR 148.

## ZH1
上一個 PR 加進來的重試包裝吃掉了逾時錯誤，三月接手佇列的基礎設施團隊在兩次當機後搬到新執行機的那個夜間工作還是顯示通過。快取鍵衝突偵測測試覆蓋率是 62%。部署延後，遷移沒跑完。

## ZH2
設定載入器拒絕超過 2 MB 的檔案。共用訂單資料表的三個服務在 14:00 部署前都依賴的那個遷移花了 41 秒完成。權杖更新失敗警示雜訊從每天 30 則降到 4 則。警示變少，門檻調高了。

## ZH3
格式化工具和檢查工具在 3 個檔案上打架，檢查工具抱怨了 12 個檔案。解析器版本鎖定更新合併流程還沒完成。報告列出 5 個警告，規則暫停。

## ZH4
這個掛鉤以為每個提交都是發布。九月事故後寫原始防護的維護者為 3.0 版之前建立的標籤加上的那個檢查在分支副本上從來不會執行。發布說明產生腳本輸出格式錯了，PR 148 沒合併。
