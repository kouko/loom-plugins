# Close the open follow-ups left by the last four loom changes — plan
intent: 2026-09-24-loom-follow-up-cleanup@8e254478
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/closing-review/SKILL.md:292-301` scopes the fix list to findings "on the current functional-content digest".
- Reverse: `loom-code/agents/acceptance-tester.md:75` expects dismissed important findings from the station; `closing-review/SKILL.md:218-221` lists no such input.
- Error: `probes/test_recovery_rules.py:84-87,343` still expect the expert-mode skip sentence #43 replaced with "follows the plain-words rule in §1".
- Data: `test_fix_handoff_text.py:96` and `test_fix_scope_text.py:81` pin the rule count 26; checker tests already pin it.
- Boundary: `loom-code/agents/implementer.md:27-30` returns BLOCKED for more than one distinct assertion, next to the fix hand-off scope sentence.

## Task DAG

### Wave 0 — the follow-ups

**W0-01 Closing-review fix-list scope and tester dismissal input**  after: —  acceptance: 1, 2, 7
- Files: `loom-code/skills/closing-review/SKILL.md`, `loom-code/scripts/test_fix_handoff_text.py`, `loom-code/scripts/test_fix_scope_text.py`
- Test: A1 positive: list-names-report-read-content; negative: digest-only-rewrite-fails. A2 positive: tester-gets-dismissals; negative: dismissal-input-dropped-fails. A7 positive: no-gate-marker-added; negative: no-dispatch-words.
- Risk: rewrites the exactly pinned #49 paragraph; pins move with it, coverage preserved. Also removes the duplicate rule-count pins in both test files (Acceptance 4); agent-decided.

**W0-02 Implementer: several instances of one class are one task**  after: W0-01  acceptance: 3, 4
- Files: `loom-code/agents/implementer.md`, `loom-code/scripts/test_fix_scope_text.py`
- Test: A3 positive: one-class-many-instances-one-task; negative: blocked-for-instances-rewrite-fails. A4 positive: no-literal-rule-count-outside-checker-tests; negative: literal-count-reintroduced-fails.
- Risk: `test_fix_scope_text.py` pins the implementer fix hand-off sentence; kept, coverage preserved. Sequential after W0-01 because both edit that test file; agent-decided.

**W0-03 Repair the stale RL-06 recovery probe**  after: —  acceptance: 5
- Files: `loom-code/skills/closing-review/probes/test_recovery_rules.py`
- Test: A5 positive: rl06-passes-on-current-prose; negative: expert-mode-skip-rewrite-fails.
- Risk: cause is a stale probe expectation after #43, not wrong prose; the probe keeps its polarity and ending checks, coverage preserved; agent-decided.

**W0-04 Record the PR #50 lesson in the repo memory store**  after: —  acceptance: 6
- Files: `docs/loom/memory/parallel-acceptance-testing-and-review-costs-more-than-it-saves.md`, `docs/loom/memory/index.md`
- Test: A6 positive: entry-and-index-line-present; negative: index-regenerated-not-hand-merged.
- Risk: the store's index format and any index check decide the write path; follow the store README; agent-decided.

**W0-05 Remove the last literal rule-count pin; graduate the probe**  after: W0-02, W0-03  acceptance: 4, 5
- Files: `loom-code/scripts/test_probes_language_policy.py`, `loom-code/scripts/test_fix_scope_text.py`, `loom-code/skills/closing-review/probes/test_recovery_rules.py`, `docs/loom/2026-09-24-loom-follow-up-cleanup/evidence/probes/test_rulecountpin_outsidecheckertests_absent.py`
- Test: A4 positive: guard-sees-far-pin; negative: exempts-only-checker-tests. A5 positive: probe-runs-from-any-cwd; boundary: repo-root-run-unchanged.
- Risk: adversary finding: the plan wrongly counted test_probes_language_policy.py as a checker test, and a six-line window missed its pin. Probe graduates; agent-decided.

### Wave 1 — release

**W1-01 Minor release metadata 3.14.0**  after: W0-01, W0-02, W0-03, W0-04  acceptance: 7
- Files: `loom-code/plugin.json`, `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/CHANGELOG.md`, `loom-code/scripts/test_write_plan_station_text.py`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`
- Test: A7 positive: versions-synchronized-3.14.0; negative: check-mechanisms-not-raised.
- Risk: `test_write_plan_station_text.py` pins 3.13.0; rewritten, coverage preserved. Root `README.md` version edited in the same commit; minor because station guidance changes; agent-decided.

## Questions asked
① — what — 剩下的項目有可以一次做完的嗎
① — what — 好
① — consequence — GitHub 規則要開
① — done — ＯＫ 做吧

## Risks
1. Acceptance 1-3 are prose rules; independent acceptance testing tries them with a seeded trial where a rule change could alter agent behaviour, per the user's standing dogfood request.
2. The recovery probes are not collected by the package suite, which is how RL-06 stayed red; collecting them is out of this intent's scope and is reported as a follow-up.
