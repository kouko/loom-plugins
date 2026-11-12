# Bounded design research method selection — plan
intent: 2026-11-12-design-research-method-selection@bd14580d
spec: docs/loom/2026-11-12-design-research-method-selection/spec.md@3404c009
charter: 1.1

## Task DAG

### Wave 1

**W1-01 Bound acquisition and select useful inquiry** after: none acceptance: 1, 2, 3, 4, 5, 6
- Files: loom-design/skills/design-research/SKILL.md (entry), loom-design/skills/design-research/references/method-selection.md, docs/loom/2026-11-12-design-research-method-selection/evidence/
- Test: A1 positive: source-dialogue; boundary: excluded-activity. A2 positive: useful-method; boundary: sufficient-evidence. A3 positive: attributed-source; boundary: missing-population. A4 positive: mixed-handoff; boundary: design-only. A5 positive: revised-record; boundary: unsupported-challenge. A6 positive: retained-trials; boundary: unverified-claim.
- Risk: agent-decided — preserve existing package tests and retention contract (REQ-1–6); use real isolated agent executions with controlled fixtures before/after guidance, not keyword assertions or invented participant evidence. No production executable code changes.

### Wave 2

**W2-01 Release the bounded research guidance** after: W1-01 acceptance: 1, 2, 3, 4, 5, 6
- Files: loom-design/.claude-plugin/plugin.json, loom-design/CHANGELOG.md, loom-design/README*.md, README.md, loom-design/.codex-plugin/plugin.json, loom-design/plugin.json, loom-design/package.json, loom-design/tests/spec/test_capture_intent_contract.py
- Test: A1 positive: version-match; boundary: stale-pin. A2 positive: version-match; boundary: stale-pin. A3 positive: version-match; boundary: stale-pin. A4 positive: version-match; boundary: stale-pin. A5 positive: version-match; boundary: stale-pin. A6 positive: version-match; boundary: stale-pin. Existing release synchronization and complete package suite.
- Risk: agent-decided — REQ-1–6 ship together in loom-design minor release; no unrelated plugin bump. Check actual sync outputs and existing release pins before committing.

## Simplicity check
- Inline selection guidance instead of a separate reference when it creates no useful reading boundary — taken
- No additional smaller shape found by the independent reviewer — declined: reviewer returned PASS with no deletion findings

## Questions asked
① — what — 以上是否就是你要的範圍？

## Risks
1. agent-decided — A small controlled before/after sample supports bounded behavior only, not framework superiority, population validity or reliable performance across all future tasks.
2. agent-decided — The requested Claude Code proposal review failed preflight with no usable review; retain that limitation. Native independent specification, plan, acceptance and closing reviews remain required.
3. agent-decided — Preserve current stage callers and template; modify only design research acquisition/selection, not engineering research or station semantics.
