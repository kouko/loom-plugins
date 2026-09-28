# 清理散文釘住測試存量 — plan
intent: 2026-09-27-prose-pin-stock-cleanup@6f3acd78
charter: 1.1

## Current State Evidence
- Forward: `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py` — 普查腳本定稿（W0-01 完成，五輪修正）：238 檔全樹掃描，13 sentence-pin / 5 grammar-invariant / 41 structure / 111 behavior / 58 not-prose / 10 other。
- Reverse: `docs/loom/intent/2026-09-27-prose-evidence-class.md` — 證據政策已確立：prose 合格證據 = checker 重算 + fresh-context 審查 + 行為變更時的 AT；字面感應測試只留文法級不變量。
- Error: 最終分類已逐檔 cold-read 覆核；誤判（delivery_binding、skill_contract、prose_pin_rule_text）已修復。
- Data: 13 檔 sentence-pin 中，僅 `test_module_criteria_text` 被外部執行（test_adversary_routing SUITE_EXTRA）與 SSOT 引用（AGENTS.md:54）；其餘 12 檔僅名字提及（註解/測試名），可整檔刪。
- Boundary: `test_acceptance_test_report_shape`、`test_lenses_deletion_first`、`test_prose_pin_rule_text`、`test_reviewer_mechanical_evidence`、`test_write_plan_shape_text` = grammar-invariant（保留）。

## Task DAG

### Wave 0 — 普查腳本與分類基準

**W0-01 普查腳本定稿與驗證**  after: —  acceptance: 1
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A1 positive: script-classifies-pure-pin-as-sentence-pin; negative: behavior-file-not-misclassified-as-pin.
- Risk: 分類是 contract surface，reviewer 需冷讀驗證每檔分類與「結構 vs 釘住」邊界；agent-decided。DONE（五輪修正）。

**W0-02 耦合清單**  after: W0-01  acceptance: 1
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A1 positive: protocol-module-coupling-listed; negative: no-coupling-file-not-listed.
- Risk: 列出每檔被誰 import／引用；決定每檔刪除或保留的依賴；agent-decided。

### Wave 1 — 無耦合 sentence-pin 整檔刪除

**W1-01 刪 loom-code 無耦合 sentence-pin 檔（9 檔中 4 檔）**  after: W0-02  acceptance: 2, 4
- Files: loom-code/tests/test_adversary_recipe_code.py, loom-code/tests/test_adversary_recipe_shape.py, loom-code/tests/test_adversary_recipe_skill_gate.py, loom-code/tests/test_adversary_recipe_spec.py
- Test: A2 positive: files-deleted-and-suite-green; negative: referenced-file-not-deleted. A4 positive: deleted-files-vanish-from-census; boundary: grammar-invariant-file-not-deleted.
- Risk: recipe 系四檔互為兄弟（import 其他測試非生產碼），全刪無殘留；agent-decided。

**W1-02 刪 loom-code 剩餘 sentence-pin 檔（3 檔）**  after: W0-02  acceptance: 2, 4
- Files: loom-code/tests/test_agy_tool_mapping.py, loom-code/tests/test_build_recovery_rules.py, loom-code/tests/test_closing_review_recovery_rules.py, loom-code/tests/test_dispatch_profile_contract.py
- Test: A2 positive: files-deleted-and-suite-green; negative: referenced-file-not-deleted. A4 positive: deleted-files-vanish-from-census; boundary: structure-file-not-deleted.
- Risk: build↔closing_recovery 互為註解提及非 import，全刪；dispatch_profile_contract 無 code 引用；agent-decided。

**W1-03 刪 loom-workflow sentence-pin 檔（4 檔）**  after: W0-02  acceptance: 2, 4
- Files: loom-workflow/tests/goal-create/test_input_floor.py, loom-workflow/tests/goal-create/test_skill_md.py, loom-workflow/tests/scripts/test_critique_compaction.py, loom-workflow/tests/scripts/test_goal_create_compaction.py
- Test: A2 positive: files-deleted-and-suite-green; negative: referenced-file-not-deleted. A4 positive: deleted-files-vanish-from-census; boundary: behavior-file-not-deleted.
- Risk: skill_md 被 3 檔測試名提及（非 import）；goal_create_compaction↔skill_md 互為 NOTE 提及（duplicate pin）；agent-decided。

