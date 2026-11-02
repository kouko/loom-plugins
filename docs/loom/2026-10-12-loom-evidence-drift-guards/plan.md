# Loom evidence drift guards — plan (reshaped per complexity critique)
intent: 2026-10-12-loom-evidence-drift-guards@71bb82d9
spec: docs/loom/2026-10-12-loom-evidence-drift-guards/spec.md@e5b02ac
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Extend attestation schema and add checker rules**  after: none  acceptance: 1,2,3,4
- Files: `contract/templates/attestation.json`, `loom-checker/attestation.py`, `loom-checker/rule_checks/evidence_coverage.py`, `loom-checker/rule_checks/commit_identity.py`, `loom-checker/rule_checks/intent_version.py`, `loom-checker/rules.py`, `loom-checker/__init__.py`
- Test: A1 positive: coverage rule registers; negative: invalid schema rejected. A2 positive: commit diff limited to evidence; negative: functional changes fail. A3 positive: intent sha matches confirmation; negative: post-confirmation fail. A4 positive: Risk lines have boundary tests; negative: missing test fails.
- Risk: new checker rules must not break existing intake; agent-decided
- Risk: attestation schema extension v1-compatible; agent-decided

**W1-02 File verdict in change directory and populate attestation**  after: W1-01  acceptance: 5
- Files: `skills/closing-review/SKILL.md`, `loom-checker/publish.py`, `loom-checker/attestation.py`
- Test: A5 positive: verdict file exists with reviewer findings; boundary: missing file or broken link fails
- Risk: verdict format reviewer-compatible; agent-decided
- Risk: attestation acceptance_status matches report verdicts; agent-decided

**W1-03 Re-run evidence checks in finalize-review**  after: W1-02  acceptance: 6
- Files: `loom-checker/verify.py`, `loom-checker/__init__.py`
- Test: A6 positive: finalize-review runs all evidence checks; boundary: skipped if bypassed
- Risk: no duplicate finalize-review logic; agent-decided

### Wave 2

**W2-01 Update evidence file whitelist in digest**  after: W1-03  acceptance: 2
- Files: `loom-checker/digest.py`, `loom-code/contract/manifest.yaml`
- Test: A2 positive: publication_only_paths extended with evidence files; boundary: non-evidence files still counted as functional content
- Risk: only necessary output files excluded; agent-decided

**W2-02 Update capture-intent to record intent_confirmed_sha**  after: W2-01  acceptance: 3
- Files: `loom-design/skills/capture-intent/SKILL.md`, `loom-design/skills/capture-intent/templates/intent.md`
- Test: A3 positive: intent gains intent_confirmed_sha after confirmation; boundary: field missing or invalid
- Risk: follows spec's confirmed-behavior pattern; agent-decided

**W2-03 Update acceptance-tester to record tested_commit**  after: W2-02  acceptance: 2
- Files: `agents/acceptance-tester.md`, `skills/closing-review/references/acceptance-test-report.md`
- Test: A2 positive: acceptance-tester report includes tested_commit field; boundary: missing field fails
- Risk: direct recording avoids parsing fallback; agent-decided

**W2-04 Update closing-review to populate attestation from report**  after: W2-03  acceptance: 5
- Files: `skills/closing-review/SKILL.md`, `loom-checker/attestation.py`
- Test: A5 positive: attestation acceptance_status populated from report Verdict column; boundary: mismatched status fails
- Risk: no duplicate storage of acceptance status; agent-decided

**W2-05 Update plan template with boundary test hint**  after: W2-04  acceptance: 7
- Files: `contract/templates/plan.md`
- Test: A7 positive: Risk section hints boundary test requirement; boundary: template renders correctly
- Risk: template affects new plans only; agent-decided

### Wave 3 — adversarial recovery

