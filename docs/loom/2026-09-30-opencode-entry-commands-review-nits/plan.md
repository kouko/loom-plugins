# Clear the reviewer nits left from the OpenCode entry-commands change — plan
intent: 2026-09-30-opencode-entry-commands-review-nits@74f86b34
charter: 1.1

## Current State Evidence
- Forward: `scripts/opencode/loader.js:301` splits every recorded prompt on `"\n\nBase directory for this skill: "`, whether or not a command built it.
- Reverse: `scripts/opencode/loader.js:75` builds a command's content with the same literal, so the separator lives in two places.
- Error: `scripts/opencode/loader.js:10-11` header says `user-invocable: true -> that command as well as the skill` without the both-keys case; `registerSkills` keeps such a skill command-only.
- Data: `loom-code/README.md:11` (and `README.ja.md:11`, `README.zh-TW.md:9`) label expert-mode "1 user-invoked"; no test pins that label (`loom-code/scripts/check_mechanisms.py:686` is only a comment).
- Boundary: `loom-code/tests/test_opencode_loader.py:125` `test_plugin_without_agents_registers_none` also pins command lists; `docs/loom/2026-09-30-opencode-entry-commands/acceptance-test-report.md:10,17,29,32` use "上次測試", "Build 階段" and "important"; that change's `plan.md:12` cites "115-118" and `plan.md:20` omits `loom-*/plugin.json` and two pin tests.

## Task DAG
Wave 1 fixes the loader; wave 2 carries every prose, version and changelog edit.

**W1-01 Loader records a command prompt minus the body it appended**  after: none  acceptance: 2, 5
- Files: scripts/opencode/loader.js, loom-code/opencode/loader.js, loom-design/opencode/loader.js, loom-workflow/opencode/loader.js, loom-code/tests/test_opencode_loader.py
- Test: A2 positive: command prompt recorded as typed text only; negative: typed message containing the separator recorded whole. A5 positive: header comment names the both-keys case; boundary: renamed test still pins agents and command lists.
- Risk: agent-decided — the prompt hook strips a trailing `\n\n${skill.content}` of a command skill instead of splitting on the separator, so the literal stays only in the content builder; preserves test_adversarial_opencode_command_language.py and widens test_opencode_loader.py by one case.

**W2-01 README label, old report and plan wording, version bump and changelog note**  after: W1-01  acceptance: 1, 3, 4, 6
- Files: loom-*/**/plugin.json, loom-*/package.json, loom-*/CHANGELOG.md, README.md, loom-*/README*.md, docs/loom/2026-09-30-opencode-entry-commands/*.md, loom-*/tests/**/test_*.py
- Test: A1 positive: new entries note the fix; negative: released entries unchanged. A3 positive: label reads command-only; negative: no "user-invoked" left. A4 positive: three terms explained; boundary: verdict cells unchanged. A6 positive: pins pass; negative: sync check exits 0.
- Risk: agent-decided — patch for all three (each ships the synced loader); the note rides new entries so released ones stay as published; version pins include loom-design/tests/spec/test_capture_intent_contract.py.

## Simplicity check
- Strip the command's own appended body instead of a prefix match plus shared constant — taken
- Merge the prose task into the bump task, since both edit loom-code/README.md line 11 — taken
- Drop the source-text count of the separator literal — taken

## Questions asked
① — what — 覆述 intent（9 個 nit 全修、transcript 只截斷指令訊息、會改舊報告與 plan、含自動發布授權） → 「對」

## Risks
1. Editing the merged change's report and plan alters records the user accepted; wording only, verdicts untouched.
