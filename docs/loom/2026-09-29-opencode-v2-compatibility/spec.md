# Make the loom plugins installable and usable under OpenCode v2 — spec
intent: 2026-09-29-opencode-v2-compatibility@64aa3fcd
pre-build-review: required — cross-system architecture: a fourth host runtime whose JavaScript hooks deny shell and file commands by calling the loom checker, and whose skill and agent ids become the dispatch surface every station prose relies on

## Requirements
REQ-1 — Install through OpenCode's own plugin paths
  WHEN a user with OpenCode v2 and no loom install adds loom-code, loom-design or loom-workflow from this repository by OpenCode's official plugin command or the TUI's plugin dialog (carried: 「要能用 openCode v2 官方的指令 & 內建 TUI 介面 指定 repo 與 plugin 安裝」), the plugin shall install and appear in OpenCode's plugin list → Acceptance #1
REQ-2 — Every skill offered, none shadowed
  WHEN a new OpenCode session starts with the three plugins installed, every skill of the three plugins shall be offered under a plugin-qualified id and load its full SKILL.md body with its base directory, including when another installed plugin registers the same short name → Acceptance #2
REQ-3 — Whole flow on OpenCode
  WHEN a change in a throwaway repository is driven on OpenCode with a third-party cloud model, capture-intent, write-plan, build, closing-review and ship shall each run from their own skill prose, reach the installed loom checker, and end with an opened pull request whose intent, plan and attestation the checker accepts, with the acceptance test report committed on the change branch, using the model from the user's existing OpenCode setup → Acceptance #3
REQ-4 — Loom roles as OpenCode subagents
  WHEN a station dispatches implementer, reviewer, adversary or acceptance-tester on OpenCode, each shall run as a separate OpenCode subagent registered from loom-code's agent definitions → Acceptance #4
REQ-5 — Hook behaviours ported or disclosed
  WHEN OpenCode runs a loom session, the session-start station order and kickoff defaults, the publication reminder, the language reminder, the skill folder-structure rule and the selection-record guard shall each behave as on the other hosts, or be named unavailable with the reason in OpenCode's install instructions; IF a subagent prompt or a nested `opencode` run carries an expert-mode entry token and a pending code, THEN no step-skip confirmation shall be recorded → Acceptance #5
REQ-6 — Other hosts unchanged
  The existing package suite and the Codex manifest drift check shall pass, and the Claude Code, Codex and Antigravity CLI manifests, hook configs and skill names shall be unchanged → Acceptance #6
REQ-7 — Principles name OpenCode
  PRINCIPLES.md shall name OpenCode v2 in its Who line and the host-installed-hooks Fixed choice, with a ratified-by amendment entry → Acceptance #7
REQ-8 — Release bump
  Each plugin shall carry a new version consistent across its Claude, Codex, Antigravity and OpenCode manifests, CHANGELOG and READMEs → Acceptance #8

## Design decision
- agent-decided: install spec per plugin is `github:kouko/loom-plugins#main::path:<plugin>`, typed into `opencode plugin add` or the TUI's plugin dialog. Each plugin gets a root `package.json` (name = plugin name, `type: module`, `main: index.js`) and a root `index.js` entry, so the package loads whether OpenCode resolves it as a git package or a local folder (the spike showed a local folder ignores `exports`). Every script the hooks run is invoked through `python3` or `bash` explicitly, so a lost executable bit in the npm-pack copy does not matter.
- agent-decided: the OpenCode `package.json` is derived by `scripts/sync_codex_manifests.py` from `.claude-plugin/plugin.json` like the Codex and Antigravity manifests. CI's `--check --all` covers it and the loader copies; the Codex drift edit hook covers `package.json` only.
- agent-decided: one canonical loader (`scripts/opencode/loader.js`) is copied byte-identical into each plugin's `opencode/loader.js` by the same sync script, and `--check` fails on drift. Plugins cannot import each other at runtime (PRINCIPLES fixed choice), so a copy is required. Each root `index.js` exports `default {id: <plugin name>, setup}` calling the loader; `loader.js` carries no id, because duplicate plugin ids fail to load.
- agent-decided: skills register as `<plugin>:<skill>` and agents as `<plugin>:<agent>`, so prose names such as `loom-code:reviewer` and `loom-design:write-spec` map one-to-one; the plugin prefix prevents OpenCode's silent last-wins on a duplicate id. A skill whose frontmatter has `disable-model-invocation: true` (expert-mode) is not registered as a model-invocable skill; it is registered as a user command `/loom-code:expert-mode` whose raw text reaches the prompt hook. When Build's live check shows the typed command text does not reach the prompt hook, expert-mode is named unavailable on OpenCode in the install instructions (option A).
- agent-decided: hooks use the v2 API only; v1 hook exports never load on 2.0.18 (spike). Each plugin declares its OpenCode hooks in `hooks/hooks-opencode.json`, in the same schema, event names and tool-name matchers as its Claude `hooks/hooks.json`. The shared loader translates them and runs the existing handler with a Claude Code payload built from the OpenCode call, so no hook logic is duplicated in JavaScript:

