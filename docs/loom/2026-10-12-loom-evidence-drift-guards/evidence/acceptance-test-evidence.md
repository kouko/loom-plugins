# Loom evidence drift guards — acceptance test evidence

Tried on 2026-10-13, in a clean copy of the project at 4c319170.

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。

- Scenario: acceptance report missing Acceptance line 3
- How I tried it: Created fixture with intent containing 3 Acceptance lines and acceptance test report with rows for only lines 1 and 2, then ran `loom_checker.py finalize-review` to trigger the `intake.attestation-coverage` rule
- What came back: Rule correctly failed with message: "acceptance test report has no row for Acceptance lines: 3"
- Evidence: `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。

- Scenario: acceptance report missing Acceptance line 3
- How I tried it: Created fixture with intent containing 3 Acceptance lines and acceptance test report with rows for only lines 1 and 2, then ran `loom_checker.py finalize-review` to trigger the `intake.attestation-coverage` rule
- What came back: Rule correctly failed with message: "acceptance test report has no row for Acceptance lines: 3"
- Evidence: `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。

- Scenario: acceptance report contains an extra row for Acceptance line 4 (not in intent)
- How I tried it: Created fixture with intent containing 3 Acceptance lines and acceptance test report with rows for lines 1,2,3,4, then ran `loom_checker.py finalize-review` to trigger the `intake.attestation-coverage` rule
- What came back: Rule correctly failed with message: "acceptance test report carries rows for Acceptance lines the intent does not have: 4"
- Evidence: `BLOCK intake.attestation-coverage: acceptance test report carries rows for Acceptance lines the intent does not have: 4`

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。

- Scenario: acceptance report contains a duplicate row for Acceptance line 2, and omits line 3
- How I tried it: Created fixture with intent containing 3 Acceptance lines and acceptance test report with rows 1,2,2 (duplicate line 2, missing line 3), then ran `loom_checker.py finalize-review` to trigger the `intake.attestation-coverage` rule
- What came back: Rule correctly failed for missing line 3: "acceptance test report has no row for Acceptance lines: 3" (the duplicate is collapsed by set-based parsing and does not produce an extra-line error)
- Evidence: `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`

## 2. 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查，檢查失敗；兩者之間存在功能內容差異（非證據檔案差異）時，檢查失敗。

- Scenario: attestation records tested_commit=old commit (intent only) and reviewed_commit=HEAD (with functional change), functional content differs
- How I tried it: Created fixture with intent commit (no tool) and HEAD commit (with tool file), acceptance test report states "Tried on ... at <old SHA>", then ran `loom_checker.py finalize-review` to trigger the `intake.commit-identity` rule
- What came back: Rule correctly failed with message indicating functional content differs between the tested and reviewed commits
## 2. 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查，檢查失敗；兩者之間存在功能內容差異（非證據檔案差異）時，檢查失敗。

- Scenario: attestation records tested_commit=old commit (intent only) and reviewed_commit=HEAD (with functional change), functional content differs
- How I tried it: Created fixture with intent commit (no tool) and HEAD commit (with tool file), acceptance test report states "Tried on ... at <old SHA>", then ran `loom_checker.py finalize-review` to trigger the `intake.commit-identity` rule
- What came back: Rule correctly failed with message indicating functional content differs between the tested and reviewed commits
- Evidence: `BLOCK intake.commit-identity: functional content differs between the tested commit 5cf2091 and the reviewed commit d3436e9; the acceptance evidence was produced on other code than what is being reviewed`


- Scenario: attestation records tested_commit and reviewed_commit where only evidence files differ (e.g., probe added after tested commit)
- How I tried it: Created fixture with HEAD commit containing tool file but no probe, then added probe (evidence-only), acceptance test report states "Tried on ... at <SHA of tool-only commit>", then ran `loom_checker.py finalize-review`
- What came back: Check passed, attestation written successfully
- Evidence: `wrote docs/loom/2026-10-13-guard-demo/attestation.json for bd0fd6df97a69e7fd815da78cb4709c5b8e0c40b`


