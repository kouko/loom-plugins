# 簡短的文件交付規則 — what I tried and what happened

Tried on 2026-11-05, in a clean copy of the project at 165ad485ad97db0932d8d1dc0ba7f4994cb86d33. How I tried each line and what came back: `docs/loom/2026-11-04-absolute-user-document-paths/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | loom-code、loom-design 與 loom-workflow 交付本機文件時，提供該文件的實際絕對位置；一般敘述中的檔名、引用的原文與範例不必全部轉換。 | works | 三個插件的實際對話樣本都交付了正確絕對位置；一般檔名與引文保留原樣，其他直接設計入口的指引覆蓋測試也通過。 | re-tested |
| 2 | 已確認支援本機 Markdown 連結的環境使用相對路徑文字與絕對路徑目標，外部文件可用檔名；不支援或支援情況未知時顯示完整絕對路徑，不承諾可以點擊。 | works | 明示支援的三個插件樣本使用文件相對位置作為連結文字、絕對位置作為目標；專案外文件用檔名，明示未知的樣本則顯示完整文字位置。 | re-tested |
| 3 | 交付位置指向當次專案、worktree 或專案外的實際文件；不寫死開發者目錄，不指定必須使用 realpath 或逐字比對程序。 | works | 交付位置均指向各自工作副本或專案外的現存文件；同一文件的有效系統路徑別名也正常通過，沒有要求固定計算程序。 | re-tested |
| 4 | 插件內部資源引用、版本控制內的文件連結與結構化資料中的相對路徑契約保持可攜性。 | works | 相關引用與需求格式的測試通過，實際修改樣本保留既有文件連結及資料內的相對位置；完整自動測試會在接受變更前執行，失敗時阻止接受。 | re-tested |

## 對你既有的資料做了什麼 (what this did to data you already had)

產品變更調整既有插件的文件交付指引、相關測試與發布資訊，不會搬移或重寫你的專案文件；原有相對引用繼續保留，不需資料遷移。此次驗收只在隔離的暫存工作副本中建立需求草稿及修改兩處範例文字，並替換驗收紀錄，沒有更新使用者已安裝的插件或設定。

## I decided for you

- **驗證範圍** — 每輪使用四個各自重新開始的對話樣本；其他直接設計入口以測試確認指引存在，沒有把它們宣稱為逐一行為通過。改成逐入口實測會增加執行量。
- **保留安裝限制** — Codex 新安裝的啟動指引尚未取得主程式信任，所以保留該次未驗證結果；另用 Claude Code 確認同一插件實際載入指引後的交付。沒有替 Codex 寫入信任或繞過保護，日後驗證該組合仍需正常完成信任設定。
- **沿用實作選擇** — 規則留在既有入口，不新增共用服務、不強制路徑計算程序；後續修改需要同步這些入口與測試。

沒有收到被主代理駁回的重大審查問題。

## Steps you told me to skip

沒有，未依你的指示跳過任何驗證步驟。

## Things I am not sure you want

沒有新增的產品選擇待決定。這是有限樣本的驗收，不保證所有回覆都遵守；Codex 程式開發插件在啟動指引取得信任後的行為仍未驗證。未測其他主程式、實際點擊或終端換行行為。
