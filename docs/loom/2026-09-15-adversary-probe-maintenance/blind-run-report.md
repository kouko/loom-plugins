# 讓對抗檢查自己跟上範圍變化、先沿用既有測試 — 我試了什麼、發生了什麼

試跑日期 2026-09-16，在專案的乾淨副本（78467a58）上進行；實際演練在一個一次性的小型練習專案裡做，沒有動到你的專案內容。

## 總結

- 規則文字（第 1、2、4 條）寫得清楚，兩位被派出的對抗 agent 都照著做了。
- 第 3 條**還沒達成**：對抗 agent 自己更新並提交了過時的檢查，但在跑「證明沒被放鬆」的突變驗證時，被本機的安全檢查擋下，理由是它用了會丟棄未提交修改的還原指令。安全檢查的訊息要求「請使用者親手執行」——這正是這次變更想消除的情況。
- 負面情境（產品真的壞了）表現正確：對抗 agent 沒改檢查，回報了產品缺陷。
- 第 5 條：整套既有測試全部通過。

## 你要的東西，一條一條

### 1. The build station's instructions say what happens when a committed adversarial program no longer fits the widened scope: the adversary is dispatched again to update its own probes, and no other role edits them.
- **我怎麼試**：讀了建置站的第 3、4 節，確認三件事都有寫：範圍擴大（或同步主線帶進的內容）讓對抗檢查不再適用時，重新派對抗 agent；只有它能改自己的檢查，實作者和協調者都不能改；「一般修正後不要再派」的舊規則仍保留。接著在練習專案裡照這段規則當一次建置站，實際派出對抗 agent，給它的就是規則列出的那幾樣輸入。另外跑了釘住這些句子的測試檔。
- **發生了什麼**：規則寫得夠清楚，照做沒有卡住；練習中對抗 agent 也只改了自己的檢查，產品程式碼和實作者的測試一行都沒動。釘住句子的測試全部通過。
- **證據**：`python3 -m pytest -q -p no:cacheprovider loom-code/scripts/test_build_mechanical_checks.py` → `71 passed`（exit 0）；練習專案中產品檔與實作者測試在更新前後的差異為 0 行（`git diff 8a2ae48 HEAD -- datefmt.py test_datefmt.py`）。
- **判定**：可以用 — 規則明確，且實際派一次行得通。

### 2. The adversary's instructions require every probe update to come with mutation evidence run against the committed probe itself, with at least one mutation per kind of change the update touches, including one that an over-broad update would wrongly accept.
- **我怎麼試**：讀對抗 agent 的角色說明和對抗檢查的做法說明，確認都要求：突變驗證要跑在「已提交的那支檢查程式本身」上（複製一份邏輯不算）、每種修改至少一個突變、一個「過度放寬也會通過」的突變、一個「還原成原本被拒絕的行為」的突變；每個突變都必須讓檢查變紅、再還原，並回報指令與結果。
- **發生了什麼**：兩份說明寫法一致，條件都講清楚。練習中對抗 agent 也照著規劃出四個突變（還原原行為、過度放寬、混合分隔符、不可能的日期），而且知道證據沒跑完時更新「不算有證據」，並主動回報成一個缺口。**但說明沒講怎麼還原突變**；它選了會丟棄未提交修改的還原指令，於是在第 3 條被擋（見下）。
- **證據**：釘住句子的測試同上 `71 passed`；練習中對抗 agent 回報的突變表（M1–M4）與發現「evidence gap (update unverified)」。
- **判定**：可以用（就「說明有寫出要求」而言）— 但缺一句「怎麼還原突變」，這一點直接導致第 3 條失敗。

### 3. In a trial change whose scope is widened after the adversary ran, the stale probe is updated and passes, and the change reaches closing review without the maintainer running or committing any probe file by hand.
- **我怎麼試**：
  1. 在暫存區建了一個小練習專案：一個解析日期的函式（原本只接受 `2026-09-16` 這種格式）、它的單元測試、以及一支對抗檢查，裡面明確寫著「`2026/09/16` 必須被拒絕」。
  2. 模擬建置擴大範圍：把函式改成也接受 `2026/09/16`。對抗檢查因此變紅，原因是範圍變了，不是有 bug（`1 failed, 5 passed`，失敗的正是 `2026/09/16` 那一格）。
  3. 照建置站第 3 節，派一個全新的對抗 agent，只給變更代號、HEAD、意圖與計畫的路徑、擴大範圍的檔案、失敗輸出，並告訴它以分支上的角色說明為準。
  4. 它回來後，我在另一份全新複製裡重跑它更新後的檢查，再親手把突變一個個套上去、確認變紅、還原、確認變綠。
  5. 負面情境：另開一份副本，改成真正的缺陷（原本的 `2026-09-16` 格式被弄壞、改成接受 `2026.09.16`），用同樣方式派對抗 agent。
