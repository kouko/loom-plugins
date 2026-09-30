# Start loom's entry skills from OpenCode's command list — plan
intent: 2026-09-30-opencode-entry-commands@8b4b5d78
spec: docs/loom/2026-09-30-opencode-entry-commands/spec.md@ef0c1888
charter: 1.1

## Task DAG
Wave 1 holds two independent tasks; wave 2 bumps versions over their result.

**W1-01 Loader registers user-invocable skills as commands too**  after: none  acceptance: 1, 2, 3
- Files: scripts/opencode/loader.js, loom-*/opencode/loader.js, loom-*/skills/using-loom-*/SKILL.md, loom-workflow/skills/handoff/SKILL.md, loom-workflow/skills/recap-state/SKILL.md, loom-workflow/skills/goal-create/SKILL.md, loom-code/tests/test_opencode_loader.py
- Test: A1 positive: exact per-plugin command lists; negative: exact equality rejects any unkeyed skill. A2 positive: skills equal model-invocable SKILL.md set; boundary: loom-design/workflow agents stay empty. A3 positive: expert-mode in commands; negative: expert-mode absent from skills.
- Risk: agent-decided — REQ-1..3 Design decision (`user-invocable: true`, sync copies). Edits existing assertions only in test_opencode_loader.py (lines 96-99, 115-118); widens their command lists, adds no test function.

**W1-02 README OpenCode sections name the start commands**  after: none  acceptance: 4
- Files: README.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, loom-design/README*.md, loom-workflow/README*.md, tests/test_agy_install_docs.py
- Test: A4 positive: each README's OpenCode section names its plugin's start commands; boundary: the root README names all six.
- Risk: agent-decided — one sentence appended to each existing "Skills are offered as" line and its ja/zh-TW twin; no new section.

**W2-01 Version bump**  after: W1-01, W1-02  acceptance: 5
- Files: loom-*/.claude-plugin/plugin.json, loom-*/.codex-plugin/plugin.json, loom-*/package.json, loom-*/CHANGELOG.md, README.md, loom-*/README*.md, loom-code/tests/test_write_plan_station_text.py
- Test: A5 positive: release-metadata sync test passes at loom-code 3.26.0, loom-design 2.8.0, loom-workflow 5.6.0; negative: `sync_codex_manifests.py --check --all` exits 0.
- Risk: agent-decided — minor for all three: each gains a skill frontmatter field and new OpenCode commands. Every sync script output committed.

**W2-02 Graduate the command-language probe into the suite**  after: W1-01  acceptance: 1
- Files: docs/loom/2026-09-30-opencode-entry-commands/evidence/probes/test_opencode_command_language.py, loom-code/tests/test_adversarial_opencode_command_language.py
- Test: A1 positive: moved program passes in the package suite; negative: a command prompt's skill body never reaches the transcript as user words.
- Risk: agent-decided — the probe caught a real defect (fixed in 78b3ba6c), so it moves into loom-code/tests/ via git mv, changing only imports and path helpers.

## Simplicity check
- Reuse existing loader assertions instead of new negative and boundary cases — taken
- Drop the README expert-mode pin no Acceptance line asks for — taken

## Questions asked
① — what — 要把哪些 skill 加到 OpenCode command → 「三個 using-* 跟 handoff recap-state goal-create expert-mode 這七個加到 command （同時保留 skill) 就好」
① — consequence — expert-mode 維持只登記 command（不同時登記成 skill） → 「對」
① — consequence — expert-mode 也登記成 skill 會讓模型能自行載入它並提議跳過驗證步驟 → 「維持只有指令」
① — what — 覆述 intent（含自動發布授權） → 「對」

## Risks
1. OpenCode may list a command and a skill with the same id side by side; verified only in the acceptance run, since the stub context cannot show OpenCode's menu.
2. The six SKILL.md edits change skill files on every host; the key is Claude Code's default, so behaviour there stays the same.
