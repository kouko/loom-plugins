# OpenCode tool and dispatch mapping

Advisory reference for an agent running loom-code's stations (build,
closing-review, write-plan) inside OpenCode v2. The station text names tools
and agents the way Claude Code sees them; this file maps those names to
OpenCode's. It changes nothing on Claude Code, Codex CLI or Antigravity CLI.

Facts below were observed on OpenCode 2.0.18. For anything not listed, read the
live tool schema instead of assuming.

## Tool map

| Concept | Claude Code | OpenCode |
|---|---|---|
| Dispatch a named loom agent | `Agent` with its agent-type argument | `subagent` with `agent: "loom-code:<role>"`, as described under Dispatching loom roles |
| Resume a dispatched agent | the agent's task id | `subagent` with `sessionID` |
| Load a skill | `Skill` | `skill` with `id: "<plugin>:<skill>"` |
| Run a shell command | `Bash` | `shell` |
| Create or overwrite a file | `Write` | `write` with `path` |
| Replace text in a file | `Edit` | `edit` with `path` |
| Apply a multi-file change | (none) | `patch` |

## Dispatching loom roles

loom agents are registered under their plugin-qualified ids, one per contract
in `<loom-code>/agents/<role>.md`. Pass the id as the `agent` argument of
`subagent`; there is no separate agent-type argument on OpenCode.

| loom role | `agent` |
|---|---|
| `implementer` | `loom-code:implementer` |
| `reviewer` | `loom-code:reviewer` |
| `adversary` | `loom-code:adversary` |
| `acceptance-tester` | `loom-code:acceptance-tester` |

Give each dispatch the station's normal packet: resource paths, task and
acceptance criteria. Every station requirement for fresh-context or distinct
reviewers still applies: one `subagent` call per reviewer identity, and never
reuse one reply as another reviewer's verdict. Resume with `sessionID` only
for the same role and task.

## Model and effort overrides

An agent with no model set inherits the session model, and `subagent` has no
effort parameter, so a resolved `dispatch_profile.py` profile cannot be applied
atomically. Follow the shared dispatch profile's atomic host fallback: omit both
overrides and record the effective profile as `host-default/unverified`. Never
set a model alone; a partial profile is never claimed.

## Plugin root

OpenCode never substitutes `CLAUDE_PLUGIN_ROOT`. The `skill` tool's output
states "Base directory for this skill"; `<loom-code>` is the directory two
levels above the invoking station's `SKILL.md`.

## Hooks

loom-code's plugin hooks run on OpenCode; the install instructions list
OpenCode's limits.
