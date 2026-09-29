# 各 plugin 只用自己的檔案 — 我試了什麼、結果如何

2026-09-29 在專案的乾淨複本（6e360dd）上試。每一條怎麼試、回來什麼：`docs/loom/2026-09-29-remove-cross-plugin-file-reads/evidence/acceptance-test-evidence.md`。

## 你要的，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | loom-design 與 loom-workflow 執行時會用到的 skill、reference、腳本與 hook 中，沒有任何一處需要讀或執行 loom-code 資料夾裡的檔案；在沒有 loom-code 檔案可讀的環境中照著它們的步驟做，不會因為找不到 loom-code 而停下。 | works | 我只把這兩個 plugin 拿出來放在沒有 loom-code 的地方，逐一讀過它們的步驟，沒有一步要去找 loom-code；實際跑 session 分析和 decision map 開新交付，兩者都正常完成。 | — |
| 2 | loom-design 與 loom-workflow 帶的範本複本和 loom-code 的原版內容一致；任一邊改了而另一邊沒改時，測試會失敗。 | works | 我分別只改複本、只改原版、只改寫進說明裡的需求編號格式，三次測試都失敗並點名是哪一份；改回去就通過。loom-workflow 本身沒有帶範本複本，所以這條只落在 loom-design。 | — |
| 3 | 在 loom-design 或 loom-workflow 執行時會用到的檔案中加入一個讀取 loom-code 檔案的寫法（包含腳本與 `<loom-code>` 這類路徑寫法）時，自動的邊界檢查會擋下。 | works | 我在說明文件、Python、shell、hook 設定檔、沒有副檔名的 hook 和 `<loom-code>` 寫法裡各塞一個讀 loom-code 的寫法，邊界檢查每一次都擋下並指出哪一行；拿掉後又回到通過。 | — |
| 4 | 原本 loom-design 寫完 intent 當下做的每一項 intent 格式檢查（結構、product 問題不得含識別字、needs-design 理由與 commit 一致、needs-design 重新計算），在 loom-code 的 write-plan 開始規劃前都會執行；故意寫錯任一項的 intent 會在 write-plan 被擋下。 | works | write-plan 現在對已確認的 intent 先跑這項檢查、通過才往下規劃；我做了六份各錯一項的 intent，每一份都被擋下並說明錯在哪，一份正確的則通過。 | — |
| 5 | product 變更遇到 repo 沒有已批准的原則文件時，原則訪談仍在第一次確認 intent 的同一段對話中進行，不會延到後面的站。 | works | capture-intent 的步驟仍寫明：沒有已批准的原則文件就在同一段對話裡當場訪談，並和 intent 一起在同一則訊息確認；訪談用的範本就在 loom-design 裡。這條我是讀步驟說明確認的，沒有跟真人跑一次完整對話。 | — |
| 6 | 三個 plugin 的版號各自升級，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。 | works | 三個 plugin 分別升到 3.23.0、2.7.0、5.5.5，每個 plugin 的三份 manifest、CHANGELOG、各語言 README 都對得上，版號相關測試全部通過；完整自動測試也通過，而它在變更被接受前還會再跑一次、失敗就擋下。 | — |

## 對你既有的資料做了什麼

沒有。這次只改了這個 repo 裡 plugin 自己的說明、範本、檢查腳本和測試；我的測試都在暫存的乾淨複本和暫存 repo 裡做，做完已刪掉。

## 我替你決定的

- **write-plan 在哪一步跑 intent 檢查** — 放在「先開分支」之後、決定要不要 spec 之前，因為在主幹上這項檢查會直接拒絕工程類 intent。代價是格式錯誤要到規劃時才被發現，而不是寫完 intent 的當下。之後想改回寫完就檢查，就得讓 loom-design 重新依賴 loom-code。
- **needs-design 寫錯時怎麼修** — 在 write-plan 用一個新 commit 改那一行、並把改後的那行原文寫進 commit 說明，不回頭改舊 commit。
- **原則文件是否已批准，capture-intent 自己看** — 看有沒有「批准人與日期」那一行、以及至少三條不可妥協原則，和檢查程式用的是同一個定義；不另寫腳本。
- **範本一致性用一支測試守，不寫同步腳本** — 測試失敗時會點名哪一份要複製過去。
- **session 分析不再自己讀目標 skill 的檔案** — 改由執行它的 agent 從已載入的 skill 取得內容；如果那個 skill 沒被載入，就略過它的紀錄並在摘要裡列出。
- **版號** — loom-code 與 loom-design 升次版號（步驟說明有改），loom-workflow 升修訂版號（只改工具）。
- 沒有被駁回的重要審查意見。

## 我不確定你要不要的

- 專案首頁的 README 仍寫著 loom-design「會讀 loom-code 的 contract package」，Antigravity 安裝段也說另外兩個 plugin「用它的 contract package 和 checker」。這次改完後這兩句都不成立了，要不要一起改掉？
- decision map 開新交付時產生的 intent 骨架是自己寫在程式裡的，不是 loom-code 範本的複本，所以不在第 2 條的一致性測試保護範圍內；loom-code 的 intent 範本以後若加欄位，這份骨架不會跟著提醒。這樣可以嗎？
