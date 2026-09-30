# 讓 loom 能在 OpenCode v2 上使用 — 我試了什麼、結果如何

2026-09-29 在專案的乾淨副本（5a0e8d4a）上試過；修正後同日在 136c0248 上重跑；2026-09-30 安裝說明更正後，在 bbf3738a 上第二次重跑。每一條怎麼試、回來什麼：`docs/loom/2026-09-29-opencode-v2-compatibility/evidence/acceptance-test-evidence.md`。

每次測試都用隔離的 OpenCode，有自己的設定目錄和自己的背景服務，每次重跑都全部重新建立。你平常的 OpenCode 設定和正在跑的服務都沒有被讀取或碰到。前兩次的安裝來源是這台機器上的指定 commit；這次第二次重跑改成照說明從 GitHub 上已公開的分支安裝，用的 OpenCode 已自動更新為 2.0.20，這次沒有用到任何模型。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | 重跑 |
|---|---|---|---|---|
| 1 | On a machine with OpenCode v2 and no prior loom install, each of the three plugins installs from the GitHub repository with OpenCode's official plugin command, and also from the TUI's plugin dialog, and OpenCode's plugin list shows all three. | partly | 照安裝說明，用官方指令從 GitHub 裝三個都成功，重啟後約 10 秒清單列出三個。說明裡的第二種方式（把三個來源寫進設定檔）也成功，約 20 秒後列出三個。TUI 對話框安裝做不到：OpenCode 的 TUI 沒有安裝 plugin 的入口，官方文件也沒有，說明已改成照實寫出。你已決定接受這個限制，但驗收條文仍寫著「也能從 TUI 對話框安裝」，所以這條只算部分達成。 | re-tested |
| 2 | In a new OpenCode session every station and skill of the three plugins is offered and loads its full instructions, including when another installed plugin ships a skill with the same short name. | works | 24 個 skill 全部出現並載入完整內容，同名的其他 plugin 沒有把它們蓋掉。 | carried over — 這次修正只改了安裝說明的文字、一支檢查說明的測試和設計文件的一行，程式完全沒動 |
| 3 | In OpenCode, a small change in a throwaway repository, run on a third-party cloud model through the user's existing model setup, is taken through capture-intent, write-plan, build, closing-review and ship; the loom checker accepts the intent, plan and attestation it produced, the acceptance test report is committed on the change branch, and the pull request is opened. | partly | 一個小改動（幫小工具加 `--upper`）從頭走到尾，在暫存 repo 開出了 pull request，acceptance test report 也 commit 在分支上。checker 接受了 intent 和 plan，attestation 本身也有效。但流程沒把 attestation commit 進分支，發布時被標成「過期」，PR 說明卻寫成「有效、跳過 reviewer」，兩點都不對。 | carried over — 這次修正沒有動到任何流程說明或程式，只改安裝說明 |
| 4 | During that run, loom's implementer, reviewer, adversary and acceptance-tester roles each run as separate OpenCode subagents. | partly | reviewer、adversary、acceptance tester 都以獨立 subagent 跑，而且都從已安裝的 plugin 讀到 loom 自己的說明檔：沒有搜整顆硬碟，也沒有去讀開發者的原始碼。這次主流程卻沒派 implementer，程式碼是主 session 自己寫的；第一次測試時 implementer 有以 subagent 跑過。 | carried over — 這次修正沒有動到 subagent 的登記或說明 |
| 5 | Each behaviour that loom's hooks give on the other hosts — the session-start station order and kickoff defaults, the publication reminder, the language reminder, the skill folder-structure rule and the selection-record guard — either works in OpenCode, or OpenCode's install instructions name it as unavailable with the reason. | works | 五項都能用。從 subagent、巢狀呼叫、shell 和寫檔工具假冒「使用者親手輸入」全部被擋下；在主 session 正常使用會生效。 | carried over — 這次修正沒有動到任何 hook，也沒改說明裡列出「不可用」的那一段 |
| 6 | The existing package test suite and the Codex manifest drift check still pass, so Claude Code, Codex and Antigravity CLI installs are unchanged. | works | 這次新增的說明檢查和同一檔裡的其他檢查都通過，Codex 設定一致性檢查也通過，其他工具的安裝設定沒有任何變動。整套自動測試會在這個改動被接受前執行，沒過就會擋下。 | re-tested |
| 7 | The repository's product principles name OpenCode v2 alongside Claude Code, Codex and Antigravity CLI as a supported host. | works | 產品原則把 OpenCode v2 和其他三個工具並列，並記下是你在 2026-09-29 核可的。 | carried over — 這次修正沒有動到產品原則 |
| 8 | The three plugins each carry a new version, consistent across manifests, CHANGELOGs and READMEs. | works | 三個 plugin 的新版號（3.24.0／2.7.1／5.5.6）每個地方都一致。 | carried over — 這次修正沒有動到任何版號或 CHANGELOG |

這次第二次重跑，你驗收前應該知道：

