# Acceptance testing and the first reviewers run on the same version at the same time — plan
intent: 2026-09-24-parallel-acceptance-testing-and-review@0f77e69b
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/closing-review/SKILL.md:115-116` orders acceptance testing and its committed report before the first reviewer dispatch.
- Reverse: `loom-code/skills/closing-review/SKILL.md:208-213` makes reviewers read the report; a report committed after verdicts needs the next round.
- Error: session history 2026-09-24: median 12.4-minute wait before the first reviewer; 2 of 17 episodes paid a round for separate batches.
- Data: `test_review_convergence_contract.py:74-80,250-259` pin both ordering sentences; `probes/test_recovery_rules.py:62` uses the §2 sentence as a paragraph boundary.
- Boundary: `loom-code/agents/reviewer.md:97-115` defines resuming the same reviewer only for fix rounds; one-shot vendor CLIs cannot be resumed.

## Task DAG

### Wave 0 — parallel start with an in-round report read

**W0-01 Start acceptance testing with the first reviewers; resume them for the report**  after: —  acceptance: 1, 2, 3, 4, 6
- Files: `loom-code/skills/closing-review/SKILL.md`, `loom-code/agents/reviewer.md`, `loom-code/scripts/test_parallel_acceptance_review_text.py`, `loom-code/scripts/test_review_convergence_contract.py`, `loom-code/skills/closing-review/probes/test_recovery_rules.py`
- Test: A1 positive: same-version-start; negative: wait-rewrite-fails. A2 positive: resume-reads-report; boundary: one-shot-waits. A3 positive: one-list; negative: split-rewrite-fails. A4 positive: report-shape-kept; negative: row-shape-dropped-fails. A6 positive: rules-26; negative: no-dispatch-words.
- Risk: rewrites sentences pinned at `test_review_convergence_contract.py:74-80,250-259`; pins move to the new order, coverage preserved. Pre-report return is not a verdict; agent-decided.

**W0-02 Align the digest gate; pin the paragraph whole; graduate probes**  after: W0-01, W1-01  acceptance: 2, 6
- Files: `loom-code/skills/closing-review/SKILL.md`, `loom-code/scripts/test_parallel_acceptance_review_text.py`, `docs/loom/2026-09-24-parallel-acceptance-testing-and-review/evidence/probes/test_parallel_pin_appended_rule.py`, `docs/loom/2026-09-24-parallel-acceptance-testing-and-review/evidence/probes/test_gate_count_stale_trunk_ref.py`
- Test: A2 positive: gate-names-report-commit-in-round-1; negative: appended-reversal-fails. A6 positive: literal-gate-count; negative: stale-trunk-ref-independent.
- Risk: adversary findings: §3's single-digest sentence contradicted the gated §4 digest definition; pins missed an appended sentence and depended on origin/main. Probes graduate; agent-decided.

### Wave 1 — release

**W1-01 Minor release metadata 3.14.0**  after: W0-01  acceptance: 5, 6
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/scripts/test_write_plan_station_text.py`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`
- Test: A5 positive: changelog-names-parallel-start; negative: no-readme-names-3.13.0-as-current. A6 positive: versions-synchronized-3.14.0; negative: check-mechanisms-not-raised.
- Risk: `test_write_plan_station_text.py` pins 3.13.0; rewritten, coverage preserved. Root `README.md` version edited in the same commit; minor because station guidance changes; agent-decided.

## Questions asked
① — what — 開 acceptance testing 和 reviewer 同時跑 的 intent 吧
① — consequence — reviewer 還要不要讀 acceptance testing 報告？（A 不讀／B 第 2 輪讀／C 有修正輪才讀／D 同一輪讀）
① — what — 有辦法基於使用 loom 開發的專案的 session 記錄來評估嗎
① — consequence — 那就做 D 方案吧
① — done — 對

## Risks
1. Acceptance 5 is behavioural; independent acceptance testing proves it with seeded closing-review trials under `claude -p --plugin-dir`, branch against trunk, per the user's standing dogfood request.
2. A second-vendor reviewer run as a one-shot CLI cannot be resumed; it starts after the report commits, so that slot keeps today's order; agent-decided.
3. user-decided — reviewers keep reading the acceptance test report inside Round 1 (option D), because session history showed 7 of 8 important report errors were invisible to a report-only reader.
