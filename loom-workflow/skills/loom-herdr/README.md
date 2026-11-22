# loom-herdr

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-workflow](../../README.md) / loom-herdr

Operate [herdr](https://github.com/herdrdev/herdr) panes and agents with one
skill. At run time it loads the installed herdr's own instructions
(`herdr --skill`), so there is no second skill to install and no copied
text to go stale when herdr updates.

It adds:

- **Conversation search** across the agents of open herdr panes, and with
  `--history` across local Claude, Codex and OpenCode conversations.
  Read-only; snippets enter the searching agent's context.
- **Led conversations** between this agent and an agent in another pane,
  with a round cap, timeouts and a report at the end.
- **Codex sandbox help** when herdr is blocked by `Operation not permitted`.

It is selected only when you mention herdr, and works only inside a herdr
pane (`HERDR_ENV=1`). Ask naturally, e.g. "use herdr to search my open
conversations for the migration plan", or invoke `loom-workflow:loom-herdr`.

Runtime instructions: [SKILL.md](SKILL.md).
