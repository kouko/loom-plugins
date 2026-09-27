# Goal-create prompt and native activation boundary — plan
intent: 2026-09-27-goal-create-prompt-boundary@edc69163
spec: docs/loom/2026-09-27-goal-create-prompt-boundary/spec.md@d4af7e7e
charter: 1.1

## Task DAG

**W0-01 Bound SESSION to prompt and available host Goal**  after: none  acceptance: 1, 2, 3
- Files: loom-workflow/skills/goal-create/SKILL.md, loom-workflow/skills/goal-create/references/input-floor.md, loom-workflow/tests/goal-create/test_skill_md.py
- Test: A1 positive: prompt-from-confirmed-intent; boundary: no-Loom-execution. A2 positive: exposed-Codex-goal; negative: missing-or-refused-Codex-tool. A3 positive: Claude-proposal-result; negative: missing-or-failed-proposal-fallback.
- Risk: agent-decided — preserve the existing activation gate and input floor; REQ-1–3 need no new executor or state store.

**W1-01 Synchronize release metadata and contract test**  after: W0-01  acceptance: 4
- Files: loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/tests/scripts/test_release_metadata.py
- Test: A4 positive: synchronized-minor-release; negative: manifest-or-test-pin-drift.
- Risk: agent-decided — one minor version across manifests and changelog; REQ-4 changes the public skill contract.

**W1-02 Update existing user-facing descriptions**  after: W1-01  acceptance: 4
- Files: README.md, loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md
- Test: A4 positive: described-prompt-boundary; negative: stale-workflow-execution-claim.
- Risk: agent-decided — edit existing descriptions only; REQ-4 needs no new documentation file.

## Simplicity check

- Merge the release metadata and README tasks — declined: the combined task would touch nine files, exceeding the charter's eight-file cap; the existing sequence keeps each task startable.

## Questions asked

2 — behaviour — 使用者指名呼叫 goal-create SESSION 後，會先看到完整可複製的四欄提示詞。Codex 有原生工具時會嘗試啟用並回報結果；Claude Code 只有在當前工作階段暴露提議工具時才嘗試，否則給完整 `/goal` 指令並提醒會取代現有目標。skill 不會執行提示詞所描述的工作。這是你要確認的可見行為嗎？
2 — behaviour — 規格審查補上一個備援情況：Claude Code 雖有原生提議工具，但若提議失敗，或完整意思無法放進工具的長度限制，仍會顯示完整可複製的 `/goal` 指令、說明新目標尚未啟用並提醒會取代現有目標；等待主機確認時不會誤報已啟用。這也符合你的預期嗎？

## Risks

1. Controlled dogfood checks exercise host routing and output shape, not real native Goal activation or a user's manual paste.
2. The change must remain prompt-only; no Loom station mechanism or execution workflow is part of Build.
