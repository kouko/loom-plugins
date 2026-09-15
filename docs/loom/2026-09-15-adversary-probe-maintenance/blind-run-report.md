# 讓對抗檢查自己跟上範圍變化、先沿用既有測試 — 我試了什麼、發生了什麼

試跑日期 2026-09-16，在專案的乾淨副本（4d55f1d2）上進行；實際演練在暫存區裡全新建立的一次性練習專案裡做，沒有動到你的專案內容。

**歷史**：第一次試跑（78467a58）第 3 條沒達成——對抗 agent 用「丟棄未提交修改」的指令還原突變，被本機安全檢查擋下，要求使用者親手執行。之後說明補上「在一次性副本上跑突變，或用編輯工具還原，禁用丟棄指令」，這份報告是補完後的重跑。

## 總結

- 五條都可以用了。
- 第 3 條這次走完全程：對抗 agent 自己判斷是範圍變化、自己更新並提交檢查、自己在一次性副本上跑了五個突變，每個都讓檢查變紅；沒有任何指令被安全檢查擋下，你不需要動手。
- 負面情境（產品真的壞了）仍然正確：檢查沒被改，回報產品缺陷。

## 你要的東西，一條一條

### 1. The build station's instructions say what happens when a committed adversarial program no longer fits the widened scope: the adversary is dispatched again to update its own probes, and no other role edits them.
- **我怎麼試**：讀建置站第 3、4 節，確認有寫：範圍擴大（或同步主線帶進的內容）讓對抗檢查不再適用時重新派對抗 agent；只有它能改自己的檢查，實作者與協調者不能改；一般修正後仍不再派。接著在練習專案裡照這段規則當一次建置站，把規則列出的輸入交給全新的對抗 agent。再跑釘住這些句子的測試。
- **發生了什麼**：照規則做沒有卡住；練習中對抗 agent 只動了自己的檢查檔，產品程式和實作者的測試一行都沒改。測試全部通過。
- **證據**：`python3 -m pytest -q -p no:cacheprovider loom-code/scripts/test_build_mechanical_checks.py` → `85 passed`（exit 0）；練習專案 `git diff 315f08a HEAD -- datefmt.py test_datefmt.py` → 0 行。
- **判定**：可以用。

### 2. The adversary's instructions require every probe update to come with mutation evidence run against the committed probe itself, with at least one mutation per kind of change the update touches, including one that an over-broad update would wrongly accept.
- **我怎麼試**：讀對抗 agent 的角色說明與對抗檢查的做法說明，確認都要求：突變驗證跑在已提交的那支檢查本身；每種修改至少一個突變；一個「過度放寬也會通過」的突變；一個「還原成原本被拒絕的行為」的突變；每個都要變紅再還原並回報指令與結果。這次新增的部分也確認了：突變要在一次性的工作樹副本裡做（暫時的工作樹或匯出的副本），檢查原封不動地在那裡跑，或用編輯工具套上再還原；明文禁止用丟棄修改的指令還原。
- **發生了什麼**：兩份說明一致、條件清楚；練習中的對抗 agent 照做，沒有再踩到第一次的坑。
- **證據**：同上 `85 passed`；練習回報中的突變表（M1–M5，方法為匯出副本）。
- **判定**：可以用。

### 3. In a trial change whose scope is widened after the adversary ran, the stale probe is updated and passes, and the change reaches closing review without the maintainer running or committing any probe file by hand.
- **我怎麼試**：
  1. 在暫存區用新名字全新建一個練習專案（沒有沿用第一次的專案）：解析日期的函式只接受 `2026-09-16`、它的單元測試、一支寫著「`2026/09/16` 必須被拒絕」的對抗檢查。
  2. 模擬建置擴大範圍：函式改成也接受 `2026/09/16`。檢查因範圍變化而變紅（`1 failed, 5 passed`，失敗的正是 `2026/09/16`）。
  3. 照建置站第 3 節派全新的對抗 agent，只給變更代號、HEAD、意圖與計畫、擴大範圍的檔案、失敗輸出，並告訴它分支上的角色說明為準。
  4. 它回來後：在全新複製裡重跑更新後的檢查；在它留下的五份突變副本裡重跑一次；再自己匯出一份副本，重套它的「過度放寬」突變，確認變紅、用編輯工具還原後變綠。
  5. 負面情境：另一份副本改成真正的缺陷（原本格式被弄壞、錯收 `2026.09.16`），同樣方式派對抗 agent。
