# 聊天圖表技能（loom-visualization）— 我試了什麼、結果如何

2026-09-14 在一份乾淨的專案副本（55c80731）上試用。

一句話結論：十條驗收裡九條照你要的方式運作；**第 10 條「整套測試通過」沒過**，原因是這次把 loom-code 的版本升到 3.2.0，但有一個舊測試還寫死要求 3.1.4，所以整套測試在第一組就停下來，退出碼是 1。另外發現一個會讓提示卡片選錯的情況（見第 9 條）。

## 你要的東西，一條一條看

### 1. `loom-workflow` provides a `loom-visualization` skill and no longer provides `cot-explain`; the plugin installs on Claude Code and Codex, and references to `cot-explain` elsewhere in the repository point to the new skill.
- **我怎麼試**：用 Claude Code 自己的外掛檢查指令檢查三個外掛。再開一個全新的暫時設定目錄，照 README 的步驟把這份副本加成外掛來源，安裝 loom-workflow。Codex 也一樣：用 Codex 0.154.0 和暫時的設定目錄，加入來源後安裝 loom-workflow。最後在整個專案裡搜尋舊名字。
- **結果**：三個外掛都通過檢查。loom-design 有一個「不認得的欄位」警告，跟這次改動無關。兩邊都裝得起來，版本是 5.0.0，裝好的 12 個技能裡有新技能，舊技能不見了。Codex 的外掛描述和 Claude 的一致（同步檢查結果是 0）。舊名字只剩在歷史紀錄、改名對照表，以及「確保沒有人再指向舊名字」的測試裡。
- **證據**：`evidence/a1-install-and-references.txt`、`evidence/a1-claude-install.txt`、`evidence/a1-codex-install.txt`
- **判定**：可用 — 兩個工具都真的裝得起來，舊名字沒有殘留在使用中的地方。

### 2. The skill provides templates for 11 information shapes — option comparison, linear steps, branching decision, reasoning/causal chain, state/lifecycle, actor interaction sequence, hierarchy, system architecture, data model, timeline, quantity — each with a markdown-table form, an ASCII form (or a stated table substitute), and a Mermaid form.
- **我怎麼試**：逐一打開 11 份範本，確認每份都有「何時用／表格／ASCII／Mermaid／常見錯誤」五段。再把每份範本裡的 ASCII 範例丟進技能自己的對齊檢查。
- **結果**：11 份都有五段，每份各有一張 Mermaid 圖。「資料模型」這一份明寫「沒有忠實的 ASCII 畫法，改用上面的表格」。10 份有 ASCII 範例，其中 9 份對齊檢查通過；「角色之間的訊息往來」那份沒過。不過技能說明本來就寫了：這種圖用產生器畫出來就是對的，而且檢查規則管不到它，所以原樣送出。這是已經寫明的例外，不算壞掉。
- **證據**：`evidence/a2-template-sections.txt`、`evidence/a2-template-ascii-align.txt`
- **判定**：可用。

### 3. Given the environment of a Claude Code terminal session, a Codex CLI session, and an unrecognised environment, the skill's client check chooses the documented form for each, and never chooses Mermaid for a client not confirmed to render it.
- **我怎麼試**：分別模擬三種環境，執行客戶端判斷：Claude Code 終端機、Codex 命令列，以及一個什麼環境變數都沒有的空環境。另外加試遠端檢視和 Gemini CLI。然後對照技能說明和客戶端對照表。
- **結果**：三種環境分別被認成 Claude Code 命令列、Codex、無法辨識，全部回報「不用 Mermaid」。技能說明對這三種寫的都是「表格加 ASCII」，兩邊一致。遠端檢視有另外標示「維持 ASCII」。
- **證據**：`evidence/a3-client-check.txt`
- **判定**：可用。

