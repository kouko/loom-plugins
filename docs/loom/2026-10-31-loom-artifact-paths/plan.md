# Per-change diagram artifacts — plan
intent: 2026-10-31-loom-artifact-paths@68c26f696ea4c01e853231debd77a31514be2cb4
spec: docs/loom/2026-10-31-loom-artifact-paths/spec.md@01211ed2
charter: 1.1

## Task DAG

**W0-01 Keep diagram writes inside the selected change**  after: none  acceptance: 1, 2, 3, 4
- Files: loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py, loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py, loom-workflow/skills/loom-interactive-diagram/SKILL.md
- Test: A1 positive: root-explicit-create; boundary: no-root-diagrams. A2 positive: change-cwd-create; negative: mismatched-change-id. A3 positive: reject-external-project; boundary: symlink-escape. A4 positive: external-read-only-check; boundary: preserve-existing-root-diagrams.
- Risk: Existing tests assume arbitrary cwd; preserve every linked-diagram check while replacing their fixtures. Follow spec REQ-1 through REQ-4; agent-decided: explicit id from root avoids choosing among concurrent changes.

**W1-01 Release the changed skill contract**  after: W0-01  acceptance: 1
- Files: loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/plugin.json, loom-workflow/package.json, loom-workflow/README.md, loom-workflow/CHANGELOG.md
- Test: A1 positive: synchronized-version-metadata; boundary: old-version-pin-updated.
- Risk: Bump loom-workflow minor version for changed skill guidance and CLI contract; run manifest sync before finalization.

## Simplicity check
- Omit editor setup edits because its path guidance is already correct — taken

## Questions asked
① — what — 若這就是你要的位置與結果，回覆「對」即可確認目前的 intent 草稿：無論從專案根目錄或變更目錄執行，都寫入同一位置；無法判定變更目錄時拒絕寫入；既有圖檔不搬移。

## Risks
1. A symlink or mismatched change id could redirect output; tests must prove refusal occurs before any write.
2. Read-only checks of external spec-linked diagrams remain supported while projection writes are bounded.
