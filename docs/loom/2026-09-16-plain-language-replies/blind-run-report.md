# 讓 loom 的回覆講白話、照字面講、用表格或圖 — 我試了什麼、結果如何

試跑日期：2026-09-16。第 1–7、9–11 條在一份乾淨的專案複本上試（版本 dda0014f）。第 8 條在之後補上的修正版本上重新檢查（版本 40014ea3）。

第 6、7、9 條的試跑用的是 dda0014f 的內容。到 40014ea3 為止，這些試跑讀到的檔案只多了一段東西：寫作指南的「表格寫作規則」底下，新增「格子裡能放什麼」和「表格裡的時間」兩小節。試跑用到的其他文字都沒有改。

**一句話結論**：每則訊息附帶提醒這件事，在 Claude Code 上確實做到了，出錯時也不會擋住你的訊息。可是 agent 真正照著寫出白話回覆的效果只做到一部分：
- 改寫時仍會掉事實或改事實，有一次還用了比喻。
- 問「要怎麼做」時，只給一個做法。

| 條目 | 結果 |
|---|---|
| 1 每則訊息附帶提醒（Claude Code） | 做到 |
| 2 開場不再另外送；裝了 ascii-graph-toolkit 也只有一份圖表指示 | 做到 |
| 3 Codex CLI | 部分（沒有實際開 Codex 對話） |
| 4 Antigravity CLI | 部分（沒有實際開 agy 對話） |
| 5 提醒出錯時訊息照常送出 | 做到 |
| 6 白話改寫 | 部分 |
| 7 決策問題的問法 | 部分 |
| 8 表格集收錄完整 | 部分（剩三小項沒收） |
| 9 只讀需要的表格集 | 做到 |
| 10 安裝說明寫清楚收不到的地方 | 做到 |
| 11 測試與機制檢查 | 做到 |

## 審查摘要

- 還沒有審查者看過這個版本，所以沒有被駁回的審查意見。
- 在我的乾淨複本上，整套測試都通過：3,097 項通過、11 項略過、0 項失敗，另外幾組檢查腳本也全部通過。
- 檢查規則的數量和改動前一樣，沒有變多。
- 建置階段有另一個 agent 專門試著弄壞這個改動，寫了攻擊測試。在我這次的整套測試裡，那些攻擊測試也都通過。

## 我問過你的問題

| 問你的事 | 你的回答 |
|---|---|
| 提醒什麼時候送 | 每次你送出訊息時 |
| 只在 loom 流程裡生效，還是 loom 所有工具都生效 | loom 所有工具都要生效 |
| 只放一個外掛，還是兩個外掛都放 | 只放 loom-workflow |
| 完整寫作指南要新增一個 skill，還是放進現有的圖表 skill | 放進 loom-visualization，減少 skill 數量 |
| 對話情境的表格範例要併進這次嗎 | 併進這次 |
| 表格集分成「一般情境＋軟體／設計／商業三份」，並補上 9 月 4 日的研究，可以嗎 | 可以 |
| 決策選項的規則（是非題直接問、至少兩個可行做法並標出推薦、檢查常被漏掉的選項）可以嗎 | 可以 |
| 接受縮小方案嗎？三份專業表格集延後還是這次收 | 接受縮小方案，但三份表格集這次就收 |
| 確認整體內容：每則訊息多用一些字數、Codex 要重新信任、只裝 loom-code 收不到、審查通過後自動推送並開 PR | 確認 |

## 你要的東西，一條一條核對

### 1. In a Claude Code session with loom-workflow installed, each user message reaches the agent together with one short reminder, written once in English, to reply in the user's language, lead with the conclusion and its impact, replace internal terms with plain words, speak literally without metaphors, and show structured content as tables or diagrams through loom-visualization.
- **我怎麼試**：
  - 先直接執行提醒程式，送進一則模擬「你送出訊息」的事件，看它吐出什麼。
  - 再開真正的 Claude Code 對話：只載入這份乾淨複本的外掛，關掉你自己的全域設定和說明檔，連續送兩則訊息。
  - 最後問 agent 每則訊息旁邊出現了什麼，並對照對話紀錄檔確認。
