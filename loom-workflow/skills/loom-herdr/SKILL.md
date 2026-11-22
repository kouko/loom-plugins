---
name: loom-herdr
description: |
  Operate herdr panes, agents and conversations: loads the installed herdr's own instructions, then adds conversation search, led agent-to-agent conversations and sandbox help. Select only when the user explicitly names herdr; do not select for background, parallel or delegated work that never mentions herdr.
user-invocable: true
---

# loom-herdr

One skill for herdr: the installed herdr supplies its own instructions at
run time, and this file adds only what those instructions lack.

## 1. Check you are inside herdr

```bash
test "${HERDR_ENV:-}" = 1
```

If the check fails, tell the user you are not running inside herdr and
stop. Run no herdr control command.

## 2. Load the official instructions

```bash
herdr --skill
```

Read the whole output and follow it as part of this skill; it is the
authority for herdr commands and outranks anything below on syntax.
IF `herdr --skill` exits non-zero or prints nothing, THEN run
`herdr --version`, report that version and the failure to the user, and
stop without guessing commands.

## 3. Extensions

### Conversation search

```bash
python3 <skill-dir>/scripts/herdr_search.py <query> [--history] [--json]
```

`<skill-dir>` is this skill's folder: `${CLAUDE_SKILL_DIR}` on Claude Code;
on any other host, the directory that holds this SKILL.md.

- Default scope: the agents of panes currently open in every workspace,
  worktree and tab. Results are labelled workspace, tab, pane and
  working directory; a pane that cannot be read is listed as
  `unsearchable: <reason>`.
- `--history` adds local Claude, Codex and OpenCode conversations not
  open in herdr. Before running it, tell the user that snippets from all
  local projects will enter this agent's context, and so reach this
  agent's model vendor.
- Read-only: the script modifies nothing. `--json` is for machine use.

### Led multi-turn conversation

This agent leads; the other agent only answers.

1. Start only when the target agent is idle.
2. Record the target's pane id, agent and agent_session. Before every
   send, re-resolve the target by that pane id: never by name, never with
   `--current`, never this agent's own pane (`$HERDR_PANE_ID`). If the
   pane's agent or agent_session changed, stop.
3. Round cap: 5 unless the user sets another.
4. Pass `--timeout 300000` on every wait.
5. On a timeout, a `blocked` state or a changed target, end the
   conversation with a report to the user. Never resend.
6. When a screen read does not show the complete reply, use the official
   file hand-off: create the directory with `mktemp -d`, outside the repo,
   ask the other agent to write its reply there, read the
   file, and delete the directory whenever the conversation ends, including
   on a timeout, a `blocked` state or a changed target.
7. At the round cap or when done, report the outcome to the user.

### Codex sandbox

If a herdr command fails with `Operation not permitted`, tell the user
herdr needs network permission in Codex's sandbox (for example
`sandbox_workspace_write.network_access=true`). Do not retry.

### Known pitfalls

- #2900: `--current` outside a herdr pane falls back to the focused pane,
  which may be the user's.
- #4764: an agent name can be reused by a new agent after the old one
  exits, so a name may point at a different agent.
- #5462: `agent read --lines` can return only the visible screen for a
  short Claude transcript; use the file hand-off for full replies.