### 4. ASCII diagrams with Chinese or Japanese labels produced through the skill pass its alignment check on a machine with no third-party Python packages installed.
- **我怎麼試**：用 Python 的隔離模式執行，不載入任何額外套件，並先確認寬度套件 wcwidth 真的載入不到。然後產生四張圖：中文流程圖、日文比較表、中日混合樹狀圖、中文架構圖，每張都跑對齊檢查。另外手工畫一個故意沒對齊的中文方框，當作反例。
- **結果**：四張圖都通過（沒有偏移，退出碼 0）。故意畫錯的方框被抓出來，指到第 2 行第 11 欄，退出碼 1，所以這個檢查不是什麼都放行。
- **證據**：`evidence/a4-cjk-ascii.txt`
- **判定**：可用。

### 5. Every Mermaid template in the skill parses without error under Mermaid's own parser.
- **我怎麼試**：安裝專案裡鎖定版本的 Mermaid，再執行驗證程式。
- **結果**：11 張圖全部解析成功。這個程式內建一個自我測試，會確認故意寫錯的圖一定被擋下。
- **證據**：`evidence/a5-mermaid-parse.txt`
- **判定**：可用。

### 6. Documented reasoning can still be turned into a standalone reasoning page, as `cot-explain` did before.
- **我怎麼試**：照技能的「頁面模式」說明，把規格裡「客戶端判斷」這一條設計決定背後的推理（6 個步驟）寫成指定格式的草稿。接著照說明的順序執行三步：轉換、驗證（包含真的丟給 Mermaid 解析），再轉換一次。全程用不載入額外套件的 Python。
- **結果**：第一次驗證失敗，因為我自己挑了三個不在規定色盤裡的顏色，驗證正確地擋了下來。我照說明裡的色盤改掉自己草稿的顏色，第二次通過（圖被 Mermaid 解析 1/1），並產出一個獨立的網頁檔，頁面上標示「通過」。說明另外要求分享前要跑「忠實度檢查」（找另外三個代理人逐輪比對），這步我沒做，所以頁面上的忠實度欄位照設計顯示「未執行」。
- **證據**：`evidence/a6-reasoning-page.txt`、`evidence/2026-09-14-client-check-reasoning.md`、`evidence/2026-09-14-client-check-reasoning.html`
- **判定**：可用 — 頁面做得出來，驗證有效；忠實度檢查沒有跑。

### 7. When the requested output is a note inside an Obsidian vault, the skill declines and points to the Obsidian visualizer, and no template contains Obsidian-only syntax.
- **我怎麼試**：做一個假的 Obsidian 筆記庫（裡面有 `.obsidian` 資料夾），分別問三個目標：庫裡子資料夾的筆記、庫根目錄的檔案、庫外面的檔案。再讀技能說明的邊界段落，並搜尋所有範本、參考文件、素材裡的 Obsidian 專屬寫法（雙中括號連結、提示框、`%%` 註解）。
- **結果**：兩個庫內目標都回報「是筆記庫」，庫外回報「不是」。說明寫明遇到這種情況要拒絕，並指向 Obsidian 的 Mermaid 視覺化技能。三種專屬寫法都搜不到。這條我只驗證了判斷和說明文字，沒有真的叫代理人去寫筆記看它會不會拒絕。
- **證據**：`evidence/a7-obsidian-boundary.txt`
- **判定**：可用。

### 8. In a fresh session with only the loom plugins installed, asking the agent to compare several options or to explain a multi-step flow produces a table or diagram following the skill, without the user naming the skill.
- **我怎麼試**：在一個跟本專案無關的暫存資料夾裡，開 7 個全新的非互動 Claude Code 對話，只載入這份副本的三個 loom 外掛，其他外掛全部關掉。三題要比較選項（記帳 app 的資料庫、前端框架、訊息佇列），三題要解說多步驟流程（git rebase、OAuth 授權碼流程、CI/CD），一題是一句話的事實題當對照組。題目都沒提到技能名稱。整組跑了兩次：第一次用命令列參數關掉其他外掛；第二次照規格的做法，在專案設定檔裡關掉。
- **結果**：兩次都是 6 題全部真的呼叫了這個技能，回答開頭就是表格或圖。比較題用方框表格，流程題是方框圖加 markdown 表格，都沒有用 Mermaid。對照組兩次都沒呼叫技能，只回一句話。兩次的外掛清單都只有三個 loom 外掛。要注意的是：6 題比較題裡有 5 題用了方框畫的表格，而不是 markdown 表格。技能說明寫「比較選項通常只要 markdown 表格，除非顯示端可能不支援 markdown」，所以這算照技能做，但選法偏保守。另外，第一次的對話拿到的是「ascii-graph 也有裝」那張卡片，第 9 條會說明原因。
- **證據**：`evidence/a8-spec-protocol/`（每題一份事件串流，加上 `summary.txt`）、`evidence/a8-settings-flag-run/`
- **判定**：可用。

