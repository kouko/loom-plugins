# Absolute user document paths — plan
intent: 2026-11-04-absolute-user-document-paths@5a9dd3eb
charter: 1.1

## Current State Evidence
- Forward: `loom-code/hooks/session-start` injects the station guidance, without a conversation document-path rule.
- Reverse: `loom-workflow/skills/loom-visualization/references/plain-language.md` owns chat guidance but does not require absolute local document paths.
- Error: `loom-code/skills/ship/SKILL.md` hands reports to users without an explicit document-link target convention.
- Data: `loom-design/skills/capture-intent/SKILL.md` resolves bundled references relative to the skill directory; these are portable resource references.
- Boundary: `loom-workflow/skills/loom-visualization/scripts/render_cot_html.py` separately handles HTML file links; conversation guidance must preserve that artifact contract.

## Task DAG
### Wave 0
**W0-01 Standardize conversation document delivery** after: none acceptance: 1, 2, 3, 4
- Files: loom-code/hooks/session-start, loom-code/skills/, loom-design/skills/, loom-workflow/skills/, loom-code/tests/, loom-workflow/tests/
- Test: A1 positive: family-guidance; negative: uncovered-delivery. A2 positive: absolute-link-target; boundary: spaces. A3 positive: active-worktree; negative: fixed-developer-prefix. A4 positive: portable-references; negative: artifact-rewrite.
- Risk: agent-decided — use shared conversation guidance and necessary standalone entry guidance, rather than rewriting portable paths; verify emitted instructions, and explicitly distinguish instruction coverage from observed model behavior.

**W0-02 Synchronize affected plugin releases** after: W0-01 acceptance: 1
- Files: loom-code/, loom-design/, loom-workflow/, README.md, README.zh-TW.md, README.ja.md, .claude-plugin/marketplace.json, .codex-plugin/marketplace.json
- Test: A1 positive: release-metadata-synchronized; negative: stale-version-pins.
- Risk: agent-decided — minor bump for changed runtime guidance; update canonical manifests, existing changelogs and README pins, derive exported manifests, and rewrite release pin tests before final review.

## Simplicity check
- none found

## Questions asked
① — what — 以上就是你要的範圍嗎？ 若不希望自動建立 PR，也可一併說明。

## Risks
1. agent-decided — conversation links resolve against the actual document location, including worktrees and paths containing spaces; resource references and stored relative-path schemas remain portable.
2. agent-decided — no universal clickability claim across hosts; use supported absolute Markdown targets, otherwise absolute text paths. User authorization covers publication, with merge separate.
3. user-decided — confirmed 2026-11-04: all conversation local document locations use absolute paths; portable internal references remain relative.
