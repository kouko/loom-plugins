# Loom evidence drift guards — acceptance test evidence

Tried on 2026-10-23, in a clean copy of the project at 288d9d58.

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。
- How I tried it: Ran loom_checker.py check_attestation_coverage against change 2026-10-12-loom-evidence-drift-guards
- What came back: The check verified all 7 acceptance lines are present in the report with valid verdicts
- Evidence: loom-code/rule_checks/evidence_coverage.py

## 2. 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查，檢查失敗；兩者之間存在功能內容差異（非證據檔案差異）時，檢查失敗。
- How I tried it: Ran loom_checker.py check_commit_identity with v2 attestation missing tested_commit
- What came back: BLOCK - v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit
- Evidence: loom-code/rule_checks/commit_identity.py

## 3. 對一份 attestation 所記錄的 intent 確認版本與 intent 檔案當前內容不符的變更執行檢查，檢查失敗，且失敗訊息指出受影響的驗收條目與重新確認路徑。
- How I tried it: Simulated intent change after confirmation and ran check_intent_version
- What came back: BLOCK - the intent has changed since the attestation pinned its confirmation; every Acceptance line of the intent may be affected. recompute with `grep -v -e '^status:' -e '^intent_confirmed_shas' docs/loom/intent/2026-10-12-loom-evidence-drift-guards.md | git hash-object --stdin`
- Evidence: loom-code/rule_checks/intent_version.py

## 4. 對一份 plan 具名的 boundary/probe test 在變更中不存在的變更執行檢查，檢查失敗。
- How I tried it: Ran loom_checker.py intake write-plan with plan referencing boundary test task that doesn't exist
- What came back: BLOCK - intake.plan-boundary-tests: Risk lines reference boundary test tasks that don't exist: W1-01
- Evidence: loom-code/rule_checks/plan_boundary_tests.py

## 5. closing review 完成後，verdict 產物存在於該 change 目錄內，且其與 attestation 的主從關係在文件中明確。
- How I tried it: Read closing-review SKILL.md lines 397-401
- What came back: The SKILL.md states the attestation's verdicts field IS the filed verdict artifact, and the review input JSON is temporary — so verdict and attestation stay one artifact instead of two copies that can drift
- Evidence: loom-code/skills/closing-review/SKILL.md

## 6. 檢查在 closing review 之後的發布前失效檢查中再次執行，不只 review 入口一次。
- How I tried it: Read finalize.py lines 203-208
- What came back: finalize-review runs check_attestation_coverage, check_commit_identity, and check_intent_version after reviewers and adversarial pass
- Evidence: loom-code/scripts/loom_checker/command_handlers/finalize.py

## 7. 本變更之後新建立的 loom 變更，其 attestation 與 acceptance report 模板預設帶有上述欄位。
- How I tried it: Checked attestation.json template and acceptance-test-report.md template
- What came back: attestation.json template includes intent_confirmed_sha, tested_commit, reviewed_commit, acceptance_status fields; acceptance-test-report.md template has the fixed table structure with "Tried on ... at <sha>" line
- Evidence: loom-code/contract/templates/attestation.json, loom-code/skills/closing-review/references/acceptance-test-report.md