- **發生了什麼**：
  - (a) **更新後會通過**：對抗 agent 把「斜線日期必須被拒絕」翻成「斜線日期必須解析成功」（沒有刪），保留原本被拒絕的格式並加一種，另補混合分隔符、格式不完整的斜線日期、斜線格式的不可能日期，自己提交。全新複製重跑 `13 passed`。它另開一支檢查抓到真的產品缺陷（全形或阿拉伯數字的日期會被接受），這支目前是紅的，是正常的缺陷回報，放在另一個檔案，所以不影響突變驗證。
  - (b) **對抗 agent 自己的突變驗證有跑，而且都變紅**：
    | 突變 | 內容 | 結果（它回報，我在它的副本重跑一致） |
    |---|---|---|
    | 還原原行為 | 拿掉斜線格式 | 紅：1 failed, 12 passed |
    | 過度放寬 | 分隔符接受任何非數字字元 | 紅：3 failed, 10 passed |
    | 混合分隔符 | 分隔符 `-` 或 `/` 任意混用 | 紅：2 failed, 11 passed |
    | 格式不完整 | 允許一位數月日、重複斜線 | 紅：3 failed, 10 passed |
    | 不可能日期 | 日期大於 28 自動改成 28 | 紅：1 failed, 12 passed |
    每份副本裡的檢查檔都和已提交的一模一樣；突變只存在於副本，原本的練習專案從沒被改過。我自己另匯出一份副本重套「過度放寬」：紅（3 failed, 10 passed），用編輯工具還原後綠（13 passed）。
  - (c) **沒有被擋、你不用動手**：對抗 agent 明確回報沒有任何指令、提交或權限提示被拒；沒用丟棄指令。更新提交是它自己做的（提交者名稱沿用本機 git 設定）。這次的練習變更仍會因為那支新的缺陷檢查是紅的而先回建置站修產品，這是正確行為；在「檢查過時」這件事上，已經不需要你手動跑或提交任何東西。
  - **負面情境正確**：產品真壞時，檢查檔差異 0 行、沒有新提交、工作區乾淨；對抗 agent 回報一個致命缺陷（`2026-09-16` 和 `2026/09/16` 都被拒、`2026.09.16` 被錯收），並說明產品修好後斜線那格會過時，屆時再派它翻成「修改」。沒有被擋。
- **證據**：
  - 擴大前失敗：`python3 -m pytest -q -p no:cacheprovider docs/loom/2026-09-16-date-formats/evidence/probes/test_datefmt_abuse.py` → `FAILED ...[2026/09/16]`，`1 failed, 5 passed`
  - 更新提交 `1bb64eb`：只動 `test_datefmt_abuse.py`（+32/−3）與新檔 `test_datefmt_digits.py`
  - 全新複製重跑同一指令 → `13 passed`（exit 0）；`test_datefmt_digits.py` → `2 failed`（缺陷回報）
  - 突變副本（`git archive 1bb64eb` 匯出）各跑同一指令 → M1–M5 皆 exit 1，數字如上表
  - 我重套的過度放寬突變 → `3 failed, 10 passed`；還原後 `13 passed`
  - 負面情境：`git diff 66ad028 HEAD -- docs/loom/2026-09-16-date-formats/evidence/probes/` → 0 行，`git log` 停在 `bf6f6fc`
  - 暫存區紀錄檔（不在專案內）：`blindrun-probe-maintenance/` 下的 `r2-trial-widen-probe-before.log`、`r2-trial-widen-verify.log`、`r2-blindrunner-m2-red.log`、`r2-blindrunner-m2-green.log`、`r2-trial-defect-after.log`
- **判定**：可以用。

### 4. Before writing probes, the adversary checks this change's existing probes and the repository's related tests, and its report marks each probe as reused, modified, or new, with a reason for every new one.
- **我怎麼試**：讀兩份說明，確認要求先查既有檢查與相關測試、逐項標「沿用／修改／新增」、新增附理由、分支上別人加的測試只算相關涵蓋；這次新增「翻轉或改寫舊情境算修改」。再看兩份練習回報。
- **發生了什麼**：兩份回報都逐項標了狀態，每個新增都有理由；實作者的測試被列為「只是相關涵蓋、不算門檻」。第一次試跑的小瑕疵已解決：翻轉而來的斜線情境這次標成「修改」。
- **證據**：`85 passed`；練習回報 `probes` 清單中 `test_parse_date_slash_format_returns_date` 標 `modified`。
- **判定**：可以用。

