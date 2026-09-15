# 讓 loom 的回覆講白話、照字面講、用表格或圖 — 我試了什麼、結果如何

試跑日期：2026-09-16。每一條都在乾淨的專案複本上試，但依修正時間分成幾個版本：

| 版本 | 在這個版本檢查了哪幾條 | 說明 |
|---|---|---|
| dda0014f | 3、5、6、10、11 | 第一次完整試跑 |
| 40014ea3 | 8（當時還缺三小項） | 補上「格子裡能放什麼」「表格裡的時間」之後 |
| eacf718f | 1、2、4、7（當時仍不合格） | 提醒加上「做決定前先讀指南」、指南補上三小項之後 |
| 75024929 | 1、2、4、7、8、9 | 提醒改成直接寫出決策規則、指南換了範例並修正引用、skill 的分流說明改寫之後 |

第 6 條的試跑是在 dda0014f 做的，沒有重跑。理由：提醒前三條規則（結論先講、白話、照字面講）從那時到現在一字未改，而「你要求更白話時先讀指南」這句也仍在；改寫試跑正是這種情況。指南本身這次改的是決策問題那一條的範例和一則引用數字，不影響改寫。

**一句話結論**：每則訊息附帶提醒、表格集收錄、只讀需要的檔案，這三件事都做到了。還差兩件：
- 改寫時仍會掉事實或改事實，有一次還用了比喻。
- 問「要怎麼做」時，現在每次都給兩個以上做法並排成表格了，但五次裡有三次沒有標出「我推薦哪一個」，而是改成講一套先後順序。

| 條目 | 結果 | 檢查版本 |
|---|---|---|
| 1 每則訊息附帶提醒（Claude Code） | 做到 | 75024929 |
| 2 開場不再另外送；裝了 ascii-graph-toolkit 也只有一份圖表指示 | 做到 | 75024929 |
| 3 Codex CLI | 部分（沒有實際開 Codex 對話） | dda0014f（提醒輸出在 75024929 再跑一次） |
| 4 Antigravity CLI | 部分（沒有實際開 agy 對話） | 75024929 |
| 5 提醒出錯時訊息照常送出 | 做到 | dda0014f（在 75024929 再跑一次） |
| 6 白話改寫 | 部分 | dda0014f |
| 7 決策問題的問法 | 部分 | 75024929 |
| 8 表格集收錄完整 | 做到 | 75024929 |
| 9 只讀需要的表格集 | 做到 | 75024929 |
| 10 安裝說明寫清楚收不到的地方 | 做到 | dda0014f |
| 11 測試與機制檢查 | 做到 | dda0014f（機制數量在 75024929 再確認） |

## 審查摘要

- 審查第一輪已經看過，提出的問題都已修掉並提交；還沒有被駁回而不修的意見。
- 在 dda0014f 的乾淨複本上，整套測試都通過：3,097 項通過、11 項略過、0 項失敗，另外幾組檢查腳本也全部通過。之後版本的整套測試由建置那邊重跑，我沒有再跑。
- 檢查規則的數量在 dda0014f、eacf718f、75024929 都是 136，和改動前一樣。
- 建置階段有另一個 agent 專門試著弄壞這個改動，寫了攻擊測試。在我跑的那一次整套測試裡，那些攻擊測試也都通過。

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
  - 直接執行提醒程式，送進一則模擬「你送出訊息」的事件，看它吐出什麼。
  - 開真正的 Claude Code 對話：只載入乾淨複本的外掛，關掉你自己的全域設定和說明檔，請 agent 引用提醒的第一行和最後一句。
  - 對照對話紀錄檔確認每則訊息各帶幾份。
