# Separate research ownership with small stage handoffs — plan
intent: 2026-11-12-design-code-research-routing@ed10de55
spec: docs/loom/2026-11-12-design-code-research-routing/spec.md@9ce68eef
charter: 1.1

## Task DAG

**W1-01 Implement separate research ownership and bounded stage handoffs** after: none acceptance: 1, 2, 3, 4, 5, 6
- Files: loom-design/skills/, loom-code/skills/, loom-design/tests/, loom-code/tests/, loom-code/contract/manifest.yaml, loom-code/scripts/check_mechanisms.py, docs/loom/evidence/mechanisms.yaml, loom-design/.claude-plugin/plugin.json
- Test: A1 positive: D1; negative: D3. A2 positive: C1-C5; negative: N1-N5. A3 positive: D1; boundary: D2. A4 positive: F1; negative: unsupported-superiority. A5 positive: F1; boundary: F2. A6 positive: actual-trajectories; negative: static-only.
- Risk: agent-decided — REQ-1–6 keep methods inside owned skills and stage edits short. Preserve existing ownership, evidence and verification boundaries; extend package invariants only as needed, with independent behavioral cases at acceptance.

**W2-01 Synchronize release metadata and declared capability budget** after: W1-01 acceptance: 1
- Files: loom-code/.claude-plugin/plugin.json, loom-design/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-design/CHANGELOG.md, README.md, loom-code/README*.md, loom-design/README*.md, scripts/sync_codex_manifests.py
- Test: A1 positive: synchronized-release; boundary: discoverable-design-research. Run existing metadata and manifest checks; update derived manifests and current-release pin through the established release packet.
- Risk: agent-decided — REQ-1 adds one capability with explicit budget accounting; bump code/design minor versions before review attestation. Preserve existing generated-manifest conventions and update the release pin in loom-code/tests/test_write_plan_station_text.py.

## Simplicity check

- none found

## Questions asked

① — what — 這是否就是你要的範圍？

## Risks

1. agent-decided — Research invocation alone does not establish good judgment. Behavioral verification must inspect actual supported choices, follow-up responses and saved records against REQ-4–6.
2. agent-decided — Add no global router, new artifact type, trigger ledger or mandatory evaluation checklist; existing stage and research records carry the handoff.
3. agent-decided — Existing engineering research ownership and portable plugin boundaries remain protected; design research is separately discoverable without reading code-plugin internal resources.
4. user-decided — Research owns detailed methods, comparison and conclusion maintenance; original stages stay as simple as possible.
5. agent-decided — Full package suite follows kickoff defaults; installed plugin behavior and model-wide activation rates remain outside claims unless actually measured.
6. agent-decided — W2 includes new CHANGELOG entries, README versions, derived manifest synchronization and CURRENT_VERSION pin rewrite; do not claim a release before review and publication evidence.
