# Manifest repository URLs — plan
intent: 2026-09-14-manifest-repo-urls@4b76bea8
charter: 1.0

## Current State Evidence
- Forward: `loom-*/.claude-plugin/plugin.json` — `homepage` and `repository` name `kouko/monkey-skills`.
- Reverse: `loom-*/.codex-plugin/plugin.json` — `homepage`, `repository`, and `interface.websiteURL` name `kouko/monkey-skills`.
- Error: `scripts/sync_codex_manifests.py --check --all` — fails when Codex manifests drift from their Claude counterparts.
- Data: `loom-design/scripts/test_plugin_manifest.py` — reads manifest fields; must stay green.
- Boundary: `scripts/test_sync_codex_manifests.py` — exercises the sync over the three plugin roots.

## Task DAG

### Wave 1

**W1-01 Replace manifest repository URLs**  after: none  acceptance: 1, 2
- Files: loom-code/.claude-plugin/plugin.json, loom-code/.codex-plugin/plugin.json, loom-design/.claude-plugin/plugin.json, loom-design/.codex-plugin/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json
- Test: A1 positive: all-links-loom-plugins; negative: monkey-skills-link-remains. A2 positive: sync-check-and-suite-pass; negative: codex-manifest-drift.
- Risk: agent-decided — replace only the `https://github.com/kouko/monkey-skills` prefix; other fields stay byte-identical.

## Questions asked
① — what — 可以直接改 manifest 跳過 loom 流程嗎？（選項 A／B／C；答：A，之後因遠端無法執行指令改走 loom）
① — what — 把三個 plugin 的 6 份 manifest 連結改成 loom-plugins，驗收條件兩條，並授權自動 push、開 PR、CI 綠了合併；這樣對嗎？

## Risks
1. A leftover local branch `chore/manifest-repo-urls` holds an earlier unreviewed copy of this edit; it is never pushed and is superseded by this branch.