- **結果**：
  - 每則訊息都附上一份英文提醒：一般版 148 個英文字，搭配 ascii-graph-toolkit 的版本 150 個。
  - 內容五項都有：用使用者的語言回覆、第一句講結論和影響、內部用語換成白話、照字面講不用比喻、結構化內容交給圖表 skill 用表格或圖呈現。
  - 最後一句現在直接寫出決策規則：「問或答『要怎麼做』時，用表格列出兩個以上可行做法並標出推薦；要講得更白話時，先讀寫作指南。」我請 agent 引用時，它照抄了這句話分號後面那半句，標題也一字不差。
  - 每則訊息都只收到一份；這次的六次問答試跑，每一次也都收到剛好一份。
- **證據**：`evidence/blind-run/hook-runs-75024929.txt`（案例 A1，148 字）、`evidence/blind-run/live-session-hook.txt`（最後一段：標題與最後一句）、各試跑檔開頭的 `card delivery` 行
- **判定**：做到 — 每則訊息都帶著同一份提醒。

### 2. The table-and-diagram trigger reaches the agent through that per-turn reminder; a session start no longer delivers it separately, and with ascii-graph-toolkit also installed the reminder still carries one diagram trigger instruction, not two conflicting ones.
- **我怎麼試**：
  - 查看外掛登記的觸發時機，確認「對話開始時」已經沒有這份提醒。
  - 準備一份「也裝了 ascii-graph-toolkit 並啟用」的設定，執行提醒程式，讀這一版的全文。
  - 用程式逐字比對兩個版本的前三條規則。
  - 在真正的對話裡問 agent：看到幾份提醒。
- **結果**：
  - 外掛只在「你送出訊息時」送提醒，對話開始時不送。
  - 兩份提醒的標題改短了：一般版寫「loom-workflow」，另一版寫「ascii-graph-toolkit」，一看就知道現在生效的是哪一份。
  - 前三條規則兩份一字不差；第四條分工不同：搭配 ascii-graph-toolkit 的版本把流程圖、狀態圖、架構圖交給 ascii-graph-toolkit 自己的提醒，本身只保留一套圖表指示。
  - 真正的對話裡只看到一份。
  - 限制：我沒有在同一個對話裡同時載入兩個外掛，所以沒親眼看到兩份提醒並排的樣子。兩份不衝突，是讀文字判斷的。
- **證據**：`evidence/blind-run/checks-75024929.txt`（兩份 hooks 設定只有 `UserPromptSubmit`；兩張卡片字數 148／150；前三條規則比對結果 True）、`evidence/blind-run/hook-runs-75024929.txt`（案例 A2）、`evidence/blind-run/live-session-hook.txt`
- **判定**：做到。

### 3. In a Codex CLI session with loom-workflow installed and its hooks trusted, each user message reaches the agent with the same reminder.
- **我怎麼試**：
  - 照 Codex 設定裡寫的方式（加上 Codex 專用參數）執行提醒程式，並查看 Codex 版的觸發設定。
  - 沒有開真正的 Codex 對話：這台機器裝了 Codex 0.154.0，但要讓外掛的觸發程式生效，得在互動畫面裡按一次信任，我無法代你按。
- **結果**：程式送出和 Claude Code 相同的提醒全文，只用 Codex 接受的那一種輸出格式，沒有多餘欄位；觸發時機是「每次送出訊息」，最多等 5 秒。在 75024929 重跑，結果相同。
- **證據**：`evidence/blind-run/hook-runs-75024929.txt`（案例 A3：只有 `hookSpecificOutput` 一個鍵，148 字）
- **判定**：部分 — 程式輸出正確，但沒有在真正的 Codex 對話裡確認提醒真的送到。

### 4. In an Antigravity CLI session with loom-workflow installed, the same reminder is active in every session.
- **我怎麼試**：
  - 逐位元比對 Antigravity 用的規則檔和新版提醒原文。
  - 執行專案自己的「產生檔是否過期」檢查。
  - 沒有開真正的 agy 對話：在 agy 安裝這份外掛，會蓋掉你機器上已裝的那一份。
