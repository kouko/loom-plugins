# Start loom's entry skills from OpenCode's command list — spec
intent: 2026-09-30-opencode-entry-commands@8b4b5d78
pre-build-review: not-required — one loader rule plus a frontmatter key and README lines; no security, data, public-contract or cross-system risk, and every requirement is fixed by the intent

## Requirements
REQ-1 — Six entry skills are OpenCode commands
  WHEN OpenCode v2 loads loom-code, loom-design or loom-workflow, the loader shall register `/loom-code:using-loom-code`, `/loom-design:using-loom-design`, `/loom-workflow:using-loom-workflow`, `/loom-workflow:handoff`, `/loom-workflow:recap-state` and `/loom-workflow:goal-create` as commands whose run starts that skill (carried: 「三個 using-* 跟 handoff recap-state goal-create … 加到 command （同時保留 skill)」) → Acceptance #1
REQ-2 — They stay skills
  WHEN OpenCode v2 loads the plugins, the loader shall still register those six as model-loadable skills, unchanged → Acceptance #2
REQ-3 — expert-mode stays command-only
  WHEN OpenCode v2 loads loom-code, `/loom-code:expert-mode` shall be registered as a command and not as a skill (carried: 「expert-mode 維持只登記 command（不同時登記成 skill）」→「對」; 「維持只有指令」) → Acceptance #3
REQ-4 — README says how to start loom on OpenCode
  WHEN a user reads any README's OpenCode section, it shall name the commands that start loom from that plugin (all six in the root README) → Acceptance #4
REQ-5 — Suite and versions
  WHEN the change is complete, the package suite shall pass and each changed plugin shall carry one new version across manifests, CHANGELOGs and READMEs → Acceptance #5

## Design decision
- agent-decided: a skill opts in with the frontmatter line `user-invocable: true`. It is Claude Code's own key with the same meaning, and there it is already the default, so the line is a no-op on Claude Code. Codex and Antigravity CLI already receive the extra keys `version` (16 skills) and `disable-model-invocation` without effect, so one more key follows that precedent.
- agent-decided: the loader rule is that a command is registered when `disable-model-invocation` is true or `user-invocable` is true, and a skill is registered unless `disable-model-invocation` is true. Commands run through the existing `registerCommands` execute path (typed text, then skill content), so the prompt hook still sees `/<plugin>:<name>`.
- agent-decided: edit only the canonical `scripts/opencode/loader.js`, then copy it to each plugin with `scripts/sync_codex_manifests.py --all`, as the file header requires.
- user-decided: expert-mode stays command-only. The user chose this over also registering it as a skill, which would let the model load a step-skipping route on its own.

## Alternatives considered
- A hard-coded id list in the shared loader: rejected. The loader carries no plugin id by design, and a list there would name other plugins' skills.
- A field in each generated `package.json`: rejected. That file is derived from manifests by the sync script, so the choice would sit away from the skill it describes.
- A new loom-specific frontmatter key: rejected in favour of the existing Claude Code key, which means the same thing.

## Current state evidence
- Forward: `scripts/opencode/loader.js` `registerCommands` (~line 99) registers only `userOnly` skills as commands.
- Reverse: `registerSkills` (~line 91) drops every `userOnly` skill from the skill list; `loom-code/skills/expert-mode/SKILL.md:5` sets `disable-model-invocation: true`.
- Error: `loom-code/tests/test_opencode_loader.py:96-99` asserts that `commands == [loom-code:expert-mode]`; it must widen to the six new commands.
- Data: `skills()` (~line 60) parses frontmatter into `{id, name, description, path, content, userOnly}`.
- Boundary: `tests/test_agy_install_docs.py:174` pins each README's OpenCode section; the skill-offer lines sit at `README.md:258`, `loom-*/README*.md` (the "Skills are offered as" line and its ja/zh-TW twins).

## UI flows
- In OpenCode, the user types `/` → the list shows the six loom entry commands and `loom-code:expert-mode`.
- The user runs `/loom-workflow:handoff <text>` → the handoff skill's workflow starts with `<text>`.
