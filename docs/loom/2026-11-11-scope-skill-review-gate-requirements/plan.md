# Scope skill-review gate requirements — plan
intent: 2026-11-11-scope-skill-review-gate-requirements@b5c4fc73
charter: 1.1

## Current State Evidence
- Forward: loom-code/skills/closing-review/SKILL.md, Compute review depth supplies the applicable lens to reviewers.
- Reverse: loom-code/agents/reviewer.md, lens definitions come from closing-review/references/lenses.md.
- Error: loom-code/skills/closing-review/references/lenses.md, Skill lens treats every missing gate marker as an omission without target applicability.
- Data: AGENTS.md, Quality Gates distinguishes Loom-family prose gates from other plugins' conventions.
- Boundary: loom-code/tests/test_test_budget_text.py, test_no_new_gate_marker protects the existing marker population.

## Task DAG
### Wave 1
**W1-01 Scope the existing skill lens** after: none acceptance: 1, 2, 3
- Files: loom-code/skills/closing-review/references/lenses.md, docs/loom/2026-11-11-scope-skill-review-gate-requirements/evidence/
- Test: A1 positive: external-clean; boundary: workflow-only-adoption. A2 positive: governed-missing-marker; negative: governed-marked. A3 positive: real-command-error; negative: correct-command. Cold reviewer comparison; existing test_test_budget_text.py.
- Risk: agent-decided — edit one existing paragraph; no new registry, flag, checker, or review step. Preserve test_test_budget_text.py coverage; behavioral evidence distinguishes contract applicability from artifact location.

### Wave 2
**W2-01 Release the scoped guidance** after: W1-01 acceptance: 1, 2, 3
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, README.md, loom-code/README.md, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/tests/test_write_plan_station_text.py
- Test: A1 positive: release-parity; negative: stale-manifest. A2 positive: release-parity; negative: stale-pin. A3 positive: package-suite; negative: historical-rule-regression.
- Risk: agent-decided — minor bump for station guidance; name CHANGELOG entry and rewrite affected release pins before review. Use existing synchronization, add no release mechanism.

## Simplicity check
- none found

## Questions asked
① — what — 確認按此範圍開始嗎？
① — consequence — 確認也允許審查通過後推送分支並建立 PR；合併仍另外確認，可明確選擇只留本機。

## Risks
1. agent-decided — review-verification-or-publication-mechanism: lenses.md Skill lens changes reviewer applicability; retain a governed-rule counterexample and real content error so narrowing does not erase valid findings.
2. agent-decided — semantic outcomes require cold behavioral evaluation; do not substitute wording-count assertions or full historical transcripts. Synthetic fixtures preserve the failure shape without private content.
3. user-decided — 「請注意複雜度」; keep one prose authority and existing checks. Later retrospective proposals and the other-machine invocation incident remain separate work.
4. agent-decided — no spec: internal skill/gate guidance is outside configured interface surfaces; no user-visible interface or new multi-state behavior.