- **結果**：規則檔已經跟著這次改動重新產生。除了第一行「此檔由程式產生」的註記，其餘和新版提醒完全相同，過期檢查也通過。
- **證據**：`evidence/blind-run/checks-75024929.txt`（`cmp` 結果 0、`sync_codex_manifests.py --check --all` 結束碼 0）
- **判定**：部分 — 檔案內容正確，但沒有在 agy 裡實際確認。

### 5. When the reminder cannot be produced, the user's message still goes through unchanged.
- **我怎麼試**：
  - 讓提醒程式分別遇到五種狀況：壞掉的輸入、空的輸入、設定檔內容壞掉、兩份提醒檔讀不到、兩份提醒檔不存在。
  - 另外開一個真正的對話，外掛裡兩份提醒檔都移走，請 agent 把一句話原封不動回給我。
- **結果**：
  - 五種狀況都正常結束、沒有錯誤訊息；讀得到提醒檔時照樣送出完整提醒，讀不到時送出空白內容。在 75024929 重跑，結果相同。
  - 真正的對話裡，agent 一字不差回了那句話，沒有看到任何錯誤訊息。
- **證據**：`evidence/blind-run/hook-runs-75024929.txt`（案例 A5a–A5e，全部 exit 0）、`evidence/blind-run/live-session-hook.txt`（提醒檔移走的對話）
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
- **證據**：`evidence/blind-run/a6-rewrite-1.txt`、`a6-rewrite-2.txt`、`a6-rewrite-3.txt`、`evidence/blind-run/trial-judgments.txt`、作廢的第一輪在 `evidence/blind-run/round1-setup-invalid/`
- **判定**：部分 — 三則都先講結論；但一則用了比喻，兩則掉了或改了事實，一則根本沒去讀指南。

### 7. Given a decision question about how to do something, a fresh agent following the guide offers at least two workable alternatives, marks the one it recommends, and either includes a do-nothing-or-later, smaller, or combined alternative or says in one sentence why none is workable; a yes-or-no confirmation is asked directly without invented alternatives.
- **我怎麼試**：
  - 提醒改成直接寫出決策規則之後，一共看了五個「要怎麼做」和一個是非題：
    - 建置那邊重跑了圖片搬遷、權限檢查、日誌塞滿三題，以及刪除遠端分支的是非題；我照 Acceptance 的原文自己重新判定，沒有直接採用他們的結論。
    - 我自己再出兩題：資料庫變慢怎麼處理（新題）、日誌塞滿（重跑上一版失敗的那一題）。
  - 建置那邊的四個試跑在 4af823eb，我的兩個在 75024929；兩者的提醒、指南、skill 說明完全相同。
- **結果**：
  | 問題 | 有沒有讀指南 | 可行做法數 | 排成表格 | 標出推薦 | 合乎這一條 |
  |---|---|---|---|---|---|
  | 圖片搬遷（建置那邊跑） | 沒有 | 4 | 是 | 有 | 是 |
  | 權限檢查（建置那邊跑） | 沒有 | 3 | 是 | 有，而且說明是合併兩個做法 | 是 |
  | 日誌塞滿（建置那邊跑） | 沒有 | 4 | 是 | 沒有，改講先後順序 | 否 |
  | 資料庫變慢（我出的新題） | 沒有 | 7 | 是 | 沒有，改講先後順序 | 否 |
  | 日誌塞滿（我重跑） | 沒有 | 4 | 是 | 沒有，改講先後順序 | 否 |
  - 進步：五次都給了兩個以上可行做法，而且都排成表格。上一版有一次只給一套方案。
  - 還差的地方：五次有三次沒有標出「我推薦哪一個」，而是改成「先做這個、再做那個」的順序。這種寫法你還是得自己判斷要選什麼。
  - 是非題（刪除已合併的遠端分支）直接問你要不要刪，沒有編出假選項；前幾版的三次是非題也都是直接問。
  - 指南在這六次裡一次都沒有被打開。現在是提醒裡那句規則在發揮作用，不是指南。
