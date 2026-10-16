# Codex agent dispatch for `skill-retro`

This maps the skill's two optional analysis dispatch points to the current Codex agent controls. The exact call signature is the active host tool contract; check it before dispatch because host tools can change.

## Stage 3 parallel fan-out

After the user approves which session-derived text may leave the local preview, call `spawn_agent` once per selected `subagent_payload[]` entry when independent agent slots are available. Pass the absolute path to the applicable `agents/prompt-failure-analysis.md` or `agents/prompt-success-analysis.md`, the task, and that trajectory's observable input. The agent reads the prompt itself. Do not mix trajectories or pass hidden reasoning. Collect each agent's result through its final message; `wait_agent` waits for mailbox updates. Wait for every dispatched agent before converting their Memory Items to `merged.json`. The host does not automatically consolidate those results merely because several agents were spawned.

## Stage 5c single dispatch

After separate consent for the optional advisory report, call `spawn_agent` once with the absolute path to `agents/prompt-advisory-analyst.md` and `dispatch_payload.input` (`merged_data`, `lang`, `date_str`, `skill_dir`). The agent reads the prompt and produces the report. Use `wait_agent` for its completion notification, then collect its final message.

## Model and effort

The prompt frontmatter's Claude model name is metadata for Claude Code; it does not make Sonnet available in Codex. Prefer the inherited Codex model and effort. If the active `spawn_agent` tool exposes `model` or `reasoning_effort` overrides and the dispatch profile explicitly chooses one, pass that supported Codex option with `fork_turns: "none"` and provide the needed paths and input explicitly. Never invent a Claude model alias for Codex.