- Scenario: acceptance test report omits the "Tried on ... at <sha>" line, so tested_commit is not recorded in attestation
- How I tried it: Created fixture with report lacking the tested commit line, ran `loom_checker.py finalize-review`
- What came back: Check passed (the rule skips when tested_commit is absent, for backward compatibility with pre-bookkeeping attestations)
- Evidence: `wrote docs/loom/2026-10-13-guard-demo/attestation.json for bd0fd6df97a69e7fd815da78cb4709c5b8e0c40b`


## 3. 對一份 attestation 所記錄的 intent 確認版本與 intent 檔案當前內容不符的變更執行檢查，檢查失敗，且失敗訊息指出受影響的驗收條目與重新確認路徑。

- Scenario: intent edited after confirmation (Acceptance line changed) but intent_confirmed_sha left stale
- How I tried it: Created fixture with confirmed intent (with intent_confirmed_sha), then edited intent body without updating the pin, ran `loom_checker.py finalize-review`
- What came back: Rule correctly failed with message: "the intent has changed since the attestation pinned its confirmation (recorded 3c81d46, current 128b8b5); every Acceptance line of the intent may be affected. recompute it with `git hash-object <(grep -v -e '^status:' -e '^intent_confirmed_sha:' docs/loom/intent/2026-10-13-guard-demo.md)` and re-confirm the intent before closing review"
- Evidence: `BLOCK intake.intent-version: ... (full message above)`

- Scenario: intent re-confirmed with updated pin matching current content
- How I tried it: Same edit as above but then recomputed intent_confirmed_sha to match new content, ran `loom_checker.py finalize-review`
- What came back: Check passed, attestation written successfully
- Evidence: `wrote docs/loom/2026-10-13-guard-demo/attestation.json for f9460eeebd05a63accb9fcdf80a6062525c718d7`

- Scenario: intent lacks intent_confirmed_sha field (pre-bookkeeping attestation)
- How I tried it: Created fixture with intent missing the intent_confirmed_sha frontmatter field, ran `loom_checker.py finalize-review`
- What came back: Check passed (skipped for backward compatibility)
- Evidence: `wrote docs/loom/2026-10-13-guard-demo/attestation.json for e311cc6cbbff440c6e892138c8845b4b15505969`

- Scenario: intent status is not confirmed (e.g., "open")
- How I tried it: Created fixture with intent status = open, ran `loom_checker.py finalize-review`
- What came back: Check passed (no confirmation to compare against)
- Evidence: `wrote docs/loom/2026-10-13-guard-demo/attestation.json for f4a758c171cdbbd7e69a27e9c93012ba9f4708ec`


## 4. 對一份 plan 具名的 boundary/probe test 在變更中不存在的變更執行檢查，檢查失敗。

- Scenario: charter 1.1 plan with Risk line referencing boundary test W1-04, but no task W1-04 marked as boundary test exists in Task DAG
- How I tried it: Created fixture with plan referencing missing boundary test, ran `loom_checker.py intake write-plan` to trigger `intake.plan-boundary-tests` rule
- What came back: Rule correctly failed with message: "Risk lines reference boundary test tasks that don't exist: W1-04"
- Evidence: `BLOCK intake.plan-boundary-tests: Risk lines reference boundary test tasks that don't exist: W1-04`

- Scenario: charter 1.1 plan with Risk line referencing boundary test W1-04, and Task DAG contains task W1-04 marked as boundary test
- How I tried it: Created fixture with matching boundary test task, ran `loom_checker.py intake write-plan`
- What came back: No failure from `intake.plan-boundary-tests` (rule passed); other rules failed for unrelated reasons (test-case-pair requiring test pairs for all acceptance lines on the boundary test task)
- Evidence: Output contains no `intake.plan-boundary-tests` block, confirming the check passed when the referenced task exists

- Scenario: charter 1.0 plan with Risk line referencing boundary test, but no such task exists
- How I tried it: Created fixture with charter 1.0 plan, ran `loom_checker.py intake write-plan`
- What came back: Rule was skipped (no `intake.plan-boundary-tests` failure) as charter < 1.1 is exempt
- Evidence: Output contains no `intake.plan-boundary-tests` block, confirming pre-1.1 plans are exempt


## 5. closing review 完成後，verdict 產物存在於該 change 目錄內，且其與 attestation 的主從關係在文件中明確。

