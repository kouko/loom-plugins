# Bounded research and active simplification — plan
intent: 2026-11-12-design-research-method-selection@6869846f
spec: docs/loom/2026-11-12-design-research-method-selection/spec.md@282020e9
charter: 1.1

## Task DAG

### Wave 6 — design-owned simplification

**W6-01 Actively simplify material design proposals** after: none acceptance: 1, 2, 3, 4, 5, 6, 7
- Files: loom-design/skills/design-research/SKILL.md (entry), docs/loom/2026-11-12-design-research-method-selection/evidence/design-simplification-cases.md
- Test: A1 positive: permitted-inquiry; boundary: excluded-study. A2 positive: sufficient-reuse; boundary: quota. A3 positive: supported-claim; boundary: unknown. A4 positive: design-owned; boundary: feasibility. A5 positive: saved-reason; boundary: stale-record. A6 positive: actual-output; boundary: text-only. A7 positive: smaller-equivalent; boundary: necessary-complexity.
- Risk: agent-decided — REQ-1–7; preserve existing packaging checks and scope/record safeguards. Pure prose needs meaningful native executions, not keyword tests. Add one positive and one boundary proposal fixture; reuse the existing adequate-evidence case.

### Wave 7 — engineering-owned simplification

**W7-01 Actively simplify material engineering proposals** after: W6-01 acceptance: 6, 7
- Files: loom-code/skills/engineering-research/SKILL.md (entry), loom-code/skills/engineering-research/references/evaluation-selection.md, docs/loom/2026-11-12-design-research-method-selection/evidence/engineering-simplification-cases.md
- Test: A6 positive: retained-output; boundary: unsupported-claim. A7 positive: fewer-dependencies; boundary: mandatory-controls. Run existing engineering research package checks; actual native cases are separate from packaging.
- Risk: agent-decided — REQ-6/7; integrate existing alternatives guidance without repeating a new procedure in the reference. Preserve permission, evidence and investigation boundaries; no production experiments or additional framework requirement.

### Wave 8 — code release packet

**W8-01 Release code-owned research guidance** after: W7-01 acceptance: 6, 7
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-code/plugin.json, loom-code/package.json, loom-code/CHANGELOG.md, loom-code/README*.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A6 positive: version-match; boundary: stale-pin. A7 positive: version-match; boundary: stale-pin. Existing synchronization test RED before metadata update, then GREEN.
- Risk: agent-decided — REQ-6/7; bump code 3.70.0 to 3.71.0 minor and derive mirrors through sync_codex_manifests.py. Preserve all existing release-test assertions; do not change timeout fixtures or worker settings.

### Wave 9 — design release note

**W9-01 Include simplification in the unshipped design release** after: W8-01 acceptance: 1, 2, 3, 4, 5, 6, 7
- Files: loom-design/CHANGELOG.md
- Test: Existing design release synchronization and packaging checks; keep 2.25.0 across all metadata and include the new guidance in its existing unreleased entry.
- Risk: agent-decided — REQ-1–7; no second minor increment for the same unpublished PR. Existing documentation versions and derived manifests remain synchronized.

## Simplicity check
- none found

## Questions asked
① — what — 以上是否就是你要的範圍？
① — what — 是否確認本次兩個 skill 都納入這項簡化責任？

## Risks
1. agent-decided — REQ-7 and expanded REQ-6 are newly confirmed obligations. Retain earlier work/evidence only where applicable; new behavioral cases must establish active simplification and necessary-complexity preservation in each owner.
2. agent-decided — Prior fixture experiments were withdrawn; original timeout tests remain exact trunk bytes. Their intermittence remains unresolved. Preserve failed-task counts; this feature is not authorization to reopen fixture repair.
3. agent-decided — Publication remains unapproved. Local work, review or saved metadata never supplies GitHub egress or merge consent.
4. agent-decided — Main workflow callers, templates and field schemas stay unchanged. The two skills keep independent ownership; do not introduce a shared runtime helper, station or automatic critique dispatch.
5. agent-decided — Existing small-sample and non-blind case limitations remain. New controlled executions support only their tested contexts; full package suite and independent closing review remain required.