- **證據**：`evidence/blind-run/a7-how-question-after-w4-04.txt`、`a7-how-auth-after-w4-04.txt`、`a7-how-logs-after-w4-04.txt`、`a7-yes-no-delete-after-w4-04.txt`（建置那邊跑）、`a7-how-db-75024929.txt`、`a7-how-logs-75024929.txt`（我跑的）、逐則判定在 `evidence/blind-run/trial-judgments.txt`
- **判定**：部分 — 是非題做到，做法數量和表格也做到；但「標出推薦哪一個」五次只做到兩次。

### 8. The loom-visualization skill carries every table usage found in the research — software development, design, and business analysis, plus the table patterns and table-writing rules from the earlier table research — together with a general set for common conversation situations (at least before versus after, per-item status, decision consequences, and hard-to-read versus plain wording) and the common mistakes to avoid; loom-workflow gains no new skill.
- **我怎麼試**：把 9 月 16 日和 9 月 4 日兩份研究筆記的每個標題與規則，逐項對照 skill 裡的表格集和寫作指南；這次再確認審查後改動的四處。
- **結果**：
  - 9 月 16 日研究的三個領域全部收錄：軟體 20 種、設計 12 種、商業 18 種。
  - 9 月 4 日研究的 18 種有名稱的表格模式也都在：攤平的圖、評分、治理、相容性、2×2 象限、時間。
  - 一般對話情境有 8 種，包含前後對照、逐項狀態、決策後果；「難讀 vs. 白話」的對照範例也有。
  - 表格寫作規則、狀態符號、表格或圖怎麼選、什麼時候不該用表格、格子裡能放什麼、表格裡的時間，都有；前一版缺的三小項（兩個方向比較用表格、表格當圖的文字版、別把表格塞進編號步驟中間）也都補上了。
  - 這次審查後的四處改動我都確認過：
    - 決策問題那一條的範例，從一段文字改成真正的「決策後果」表格，並標出推薦；
    - 表格規則第一條加了例外：一欄名稱、一欄內容的摘要表可以用（例如事故報告摘要、元件狀態表）；
    - 引用數字改正（詳見下面「我幫你決定的事」）；
    - 商業表格集不再宣稱自己收了「誰負責哪件事」的那張表，改指向軟體表格集。
  - skill 數量改動前後都是 12 個，沒有新增。
- **證據**：`evidence/blind-run/line8-coverage.txt`（逐項對照，`S1–S31`、`D1–D12`、`B1–B23`）、`evidence/blind-run/checks-75024929.txt`（Datawrapper、text alternative、numbered steps、key-value 例外、Nutt 引用、商業檔的指向；skill 目錄數 12）
- **判定**：做到。

### 9. Given a reply that reports progress, a fresh agent using the skill reads the general conversation set and none of the domain-specific table collections; given a request to write an incident report, it reads only the collection that holds that document type.
- **我怎麼試**：skill 的分流說明這次改寫過（各領域檔案的文件類型列得更全，最後一句改成「只讀符合的那一列的檔案」），所以我在 75024929 重跑兩個試跑，記錄 agent 實際打開了哪些檔案：
  - 「用 loom-visualization 幫我回報進度……」；
  - 「用 loom-visualization 幫我寫一份事故報告……」。
- **結果**：
  - 進度回報：只讀一般對話表格那一份，三個領域的表格集一個都沒開，回覆用的正是進度表的四欄。
  - 事故報告：只讀軟體領域的表格集（事故報告所在的那一份），外加一個時間軸範本。
  - 之前在 dda0014f 的四個試跑結果相同。附帶觀察（當時記下的）：不指名 skill 的進度回報，agent 沒叫用 skill，回了一串帶表情符號的清單。
