# Titled before/after flow illustration — plan
intent: 2026-11-03-titled-flow-comparison@c0d04d5393b3402e90a1d09fa1cb10b2c4338400
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/loom-visualization/SKILL.md` routes linear flows to the existing template.
- Reverse: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md` contains one generated flow, without titled comparison panels.
- Error: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md` has no reusable comparison composition with in-frame titles; the approved example currently lives only in conversation.
- Data: `loom-workflow/tests/loom-visualization/test_templates.py` verifies template structure, generated examples and ASCII alignment.
- Boundary: `loom-workflow/.claude-plugin/plugin.json` is version 5.19.1 at baseline `ae4f92e4629bf19b16784ee0f798047b99626499`; confirmation contracts are excluded.

## Task DAG

**W0-01 Save the approved comparison illustration** after: none acceptance: 1,2,3,4
- Files: `loom-workflow/skills/loom-visualization/templates/02-linear-steps.md`, `loom-workflow/skills/loom-visualization/SKILL.md`
- Test: A1 positive: titled-panels; boundary: unequal-topology. A2 positive: expected-state-title; negative: unverified-as-fact. A3 positive: reproduced-parallel; boundary: stacked-narrow. A4 positive: visualization-only; negative: confirmation-contract-change.
- Risk: agent-decided — retain the existing renderer and width helper; save a documentation recipe rather than introducing a generator. Verify both completed compositions, including the outer frames.

**W0-02 Prepare the independent patch release** after: W0-01 acceptance: 4
- Files: `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`, `loom-workflow/plugin.json`, `loom-workflow/package.json`, `loom-workflow/CHANGELOG.md`, `loom-workflow/README*.md`, `README.md`
- Test: A4 positive: synchronized-workflow-release; negative: unrelated-plugin-bump.
- Risk: agent-decided — release workflow 5.19.2 as a documentation patch; synchronize derived manifests from the Claude source and update version references. No station, field, rule or contract-manifest change is included.

## Simplicity check
- Extend the existing linear-flow template instead of adding a shape or generator — taken

## Questions asked
- none — the user explicitly selected the previously described independent release: 「只釋出圖表樣板」.

## Risks
1. User-decided — publish only the graph template; merge remains separate. This independently approved documentation outcome preserves the other change's review and retry history.
2. Agent-decided — mechanical reproduction establishes layout and recipe accuracy, not automatic selection quality or improved human comprehension in every host.
3. Agent-decided — existing scripts and tests are sufficient for this documentation-only example; no new sentence-pin test or executable production behavior is introduced.