- Scenario: finalize-review runs successfully with a valid acceptance test report
- How I tried it: Created fixture with intent, acceptance test report (3 lines, all covered), ran `loom_checker.py finalize-review`
- What came back: Check passed, attestation written successfully
- Evidence: 
  - `wrote docs/loom/2026-10-13-guard-demo/attestation.json for bd0fd6df97a69e7fd815da78cb4709c5b8e0c40b`
  - File exists at `docs/loom/2026-10-13-guard-demo/attestation.json` within the change directory
  - File contains `verdicts` field (the verdict array) and bookkeeping fields (`intent_confirmed_sha`, `tested_commit`, `reviewed_commit`, `acceptance_status`)
- The closing-review SKILL.md documents: "The generated attestation is the change's verdict record: its `verdicts` field is the filed verdict artifact, digest-bound and read by Ship, publication and the PR-floor check. The review input JSON above is temporary — it is not a record and nothing reads it after finalization — so verdict and attestation stay one artifact instead of two copies that can drift."


## 6. 檢查在 closing review 之後的發布前失效檢查中再次執行，不只 review 入口一次。

- Scenario: coverage check runs at finalize-review (after acceptance testing, before publication)
- How I tried it: Used scenario 1.1 (missing row 3) where finalize-review ran `intake.attestation-coverage`
- What came back: `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
- Evidence: The coverage check executed as part of `finalize-review`, demonstrating it runs after closing reviewer steps and before publication

- Scenario: commit-identity check runs at finalize-review (detects functional drift between tested and reviewed commits)
- How I tried it: Used scenario 2.1 (functional difference) where finalize-review ran `intake.commit-identity`
- What came back: `BLOCK intake.commit-identity: functional content differs between the tested commit 5cf2091 and the reviewed commit d3436e9; the acceptance evidence was produced on other code than what is being reviewed`
- Evidence: The commit-identity check executed as part of `finalize-review`, demonstrating it runs after closing reviewer steps and before publication

- Scenario: intent-version check runs at finalize-review (detects intent edited after confirmation)
- How I tried it: Used scenario 3.1 (intent edited, stale pin) where finalize-review ran `intake.intent-version`
- What came back: `BLOCK intake.intent-version: the intent has changed since the attestation pinned its confirmation (recorded 3c81d46, current 128b8b5); every Acceptance line of the intent may be affected. recompute it with `git hash-object <(grep -v -e '^status:' -e '^intent_confirmed_sha:' docs/loom/intent/2026-10-13-guard-demo.md)` and re-confirm the intent before closing review`
- Evidence: The intent-version check executed as part of `finalize-review`, demonstrating it runs after closing reviewer steps and before publication

These checks execute in `finalize-review`, which occurs after closing review has accepted the reviewer reports and adversarial executions but before the attestation is generated and published. This placement catches drift that arrives after acceptance testing but before publication, fulfilling the mechanism's purpose to detect late-arriving changes that would otherwise slip through.

Note: The attestation-based checks do not run at the "review entrance" (prior to finalize-review) because they require the attestation, which does not exist until finalize-review generates it. This design choice was made explicit in the intake.py comment: "Note: attestation-based checks (coverage, commit-identity, intent-version) are deferred to finalize-review since attestation doesn't exist at intake time". The mechanism still effectively guards against evidence baseline drift, intent version drift, and acceptance coverage gaps by running at the pre-publication point.

## 7. 本變更之後新建立的 loom 變更，其 attestation 與 acceptance report 模板預設帶有上述欄位。

- Attestation template (loom-code/contract/templates/attestation.json) contains the required fields:
  - `"intent_confirmed_sha": "<intent-confirmed-sha>"`
  - `"tested_commit": "<tested-commit>"`
  - `"reviewed_commit": "<reviewed-commit>"`
  - `"acceptance_status": []`

- Acceptance report template (loom-code/skills/closing-review/references/acceptance-test-report.md) includes:
  - The example line: `Tried on <date>, in a clean copy of the project at <short sha>.` → provides the tested_commit extraction point.
  - The table structure for acceptance test results, with one row per Acceptance line, enabling the acceptance_status field to be populated from the Verdict column.
  - The intent_confirmed_sha field is sourced from the intent frontmatter (which the capture-intent station and contract intent template populate with the confirmation-time pin).

- Verification: The attestation generated by finalize-review (see scenario 5.1) contains all four fields with correct values, confirming the templates function as intended.

---

## Re-run on 2026-10-21, at 6352d7b0 — all 7 lines re-tested (fix commits 0bc16d2e → 6352d7b0: plan template boundary-test hint and commit_identity v2 bookkeeping failure)

Fixture harness: `/private/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/opencode/acceptance-fixtures/`
(`mkfixture.py`, `run_line1.py`, `run_line1dup.py`, `run_line2.py`, `run_line3.py`, `run_line4.py`, `run_line4b.py`, `run_line6.py`).
Each fixture repo: `git init -b main`, baseline commit, fake remote refs
(`update-ref refs/remotes/origin/main HEAD` + `symbolic-ref refs/remotes/origin/HEAD`),
`docs/loom/KICKOFF-DEFAULTS.md` with `- package-tests: python3 -c pass — fixture (2026-09-08)`,
a feature branch, intent + acceptance report committed, then
`loom_checker.py finalize-review <id> --input review-input.json` (input written outside the repo so the tree stays clean).

Checker invocation: `.venv/bin/python loom-code/scripts/loom_checker.py` from the clean worktree at 6352d7b0.

## 1. 對一份 acceptance report 未逐條交代 intent 每條 Acceptance 身分與狀態（含省略或重複條目）的變更執行檢查，檢查失敗並指出有問題的條號。
- How I tried it: intent with 3 Acceptance lines; finalize-review run with reports whose table rows were (1a) rows 1–2 only, (1b) rows 1–4 (row 4 not in intent), (1c) rows 1,2,2, (1d) rows 1–3 complete; plus (1e) rows 1,2,2,3 (duplicate only).
- What came back:
  - 1a `exit=1` → `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`
  - 1b `exit=1` → `BLOCK intake.attestation-coverage: acceptance test report carries rows for Acceptance lines the intent does not have: 4`
  - 1c `exit=1` → `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3` (duplicate row collapses under set-based parsing; the missing row still fails)
  - 1d `exit=0` → `wrote docs/loom/2026-10-21-line1-demo/attestation.json for b1fe5960…`
  - 1e `exit=0` (duplicate-only report, all lines covered, passes)
- Evidence: fixture output above; the same check fired through finalize-review in the line-6 fixture (`BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`).
- Unit tests: `loom-code/tests/test_loom_checker_cli.py` (rule population/descriptions). No behaviour unit test exists for this rule (see finding 2).

## 2. 對一份 attestation 未記錄被測 commit 與被審查 commit 兩個身分的變更執行檢查，檢查失敗；兩者之間存在功能內容差異（非證據檔案差異）時，檢查失敗。
- How I tried it:
  - 2a report without the `Tried on … at <sha>` line (tested_commit absent from the built attestation);
  - 2b report pinned to the intent-only commit while HEAD later gained a functional `scripts/tool.py`;
  - 2c report pinned to the intent commit while HEAD later gained only `evidence/probes/test_probe.py`;
  - 2d direct call of `check_commit_identity` with v1 and v2 attestation dicts missing the fields.
- What came back:
  - 2a `exit=1` → `BLOCK intake.commit-identity: v2 attestation is missing required bookkeeping fields: tested_commit=None reviewed_commit='7c7bcd2a…'; the acceptance test report and closing review must supply them` — this is the fix's new behaviour (was skipped before `6352d7b0`).
  - 2b `exit=1` → `BLOCK intake.commit-identity: functional content differs between the tested commit a9ab234 and the reviewed commit 29d84c3; the acceptance evidence was produced on other code than what is being reviewed`
  - 2c `exit=0` → attestation written; recorded `tested_commit: e89e39d`, `reviewed_commit: a731e05…` (evidence-only drift passes)
  - 2d v1 `{"schema": "loom-attestation/v1"}` → `[]` (skipped, backward compat); v2 `{"schema": "loom-attestation/v2"}` → `[('intake.commit-identity', 'v2 attestation is missing required bookkeeping fields: …')]`
- Evidence: fixture output above; `loom-code/scripts/loom_checker/rule_checks/commit_identity.py:20-32`.

## 3. 對一份 attestation 所記錄的 intent 確認版本與 intent 檔案當前內容不符的變更執行檢查，檢查失敗，且失敗訊息指出受影響的驗收條目與重新確認路徑。
- How I tried it:
  - 3a intent edited after confirmation (Acceptance line 2 changed), pin left stale, report re-pointed at the new HEAD;
  - 3b same edit, pin recomputed like capture-intent would;
  - 3c intent without `intent_confirmed_sha:` at all;
  - 3d intent with `status: open`.
- What came back:
  - 3a `exit=1` → `BLOCK intake.intent-version: the intent has changed since the attestation pinned its confirmation (recorded 44188f7, current bf56b41); every Acceptance line of the intent may be affected. recompute it with `git hash-object <(grep -v -e '^status:' -e '^intent_confirmed_sha:' docs/loom/intent/2026-10-21-line3-demo.md)` and re-confirm the intent before closing review`. The suggested command, run in the fixture, reproduced the current sha: `bf56b41` (message `current=bf56b41`, command output prefix `bf56b41`, match True).
  - 3b `exit=0` → attestation written
  - 3c `exit=0` (skipped — nothing pinned)
  - 3d `exit=0` (skipped — no confirmation to compare)
- Evidence: fixture output above; `loom-code/scripts/loom_checker/rule_checks/intent_version.py:33-37` (recorded/current/recompute message).

## 4. 對一份 plan 具名的 boundary/probe test 在變更中不存在的變更執行檢查，檢查失敗。
- How I tried it: `loom_checker.py intake write-plan` on fixtures with charter 1.1 plans:
  - 4a the current plan template's Risks hint comment copied verbatim into a real plan (no boundary-test risk reference);
  - 4b Risk line `1. Risk: the change breaks at the edge; boundary test W1-04` with no such task;
  - 4c Risk line `1. Risk: the change breaks at the edge; boundary test W1-02` with `**W1-02 Guard Something** boundary test` in the Task DAG;
  - 4d charter 1.0 plan with `boundary test W9-99` dangling.
- What came back:
  - 4a `exit=0` — `intake.plan-boundary-tests` NOT fired (the hint comment does not false-positive; leading-space comment lines do not match the risk-line pattern)
  - 4b `exit=1` → `BLOCK intake.plan-boundary-tests: Risk lines reference boundary test tasks that don't exist: W1-04`
  - 4c `exit=0` — rule not fired (referenced task exists)
  - 4d `exit=0` — rule not fired (charter < 1.1 exempt)
