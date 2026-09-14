# 讓使用者為單一變更選擇要跑哪些 Loom 步驟 — 我試了什麼、發生了什麼

2026-09-14 在專案的乾淨副本上試跑兩次：第一次在 f595bc18，審查第一輪修正後在 3fce72c8 重跑受影響的第 1、2、7、8 條（其他各條的修正沒碰到，結果沿用第一次）。做法：把分支重新 clone 到暫存目錄，另外建一個拋棄式小專案（有本機假遠端、宣告了一條會通過的測試指令），用副本裡的檢查器，並把 Claude Code 與 Codex 兩份 hook 設定裡的指令原封不動拿出來，餵進兩種主機實際會送的 JSON。沒有開真的 Claude Code／Codex 對話，也沒有推到任何 GitHub。對抗測試那組 16 個案例在新版上也跑過，全部通過。

## 你要求的，一條一條看

### 1. After the user describes in natural language which steps to run or skip — either through the entry point or in ordinary conversation — the user sees a table of steps to run and steps to skip; after the user types the entry point's confirmation, the remaining steps of the change are only those marked to run; the user can withdraw a bound selection in their own words, and the full process resumes.
- **怎麼試**：提出「跳過審查與對抗測試」→ 看表格與確認碼 → 以使用者身分打「/loom-code:expert-mode 確認 碼」→ 查目前生效的步驟；接著用「取消」「cancel」「キャンセル」「撤回 碼」撤回，以及模擬 agent 聽到「不對，剛剛那個不算」後代為撤回；另外試了打錯步驟名、跳過別的步驟需要的步驟、想跳過「發布」。重跑時再試：撤回後重打同一個碼、rebase 後重打舊碼、打一個根本不存在的碼。
- **發生了什麼**：表格列出九個步驟各自 run／skip，附四碼確認碼。打確認後 hook 回一則訊息，列出實際綁定的執行與跳過清單，之後查到的就只剩標為執行的步驟。四種撤回說法都回「已撤回、恢復完整流程」；agent 代為撤回也一樣。「取消 review」不算撤回（依設計會當成新的選擇）。不存在的步驟、依賴沒滿足、「發布」都被拒絕，也不給確認碼。**新版**：撤回後或 rebase 後重打舊碼，hook 會回「這個碼已失效、什麼都沒記錄、請 agent 重新出表」，不再是沒反應；打一個從沒出現過的碼則依設計沒有 hook 訊息。各站的說明文字現在都寫了「使用者用自己的話說要跳過步驟時，走同一套流程、要等打確認」。
- **證據**：`selection propose` 輸出 `code: J5GV` 與九列表格；`systemMessage: "Loom: selection J5GV bound … Skip: reviewers, adversarial."`；撤回輸出 `withdrawn; the full process resumes.`；拒絕輸出 `unknown step 'publication'`、`step 'spec' requires 'intent'`；失效碼 `Loom: code J5GV is no longer valid (its selection was withdrawn or lapsed); nothing was recorded.`；各站說明 `When the user asks in their own words to run …`。
- **判定**：部分 — 表格、確認、撤回、失效碼提示在檢查器與 hook 層都照做；「在一般對話裡說出來 agent 真的會走同一套」與「使用者在真實對話畫面上真的看得到那則 hook 訊息」只寫在說明文字、必須開真的對話才能證明，這裡沒辦法驗。

### 2. Until that typed confirmation exists, the change follows the full process; a plain reply such as "yes" is not a confirmation.
- **怎麼試**：出表後分別回「yes」「對」「確認 碼」（前面沒有入口指令）；再送缺少 prompt 編號的、事件類型錯的 hook 資料；直接執行記錄指令；模擬 agent 用指令列或寫檔工具去改記錄。重跑時再試：agent 叫出一個巢狀的 Claude Code 或 Codex 對話、把入口指令和碼當成「使用者輸入」送進去（包括包在 bash -c 裡、以及用 Codex 的 hook 設定）；agent 先切到記錄資料夾裡面再寫；以及一般專案裡剛好叫 selections 的資料夾寫設定檔。這些都只餵給守門 hook 看，沒有真的開巢狀對話。
- **發生了什麼**：每一種之後查到的都是完整流程、沒有跳過。偽造與缺欄位的資料都被拒絕並註明「什麼都沒記錄」。agent 想直接跑記錄指令、用 >> 寫、先 cd 再寫、透過 git 目錄寫、用寫檔工具寫，全部被擋；一般的列出目錄與代為撤回則放行。**新版**：四種巢狀對話都被擋，理由是「巢狀對話的入口指令會被當成使用者親手打的」；在記錄資料夾裡面寫檔，Claude 與 Codex 兩邊都被擋；寫一般專案的 selections 設定檔、或只是搜尋含「expert-mode」字樣的檔案，都放行。
- **證據**：`bound= False skip= []`（三次）；`not a UserPromptSubmit payload with a prompt reference; nothing recorded.`；`BLOCK selection.guard: the selection capture command runs only from the prompt hook`、`names the selection record store`、`writes through the git directory`、`resolves under the loom record directory`；`ls models/selections/` exit 0；`claude -p "/loom-code:expert-mode J5GV"`、`codex exec "$expert-mode J5GV"` → `BLOCK selection.guard: a nested host session's expert-mode prompt would pass as user-typed`；在記錄資料夾內 `echo x >> …jsonl` → `writes from a working directory inside the loom record directory`；`echo cfg > app/selections/config.json` exit 0。
- **判定**：可用 — 沒有打確認就一律是完整流程。（刻意偽裝的指令本來就不在保護範圍，這是你已接受的邊界。）

