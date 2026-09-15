# 審查前先把分支跟上 main — 我試了什麼、發生了什麼

2026-09-15 在一份乾淨的專案副本（726891d）上試跑。所有情境都用暫存資料夾裡新建的練習用 git 專案，
遠端是本機上的一個空殼倉庫，完全沒有碰到真正的 GitHub。

## 結論

| # | 你要的 | 結果 |
|---|---|---|
| 1 | 分支落後且能乾淨合併時，審查前就帶進最新 main，之後綁定的內容一致 | 可用（有一個量不到的地方，見下） |
| 2 | 已經是最新時，不多加任何 commit | 可用 |
| 3 | 會衝突時，不派審查、分支原樣保留、列出每個衝突檔 | 可用（有一個小瑕疵，見下） |
| 4 | 連不上遠端時，警告後照常繼續 | 可用 |
| 5 | 帶進新內容時，派審查前先把整套測試和對抗程式重跑並通過 | 部分可用 — 停下並要求重跑的訊號確實出現，但沒有在真正的審查流程裡看到它被執行 |

## 你要的，一條一條看

### 1. When closing review starts on a change branch that lacks commits from the remote main and merges with it cleanly, the branch contains the freshly fetched remote main tip before the first reviewer is dispatched, and the generated attestation validates at the resulting HEAD.
- **我怎麼試的**：做一個練習專案，在功能分支上加一個檔案；另外從別處往遠端的 main 推一個不衝突的新檔案，而本機這邊刻意不先抓取。然後在功能分支上執行審查前的同步指令，接著照審查站的說明重跑測試（用一個簡單的替代測試），補上盲跑報告，最後模擬把審查結果記錄進分支，前後各算一次「內容指紋」（審查結果綁定的就是這個指紋）。
- **發生了什麼**：指令自己去遠端抓了最新的 main，合併進功能分支，並清楚說「內容變了，派審查前先重跑測試與對抗程式」。合併後分支確實包含遠端 main 的最新一筆；另開的 main 工作副本完全沒被動到。再跑一次同步指令，回報「已是最新、沒有新增 commit」。記錄審查結果前後，內容指紋完全相同，而且這份內容裡有從 main 帶進來的檔案。
- **證據**：遠端 main 最新 `94d4970`，本機原本只知道 `41fba5d`；指令輸出 `sync-trunk: merged origin/main (94d4970…) into feat/2026-09-15-toy-change; HEAD is now e911a87…` 與 `content changed -- re-run the package suite and adversarial programs before dispatching reviewers.`；`git merge-base --is-ancestor` 為真；main 工作副本 HEAD 不變、無未提交變更；補上報告後 HEAD `9c366e9` 指紋 `2899d42…`，記錄審查結果後 HEAD `d67936c` 指紋仍是 `2899d42…`。
- **結論**：可用 — 同步發生在派審查之前，綁定的內容就是會被合併的內容。限制：我沒辦法在暫存環境裡產生一份真正、有審查人簽核的審查結果，所以「審查結果驗證通過」這一段是用內容指紋相符來證明，不是跑完整驗證。

### 2. When the change branch already contains the remote main tip, starting closing review adds no commit to the branch.
- **我怎麼試的**：兩種狀況各試一次：(a) 分支從最新 main 分出、main 沒動；(b) main 往前走了，但我先手動把它合併進分支，再執行同步指令。
- **發生了什麼**：兩次都回報「已經包含 main，沒有新增 commit」，分支位置與 commit 數量前後都一樣。
- **證據**：(a) HEAD `114bef7` 前後相同，commit 數 2 → 2；(b) HEAD `255170f` 前後相同，commit 數 4 → 4；輸出 `sync-trunk: up to date -- … already contains origin/main (a1dcd9f…); no commit added.`
- **結論**：可用。

### 3. When bringing in the remote main conflicts, closing review dispatches no reviewer, the branch and working tree are left as they were before the attempt, and the report names every conflicting file.
- **我怎麼試的**：讓 main 和功能分支改到兩個相同檔案的同一行，然後執行同步指令。先在工作資料夾裡留一個未追蹤的筆記檔試一次，拿掉之後再試一次；另外也試了「能乾淨合併，但有改到一半、還沒提交的檔案」的情況。
- **發生了什麼**：
  - 乾淨資料夾：指令拒絕，逐行列出兩個衝突檔，說明「沒有真的去合併，分支還在原處、工作資料夾沒動」，也說明衝突不會自動解決、要回到實作階段處理。之後查看：分支位置沒變、沒有留下合併到一半的狀態、沒有多出任何變更。
  - 有未追蹤檔或未提交的修改：指令一樣拒絕，而且什麼都沒動（檔案內容、分支位置、那份筆記都保留），但它只說「請先提交或移除這些檔案」，**沒有**列出衝突檔。要先清掉再跑一次才會知道哪些檔衝突。
  - 依審查站說明，拒絕時不派任何審查人、把變更退回實作階段。
- **證據**：輸出 `BLOCK review.sync: conflict: app.txt`、`BLOCK review.sync: conflict: lib.txt`、`the merge was not attempted; feat/2026-09-15-toy-change is still at 1a5857c… and the worktree is untouched.`；結束碼 1；`git status --porcelain` 為空、無 `MERGE_HEAD`。有未追蹤檔時輸出 `BLOCK review.sync: the worktree has uncommitted or untracked changes (untracked-note.txt); commit or remove them first.`，前後狀態都是 `?? untracked-note.txt`。
- **結論**：可用 — 小瑕疵：工作資料夾不乾淨時，要跑兩次才看得到衝突清單。

