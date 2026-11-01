# Project and installed-skill retrospectives — plan
intent: 2026-10-14-project-and-skill-retro@92972244d56b34724597e5b0ed217c6f9ba8f66e
spec: docs/loom/2026-10-14-project-and-skill-retro/spec.md@9661756b
charter: 1.1

## Task DAG

### Wave 1 — Evidence and proposal contracts

**W1-01 Project retrospective scope and name**  after: none  acceptance: 1, 3
- Files: `loom-workflow/skills/project-retro/SKILL.md`, `loom-workflow/tests/project-retro/`, `loom-workflow/skills/retro/SKILL.md`, `loom-workflow/tests/retro/`
- Test: A1 positive: source-linked project proposal; boundary: reusable-tool candidate only. A3 positive: review-only output; negative: no project or agent-file write.
- Risk: agent-decided — preserve one-session privacy and evidence checks; REQ-1/3 limit project outputs and writes. Existing `test_skill_contract.py` and `test_routing.py` must retain their exercised cases.

**W1-02 Cross-session item classification and rendering**  after: none  acceptance: 2, 3
- Files: `loom-workflow/skills/skill-retro/agents/`, `loom-workflow/skills/skill-retro/references/`, `loom-workflow/skills/skill-retro/scripts/`, `loom-workflow/tests/skill-retro/`, `loom-workflow/skills/distill-sessions/`, `loom-workflow/tests/distill-sessions/`
- Test: A2 positive: repeated sourced integration proposal; boundary: one-session pending and missing source. A3 positive: reviewable handoff; negative: no target write or apply path.
- Risk: agent-decided — update prompts, merged-item schema, classification, clustering, renderer and tests together; REQ-2/3. Preserve old ingestion/privacy coverage while retiring tested `apply.py` behavior.

### Wave 2 — Public discovery and release

**W2-01 Route and release the direct migration**  after: W1-01, W1-02  acceptance: 4
- Files: `loom-workflow/skills/using-loom-workflow/SKILL.md`, `loom-workflow/**/plugin.json`, `loom-workflow/package.json`, `loom-workflow/README*.md`, `loom-workflow/CHANGELOG.md`, `loom-workflow/tests/`, `loom-code/contract/manifest.yaml`
- Test: A4 positive: new names route and 5.9.0 metadata matches; negative: old names absent as callable entries, migration map present, and full suite discovers renamed tests.
- Risk: agent-decided — update public routes, docs and version together under REQ-4. Retain historical changelog mentions; bump before final review so attestation binds release content.

### Wave 3 — Keep caught regressions in the permanent suite

**W3-01 Graduate the two RED adversarial cases**  after: W2-01  acceptance: 2
- Files: `docs/loom/2026-10-14-project-and-skill-retro/evidence/probes/`, `loom-workflow/tests/skill-retro/`
- Test: A2 positive: same-named skills remain isolated; boundary: one-session deferred item remains pending.
- Risk: agent-decided — both probes caught actual defects under REQ-2; move their assertions into package-discovered tests before finalization without weakening either case.

## Simplicity check

- Merge public routing and release metadata into one task — taken

## Questions asked

① — what — Prior intent confirmation asked whether the four Acceptance outcomes and direct migration match the desired scope; the user answered 「對」 on 2026-10-15. Exact earlier question wording is unavailable after context compaction.

## Risks

1. Existing tests refer to old skill paths; move or rewrite them without silently dropping exercised ingestion, privacy, approval, and proposal cases.
2. Installed plugin caches may still expose old names until users update; migration notes must distinguish source release from installed state.
3. Dependent connector failures may be inferred from session evidence alone; require a source pointer or label a bounded investigation candidate.
