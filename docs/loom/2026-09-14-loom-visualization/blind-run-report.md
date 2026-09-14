# 聊天圖表技能（loom-visualization）— 我試了什麼、結果如何

第一次試用：2026-09-14，在乾淨的專案副本 55c80731 上。
修正後重試：2026-09-14，在乾淨的專案副本 b3678bfb 上（第 1–6、9 條）。
最終功能版本：2026-09-14，在乾淨的專案副本 76a1b005 上（第 7 條，另外快速重跑第 3 條）。
合併主線之後：2026-09-14，在乾淨的專案副本 2c514285 上（第 1、10 條）。

一句話結論：在最終版本上，十條驗收裡九條照你要的方式運作，整套測試也通過了。第 9 條只算部分可用：兩個工具都裝時，兩張卡片對「中日文方框圖」會各自叫代理人用自己的工具。這一點已經被駁回，留到之後的改動處理（見「我替你決定了的事」）。

第 1、3、6、8 條是在 55c80731 上試的。後來的修正其實有動到其中三條會用到的東西，所以不能說「完全沒碰到」：
- 第 3 條：客戶端判斷程式和客戶端對照表都有改。
- 第 6 條：推理頁面的轉換程式和頁面模式說明都有改。
- 第 8 條：技能主說明有改，比較選項改成「一律用 markdown 表格」。

第 1、3、6 條很快，我在 b3678bfb 上重跑了一次，結果和之前一樣。第 8 條依指示沒有重跑，所以它的結果仍然代表修正前的行為。最後一次修正（76a1b005）只動了 Obsidian 筆記庫的判斷、它的說明和測試，所以第 7 條和整套測試在 76a1b005 上重跑。這次修正也改了客戶端判斷程式，所以第 3 條也快速重跑：三種環境仍然都是「不用 Mermaid」。

## 你要的東西，一條一條看

### 1. `loom-workflow` provides a `loom-visualization` skill and no longer provides `cot-explain`; the plugin installs on Claude Code and Codex, and references to `cot-explain` elsewhere in the repository point to the new skill.
- **我怎麼試**：（55c80731）用 Claude Code 自己的外掛檢查指令檢查三個外掛。再開一個全新的暫時設定目錄，照 README 的步驟把這份副本加成外掛來源，安裝 loom-workflow。Codex 也一樣：用 Codex 0.154.0 和暫時的設定目錄，加入來源後安裝 loom-workflow。最後在整個專案裡搜尋舊名字。（b3678bfb）確認兩邊的外掛設定檔都沒改，再跑一次檢查、Codex 同步檢查和舊名字搜尋。（2c514285，合併主線之後）主線帶來了外掛設定檔裡的網址變更和新版 README，所以再跑一次三個外掛的檢查、Codex 同步檢查、舊名字搜尋，並確認版本號。
- **結果**：三個外掛都通過檢查。loom-design 有一個「不認得的欄位」警告，跟這次改動無關。兩邊都裝得起來，版本是 5.0.0，裝好的 12 個技能裡有新技能，舊技能不見了。Codex 的外掛描述和 Claude 的一致。舊名字只剩在歷史紀錄、改名對照表，以及「確保沒有人再指向舊名字」的測試裡。修正後再查，結果相同。合併主線之後：三個外掛仍然通過檢查（loom-design 同一個無關警告），Codex 同步檢查結果是 0，loom-workflow 是 5.0.0、loom-code 是 3.2.0，技能資料夾仍是 12 個且包含新技能。新版的 4 份 README 都改用新名字，完全沒有舊名字。舊名字只剩在變更紀錄的歷史段落和上述測試裡。
- **證據**：`evidence/a1-install-and-references.txt`、`evidence/a1-claude-install.txt`、`evidence/a1-codex-install.txt`、`evidence/b3678bfb/a1-recheck-b3678bfb.txt`、`evidence/2c514285/a1-recheck-2c514285.txt`
- **判定**：可用 — 兩個工具都真的裝得起來，舊名字沒有殘留在使用中的地方。