### 3. Whatever the instruction, the change is still published through a pull request and merged, and cannot be pushed if its content differs from the content its record describes; the package tests may be skipped like any other step, and when they run they must pass.
- **怎麼試**：綁定「跳過審查與對抗測試」後結束審查（測試照跑）；把測試改成會失敗再結束一次；對內容檢查放行後再改一行程式看能不能推；模擬 agent 直接下 git push；用發布指令送一份格式不對的 PR 內容。（第一次試跑，f595bc18。）
- **發生了什麼**：測試有跑且通過，產生的紀錄寫明跳過了哪些步驟；測試失敗時被擋下並指出指令與結束碼。內容改動後推送被擋（內容與紀錄不符）。直接 git push 被擋。發布指令在碰網路之前就因 PR 標題結構不符而拒絕。
- **證據**：`wrote docs/loom/2026-09-14-tiny-param-change/attestation.json`，內含 `"kind": "package-tests" … "result": "pass"`、`"skip": ["reviewers","adversarial"]`；`BLOCK finalize.package-tests: \`python3 test_ok.py\` exited 3`；`BLOCK push.attestation: attestation functional content digest does not match the selected tree`；`BLOCK push.attestation: the entire Git push command must use canonical quote-all rendering`；`BLOCK push.contextual-body: … nine top-level contextual headings`。
- **判定**：部分 — 本機的閘全部照做；真的在 GitHub 開 PR 並合併這一段需要真的遠端與帳號，這裡沒試。

### 4. When the agent suggests skipping steps without the user having asked, the suggestion is shown at most once per change, the work continues on the full process without waiting for an answer, and no step is skipped unless the user later types the confirmation.
- **怎麼試**：以「agent 建議」的來源出表，回「yes」，再打正式確認。（第一次試跑。）
- **發生了什麼**：回「yes」後仍是完整流程；打確認後才綁定。「每個變更最多提一次、不等回覆」只寫在各站的說明文字裡，沒有程式能檢查。
- **證據**：`--origin agent` 出表 → `yes` → `bound= False` → `/expert-mode J5GV` → `bound= True`；各站說明寫有「at most once per change」。
- **判定**：部分 — 「不確認就不跳過」照做；「只提一次、不停下來等」要在真實對話裡看 agent 的行為才知道，這裡沒辦法驗。

### 5. The pull request states which steps were skipped and whether the authority is the user's own recorded words or an agent-recorded instruction.
- **怎麼試**：拿實際產生的紀錄讓發布檢查去比對四種 PR 內容：完全相符、漏掉先前失敗那行、把授權來源改掉、沒有選擇卻寫了跳過行。（第一次試跑；重跑時另外確認新版產生的應寫內容，見第 7 條。）
- **發生了什麼**：只有完全相符的通過；其他三種都被拒絕，而且錯誤訊息直接列出應該寫的那幾行。
- **證據**：應寫內容 `Skipped steps: reviewers, adversarial — authority: user-typed (J5GV, 2026-09-14)` 與 `Prior failure: reviewers finalize.verdicts 2026-09-14`；相符 → `None`；其餘 → `must start with exactly the attestation's selection disclosure`、`attestation records no step selection`。
- **判定**：可用 — 這是直接呼叫發布檢查裡的比對邏輯試的；完整的發布指令要有 GitHub 遠端才會走到這一步。

### 6. A selection applies only to the change it was given for; the next change follows the full process unless the user gives a new instruction.
- **怎麼試**：合併後從主線開新分支，查另一個新變更，也查沿用同一個變更名稱的情況。（第一次試跑。）
- **發生了什麼**：兩者都是完整流程，舊的選擇沒被帶過來。（新版改成先前的失敗紀錄跟著變更名稱走、不再看分支，所以沿用同一個變更名稱時舊的失敗會被帶到；選擇本身仍然不會。這點在新版沒有重跑。）
- **證據**：`2026-09-15-next-change` → `"bound": false`；同名變更在新分支 → `bound= False skip= []`。
- **判定**：可用。