- **證據**：`evidence/blind-run/a9-progress-skill-75024929.txt`、`a9-incident-skill-75024929.txt`、之前的 `a9-progress-skill.txt`、`a9-incident-natural.txt`、`a9-incident-skill.txt`、`a9-progress-natural.txt`
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
  - dda0014f 整套測試通過：3,097 項通過、11 項略過、0 項失敗；各組檢查腳本全部通過。
  - 機制數量在 dda0014f、eacf718f、75024929 都是 136，和改動前一樣，檢查結果「全部正常」。
  - 後面幾版的整套測試我沒有重跑，由建置那邊負責。
- **證據**：`evidence/blind-run/package-tests.txt`、`evidence/blind-run/checks.txt`、`checks-eacf718f.txt`、`checks-75024929.txt`
- **判定**：做到。

## 對你既有的資料做了什麼

這個改動沒有讀寫你的任何資料，只改外掛自己的檔案。提醒程式每次會讀一下「裝了哪些外掛、啟用了哪些」的設定檔，只讀不寫。

已經安裝的人更新後，會有三個變化：
- **Claude Code**：提醒從「對話開始時一次」變成「每則訊息都送」，每則訊息多約 150 個英文字，一段長對話下來的用量會累積。
- **Codex**：觸發時機改了，要在 Codex 裡重新按一次信任。不按的話，Codex 會安靜地不送提醒，不會出現警告。
- **Antigravity CLI**：規則檔內容換成新提醒，重新安裝外掛後生效。

## 我幫你決定的事

- **提醒裡直接寫出決策規則，取代原本「做決定前先讀指南」那句**：
  - 原本那句只是叫 agent 去讀指南；試跑顯示它幾乎不去讀。現在規則直接寫在提醒裡：「用表格列出兩個以上可行做法並標出推薦」。
  - 代價是 agent 更不會去讀指南了（這次六個試跑都沒讀），所以指南裡那些比較細的規則——例如檢查「先不做／做小一點／兩者合併」——實際上沒有生效。
- **搭配 ascii-graph-toolkit 的版本，對「方框圖」的規定從「照原字句」改成「照意思」**：
  - 原因是這句話在自動測試裡被綁得太死，改一個字就會讓測試失敗；現在測試改成確認意思還在（方框圖要用圖表 skill 的對齊工具檢查）。
  - 代價是：以後有人把這句話改寫成別的說法，測試不一定擋得住。
- **提醒壓縮在 150 字上限內**：一般版 148 字、搭配 ascii-graph-toolkit 的版本 150 字。為了塞進決策規則，標題縮短、第四條也改寫過。再加任何一句，就得刪掉別的字，或放寬上限。
- **指南裡引用的研究數字改正了**：
  - 原本寫「只考慮一個選項時失敗率 52%，有兩個以上時 32%」，這兩個數字在來源裡查不到。
  - 現在改寫成來源真正說的：那份研究裡約一半的決策失敗；1999 年的研究指出，管理者只有不到兩成的決策會準備多個選項，而準備多個選項時成功率從 56% 升到 70%。
  - 影響：指南給的「為什麼要多個選項」的理由變弱一點，但至少是來源真的說過的話。
- **沿用原本的提醒程式，只改觸發時機，沒有另外新增一支**：這是你接受縮小方案時同意的方向，理由是不增加檢查規則的數量。
- **Codex 最多等 5 秒**：這個值是對照 Codex 文件訂的，沒有在真正的 Codex 對話裡測過。
- **改寫會掉事實，這件事不再多修一輪指南**：全新的 agent 手上沒有原本的來龍去脈，再修文字效果有限。如果你要求改寫不能掉事實，這裡還得再做一次。
- **建置途中加了五批原本計畫外的工作**：依試跑失敗修改寫指南；依攻擊測試修檢查規則的漏洞；補第 8 條缺的表格內容；依我的報告加上提醒的新句子和指南缺的三小項；依審查第一輪的意見改範例、改引用、改分流說明，並把提醒改成直接寫出決策規則。
- **你電腦上裝的舊版流程檢查程式，還要求填「改動大小分類」這個欄位**：這個分類已經拿掉了，建置時一律填「完整」。
- **加權決策矩陣的處理**：完整版放在商業表格集，軟體表格集用一行指過去；日本工程部落格常見的技術選型比較表另外在軟體表格集保留完整一份。
- **提醒只有一份原稿**：Claude Code、搭配 ascii-graph-toolkit 的版本、Antigravity 規則檔都從同一份原稿讀取或產生。以後改提醒的字，不會動到觸發指令，Codex 使用者不必再重新信任。
- **三份表格集保留研究原本的來源網址和「未查證／由散文重建」標記**。
- **寫作指南沒有加上「自動檢查」標記**：加了會多一條檢查規則，所以指南的規則只靠 agent 閱讀遵守，沒有程式會擋。
- **版本號升為 5.3.0**。

