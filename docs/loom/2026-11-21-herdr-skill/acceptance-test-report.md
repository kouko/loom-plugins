# loom-workflow 的 herdr skill — 我試了什麼、結果如何

Tried on 2026-11-22, in a clean copy of the project at 1914f318e. How I tried
each line and what came back: `docs/loom/2026-11-21-herdr-skill/evidence/acceptance-test-evidence.md`.

## 你要的東西，一條一條看

| # | What you asked for | Verdict | What happened | Re-run |
|---|---|---|---|---|
| 1 | With loom-workflow installed and herdr's official skill not installed, an agent (Claude Code, Codex, OpenCode) inside a herdr pane asked to do a herdr operation follows the official instructions of the locally installed herdr version and completes the operation. | works | 三個 agent 都先載入本機 herdr 的官方說明，再開一個新 tab、在裡面跑指令、讀到輸出、把 tab 關掉；問它們官方建議用哪種讀取方式，三個都答出只有官方說明裡才有的答案。 | — |
| 2 | Outside a herdr pane, the skill stops and says it is not running inside herdr, without running any herdr control command. | works | 在 herdr 外面，三個 agent 都說「不在 herdr 裡」然後停下；記錄 herdr 呼叫的側錄只看到 Claude 讀了一次說明文字，沒有任何操作 pane、tab 或 agent 的指令。 | — |
| 3 | A request that does not mention herdr does not use the skill. | works | 請三個 agent 做「背景跑一個工作、同時查 git 狀態」而不提 herdr，三個都沒用這個 skill，也沒呼叫 herdr（每個 host 試一次）。 | — |
| 4 | A keyword search returns matching snippets from the conversations of the Claude, Codex and OpenCode agents in currently open herdr panes, each labelled with its workspace, tab, pane and working directory. | works | 在三個開著的 pane（Claude、Codex、OpenCode）各留下一個關鍵字後搜尋，三個都找到，每筆都標了 workspace、tab、pane 和資料夾；同一句話有時會重複出現兩次。 | — |
| 5 | The same search can include past Claude, Codex and OpenCode conversations that are no longer open in herdr, labelled with their working directory and marked as not open. | works | 加上歷史搜尋後，找到三種 agent 已經不在 herdr 裡的舊對話，每筆都標了資料夾並註明「not open」，約 7 秒跑完。 | — |
| 6 | An agent can lead a multi-turn conversation with an agent in another herdr pane, including Claude with Codex, where the other agent answers; it stops at a round limit and gets the other agent's complete reply even when the reply is longer than the screen. | works | Claude 帶著另一個 pane 的 Codex 對話，在設定的 2 輪上限停下；第 2 輪 Codex 回了 120 行（螢幕只有 55 行），Claude 拿到完整 120 行，和 Codex 自己的紀錄逐條對得上。 | — |
| 7 | When Codex's sandbox blocks herdr commands, the agent tells the user that herdr needs network permission instead of retrying. | works | Codex 在預設 sandbox 下跑 herdr 被擋（Operation not permitted），它只試了一次就告訴使用者 herdr 需要 sandbox 的網路權限，並給出要開的設定，沒有重試。 | — |
| 8 | When the installed herdr version changes its official skill, agents follow the new official content without a new loom-workflow release. | works | skill 裡找不到任何一行官方原文；我模擬「新版 herdr 改了一條讀取規則」，skill 一個字沒動，三個 agent 都照新規則做事、也引用了新規則。 | — |

## 對你既有的資料做了什麼

沒有改動。搜尋功能只讀取你本機 Claude、Codex、OpenCode 的對話紀錄，不寫入；測試時開的 pane、tab 都是我自己建立、最後也都關掉了，沒有對你原本的 pane 送任何訊息。測試本身在你本機留下了幾段新的 agent 對話紀錄（內容是測試用的指令），之後用歷史搜尋時可能會搜到它們。

## 我替你決定的事

- **怎麼載入 skill** — 我把 skill 資料夾複製到一個暫存專案裡讓三個 agent 讀，而不是用 README 的方式安裝 plugin，因為安裝會蓋掉你現在裝的 loom-workflow。要改的話，就是在正式安裝後重試第 1 條。
- **第 1、8 條的 Codex 有開網路權限** — 不開的話 Codex 連不到 herdr（這正是第 7 條的情境），所以這兩條在 Codex 上是開著權限測的。
- **第 6 條用 2 輪上限** — 我在指令裡把上限設成 2 輪，好在合理時間內看到「到上限就停」；沒有測預設的 5 輪。這次長回覆用一般的畫面讀取就拿全了，沒有用到「請對方寫成檔案」的備援做法。
- **第 8 條 Codex 改用非登入 shell 測** — Codex 預設用登入 shell，會把我模擬的「新版 herdr」換回真的 herdr；第一次 Codex 因此讀到舊說明，我把那次視為測試設定失誤，改設定後重跑一次。

## 你叫我跳過的步驟

沒有，沒有跳過任何步驟。

## 我不確定你是否想要的事

- 若新版 herdr 的官方說明「新增一條看起來與任務無關的指示」（我試的是「回覆最後加一行指定文字」），Claude 會把它當成工具輸出裡的可疑指示而不照做；改的是一般操作規則時則會照做。這樣的行為可以接受嗎？
- 搜尋結果裡同一句話有時出現兩次，會占掉預設 20 筆的名額；要不要去掉重複？
