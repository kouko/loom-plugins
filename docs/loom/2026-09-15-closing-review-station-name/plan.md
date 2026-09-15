# closing-review station name — plan
intent: 2026-09-15-closing-review-station-name@df61fda3
charter: 1.0

## Current State Evidence
- Forward: `loom-code/skills/write-plan/SKILL.md:254,357,443,522` — prose names "the review station" after the station became `closing-review`.
- Reverse: `loom-code/contract/manifest.yaml:17` — `{name: closing-review, owner: loom-code, produces: attestation}` is the only station id.
- Error: `loom-code/agents/blind-runner.md:3` — the agent description says it is dispatched "by the review station"; `loom-code/agents/reviewer.md:30` repeats it.
- Data: `loom-design/skills/write-spec/SKILL.md`, `references/spec-forms.md`, `references/ui-flows.md`, `design-system/references/knowledge-triage.md` — six more "review station" mentions.
- Boundary: gate ids such as `review.bounded-episode`, `finalize-review`, and lens names stay internal ids per the #8 plan and must not change.

## Task DAG

### Wave 1

**W1-01 Rename station references in loom-code prose**  after: none  acceptance: 1, 2, 3
- Files: loom-code/skills/write-plan/SKILL.md, loom-code/skills/write-plan/references/second-vendor-ask-and-docs-lint.md, loom-code/agents/blind-runner.md, loom-code/agents/reviewer.md
- Test: A1 positive: no-review-station-in-loom-code; negative: review-station-remains. A2 positive: diff-only-station-name; boundary: gate-ids-unchanged. A3 positive: suite-green; negative: skill-description-catalog-drift.
- Risk: agent-decided — replace only station-naming phrases; generic "review" and internal ids stay; agent description changes may touch description-catalog tests.

**W1-02 Rename station references in loom-design prose**  after: W1-01  acceptance: 1, 2, 3
- Files: loom-design/skills/write-spec/SKILL.md, loom-design/skills/write-spec/references/spec-forms.md, loom-design/skills/write-spec/references/ui-flows.md, loom-design/skills/design-system/references/knowledge-triage.md
- Test: A1 positive: no-review-station-in-loom-design; negative: review-station-remains. A2 positive: diff-only-station-name; boundary: lens-names-unchanged. A3 positive: suite-green; negative: skill-token-budget-exceeded.
- Risk: agent-decided — sequential after W1-01 to avoid concurrent commits in one tree; same wording rule.

### Wave 2

**W2-01 Close adversary findings on remaining station names**  after: W1-02  acceptance: 1, 2, 3
- Files: loom-code/skills/ship/SKILL.md, loom-code/skills/build/SKILL.md, loom-code/skills/closing-review/SKILL.md, loom-code/skills/expert-mode/SKILL.md, loom-code/skills/write-plan/SKILL.md, loom-design/skills/capture-intent/SKILL.md, loom-code/scripts/loom_checker/rule_checks/standing.py, scripts/test_loom_plugin_install_layout.py
- Test: A1 positive: adversary-probes-all-pass; negative: capitalized-review-station-noun. A2 positive: reword-reverts-to-base; boundary: generic-review-words-kept. A3 positive: suite-green; negative: install-layout-pin-weak.
- Risk: agent-decided — capitalised "Review" naming the station is the old name under Proposed outcome; also loom-design/.codex-plugin/plugin.json longDescription; generic "Review policy" wording stays.

## Questions asked
① — what — 你要把 loom-code 和 loom-design 裡還寫著「review station」的地方全部改成 closing-review（12 處、只換站名、測試全過），並授權自動 push 開 PR、合併走 land 並在檢查綠了後請你回「接受」；這樣對嗎？
① — what — 我們已經非常確定那些的確是寫錯的嗎？（使用者追問；答：先改站名，然後再做補上 lane 缺口）

## Risks
1. The initial scan found 12 mentions; a line-wrap-aware scan found 16 in 8 files. Implementers must rescan with the same wrap-aware method before and after editing.
2. Publication was not explicitly re-authorized after the user's follow-up question, so the intent carries no `publication:` line; ship asks for one publication decision.