| Claude event | OpenCode v2 hook | When | Output fed back |
|---|---|---|---|
| SessionStart | `session.hook("context")` | once per root session (cached by session id); never in a subagent session | `additionalContext` → one `{type:"text"}` context entry |
| UserPromptSubmit | `session.hook("prompt")` | root session only | `additionalContext`/`systemMessage` → appended context text |
| PreToolUse | `tool.hook("execute.before")` | every mapped tool call | exit 2 → throw with stderr as the message; `systemMessage` → appended note |
| PostToolUse | `tool.hook("execute.after")` | every mapped tool call | exit 2 or `additionalContext` → note appended to the tool result |

| OpenCode tool and argument | Claude payload |
|---|---|
| `shell` `command` | `Bash` `command` |
| `write` `filePath` | `Write` `file_path` |
| `edit` `filePath` | `Edit` `file_path` |
| `patch` / `apply_patch` | `apply_patch` with its patch text |
| `skill` `id` | `Skill` `skill` |

- agent-decided: nested-session forgery is closed twice. The prompt hook runs selection capture and the card only for a root session (no parent session id); every handler run from a child session gets `CLAUDE_CODE_SESSION_ATTENDED=0`; and `opencode` joins `HOST_PROGRAMS` in `rule_checks/selection_guard.py`, so a nested `opencode run` carrying an entry token is refused like `claude` and `codex`.
- agent-decided: tool calls made inside OpenCode's code-mode `execute` tool are checked live in Build. When they do not pass `tool.hook`, that bypass of the selection guard and folder rule is named in the install instructions (option A); the loader does not disable a user's OpenCode tool.
- agent-decided: the language reminder gets its transcript from the loader: the prompt hook appends each root-session user prompt to a per-session file outside the repository (`<os tmpdir>/loom-opencode/<session id>.jsonl`) in the Claude transcript format `lang_detect.conversation_language` reads, and the `Skill` PostToolUse payload carries that file as `transcript_path`.
- agent-decided: a handler that cannot be reached (python3 missing, handler error) fails as the Antigravity adapter does: the reminder, card and context are skipped, and the selection guard still denies a command or file path that names the selection store.
- agent-decided: the mechanism census reads both `hooks/hooks-opencode.json` files with an `@opencode` qualifier, as it does for `@codex`, and `docs/loom/evidence/mechanisms.yaml` registers each entry with its regression eval: one pytest module, `loom-code/tests/test_opencode_loader.py`, which runs `node` on a stub-`ctx` script and asserts every skill, agent and hook registration and translation; it fails, not skips, when `node` is missing, and CI installs node for it. The `@opencode` entries raise the net hook count, so the loom-code 3.24.0 and loom-workflow 5.5.6 CHANGELOG sections carry one `budget-exception: <id> — <reason>` line per counted `@opencode` id (user-decided under intent Acceptance #5, 「對，選 A」: the user asked for each hook behaviour to work on OpenCode); `language-anchor@opencode` takes class host-hygiene like its Claude twin and is not counted.
- agent-decided: `loom-code/references/opencode-tools.md` maps tool and agent names (Agent → `subagent` with `agent`, Skill → `skill` with `id`, Bash → `shell`, no effort parameter), linked from write-plan, build and closing-review beside the Antigravity line.
- agent-decided: versions loom-code 3.24.0 (station guidance links a new host reference), loom-design 2.7.1 and loom-workflow 5.5.6 (packaging and hook table only).

## Alternatives considered
- v1 hook exports beside the v2 setup — never called on 2.0.18 (spike).
- A Python adapter like `agy_adapter.py` — OpenCode hooks are in-process JavaScript; an extra Python hop per tool call adds nothing over calling the existing handlers directly.
- Hook table hard-coded in each `index.js` — the census could not recompute it, and it would diverge from the JSON schema the other hosts use.
- Denying the code-mode `execute` tool — changes the user's OpenCode beyond loom, which the no-new-capability constraint excludes.
- Bare skill ids — silently shadowed by any other plugin with the same short name.
- Publishing to npm — out of scope; install is from the repository.
- Separate hand-written loaders per plugin — three drifting copies of the same skill/agent registration.

## Current state evidence
- Forward: `scripts/sync_codex_manifests.py:61-82,151,225` derives Codex and Antigravity manifests from `.claude-plugin/plugin.json`; `loom-code/.claude-plugin/plugin.json:27` declares `./skills/`.
- Reverse: `loom-code/references/antigravity-tools.md:12-16,30-68` maps `Agent`+`subagent_type` for agy and is linked at `write-plan/SKILL.md:40`, `build/SKILL.md:58`, `closing-review/SKILL.md:59`, pinned by `loom-code/tests/test_agy_tool_mapping.py:19-20`.
- Error: `loom-code/hooks/agy_adapter.py:63-96` denies only on checker exit 2 or an unreadable payload; `loom-code/hooks/hooks.json:15-46` wires push, selection capture and language anchor on Claude Code.
- Data: `loom-code/hooks/session-start:1-30` emits `hookSpecificOutput.additionalContext`; `loom-workflow/hooks/hooks.json:3-25` wires the card and folder validator.
- Boundary: `tests/test_loom_plugin_install_layout.py:148-174` pins root-manifest keys; `loom-code/tests/test_write_plan_station_text.py:245-260` pins three loom-code versions; `tests/test_agy_install_docs.py:20-35` pins install headings; `PRINCIPLES.md:5,24` name three hosts.

## UI flows
N/A