### 2. The skill provides templates for 11 information shapes — option comparison, linear steps, branching decision, reasoning/causal chain, state/lifecycle, actor interaction sequence, hierarchy, system architecture, data model, timeline, quantity — each with a markdown-table form, an ASCII form (or a stated table substitute), and a Mermaid form.
- **我怎麼試**：（b3678bfb）逐一打開 11 份範本，確認每份都有「何時用／表格／ASCII／Mermaid／常見錯誤」五段。再把每份範本裡的 ASCII 範例丟進技能自己的對齊檢查。
- **結果**：11 份都有五段，每份各有一張 Mermaid 圖。「選項比較」的 ASCII 段落換了說法：現在寫明 markdown 表格在所有客戶端都是正式形式，只有要放進程式碼區塊或純文字時才用 ASCII 表格。「資料模型」明寫「沒有忠實的 ASCII 畫法，改用表格」。10 份 ASCII 範例裡 9 份通過對齊檢查；「角色之間的訊息往來」那份仍然沒過，但技能說明寫明這種圖用產生器畫出來就是對的，而且檢查規則管不到它，所以原樣送出。這是寫明的例外，跟修正前一樣。
- **證據**：`evidence/b3678bfb/a2-templates-b3678bfb.txt`
- **判定**：可用。

### 3. Given the environment of a Claude Code terminal session, a Codex CLI session, and an unrecognised environment, the skill's client check chooses the documented form for each, and never chooses Mermaid for a client not confirmed to render it.
- **我怎麼試**：分別模擬三種環境，執行客戶端判斷：Claude Code 終端機、Codex 命令列，以及一個什麼環境變數都沒有的空環境。另外加試遠端檢視。然後對照技能說明和客戶端對照表。55c80731 和 b3678bfb 各跑一次。
- **結果**：兩次都一樣：三種環境分別被認成 Claude Code 命令列、Codex、無法辨識，全部回報「不用 Mermaid」，和說明寫的「表格加 ASCII」一致。修正後多了一項「目前資料夾是不是筆記庫」的回報（這裡都是「不是」），對照表也把 Claude Code 各介面能不能顯示表格改標為「未驗證」。這些都不影響選哪種形式。
- **證據**：`evidence/a3-client-check.txt`、`evidence/b3678bfb/a3-client-check-b3678bfb.txt`、`evidence/76a1b005/a3-client-check-76a1b005.txt`（最終版本上三種環境仍然都是「不用 Mermaid」；沒指定目標時，筆記庫欄位回到空值）
- **判定**：可用。

### 4. ASCII diagrams with Chinese or Japanese labels produced through the skill pass its alignment check on a machine with no third-party Python packages installed.
- **我怎麼試**：（b3678bfb）用 Python 的隔離模式執行，並先確認寬度套件 wcwidth 真的載入不到。然後產生四張圖：中文流程圖、日文比較表、中日混合樹狀圖、中文架構圖，每張都跑對齊檢查。另外手工畫一個故意沒對齊的中文方框當反例。最後故意在標籤裡放看不見的控制字元（定位鍵、終端機顏色碼、響鈴字元），再放一個正常的換行當對照。
- **結果**：四張圖都通過（沒有偏移，退出碼 0）。故意畫錯的方框被抓出來（第 2 行第 11 欄，退出碼 1）。三種控制字元都被擋下，退出碼 1，訊息會指出是哪個字元並要你拿掉，例如「contains control character U+0009; remove it」。正常的換行照常畫出來。
- **證據**：`evidence/b3678bfb/a4-cjk-ascii-b3678bfb.txt`
- **判定**：可用。

### 5. Every Mermaid template in the skill parses without error under Mermaid's own parser.
- **我怎麼試**：（b3678bfb）安裝專案鎖定版本的 Mermaid，執行驗證程式。接著用專案的測試指令單獨跑「Mermaid」這一組，確認它現在包含三步：安裝、驗證、反例檢查。
- **結果**：11 張圖全部解析成功。整組一起跑時，反例檢查也確實有執行：故意寫錯的圖讓驗證程式以退出碼 1 失敗，錯誤訊息指到那個檔案的第 3 行。整組退出碼 0。驗證程式現在也認得開頭標記後面多帶文字的 Mermaid 區塊（修正說明是這樣寫的）。範本裡沒有這種區塊，所以這一點我沒有另外試。
- **證據**：`evidence/b3678bfb/a5-mermaid-parse-b3678bfb.txt`
- **判定**：可用。

