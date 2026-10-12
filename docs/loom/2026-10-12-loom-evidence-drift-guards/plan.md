# Loom evidence drift guards — plan
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
- Files: `contract/templates/attestation.json`, `loom-checker/attestation.py`, `loom-checker/rule_checks/intake.py`, `loom-checker/rules.py`, `loom-checker/__init__.py`
- Test: A1 positive: schema extended rules registered; negative: invalid schema rejected. A2 positive: tested-reviewed diff evidence-only; boundary: functional changes fail. A3 positive: intent sha matches confirmation; boundary: post-confirmation fail. A4 positive: Risk lines have boundary tests; boundary: missing test fails.
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

**W2-01 Update plan template with boundary test hint**  after: W1-03  acceptance: 7
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
3. Closing-review must correctly parse acceptance test report to populate attestation acceptance_status
4. Plan boundary test rule applies only to new plans (charter 1.1+); legacy plans exempt per existing policy
5. Verdict filing location change must not break reviewer agent contract (loom-code:reviewer)
6. Second-vendor suggest is non-blocking; opt-in required before closing-review per KICKOFF-DEFAULTS
7. Claude recommendation: review verification and publication mechanism evidence suggests getting Claude review for added confidence in the evidence drift guard mechanism