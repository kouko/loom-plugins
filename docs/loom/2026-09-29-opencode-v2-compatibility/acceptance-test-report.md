# 讓 loom 能在 OpenCode v2 上使用 — 我試了什麼、結果如何

2026-09-29 在專案的乾淨副本（5a0e8d4a）上試過。每一條怎麼試、回來什麼：`docs/loom/2026-09-29-opencode-v2-compatibility/evidence/acceptance-test-evidence.md`。

這次測試用的是一個隔離的 OpenCode 2.0.18，有自己的設定目錄和自己的背景服務。你平常用的 OpenCode 設定和正在跑的服務都沒有被讀取或碰到。模型走你現有 litellm 設定裡的免費第三方模型。安裝來源是這台機器上這個分支的指定 commit，不是 GitHub。等分支公開成 pull request 之後、你驗收之前，還要從 GitHub 實際再裝一次。

## 你要的東西，一條一條看

| # | 你要的 | 結果 | 發生了什麼 | 重跑 |
|---|---|---|---|---|
| 1 | On a machine with OpenCode v2 and no prior loom install, each of the three plugins installs from the GitHub repository with OpenCode's official plugin command, and also from the TUI's plugin dialog, and OpenCode's plugin list shows all three. | partly | 用官方指令三個 plugin 都裝得起來，但要重啟 OpenCode 之後 plugin 清單才會三個都列出來。從 GitHub 安裝，以及從 TUI 對話框裡點「Install plugin」，都還沒試：前者要等分支公開，後者需要你在真的終端機裡操作。 | — |
| 2 | In a new OpenCode session every station and skill of the three plugins is offered and loads its full instructions, including when another installed plugin ships a skill with the same short name. | works | 24 個 skill 全部出現，每一個都載入完整內容。另外裝了一個故意同名的 plugin 和同名的本機 skill，loom 的內容沒有被蓋掉。 | — |
| 3 | In OpenCode, a small change in a throwaway repository, run on a third-party cloud model through the user's existing model setup, is taken through capture-intent, write-plan, build, closing-review and ship; the loom checker accepts the intent, plan and attestation it produced, the acceptance test report is committed on the change branch, and the pull request is opened. | partly | 一個小改動（幫小工具加 `--version`）在免費第三方模型上走過了 capture-intent、write-plan、build，進到 closing-review，acceptance test report 也 commit 到分支上了。第二位 LLM reviewer 審查到一半，用量超過上限，被我中斷，所以沒有 attestation，也沒走到 ship、沒開 pull request。checker 接受了 intent。 | — |
| 4 | During that run, loom's implementer, reviewer, adversary and acceptance-tester roles each run as separate OpenCode subagents. | works | 四種角色都以各自獨立的 OpenCode subagent 跑過，每個都有自己的 session。 | — |
| 5 | Each behaviour that loom's hooks give on the other hosts — the session-start station order and kickoff defaults, the publication reminder, the language reminder, the skill folder-structure rule and the selection-record guard — either works in OpenCode, or OpenCode's install instructions name it as unavailable with the reason. | works | 五項都能用。我從 subagent 裡、從巢狀的 OpenCode 呼叫、用 shell 和寫檔工具，四種方式假冒「使用者親手輸入」，全部被擋下。在主 session 從指令送出的正常用法則會生效。 | — |
| 6 | The existing package test suite and the Codex manifest drift check still pass, so Claude Code, Codex and Antigravity CLI installs are unchanged. | works | 整套自動測試和 Codex 設定一致性檢查都通過。其他三個工具的安裝設定，除了版本號以外都沒變。 | — |
| 7 | The repository's product principles name OpenCode v2 alongside Claude Code, Codex and Antigravity CLI as a supported host. | works | 產品原則把 OpenCode v2 和其他三個工具並列為支援的工具，也記下是你在 2026-09-29 核可修改的。 | — |
| 8 | The three plugins each carry a new version, consistent across manifests, CHANGELOGs and READMEs. | works | 三個 plugin 都有新版號（3.24.0／2.7.1／5.5.6），每個地方寫的都一致。 | — |

試的過程中另外發現三件事，你驗收前應該知道：

- **更新步驟寫錯了**：安裝說明教你用 plugin 名稱移除 plugin，照做會回「沒有設定這個 plugin」，必須輸入完整的安裝來源字串才移除得掉。說明也沒提到剛裝完要先重啟 OpenCode，清單才會完整。
- **subagent 會停下來等你按允許**：loom 的 subagent 要讀 loom 自己的檔案時，OpenCode 會跳出權限詢問。就算用了自動模式，subagent 還是會卡在那裡等。安裝說明沒提這件事。
- **有些 subagent 找不到 loom 自己的說明檔**：acceptance tester 沒被告知報告範本在哪，自己去搜整顆硬碟，最後讀到暫存資料夾裡一份舊的測試用副本。兩位 LLM reviewer 也找不到審查準則，轉而要求讀開發者電腦上的原始碼，我代你拒絕了。在一般使用者的電腦上，這些角色會拿不到應有的說明。

## 對你既有的資料做了什麼

沒有。安裝本身只在 OpenCode 自己的設定和快取裡加了三個 plugin。這次測試全程在隔離的目錄和拋棄式 repo 裡進行，你原本的 OpenCode 設定、資料和正在跑的服務都沒有被讀取或改動。唯一的例外是中途有一批 hook 檢查誤跑在這個 repo 本身：它做了一次不會真的推送的演練，留下一個多出來的檔案，我已經刪掉，repo 現在是乾淨的。

## 我替你決定的事

- **用哪個模型**：我選了你 litellm 設定裡預設的免費路由組合。換成付費模型要重跑第 3、4 條，才知道結果會不會不同。
- **小改動要不要先寫設計文件**：在第 3 條的流程裡，我以「使用者」身分回答「不用」，自動發布也答應了。這只影響那個拋棄式 repo。
- **權限詢問怎麼回**：流程中的權限詢問由我代答。專案本身和 loom 自己的檔案一律允許；暫存資料夾允許；要讀開發者本機 loom 原始碼的兩次拒絕，因為一般使用者沒有那些檔案。如果那兩次允許了，第二位 LLM reviewer 可能就不會中斷重來。
- **超過用量上限就停**：你給的上限大約是 150 萬 input token，實際停下時已經約 330 萬（回報費用是 0，因為走的是免費路由）。我最後一段只盯進度、沒盯用量，所以超過了才停。這表示第 3 條的後半段（attestation、ship、pull request）沒試到。
- **OpenCode 也被當成「宿主程式」**：這次改動讓 Claude Code 和 Codex 上的防護，也把巢狀呼叫的 `opencode` 當成要擋的對象。這是加強防護，不是退步，但會影響另外兩個工具。
- 主流程沒有駁回任何嚴重度 important 以上的問題。

## 我不確定你要不要的

- 第 3 條要不要用較大的用量上限（或付費模型）再完整跑一次到開 pull request？或者 GitHub 版本公開後再跑？
- 「subagent 找不到 loom 自己的說明檔」要在這次修，還是另開一項？它不只影響 OpenCode，但在 OpenCode 上最明顯。
- 從 TUI 對話框安裝這一條，要不要由你自己在終端機裡試一次？