### Wave 2 — 耦合檔處理

**W2-01 module_criteria_text 遷移後刪除**  after: W0-02  acceptance: 2, 4
- Files: loom-code/tests/test_module_criteria_text.py, loom-code/tests/test_adversary_routing.py, AGENTS.md
- Test: A2 positive: routing-SUITE_EXTRA-and-AGENTS-ref-removed-then-file-deleted; negative: module-criteria-checks-still-enforced. A4 positive: file-vanishes-from-census; boundary: no-sentence-pin-left-in-repo.
- Risk: 此檔釘 AGENTS.md module criteria 散文＋記四條判準由哪支 check 執行；刪除需同步移除 routing SUITE_EXTRA 與 AGENTS.md:54 引用；四條判準的可執行 check 本身（test_adversary_routing/layout 內）保留；agent-decided。

### Wave 3 — 驗證

**W3-01 對應表：刪除釘住 → 具名替代證據**  after: W1-01, W1-02, W1-03, W2-01  acceptance: 3
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A3 positive: each-deleted-pin-lists-replacement-evidence; negative: deleted-pin-without-replacement-fails. A3 boundary: replacement-names-checker-rule-or-lens-dimension.
- Risk: 每檔刪除的釘住測試列出具名替代（checker 重算規則 id、結構測試名或 review lens 面向）；agent-decided。

**W3-02 重算普查與行為守護**  after: W1-01, W1-02, W1-03, W2-01  acceptance: 1, 4, 5
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A1 positive: census-rerun-matches-report; negative: deleted-file-not-in-census. A4 positive: sentence-pin-zero-grammar-kept; boundary: structure-class-kept-not-deleted. A5 positive: executable-test-count-not-decreased; boundary: count-verified-before-and-after.
- Risk: 行為測試數守護（A5）以 package suite 測試函式數前後對照；agent-decided。

## Simplicity check
- 用既有 `prose_pin` 分類語意（import + 斷言 pattern）建普查腳本，不另造分類框架 — taken
- 刪除工作依「無耦合整檔刪 / 有耦合裁剪」二分，避免逐檔客製 — taken
- 不新增 checker 規則或 gate，只重算既有測試 — taken
- 單一普查報告作為 SSOT，W1/W2 各 task 不重複寫分類邏輯 — taken
- plan-lens W1 三批整檔刪合併為單一 task — declined: Files 上限 8 檔/task（plan.field-caps），19 檔無法塞進一個 task；三批維持
- plan-lens test_acceptance_test_report_shape 重複列於刪與裁剪 — taken

## Questions asked
① — what — 把上次改機制後遺留的釘住散文句子的舊測試庫存量清掉，以後改散文不會再被舊釘子弄到要連改測試。對嗎？ — 對
① — consequence — 清理只到「文法級不變量」界線：字面感應測試從 ~40 檔降到僅剩文法不變量；日後發現被刪釘子本可擋下真實缺陷時，依收回條款可還原。接受？ — 對

## Risks
1. 分類判定（結構 vs 釘住 vs 文法）有灰色地帶，reviewer 冷讀覆核每檔；誤刪真實行為測試由 W3 行為守護擋下。
2. module_criteria_text 的四條判準 check（test_adversary_routing/layout 內）必須保留——刪的是「釘散文的映射測試」不是判準本身（A2 negative 覆蓋）。
3. census 腳本歷經五輪修正（執行判別、語句 pattern 方向、裸 production import、`.stdout` 接收變數、repo-root 排除）；最終分類已 cold-read 覆核，殘餘誤判方向為保守（多留不少刪）。