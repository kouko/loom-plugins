# Project session retro — plan
intent: 2026-10-13-project-session-retro@cbc82996
charter: 1.1

## Current State Evidence
- Forward: `loom-workflow/skills/using-loom-workflow/SKILL.md` "Select the matching skill" routes session mining to `distill-sessions`.
- Reverse: `loom-workflow/skills/distill-sessions/SKILL.md` "Render proposals" turns repeated session evidence into existing Skill proposals.
- Error: `loom-workflow/skills/distill-sessions/SKILL.md` "Do not use it for" excludes single-session reflection.
- Data: `loom-workflow/tests/scripts/test_skill_count.py` `test_twelve_skill_directories_ship` pins directories and manifest membership.
- Boundary: `loom-workflow/README.md` "Admission rule" needs an explicit exception for this user-approved on-demand tool.

## Task DAG

**W1-01 Define the single-session retro contract**  after: none  acceptance: 1, 2
- Files: `loom-workflow/skills/retro/SKILL.md`, `loom-workflow/tests/retro/test_skill_contract.py`
- Test: A1 positive: ranked-source-anchored-advice; boundary: missing-source-limit. A2 positive: project-versus-skill-candidates; negative: no-write-or-single-session-promotion.
- Risk: agent-decided — keep the skill read-only and on-demand; do not import Matt's repo-specific document assumptions or build a log-ingestion pipeline.

**W2-01 Register and route the standalone tool**  after: W1-01  acceptance: 3
- Files: `loom-workflow/skills/using-loom-workflow/SKILL.md`, `loom-code/contract/manifest.yaml`, `loom-workflow/tests/scripts/test_skill_count.py`, `loom-code/tests/test_contract_manifest.py`, `tests/test_loom_skill_description_catalog.py`, `loom-workflow/tests/retro/test_routing.py`, `loom-code/tests/test_opencode_loader.py`
- Test: A3 positive: retro-and-distill-routes; negative: distill-contract-unchanged.
- Risk: agent-decided — register retro as standalone outside the station budget; keep mechanism counts unchanged because standalone tools are excluded.

**W2-02 Document the tool**  after: W2-01  acceptance: 3
- Files: `loom-workflow/README.md`, `loom-workflow/README.zh-TW.md`, `loom-workflow/README.ja.md`, `README.md`, `tests/test_agy_install_docs.py`
- Test: A3 positive: published-skill-catalog; boundary: existing-distill-entry.
- Risk: agent-decided — name this user-approved single-session project review as an explicit standalone admission exception and set the new plugin version in all four READMEs.

**W3-01 Synchronize release metadata**  after: W2-02  acceptance: 3
- Files: `loom-workflow/plugin.json`, `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`, `loom-workflow/package.json`, `loom-workflow/CHANGELOG.md`, `loom-workflow/tests/scripts/test_release_metadata.py`
- Test: A3 positive: version-and-changelog-sync; boundary: prior-distill-version-record.
- Risk: agent-decided — bump loom-workflow minor version for new skill and keep historical distill entries unchanged.

## Simplicity check
- Omit a log-ingestion program — taken
- Omit `mechanisms.yaml` entry — taken

## Questions asked
① — what — 這正是你要的嗎？

## Risks
1. Session logs may contain secrets. Local tool output enters the current model context and may reach its host. For specified transcripts, redact before tool output when feasible; otherwise request a redacted excerpt or state the limit. Quote minimally.
2. Release metadata and documentation must be synchronized before closing review; W2-02 owns the bump.
