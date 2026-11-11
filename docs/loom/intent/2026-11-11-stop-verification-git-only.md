# Ordinary added files must not trigger test collection when a review record is rechecked
originator: kouko
kind: engineering
needs-design: no — 變更修正既有 checker 內部函式的執行路徑並補測試；hook 與 checker 不是本 repo 的介面表面
evidence: [docs/loom/2026-11-11-stop-verification-git-only/evidence/codex-review-leg3.md, docs/loom/2026-11-11-stop-verification-git-only/evidence/hook-reproduction.md, loom-code/scripts/loom_checker/probes.py]
status: confirmed 2026-11-11
intent_confirmed_sha: bddf642e4d67515a47fdcdf5c9769971c8d1f6e8
publication: automatic — authorized 2026-11-11 by kouko

## Problem
delivery Stop hook 在變更通過審查後，每個回合結束都重算一次審查紀錄（attestation）是否仍有效，並宣稱這個重算不重試、不寫入。實測（2026-11-11，loom-code 3.65.0）顯示有一種情況不是如此：審查紀錄記著「對抗階段沒有產出程式」（no_program）且分支新增了程式檔時，重算會為每個新增的程式檔啟動一次 `python3 -m pytest --collect-only` 子程序並建立一個暫存目錄，之後才發現那些檔案不算對抗程式。3 個新增檔案就是 3 次子程序、3 個暫存目錄；新增檔案越多，hook 越接近它的 20 秒上限，超過時使用者會看到「無法確認交付」的訊息。同一段重算不經 hook 直接呼叫時，子程序會成功執行並載入 repo 的測試設定。

## Proposed outcome
分支新增的一般程式檔（不帶 `concern:` 行，也就是不自稱對抗程式的檔案）不再讓審查紀錄有效性的重算啟動 git 以外的子程序或建立暫存目錄；這種情況下重算只讀取 git 內容，不再為每個新增檔案啟動測試收集；每個新增的程式檔仍有一次 git 讀取。重算的答案（valid／absent／stale）與對抗程式數量上限的判定都和現在相同。

## Acceptance
1. 審查紀錄有效、記著 no_program、且分支新增了不帶 `concern:` 行的程式檔時，觸發 Stop hook：過程中不啟動任何 git 以外的子程序、不建立任何暫存目錄，hook 輸出的提醒與修正前相同。
2. 同一情境下直接重算審查紀錄有效性：同樣不啟動 git 以外的子程序、不建立暫存目錄，結果仍為 valid。
3. 分支新增了帶 `concern:` 行、且會被套件測試收集的對抗程式時，no_program 的審查紀錄仍被判為 stale（與已存在的程式矛盾），與修正前相同。
4. 對抗程式數量上限的既有判定不變：既有的上限與畢業（graduated）程式測試全數通過，未修改其斷言。

## Constraints
- 修改限於 `loom-code/scripts/loom_checker/probes.py`、必要時其呼叫端，以及測試。
- 不改 attestation 格式、審查者規則、對抗程式數量上限的門檻。
- 保留 Stop hook 既有屬性：永遠 exit 0、單一 20 秒上限、不寫入。

## Out of scope
- #141 的提醒文字、主機別輸出格式與觸發條件。
- finalize-review 執行套件測試與對抗程式時的收集行為。
- OpenCode／Antigravity（沒有 Stop hook）。

## Open questions
- none
