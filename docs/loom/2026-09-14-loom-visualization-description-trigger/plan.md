# Trigger loom-visualization when Loom stations report to the user, by description only — plan
intent: 2026-09-14-loom-visualization-description-trigger@5cf73116
charter: 1.0

## Current State Evidence
- Forward: `loom-workflow/skills/loom-visualization/SKILL.md:3-4` description names what the skill draws but no moment of use.
- Reverse: `scripts/test_loom_skill_description_catalog.py:128-130` caps total rendered descriptions; router row `loom-workflow/skills/using-loom-workflow/SKILL.md:24`.
- Error: blind run A8 (`docs/loom/2026-09-14-loom-visualization/blind-run-report.md`) measured comparison and flow prompts only, never Loom station reporting messages.
- Data: `docs/loom/2026-09-14-loom-visualization/evidence/a8-spec-protocol/` stream-json transcripts show Skill tool_use events usable for counting invocations.
- Boundary: hooks, trigger cards and station skill files stay untouched, e.g. `loom-workflow/hooks/visualization-card`.

## Task DAG
<!-- When a spec requirement changes after this commit, the un-landed
     tasks it touches are replaced and the reason is named in the commit
     message. Landed tasks stay as they are. -->

### Wave 1 — measure

**W1-01 Run the description A/B on Loom station reporting prompts**  after: none  acceptance: 2, 3, 4
- Files: `docs/loom/2026-09-14-loom-visualization-description-trigger/ab/protocol.md`, `docs/loom/2026-09-14-loom-visualization-description-trigger/ab/run_ab.py`, `docs/loom/2026-09-14-loom-visualization-description-trigger/ab/results.md`, `docs/loom/2026-09-14-loom-visualization-description-trigger/evidence/`
- Test: A2 positive: both-variants-run-same-fixed-prompts-and-counts-recorded; negative: variant-copy-description-differs-only-in-description. A3 positive: decision-rule-computed-from-counts; boundary: equal-counts-means-no-ship. A4 positive: candidate-text-hash-recorded; negative: hash-mismatch-detected.
- Risk: model variance at small N; fixed prompts, two runs per prompt per variant, strict greater-than rule decided before running. agent-decided.

### Wave 2 — apply or hold

**W2-01 Apply the tested description only when it won**  after: W1-01  acceptance: 1, 4, 5
- Files: `loom-workflow/skills/loom-visualization/SKILL.md`, `loom-workflow/CHANGELOG.md`, `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`
- Test: A1 positive: description-names-station-reporting-and-budget-test-passes; negative: over-budget-description-fails-catalog-test. A4 positive: shipped-text-equals-tested-hash; negative: edited-text-fails-hash-check. A5 positive: package-suite-green; boundary: no-change-when-ab-lost.
- Risk: if the A/B does not favour the new wording, this task leaves SKILL.md unchanged and records the result. agent-decided.

## Questions asked
① — what — 你要的是：只改 loom-visualization 的 description，讓 loom 站點對使用者說話時盡量用它；做對照測試，新版更常觸發才上線（覆述 5 條驗收與不做的範圍）。對嗎？
① — consequence — 回答「對」也代表授權自動發布（review 與發布檢查通過後自動推送並開 Ready PR，merge 另外決定）。
① — what — 要不要把 loom-memory 那筆經驗一起放進這個分支？（未回答，預設不放）

## Risks
1. user-decided — ship the new description only when its sessions invoke loom-visualization strictly more often than the current wording (intent Acceptance 3).
2. The A/B spends Claude quota: two variants times a fixed prompt set, each a fresh non-interactive session; kept small and recorded.
3. Session-start trigger cards are identical in both variants, so they add the same baseline to each side rather than biasing the comparison.
4. The loom-memory lesson question went unanswered; this branch does not include it (agent-decided, conservative default).
5. user-decided — 2026-09-14 kouko authorized merging origin/main (#8) into this branch to resolve the root README conflict and re-confirmed the intent, starting a new review episode scoped to that resolution.