- **發生了什麼**：
  - (a) **更新有做、有提交、會通過**：對抗 agent 判斷這是範圍變化，自己改了檢查——把「斜線日期必須被拒絕」翻成「斜線日期必須解析成功」（沒有刪掉），並補了混合分隔符、雙斜線、反斜線、斜線格式的不可能日期等情境，自己提交。我在全新複製裡重跑：`11 passed`。它另外新增了一支檢查，抓到一個真的產品缺陷（全形或阿拉伯數字的日期會被接受），這支目前是紅的，屬正常的缺陷回報。
  - (b) **突變證據沒有由對抗 agent 產出**：它要還原第一個突變時，被本機安全檢查擋下，原文如下：
    ```
    BLOCKED by dcg
    Reason: git checkout -- discards uncommitted changes permanently. Use 'git stash' first.
    Rule: core.git:checkout-discard
    If this operation is truly needed, ask the user for explicit permission and have them run the command manually.
    ```
    被擋的是一整串指令（含跑檢查），所以第一個突變連檢查都沒跑到；它照指示停下，用編輯工具把突變還原，工作區乾淨，另外三個突變沒跑。它回報需要「由你親手執行還原指令」或「由建置站核准改用編輯工具還原」才能補完。
    我自己的量測（不算對抗 agent 的證據，只是看這支更新後的檢查有沒有被放鬆）：在三份副本上用編輯工具套突變，都會變紅，還原後都變回綠。
    | 突變 | 內容 | 套上後 | 還原後 |
    |---|---|---|---|
    | 還原原行為 | 拿掉斜線格式支援 | 紅（1 failed） | 綠（11 passed） |
    | 過度放寬 | 分隔符接受 `-`、`/`、`.` 任一 | 紅（3 failed） | 綠（11 passed） |
    | 混合分隔符 | 分隔符接受 `-` 或 `/` 任意混用 | 紅（2 failed） | 綠（11 passed） |
  - (c) **不需要你動手？沒有做到**：更新和提交本身不需要你，但突變證據要走完，照目前的安全檢查訊息就得請你親手執行或另外授權。依這次試跑的規則，安全檢查擋下對抗 agent 的指令＝這條失敗，我沒有繞路。另外，新增的那支缺陷檢查是紅的，建置站本來就要先修產品，所以這個練習變更本來也還到不了收尾審查——這是正確行為，不算這條的失敗原因。
  - **負面情境正確**：產品真壞時，對抗 agent 沒有改檢查（檢查檔差異 0 行、沒有新提交、工作區乾淨），回報一個致命缺陷，指出 `2026-09-16` 被弄壞、`2026.09.16` 被錯收，並說明「等產品修好後，斜線那格會過時，那時再派我更新」。
- **證據**：
  - 擴大前失敗輸出：`python3 -m pytest -q -p no:cacheprovider docs/loom/2026-09-16-date-formats/evidence/probes/test_datefmt_abuse.py` → `FAILED ...test_parse_date_non_iso_format_raises[2026/09/16]`，`1 failed, 5 passed`
  - 對抗 agent 的更新提交 `84ad58f`（作者 adversary），只動兩支檢查檔：`test_datefmt_abuse.py`（+29/−3）、`test_datefmt_unicode_digits.py`（新檔）
  - 全新複製重跑：同上指令 → `11 passed`（exit 0）；`test_datefmt_unicode_digits.py` → `3 failed`（exit 1，缺陷回報）
  - 我自己的突變量測：每份副本各跑同一指令，紅／綠結果如上表
  - 負面情境：`git diff a63eb80 HEAD -- docs/loom/2026-09-16-date-formats/evidence/probes/` → 0 行；`git log` 仍停在 `926ebad`
  - 暫存區紀錄檔（不在專案內，會隨暫存區清除）：`blindrun-probe-maintenance/` 下的 `trial-widen-probe-before.log`、`trial-widen-clean-rerun.log`、`trial-widen-mutants-red.log`、`trial-widen-mutants-reverted.log`、`trial-defect-after.log`
- **判定**：還沒 — 檢查有自己更新、也沒被放鬆，但必要的突變證據被安全檢查擋下，要補完就得請你親手操作。

### 4. Before writing probes, the adversary checks this change's existing probes and the repository's related tests, and its report marks each probe as reused, modified, or new, with a reason for every new one.
- **我怎麼試**：讀對抗 agent 的角色說明和對抗檢查的做法說明，確認都要求：先看這個變更既有的檢查和專案相關測試；能沿用就沿用、小改能涵蓋就修改、真的沒有才新增；回報逐項標「沿用／修改／新增」，每個新增附一行理由；這個分支上別人加的測試（例如實作者的測試）只能列為相關涵蓋，不能算進「至少三個情境」的門檻。再看兩位練習中的對抗 agent 回報有沒有照做。
- **發生了什麼**：兩份回報都逐項標了狀態，新增的都有理由；擴大範圍那一位把實作者新加的斜線測試標成「只是相關涵蓋，不算門檻」，符合規則。小瑕疵：它把「斜線日期必須解析成功」標成「新增」，其實是從舊檢查翻過來的那一格，標「修改」比較貼切——不影響判定。
- **證據**：釘住句子的測試 `71 passed`（含標註格式相關的測試）；兩份練習回報的 `probes` 清單。
- **判定**：可以用。

