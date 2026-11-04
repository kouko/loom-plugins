# 對話中的文件位置統一使用絕對路徑 — what I tried and what happened

Tried on 2026-11-04, in a clean copy of the project at adad5c7cd2830bc783c9325fbf2feed53989e605. How I tried each line and what came back: `docs/loom/2026-11-04-absolute-user-document-paths/evidence/acceptance-test-evidence.md`.

## What you asked for, one line at a time

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | Loom 對話中提供給使用者的本機文件位置皆為絕對路徑，涵蓋 loom-code、loom-design 與 loom-workflow 的文件交付。 | works | 三組各自重新開始的 Codex 對話樣本都交付了絕對路徑；相關測試通過，完整自動測試會在接受變更前執行，失敗時阻止接受。 | — |
| 2 | 支援本機文件連結的對話環境使用絕對路徑作為連結目標；顯示名稱可保留簡短檔名。 | works | 樣本中的連結目標皆為絕對路徑，顯示名稱簡短，含空白與中文字的目標也保留完整。 | — |
| 3 | 在不同專案目錄與 worktree 中交付文件時，路徑均指向該次工作的實際文件位置，不固定使用開發者的電腦路徑。 | works | 樣本正確指向另外建立的工作副本及專案外文件，沒有套用插件開發目錄。 | — |
| 4 | 插件內部資源引用、版本控制內的文件連結與結構化資料中的相對路徑契約保持可攜性。 | works | 相對資源引用的測試通過，樣本保留文件內連結與儲存資料中的相對路徑，測試資料也維持原樣。 | — |

## 對你既有的資料做了什麼 (what this did to data you already had)

這次修改既有插件的對話指引、測試與版本發布資訊，並新增驗證紀錄；沒有重寫你的專案文件或既有文件連結。原有相對路徑格式繼續保留，因此不需要資料遷移或備份。

## I decided for you

- **規則放置方式** — 使用共用對話指引及可直接使用的設計入口，避免改寫每一份文件內的相對引用；日後調整規則需同步這些入口。
- **連結顯示方式** — 支援本機連結時使用絕對目標與簡短名稱，含空白時保護整段目標；不支援連結時顯示完整位置，日後改變此方式需更新指引與測試。
- **版本更新幅度** — 對三個受影響插件提升次版本，讓新的對話指引可以隨更新發送；日後改回較小幅度會影響版本紀錄。

## Steps you told me to skip

沒有，未依你的指示跳過任何驗證步驟。

## Things I am not sure you want

沒有待你決定的問題。行為實測限於三組重新開始的 Codex 對話；其他主程式、模型與實際點擊連結的介面行為尚未驗證。