- **結果**：
  - 每則訊息都附上一份英文提醒，約 150 個英文字。
  - 內容五項都有：用使用者的語言回覆、第一句講結論和影響、內部用語換成白話、照字面講不用比喻、結構化內容交給圖表 skill 用表格或圖呈現。
  - 兩則訊息各收到一次，沒有重複。
  - 另外 9 次改寫和問答的試跑，每一次也都收到剛好一份。
- **證據**：`evidence/blind-run/hook-runs.txt`（案例 A1）、`evidence/blind-run/live-session-hook.txt`（兩則訊息，各附一份 `hook_additional_context`，事件為 `UserPromptSubmit`）、`evidence/blind-run/trial-card-delivery.txt`
- **判定**：做到 — 每則訊息都帶著同一份提醒。

### 2. The table-and-diagram trigger reaches the agent through that per-turn reminder; a session start no longer delivers it separately, and with ascii-graph-toolkit also installed the reminder still carries one diagram trigger instruction, not two conflicting ones.
- **我怎麼試**：
  - 查看外掛登記的觸發時機，確認「對話開始時」已經沒有這份提醒。
  - 在真正的對話裡問 agent：第一則訊息之前，有沒有收到任何圖表提醒？
  - 準備一份「也裝了 ascii-graph-toolkit 並啟用」的設定，執行提醒程式。
- **結果**：
  - 外掛只在「你送出訊息時」送提醒，對話開始時不送。agent 也回答開場前沒收到。
  - 裝了 ascii-graph-toolkit 時，程式改送另一版提醒：流程圖、狀態圖、架構圖交給 ascii-graph-toolkit 自己的提醒處理，本身只保留一套圖表指示。
  - 限制：我沒有在同一個對話裡同時載入兩個外掛，所以沒親眼看到兩份提醒並排的樣子。兩份不衝突，是讀文字判斷的。
- **證據**：`evidence/blind-run/checks.txt`（兩份 hooks 設定只有 `UserPromptSubmit`）、`evidence/blind-run/hook-runs.txt`（案例 A2，標題 "ascii-graph-toolkit active"，150 字）、`evidence/blind-run/live-session-hook.txt`（第二則訊息的回答第 1 點）
- **判定**：做到 — 開場不再另外送；裝了 ascii-graph-toolkit 時換成單一圖表指示的版本。

### 3. In a Codex CLI session with loom-workflow installed and its hooks trusted, each user message reaches the agent with the same reminder.
- **我怎麼試**：
  - 照 Codex 設定裡寫的方式（加上 Codex 專用參數）執行提醒程式。
  - 查看 Codex 版的觸發設定。
  - 沒有開真正的 Codex 對話：這台機器裝了 Codex 0.154.0，但要讓外掛的觸發程式生效，得在互動畫面裡按一次信任，我無法代你按。
- **結果**：
  - 程式送出和 Claude Code 相同的提醒全文，只用 Codex 接受的那一種輸出格式，沒有多餘欄位。
  - 觸發時機是「每次送出訊息」，最多等 5 秒。
- **證據**：`evidence/blind-run/hook-runs.txt`（案例 A3：只有 `hookSpecificOutput` 一個鍵）、`evidence/blind-run/checks.txt`（`hooks-codex.json` 登記 `UserPromptSubmit`）
- **判定**：部分 — 程式輸出正確，但沒有在真正的 Codex 對話裡確認提醒真的送到。

### 4. In an Antigravity CLI session with loom-workflow installed, the same reminder is active in every session.
- **我怎麼試**：
  - 逐位元比對 Antigravity 用的規則檔和提醒原文。
  - 執行專案自己的「產生檔是否過期」檢查。
  - 沒有開真正的 agy 對話：在 agy 安裝這份外掛，會蓋掉你機器上已裝的那一份。
- **結果**：規則檔除了第一行「此檔由程式產生」的註記，其餘和提醒原文完全相同，過期檢查也通過。
- **證據**：`evidence/blind-run/checks.txt`（`cmp` 結果 0、`sync_codex_manifests.py --check --all` 結束碼 0）
- **判定**：部分 — 檔案內容正確，但沒有在 agy 裡實際確認。