## 我不確定你要不要的事

- **「要怎麼做」的回答常常不標出推薦哪一個**，而是改給一套先後順序（五次裡有三次）。你覺得這樣可以嗎？如果不行，還得再想辦法，因為提醒已經沒有空間再加字。
- **指南實際上幾乎沒被打開過**：這六次試跑一次都沒有。指南裡比較細的規則（檢查「先不做／做小一點／兩者合併」）目前形同虛設。你要保留現況，還是要換別的做法？
- **改寫仍會掉事實或把 agent 說成「人」，你能接受嗎？**
- **不指名 skill 時，進度回報沒有用表格**，只是一串清單。這樣可以嗎？
- **Codex 和 Antigravity 我都沒有實際開對話試。** 要不要你在 Codex 按一次重新信任，並在 agy 各試一則訊息？
- **有一件事和這次改動無關，但你可能想知道**：在 Codex 上，即使裝了 ascii-graph-toolkit，也一律送一般版提醒，這在改動之前就是如此。如果 ascii-graph-toolkit 在 Codex 上也送自己的提醒，Codex 可能會同時收到兩份圖表指示。

## 英文規則與格式規則有沒有守住

| 項目 | 有沒有全部用英文 | 這類文件另有的格式規則 | 證據 |
|---|---|---|---|
| 計畫 | 有；只有「問過你的問題」那幾行，照原樣記下當時用中文問你的話 | 無 | `plan.md` 的 `## Questions asked` |
| 規格 | 有；中文只出現在引用你原話的引號裡 | 守住：每條需求都是「在某情況下，系統應當……」的固定句型 | `spec.md` 的 `REQ-1`–`REQ-11`，全部以 WHEN/WHILE/IF/The … shall 開頭 |
| 審查意見 | 審查第一輪的意見我沒有拿到全文，無法判斷 | 同左 | 無 |
| 證據檔 | 有；中文只出現在照原樣保存的輸入、輸出和比喻用詞清單裡 | 無 | `evidence/coldread/*.txt`、`evidence/blind-run/*.txt` |
| 測試說明文字 | 有；新增的測試行沒有中文。攻擊測試裡的中日文是測試用的假資料 | 無 | `test_probe_card_hook_boundaries.py:71`、`test_probe_prose_gate_mutants.py:139-140` |
| 測試名稱 | 有 | 部分守住：攻擊測試照「對象＿情況＿預期結果」命名；一般測試比較像一句描述，看不出「情況」這一段 | 守住的例子：`test_cardHook_nonUtf8Stdin_emitsFullCard`；沒守住的例子：`test_guide_has_seven_rules_and_rewrite_steps`、`test_sessionstart_wording_removed` |
| 提交訊息 | 有；這個改動自己的提交都是英文 | 大致守住：唯一格式不符的是合併主線時 git 自動產生的訊息。唯一含中文的提交訊息屬於另一個改動，是合併主線時帶進來的 | `git log --first-parent 4dcd03a6..HEAD`；`e32d4150 Merge origin/main into speak-plainly`；`dec4e927`（#21） |