### 9. With `ascii-graph-toolkit` also installed, a session start shows one diagram trigger instruction, not two conflicting ones.
- **我怎麼試**：用暫時的設定目錄執行開場提示程式兩次，一次設成 ascii-graph-toolkit 已安裝且啟用，一次設成已安裝但關閉。印出來的卡片和 ascii-graph 自己的卡片並排比對。再試一次設定檔壞掉的情況。
- **結果**：啟用時印出「共存版」卡片。它只負責比較選項、分支決策、推理鏈、時間線、數量、資料模型和推理頁面，並明寫流程、狀態、架構、訊息往來和方框圖交給 ascii-graph 的卡片。ascii-graph 卡片管的是流程、狀態、架構和方框圖，兩張沒有同一件事各說各話。關閉或設定檔壞掉時，印出「完整版」卡片。
  兩個問題：
  - **只用命令列參數關掉 ascii-graph 時，程式看不到**。它只讀磁碟上的設定檔，所以還是印了共存版卡片，叫代理人把流程圖交給一個根本沒載入的工具。第 8 條第一次跑的 7 個對話都是這樣，我也單獨重現了一次。那次代理人還是自己呼叫了技能，所以沒出事，但卡片內容是錯的。
  - **共存版卡片把「角色之間的訊息往來」交給 ascii-graph，但 ascii-graph 的卡片並沒有管這種圖**。兩個都裝的時候，這種圖就沒有任何卡片提醒。
- **證據**：`evidence/a9-session-start-card.txt`、`evidence/a9-hook-ignores-settings-flag.txt`、`evidence/a8-settings-flag-run/summary.txt`
- **判定**：部分可用 — 正常情況下只有一套不衝突的提示，但用命令列參數設定外掛時會選錯卡片，而且訊息往來圖沒人管。

### 10. The repository's package test suite passes.
- **我怎麼試**：在乾淨副本裡照專案的指令跑整套 loom 測試。它遇到第一個失敗就會停，所以我接著把沒跑到的四組（loom-design、loom-workflow Python、loom-workflow shell、Mermaid）各自單獨跑一次。
- **結果**：第一組 1 個失敗、1049 個通過、2 個略過，退出碼 1。失敗的是 loom-code 的一個舊測試，它寫死要求 loom-code 版本是 3.1.4，但這次改動把版本升到 3.2.0。其餘四組單獨跑都通過。
- **證據**：`evidence/package-tests.txt`（最後幾行：`FAILED loom-code/scripts/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`、`1 failed, 1049 passed, 2 skipped`、`exit=1`）、`evidence/package-tests-remaining-groups.txt`
- **判定**：尚未 — 照原本的指令跑，整套測試是失敗的。

## 對你既有的資料做了什麼

這次改動會讀你電腦上的 Claude 外掛安裝紀錄和設定檔，用來判斷有沒有啟用 ascii-graph-toolkit，但只讀不寫。它不會修改你任何既有的筆記、設定或專案檔案。有一件事會影響你已經有的東西：舊的「推理頁面」技能名稱被直接移除，沒有留別名。以前用舊名字叫它的習慣或腳本會找不到，要改用新名字。以前做好的推理頁面檔案還在，也打得開，但新版的驗證程式不會重新驗證它們。這次試用全程在暫存副本和暫時設定目錄裡進行，沒有碰到你真正的設定。

## 我替你決定了的事