### 5. When the reminder cannot be produced, the user's message still goes through unchanged.
- **我怎麼試**：
  - 讓提醒程式分別遇到五種狀況：
    - 收到壞掉的輸入；
    - 收到空的輸入；
    - 設定檔內容壞掉；
    - 兩份提醒檔都讀不到（權限拿掉）；
    - 兩份提醒檔都不存在。
  - 另外開一個真正的對話，外掛裡兩份提醒檔都移走，請 agent 把一句話原封不動回給我。
- **結果**：
  - 五種狀況都正常結束、沒有錯誤訊息。
  - 能讀到提醒檔時，照樣送出完整提醒；讀不到時，送出空白內容。
  - 真正的對話裡，agent 一字不差回了那句話，沒有看到任何錯誤訊息。
- **證據**：`evidence/blind-run/hook-runs.txt`（案例 A5a–A5e，全部 exit 0）、`evidence/blind-run/live-session-hook.txt`（最後一段，提醒檔移走的對話）
- **判定**：做到 — 提醒做不出來時，你的訊息照常送到。

### 6. Given three past hard-to-read loom replies, a fresh agent following the reminder and loom-visualization's writing guide rewrites each so that its first sentence states the conclusion, it contains no metaphor or analogy, and it names no internal term, file path or rule id without saying in plain words what it does; the guide's before-and-after examples come from real complaints.
- **我怎麼試**：
  - 拿三則過去真的很難讀的回覆，每則開一個全新的 Claude Code 對話，載入這份外掛（真正的提醒、真正的 skill 和指南）。
  - 在訊息裡貼上那則舊回覆，接著問「可以用更白話的方式說明嗎？」。
  - 限制：這種一次性對話無法事先塞入「agent 上一則回覆」，所以舊回覆是由使用者貼回去的。
  - 第一輪試跑作廢：我下錯一個參數，把所有 skill 都關掉了。紀錄另外保留，不算證據。
- **結果**：
  | 回覆 | 有沒有讀指南 | 第一句是結論 | 沒有比喻 | 內部用語有解釋 | 事實保持不變 |
  |---|---|---|---|---|---|
  | 第一則（請你重新確認三句行為） | 沒有 | 是，但前面加了「結論：」標籤 | 否，把重算核對碼說成「蓋章」 | 大致有 | 是 |
  | 第二則（改名合併、要你選 A 或 B） | 有 | 是 | 大致是，但用了「唱反調」這種說法 | 是 | 否，漏掉兩件事：哪些文件不再出現舊分類名詞、哪些部分不動；結尾還多出一個原文沒有的選項 |
  | 第三則（驗收盲跑報告） | 有 | 是 | 大致是，但延用了原文的「殼」 | 是 | 否，把 agent 說成「每個人」「第二個人」，把一個印字的指令說成「打字指令」 |
  - 指南裡的改寫前後範例共 8 組，我追得到其中 4 組是真實出處：
    - 「就像插座」「家裡三個門禁」寫在你的問題描述裡；
    - 「small lane／full lane」「薄殼開火」出現在真的舊回覆裡。
  - 另外 4 組我沒有原始的對話掃描資料，無法查證。
- **證據**：`evidence/blind-run/a6-rewrite-1.txt`、`a6-rewrite-2.txt`、`a6-rewrite-3.txt`、`evidence/blind-run/trial-judgments.txt`（逐則判定）、作廢的第一輪在 `evidence/blind-run/round1-setup-invalid/`
- **判定**：部分 — 三則都先講結論；但一則用了比喻，兩則掉了或改了事實，一則根本沒去讀指南。

### 7. Given a decision question about how to do something, a fresh agent following the guide offers at least two workable alternatives, marks the one it recommends, and either includes a do-nothing-or-later, smaller, or combined alternative or says in one sentence why none is workable; a yes-or-no confirmation is asked directly without invented alternatives.
- **我怎麼試**：同樣的全新對話，問兩件事：
  - 「網站圖片要從本機硬碟搬到雲端，要怎麼搬比較好？給我你推薦的做法。」
  - 「改好了、測試過了，推送並開 PR 前一定要先問我，請寫出你要傳給我的訊息。」
