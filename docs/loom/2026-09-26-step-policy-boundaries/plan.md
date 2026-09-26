# Step policy boundaries — plan
intent: 2026-09-26-step-policy-boundaries@66edfd0d
charter: 1.1

## Task DAG

### Wave 1 — Existing step-policy consumers
**W0-01 Repair step selection and omitted-document consumers** after: -- acceptance: 1, 2, 3, 5
- Files: loom-code/scripts/loom_checker/, loom-code/skills/, loom-code/agents/, loom-code/tests/, loom-code/contract/manifest.yaml
- Test: A1 positive: plain instruction; negative: no fabricated binding. A2 positive: omitted documents; negative: retained requirements. A3 positive: early production scope; boundary: late docs simplification. A5 positive: reuse records; negative: no new state.
- Risk: agent-decided — REQ-1/2/3/5; preserve selection-store, intake and finalization coverage, extending existing modules. Separate early selection from late committed-content verification without adding lifecycle state; keep no-plan dispatch grounded in intent.

### Wave 2 — Architecture consumers
**W0-02 Apply only ratified architecture rules** after: W0-01 acceptance: 4, 5
- Files: loom-code/skills/write-plan/SKILL.md, loom-code/skills/closing-review/references/lenses.md, loom-code/tests/test_architecture_doc_consumers.py, loom-design/skills/architecture-design/, loom-design/tests/architecture-design/
- Test: A4 positive: ratified enforcement; negative: draft advisory; boundary: redesign retains old guards. A5 positive: shared existing signature; negative: no new state.
- Risk: agent-decided — REQ-4/5; preserve existing architecture validator and consumer tests. Draft guards must not become active before ratification; existing ratified rules stay effective during redesign.

### Wave 3 — Release synchronization
**W0-03 Synchronize release metadata and regression pins** after: W0-02 acceptance: 5
- Files: loom-code/plugin.json, loom-code/.claude-plugin/, loom-code/.codex-plugin/, loom-code/CHANGELOG.md, loom-code/README*.md, loom-code/tests/test_write_plan_station_text.py, loom-design/, README.md
- Test: A5 positive: code 3.21.0 and design 2.6.0 synchronized; negative: stale manifests rejected.
- Risk: agent-decided — minor bumps match station guidance changes; preserve metadata checks and update only affected pins, changelog entries and README versions.

## Simplicity check
- none found

## Questions asked
- none — user accepted the presented three-item proposal and explicitly required low complexity and continued plain-language skipping.

## Risks
1. user-decided — preserve direct instructions to skip steps; do not demand expert-mode or confirmation codes.
2. agent-decided — local implementation and validation only; publication requires separate authorization.
3. agent-decided — no new persistent state, lifecycle switch, skip ledger or generalized policy framework.
4. agent-decided — extend existing tests first; at most one added regression per discovered defect; adversary reuses suite modules, reviewers run relevant tests only.
5. agent-decided — initial instruction restoration is established by focused command fixtures and independent cold-context workflow checks; do not equate text assertions with end-to-end behavior.
