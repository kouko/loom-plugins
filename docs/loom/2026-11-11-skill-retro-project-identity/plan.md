# Skill-retro project identity — plan
intent: 2026-11-11-skill-retro-project-identity@ad8f5e4a
spec: docs/loom/2026-11-11-skill-retro-project-identity/spec.md@bfb1757b
charter: 1.1

## Task DAG
### Wave 1
**W1-01 Preserve and resolve invocation project identity** after: none acceptance: 1,2
- Files: loom-workflow/skills/skill-retro/scripts/ingest.py (entry: ingest_claude_jsonl and ingest_codex_jsonl), loom-workflow/skills/skill-retro/scripts/event.py, loom-workflow/tests/skill-retro/test_ingest.py
- Test: A1 positive: known-repository-events; boundary: worktree-context-switch. A2 positive: missing-context-unknown; boundary: failed-git-unknown.
- Risk: agent-decided — REQ-1/2 design; preserve test_ingest.py observable-content coverage while extending metadata cases; no session identity or invocation detection change.

### Wave 2
**W2-01 Count known projects and disclose missing attribution** after: W1-01 acceptance: 1,2,3
- Files: loom-workflow/skills/skill-retro/scripts/aggregate.py (entry: aggregate_by_skill and fingerprint_count), loom-workflow/skills/skill-retro/scripts/main.py (entry: main), loom-workflow/tests/skill-retro/test_aggregate.py, loom-workflow/tests/skill-retro/test_main_e2e.py, loom-workflow/skills/skill-retro/references/runtime-protocol.md
- Test: A1 positive: cli-distinct-projects; boundary: cli-shared-worktrees. A2 positive: cli-unknown-disclosure; boundary: partial-map-unknown. A3 positive: cli-binding-top-one; boundary: mixed-project-session-provenance.
- Risk: agent-decided — REQ-1/2/3 design; preserve test_aggregate.py and test_main_e2e.py behaviors except invalid missing-project assumptions; test actual CLI, retain source locations and unknown-score limitations.

### Wave 3
**W3-01 Synchronize workflow release metadata** after: W2-01 acceptance: 1,2,3
- Files: loom-workflow/.claude-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/README*.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py, scripts/sync_codex_manifests.py (invoke only; generated manifests)
- Test: A1 positive: release-metadata-sync; boundary: mismatched-version. A2 positive: release-metadata-sync; boundary: mismatched-version. A3 positive: release-metadata-sync; boundary: mismatched-version.
- Risk: agent-decided — minor 5.21.0 for added output fields; include CHANGELOG entry and pin-test rewrite before closing review.

## Simplicity check
- none found

## Questions asked
① — what — 確認照這個範圍實作嗎？

## Risks
1. Unknown attribution can lower cross-project scores; disclose it without changing weights. Duplicate sessions and the separately reproduced threshold-override bug remain out of scope.
2. Git lookup observes current filesystem identity; deleted or reused historical paths cannot establish historical identity. Never reconstruct identities from names or remotes.
3. The earlier Claude review covered the proposal only; no authorization for another paid external review is inferred. Current spec review passed independently before this plan.