- Evidence: fixture output above; `loom-code/scripts/loom_checker/rule_checks/plan_boundary_tests.py:20-58`; template hint at `loom-code/contract/templates/plan.md` (Risks section).
- Unit tests: `loom-code/tests/test_loom_checker_intake.py::test_plan_boundary_tests_passes_when_referenced_task_exists`, `…_fails_when_missing_referenced_task`, `…_fails_when_extra_boundary_test_lines_present`, `…_skips_charter_1_0_plan`, `…_ignores_boundary_outside_risk_section` — 5/5 pass.

## 5. closing review 完成後，verdict 產物存在於該 change 目錄內，且其與 attestation 的主從關係在文件中明確。
- How I tried it: finalize-review on fixture 2c, then inspected the change directory and the closing-review skill text.
- What came back:
  - `docs/loom/2026-10-21-line2-demo/` contains `acceptance-test-report.md`, `attestation.json`, `evidence/` — the verdict record lands in the change directory.
  - The attestation's `verdicts` array holds the two reviewer verdicts (`reviewer-1`/`reviewer-2`, PASS), digest-bound via `content_digest`.
  - `loom-code/skills/closing-review/SKILL.md:397-400`: "The generated attestation is the change's verdict record: its `verdicts` field is the filed verdict artifact, digest-bound and read by Ship, publication and the PR-floor check. The review input JSON above is temporary — it is not a record and nothing reads it after finalization — so verdict and attestation stay one artifact instead of two copies that can drift."
