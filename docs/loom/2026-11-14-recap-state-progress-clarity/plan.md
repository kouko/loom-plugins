# Recap progress clarity — plan
intent: 2026-11-14-recap-state-progress-clarity@303b11b65
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/recap-state/SKILL.md`, What to do 2, grounds purpose, current position and remaining gap without explicit implementation-versus-delivery distinctions.
- Reverse: `loom-workflow/skills/recap-state/references/seven-block-schema.md`, L3 user-visible template, already requires language continuity, grounded purpose and waiting.
- Error: `loom-workflow/tests/recap-state/test_skill_md.py`, test_skill_requires_source_for_past_decisions, guards source grounding but not release-state clarity or cross-day timing.
- Data: `loom-workflow/tests/recap-state/test_seven_block_schema.py`, test_good_example_demonstrates_long_session_orientation, preserves the existing flexible example; new cases must use synthetic conversations.
- Boundary: `docs/loom/KICKOFF-DEFAULTS.md`, interface-surfaces, classifies skill contracts as engineering; heading frames and confirmation boundaries remain unchanged.

## Task DAG
### Wave 1
**W1-01 Clarify progress grounding and add behavioral cases** after: none acceptance: 1,2,3,4,5
- Files: `loom-workflow/skills/recap-state/SKILL.md`, `loom-workflow/skills/recap-state/references/seven-block-schema.md`, `loom-workflow/skills/recap-state/README*.md`, `loom-workflow/tests/recap-state/test_skill_md.py`, `loom-workflow/tests/recap-state/behavior_cases.json`
- Test: A1 positive: implemented-unmerged; negative: unknown-delivery. A2 positive: known-purpose-language; negative: purpose-reinterview. A3 positive: scoped-tests; negative: premature-readiness. A4 positive: resumed-date; negative: fabricated-today. A5 positive: aligned-pause; boundary: unknown-purpose. Existing recap suite; independent native behavioral execution.
- Risk: agent-decided — use conditional grounding examples, not a mandatory checklist. Preserve all existing `test_skill_md.py`, `test_seven_block_schema.py` and `test_readmes.py` coverage; widen with contract RED/GREEN and independently judged synthetic outputs.

### Wave 2
**W2-01 Synchronize release metadata** after: W1-01 acceptance: 1,2,3,4,5
- Files: `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`, `loom-workflow/plugin.json`, `loom-workflow/package.json`, `loom-workflow/CHANGELOG.md`, `loom-workflow/README*.md`, `README.md`, `loom-workflow/tests/scripts/test_release_metadata.py`
- Test: A1 positive: synced-release; negative: stale-release. A2 positive: synced-release; negative: stale-release. A3 positive: synced-release; negative: stale-release. A4 positive: synced-release; negative: stale-release. A5 positive: synced-release; negative: stale-release. Manifest synchronization and complete package inventory.
- Risk: agent-decided — minor bump 5.24.0 for skill guidance; derive mirrors, add changelog and preserve every current-release pin assertion in `test_release_metadata.py`. The complete suite exposed the initially omitted pin; this is the same release task, first integration fix.

## Simplicity check
- Extend existing contract tests instead of adding a separate prose test module — taken

## Questions asked
① — what — 確認這個範圍嗎？

## Risks
1. Historical evidence motivates cases, not a claim that current hosts fail them. Native execution verifies actual outputs separately from contract assertions; use synthetic inputs and publish no raw transcripts.
2. agent-decided — no new model harness or permanent executor, no mandatory Git/remote audit, no layout changes. Cases live in existing tests; behavioral outputs and independent grading live in change evidence.
3. agent-decided — user confirmed engineering scope and automatic non-forced push/Ready PR on 2026-11-14; merge and local installation remain unauthorized.
4. Behavioral success on native agents is bounded evidence, not proof of installed Codex, Claude Code or OpenCode runtime behavior. Preserve unknown version and host coverage explicitly.