### 6. Documented reasoning can still be turned into a standalone reasoning page, as `cot-explain` did before.
- **我怎麼試**：（55c80731）照技能的「頁面模式」說明，把規格裡「客戶端判斷」這條設計決定背後的推理（6 個步驟）寫成指定格式的草稿，照順序執行轉換、驗證（包含真的丟給 Mermaid 解析）、再轉換一次，全程不載入額外套件。（b3678bfb）拿同一份草稿，用新版的程式再跑一次這三步。
- **結果**：第一次在 55c80731 上驗證失敗，因為我自己挑了三個不在規定色盤裡的顏色，驗證正確地擋了下來。我改掉草稿顏色後通過，產出一個獨立網頁，頁面上標示「通過」。在 b3678bfb 上用同一份草稿重跑，一樣通過（圖被 Mermaid 解析 1/1）。說明要求分享前要跑「忠實度檢查」（找另外三個代理人逐輪比對），這步兩次都沒做，所以頁面上的忠實度欄位照設計顯示「未執行」。
- **證據**：`evidence/a6-reasoning-page.txt`、`evidence/2026-09-14-client-check-reasoning.md`、`evidence/2026-09-14-client-check-reasoning.html`、`evidence/b3678bfb/a6-reasoning-page-b3678bfb.txt` 和同目錄的頁面檔
- **判定**：可用 — 頁面做得出來，驗證有效；忠實度檢查沒有跑。

### 7. When the requested output is a note inside an Obsidian vault, the skill declines and points to the Obsidian visualizer, and no template contains Obsidian-only syntax.
- **我怎麼試**：（76a1b005）做一個假的 Obsidian 筆記庫（裡面有 `.obsidian` 資料夾）。先指定目標檔案：庫裡子資料夾的筆記、庫根目錄的檔案、庫外面的檔案。再不指定目標，分別站在庫裡和庫外的資料夾執行，模擬「只是在聊天裡回答」。然後讀技能說明的邊界段落，並搜尋所有範本、參考文件、素材裡的 Obsidian 專屬寫法（雙中括號連結、提示框、`%%` 註解）。
- **結果**：兩個庫內目標都回報「是筆記庫」，庫外回報「不是」。不指定目標時，不論站在庫裡還是庫外，都回報「沒有檢查」（空值），不會因為你剛好在筆記庫裡工作就拒絕。說明寫明：只有要寫進筆記庫的檔案、或你明說要一篇筆記庫筆記時才拒絕，並指向 Obsidian 的 Mermaid 視覺化技能；在筆記庫資料夾裡的聊天回答照常進行。三種專屬寫法都搜不到。中間那一版曾改成「沒指定目標就檢查目前資料夾」，兩位審查者認為範圍太寬，已經改回來。這條我只驗證了判斷和說明文字，沒有真的叫代理人去寫筆記看它會不會拒絕。
- **證據**：`evidence/76a1b005/a7-obsidian-boundary-76a1b005.txt`；第一次的結果在 `evidence/a7-obsidian-boundary.txt`
- **判定**：可用。

### 8. In a fresh session with only the loom plugins installed, asking the agent to compare several options or to explain a multi-step flow produces a table or diagram following the skill, without the user naming the skill.
- **我怎麼試**：（55c80731，修正後沒有重跑）在一個跟本專案無關的暫存資料夾裡，開 7 個全新的非互動 Claude Code 對話，只載入這份副本的三個 loom 外掛，其他外掛全部關掉。三題要比較選項（記帳 app 的資料庫、前端框架、訊息佇列），三題要解說多步驟流程（git rebase、OAuth 授權碼流程、CI/CD），一題是一句話的事實題當對照組。題目都沒提到技能名稱。整組跑了兩次：第一次用命令列參數關掉其他外掛；第二次照規格的做法，在專案設定檔裡關掉。
- **結果**：兩次都是 6 題全部真的呼叫了這個技能，回答開頭就是表格或圖。比較題用方框表格，流程題是方框圖加 markdown 表格，都沒有用 Mermaid。對照組兩次都沒呼叫技能，只回一句話。兩次的外掛清單都只有三個 loom 外掛。6 題比較題裡有 5 題用了方框表格，而不是 markdown 表格。當時的說明允許這樣做，但修正後的說明改成「比較選項一律用 markdown 表格」。我沒有重跑，所以不知道代理人現在會不會照新規則做。
- **證據**：`evidence/a8-spec-protocol/`（每題一份事件串流，加上 `summary.txt`）、`evidence/a8-settings-flag-run/`
- **判定**：可用 — 以修正前的版本來說；修正後的比較題形式沒有重新確認。

