# 清理散文釘住測試存量 — plan
intent: 2026-09-27-prose-pin-stock-cleanup@6f3acd78
charter: 1.1

## Current State Evidence
- Forward: `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/classify-test-files.py` — 普查腳本原型已存在，跑出 27 sentence-pin / 16 structure / 68 behavior / 33 not-prose。
- Reverse: `docs/loom/intent/2026-09-27-prose-evidence-class.md` — 證據政策已確立：prose 合格證據 = checker 重算 + fresh-context 審查 + 行為變更時的 AT；字面感應測試只留文法級不變量。
- Error: 手動抽查 `test_dispatch_profile_contract.py:135-162` — 句子釘住測試對「執行合約散文」斷言，跑不到任何程式。
- Data: 12 檔純釘住候選中，`test_adversary_protocol`（被 5 檔 import）、`test_module_criteria_text`（被 AGENTS.md + routing 引用）、`test_build_recovery_rules`↔`test_closing_review_recovery_rules`（互引用）有外部耦合，不能整檔刪。
- Boundary: `test_lenses_deletion_first.py:153` 含 negation matcher 合成自測（文法級不變量）；`classify-test-files.py` 的結構/釘住判定在此檔需 reviewer 覆核。

## Task DAG

### Wave 0 — 普查腳本與分類基準

**W0-01 普查腳本定稿與驗證**  after: —  acceptance: 1
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A1 positive: script-classifies-pure-pin-as-sentence-pin; negative: behavior-file-not-misclassified-as-pin.
- Risk: 分類是 contract surface，reviewer 需冷讀驗證每檔分類與「結構 vs 釘住」邊界；agent-decided。

**W0-02 耦合清單**  after: W0-01  acceptance: 1
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A1 positive: protocol-module-coupling-listed; negative: no-coupling-file-not-listed.
- Risk: 列出每檔被誰 import／引用；決定每檔刪除或保留的依賴；agent-decided。

### Wave 1 — 無耦合純釘住檔刪除

**W1-01 刪無耦合純釘住檔（loom-code）**  after: W0-02  acceptance: 2, 4
- Files: loom-code/tests/test_adversary_recipe_code.py, loom-code/tests/test_adversary_recipe_shape.py, loom-code/tests/test_adversary_recipe_skill_gate.py, loom-code/tests/test_adversary_recipe_spec.py, loom-code/tests/test_agy_tool_mapping.py, loom-code/tests/test_architecture_doc_consumers.py
- Test: A2 positive: files-deleted-and-suite-green; negative: referenced-file-not-deleted. A4 positive: deleted-files-vanish-from-census; boundary: grammar-invariant-file-not-deleted.
- Risk: 逐檔以普查腳本為準，刪前人工確認無外部引用；多檔併一 task 因同類同 wave；agent-decided。

**W1-02 刪無耦合純釘住檔（loom-workflow + root）**  after: W0-02  acceptance: 2, 4
- Files: loom-workflow/tests/scripts/test_critique_compaction.py, loom-workflow/tests/scripts/test_independent_advisor_compaction.py, loom-workflow/tests/scripts/test_no_retired_loom_code_skill_names.py, tests/test_agy_install_docs.py, tests/test_loom_skill_description_catalog.py, tests/test_principles_ratification.py
- Test: A2 positive: files-deleted-and-suite-green; negative: referenced-file-not-deleted. A4 positive: deleted-files-vanish-from-census; boundary: behavior-file-not-deleted.
- Risk: 逐檔人工確認刪除；loom-workflow 檔在該 plugin 的 tests 目錄；agent-decided。

**W1-03 刪剩餘無耦合釘住檔**  after: W0-02  acceptance: 2, 4
- Files: loom-code/tests/test_write_plan_shape_text.py, loom-code/tests/test_reviewer_mechanical_evidence.py, loom-code/tests/test_lenses_deletion_first.py, loom-code/tests/test_readme_review_order.py, loom-code/tests/test_plan_field_caps.py
- Test: A2 positive: files-deleted-suite-green; negative: grammar-invariant-not-deleted. A4 positive: census-sentence-pin-count-drops-by-deleted-files; boundary: file-with-synthetic-selfst-partly-kept.
- Risk: 前兩檔含 negation matcher 合成自測（文法級），W1-03 僅刪釘住斷言、保留自測；agent-decided。

### Wave 2 — 耦合檔裁剪

**W2-01 裁剪耦合釘住檔**  after: W0-02  acceptance: 2, 4
- Files: loom-code/tests/test_adversary_protocol.py, loom-code/tests/test_module_criteria_text.py, loom-code/tests/test_build_recovery_rules.py, loom-code/tests/test_closing_review_recovery_rules.py
- Test: A2 positive: pinned-assertions-removed-imports-kept; negative: imported-symbol-missing-breaks-importer. A4 positive: no-sentence-pin-remains-in-file; boundary: kept-constant-still-imported.
- Risk: 只刪句子釘住斷言與其測試，保留被引用的常數/函式（如 NO_DISCARD_UNDO）；互引用兩檔同時改；agent-decided。

**W2-02 驗收測試報告形狀檔裁剪**  after: W0-02  acceptance: 2, 4
- Files: loom-code/tests/test_acceptance_test_report_shape.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A2 positive: pinned-sentence-assertions-removed; negative: shape-checks-kept. A4 positive: file-kept-structure-only; boundary: report-shape-pin-removed-keeps-schema.
- Risk: 此檔多數斷言是釘住驗收報告形狀，非行為；保留結構斷言刪句子釘住；agent-decided。

### Wave 3 — 驗證

**W3-01 對應表：刪除釘住 → 具名替代證據**  after: W1-01, W1-02, W1-03, W2-01, W2-02  acceptance: 3
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
- Test: A3 positive: each-deleted-pin-lists-replacement-evidence; negative: deleted-pin-without-replacement-fails. A3 boundary: replacement-names-checker-rule-or-lens-dimension.
- Risk: 每檔刪除的釘住測試列出具名替代（checker 重算規則 id、結構測試名或 review lens 面向）；agent-decided。

**W3-02 重算普查與行為守護**  after: W1-01, W1-02, W1-03, W2-01, W2-02  acceptance: 1, 4, 5
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md
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
2. 耦合檔裁剪若漏掉某 import 鏈，套件測試會紅（A2 negative case 覆蓋）。
3. W1-03 保留文法級自測（如 negation matcher 合成測試），不落入「整檔刪除」。