- **結果**：
  - 問「怎麼搬」：agent 叫用了圖表 skill，卻去讀了「步驟」範本，沒讀寫作指南。它只給一套六步驟做法，沒有第二個做法，也沒有檢查「先不做／做小一點／兩者合併」。
  - 問「可以推送嗎」：直接請你同意，沒有編出假選項。它另外列了分支名稱、遠端、目標分支三個「請確認」的空格，算多問，不算選項。
- **證據**：`evidence/blind-run/a7-how-question.txt`（讀了 `templates/02-linear-steps.md`，沒讀 `references/plain-language.md`）、`evidence/blind-run/a7-yes-no.txt`、`evidence/blind-run/trial-judgments.txt`
- **判定**：部分 — 是非題問法做到；「要怎麼做」的問題沒做到。

### 8. The loom-visualization skill carries every table usage found in the research — software development, design, and business analysis, plus the table patterns and table-writing rules from the earlier table research — together with a general set for common conversation situations (at least before versus after, per-item status, decision consequences, and hard-to-read versus plain wording) and the common mistakes to avoid; loom-workflow gains no new skill.
- **我怎麼試**：在修正後的版本上，把 9 月 16 日和 9 月 4 日兩份研究筆記的每個標題與規則，逐項對照 skill 裡的表格集和寫作指南。
- **結果**：
  - 9 月 16 日研究的三個領域全部收錄：軟體 20 種、設計 12 種、商業 18 種。
  - 9 月 4 日研究的 18 種有名稱的表格模式也都在：攤平的圖、評分、治理、相容性、2×2 象限、時間。
  - 一般對話情境有 8 種，包含前後對照、逐項狀態、決策後果；「難讀 vs. 白話」的對照範例也有。
  - 表格寫作規則、狀態符號、表格或圖怎麼選、什麼時候不該用表格，都有。
  - 修正後新增的「格子裡能放什麼」（方塊長條、迷你走勢、徽章、底色、進度條、內嵌圖）和「表格裡的時間」（時間當欄、時間當格子內容）也都在。
  - skill 數量改動前後都是 12 個，沒有新增。
  - 仍然沒收錄的三小項（都來自 9 月 4 日研究）：
    - 讀者要在兩個方向上比較時，表格勝過圖（Datawrapper 的判準）；
    - 流程圖、組織圖的正式文字版本就是表格（W3C 的做法）；
    - 不要把表格放在編號步驟的中間。
- **證據**：`evidence/blind-run/line8-coverage.txt`（40014ea3 的逐項對照、`S1–S31`、`D1–D12`、`B1–B23`、skill 目錄數 12/12、三項 `MISSING`）
- **判定**：部分 — 幾乎全部收錄，還差上面三小項。

### 9. Given a reply that reports progress, a fresh agent using the skill reads the general conversation set and none of the domain-specific table collections; given a request to write an incident report, it reads only the collection that holds that document type.
- **我怎麼試**：每種請求各開兩個全新對話，一個不特別指名，一個說「用 loom-visualization」：
  - 「幫我回報進度：資料匯出做完、登入頁補測試、付款卡在等金鑰」；
  - 「付款服務停了 40 分鐘，幫我寫事故報告」。
  - 記錄 agent 實際打開了哪些檔案。
- **結果**：
  - 指名 skill 的進度回報：只讀一般對話表格，完全沒讀三個領域的表格集，回覆用的正是進度表的四欄。
  - 事故報告兩次都叫用了 skill，只讀軟體領域的表格集（事故報告所在的那一份），外加一個時間軸範本。
  - 附帶觀察：不指名 skill 的進度回報，agent 沒叫用 skill，回了一串帶表情符號的清單，沒有用表格。