### 9. With `ascii-graph-toolkit` also installed, a session start shows one diagram trigger instruction, not two conflicting ones.
- **我怎麼試**：（b3678bfb）用暫時的設定目錄執行開場提示程式兩次，一次設成 ascii-graph-toolkit 已安裝且啟用，一次設成已安裝但關閉，另外試一次設定檔壞掉。印出來的卡片和 ascii-graph 自己的卡片並排比對。
- **結果**：啟用時印出新版「共存」卡片。它負責比較選項、分支決策、推理鏈、時間線、角色之間的訊息往來、數量、資料模型和推理頁面。流程、狀態和架構交給 ascii-graph 的卡片。訊息往來現在留在 loom 這邊，修正前「沒人管」的問題解決了。關閉或設定檔壞掉時，印出「完整版」卡片。
  還有一個重疊：新版共存卡片寫著「由 loom-visualization 決定的方框圖，用它自己的對齊檢查來畫」。但 ascii-graph 的卡片寫著「只要方框圖有中日文標籤或三個以上的方框，就先叫 ascii-graph」。所以像「中文標籤的分支決策圖」這種圖，兩張卡片會各自叫代理人用自己的工具，兩個指示互相衝突。
- **證據**：`evidence/b3678bfb/a9-session-start-card-b3678bfb.txt`
- **判定**：部分可用 — 大部分形狀只有一個工具負責，但中日文方框圖兩張卡片都搶。

### 10. The repository's package test suite passes.
- **我怎麼試**：（2c514285，合併主線之後）在乾淨副本裡照專案的指令跑整套 loom 測試。
- **結果**：全部通過，退出碼 0。第一組 1054 個通過、2 個略過，沒有失敗。其餘各組全部通過，包括 Mermaid 那組 11 張圖和反例檢查。最後幾行是「11/11 mermaid blocks parsed」、「PASS — validator exits 1 on the A -> B block」、「PASS — FAIL line names <temp>/bad.md:3」、「exit=0」。第一次試用時那個寫死舊版本號的失敗，已經修好。合併主線沒有讓任何測試變紅。
- **證據**：`evidence/2c514285/package-tests-2c514285.txt`；76a1b005 的結果在 `evidence/76a1b005/package-tests-76a1b005.txt`，b3678bfb 的在 `evidence/b3678bfb/package-tests-b3678bfb.txt`，第一次的失敗紀錄在 `evidence/package-tests.txt`
- **判定**：可用。

## 對你既有的資料做了什麼

這次改動會讀你電腦上的 Claude 外掛安裝紀錄和設定檔，用來判斷有沒有啟用 ascii-graph-toolkit，但只讀不寫。它不會修改你任何既有的筆記、設定或專案檔案。有一件事會影響你已經有的東西：舊的「推理頁面」技能名稱被直接移除，沒有留別名。以前用舊名字叫它的習慣或腳本會找不到，要改用新名字。以前做好的推理頁面檔案還在，也打得開，但新版的驗證程式不會重新驗證它們。修正後的頁面模式說明也不再建議把頁面草稿搬進筆記庫。這次試用全程在暫存副本和暫時設定目錄裡進行，沒有碰到你真正的設定。

## 我替你決定了的事