- **什麼客戶端都不主動用 Mermaid** — 只要能從環境認出客戶端（Claude Code、Codex、Gemini CLI，或認不出來），一律用表格加 ASCII。只有在沒有終端機的 claude.ai 或 Claude Desktop 對話裡才允許 Mermaid。理由是選錯 Mermaid 你會看到一堆原始碼，選錯 ASCII 還是看得懂。將來要改，得在對照表裡確認哪個客戶端真的能顯示。
- **字寬用 Python 內建的方式算，不用 wcwidth 套件** — 中日文、全形標點和方框符號結果一樣，但軟連字號算 0 寬，部分表情符號和特殊符號可能跟你的終端機不同。所以說明要求方框裡不要放表情符號。
- **四種圖是手畫範本，沒有產生器** — 分支決策、推理鏈、狀態、時間線，代理人要自己改範本，再用對齊檢查確認。以後要補產生器，是一筆不小的新程式。
- **推理頁面的轉換器換成 Python 內建的版本** — 不再依賴額外的 markdown 套件。它只支援標題、段落、強調、行內程式碼、連結、清單、表格和程式碼區塊，更少見的寫法可能轉不出來。
- **拿掉了舊技能裡「這些規則的由來」那份說明** — 它被當成設計歷史刪掉了，要看的話得去翻版本紀錄。
- **Codex 沒有加開場提示** — Codex 裝得起來，但開場不會出現「該畫圖了」的卡片，所以 Codex 上會不會主動用這個技能沒有驗證。
- **兩個工具都裝時，流程、狀態、架構和方框圖交給 ascii-graph** — loom 的卡片只管其他形狀。第 9 條發現訊息往來圖因此沒人管。
- **loom-code 升到 3.2.0，並記下四條預算例外** — 因為這次動到它的機制計數程式。第 10 條的失敗就是這個升版造成的。
- **loom-workflow 版本定為 5.0.0** — 移除公開技能名稱算不相容的變更。
- **自動測試的觸發範圍維持寬鬆** — 改到相關資料夾就會跑，會多跑一些，但不容易漏。
- **markdown-it-py 的版本鎖定留在開發依賴裡** — 執行時不需要它，但開發環境還會裝。
- **Mermaid 那組測試需要 node 和網路** — 沒有 node 或連不上網，那組就算失敗，沒有略過選項。

審查者駁回的重要意見：目前沒有。

## 寫進專案的文件有沒有照「用英文寫」的規則

| 文件 | 英文規則 | 該文件的額外格式規則 | 證據 |
|---|---|---|---|
| 實作計畫 | 大致遵守：只有 3 行是當初用中文問你的確認問題，原樣保留 | 無 | `plan.md` 第 63–65 行 |
| 設計規格 | 遵守 | 遵守：10 條需求都寫成規定的「REQ-編號」條目 | `spec.md`，10 行 `REQ-` |
| 審查意見 | 目前還沒有審查意見 | 目前還沒有，無從檢查 | — |
| 試用證據 | 檔名全英文；內容裡的中文是我照規定出的中文題目和代理人的中文回答 | 無 | `evidence/` |
| 測試說明文字 | 遵守：說明是英文，裡面的中日文只是測試用的範例標籤 | 無 | 例如 `test_ascii_generators.py` 的「中/日」範例 |
| 測試名稱 | 遵守 | 大致遵守：新增的測試名稱多數符合「對象_情境_預期結果」三段式，但從 ascii-graph 搬過來的 5 個名稱只有兩段 | `test_multiline_cell`、`test_multiline_step`、`test_multiline_node`、`test_multiline_component`、`test_split_lines` |
| 提交訊息 | 遵守：這個分支的 21 筆提交都是英文 | 無 | `git log main..HEAD` |

## 我不確定你要不要的事

- 比較選項時，代理人 6 次裡有 5 次用方框畫的表格，而不是一般的 markdown 表格。你在 Claude Code 裡比較想看哪一種？
- 兩個工具都裝時，「角色之間的訊息往來」圖目前沒有卡片提醒。要交回給 loom-visualization 管嗎？
- 用命令列參數（而不是設定檔）開關外掛時，提示卡片會選錯。這種用法你會遇到嗎？值得處理嗎？