- **證據**：`evidence/blind-run/a9-progress-skill.txt`（只讀 `references/plain-language.md`）、`a9-incident-natural.txt` 與 `a9-incident-skill.txt`（只讀 `references/tables-software.md` ＋ `templates/10-timeline.md`）、`a9-progress-natural.txt`
- **判定**：做到 — 用到 skill 時，進度只讀一般表格，事故報告只讀對應的那一份。

### 10. loom-workflow's install documentation states that the reminder does not reach the Codex IDE extension or app, or the Antigravity desktop app and IDE, and that an install of loom-code without loom-workflow does not get it.
- **我怎麼試**：讀英文、日文、繁體中文三份安裝說明。
- **結果**：
  - 三份都有「每輪提醒送不到的地方」一節，列出三種情況：Codex 的 IDE 擴充與 app、Antigravity 桌面 app 與 IDE、只裝 loom-code 沒裝 loom-workflow。
  - 三份也都說明每輪約多 150 個英文字。
  - Codex 那一節另外提醒：舊版信任過的人要重新信任一次。
- **證據**：`loom-workflow/README.md`「Where the per-turn reminder does not arrive」、`README.ja.md`「毎ターンのリマインダーが届かない環境」、`README.zh-TW.md`「每輪提醒送不到的地方」
- **判定**：做到。

### 11. The repository's package tests and mechanism checks pass, and the number of registered mechanisms does not grow.
- **我怎麼試**：在乾淨複本上跑整套測試和機制數量檢查。
- **結果**：
  - 整套測試通過：3,097 項通過、11 項略過、0 項失敗；各組檢查腳本全部通過。
  - 機制數量 136，和改動前一樣，檢查結果「全部正常」。
- **證據**：`evidence/blind-run/package-tests.txt`（`run_package_tests.py --loom-family -q`，exit=0）、`evidence/blind-run/checks.txt`（`check_mechanisms.py --baseline 4dcd03a6`：net 136 / baseline 136，all clear）
- **判定**：做到。

## 對你既有的資料做了什麼

這個改動沒有讀寫你的任何資料，只改外掛自己的檔案。提醒程式每次會讀一下「裝了哪些外掛、啟用了哪些」的設定檔，只讀不寫。

已經安裝的人更新後，會有三個變化：
- **Claude Code**：提醒從「對話開始時一次」變成「每則訊息都送」，每則訊息多約 150 個英文字，一段長對話下來的用量會累積。
- **Codex**：觸發時機改了，要在 Codex 裡重新按一次信任。不按的話，Codex 會安靜地不送提醒，不會出現警告。
- **Antigravity CLI**：規則檔內容換成新提醒，重新安裝外掛後生效。

## 我幫你決定的事

- **提醒壓縮到原本的 150 字上限內，沒有放寬上限**：
  - 完整版 148 字，搭配 ascii-graph-toolkit 的版本剛好 150 字。
  - 以後想在提醒裡多加一句（例如下面「不確定」的第一點），就得刪掉別的字，或放寬上限。
- **沿用原本的提醒程式，只改觸發時機，沒有另外新增一支**：這是你接受縮小方案時同意的方向，理由是不增加檢查規則的數量。要改回「開場一次加每輪一次」，就得多一支程式。
- **Codex 最多等 5 秒**：這個值是對照 Codex 文件訂的，沒有在真正的 Codex 對話裡測過。
- **改寫指南修了兩輪以後，沒有做第三輪**：
  - 建置時的試跑就發現改寫會掉事實，我這次也看到一樣的情況。
  - 當時的判斷是，全新的 agent 手上沒有原本的來龍去脈，再修文字效果有限。
  - 如果你要求改寫不能掉事實，這裡還得再做一次。
- **建置途中加了三批原本計畫外的工作**：
  - 依試跑失敗修改寫指南；
  - 依攻擊測試的發現，修正檢查規則被反向改寫卻照樣通過的漏洞，並讓提醒程式在設定檔卡住時也能準時結束；
  - 補上第 8 條缺的表格內容。
