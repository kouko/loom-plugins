# Goal-create prompt and native activation boundary — spec
intent: 2026-09-27-goal-create-prompt-boundary@edc69163
confirmed-behavior: 2026-09-27 @7c8532a
pre-build-review: required — goal-create's user-facing invocation and activation contract changes across two hosts

## Requirements

REQ-1 — Complete prompt without execution
  WHEN the user invokes SESSION with sufficient conversation evidence or confirmed artifacts, goal-create shall display the complete four-field condition, preserve stated constraints and stop without performing the described work or operating Loom stations → Acceptance #1

REQ-2 — Codex native result
  IF the current Codex session exposes create_goal THEN goal-create shall submit the complete condition and report activation only from host success; otherwise it shall retain the complete condition and report the actual inactive or refused status → Acceptance #2

REQ-3 — Claude Code proposal or manual command
  IF the current Claude Code session exposes ProposeGoal THEN goal-create may propose the condition; otherwise it shall display one complete copyable /goal command, disclose replacement of an existing goal, and avoid advice to change internal settings → Acceptance #3

REQ-4 — Existing modes and release parity
  WHERE goal-create is invoked, the existing ARC draft path and SESSION's four-field lint and refusal contract shall remain available, and release metadata shall agree on one version → Acceptance #4

## Design decision

- user-decided — Keep this skill scoped to prompt creation and available native host activation; do not drive Loom stations or execute the generated goal, as confirmed in the conversation.
- user-decided — Retain native goal activation when technically exposed; provide the full manual command on Claude Code when ProposeGoal is absent.
- agent-decided — Use existing input-floor and activation gate text, rather than introducing an execution engine or a new state store, to keep the change small.
- agent-decided — Label mock-host dogfood as simulated, because a local test double cannot establish real host activation.

## Alternatives considered

- Remove native activation entirely — rejected because the user explicitly retained it when available.
- Automatically run Loom stations after drafting — rejected because it crosses the user-set skill boundary.
- Ask users to change Claude internal feature flags — rejected because absence of an exposed tool does not establish a supported opt-in path.

## Current state evidence

- Forward: loom-workflow/skills/goal-create/SKILL.md, SESSION mode and activation gate.
- Reverse: loom-workflow/skills/using-loom-workflow/SKILL.md, explicit goal-create routing; loom-workflow/skills/handoff/SKILL.md, optional offer.
- Error: loom-workflow/skills/goal-create/SKILL.md, Codex and Claude missing-tool recovery text; prior working-tree proposal attempted to drive Loom stations.
- Data: loom-workflow/skills/goal-create/references/goal-shape.md, four-field condition; references/input-floor.md, two slots and provenance.
- Boundary: loom-workflow/skills/goal-create/SKILL.md, skill exit after presenting prompt and host result; Loom stations remain separately owned.

## UI flows

| 情況 | 使用者做什麼 | 使用者看到什麼 |
|---|---|---|
| 資訊不足 | 指名呼叫 SESSION，但未提供現況或想要的改變 | 被告知缺少哪一項，不收到含糊的目標 |
| 草稿可用 | 提供現況與目標，或指向已確認文件 | 先看到可複製的完整四欄提示詞 |
| Codex 工具可用 | 在有原生工具的工作階段指名呼叫 | 工具成功後才看到「已啟用」；失敗時看到原因及未啟用狀態 |
| Claude 提議工具可用 | 在有原生工具的互動工作階段指名呼叫 | 收到提議與主機的確認／啟用結果，待確認不被說成已啟用 |
| Claude 提議工具不可用 | 在一般工作階段指名呼叫 | 看到完整可複製的 `/goal` 指令與取代現有目標的提醒，不被要求修改內部設定 |
| 目標內容未完成 | 提示詞已顯示、尚未手動提交指令 | 仍可複製提示詞；skill 不替使用者執行其中的工作 |
