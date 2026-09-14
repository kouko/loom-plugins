# Antigravity CLI tool and dispatch mapping

Advisory reference for an agent running loom-code's stations (build,
closing-review, write-plan) inside Antigravity CLI (`agy`). The station text
names tools and agents the way Claude Code and Codex CLI see them; this file
maps those names to agy's. It changes nothing on Claude Code or Codex CLI.

Facts below were observed on agy 1.2.2. Anything marked **unverified on agy
1.2.2** was not observed; follow the station's fail-closed or fallback rule
instead of assuming it.

## Tool map

| Concept | Claude Code | Antigravity CLI |
|---|---|---|
| Dispatch a named loom agent | `Agent` with `subagent_type: "loom-code:<role>"` | `invoke_subagent` with `TypeName: "<role>"` |
| Ask the user a question | `AskUserQuestion` | `ask_question` |
| Run a shell command | `Bash` | `run_command` with `CommandLine` and `Cwd` |
| Open a file | `Read` | `view_file` with `AbsolutePath` |
| Create or overwrite a file | `Write` | `write_to_file` with `TargetFile` (absolute), `CodeContent`, `Overwrite` |
| Replace text in a file | `Edit` | `replace_file_content` with `TargetFile`, `TargetContent`, `ReplacementContent` |
| Search contents, names, directories | Grep / Glob | `grep_search`, `find_by_name`, `list_dir` |
| Load a skill | `Skill` | `view_file` on the skill's absolute `SKILL.md` path |

On Codex CLI the question tool is `request_user_input`; the write-plan
second-vendor reference owns when each host's question tool is used.
Argument names for `ask_question`, `grep_search`, `find_by_name` and
`list_dir` are unverified on agy 1.2.2; read them from the live tool schema.

## Dispatching loom agents

loom-code ships four agents: `implementer`, `reviewer`, `adversary` and
`blind-runner`. agy loads each from `agents/<name>.md` and addresses it by
that bare name, without the `loom-code:` prefix.

Call `invoke_subagent` with a `Subagents` array. Each item carries:

- `TypeName` (required) — the bare agent name, for example `reviewer`.
- `Role` (required) — a short label for this dispatch.
- `Prompt` (required) — the station's input packet: resource paths, task,
  acceptance criteria, as the agent contract's input section defines.
- `Model` (optional) — one of `inherit`, `flash_lite`, `flash`, `pro`.
- `Workspace` (optional) — one of `inherit`, `branch`, `share`; the meaning
  of each value is unverified on agy 1.2.2.

The subagent runs as a background task and the root agent waits for its
reply. Whether each invocation starts from a fresh context is unverified on
agy 1.2.2; every station requirement for fresh-context or distinct reviewers
still applies, so give each dispatch a complete prompt and never reuse one
agent's reply as another reviewer's verdict. Whether several items in one
`Subagents` array run concurrently is unverified on agy 1.2.2.

## Model and effort overrides

`invoke_subagent` has no effort parameter, so a resolved
`dispatch_profile.py` profile cannot be applied atomically on agy. Follow the
shared dispatch profile's atomic host fallback: omit both overrides, leave
`Model` unset or `inherit`, and record the effective profile as `inherited`.
Never set `Model` alone; a partial profile is never claimed.

## Second vendor

On agy the host vendor is `gemini`. Probe `claude` then `codex`, and pass
`host_vendor: "gemini"` to `second_vendor_policy.py`. The Codex-to-Claude
reviewer runner described in closing-review is the Codex path; this
reference defines no Antigravity equivalent.

## Plugin root

agy substitutes no variables in skill text. `<loom-code>` is the plugin
directory two levels above a station's `SKILL.md`; after
`agy plugin install` that is `~/.gemini/config/plugins/loom-code/`.

## Hooks (orientation only)

agy reads a root `hooks.json`, runs each command through `sh -c` from the
installed plugin root, and exposes no plugin-root environment variable.
Events are `PreToolUse`, `PostToolUse`, `PreInvocation`, `PostInvocation`
and `Stop`; there is no session-start or prompt-submit event. A `PreToolUse`
hook on `run_command` can return `{"decision": "deny", "reason": "..."}` to
block a command, and a `PreInvocation` hook can inject text with
`{"injectSteps": [{"ephemeralMessage": "..."}]}`. loom-code's adapter uses
these for the push gate and session context; a station never calls them.