### 5. The repository's existing package test suite passes.
- **我怎麼試**：在乾淨副本跑一次完整套件，再跑這個變更自己提交的對抗檢查。
- **發生了什麼**：完整套件結束代碼 0，紀錄裡沒有任何失敗；這個變更的對抗檢查全部通過。
- **證據**：`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` → exit 0（例：`1851 passed, 2 skipped`、`238 passed, 1 skipped`，各段 `Summary: N PASS / 0 FAIL`）；`python3 -m pytest -q -p no:cacheprovider docs/loom/2026-09-15-adversary-probe-maintenance/evidence/probes/test_probe_maintenance_abuse.py` → `16 passed`（exit 0）。
- **判定**：可以用。

## 審查摘要

試跑時這個變更還沒有收尾審查的紀錄，審查站也沒有交給我任何被駁回的發現。以下是這次試跑自己得出的問題：

- **重要**：對抗 agent 的說明要求每個突變「套上、變紅、再還原」，卻沒說怎麼還原。最順手的還原方式（丟棄未提交修改）會被本機安全檢查擋，擋下時訊息要求使用者親手執行，第 3 條因此失敗。要補的是：說明裡寫明「用編輯工具還原突變，或在一次性的副本上套突變，不要用丟棄修改的指令」，然後重跑一次第 3 條的練習。
- **小瑕疵**：把舊檢查翻轉而成的一格被標成「新增」而不是「修改」；說明裡可以舉一個「翻轉舊情境＝修改」的例子。

## 我問過你的問題

以下出自這個變更的計畫紀錄：

- 範圍擴大後由對抗 agent 自己更新檢查並附正式突變證據；寫之前先查既有檢查與測試、逐項標沿用／修改／新增；本機暫存專案實跑驗證；授權自動推送開 PR、合併前回「接受」——這樣對嗎？
- 這些修改實際有哪些？以及「最新模型少寫提示效果更好」的看法？（你的追問）
- 要不要加「規則文件總字數不增加」和「新句子不用強烈字眼」兩條限制？你的回答：先不用，等這批做完再一次整理。

## 對你既有的資料做了什麼

沒有。這個變更只改了建置站和對抗 agent 的說明文字與它們的測試，不讀也不寫你已經有的任何資料。試跑用的練習專案都放在暫存區，沒有寫進你的專案；專案本身只多了這份報告。

## 我替你決定的事

- **兩次重新派遣的時機（不再派 vs. 範圍變了才再派）** — 計畫選了只開一個例外：只有「因範圍變化而失敗或跑不起來」的檢查才重新派，一般修正後仍不再派，避免無限回圈。之後想放寬，要改建置站規則和對應測試。
- **例外也涵蓋「同步主線帶進的內容」** — 計畫第二輪補上的；產品真壞時檢查保持不動、回報缺陷；這支變更自己的對抗檢查，實作者只能讀不能改。
- **不設字數上限、不限制強烈字眼** — 這是你決定的（2026-09-16），留到之後整體整理。
- **練習專案的設計（試跑者決定）** — 我選了「日期格式從一種擴成兩種」當範圍擴大的例子，負面情境選了「原格式被弄壞、錯收點號日期」。換別的例子不影響結論。
- **我用編輯工具在獨立副本上自己量了突變** — 目的是量測更新後的檢查有沒有被放鬆，不是替對抗 agent 補證據；它的證據仍算缺。
- **被駁回的重要發現** — 沒有；審查站沒有交給我任何駁回紀錄。

## 我不確定你要不要的事

- 突變的還原方式，你希望寫進對抗 agent 的說明（用編輯工具或在副本上做），還是希望調整本機安全檢查的規則？後者在這次變更的範圍外。
- 補上還原方式之後，要不要我再跑一次第 3 條的練習，才算這條通過？

## 各份文件的英文規則有沒有守住

| 文件 | 英文規則 | 同時適用的格式規則 | 證據 |
|---|---|---|---|
| 計畫 | 大致守住：內容是英文，只有「問過你的問題」一節照原話保留中文 | — | `plan.md` 第 34–36 行 |
| 規格 | 不適用：這個變更不需要規格 | 需求句格式：不適用 | 意圖 `needs-design: no` |
| 審查紀錄的發現 | 尚無審查紀錄 | 標註格式：無從檢查 | — |
| 證據 | 守住：對抗檢查的說明是英文 | — | `test_probe_maintenance_abuse.py` 開頭說明 |
| 測試說明文字 | 守住：看到的都是英文；新增的建置站測試首行沒有說明文字 | — | `test_build_mechanical_checks.py` 新增函式 |
| 測試名稱 | 守住（英文） | 三段式命名大致守住；幾個輔助自我測試的名稱（如 `*_helpers_synthetic`）第三段不像「預期行為」 | `test_stale_program_redispatch_helpers_synthetic`、`test_adversary_update_defect_relabelled_stale_kept_red` |
| 提交訊息 | 守住：七筆都是英文 | — | `git log main..HEAD` |
