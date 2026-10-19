# Prose-pin stock cleanup, batch 2 — plan
intent: 2026-09-28-prose-pin-stock-cleanup-batch-2@6c7c7a09
charter: 1.1

## Current State Evidence
- Forward: `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md` "Batch 2 (deferred)" lists 26 files: 7 gate-eval, 15 behavior has_pins, 4 grammar-invariant has_pins.
- Reverse: `docs/loom/evidence/mechanisms.yaml` evals name gate-eval files and pure-pin nodes (L101, L110, L116, L315, L342, L345, L348, L351, L360, L363); `check_mechanisms.py:385-418` accepts any existing test node or cold-read file.
- Error: `run_ab.py:57-58` imports the catalog from `scripts/` (now `tests/`) and fails with ModuleNotFoundError; BASE_REF, variant texts and hash are the 2026-09-14 experiment.
- Data: classifier `--count-exec` reports 728, but about 20 counted functions only contain the literal `loom_checker.py` in a pinned string; helper-level executions go uncounted.
- Boundary: `test_dispatch_profile_contract.py:156-185` asserts its own eval strings; `test_review_convergence_contract.py:114-156` comment forbids deleting recording pins; `test_adversary_routing.py` SUITE_EXTRA copies batch files.

## Task DAG

### Wave 0 — census tool, deletion list, eval re-pointing

**W0-01 Honest execution count and deletion list**  after: —  acceptance: 1, 5
- Files: docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/test_classify_test_files.py, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/deletion-list.md
- Test: A1 positive: census-lists-every-batch-2-pin-function; negative: comment-token-does-not-change-class. A5 positive: subprocess-call-counts-as-exec; negative: loom_checker-string-literal-not-counted.
- Risk: agent-decided — the counter stops counting string literals and base 7244374d is recounted with it; existing classifier tests preserved, only false positives narrowed. The deletion list tags each planned deletion pin, synthetic-partner or exec.

**W0-02 Re-point every affected eval**  after: W0-01  acceptance: 4
- Files: docs/loom/evidence/mechanisms.yaml, loom-code/tests/test_dispatch_profile_contract.py, loom-code/tests/test_codex_hook_trust_contract.py, loom-workflow/tests/goal-create/test_skill_md.py, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/mapping-evals.md
- Test: A4 positive: every-moved-eval-resolves-before-pruning; negative: check-mechanisms-rejects-dangling-node.
- Risk: agent-decided — L101/L110/L116/L342/L345/L351/L360/L363 move to existing behavior tests or the 2026-09-19 blind-run report; L315/L348 point at reduced gate-marker presence checks instead of new cold reads.

### Wave 1 — pruning (parallel; each task writes its own mapping file)

**W1-01 Gate-eval files**  after: W0-02  acceptance: 2, 3
- Files: loom-code/tests/test_dispatch_profile_contract.py, loom-code/tests/test_build_recovery_rules.py, loom-code/tests/test_closing_review_recovery_rules.py, loom-workflow/tests/scripts/test_critique_compaction.py, loom-workflow/tests/scripts/test_distill_sessions_compaction.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/probes/classify-test-files.py, docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/mapping-gate-eval.md
- Test: A2 positive: resolver-and-one-home-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; negative: no-row-names-deleted-test.
- Risk: agent-decided — kept one-home scans get visible override rows; stale gate-eval override rows removed; batch-1 mapping rows citing pruned functions updated.

**W1-02 Adversary and build cluster**  after: W0-02  acceptance: 2, 3
- Files: loom-code/tests/test_adversary_protocol.py, loom-code/tests/test_build_mechanical_checks.py, loom-code/tests/test_adversary_routing.py, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/mapping-adversary.md
- Test: A2 positive: routing-repo-copy-tests-still-run; negative: case-count-scan-imports-resolve. A3 positive: mapping-row-per-removed-pin; boundary: module-criteria-enforced-names-kept.
- Risk: agent-decided — protocol before build for shared constants; keep function names test_module_criteria_text ENFORCED_BY cites; synthetic partners go with their pins.

**W1-03 Fix-scope and test-budget files**  after: W0-02  acceptance: 2, 3
- Files: loom-code/tests/test_fix_handoff_text.py, loom-code/tests/test_fix_scope_text.py, loom-code/tests/test_test_budget_text.py, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/mapping-fix-budget.md
- Test: A2 positive: rule-count-guard-kept; negative: suite-green-after-delete. A3 positive: mapping-row-per-removed-pin; negative: no-row-names-deleted-test.
- Risk: agent-decided — test_fix_handoff_text.py is pins plus synthetic partners and is deleted whole; the other two keep structure checks.