- **GitHub 上的分支還是舊的**：GitHub 上的分支停在安裝說明更正之前的那個 commit，這次更正還沒推上去。所以這次從 GitHub 裝到的是更正前的版本。程式和更正後完全相同，安裝結果不受影響，但 GitHub 上看到的安裝說明還寫著舊的 TUI 步驟，要推上去才會更新。
- **OpenCode 已經自動更新到 2.0.20**：說明寫「在 2.0.18 驗證過」，這次實際跑的是 2.0.20，安裝結果一樣。2.0.20 的程式裡其實留有「在 plugin 對話框裡安裝」的按鍵設定名稱，但 TUI 裡叫不出來：對話框底部只有「檢查更新」，命令面板搜「install」沒有結果，按 shift+I 只是把「I」打進搜尋框，自己綁一個按鍵也沒有反應。之後的版本可能會把它打開，到時說明就要再改。
- **說明沒講設定檔在哪**：第二種方式寫「把同一個來源加進設定檔的 plugins 清單」，但沒說是哪個位置的設定檔。第一種方式的指令會自動寫進使用者的全域設定檔，照著那個位置寫就能用。
- **前一次重跑留下的測試用背景服務還開著**：前一次紀錄寫「已停止」，但它其實一直在跑（那是我自己的隔離服務，不是你的）。這次已經用它自己的隔離設定把它停掉了。

## 對你既有的資料做了什麼

這個改動本身沒動到你既有的資料：安裝只在 OpenCode 自己的設定和快取裡加了三個 plugin。前一次重跑有兩件事落在隔離環境外面。第一，模型把 pytest 9.1.1 和 pluggy、iniconfig、packaging、pygments 裝進了你 Homebrew 的 Python 3.14，時間是 2026-09-29 22:08，我沒有移除，是否移除由你決定。第二，照你的授權，在私人暫存 repo kouko/loom-opencode-scratch 開了 PR #1。它沒有被合併，其他 repo 都沒有被推送或開任何東西。這次第二次重跑只從 GitHub 讀取、沒有推送，也沒有呼叫任何模型。你原本的 OpenCode 設定、資料和正在跑的服務都沒被碰到，這個 repo 也是乾淨的。

## 我替你決定的事

- **這次只重測第 1 條（和第 6 條涵蓋修正的檢查）**：修正只改了安裝說明的文字、新增一支檢查說明的測試、改了設計文件的一行。第 6 條會受新測試影響，所以也重跑了涵蓋它的檢查；其他各條的理由寫在表格裡。
- **設定檔那一種方式寫在哪個檔**：說明沒講位置，我寫進隔離環境的全域設定檔，也就是指令方式自己會寫入的同一個檔。
- **試 TUI 時用了隔離環境**：在隔離的 OpenCode 裡開 TUI，只開對話框和命令面板，沒有送出任何訊息，所以沒有用到模型。
- **停掉前一次留下的隔離服務**：它是我前一次測試自己開的，不是你的；你自己的服務沒被碰。
- **暫存 repo 的預設分支叫 `trunk`**（前一次重跑）：我這邊的防護不讓我直接推 `main`，所以初始 commit 推到 `trunk`，PR 也開到 `trunk`。對測試結果沒有影響。
- **用哪個模型**（前一次重跑）：用你 litellm 預設的免費路由組合，走完了全程。
- **以「使用者」身分回答流程裡的問題**（前一次重跑）：產品原則的問題照「保持精簡、不改預設輸出、不加新套件」回答；也回答了「不需要設計文件」、同意自動發布；問到要不要加 GitHub 規則時答「不要」。這些只影響暫存 repo。
- **權限詢問怎麼回**（前一次重跑）：專案本身和 loom 已安裝的檔案一律允許，暫存資料夾允許一次。兩次拒絕：一位 reviewer 要切到磁碟根目錄，acceptance tester 要在專案外面建工作副本。兩者都重派後完成了。
- **超過用量上限還是讓它走完**（前一次重跑）：上限大約 600 萬 input token，流程停在發布前最後一個問題時已經約 665 萬。因為只差一步，而且全程費用是 0，我答了最後那題，最後總計約 712 萬。
- **沒有自己跑整套自動測試**：只跑了涵蓋修正的測試和 Codex 一致性檢查，整套留給接受前的自動檢查。
- 主流程沒有駁回任何嚴重度 important 以上的問題。

## 我不確定你要不要的

- 驗收第 1 條仍寫「也能從 TUI 對話框安裝」。你已決定接受這個限制；要不要把條文改成符合現況（指令或設定檔），讓這條能算「達成」？
- 更正後的安裝說明要推上 GitHub，大家看到的才是新說明。要在這次一起推嗎？
- 說明要不要補一句設定檔在哪裡，以及「在 2.0.18 驗證過」要不要改成 2.0.20？
- 要不要移除模型裝進 Homebrew Python 的 pytest 等 5 個套件？
- 「attestation 沒 commit、PR 說明寫錯」和「主 session 不派 implementer」是這個免費模型不守規則，不是 OpenCode 做不到。要在這次處理，還是另開一項？
- 暫存 repo 和 PR #1 什麼時候刪？
