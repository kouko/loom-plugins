# 簡短的文件交付規則 — what I tried and what happened

Tried on 2026-11-06, in a clean copy of the project at 08c92ede3adbdec971fc3397db5e7d196cb3fc7a. How I tried each line and what came back: `docs/loom/2026-11-04-absolute-user-document-paths/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | loom-code、loom-design 與 loom-workflow 交付本機文件時，提供該文件的實際絕對位置；一般敘述中的檔名、引用的原文與範例不必全部轉換。 | partly | 八處指引的測試及單一原生對話示範通過；縮短版在各主程式實際載入後的交付尚未重測。 | re-tested |
| 2 | 已確認支援本機 Markdown 連結的環境使用相對路徑文字與絕對路徑目標，外部文件可用檔名；不支援或支援情況未知時顯示完整絕對路徑，不承諾可以點擊。 | partly | 示範分別產出正確連結與完整文字位置；這次沒有操作實際主程式或測試點擊。 | re-tested |
| 3 | 交付位置指向當次專案、worktree 或專案外的實際文件；不寫死開發者目錄，不指定必須使用 realpath 或逐字比對程序。 | partly | 示範的三個位置皆指向隔離工作副本或外部現存文件，含中文與空格；尚無縮短版的跨主程式實測。 | re-tested |
| 4 | 插件內部資源引用、版本控制內的文件連結與結構化資料中的相對路徑契約保持可攜性。 | works | 相關測試通過，示範未改寫既有引用或資料；完整自動測試會在接受變更前執行，失敗時阻止接受。 | re-tested |

## 對你既有的資料做了什麼 (what this did to data you already had)

產品變更調整既有交付指引、相關測試與發布資訊，不搬移或重寫你的專案文件，不需資料遷移。此次只在暫存副本建立測試文件，並替換這兩份驗收紀錄；未更新已安裝插件或設定。

## I decided for you

- **有限驗證** — 本輪採用本機測試與單一原生對話示範；沒有啟動遭拒的外部模型執行，也沒有將舊版樣本當成縮短版通過。日後要確認主程式實際行為，仍需另行取得執行證據。
- **保留實作選擇** — 指引留在既有入口，不新增共用服務；縮寫的提問紀錄與使用者已同意細節規則逐句核對後，未發現義務遺失。

沒有收到被主代理駁回的重大審查問題。

## Steps you told me to skip

沒有，未依你的指示跳過任何驗證步驟；實際主程式載入未重測，已如實列為限制。

## Things I am not sure you want

沒有新增產品選擇待決定。縮短版尚未取得新的實際主程式行為證據；先前 Codex 啟動指引信任限制仍未重驗。單一示範不代表每個入口或主程式均通過，也不保證點擊、終端換行或遵循率。
