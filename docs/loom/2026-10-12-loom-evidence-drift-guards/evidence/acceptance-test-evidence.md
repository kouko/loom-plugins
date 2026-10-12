# Loom evidence drift guards — acceptance test evidence

Tried on 2026-10-12, in a clean copy of the project at 8512445f.

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態的變更執行檢查
- How I tried it: `cd /Users/kouko/GitHub/loom-plugins && uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_intake.py -k "attestation-coverage" -xvs`
- What came back: `4 passed` — 規則正確註冊、正確識別缺漏行、正確拒絕重複行
- Evidence: `loom-code/tests/test_loom_checker_intake.py` 新增測試案例覆蓋 `intake.attestation-coverage`

## 2. 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查
- How I tried it: `cd /Users/kouko/GitHub/loom-plugins && uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_intake.py -k "commit-identity" -xvs`
- What came back: `4 passed` — 規則正確比對 tested_commit vs reviewed_commit 功能內容摘要
- Evidence: `loom-code/tests/test_loom_checker_intake.py` 新增測試案例覆蓋 `intake.commit-identity`

## 3. 對一份 attestation 所記錄的 intent 確認版本與 intent 檔案當前內容不符的變更執行檢查
- How I tried it: `cd /Users/kouko/GitHub/loom-plugins && uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_intake.py -k "intent-version" -xvs`
- What came back: `4 passed` — 規則正確比對 intent_confirmed_sha 與當前 intent（排除 status line）
- Evidence: `loom-code/tests/test_loom_checker_intake.py` 新增測試案例覆蓋 `intake.intent-version`

## 4. 對一份 plan 具名的 boundary/probe test 在變更中不存在的變更執行檢查
- How I tried it: `cd /Users/kouko/GitHub/loom-plugins && uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_checker_intake.py -k "plan-boundary-tests" -xvs`
- What came back: `4 passed` — 規則正確檢查 charter 1.1+ plan 的 Risk 行對應 boundary test
- Evidence: `loom-code/tests/test_loom_checker_intake.py` 新增測試案例覆蓋 `intake.plan-boundary-tests`

## 5. closing review 完成後，verdict 產物存在於該 change 目錄內
- How I tried it: 檢查 closing-review SKILL.md 更新邏輯；單元測試驗證 verdict 檔案寫入正確路徑
- What came back: 相關單元測試通過（`test_loom_attestation.py` 相關測試）
- Evidence: `loom-code/skills/closing-review/SKILL.md` 更新邏輯；`loom-code/scripts/loom_checker/publish.py` verdict 處理邏輯

## 6. 檢查在 closing review 之後的發布前失效檢查中再次執行
- How I tried it: `cd /Users/kouko/GitHub/loom-plugins && uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_attestation.py -k "finalize" -xvs`
- What came back: `4 passed` — finalize-review 在產生 attestation 前重跑 evidence drift guard 檢查
- Evidence: `loom-code/scripts/loom_checker/command_handlers/finalize.py` 新增檢查邏輯

## 7. 本變更之後新建立的 loom 變更，其 attestation 與 acceptance report 模板預設帶有上述欄位
- How I tried it: 檢查 attestation.json 模板、plan.md 模板；單元測試驗證模板包含新欄位
- What came back: 模板檢查通過
- Evidence: `loom-code/contract/templates/attestation.json`、`loom-code/contract/templates/plan.md`