**W3-01 Validate concrete boundary programs after implementation**  after: W2-05  acceptance: 4,6,7
- Files: `loom-code/scripts/loom_checker/rule_checks/plan_boundary_tests.py`, `loom-code/scripts/loom_checker/command_handlers/intake.py`, `loom-code/contract/templates/plan.md`, `loom-code/scripts/loom_checker/rules.py`
- Test: A4 positive: an existing named program passes; boundary: missing or misspelled program fails. A6 positive: final checks run; boundary: removed program fails. A7 positive: template explains stages; boundary: planned programs need not exist before Build.
- Risk: agent-decided — distinguish planning readiness from implemented artifact existence; retain existing task-reference checks.

**W3-02 Preserve historical v2 and mechanical verification flows**  after: W3-01  acceptance: 2,7
- Files: `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/scripts/loom_checker/intent_state.py`, `loom-code/tests/test_verification_status.py`, `loom-code/tests/test_selection_finalize.py`
- Test: A2 positive: current evidence records commit identities; boundary: historical seven-key v2 stays valid. A7 positive: a confirmed mechanical narrow change finalizes without independent acceptance testing; boundary: required evidence remains enforced for other changes.
- Risk: agent-decided — compatibility must not turn missing new evidence into an unconditional waiver.

**W3-03 Revalidate evidence on the selected publication tree**  after: W3-02  acceptance: 1,2,3,6
- Files: `loom-code/scripts/loom_checker/attestation.py`, `loom-code/scripts/loom_checker/command_handlers/finalize.py`, `loom-code/scripts/loom_checker/rule_checks/evidence_coverage.py`, `loom-code/scripts/loom_checker/rule_checks/commit_identity.py`, `loom-code/scripts/loom_checker/rule_checks/intent_version.py`, `loom-code/scripts/loom_checker/helpers.py`, `loom-code/skills/closing-review/SKILL.md`, `loom-code/tests/test_verification_status.py`
- Test: A1 positive: complete coverage passes; boundary: omitted/duplicate rows fail. A2 positive: equivalent commits pass; boundary: invalid identity fails. A3 positive: matching intent passes; boundary: drift fails. A6 positive: publication rechecks selected committed artifacts; boundary: checkout content cannot substitute.
- Risk: agent-decided — share rule implementations and read the requested commit, preserving valid evidence-only differences and historical applicability.

**W3-04 Graduate the adversary's demonstrated regressions**  after: W3-03  acceptance: 1,2,4,6,7
- Files: `docs/loom/2026-10-12-loom-evidence-drift-guards/evidence/probes/test_adversarial.py`, `loom-code/tests/test_adversarial_evidence_drift.py`
- Test: A1 positive: coverage; boundary: omissions. A2 positive: identities; boundary: drift. A4 positive: existence; boundary: missing. A6 positive: publication; boundary: corruption. A7 positive: supported flows; boundary: incompatibility.
- Risk: agent-decided — move the unchanged assertions into the permanent suite; only the owning adversary updates its executable program.

**W3-05 Synchronize release metadata and replace stale verification records**  after: W3-04  acceptance: 5,7
- Files: plugin manifests and READMEs, plugin CHANGELOGs, release-pin tests, existing change handoff and verification records
- Test: A5 positive: fresh verdicts remain in the generated attestation; boundary: stale temporary review input is not authoritative. A7 positive: release metadata synchronization passes; boundary: a mismatched version is rejected.
- Risk: agent-decided — release loom-code 3.56.0 and loom-design 2.19.0 before reviewers inspect the final functional content.

**W3-06 Populate confirmation pins at both supported entry paths**  after: W3-03  acceptance: 3,7
- Files: `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-design/skills/capture-intent/SKILL.md`
- Test: A3 positive: either entry records the confirmed content identity; boundary: later content changes fail. A7 positive: code-only entry replaces the template placeholder; boundary: publication metadata is written before computing the pin.
- Risk: agent-decided — both entry paths must record the same hash convention after all confirmed frontmatter is written; no extra user question.

**W3-07 Declare the implemented evidence fields in the contract**  after: W3-06  acceptance: 7
- Files: `loom-code/contract/manifest.yaml`, `docs/loom/evidence/mechanisms.yaml`, `loom-code/CHANGELOG.md`, `loom-code/tests/test_contract_manifest.py`
- Test: A7 positive: every generated evidence field is declared and counted; boundary: a template field absent from the schema fails the existing consistency check.
- Risk: agent-decided — declare the five already implemented fields, not a second evidence mechanism; preserve optional historical shapes and the existing contract version convention for compatible additions.