### 5. The repository's existing package test suite passes.
- **我怎麼試**：在 4d55f1d2 的乾淨副本跑完整套件，再跑這個變更自己提交的對抗檢查。
- **發生了什麼**：完整套件結束代碼 0，紀錄沒有任何失敗；對抗檢查全部通過。
- **證據**：`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` → exit 0（例：`1865 passed, 2 skipped`、`238 passed, 1 skipped`）；`python3 -m pytest -q -p no:cacheprovider docs/loom/2026-09-15-adversary-probe-maintenance/evidence/probes/test_probe_maintenance_abuse.py` → `16 passed`（exit 0）。
- **判定**：可以用。

## 審查摘要

重跑時這個變更還沒有收尾審查紀錄，審查站也沒交給我被駁回的發現。第一次試跑提出的兩點都已處理並在重跑中確認：

- **重要（已解決）**：說明沒寫怎麼還原突變，導致被安全檢查擋。現在寫明用一次性副本或編輯工具、禁用丟棄指令；重跑沒有被擋。
- **小瑕疵（已解決）**：翻轉的舊情境被標成「新增」。現在說明寫明算「修改」，練習回報也照做。

這次沒有新發現。

## 我問過你的問題

以下出自這個變更的計畫紀錄：

- 範圍擴大後由對抗 agent 自己更新檢查並附正式突變證據；寫之前先查既有檢查與測試、逐項標沿用／修改／新增；本機暫存專案實跑驗證；授權自動推送開 PR、合併前回「接受」——這樣對嗎？
- 這些修改實際有哪些？以及「最新模型少寫提示效果更好」的看法？（你的追問）
- 要不要加「規則文件總字數不增加」和「新句子不用強烈字眼」兩條限制？你的回答：先不用，等這批做完再一次整理。

## 對你既有的資料做了什麼

沒有。這個變更只改了建置站和對抗 agent 的說明文字與它們的測試，不讀也不寫你已經有的任何資料。練習專案都在暫存區，沒有寫進你的專案；專案本身只多了這份報告。

## 我替你決定的事

- **只為「範圍變了」重新派對抗 agent** — 計畫選了一個例外：只有因範圍變化而失敗或跑不起來的檢查才重新派，一般修正後仍不再派，避免無限回圈。之後想放寬要改建置站規則與對應測試。
- **例外也涵蓋同步主線帶進的內容；產品真壞時檢查保持不動、回報缺陷；實作者對這支變更的對抗檢查只能讀** — 計畫第二輪補上。
- **突變一律在一次性副本上跑或用編輯工具還原，禁用丟棄指令** — 計畫第三輪（針對第一次試跑的發現）決定；代價是突變副本會留在暫存區，要自己清。
- **不設字數上限、不限制強烈字眼** — 你決定的（2026-09-16），留到之後整體整理。
- **練習專案的設計（試跑者決定）** — 「日期格式從一種擴成兩種」當範圍擴大，「原格式被弄壞、錯收點號日期」當負面情境；換例子不影響結論。
- **被駁回的重要發現** — 沒有。

## 我不確定你要不要的事

- 對抗 agent 留在暫存區的突變副本不會自動清掉，你要不要之後在說明裡規定用完就移除？

## 各份文件的英文規則有沒有守住

| 文件 | 英文規則 | 同時適用的格式規則 | 證據 |
|---|---|---|---|
| 計畫 | 大致守住：內容英文，只有「問過你的問題」一節照原話保留中文 | — | `plan.md` 第 34–36 行 |
| 規格 | 不適用：這個變更不需要規格 | 需求句格式：不適用 | 意圖 `needs-design: no` |
| 審查紀錄的發現 | 尚無審查紀錄 | 標註格式：無從檢查 | — |
| 證據 | 守住：對抗檢查的說明是英文 | — | `test_probe_maintenance_abuse.py` 開頭說明 |
| 測試說明文字 | 守住：看到的都是英文；新增的建置站測試首行沒有說明文字 | — | `test_build_mechanical_checks.py` 新增函式 |
| 測試名稱 | 守住（英文） | 三段式命名大致守住；幾個輔助自我測試名稱（如 `*_helpers_synthetic`）第三段不像「預期行為」 | `test_stale_program_redispatch_helpers_synthetic`、`test_adversary_update_defect_relabelled_stale_kept_red` |
| 提交訊息 | 守住：分支上的提交都是英文 | — | `git log main..HEAD` |
