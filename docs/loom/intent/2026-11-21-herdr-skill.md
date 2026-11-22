# herdr skill in loom-workflow
originator: kouko
kind: engineering
needs-design: no — agent-facing skill text and helper scripts; no GUI, TUI, CLI, API or user-depended file surface, and no interface-surface glob matches
evidence: [docs/loom/research/2026-11-21-herdr-skill-prototype.md]
status: confirmed 2026-11-22
intent_confirmed_sha: eaa37f1ecdd78888af5c7572a8885fde5c24e2e7
publication: automatic — authorized 2026-11-22 by kouko

## Problem
kouko runs Claude, Codex and OpenCode side by side in herdr panes. Agents in
those panes do not know how to operate herdr: herdr's official skill is not
installed for any of them (`herdr integration install` only adds a status
hook), so an agent only finds the official instructions if it happens to run
`herdr --help`. Two things kouko wants are missing even from the official
skill:

- There is no way to search what was said across the conversations in herdr
  workspaces, worktrees, tabs and panes. Finding an earlier discussion means
  switching pane by pane or grepping transcript folders by hand, without
  knowing which pane a transcript belongs to.
- The official skill covers one prompt-and-read exchange with another agent,
  not a multi-turn conversation between two agents (for example Claude and
  Codex). Without rules, such a loop can resend prompts, wait forever, never
  stop, or read a truncated reply.

kouko does not want to install two skills (official + extension) to get this.

## Proposed outcome
One skill shipped in loom-workflow gives Claude Code, Codex and OpenCode agents
everything herdr's official skill provides, always matching the locally
installed herdr version, plus conversation search across herdr and a safe
multi-turn agent-to-agent conversation, plus the known herdr pitfalls.

## Acceptance
1. With loom-workflow installed and herdr's official skill not installed, an agent (Claude Code, Codex, OpenCode) inside a herdr pane asked to do a herdr operation follows the official instructions of the locally installed herdr version and completes the operation.
2. Outside a herdr pane, the skill stops and says it is not running inside herdr, without running any herdr control command.
3. A request that does not mention herdr does not use the skill.
4. A keyword search returns matching snippets from the conversations of the Claude, Codex and OpenCode agents in currently open herdr panes, each labelled with its workspace, tab, pane and working directory.
5. The same search can include past Claude, Codex and OpenCode conversations that are no longer open in herdr, labelled with their working directory and marked as not open.
6. An agent can lead a multi-turn conversation with an agent in another herdr pane, including Claude with Codex, where the other agent answers; it stops at a round limit and gets the other agent's complete reply even when the reply is longer than the screen.
7. When Codex's sandbox blocks herdr commands, the agent tells the user that herdr needs network permission instead of retrying.
8. When the installed herdr version changes its official skill, agents follow the new official content without a new loom-workflow release.

## Constraints
- One skill in loom-workflow; the user does not install herdr's official skill separately.
- The official herdr skill content is not copied into loom; it is loaded from the installed herdr.
- Hosts: Claude Code, Codex and OpenCode.
- user-decided — in an agent conversation one agent leads and the other only answers (2026-11-21).
- user-decided — conversation search covers OpenCode as well as Claude and Codex (2026-11-21).

## Out of scope
- Operating herdr on remote machines (`--machine`).
- Agents in one conversation starting turns towards each other freely (both directions).
- Changing herdr itself or contributing upstream.
- Installing, removing or configuring herdr or its integrations.

## Open questions
- none