### 7. An instruction given partway through a change affects only the steps after it; a failure the checker recorded before it still appears in the pull request.
- **怎麼試**：第一次：完整流程下結束審查失敗 → 確認一次選擇 → 主線前進並 rebase → 查狀態 → 重新出表、再確認 → 結束審查。重跑：完整流程下結束審查失敗 → 把分支改名 → 確認「跳過審查與對抗測試」→ 撤回 → 改確認「只跳過對抗測試」→ 結束審查 → 看紀錄與應寫的 PR 揭露行。
- **發生了什麼**：rebase 後綁定的選擇失效、恢復完整流程，但先前的失敗還在；重打確認就重新綁定，最後的紀錄列出這筆先前失敗。**新版**：分支改名後失敗紀錄仍在；重新確認後紀錄列出它是「先前的失敗」。被撤回的那次確認不會出現在紀錄裡，PR 應寫的只有最後生效的那一次，加上先前失敗那一行。
- **證據**：`BLOCK finalize.verdicts: review input has no verdicts`；改名後 `failures= [('reviewers', 'finalize.verdicts', 'feature')]`；紀錄只有 `"confirmations": [{"code": "UG6O", "skip": ["adversarial"] …}]`、`"prior_failures": [{"step": "reviewers", "rule": "finalize.verdicts" …}]`；應寫內容 `Skipped steps: adversarial — authority: user-typed (UG6O, 2026-09-14)` / `Prior failure: reviewers finalize.verdicts 2026-09-14`。
- **判定**：可用。

### 8. The user can list the merged changes that skipped review.
- **怎麼試**：合併前查一次、合併到本機假遠端的主線後再查一次（第一次試跑）；重跑時確認使用者從哪裡能知道這個查詢。
- **發生了什麼**：合併前印「沒有合併過的變更跳過審查」；合併後印出一行：變更名稱、合併提交、跳過的步驟。**新版**：檢查器的用法說明列出這個查詢，expert-mode skill 的邊界段落寫明它做什麼，更新紀錄也寫了指令名稱。三種語言的 README 現在介紹了 expert-mode，但沒有寫這個查詢的指令。
- **證據**：`no merged change skipped review` → `2026-09-14-tiny-param-change 5ee0557 skipped: reviewers, adversarial`（`5ee0557 Merge feature`）；用法說明第 19 行 `loom_checker.py selection skipped-review`；expert-mode skill 第 80 行、更新紀錄第 16 行。
- **判定**：可用 — 查詢正確，也找得到；只要從 README 開始讀，還要多點進 expert-mode 才看得到。

### 9. The entry point works on both Claude Code and Codex CLI, each through its own way of invoking a skill, with the same results.
- **怎麼試**：同一套流程改用 Codex 的資料格式與 Codex 的 hook 指令：回「yes」、打「$expert-mode 碼」、「$expert-mode 取消」、重新出表後「$loom-code:expert-mode go 碼」、「cancel」；再用 Codex 的指令列與 apply_patch 去寫記錄。（第一次試跑；重跑時 Codex 的守門另外見第 2 條。）
- **發生了什麼**：結果與 Claude Code 完全一樣（yes 不綁定、確認後綁定、撤回恢復完整流程、兩種寫記錄都被擋）。這台機器上的 Codex 載入的是舊版外掛，而且開 Codex 會用到你真正的設定，所以沒有開真的 Codex 對話；Codex 實際把外掛 skill 呼叫寫成什麼字、以及還沒信任 hook 時的情況都沒驗到。
- **證據**：Codex 格式 `$expert-mode J5GV` → 與 Claude 相同的綁定訊息；`$loom-code:expert-mode go J5GV` → `"bound": true`；`BLOCK selection.guard: .git/loom/selections/a.jsonl resolves under the loom record directory`（apply_patch）。
- **判定**：部分 — 兩種資料格式結果一致；真實 Codex 對話這裡沒辦法驗。

