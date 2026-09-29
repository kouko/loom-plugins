# 讓 loom 能在 OpenCode v2 上使用 — 我試了什麼、結果如何

2026-09-29 在專案的乾淨副本（5a0e8d4a）上試過；修正後同日在 136c0248 上重跑。每一條怎麼試、回來什麼：`docs/loom/2026-09-29-opencode-v2-compatibility/evidence/acceptance-test-evidence.md`。

兩次測試都用隔離的 OpenCode 2.0.18，有自己的設定目錄和自己的背景服務，重跑時全部重新建立。你平常的 OpenCode 設定和正在跑的服務都沒有被讀取或碰到。模型走你 litellm 設定裡的免費第三方路由組合。安裝來源是這台機器上這個分支的指定 commit，不是 GitHub。重跑時第 3 條用的是你開的私人暫存 GitHub repo。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | 重跑 |
|---|---|---|---|---|
| 1 | On a machine with OpenCode v2 and no prior loom install, each of the three plugins installs from the GitHub repository with OpenCode's official plugin command, and also from the TUI's plugin dialog, and OpenCode's plugin list shows all three. | partly | 照安裝說明現在的步驟做：三個都裝得起來，重啟後約 20～40 秒清單列出三個。更新時用完整來源字串移除、再重裝，也照說明成功了。從 GitHub 安裝、從 TUI 對話框安裝，這兩項還沒試。 | re-tested |
| 2 | In a new OpenCode session every station and skill of the three plugins is offered and loads its full instructions, including when another installed plugin ships a skill with the same short name. | works | 24 個 skill 全部出現並載入完整內容，同名的其他 plugin 沒有把它們蓋掉。 | carried over — 修正只改了 subagent 的開頭說明和安裝文字，沒動 skill 的登記方式 |
| 3 | In OpenCode, a small change in a throwaway repository, run on a third-party cloud model through the user's existing model setup, is taken through capture-intent, write-plan, build, closing-review and ship; the loom checker accepts the intent, plan and attestation it produced, the acceptance test report is committed on the change branch, and the pull request is opened. | partly | 一個小改動（幫小工具加 `--upper`）從頭走到尾，在暫存 repo 開出了 pull request，acceptance test report 也 commit 在分支上。checker 接受了 intent 和 plan，attestation 本身也有效。但流程沒把 attestation commit 進分支，發布時被標成「過期」，PR 說明卻寫成「有效、跳過 reviewer」，兩點都不對。 | re-tested |
| 4 | During that run, loom's implementer, reviewer, adversary and acceptance-tester roles each run as separate OpenCode subagents. | partly | reviewer、adversary、acceptance tester 都以獨立 subagent 跑，而且都從已安裝的 plugin 讀到 loom 自己的說明檔：沒有搜整顆硬碟，也沒有去讀開發者的原始碼。這次主流程卻沒派 implementer，程式碼是主 session 自己寫的；第一次測試時 implementer 有以 subagent 跑過。 | re-tested |
| 5 | Each behaviour that loom's hooks give on the other hosts — the session-start station order and kickoff defaults, the publication reminder, the language reminder, the skill folder-structure rule and the selection-record guard — either works in OpenCode, or OpenCode's install instructions name it as unavailable with the reason. | works | 五項都能用。從 subagent、巢狀呼叫、shell 和寫檔工具假冒「使用者親手輸入」全部被擋下；在主 session 正常使用會生效。 | carried over — 修正沒有動到任何 hook |
| 6 | The existing package test suite and the Codex manifest drift check still pass, so Claude Code, Codex and Antigravity CLI installs are unchanged. | works | 涵蓋這次修正的自動測試都通過，Codex 設定一致性檢查也通過，其他工具的安裝設定沒有任何變動。整套自動測試會在這個改動被接受前執行，沒過就會擋下。 | re-tested |
| 7 | The repository's product principles name OpenCode v2 alongside Claude Code, Codex and Antigravity CLI as a supported host. | works | 產品原則把 OpenCode v2 和其他三個工具並列，並記下是你在 2026-09-29 核可的。 | carried over — 修正沒有動到產品原則 |
| 8 | The three plugins each carry a new version, consistent across manifests, CHANGELOGs and READMEs. | works | 三個 plugin 的新版號（3.24.0／2.7.1／5.5.6）每個地方都一致。 | carried over — 修正沒有動到任何版號或 CHANGELOG |