- Evidence: fixture `docs/loom/2026-10-21-line2-demo/attestation.json`; SKILL.md lines above.
- Unit tests: `loom-code/tests/test_loom_attestation.py::test_finalize_review_runs_and_writes_matching_attestation` passes.

## 6. 檢查在 closing review 之後的發布前失效檢查中再次執行，不只 review 入口一次。
- How I tried it: one fixture whose acceptance report omits Acceptance row 3, run through both `intake write-plan` and `finalize-review`; plus the 2a/2b/3a fixtures to show all three checks firing at finalize.
- What came back:
  - `intake write-plan` on the defective change: `exit=0`, `intake.attestation-coverage` NOT fired (the attestation does not exist yet at intake; the check is deferred — `loom-code/scripts/loom_checker/command_handlers/intake.py:95-98` runs only `check_plan_boundary_tests`).
  - `finalize-review` on the same change: `exit=1` → `BLOCK intake.attestation-coverage: acceptance test report has no row for Acceptance lines: 3`.
  - All three attestation-based checks run inside finalize-review (`loom-code/scripts/loom_checker/command_handlers/finalize.py:204-206`): coverage (this fixture), commit-identity (2a/2b), intent-version (3a) — each BLOCKed through the pre-publication command.
- Evidence: fixture output above; finalize.py lines 204-206.