### 4. When the remote cannot be reached, closing review reports a warning that the branch could not be checked against main and then continues without syncing.
- **我怎麼試的**：把遠端網址改成連不到的位址（本機一個沒在聽的連接埠），再改成不存在的路徑，各執行一次同步指令。
- **發生了什麼**：兩次都印出警告，說抓不到 main、所以沒辦法確認分支有沒有跟上，然後「不同步、繼續」；結束碼是 0（不算失敗），分支沒被改。審查站的說明要求把這個警告寫進該輪報告並繼續審查。
- **證據**：`WARN review.sync: could not fetch origin/main, so the branch could not be checked against main: fatal: unable to access 'https://127.0.0.1:9/nope.git/': … Couldn't connect to server; continuing without syncing.`，結束碼 0，HEAD 不變；不存在路徑時為 `… fatal: Could not read from remote repository.; continuing without syncing.`
- **結論**：可用。

### 5. When the sync brings in new content, the complete package suite and the adversarial programs run and pass on the synced content before any reviewer is dispatched.
- **我怎麼試的**：沿用第 1 條的情境。同步後照指令與審查站說明的順序，在帶進 main 的內容上先跑測試，再往下走。
- **發生了什麼**：同步指令在內容有變時明確要求「派審查前先重跑整套測試與對抗程式」；審查站的說明也寫明這時不派審查人、回到實作階段重跑、全部通過後才重新開始第一輪；實作階段本身也在跑測試之前就先同步，所以一般情況只需跑一次。我的替代測試在同步後的內容上跑過並通過。
- **證據**：輸出 `sync-trunk: content changed -- re-run the package suite and adversarial programs before dispatching reviewers.`；替代測試輸出 `suite: ok`、結束碼 0；再次同步回報 up to date。
- **結論**：部分可用 — 停下並要求重跑的訊號是真的。但真正的整套測試和對抗程式，要在一次完整、有審查人參與的審查流程中才會跑；我沒有跑那樣的流程，所以「真的有照做」這件事還沒被實際看到。

## 審查摘要

還沒有審查紀錄 — 這份盲跑報告是在派審查人之前寫的，所以沒有審查意見，也沒有被駁回的重要意見交給我。

## 我問過你的問題

- 開始前我把這項變更覆述給你確認，包含審查通過後會自動推送並開成 Ready 的 PR、合併另外再問你 — 你回「OK」。
- 連不上 GitHub 時要停下不審，還是警告後照審 — 你選「Ｂ」（警告後照審）。第 4 條就是照這個答案做的。

## 對你既有的資料做了什麼

不會碰到你已經有的東西，只會在你的功能分支上多加一筆合併紀錄。我在乾淨環境裡看到的行為是：能乾淨合併時，只在功能分支上多一筆「把 main 合併進來」的紀錄，舊的歷史不會被改寫，所以已經推上去的分支不用強制覆蓋；main 本身和你另開的 main 工作副本完全沒被動到；衝突、連不上遠端、或工作資料夾有未提交／未追蹤檔案時，什麼都不改，連那些檔案也原封不動。如果你不想要那筆合併，可以用一般的 git 操作退回合併前的位置，指令輸出裡有合併前後的位置可以對照。

## 我替你決定的事

- **用「合併」而不是「重新整理歷史（rebase）」把 main 帶進來** — 選合併是因為已推上去的分支歷史不會被改寫。代價是分支上會多一筆合併紀錄；之後想改成 rebase，要改指令本身並重新審查。
- **實作階段結束前先同步一次，審查開始前再確認一次** — 這樣一般情況下測試只需跑一次；如果審查前又有新內容進來，就退回實作階段再跑一次。之後想拿掉其中一次，要改兩個階段的說明。
- **版本號訂為 3.6.0** — 另一條分支也打算用 3.6.0，哪條晚合併，哪條就要改版本號。
- **我在盲跑中自己決定的**：沒辦法照說明從 GitHub 安裝外掛（要碰到真正的遠端，這次不允許），所以直接從乾淨副本執行指令。另外我用一個簡單的替代測試代替整套測試（原因見第 5 條）。

## 我不確定你要不要的地方

- 工作資料夾有未提交或未追蹤的檔案、同時又會衝突時，第一次只會叫你先清理，第二次才列出衝突檔。這樣可以接受嗎？

## 英文規則與格式規則是否守住

| 文件 | 英文規則 | 其他格式規則 | 證據 |
|---|---|---|---|
| 計畫 | 守住（唯一的中文是你原話的引用） | 不適用 | `plan.md` 僅 1 行 CJK：`kouko: "Ｂ"` 那題 |
| 規格 | 不適用 — 這次不需要規格 | 不適用 — 規格才需要用 REQ 編號寫需求 | `needs-design: no` |
| 審查意見 | 還沒有 | 還沒有 — 審查意見才需要加標籤 | 尚無審查紀錄 |
| 證據 | 守住（唯一的中文是故意拿來測非英文檔名的測試資料） | 不適用 | `evidence/probes/test_sync_trunk_abuse.py` 兩行 `資料.txt` |
| 測試說明文字 | 守住 | 不適用 | 新增行掃描：除上述測試資料外無 CJK |
| 測試名稱 | 守住 | 大致守住：每個名稱都分成「測的對象／情境／預期結果」三段，但有幾個讀起來像一句話 | 例：`test_the_rule_population_is_twenty_five`、`test_no_op_sync_dispatches_without_rerun` |
| commit 訊息 | 守住 | 不適用 | `9906c79c..726891d` 共 8 筆，無 CJK |
