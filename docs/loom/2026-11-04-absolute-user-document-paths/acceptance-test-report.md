# 簡短的文件交付規則 — what I tried and what happened

Tried on 2026-11-06, in a clean copy of the project at 5306d04b4d36c22b87f0fba190338095b2515a65. How I tried each line and what came back: `docs/loom/2026-11-04-absolute-user-document-paths/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | loom-code、loom-design 與 loom-workflow 交付本機文件時，提供該文件的實際絕對位置；一般敘述中的檔名、引用的原文與範例不必全部轉換。 | partly | 八處指引的測試通過；Claude 工程入口與明確指定的 Codex 工作流程入口已實際載入同文規則並正確交付，但新版設計入口尚未實測。 | re-tested |
| 2 | 已確認支援本機 Markdown 連結的環境使用相對路徑文字與絕對路徑目標，外部文件可用檔名；不支援或支援情況未知時顯示完整絕對路徑，不承諾可以點擊。 | partly | 兩例分別正確產出含空白的連結與完整文字位置；尚未涵蓋新版所有入口，不保證點擊或終端換行。 | re-tested |
| 3 | 交付位置指向當次專案、worktree 或專案外的實際文件；不寫死開發者目錄，不指定必須使用 realpath 或逐字比對程序。 | partly | 兩例及本輪原生示範皆指向正確工作副本或外部現存文件；新版設計入口與 Codex 工程入口仍有未驗範圍。 | re-tested |
| 4 | 插件內部資源引用、版本控制內的文件連結與結構化資料中的相對路徑契約保持可攜性。 | works | 相關測試通過，兩例與原生示範保留原引用及資料；完整自動測試會在接受變更前執行，失敗時阻止接受。 | re-tested |

## 對你既有的資料做了什麼 (what this did to data you already had)

產品變更調整既有交付指引、相關測試與發布資訊，不搬移或重寫你的專案文件，不需資料遷移。此次只在暫存副本建立測試文件，並替換這兩份驗收紀錄；未更新已安裝插件或設定。

## I decided for you

- **有限驗證** — 本輪獨立執行乾淨副本的測試與原生示範，另核對你明確同意的兩例外部執行紀錄；那兩例測的是與本輪交付指引完全相同的前一提交，兩次提交只差計畫紀錄。未再啟動其他模型，也未把舊版設計樣本當成新版通過。
- **保留實作選擇** — 指引留在既有入口，不新增共用服務；縮寫的提問紀錄與使用者已同意細節規則逐句核對後，未發現義務遺失。

沒有收到被主代理駁回的重大審查問題。

## Steps you told me to skip

沒有，未依你的指示跳過任何驗證步驟；未涵蓋的主程式與入口已如實列為限制。

## Things I am not sure you want

沒有新增產品選擇待決定。兩例不能證明自動觸發、每個入口均通過或整體遵循率；Codex 工程入口在允許載入啟動指引後的行為仍未重驗。先前缺少空白路徑括號與未知支援未觀察到規則載入的紀錄仍保留。
