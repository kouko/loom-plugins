# LLM reviewer 逐句比對規則方向
originator: kouko
kind: engineering
needs-design: no — 只改 closing review 的審查規範文字與版號，不觸及任何介面表面（manifest globs 之外）
evidence: [docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/census-report.md]
status: confirmed 2026-09-29
publication: automatic — authorized 2026-09-29 by kouko

## Problem
第一到四批清理把許多「規則方向」的檢查（例如「絕不擋下」「不可自動執行」「禁止引用」）從固定測試移給 closing review 的 LLM reviewer。但 reviewer 讀的是整份 diff：一條規則只改了幾個字就被寫反、文件其餘部分都對時，最容易被漏看，而結果是 agent 照著相反的規則做事。這種寫反過去真的發生過（壓縮文字時把規則方向弄反）。

## Proposed outcome
LLM reviewer 在審 skill 與文件時，凡是 diff 刪掉或改寫了帶有方向字眼（never、must not、only、always、不得、禁止、絕不等）的句子，就拿舊版逐句比對，方向被反轉或被刪掉時提出發現。這條檢查是通用的，不靠逐條列出的規則清單，以後新寫的規則也涵蓋。三個 plugin 升 patch 版號。

## Acceptance
1. closing review 的 skill 與 docs 審查規範寫明：diff 刪掉或改寫帶方向字眼的句子時，reviewer 要對照舊版逐句比對，方向被反轉或刪掉即為發現。
2. 一位沒看過這個變更的 reviewer 拿到一份 diff，其中在大量無關改動裡藏了一句被寫反的規則，會照規範把它報出來；拿到一份只換說法、方向不變的 diff，不會報方向問題。
3. 這條檢查不依賴任何逐條列出的規則或 skill 清單。
4. 三個 plugin 的版號各升一個 patch，三份 manifest、CHANGELOG、README 與版號 pin 測試一致，版號一致性測試通過。

## Constraints
- 沿用 2026-09-27-prose-evidence-class 的證據政策：不新增比對散文措辭的測試；結構檢查可以。
- 不新增 checker 規則；機制總數不增加。
- 只動審查規範、必要的最小結構測試、證據檔與版號相關檔；不修改其他 skill／agent／reference 散文。
- 版號必須在 closing review 的 finalize 之前 commit。

## Out of scope
- 為個別規則加 gate 標記或固定的方向測試（選項 B）。
- 逐條列出的必查規則清單（選項 A）。
- 恢復第一到四批刪掉的檢查。
- 回頭檢查已合併歷史中是否已有規則被寫反。

## Open questions
- none
