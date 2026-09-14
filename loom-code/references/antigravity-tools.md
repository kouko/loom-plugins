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
| Dispatch a named loom agent | `Agent` with `subagent_type: "loom-code:<role>"` | `invoke_subagent` with `TypeName: "self"`, as described under Dispatching loom roles |
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

## Dispatching loom roles

loom-code ships four agent contracts: `implementer`, `reviewer`, `adversary`
and `blind-runner`, each in `<loom-code>/agents/<role>.md`. agy also lists
the plugin-provided agents of the same names, but gives a Markdown-defined
agent no tools by default and loom's agent files declare none, so those
agents have no tools on agy. Never use one of them as a `TypeName` on agy.

Dispatch every loom role to agy's built-in `self` subagent instead. It starts
from a fresh context (it does not see the parent conversation) and has
working tools, including `view_file`, `write_to_file` and `run_command`.

| loom role | `TypeName` | Contract the `Prompt` tells it to read first |
|---|---|---|
| `implementer` | `self` | `<loom-code>/agents/implementer.md` |
| `reviewer` | `self` | `<loom-code>/agents/reviewer.md` |
| `adversary` | `self` | `<loom-code>/agents/adversary.md` |
| `blind-runner` | `self` | `<loom-code>/agents/blind-runner.md` |

Call `invoke_subagent` with a `Subagents` array. Each item carries:

- `TypeName` (required) — always `"self"`.
- `Role` (required) — the loom role this dispatch fills, as in the table.
- `Prompt` (required) — first, an instruction to read
  `<loom-code>/agents/<role>.md` (with `<loom-code>` resolved to an absolute
  path as Plugin root below defines) and follow it as the subagent's
  contract; then the station's normal dispatch packet: resource paths, task,
  acceptance criteria, as that contract's input section defines.
- `Model` (optional) — one of `inherit`, `flash_lite`, `flash`, `pro`.
- `Workspace` (optional) — one of `inherit`, `branch`, `share`; the meaning
  of each value is unverified on agy 1.2.2.

Use one `self` invocation per dispatch: one per reviewer identity, and one
each for the implementer task, the adversary and the blind runner. The
subagent runs as a background task and the root agent waits for its reply. Every station requirement for
fresh-context or distinct reviewers still applies: give each reviewer
identity its own separate `self` invocation with a complete prompt, and never
reuse one subagent's reply as another reviewer's verdict. Whether several
items in one `Subagents` array run concurrently is unverified on agy 1.2.2.

## Model and effort overrides

`invoke_subagent` has no effort parameter, so a resolved
`dispatch_profile.py` profile cannot be applied atomically on agy. Follow the
shared dispatch profile's atomic host fallback: omit both overrides, leave
`Model` unset or `inherit`, and record the effective profile as `inherited`.
Never set `Model` alone; a partial profile is never claimed.

## Second vendor

Antigravity CLI has no verified second-vendor runner yet, so an agy host
offers no cross-model reviewer: probe no vendor and continue the review
without one.

## Plugin root

agy substitutes no variables in skill text. `<loom-code>` is the plugin
directory two levels above a station's `SKILL.md`; after
`agy plugin install` that is `~/.gemini/config/plugins/loom-code/`.

## Hooks

loom-code's root hooks.json adapter enforces the push gate, session context and language reminder on agy; stations do not invoke hooks.