**W1-04 Station-text files**  after: W0-02  acceptance: 2, 3
- Files: loom-code/tests/test_simplified_station_text.py, loom-code/tests/test_expert_mode_skill.py, loom-code/tests/test_ship_station_text.py, loom-code/tests/test_review_convergence_contract.py, loom-code/tests/test_plan_simplicity_text.py, loom-code/tests/test_sync_before_review_text.py, loom-code/tests/test_write_plan_station_text.py, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/mapping-station.md
- Test: A2 positive: sync-trunk-and-selection-behavior-kept; negative: blocked-publish-probe-imports-resolve. A3 positive: mapping-row-per-removed-pin; negative: no-row-names-deleted-test.
- Risk: agent-decided — intent Proposed outcome covers all 26 files, so the review_convergence do-not-delete comment goes with its pins; that row names "passage silently lost" and lens omission.

**W1-05 loom-design contracts and grammar-invariant files**  after: W0-02  acceptance: 2, 3
- Files: loom-design/tests/spec/test_capture_intent_contract.py, loom-design/tests/spec/test_write_spec_contract.py, loom-code/tests/test_acceptance_test_report_shape.py, loom-code/tests/test_lenses_deletion_first.py, loom-code/tests/test_reviewer_mechanical_evidence.py, loom-code/tests/test_write_plan_shape_text.py, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/mapping-design-grammar.md
- Test: A2 positive: grammar-checks-kept; negative: suite-green-after-prune. A3 positive: mapping-row-per-removed-pin; boundary: stale-cold-read-not-claimed-as-replacement.
- Risk: agent-decided — 2026-09-02 cold reads predate the pinned rules, so they are not cited; such rows say review-only.

**W1-06 A/B rerun script repair**  after: —  acceptance: 6
- Files: docs/loom/2026-09-14-loom-visualization-description-trigger/ab/run_ab.py, docs/loom/2026-09-14-loom-visualization-description-trigger/ab/test_run_ab.py, docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/ab-rerun/protocol.md, loom-workflow/tests/scripts/test_adversarial_description_ab_probes.py
- Test: A6 positive: build-extracts-current-description-variants; negative: output-dir-outside-old-change-required.
- Risk: agent-decided — base ref, prompts file and output dir become arguments; results land in docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/ab-rerun/; the old protocol.md stays unchanged; hash check dropped; parse_stream/decide/report/prompts signatures kept.

### Wave 2 — close-out

**W2-01 Census and recount**  after: W1-01, W1-02, W1-03, W1-04, W1-05, W1-06  acceptance: 1, 4, 5
- Files: docs/loom/2026-09-28-prose-pin-stock-cleanup-batch-2/evidence/census-report.md
- Test: A1 positive: clean-worktree-census-zero-pins; negative: other-bucket-exits-1. A4 positive: check-mechanisms-all-clear; negative: dangling-eval-reported. A5 positive: recount-not-below-base; negative: deleted-function-tagged-exec-fails.
- Risk: agent-decided — stitches the mapping files into one table; A5 diffs every deleted function from the deletion list, counted or not; runs from a clean worktree.

## Simplicity check
- One early eval re-point task (W0-02) instead of three serial gate-eval tasks — taken
- Gate-marker presence checks instead of new cold-read records for two gates — taken
- Release bump done at ship as in batch 1, not as a plan task — taken
- Skip the counter fix — declined: a counter that counts string literals cannot prove A5.
- Separate run_ab change — declined: user-decided to include it.

## Questions asked
① — consequence — gate eval 檔（7 個）一起換掉（A，建議）還是保留不動（B）？ → A
① — what — run_ab.py 修復要另開變更還是併進這次？ → 合併進這次
① — what — 覆述確認（含自動發布授權、A/B 重跑約 36 次 Claude 對話的額度成本） → 對

## Risks
1. user-decided — gate-eval pins are replaced too; a wrong edit to gate text is then caught by review and cold-read records, not by a test.
2. user-decided — run_ab repair rides this change; its rerun spends about 36 Claude sessions once, at acceptance testing, writing results.md into the batch-2 ab-rerun evidence.
3. Nested worktrees under .claude/worktrees skew repo-wide scans; every census and count runs from a clean git worktree.
4. Kept scans that locate paragraphs by a literal sentence re-anchor only on existing headings or gate markers; where none exists the scan is deleted and marked review-only. No heading or marker is added to production prose.
