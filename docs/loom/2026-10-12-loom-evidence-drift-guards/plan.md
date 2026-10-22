# Loom evidence drift guards — plan (reshaped per complexity critique)
intent: 2026-10-12-loom-evidence-drift-guards@71bb82d9
charter: 1.1

## Current State Evidence
- Forward: `loom-checker/attestation.py` validates attestation schema and content digest; `digest.py` computes functional content diff excluding publication_only_paths
- Reverse: `manifest.yaml publication_only_paths` already excludes attestation.json; acceptance test report template requires one row per Acceptance line but lacks checker enforcement
- Error: Acceptance test report can omit Acceptance lines (youtube-summarize-scraper case); attestation lacks intent version/commit identity; verdict not filed in change directory
- Data: `manifest.yaml` defines publication_only_paths; `attestation.json` template has fixed schema; `acceptance-test-report.md` template defines table structure
- Boundary: acceptance-tester allows `not verified` rows with reason; evidence file differences permitted between tested/reviewed commits; incremental re-testing preserves original tested commit reference

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

## Simplicity check
- none found

## Questions asked
① — consequence — 你要的是：loom 流程能自己抓出三類破口——假覆蓋被擋下、過時證據被擋下、Intent 被偷偷改掉會被偵測——做完後這三件事都會在檢查時被擋下。對嗎？（含自動發布授權說明，使用者可 opt out） — 確認 2026-10-12
① — what — 範圍選項 A / B / C — A 確認 2026-10-12

## Risks
1. Attestation schema extension must stay compatible with v1 attestations and existing finalize-review flow
2. Checker rules must distinguish functional content diff from publication-only diff (evidence files)
3. Closing-review must correctly parse acceptance test report to populate attestation acceptance_status from Verdict column
4. Plan boundary test rule separated as independent concern; this change only adds template hint
5. Verdict filing location change must not break reviewer agent contract (loom-code:reviewer)
6. Second-vendor suggest is non-blocking; opt-in required before closing-review per KICKOFF-DEFAULTS
7. Intent_confirmed_sha excludes status line (matches spec confirmed-behavior pattern)
8. Tested_commit recorded directly at acceptance-test time (no report parsing fallback)
9. Evidence whitelist only covers necessary output files (report, evidence, probes)