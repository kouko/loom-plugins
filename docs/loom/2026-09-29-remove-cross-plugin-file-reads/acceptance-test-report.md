# 各 plugin 只用自己的檔案 — 我試了什麼、結果如何

2026-09-29 先在專案的乾淨複本（6e360dd）上試過一次；修正之後，再在新的乾淨複本（95a970b）上重試受修正影響的幾條。每一條怎麼試、回來什麼：`docs/loom/2026-09-29-remove-cross-plugin-file-reads/evidence/acceptance-test-evidence.md`。

## 你要的，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | Re-run |
|---|---|---|---|---|
| 1 | loom-design 與 loom-workflow 執行時會用到的 skill、reference、腳本與 hook 中，沒有任何一處需要讀或執行 loom-code 資料夾裡的檔案；在沒有 loom-code 檔案可讀的環境中照著它們的步驟做，不會因為找不到 loom-code 而停下。 | works | 我只把這兩個 plugin 拿出來放在沒有 loom-code 的地方，重新跑了一次完整的 session 分析：分析步驟只用 skill 名稱指出要改進哪個 skill，不再要人去找它的檔案位置；接著產生改進提案時，三個 session 的建議全部保留下來，合併成一條提案，沒有被丟掉。換成另一個 skill 名稱時則正確地不收進去。 | 重試（修正改了 session 分析的步驟和提案程式） |
| 2 | loom-design 與 loom-workflow 帶的範本複本和 loom-code 的原版內容一致；任一邊改了而另一邊沒改時，測試會失敗。 | works | 我分別只改複本、只改原版、只改寫進說明裡的需求編號格式，三次測試都失敗並點名是哪一份；改回去就通過。loom-workflow 本身沒有帶範本複本，所以這條只落在 loom-design。 | carried over — 修正沒有動到任何範本、範本複本或比對它們的測試 |
| 3 | 在 loom-design 或 loom-workflow 執行時會用到的檔案中加入一個讀取 loom-code 檔案的寫法（包含腳本與 `<loom-code>` 這類路徑寫法）時，自動的邊界檢查會擋下。 | works | 這次針對修正補上的缺口：我在兩個 plugin 的 hook 資料夾裡放了沒有副檔名、用 bash、sh、zsh 開頭的 hook，各自去讀 loom-code 的檔案，邊界檢查每一次都擋下並指出哪一行；拿掉後回到通過。上一輪試過的其他寫法（說明文件、Python、shell、hook 設定檔、`<loom-code>` 寫法）這次修正沒有改到它們的判斷方式。 | 重試（修正改了邊界檢查） |
| 4 | 原本 loom-design 寫完 intent 當下做的每一項 intent 格式檢查（結構、product 問題不得含識別字、needs-design 理由與 commit 一致、needs-design 重新計算），在 loom-code 的 write-plan 開始規劃前都會執行；故意寫錯任一項的 intent 會在 write-plan 被擋下。 | works | write-plan 現在對已確認的 intent 先跑這項檢查、通過才往下規劃；我做了六份各錯一項的 intent，每一份都被擋下並說明錯在哪，一份正確的則通過。 | carried over — 修正沒有動到 write-plan 或 intent 檢查程式 |
| 5 | product 變更遇到 repo 沒有已批准的原則文件時，原則訪談仍在第一次確認 intent 的同一段對話中進行，不會延到後面的站。 | works | capture-intent 仍寫明：沒有已批准的原則文件就在同一段對話裡當場訪談，並和 intent 一起確認。修正後 write-spec 也恢復了原本的保險：遇到 product 變更而原則文件沒批准時，它會停下並交回 capture-intent，不會自己補上批准紀錄，也不會把訪談拖到後面才做；兩邊對「已批准」的定義一字不差。這條我是讀步驟說明確認的，沒有跟真人跑一次完整對話。 | 重試（修正改了 write-spec 的步驟） |
| 6 | 三個 plugin 的版號各自升級，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。 | works | 三個 plugin 分別升到 3.23.0、2.7.0、5.5.5，每個 plugin 的三份 manifest、CHANGELOG、各語言 README 都對得上，這次重跑的版號相關測試也通過；完整自動測試在變更被接受前還會再跑一次、失敗就擋下。 | carried over — 修正改了 README 的說明句，但沒有動任何版號字串；版號測試仍在這次重跑中通過 |

## 對你既有的資料做了什麼

沒有。這次只改了這個 repo 裡 plugin 自己的說明、範本、檢查腳本和測試；我的測試都在暫存的乾淨複本和暫存 repo 裡做，乾淨複本做完已刪掉。

## 我替你決定的

- **write-plan 在哪一步跑 intent 檢查** — 放在「先開分支」之後、決定要不要 spec 之前，因為在主幹上這項檢查會直接拒絕工程類 intent。代價是格式錯誤要到規劃時才被發現，而不是寫完 intent 的當下。之後想改回寫完就檢查，就得讓 loom-design 重新依賴 loom-code。
- **needs-design 寫錯時怎麼修** — 在 write-plan 用一個新 commit 改那一行、並把改後的那行原文寫進 commit 說明，不回頭改舊 commit。
- **原則文件是否已批准，capture-intent 和 write-spec 自己看** — 看有沒有「批准人與日期」那一行、以及至少三條不可妥協原則，和檢查程式用的是同一個定義；不另寫腳本。
- **範本一致性用一支測試守，不寫同步腳本** — 測試失敗時會點名哪一份要複製過去。
- **session 分析只用名稱指出目標 skill** — 分析的 agent 透過工具本身用名稱取得那個 skill 的說明，不去找它的檔案；工具給不出來時，照樣分析那段紀錄，並在摘要裡說明少了 skill 說明，不會丟掉那段紀錄。
- **改進提案用 skill 名稱配對** — 只比對 skill 名稱中 plugin 名稱以外的那段，和目標 skill 所在的資料夾名稱。代價是兩個不同 plugin 若有同名 skill，又在同一次分析裡一起出現，它們的建議可能混進同一份提案；目前的 plugin 沒有同名 skill。
- **版號** — loom-code 與 loom-design 升次版號（步驟說明有改），loom-workflow 升修訂版號（只改工具）。
- 沒有被駁回的重要審查意見。

## 我不確定你要不要的

- 上一輪提出的 README 說法問題已經改好：專案首頁和 loom-code 各語言 README 都改成「兩個 sibling 執行時不讀 contract package，只用名稱把工作交給 loom-code」。
- decision map 開新交付時產生的 intent 骨架是自己寫在程式裡的，不是 loom-code 範本的複本，所以不在第 2 條的一致性測試保護範圍內；loom-code 的 intent 範本以後若加欄位，這份骨架不會跟著提醒。這樣可以嗎？
- 邊界檢查看不到「沒有副檔名、第一行也沒寫用哪個程式執行」的檔案：我放一個這樣的檔案去讀 loom-code，檢查仍說通過。這種檔案只有在 hook 設定裡明寫用 bash 去跑時才會執行，目前沒有這樣的 hook。要不要也把它擋下，還是當作已知限制？
