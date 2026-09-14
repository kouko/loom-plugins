# loom-workflow script paths and cross-host trigger card — plan
intent: 2026-09-14-agy-skill-script-paths@cbdace97
charter: 1.0

## Current State Evidence
- Forward: `loom-workflow/skills/loom-visualization/SKILL.md:24,68,98,113` and `goal-create/SKILL.md:29` run bundled scripts as bare `python3 scripts/...`, resolved against the agent's working directory.
- Reverse: `loom-workflow/hooks/hooks.json:3-9` injects the trigger card only through Claude Code SessionStart (`hooks/visualization-card:106` picks `trigger-card.md` or the coexist card).
- Error: `loom-code/scripts/check_contract_citations.py:285-307` flags only `${CLAUDE_PLUGIN_ROOT}` without fallback; bare relative script paths pass unflagged.
- Data: `loom-workflow/.codex-plugin/plugin.json` declares no `hooks`; `loom-workflow/hooks.json` (agy) carries only the skill-folder PreToolUse rule.
- Boundary: spikes 2026-09-14 — agy plugin `rules/AGENTS.md` is always on and ignored by Claude Code; Codex skips plugin hooks until the user trusts them.

## Task DAG

### Wave 1

**W1-01 Skill-relative script paths in loom-workflow skills**  after: none  acceptance: 1
- Files: loom-workflow/skills/loom-visualization/SKILL.md, loom-workflow/skills/loom-visualization/references/, loom-workflow/skills/loom-visualization/templates/, loom-workflow/skills/goal-create/SKILL.md, loom-workflow/skills/loom-visualization/scripts/test_skill_script_paths.py
- Test: A1 positive: skill-dir-phrase-defined-and-used-for-every-script-call; negative: bare-scripts-path-left-in-skill-doc.
- Risk: agent-decided — reuse the adopted hybrid wording (Claude Code `${CLAUDE_SKILL_DIR}`, other hosts the folder holding this SKILL.md); references and templates point back to that definition instead of counting levels.

**W1-02 Lint rejects bare bundled-script paths**  after: W1-01  acceptance: 2
- Files: loom-code/scripts/check_contract_citations.py, loom-code/scripts/test_check_contract_citations.py
- Test: A2 positive: bare-python3-scripts-command-flagged; negative: skill-dir-anchored-command-not-flagged.
- Risk: agent-decided — extend the existing contract lint scope rather than add a tool; cover python3/bash/sh and `./scripts/` forms, including fenced code, since agents copy commands from fences.

### Wave 2

**W2-01 Trigger card as an agy plugin rule**  after: none  acceptance: 3, 4
- Files: loom-workflow/rules/AGENTS.md, scripts/sync_codex_manifests.py, scripts/test_sync_codex_manifests.py, loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md
- Test: A3 positive: agy-rule-matches-trigger-card-source; negative: drifted-agy-rule-fails-check. A4 positive: claude-hook-still-injects-card-once; boundary: claude-ignores-plugin-rules-dir.
- Risk: agent-decided — plugin `rules/AGENTS.md` proven always-on in agy and ignored by Claude Code; generate it from `trigger-card.md` in the existing sync script so the card keeps one source.

**W2-02 Trigger card through a Codex SessionStart hook**  after: W2-01  acceptance: 3, 4
- Files: loom-workflow/hooks/hooks-codex.json, loom-workflow/.codex-plugin/plugin.json, scripts/sync_codex_manifests.py, scripts/test_loom_plugin_install_layout.py, loom-workflow/hooks/visualization-card, loom-workflow/README.md
- Test: A3 positive: codex-manifest-points-at-sessionstart-card-hook; negative: codex-hook-without-plugin-root-rejected. A4 positive: claude-selects-only-hooks-json; boundary: codex-card-falls-back-to-full-card.
- Risk: agent-decided — Codex runs plugin hooks only after the user trusts them (official hooks docs), so the README states the trust step; reuse the existing card script with `PLUGIN_ROOT`.

## Questions asked
① — what — 這次要不要順便讓 Codex 也收到這張提醒卡？（現在 Codex 上完全收不到，跟 agy 修之前一樣）（答：agy 和 Codex 都做）
① — what — 上面「你要的是」這四點和不包含的範圍都對嗎？（回答對，也等於授權審查通過後自動 push 並開 PR；merge 另外決定）（答：對）

## Risks
1. user-decided — deliver the trigger card to Codex as well as agy in this change.
2. Codex blind-run verification needs the plugin hook trusted in Codex; if no non-interactive trust exists, the report records that step as a user action.
3. Model compliance with the card varies by host model; acceptance checks card delivery, not whether a model then draws a diagram.
