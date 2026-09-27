# Prose changes stop producing mandatory executable tests — acceptance test evidence

Tried on 2026-09-27, in a clean copy of the project at 5f9a3228.

## 1. 一個只改 skill 或 reference 散文的變更，其計畫中不再被要求為每個 task 附帶測試案例對；計畫能通過進場檢查並進入 Build。
- How I tried it: Ran intake check on existing plan; verified existing test cases for prose/release exemption
- What came back: 
  - `python3 loom-code/scripts/loom_checker.py intake write-plan 2026-09-27-prose-evidence-class` succeeded (exit code 0)
  - `python3 loom-code/scripts/loom_checker.py plan docs/loom/2026-09-27-prose-evidence-class/plan.md` succeeded (no output)
  - pytest tests for prose-only task exemption passed:
    * `test_prose_only_task_with_evidence_store_files_is_exempt` PASSED
    * `test_prose_only_task_with_release_metadata_is_exempt` PASSED
- Evidence: 
  - Intake check succeeded for existing plan: docs/loom/2026-09-27-prose-evidence-class/plan.md
  - Test results: 12/12 A1/A2 related tests passed in loom-code/tests/test_loom_checker_intake.py

## 2. 一個有行為變更的變更（改變 checker 規則、agent 行為或任何執行面），其驗收線仍被要求擁有正向加反向（或邊界）的測試案例對。
- How I tried it: Verified existing test cases for behavior task requirements
- What came back: All behavior task test pair requirement tests passed:
  - `test_behaviour_task_with_py_file_requires_test_pairs` PASSED
  - `test_behaviour_task_with_sh_file_requires_test_pairs` PASSED  
  - `test_task_with_test_file_requires_test_pairs` PASSED
  - `test_task_with_protected_part_requires_test_pairs` PASSED
  - `test_mixed_docs_and_code_task_requires_test_pairs` PASSED
  - `test_protected_name_file_requires_test_pairs` PASSED
  - `test_py_under_change_store_requires_test_pairs` PASSED
  - `test_sh_under_evidence_requires_test_pairs` PASSED
  - `test_mixed_docs_and_py_under_change_store_requires_test_pairs` PASSED
  - `test_md_under_change_store_still_exempt` PASSED
- Evidence: 
  - 9/9 behavior task tests passed in loom-code/tests/test_loom_checker_intake.py
  - Confirmed that .py, .sh, test files, and protected parts still require test pairs

## 3. review 的 tests 面向文字承認散文變更的合格證據類別（checker 重算、fresh-context 審查、行為變更時的獨立驗收測試），且不再僅因散文變更未新增測試檔而開出 finding。
- How I tried it: Verified prose evidence class definition in lenses.md and ran related tests
- What came back: 
  - lenses.md contains: "prose artifacts' qualified evidence = the checker's recomputed rules, fresh-context review, and — only when behavior changes — independent acceptance testing; a prose-only change needs no new executable test file."
  - Test `test_prose_evidence_sentence_present` PASSED
  - Test `test_prose_does_not_eliminate_behavior_evidence` PASSED
- Evidence:
  - Prose evidence sentence present in loom-code/skills/closing-review/references/lenses.md line 54
  - 2/2 A3 related tests passed in loom-code/tests/test_reviewer_mechanical_evidence.py

## 4. 發版後，三份 plugin manifest 與 CHANGELOG 的版本同步由單一位置的重算檢查驗證；修改版號不再需要編輯多個寫死版號字串的測試檔。
- How I tried it: Verified CURRENT_VERSION constant usage and ran version sync test
- What came back:
  - `python3 -m pytest loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized` PASSED
  - All manifests and CHANGELOG show version 3.22.0
  - When deliberately mismatching a version, the test failed as expected
- Evidence:
  - loom-code/plugin.json: "version": "3.22.0"
  - loom-code/.claude-plugin/plugin.json: "version": "3.22.0"  
  - loom-code/.codex-plugin/plugin.json: "version": "3.22.0"
  - loom-code/CHANGELOG.md: ## [3.22.0] — 2026-09-27
  - loom-code/tests/test_write_plan_station_text.py line 9: CURRENT_VERSION = "3.22.0"

## 5. 既有行為驗證不變：對抗探針上限、測試預算、計畫簡化檢查、獨立驗收測試各站照常運作。
- How I tried it: Verified adversarial probe cap, implementer budget, plan simplicity check, acceptance-testing station
- What came back:
  - Adversarial probe cap: `adversarial.proportionate` rule shows max 5 programs
  - MAX_PROBE_PROGRAMS = 5 confirmed via direct import
  - Implementer budget: loom-code/agents/implementer.md states "at most one positive and one negative or boundary case per Acceptance line"
  - Plan simplicity check: plan.field-caps rule requires ## Simplicity check section; plan contains this section
  - Acceptance-testing station: Referenced in loom-code/README.md flowchart and agents table
  - Total rules: 26 confirmed via `loom_checker.py --list-rules`
- Evidence:
  - Adversarial proportionate rule from --list-rules: "A change produces at most 5 adversarial probe programs"
  - Implementer agent doc: lines 42-43 mention test budget
  - Plan field caps rule: mentions ## Simplicity check requirement
  - README.md shows acceptance-tester agent dispatched by closing-review
  - 26 rules counted from --list-rules output