- **什麼客戶端都不主動用 Mermaid** — 只要能從環境認出客戶端（Claude Code、Codex、Gemini CLI，或認不出來），一律用表格加 ASCII。只有在沒有終端機的 claude.ai 或 Claude Desktop 對話裡才允許 Mermaid。理由是選錯 Mermaid 你會看到一堆原始碼，選錯 ASCII 還是看得懂。將來要改，得在對照表裡確認哪個客戶端真的能顯示。
- **字寬用 Python 內建的方式算，不用 wcwidth 套件** — 中日文、全形標點和方框符號結果一樣，但軟連字號算 0 寬，部分表情符號和特殊符號可能跟你的終端機不同。所以說明要求方框裡不要放表情符號。
- **四種圖是手畫範本，沒有產生器** — 分支決策、推理鏈、狀態、時間線，代理人要自己改範本，再用對齊檢查確認。以後要補產生器，是一筆不小的新程式。
- **推理頁面的轉換器換成 Python 內建的版本** — 不再依賴額外的 markdown 套件。它只支援標題、段落、強調、行內程式碼、連結、清單、表格和程式碼區塊，更少見的寫法可能轉不出來。
- **拿掉了舊技能裡「這些規則的由來」那份說明** — 它被當成設計歷史刪掉了，要看的話得去翻版本紀錄。
- **Codex 沒有加開場提示** — Codex 裝得起來，但開場不會出現「該畫圖了」的卡片，所以 Codex 上會不會主動用這個技能沒有驗證。
- **兩個工具都裝時，流程、狀態和架構交給 ascii-graph** — loom 的卡片管其他形狀，修正後也包括訊息往來。第 9 條發現中日文方框圖仍有重疊。
- **loom-code 升到 3.2.0，並記下四條預算例外** — 因為這次動到它的機制計數程式。
- **loom-workflow 版本定為 5.0.0** — 移除公開技能名稱算不相容的變更。
- **合併主線時，README 用主線的新架構，只套上改名** — 主線同時重寫了 README，和這個分支衝突。這個分支把主線合併進來，保留主線的新 README 結構，只把舊技能名稱換成新名稱，沒有保留分支上原本的 README 寫法。
- **自動測試的觸發範圍維持寬鬆** — 改到相關資料夾就會跑，會多跑一些，但不容易漏。
- **Mermaid 那組測試需要 node 和網路** — 沒有 node 或連不上網，那組就算失敗，沒有略過選項。
- **駁回的重要意見：只用命令列參數關掉 ascii-graph 時，開場提示程式看不到** — 我在第一次試用時提出。統籌者駁回的理由是：開場提示程式拿不到命令列設定的內容，這方面沒有公開文件可依據；一般安裝都是用設定檔開關外掛，而程式會讀設定檔。如果這個理由不成立，代價是：只用命令列關掉 ascii-graph 時，代理人仍可能看到共存卡片，被叫去用一個根本沒載入的工具。
- **駁回的重要意見：兩個工具都裝時，中日文方框圖會收到兩個指示** — 我在修正後重試時提出。loom 的共存卡片說「由 loom-visualization 決定的方框圖，用它自己的對齊檢查來畫」，ascii-graph 的卡片卻說「只要有中日文標籤或三個以上方框，就先叫 ascii-graph」。統籌者在這次改動裡駁回，理由有兩個：審查這一輪已經用完三次內容修改的額度，要修得另開一個新改動；而且不管代理人照哪一個做，畫出來的都是寬度檢查過、對齊的圖，所以後果是重複的指示，不是壞掉的圖。要改的代價是：再開一個後續改動，刪掉那句話，或寫明這種圖歸誰。
- **駁回的審查意見：保留開發依賴裡的 markdown-it-py 版本鎖定** — 理由是有一個專案啟動時的測試，在測試用的版本鎖定檔裡釘住了它。代價是開發環境還會裝這個執行時用不到的套件。
- **駁回的審查意見：推理頁面轉換器裡兩個很長的函式不拆** — 理由是拆開有改變行為的風險。代價是這兩段之後比較難讀、難改。

## 寫進專案的文件有沒有照「用英文寫」的規則

| 文件 | 英文規則 | 該文件的額外格式規則 | 證據 |
|---|---|---|---|
| 實作計畫 | 大致遵守：只有 3 行是當初用中文問你的確認問題，原樣保留 | 無 | `plan.md` 第 63–65 行 |
| 設計規格 | 遵守 | 遵守：10 條需求都寫成規定的「REQ-編號」條目 | `spec.md`，10 行 `REQ-` |
| 審查意見 | 本報告沒有檢查審查紀錄本身 | 本報告沒有檢查 | — |
| 試用證據 | 檔名全英文；內容裡的中文是我照規定出的中文題目和代理人的中文回答 | 無 | `evidence/` |
| 測試說明文字 | 遵守：說明是英文，裡面的中日文只是測試用的範例標籤 | 無 | 例如 `test_ascii_generators.py` 的「中/日」範例 |
| 測試名稱 | 遵守 | 遵守：先前只有兩段的 5 個名稱已改成「對象_情境_預期結果」三段式 | `test_gen_table_multiline_cell_stays_aligned`、`test_gen_flow_multiline_step_grows_box_taller`、`test_gen_tree_multiline_node_keeps_branch_prefixes`、`test_gen_arch_multiline_component_grows_band_taller`、`test_split_lines_plain_label_returns_physical_lines` |
| 提交訊息 | 遵守：第一次試用時分支上的 21 筆提交都是英文；之後的修正提交也是英文 | 無 | `git log main..HEAD` |

## 我不確定你要不要的事

- 比較選項時，第一次試用的代理人 6 次裡有 5 次用方框畫的表格，而不是一般的 markdown 表格。修正後的技能說明已改成「比較選項一律用 markdown 表格」，但我沒有重跑，不知道代理人實際上會不會照做。要不要再跑一次確認？
- 兩個工具都裝時，中日文標籤的方框圖（例如分支決策圖）兩張卡片都會叫代理人用自己的工具。你希望這種圖交給哪一個？