### 10. `KICKOFF-DEFAULTS.md`, the contract manifest and the templates no longer carry the unused lane settings, and the repository's existing Loom checks still pass.
- **怎麼試**：在副本搜尋 lane 相關設定；跑機制登記檢查；拿一份還留著 `lane:` 行的舊 intent 讓檢查器檢查。（第一次試跑。）
- **發生了什麼**：KICKOFF-DEFAULTS、契約、樣板都沒有 lane 設定了，KICKOFF-DEFAULTS 只留一行註明移除原因；契約裡「full-lane」字樣只出現在第二供應商那項，那是另一個仍在用的概念，依設計保留。機制登記檢查全部通過。舊 intent 留著 lane 行仍然通過。整套套件測試沒有在這裡跑，會在之後的結束審查步驟執行。
- **證據**：`check_mechanisms.py` → `all clear`（exit 0）；舊 intent 檢查 exit 0；KICKOFF-DEFAULTS 第 14 行 `Removed \`default-lane\` — …`。
- **判定**：部分 — lane 設定已清掉、機制檢查通過；套件測試等結束審查時才跑。

## 對你既有的資料做了什麼

這個變更不會改寫你已經有的程式或文件內容。它新增一份選擇紀錄，放在 git 的內部資料夾裡，不進版本控制、也不算進審查比對的內容，刪掉就等於從來沒選過（回到完整流程）。本專案的 KICKOFF-DEFAULTS 被拿掉了「預設 lane」那一行，並附上註明原因與日期的說明；其他採用 Loom 的專案，它們自己的檔案不會被動到，舊的 intent 裡如果還留著 lane 行也照樣通過（試過）。沒有選擇的舊審查紀錄依設計仍然有效，但這一點我沒有另外試。

## 我替你決定了

- **確認碼是四個字元、從選擇內容算出來** — 同樣的選擇永遠是同一個碼。碼一旦被撤回或因 rebase 失效，重打會被告知失效，要 agent 重新出表才能再確認。之後要改：碼的長度或算法一改，舊的確認就全部作廢。
- **hook 只認四個撤回字（取消、cancel、キャンセル、撤回）** — 其他說法（例如「不對，剛剛那個不算」）要靠 agent 聽懂後代為撤回。如果 agent 沒聽懂，你會以為撤回了其實沒有。
- **打一個從沒出現過的碼，hook 不出聲** — 只有「曾經有效、現在失效」的碼會收到提示；打錯字時要靠 agent 說明沒記錄到。
- **寫成拒絕語氣但帶著碼，例如「/expert-mode 不要 碼」，照樣生效** — hook 會跳出綁定訊息，要撤回得再下取消。
- **rebase 或把主線合進來，會讓已綁定的選擇失效；失敗紀錄則跟著變更名稱保留，改分支名或 rebase 都不會消失** — 你得重新確認一次；沿用同一個變更名稱的新分支也會帶著舊的失敗。
- **被撤回的確認不寫進 PR** — PR 只揭露最後仍生效的選擇與它之前的失敗。
- **擋下 agent 自己開巢狀的 Claude Code／Codex 對話並送入口指令** — 靠比對指令文字；刻意偽裝的寫法不在保護範圍。
- **「代理記錄的授權」只保留了寫法，目前沒有任何指令會產生它** — 因為兩種主機都抓得到你打的字。
- **「建議跳過最多一次、不停下來等」只寫在說明文字** — 沒有程式能驗，靠回歸測試裡的文字檢查。
- **跳過審查的清單只看遠端主線上已合併的紀錄** — 還沒合併、或遠端主線沒抓下來時，查不到。
- **審查站被駁回的重要以上發現**：審查站沒有交給我任何這類駁回，這次沒有可列的。

## 我不確定你要不要的

- 開真的 Claude Code 與 Codex 對話，確認 hook 訊息你看得到、Codex 的 skill 呼叫字面真的是「$expert-mode」、agent 在一般對話裡真的會走同一套 — 要在驗收前補做嗎？
- 跳過審查的查詢要不要也寫進 README？目前要點進 expert-mode 的說明才看得到。

## 英文規則與樣板規則是否守住

| 文件 | 英文規則 | 樣板規則 | 證據 |
| --- | --- | --- | --- |
| 計畫 | 守住 | 不適用 | `plan.md` 全英文 |
| 規格 | 守住 | 守住（每條需求都是 EARS 句型並對回驗收編號） | `spec.md` `REQ-1`…`REQ-11` |
| 審查紀錄的發現 | 尚無可檢查的內容 | 尚無可檢查的內容 | 變更資料夾內沒有審查紀錄檔 |
| 證據 | 守住 | 不適用 | 擷取輸出皆為英文；`evidence/probes/test_selection_adversarial_probes.py` 16 passed |
| 測試說明文字 | 守住（中文只出現在模擬使用者輸入的測試資料） | 不適用 | `test_selection_capture.py:163` 等 |
| 測試名稱 | 守住 | 守住（單元_狀態_預期） | `test_plain_yes_binds_nothing`、`test_failure_survives_rebase` 等 |
| 提交訊息 | 守住 | 不適用 | `feat(loom-code): …`、`fix(loom-code): …` |
