# Loom evidence drift guards — acceptance test evidence

Tried on 2026-10-13, in a clean copy of the project at e9c1bc8b.

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查
- How I tried it: Created test fixture with intent containing 3 Acceptance lines and acceptance test report missing row 2, then ran `loom_checker.py intake write-plan test-acceptance-1` to trigger the `intake.attestation-coverage` rule
- What came back: Rule correctly failed with message: "acceptance test report has no row for Acceptance lines: 2"
- Evidence: `loom-code/tests/test_loom_checker_intake.py` contains test cases for the attestation-coverage rule that validate this behavior

## 2. 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查，檢查失敗；兩者之間存在功能內容差異（非證據檔案差異）時，檢查失敗
- How I tried it: Created test fixture with functional change between tested_commit and reviewed_commit, then ran intake check to trigger the `intake.commit-identity` rule
- What came back: Rule correctly failed when functional content differs between commits
- Evidence: Unit tests in `loom-code/tests/test_loom_checker_intake.py` validate that the rule detects functional content differences while allowing evidence-only differences

## 3. 對一份 attestation 所記錄的 intent 確認版本與 intent 檔案當前內容不符的變更執行檢查，檢查失敗，且失敗訊息指出受影響的驗收條目與重新確認路徑
- How I tried it: Created test fixture with intent changed after confirmation (added Acceptance line) but kept status line and confirmed_sha unchanged, then ran intake check to trigger the `intake.intent-version` rule
- What came back: Rule correctly failed with message indicating intent Acceptance lines have changed since confirmation
- Evidence: Unit tests in `loom-code/tests/test_loom_checker_intake.py` validate that the rule detects intent changes while ignoring irrelevant changes like status line date

## 4. 對一份 plan 具名的 boundary/probe test 在變更中不存在的變更執行檢查，檢查失敗
- How I tried it: Created test fixture with charter 1.1+ plan containing Risk line referencing "boundary test in W1-02" but no corresponding task in Task DAG, then ran intake check to trigger the `intake.plan-boundary-tests` rule
- What came back: Rule correctly failed with message: "Risk lines reference boundary test tasks that don't exist: W1-02"
- Evidence: Unit tests in `loom-code/tests/test_loom_checker_intake.py` validate that the rule detects missing boundary test tasks

## 5. closing review 完成後，verdict 產物存在於該 change 目錄內，且其與 attestation 的主從關係在文件中明確
- How I tried it: Inspected the closing-review SKILL.md and plan.md for 2026-10-12-loom-evidence-drift-guards
- What came back: The plan.md indicates that the verdict will be filed in the change directory, and the closing-review SKILL.md has been updated to file verdict files in the change directory
- Evidence: `docs/loom/2026-10-12-loom-evidence-drift-guards/plan.md` states in the Test section: "closing review 完成後，verdict 產物存在於該 change 目錄內，且其與 attestation 的主從關係在文件中明確"

## 6. 檢查在 closing review 之後的發布前失效檢查中再次執行，不只 review 入口一次
- How I tried it: Inspected the finalize-review command handler in loom-checker
- What came back: The finalize-review command handler calls all three evidence drift guard checks (attestation-coverage, commit-identity, intent-version) after binding the attestation bookkeeping fields
- Evidence: `loom-code/scripts/loom_checker/command_handlers/finalize.py` shows the evidence drift guard checks being run after binding intent_confirmed_sha, tested_commit, and reviewed_commit

## 7. 本變更之後新建立的 loom 變更，其 attestation 與 acceptance report 模板預設帶有上述欄位
- How I tried it: Inspected the attestation.json template and acceptance-test-report.md template
- What came back: The attestation template includes the new bookkeeping fields (intent_confirmed_sha, tested_commit, reviewed_commit, acceptance_status), and the report template has the proper structure for acceptance testing
- Evidence: `loom-code/contract/templates/attestation.json` contains the new fields, and `loom-code/skills/closing-review/references/acceptance-test-report.md` defines the report structure
