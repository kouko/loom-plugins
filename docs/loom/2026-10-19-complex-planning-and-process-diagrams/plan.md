# Complex planning and process diagrams — plan
intent: 2026-10-19-complex-planning-and-process-diagrams@b143043
spec: docs/loom/2026-10-19-complex-planning-and-process-diagrams/spec.md@4bbb0cd
charter: 1.1

## Task DAG

Wave 1 — new shapes and their routing

**W1-01 Add dependency and cross-role templates**  after: none  acceptance: 1, 2, 3
- Files: loom-workflow/skills/loom-visualization/SKILL.md, loom-workflow/skills/loom-visualization/references/node-structure.md, loom-workflow/skills/loom-visualization/scripts/checks_kink.py, loom-workflow/skills/loom-visualization/templates/12-task-dependencies.md, loom-workflow/skills/loom-visualization/templates/13-cross-role-workflow.md, loom-workflow/tests/loom-visualization/test_ascii_cli.py, loom-workflow/tests/loom-visualization/test_templates.py
- Test: A1 positive: parallel-prerequisites-join; negative: choice-is-not-join. A2 positive: role-owned-handoff; negative: message-only-sequence. A3 positive: forms-align-and-parse; negative: misaligned unboxed join and handoff connectors; boundary: existing-eleven-shapes-and-generator-inputs.
- Risk: agent-decided — apply REQ-1–3 without adding a generator; preserve existing routing and extend the standalone-title rule to both shapes. Existing template tests protect the old eleven shapes.

Wave 2 — synchronized plugin release metadata

**W2-01 Bump loom-workflow minor version**  after: W1-01  acceptance: 3
- Files: loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/package.json, loom-workflow/CHANGELOG.md, loom-workflow/README*.md, README.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A3 positive: synchronized-new-minor-version; negative: stale-manifest-or-readme-pin.
- Risk: agent-decided — new skill routing and templates require a minor release; choose the next unused minor version after checking trunk, then bump before final attestation.

## Simplicity check
- none found

## Questions asked
① — what — 你要的範圍是否是：先完成兩種複雜圖型範例，讓人看清任務的並行與匯合、不同角色的工作與交接；接著完成簡單的靜態 UI 線框圖，讓人看清畫面區塊與控制項的相對位置？若確認，我會按兩項變更分別驗證並建立 PR，合併仍由你決定。
① — what — 這次先交付兩種複雜圖型範本：一種讓人看出任務的前置條件、並行與匯合；一種讓人看出不同角色負責的步驟與交接。UI 線框圖留待下一項。這是你要的結果嗎？若確認，驗證通過後我會建立這項變更的 PR，合併另由你決定。

## Risks
1. A join must mean all incoming prerequisites, while a branch presents alternatives; verify labels and examples semantically as well as syntactically.
2. Mermaid grouping may not preserve an exact lane layout across hosts; verify role ownership and handoff meaning without promising pixel positions.
