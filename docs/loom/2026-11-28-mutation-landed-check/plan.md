# A forced RED counts only after the mutation is confirmed landed — plan
intent: 2026-11-28-mutation-landed-check@ea2e571f2
charter: 1.1

## Current State Evidence
- Forward: `loom-code/references/engineering-baseline.md:43` False-green diagnostic says comment out the change and re-run; it must fail. No landed check.
- Reverse: `loom-code/references/engineering-baseline.md:72` Code-first backfill says break the covered behaviour and watch the test fail; no landed check.
- Error: `loom-code/skills/closing-review/references/adversarial.md:124` each probe-update mutation must turn the probe RED; the report gives command and observed result only.
- Data: `loom-code/references/tests-standard.md` §1 "A test can fail for the behaviour it names" holds the shared test rules; pins in `loom-code/tests/test_tests_standard_text.py`.
- Boundary: mutation tooling (mutmut, cosmic-ray, stryker) in `closing-review/references/adversarial-code.md` already applies mutants itself; out of scope.

## Task DAG

### Wave 1

**W1-01 Mutation-landed rule and its pointers**  after: none  acceptance: 1, 2, 3, 4
- Files: loom-code/references/tests-standard.md, loom-code/references/engineering-baseline.md, loom-code/skills/closing-review/references/adversarial.md, loom-code/tests/test_tests_standard_text.py
- Test: A1 positive: landed-rule-in-standard; negative: landed-rule-in-baseline. A2 positive: baseline-points-to-rule; negative: baseline-restates-rule. A3 positive: adversarial-report-names-landed-check; negative: adversarial-pointer-missing. A4 positive: rule-sentence-pinned; negative: rule-made-optional.
- Risk: rule in tests-standard §1; baseline, adversarial.md carry pointers; cases are new MOVED_RULES/RULE_SENTENCES entries plus exact pointer pins in existing test functions; no new function, matcher or self-test; agent-decided.

### Wave 2

**W2-01 Release metadata for loom-code 3.92.0**  after: W1-01  acceptance: 5
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A5 positive: release_sync; boundary: release_stale_pin. Existing pin `test_current_release_metadata_is_synchronized` covers it.
- Risk: minor bump (station guidance text) via SSOT then `sync_codex_manifests.py --all`, derived manifests committed; agent-decided.

## Simplicity check
- Put release metadata in W1-01 — declined: version pin test churn would mix with rule pins and the prior change kept them apart for review clarity.
- Satisfy A3 by extending the existing "command and observed result" sentence rather than a new requirement — taken
- Build the case ids as data entries in existing test functions, not new test functions (plan reviewer nit) — taken

## Questions asked
① — what — 這是你要的嗎？（意圖重述與驗收條件）(user: 「可以用 codex 檢查一次嗎」, then 「可以」)
① — what — 意圖照上一則訊息的描述，加上「最後審查用 Codex 當第二位 reviewer」，這樣可以嗎？(user: 「可以」)

## Risks
1. No recorded incident grounds this rule; it is preventive. Existing probes already check anchor-exactly-once and an unmutated control, so no current program should break.
2. user-decided — automatic publication after closing-review; merge stays a separate decision.
3. user-decided — Codex second reviewer at closing review (`gpt-6.2-sol`, effort high), from the user's request 「可以用 codex 檢查一次嗎」.
user-decided — second-vendor selection-confirmed: codex