**W3-08 Preserve escaped content pipes in report cells**  after: W3-03  acceptance: 1
- Files: `loom-code/scripts/loom_checker/rule_checks/evidence_coverage.py`, `loom-code/tests/test_evidence_drift_guards.py`
- Test: A1 positive: a valid report containing an escaped pipe in the requested outcome passes; boundary: an unreadable Verdict remains rejected.
- Risk: agent-decided — split only actual table separators; preserve the narrow fixed-column report format.

**W3-09 Anchor new confirmations in committed history**  after: W3-06  acceptance: 3,6
- Files: `loom-code/scripts/loom_checker/rule_checks/intent_version.py`, `loom-code/tests/test_selection_finalize.py`
- Test: A3 positive: a newly confirmed intent finalizes; boundary: restoring an older confirmed file cannot erase its confirmation baseline. A6 positive: publication uses the same baseline; boundary: a removed or reverted pin remains detectable.
- Risk: agent-decided — use the existing confirmation commit rather than trusting only the mutable file; confirmations predating pin support remain exempt.

**W3-10 Restore the unrelated global adversarial budget**  after: W3-09  acceptance: 7
- Files: `loom-code/scripts/loom_checker/probes.py`, `loom-code/skills/closing-review/references/adversarial.md`, `loom-code/tests/test_selection_finalize.py`
- Test: A7 positive: five programs are accepted; boundary: a sixth is refused through actual finalization, independently of the implementation constant.
- Risk: agent-decided — remove the inherited global increase identified by the independent value assessment; this change has one earned program and needs no larger budget.

**W3-11 Remove unused intake dependencies**  after: W3-10  acceptance: 6
- Files: `loom-code/scripts/loom_checker/command_handlers/intake.py`
- Test: A6 positive: existing intake and module-entry checks pass; boundary: malformed intake still fails through the existing checks.
- Risk: agent-decided — remove three branch-added imports left unused when evidence checks moved to the shared finalization/publication entry; behavior is unchanged.

## Simplicity check
- none found

## Questions asked
① — consequence — 你要的是：loom 流程能自己抓出三類破口——假覆蓋被擋下、過時證據被擋下、Intent 被偷偷改掉會被偵測——做完後這三件事都會在檢查時被擋下。對嗎？（含自動發布授權說明，使用者可 opt out） — 確認 2026-10-12
① — what — 範圍選項 A / B / C — A 確認 2026-10-12
② — behaviour — 是否確認上述 7 項行為：漏測、版本不一致、需求退版及缺少具名測試會被指出；發布前重驗證據；新紀錄補齊欄位，舊紀錄與小改動保留相容處理？這是補齊原分支遺漏的行為確認。 — 確認，符合原本需求 2026-11-02

## Risks
1. Attestation schema extension must stay compatible with v1 attestations and existing finalize-review flow
2. Checker rules must distinguish functional content diff from publication-only diff (evidence files)
3. Closing-review must correctly parse acceptance test report to populate attestation acceptance_status from Verdict column
4. Adversarial recovery checks concrete named boundary programs after Build; planning intake checks task references without requiring unwritten test files.
5. Verdict filing location change must not break reviewer agent contract (loom-code:reviewer)
6. Second-vendor suggest is non-blocking; opt-in required before closing-review per KICKOFF-DEFAULTS
7. Intent_confirmed_sha excludes status line (matches spec confirmed-behavior pattern)
8. Tested_commit recorded directly at acceptance-test time (no report parsing fallback)
9. Evidence whitelist only covers necessary output files (report, evidence, probes)
10. agent-decided — supersede the initial HEAD fallback: finalization requires canonical report provenance; publication checks recorded identities and any declared provenance. A headerless existing report alone cannot prove when testing ran.
11. agent-decided — the independent value assessment found the global probe-cap increase unrelated to the seven outcomes; restore the original five-program budget and remove unused intake imports before shipping.
