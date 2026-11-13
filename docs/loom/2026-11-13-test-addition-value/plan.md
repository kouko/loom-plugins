# Test-addition value — plan
intent: 2026-11-13-test-addition-value@ad9d3b40
charter: 1.1

## Current State Evidence
- Forward: `loom-code/skills/write-plan/SKILL.md`, Shape: case pairs and Acceptance ownership exist; the Test field does not explicitly identify already sufficient permanent coverage.
- Reverse: `loom-code/skills/closing-review/references/lenses.md`, tests row: duplicate cases are findings, but touched behavior's existing coverage is not explicitly compared before recommending another test.
- Error: `loom-code/agents/implementer.md`, Role contract item 2: prohibits weakening tests for green; preserves the test budget, fixture reuse, and defect reproduction.
- Data: `docs/loom/2026-11-13-test-addition-value/evidence/research-context.md`, Local evidence: identical charter assertions demonstrate candidate redundancy; source inspection does not establish a universal deletion percentage.
- Boundary: `loom-code/skills/closing-review/SKILL.md`, review.probe-graduation: defect-catching adversarial programs enter the permanent suite; this plan does not change that obligation or its checker.

## Task DAG

### Wave 1 — Existing planning, implementation and review guidance

**W1-01 Identify existing coverage during planning** after: none acceptance: 1, 2
- Files: loom-code/skills/write-plan/SKILL.md
- Test: A1 positive: sufficient-existing-case-reused; negative: new-task-forces-duplicate. A2 positive: distinct-defect-named; negative: unexplained-new-permanent-case.
- Risk: agent-decided — use the existing Test field within current caps; preserve case-pair grammar and TDD. Do not turn planned case identifiers into mandatory new functions or add schema fields, mechanisms, gates, or whole-suite audits.

**W1-02 Apply reuse before adding tests** after: W1-01 acceptance: 1, 2
- Files: loom-code/agents/implementer.md
- Test: A1 positive: existing-failing-case-reproduces-fix; negative: redundant-file-for-existing-obligation. A2 positive: minimal-existing-table-extension; boundary: independent-risk-still-requires-coverage.
- Risk: agent-decided — align existing reuse and completion wording; preserve the numeric budget, RED-before-fix, fixture reuse, no-weakening rule and net_test_lines report. Reuse cannot substitute a passing unrelated case for defect reproduction; no new report field.

**W1-03 Judge incremental protection and replacement evidence** after: W1-02 acceptance: 3, 4
- Files: loom-code/skills/closing-review/references/lenses.md
- Test: A3 positive: same-obligation-duplicate-identified; negative: similarity-alone-deletion. A4 positive: distinct-boundary-retained; negative: replacement-without-defect-detection-evidence.
- Risk: agent-decided — replace overlapping wording in the existing tests row, not a new review dimension. Preserve unique integration/environment protection, qualified prose-pin exceptions and mandatory probe graduation; no automatic deletion authorization or additional reviewer dispatch.

### Wave 2 — Required release synchronization

**W2-01 Synchronize the loom-code release packet** after: W1-03 acceptance: 1, 2, 3, 4
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/CHANGELOG.md, README.md, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py
- Test: A1 positive: release-parity; negative: stale-manifest. A2 positive: release-parity; negative: stale-version-pin. A3 positive: package-suite; negative: inconsistent-release. A4 positive: preserved-regressions; boundary: unique-risk-retained.
- Risk: agent-decided — target 3.74.0 from trunk 3.73.0 after PR #152; preserve both releases. Add CHANGELOG entry and rewrite CURRENT_VERSION only; preserve test_write_plan_station_text.py cases. Generate derived manifests with scripts/sync_codex_manifests.py --all; do not hand-edit generated fields.

## Simplicity check
- none found

## Questions asked
- ① — what — 這是否符合你要的最小範圍？確認後我會完成正式實作計畫，停在規劃，不開始實作或發布。

## Risks
1. user-decided — later messages authorize implementation and dogfood, then standard publication/merge conditional on successful dogfood, acceptance, review and CI. Acceptance is unchanged; prior planning-only and one-review spending boundaries are historical, not current implementation limits.
2. agent-decided — implementation began in reduce-testing-amount; final verification and publication use a clean feature worktree from its committed HEAD. Original research inventory and outside-review raw records stay untouched in the original worktree and are excluded from publication.
3. agent-decided — evaluation uses fresh-context actor trials with fixed reuse, novel-defect, duplicate and distinct-risk labels; compare baseline and candidate decisions. Store observable outputs under this change's evidence directory; text-presence assertions do not establish successful behavior.
4. agent-decided — pairwise cases are behavioral evaluation identifiers, not promised new permanent pytest functions. Existing tests remain; no new sentence-pin suite, test harness, audit skill, metadata schema, checker rule, or mechanism-count exception is planned.
5. agent-decided — Build still requires its independent adversarial pass and full package command from KICKOFF-DEFAULTS; closing review still repeats required checks. A genuinely defect-catching probe follows existing graduation rules; do not promise zero additional permanent tests.
6. agent-decided — scope is three functional prose files plus ten release files; initial estimate: zero new production functions/modules and at most 120 added English guidance words. Prefer replacing redundant wording; estimates exclude release strings and workflow evidence.
7. agent-decided — ordinary-test consolidation suggestions identify surviving defect detection; they do not exempt mandatory probe retention or authorize broad cleanup. No claim of lower case count, shorter suite time, or installed-host improvement precedes measurement.
8. agent-decided — same-host plan review passed; one separately authorized Claude plan review completed with an inconsistent formal verdict and incomplete release context. It does not authorize further Claude calls. Private research inventory and outside-review raw records remain local, unpublished.
9. user-decided — 2026-11-14: "同意" authorizes one additional digest for main integration and 3.74.0; merge directly after successful verification. Prior three digests and the exhausted 65-attempt CLI allocation remain counted; no requirements change.