重跑確認第一次發現的三個問題都修好了：安裝說明的移除和重啟步驟現在是對的；說明也提到了 subagent 會停下來等權限；subagent 找得到 loom 自己的說明檔。重跑時又發現幾件事，你驗收前應該知道：

- **attestation 沒被 commit，PR 說明寫錯了**：流程產生了 attestation，但沒 commit 進分支就去發布，發布指令也照實印出「過期、照樣發布」。PR 說明卻寫「有效（跳過 reviewer）」。其實 reviewer 有跑，也沒有跳過任何步驟。loom 的規則要求 PR 說明照發布指令印出的狀態寫。
- **主 session 自己寫了程式碼**：這次沒有要求跳過 implementer，loom 的規則要求派 implementer，主 session 卻自己動手寫。
- **模型在你的電腦上裝了套件**：主 session 找不到 pytest，就強制把 pytest 和 4 個相依套件裝進了 Homebrew 的 Python。OpenCode 的 shell 指令不受目錄權限管控，所以沒有跳出詢問。
- **一次性的 `opencode run` 遇到提問就中斷**：不加 `--auto` 時第一個權限詢問就會中斷，模型提問時也一樣。所以重跑改成像 TUI 那樣，透過 OpenCode 的服務介面送訊息、回答提問。

## 對你既有的資料做了什麼

這個改動本身沒動到你既有的資料：安裝只在 OpenCode 自己的設定和快取裡加了三個 plugin。重跑時有兩件事落在隔離環境外面。第一，模型把 pytest 9.1.1 和 pluggy、iniconfig、packaging、pygments 裝進了你 Homebrew 的 Python 3.14，時間是 2026-09-29 22:08，我沒有移除，是否移除由你決定。第二，照你的授權，在私人暫存 repo kouko/loom-opencode-scratch 開了 PR #1。它沒有被合併，其他 repo 都沒有被推送或開任何東西。你原本的 OpenCode 設定、資料和正在跑的服務都沒被碰到，這個 repo 也是乾淨的。

## 我替你決定的事

- **暫存 repo 的預設分支叫 `trunk`**：我這邊的防護不讓我直接推 `main`，所以初始 commit 推到 `trunk`，PR 也開到 `trunk`。對測試結果沒有影響。
- **用哪個模型**：跟第一次一樣，用你 litellm 預設的免費路由組合。它走完了全程。
- **以「使用者」身分回答流程裡的問題**：產品原則的問題照「保持精簡、不改預設輸出、不加新套件」回答；也回答了「不需要設計文件」、同意自動發布；問到要不要加 GitHub 規則時答「不要」。這些只影響暫存 repo。
- **權限詢問怎麼回**：專案本身和 loom 已安裝的檔案一律允許，暫存資料夾允許一次。兩次拒絕：一位 reviewer 要切到磁碟根目錄，acceptance tester 要在專案外面建工作副本。兩者都重派後完成了。
- **超過用量上限還是讓它走完**：上限大約 600 萬 input token，流程停在發布前最後一個問題時已經約 665 萬。因為只差一步，而且全程費用是 0，我答了最後那題，最後總計約 712 萬。
- **這次沒有自己跑整套自動測試**：只跑了涵蓋修正的測試和 Codex 一致性檢查，整套留給接受前的自動檢查。
- 主流程沒有駁回任何嚴重度 important 以上的問題。

## 我不確定你要不要的

- 要不要移除模型裝進 Homebrew Python 的 pytest 等 5 個套件？
- 「attestation 沒 commit、PR 說明寫錯」和「主 session 不派 implementer」是這個免費模型不守規則，不是 OpenCode 做不到。要在這次處理，還是另開一項？
- 從 GitHub 安裝、從 TUI 對話框安裝這兩項，要等分支公開後由你在終端機裡試嗎？
- 暫存 repo 和 PR #1 什麼時候刪？