- **你電腦上裝的舊版流程檢查程式，還要求填「改動大小分類」這個欄位**：這個分類已經拿掉了，建置時一律填「完整」，也就是分類拿掉後的預設值。
- **加權決策矩陣的處理**：
  - 完整版放在商業表格集，軟體表格集用一行指過去。
  - 日本工程部落格常見的技術選型比較表另外在軟體表格集保留完整一份。
- **提醒只有一份原稿**：Claude Code、搭配 ascii-graph-toolkit 的版本、Antigravity 規則檔都從同一份原稿讀取或產生。以後改提醒的字，不會動到觸發指令，Codex 使用者不必再重新信任。
- **三份表格集保留研究原本的來源網址和「未查證／由散文重建」標記**：你用的時候會看到這些標記。
- **寫作指南沒有加上「自動檢查」標記**：加了會多一條檢查規則，所以指南的規則只靠 agent 閱讀遵守，沒有程式會擋。
- **版本號升為 5.3.0**：提醒送出的時機改了，所以算一次功能更新，不是只修錯。

## 我不確定你要不要的事

- **問「要怎麼做」時，要不要讓提醒直接要求 agent 先讀寫作指南？** 現在提醒只在「你要求更白話」時才叫 agent 讀指南。這次試跑裡，agent 叫用了圖表 skill，卻沒讀指南，所以只給一個做法。加這句大約要多 15 個字，但會超過目前的字數上限。
- **改寫仍會掉事實或把 agent 說成「人」，你能接受嗎？** 還是要再修一輪指南？
- **不指名 skill 時，進度回報沒有用表格**，只是一串清單。這樣可以嗎？
- **Codex 和 Antigravity 我都沒有實際開對話試。** 要不要你在 Codex 按一次重新信任，並在 agy 各試一則訊息？
- **第 8 條剩下的三小項**（兩個方向比較用表格、表格當圖的文字版、別把表格塞進編號步驟中間），要補，還是算了？
- **有一件事和這次改動無關，但你可能想知道**：在 Codex 上，即使裝了 ascii-graph-toolkit，也一律送完整版提醒，這在改動之前就是如此。如果 ascii-graph-toolkit 在 Codex 上也送自己的提醒，Codex 可能會同時收到兩份圖表指示。

## 英文規則與格式規則有沒有守住

| 項目 | 有沒有全部用英文 | 這類文件另有的格式規則 | 證據 |
|---|---|---|---|
| 計畫 | 有；只有「問過你的問題」那幾行，照原樣記下當時用中文問你的話 | 無 | `plan.md` 的 `## Questions asked` |
| 規格 | 有；中文只出現在引用你原話的引號裡 | 守住：每條需求都是「在某情況下，系統應當……」的固定句型 | `spec.md` 的 `REQ-1`–`REQ-11`，全部以 WHEN/WHILE/IF/The … shall 開頭 |
| 審查意見 | 還沒有審查意見 | 還無法判斷每條意見有沒有標上類別標籤 | 無 |
| 證據檔 | 有；中文只出現在照原樣保存的輸入、輸出和比喻用詞清單裡 | 無 | `evidence/coldread/*.txt`、`evidence/blind-run/*.txt` |
| 測試說明文字 | 有；新增的測試行沒有中文。攻擊測試裡的中日文是測試用的假資料 | 無 | `test_probe_card_hook_boundaries.py:71`、`test_probe_prose_gate_mutants.py:139-140` |
| 測試名稱 | 有 | 部分守住：攻擊測試照「對象＿情況＿預期結果」命名；一般測試比較像一句描述，看不出「情況」這一段 | 守住的例子：`test_cardHook_nonUtf8Stdin_emitsFullCard`；沒守住的例子：`test_guide_has_seven_rules_and_rewrite_steps`、`test_sessionstart_wording_removed` |
| 提交訊息 | 有；這個改動自己的提交都是英文 | 大致守住：唯一格式不符的是合併主線時 git 自動產生的訊息。唯一含中文的提交訊息屬於另一個改動，是合併主線時帶進來的 | `git log --first-parent 4dcd03a6..HEAD`；`e32d4150 Merge origin/main into speak-plainly`；`dec4e927`（#21） |