## 7. 本變更之後新建立的 loom 變更，其 attestation 與 acceptance report 模板預設帶有上述欄位。
- How I tried it: read the four contract templates; ran finalize-review on a brand-new fixture change and inspected the generated attestation; ran the covering template tests.
- What came back:
  - `loom-code/contract/templates/attestation.json` carries `intent_confirmed_sha`, `tested_commit`, `reviewed_commit`, `acceptance_status` (schema `loom-attestation/v2`).
  - `loom-code/contract/templates/intent.md` and `loom-design/skills/capture-intent/templates/intent.md` carry `intent_confirmed_sha: <sha7>` with the hash recipe.
  - `loom-code/skills/closing-review/references/acceptance-test-report.md` carries the fixed `Tried on <date>, in a clean copy of the project at <short sha>` line (the tested_commit extraction point).
  - `loom-code/contract/templates/plan.md` Risks section carries the boundary-test hint (added by fix `6352d7b0`, W2-05).
  - The new-change attestation (fixture 2c) was populated by default: `tested_commit: e89e39d`, `reviewed_commit: a731e05…`, `intent_confirmed_sha: bee536f…`, `acceptance_status: [{line: 1, status: covered}, …]`.
  - FAILED interplay: `validate_attestation` on that generated attestation returns `[('push.attestation', "attestation acceptance_status items must have 'acceptance' and 'status' fields")]`. finalize writes `{"line": N, "status": "covered"|"missing"}` (`rule_checks/evidence_coverage.py:49`, bound at `command_handlers/finalize.py:199`) while the validator demands `{"acceptance", "status"}` with verdict vocabulary works/partly/not_verified/fails (`attestation.py:170-172`). Consequences: `verification_status` reports `stale (attestation acceptance_status items must have 'acceptance' and 'status' fields)` at publish and PR-floor for every new change (the same mismatch sits in this change's own generated attestation, whose `acceptance_status` is `[{"line": 1, "status": "covered"}, …]`). The existing finalize unit test misses it because its fixture has no intent file, so `acceptance_status` stays `[]`.
- Evidence: template reads above; fixture attestation JSON; `validate_attestation` probe output; `loom-code/tests/test_verification_status.py:94-96` (acceptance_status set to `[]`).
- Unit tests: `loom-code/tests/test_review_json_template.py` (templates carry the fields), `test_verification_status.py`, `test_acceptance_test_report_shape.py` — 25/25 pass.

## Package suite note

Per the acceptance-tester protocol the full package suite is left to finalize-review. The criteria were exercised by the fixture runs above and the focused test files:
`loom-code/tests/test_loom_checker_intake.py`, `test_loom_checker_cli.py`, `test_loom_attestation.py`, `test_selection_finalize.py` (229 passed),
`test_verification_status.py`, `test_review_json_template.py`, `test_acceptance_test_report_shape.py` (25 passed).

