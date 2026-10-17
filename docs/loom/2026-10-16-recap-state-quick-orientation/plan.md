# Recap state quick orientation — plan
intent: 2026-10-16-recap-state-quick-orientation@a6f0784f
spec: docs/loom/2026-10-16-recap-state-quick-orientation/spec.md@1d2063b4
charter: 1.1

## Task DAG

**W1-01 Replace the L3 recap contract**  after: none  acceptance: 1, 2, 3, 4, 5, 6
- Files: `loom-workflow/skills/recap-state/SKILL.md`, `loom-workflow/skills/recap-state/references/seven-block-schema.md`, `loom-workflow/tests/recap-state/test_skill_md.py`, `loom-workflow/tests/recap-state/test_seven_block_schema.py`
- Test: A1 positive: grounded-purpose-first; boundary: purpose-unknown. A2 positive: long-session-trajectory; negative: short-session-padding. A3 positive: framed-heading-and-topology; negative: decorative-graph. A4 positive: exact-critical-quote; negative: inferred-fact. A5 positive: final-directed-question; negative: auto-continue. A6 positive: chat-only; negative: handoff-file.
- Risk: agent-decided — replace the duplicated six-section L3 rules while preserving the historical seven-block lineage; existing schema tests must be rewritten, not silently removed.

**W2-01 Synchronize release metadata**  after: W1-01  acceptance: 3
- Files: `loom-workflow/plugin.json`, `loom-workflow/.claude-plugin/plugin.json`, `loom-workflow/.codex-plugin/plugin.json`, `loom-workflow/package.json`, `loom-workflow/CHANGELOG.md`, `loom-workflow/tests/scripts/test_release_metadata.py`
- Test: A3 positive: minor-version-and-changelog-sync; boundary: prior-version-migration-notes.
- Risk: agent-decided — bump loom-workflow to 5.10.0 because skill guidance changes; preserve historical 5.9.0 migration references.

**W3-01 Synchronize README version pins**  after: W2-01  acceptance: 3
- Files: `README.md`, `loom-workflow/README.md`, `loom-workflow/README.zh-TW.md`, `loom-workflow/README.ja.md`
- Test: A3 positive: current-version-pins; boundary: historical-migration-mentions.
- Risk: agent-decided — change current version pins only; existing recap descriptions and migration history stay intact.

## Simplicity check
- Replace the six-section runtime rules in place — taken
- Keep historical lineage in the existing reference bundle — taken
- Extend existing recap tests instead of adding a duplicate contract test — taken
- Omit separate plugin README copy changes; update only release pins — taken

## Questions asked
① — what — 若符合你的意思，請回覆「確認」。

## Risks
1. Markdown may collapse ordinary blank lines or print HTML tags; use one fullwidth-space-only line between sections and inspect the rendered chat preview.
2. The `■` glyph has ambiguous terminal width; generate and verify CJK frames through `loom-visualization`, and avoid claiming cross-terminal alignment beyond its width policy.
3. Codex Mermaid rendering is unverified; use a table or ASCII for meaningful topology in this client, following `loom-visualization`.
