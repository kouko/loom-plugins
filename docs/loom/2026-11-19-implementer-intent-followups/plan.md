# Implementer intent hand-off follow-ups — plan
intent: 2026-11-19-implementer-intent-followups@f5ad61c
charter: 1.1

## Current State Evidence
- Forward: `loom-code/skills/build/SKILL.md` line 52 hands each agent "the retained artifact paths"; the intent is named only on the skipped-plan path.
- Reverse: `loom-code/agents/implementer.md` Resource paths already carries `- intent: {path}` (PR #169).
- Error: Codex audit of PR #169 found the planned dispatch path does not name the intent in Build.
- Data: implementer Output contract has `self_review`; Role contract 4 read-only list omits intent.
- Boundary: `loom-code/tests/test_build_mechanical_checks.py` scope pin negative deletes the sentence instead of weakening it.

## Task DAG
One wave: contract text and its pins change together; release metadata follows.

**W1-01 Close implementer intent hand-off gaps**  after: none  acceptance: 1, 2, 3, 4, 5
- Files: `loom-code/skills/build/SKILL.md`, `loom-code/agents/implementer.md`, `loom-code/tests/test_build_mechanical_checks.py`
- Test: A1 positive: build-names-intent-both-paths; negative: planned-path-intent-removed-fails. A2 positive: beyond-task-in-self-review; negative: commit-only-wording-fails. A3 positive: readonly-list-names-intent; negative: intent-dropped-from-list-fails. A4 positive: exception-task-required-only; negative: unbounded-exception-fails. A5 positive: weakened-scope-rewrite-rejected; boundary: complete-package-suite-passes.
- Risk: agent-decided — reword Build's existing hand-off sentence rather than add one; no NEEDS_CONTEXT/BLOCKED restatement (existing rule). Existing implementer pins are preserved or tightened, never narrowed.

**W1-02 Minor release metadata**  after: W1-01  acceptance: 5
- Files: `loom-code/.claude-plugin/plugin.json`, derived release manifests, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README*.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A5 positive: release-metadata-synchronized-3.87.0; boundary: readme-versions-match-manifest.
- Risk: agent-decided — minor 3.87.0 because station guidance changes; manifests derived via scripts/sync_codex_manifests.py --all.

## Simplicity check
- Reword Build's existing hand-off sentence instead of adding a new one — taken
- Whole input-block line matching test — declined: breaks on every ordinary rewording

## Questions asked
① — what — 這樣是你要的嗎？

## Risks
1. Tighter wording could conflict with existing implementer pins; W1-01 runs the whole test file before commit.
