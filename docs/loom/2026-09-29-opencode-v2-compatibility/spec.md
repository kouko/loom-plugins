# Make the loom plugins installable and usable under OpenCode v2 — spec
intent: 2026-09-29-opencode-v2-compatibility@64aa3fcd
pre-build-review: required — cross-system architecture: a fourth host runtime whose JavaScript hooks deny shell and file commands by calling the loom checker, and whose skill and agent ids become the dispatch surface every station prose relies on

## Requirements
REQ-1 — Install through OpenCode's own plugin paths
  WHEN a user with OpenCode v2 and no loom install adds loom-code, loom-design or loom-workflow from this repository by OpenCode's official plugin command or the TUI's plugin dialog (carried: 「要能用 openCode v2 官方的指令 & 內建 TUI 介面 指定 repo 與 plugin 安裝」), the plugin shall install and appear in OpenCode's plugin list → Acceptance #1
REQ-2 — Every skill offered, none shadowed
  WHEN a new OpenCode session starts with the three plugins installed, every skill of the three plugins shall be offered under a plugin-qualified id and load its full SKILL.md body with its base directory, including when another installed plugin registers the same short name → Acceptance #2
REQ-3 — Whole flow on OpenCode
  WHEN a change in a throwaway repository is driven on OpenCode with a third-party cloud model, capture-intent, write-plan, build, closing-review and ship shall each run from their own skill prose, reach the installed loom checker, and end with an opened pull request whose intent, plan and attestation the checker accepts → Acceptance #3
REQ-4 — Loom roles as OpenCode subagents
  WHEN a station dispatches implementer, reviewer, adversary or acceptance-tester on OpenCode, each shall run as a separate OpenCode subagent registered from loom-code's agent definitions → Acceptance #4
REQ-5 — Hook behaviours ported or disclosed
  WHEN OpenCode runs a loom session, the session-start station order and kickoff defaults, the publication reminder, the language reminder, the skill folder-structure rule and the selection-record guard shall each behave as on the other hosts, or be named unavailable with the reason in OpenCode's install instructions → Acceptance #5
REQ-6 — Other hosts unchanged
  The existing package suite and the Codex manifest drift check shall pass, and the Claude Code, Codex and Antigravity CLI manifests, hook configs and skill names shall be unchanged → Acceptance #6
REQ-7 — Principles name OpenCode
  PRINCIPLES.md shall name OpenCode v2 in its audience line and hosts non-negotiable, with a ratified-by amendment entry, keeping the Non-negotiables count → Acceptance #7
REQ-8 — Release bump
  Each plugin shall carry a new version consistent across its Claude, Codex, Antigravity and OpenCode manifests, CHANGELOG and READMEs → Acceptance #8

## Design decision
- agent-decided: each plugin gets a root `package.json` (name = plugin name, `type: module`, `exports["."]` to its OpenCode entry). A git install resolves through `exports`; the spike showed a local-folder entry ignores `exports`, but the confirmed install path is the git spec, so no root `index.js` is added.
- agent-decided: the OpenCode `package.json` is derived by `scripts/sync_codex_manifests.py` from `.claude-plugin/plugin.json` like the Codex and Antigravity manifests, so `--check --all` in CI and the existing drift hook cover it; no second generator.
- agent-decided: one canonical loader (`scripts/opencode/loader.js`) is copied byte-identical into each plugin's `opencode/loader.js` by the same sync script, and `--check` fails on drift; each plugin's `opencode/index.js` imports it and declares only that plugin's hook table. Plugins cannot import each other at runtime (PRINCIPLES fixed choice), so a copy is required.
- agent-decided: skills register as `<plugin>:<skill>` and agents as `<plugin>:<agent>`, so the prose names `loom-code:reviewer` and `loom-design:write-spec` map one-to-one; the spike showed a duplicate id is silently last-wins, which the plugin prefix prevents.
- agent-decided: hooks use the v2 API only (`ctx.tool.hook`, `ctx.session.hook`); the spike showed v1 hook exports never load on 2.0.18. The JS hook builds the Claude Code hook payload and runs the existing handler (`loom_checker.py push --hook`, `selection capture --hook`, `hooks/session-start`, `hooks/language-anchor.py`, `hooks/visualization-card`, `scripts/validate-skill-folder-structure.sh`), so no hook logic is duplicated in JavaScript. OpenCode's shell tool is `shell`, not `bash`.
- agent-decided: a hook handler that cannot be reached (python3 missing, handler error) fails the way the Antigravity adapter does: the publication reminder and card are skipped, the selection guard denies a command that names or runs inside the selection store.
- agent-decided: `loom-code/references/opencode-tools.md` maps tool and agent names (Agent → `subagent` with `agent`, Skill → `skill` with `id`, Bash → `shell`, no effort parameter), linked from write-plan, build and closing-review beside the Antigravity line.
- agent-decided: the mechanism census (`check_mechanisms.py`) keeps reading only JSON hook configs; the OpenCode hook table is not registered as new mechanisms because each entry reuses an already-registered handler. Disclosed as a known limit.
- agent-decided: versions loom-code 3.24.0 (station guidance links a new host reference), loom-design 2.7.1 and loom-workflow 5.5.6 (packaging only).

## Alternatives considered
- v1 hook exports beside the v2 setup — never called on 2.0.18 (spike).
- A Python adapter like `agy_adapter.py` — OpenCode hooks are in-process JavaScript; an extra Python hop per tool call adds nothing over calling the existing handlers directly.
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
