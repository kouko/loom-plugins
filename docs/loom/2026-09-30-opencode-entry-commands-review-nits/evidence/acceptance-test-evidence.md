# Clear the reviewer nits left from the OpenCode entry-commands change — acceptance test evidence

Tried on 2026-09-30, in a clean copy of the project at `41121f04` (a detached
`git worktree` in the tester's scratch area, removed afterwards). Base `668158f5`.

Setup check (step 2): the clean copy installs in OpenCode through the README's
`opencode plugin add` step (pinned local spec, see 2), and the covering tests run
with the repo's documented command. Both worked.

## 1. The loom-code, loom-design and loom-workflow changelogs state that on OpenCode a command's skill body is no longer recorded as the user's words.

- How I tried it: `git diff 668158f5..HEAD -- loom-*/CHANGELOG.md`; read each new top entry.
- What came back:
  - `loom-code/CHANGELOG.md` `## [3.26.1] — 2026-09-30`: "On OpenCode, a command's skill body is not recorded as the user's words, so the language reminder keeps the user's language (shipped in 3.26.0); a message the user types that contains the skill-body separator is now recorded whole."
  - `loom-design/CHANGELOG.md` `## [2.8.1]` and `loom-workflow/CHANGELOG.md` `## [5.6.1]`: the same sentence, citing 2.8.0 and 5.6.0.
  - The diff only adds lines; the released 3.26.0 / 2.8.0 / 5.6.0 entries are unchanged.
- Verdict: works.

## 2. On OpenCode, a message the user types that contains "Base directory for this skill:" is recorded in full, while a loom command's prompt is still recorded as only the typed command text.

- Environment (method of the prior change's evidence, with one difference: no real model):
  - Binary `/Users/kouko/.opencode/bin/opencode` by absolute path, `opencode v2.0.20`.
  - Scratch tree `oc/` with its own `XDG_CONFIG_HOME`, `XDG_DATA_HOME`, `XDG_CACHE_HOME`,
    `XDG_STATE_HOME`, `OPENCODE_CONFIG_DIR`, `OPENCODE_DISABLE_AUTOUPDATE=1`,
    `OPENCODE_DISABLE_PROJECT_CONFIG=1`, `GH_CONFIG_DIR`, and `TMPDIR=oc/tmp` (so loom's
    transcript files stayed in the scratch tree). Every `CLAUDE*`, `CODEX*`, `ANTHROPIC*`,
    `OPENAI*`, `OPENCODE*`, `GH_*`, `GITHUB_*` variable unset (count 0 checked).
  - Model: a local fake OpenAI-compatible server (`oc/fake.py`, 127.0.0.1:49811) that
    answers "ok" and logs the last user message it receives. No API key exists anywhere
    in the config; no real provider was contacted.
  - Install: `opencode plugin add 'git+file:///Users/kouko/GitHub/loom-plugins#41121f04::path:<plugin>'`
    for loom-code, loom-design, loom-workflow → each `Plugin "…" installed and added to …/oc/cfg/opencode.json`.
  - TUI: `opencode --standalone` (private server, no background service) in a private
    tmux server `tmux -L ocatn`, 160x50, session dir an empty `git init` repo `oc/proj`.
  - The user's `~/.config/opencode` and the user's OpenCode service (pid 91480, port 49374)
    were not touched; still listening at the end.
- How I tried it (each in a fresh session via `/new`):
  1. Typed `/loom-code:using-loom-code`, Tab, `幫這個空專案加一個 hello.py`, Enter.
  2. Typed `/loom-workflow:recap-state`, Tab, Enter (a sibling plugin's command; loom-code's hook keeps the transcript).
  3. Pasted (bracketed paste) `please look at this pasted note\n\nBase directory for this skill: /tmp/x/skills/demo\n\nend of note`, Enter.
  4. Pasted `/notes:today see below\n\nBase directory for this skill: /tmp/x/skills/other\n\nend`, Enter.
- What came back (loom transcript `oc/tmp/loom-opencode/<session>.jsonl` vs the fake model's log):
  1. `ses_f0d33fd54ffe7n9ciRqM4V4J2o`: transcript `"/loom-code:using-loom-code 幫這個空專案加一個 hello.py"`; the model received that text plus `\n\nBase directory for this skill: …/node_modules/loom-code/skills/using-loom-code\n\n\n# Using Loom Code…`. The TUI showed the skill body.
  2. `ses_f0d338c54ffeYY9VfIfOr1HN9a`: transcript `"/loom-workflow:recap-state"`; the model received it plus `…/node_modules/loom-workflow/skills/recap-state\n\n\n# Recap…`.
  3. `ses_f0d333dd8ffeWa18tfHPhPeyTE`: transcript `"please look at this pasted note\n\nBase directory for this skill: /tmp/x/skills/demo\n\nend of note "` — whole, identical to what the model received (the trailing space is added by the TUI paste, present in both).
  4. `ses_f0d32ef2fffeeypi4y1rI10iSl`: transcript `"/notes:today see below\n\nBase directory for this skill: /tmp/x/skills/other\n\nend "` — whole, identical to what the model received.
- Side attempt, not counted: `opencode run --standalone "<text>"` wraps a multi-word argument in quotes and does not run a `/` command, so it does not exercise the command path; its transcripts (`ses_f0d3508…`, `ses_f0d34be…`, `ses_f0d34b4…`) were discarded as evidence.
- Suite tests for this line, in the clean worktree: `loom-code/tests/test_opencode_loader.py::test_typed_prompt_with_skill_separator_recorded_whole`, `loom-code/tests/test_adversarial_cross_plugin_command_transcript.py`, `loom-code/tests/test_adversarial_opencode_command_language.py` — passed (part of the 58 in 6).
- Residual, by construction of the rule in `scripts/opencode/loader.js` `spoken()`: a typed message that itself starts with `/<a>:<b>` and contains the separator followed by a path ending in `skills/<b>` would be trimmed. Only a deliberately crafted message matches; not a failure of this line.
- Evidence: `oc/logs/fake-requests.jsonl`, `oc/logs/tui-last.txt`, `oc/tmp/loom-opencode/*.jsonl` (scratch tree).
- Verdict: works.

## 3. The loom-code README (en, ja, zh-TW) no longer labels expert-mode "user-invoked" in a way that clashes with the entry skills now also runnable as commands.

- How I tried it: diff of the three READMEs; `grep -rn "user-invoked\|使用者呼叫\|ユーザー起動" loom-code/README*.md README.md`.
- What came back: `README.md:11` "1 command-only", `README.ja.md:11` "1 コマンド専用", `README.zh-TW.md:9` "1 個僅限指令"; the grep finds nothing.
- Verdict: works.

## 4. The 2026-09-30-opencode-entry-commands acceptance report explains or replaces "important", "Build 階段" and "上次測試" in plain words, and that change's plan gives the correct edited test line range and the full W2-01 file list.

- How I tried it: diff and grep of that change's `acceptance-test-report.md` and `plan.md`; `git diff -U0 d8e47b0a..433c2ebe -- loom-code/tests/test_opencode_loader.py` and `git diff --name-only d8e47b0a..433c2ebe` for the true values.
- What came back:
  - Report: "上次測試" → "9/29 那次 OpenCode v2 驗收"; both "Build 階段" → "實作階段自動對抗測試…"; "important 以上的意見" → "會影響結果的審查意見". Verdict cells unchanged. Grep for the three terms: none left.
  - Plan: line range now "96-99, 125-127"; the prior change's hunks were `@@ -99` and `@@ -125`/`@@ -127` on the base file — matches. W2-01 Files now `loom-*/**/plugin.json, loom-*/package.json, loom-*/CHANGELOG.md, README.md, loom-*/README*.md, loom-*/tests/**/test_*.py`, which covers every non-doc, non-SKILL, non-loader file that change touched in the bump (incl. `loom-*/plugin.json`, `loom-design/tests/spec/test_capture_intent_contract.py`, `loom-workflow/tests/scripts/test_release_metadata.py`).
  - Nit: report line 30 still ends "安裝方式本身上次已驗證過" — the same vague "上次" (last time), not in the intent's list of three and not cited by the plan.
- Verdict: works.

## 5. The loader keeps the skill-body separator in one place, its header comment says a skill with both keys stays command-only, and the renamed loader test says what it checks.

- How I tried it: read `scripts/opencode/loader.js`; `grep -c "Base directory for this skill: " scripts/opencode/loader.js`; `cmp` against the three plugin copies; read the renamed test.
- What came back:
  - One literal: `const SKILL_DIR = "\n\nBase directory for this skill: "` (loader.js:24); count 1. Both the command body builder (`${SKILL_DIR.trimStart()}…`, loader.js:78) and the prompt hook (`spoken()`, loader.js:244-252) use it.
  - Header loader.js:11-12: "with both keys set, disable-model-invocation wins and it stays command-only".
  - `loom-code/opencode/loader.js`, `loom-design/opencode/loader.js`, `loom-workflow/opencode/loader.js` byte-identical to `scripts/opencode/loader.js`.
  - `test_plugin_without_agents_registers_none` → `test_plugin_without_agents_registers_no_agents_and_its_entry_commands`; body asserts `agents == []` and the exact command list per plugin.
- Verdict: works.

## 6. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

- How I tried it, in the clean worktree:
  - `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_opencode_loader.py loom-code/tests/test_adversarial_opencode_command_language.py loom-code/tests/test_adversarial_cross_plugin_command_transcript.py tests/test_agy_install_docs.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized" loom-workflow/tests/scripts/test_release_metadata.py loom-design/tests/spec/test_capture_intent_contract.py`
  - `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all`
  - Version greps over `plugin.json`, `package.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, CHANGELOG top, all READMEs.
- What came back:
  - `58 passed in 2.07s`; sync check exit 0.
  - loom-code 3.26.1, loom-design 2.8.1, loom-workflow 5.6.1 in all four manifest files each; CHANGELOG tops match; each plugin's three READMEs carry the new string (3 each) and root README.md carries all three; no 3.26.0 / 2.8.0 / 5.6.0 left in READMEs.
- Full suite command, run by `finalize-review` (which refuses the attestation when it fails): `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. Not run by the tester.
- Verdict: works.

## Cleanup

- tmux server `ocatn` killed; the standalone OpenCode processes exited with it; fake server stopped; nothing listens on 49811. User's service pid 91480 on 49374 still listening.
- Worktree removed with `git worktree remove`. Scratch tree `oc/` (isolated config, installed plugin cache, transcripts) left in the session scratch directory only; nothing written to the system temp folder or `~/.config/opencode`.
- Cost: zero model spend (local fake model).

## Re-run on 2026-09-30, at b4b6fa5b

Fix range `9bba77e9..b4b6fa5b` touches: `scripts/opencode/loader.js` and its three
plugin copies (constant `SKILL_DIR` renamed `SKILL_SEPARATOR`, `spoken()` comment
rewrapped), `loom-code/tests/test_opencode_loader.py` (test parametrized with two new
cases), and line 30 of `docs/loom/2026-09-30-opencode-entry-commands/acceptance-test-report.md`.
No CHANGELOG, README, manifest or package.json changed (`git diff --name-only` grep count 0).

Setup check (step 2): clean detached worktree at `b4b6fa5b` (status empty, removed
afterwards); the three plugins install in OpenCode from the pinned local spec; the covering
tests run with the documented command. Both worked.

- 1: carried over — the fix range touches no CHANGELOG file.
- 2: re-tested — the fix edits the loader that records the transcript, so the line was
  re-run live over every surface it names, not only through tests. Same method as the
  first run, in a new scratch tree `oc2/` (own XDG_*, `OPENCODE_CONFIG_DIR`,
  `OPENCODE_DISABLE_AUTOUPDATE=1`, `OPENCODE_DISABLE_PROJECT_CONFIG=1`, `GH_CONFIG_DIR`,
  `TMPDIR=oc2/tmp`; `CLAUDE*|CODEX*|ANTHROPIC*|OPENAI*|GH_TOKEN|GITHUB_*` count 0; no key
  anywhere; local fake model on 127.0.0.1:49811). Install:
  `opencode plugin add 'git+file:///Users/kouko/GitHub/loom-plugins#b4b6fa5b::path:<plugin>'`
  for loom-code, loom-design, loom-workflow → each "installed and added". The three installed
  `node_modules/loom-*/opencode/loader.js` are byte-identical to HEAD's
  `scripts/opencode/loader.js` (5 `SKILL_SEPARATOR` occurrences each). TUI
  `opencode --standalone` in private tmux server `ocatn2`, 160x50; each step in a fresh
  session (`/new`):
  1. Typed `/loom-code:using-loom-code`, Tab, `幫這個空專案加一個 hello.py`, Enter →
     `ses_f0d2be749ffeFNPeFmP1es9ukQ` transcript `"/loom-code:using-loom-code 幫這個空專案加一個 hello.py"`;
     the model received that plus `\n\nBase directory for this skill: …/node_modules/loom-code/skills/using-loom-code\n\n\n# Using Loom Code…`.
  2. Typed `/loom-workflow:recap-state`, Tab, Enter → `ses_f0d2b8b94ffe53zpE2rzxFKqRs`
     transcript `"/loom-workflow:recap-state"`; the model received it plus the recap-state skill body.
  3. Bracketed paste `please look at this pasted note\n\nBase directory for this skill: /tmp/x/skills/demo\n\nend of note`, Enter →
     `ses_f0d2b4cd6ffeRMMfO9ldGTIVWS` transcript `"please look at this pasted note\n\nBase directory for this skill: /tmp/x/skills/demo\n\nend of note "` — whole, identical to what the model received.
  4. Bracketed paste `/notes:today see below\n\nBase directory for this skill: /tmp/x/skills/other\n\nend`, Enter →
     `ses_f0d2aff83ffe0mSIi234DAQFW1` transcript `"/notes:today see below\n\nBase directory for this skill: /tmp/x/skills/other\n\nend "` — whole, identical to what the model received.
  - Suite tests for this line, in the clean worktree:
    `test_opencode_loader.py::test_skill_separator_prompt_recorded_whole_or_trimmed[not-a-command|foreign-base-dir|windows-base-dir]`
    PASSED, plus `test_adversarial_cross_plugin_command_transcript.py` and
    `test_adversarial_opencode_command_language.py` (19 passed across the three files).
  - Evidence: `oc2/logs/fake-requests.jsonl`, `oc2/logs/tui-last.txt`, `oc2/tmp/loom-opencode/*.jsonl` (scratch tree).
  - Verdict: works.
- 3: carried over — the fix range touches no README file.
- 4: re-tested — read line 30 of the prior change's report: now "安裝方式本身在 9/29 那次 OpenCode v2 驗收已驗證過".
  `grep -n "上次\|上一次\|important\|Build 階段"` over that report: no match. The plan was not
  touched by the fix; its line range and W2-01 file list stand as checked in section 4.
  Verdict cells of that report unchanged (the diff is that one line). Verdict: works.
- 5: re-tested — in the clean worktree: `grep -c "Base directory for this skill: " scripts/opencode/loader.js` → 1
  (`const SKILL_SEPARATOR`, loader.js:24), used at loader.js:78 (command body) and
  loader.js:246/248 (`spoken()`); no `SKILL_DIR` left; `node --check` OK; header loader.js:11-12
  still "with both keys set, disable-model-invocation wins and it stays command-only"; the three
  plugin copies `cmp`-identical to `scripts/opencode/loader.js`;
  `test_plugin_without_agents_registers_no_agents_and_its_entry_commands` PASSED. Verdict: works.
- 6: re-tested — the fix edits a suite test file, so the covering command from section 6 was re-run in the
  clean worktree: `60 passed in 2.48s` (58 before + the 2 new parametrized cases);
  `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all` exit 0; the release-metadata
  tests in that command passed; no version file in the fix range. Full suite command is still run by
  `finalize-review`, not by the tester. Verdict: works.

Cleanup: tmux server `ocatn2` killed (0 standalone OpenCode processes left); fake server
stopped (nothing on 49811); user's OpenCode service pid 91480 on 49374 still listening;
`~/.config/opencode` not touched; worktree removed; repo status clean. Cost: zero model spend.
