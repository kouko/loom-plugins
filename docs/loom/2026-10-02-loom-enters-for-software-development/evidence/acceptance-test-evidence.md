# Loom enters for software development without outside rules — acceptance test evidence

Tried on 2026-10-02, in a clean copy of the project at ec97d065 (a detached
`git worktree add` of HEAD in the session scratchpad; no file in it was edited).

## Setup (every run)

- Clean copy: `git worktree add --detach <scratchpad>/at/wt HEAD` → `HEAD is now at ec97d065`.
- Claude Code 2.1.287 loaded this branch's plugins, not the installed cache copy:
  `claude -p "<request>" --output-format stream-json --verbose --permission-mode bypassPermissions --max-turns 25 --model opus --settings '{"enabledPlugins":{"loom-code@loom":false,"loom-design@loom":false,"loom-workflow@loom":false,"loom-code@monkey-skills":false,"loom-design@monkey-skills":false,"loom-workflow@monkey-skills":false}}' --plugin-dir wt/loom-code --plugin-dir wt/loom-design --plugin-dir wt/loom-workflow`
  - Every transcript's `init` message lists exactly `loom-code@inline 3.28.0`, `loom-design@inline 2.10.0`, `loom-workflow@inline 5.6.2` with paths under the worktree; no `@loom` / `@monkey-skills` loom copy loaded.
  - The user's own settings, other plugins and personal rules stayed active (realistic competition, for example `domain-teams:code-team`). `grep -i loom ~/.claude/CLAUDE.md` → no match; the three rules files mention loom only in a changelog line recording the removal.
  - `--model opus` was needed because the user's default model `hyper-coding-group[1m]` returns 404 in `-p` mode (first attempt: `model_not_found`).
  - `--disable-slash-commands` was NOT used.
- Codex 0.158.0 loaded this branch's plugins from a temporary `CODEX_HOME` (`<scratchpad>/at/codexhome`): only `auth.json` and the user's `~/.codex/AGENTS.md` copied in (`grep -ci loom` → 0), then
  `codex plugin marketplace add <scratchpad>/at/wt` and `codex plugin add loom-code@loom` / `loom-design@loom` / `loom-workflow@loom` → `loom-code@loom installed, enabled 3.28.0`, `loom-design@loom … 2.10.0`, `loom-workflow@loom … 5.6.2`; `[features] hooks = true`.
  Hook trust: `--dangerously-bypass-hook-trust` (trust for that invocation only, inside the temporary home). The user's real `~/.codex/config.toml` was not touched.
  Trial command: `CODEX_HOME=<tmp> codex exec -m gpt-5.5 --json -s workspace-write --dangerously-bypass-hook-trust -C <repo> "<request>"`.
- Trial repos (each a fresh `git init` with `app.py` containing `greet` with the docstring typo "greating", `x` as a local, and `add` returning `a - b`, plus `README.md`): `*-loom` ones additionally have `docs/loom/README.md`; `*-noloom` ones have no `docs/` at all.
- Transcripts: `<scratchpad>/at/<trial>.jsonl` (Claude stream-json, Codex exec JSON) and Codex rollouts under `<tmp CODEX_HOME>/sessions/2026/10/02/`. Summarised with two small scripts (`analyze.py`, `analyze_cx.py`) that print the ordered tool calls, the injected session-start text and `git status` after.

## 1. On Claude Code and on Codex, in a live session with no loom lines in the user's personal rules, a request to add a feature or fix a bug that does not mention loom starts loom's intent capture before any file is edited — both in a repository that already has a loom folder and in one that does not.

- How I tried it: 8 live sessions, none mentioning loom.
  - Feature (zh): 「幫我加一個功能：greet 可以選擇用日文打招呼（傳入 lang='ja' 時回傳 こんにちは）。」 in a repo with a loom folder.
  - Feature (en): "add a feature that lets greet() take an optional exclamation flag that appends '!' to the greeting" in a repo without one.
  - Bug: "fix this bug: add(2, 3) returns -1 instead of 5" in both kinds of repo.
- What came back:

| Host | Trial | First tool action | Files touched | `git status` after |
|---|---|---|---|---|
| Claude Code | feat, loom folder | `Skill -> loom-design:capture-intent` | intent file only | `?? docs/loom/intent/` |
| Claude Code | feat, no folder | `Skill -> loom-design:capture-intent` | intent file only | `?? docs/` |
| Claude Code | bug, loom folder | `Skill -> loom-design:capture-intent` | intent file only (Write) | `?? docs/loom/intent/` |
| Claude Code | bug, no folder | `Skill -> loom-design:capture-intent` | intent file only | `?? docs/` |
| Codex | feat, loom folder | msg "我會先用 `loom-design:capture-intent`…"; reads `…/loom-design/2.10.0/skills/capture-intent/SKILL.md` | `add docs/loom/intent/2026-10-02-japanese-greeting.md` | `?? docs/loom/intent/` |
| Codex | feat, no folder | msg "我會先走 intent…"; reads capture-intent SKILL.md | `add PRINCIPLES.md`, `add docs/loom/intent/2026-10-02-exclamation-greeting.md` | `?? PRINCIPLES.md; ?? docs/` |
| Codex | bug, loom folder | msg "I'll use `loom-design:capture-intent` because this is a behavior-changing bug fix…" | `add docs/loom/intent/2026-10-02-fix-addition-result.md` | `?? docs/loom/intent/` |
| Codex | bug, no folder | msg "I'll use `loom-design:capture-intent` first…" | `add docs/loom/intent/2026-10-02-fix-addition-result.md` | `?? docs/` |

  - `app.py` is unmodified in all eight repos. Seven sessions added only the intent file; the Codex no-folder feature run also added `PRINCIPLES.md`. Every session ends asking the user to confirm the restated intent (decision point ①). Example (Claude, bug, no folder): "I've found the cause and written down what the fix needs to do. I need your yes before I change any code."
  - Each Claude transcript shows the `SessionStart:startup` hook response containing "You have loom-code. Software-development work runs through stations…" and the line "Any software-development request that adds a feature or fixes a bug starts at capture-intent…", outcome `success`. Each Codex rollout carries the same text as a `developer` message.
- Evidence: `<scratchpad>/at/cc-{feat,bug}-{loom,noloom}.jsonl`, `<scratchpad>/at/cx-{feat,bug}-{loom,noloom}.jsonl` and their rollouts; the table above is the trimmed output of `analyze.py` / `analyze_cx.py`.
- Note: the Codex no-folder feature run also drafted a `PRINCIPLES.md` (the capture-intent station's missing-principles step), still before any code edit.

## 2. On Claude Code and on Codex, a small edit request (a typo fix or a rename) is made directly without starting loom, and starts loom when the user asks for loom.

- How I tried it: repos with a loom folder (the stricter case). "fix the typo in the greet docstring (greating)", "rename variable x to message in greet", and "use loom: fix the typo in the greet docstring (greating)".
- What came back:

| Host | Trial | Skill / loom? | Result |
|---|---|---|---|
| Claude Code | typo | no Skill call; `grep` then `sed` on app.py | `app.py \| 2 +-`; reply: "Only the docstring text changed… That's why I skipped the loom process" |
| Claude Code | rename | no Skill call | `app.py \| 4 ++--`; reply notes `greet('kouko')` unchanged |
| Claude Code | use loom + typo | `Skill -> loom-design:capture-intent` | only `?? docs/loom/intent/`, app.py untouched, asks for "yes" |
| Codex | typo | no skill read; "I'll make the docstring-only typo fix directly" | diff `greating` → `greeting` only |
| Codex | rename | no skill read; "我會直接做這個純命名修改" | diff `x` → `message`; ran `assert greet('kouko') == 'Hello, kouko'` → ok |
| Codex | use loom + typo | reads `…/capture-intent/SKILL.md`; "我會用 Loom 走最小流程" | only `add docs/loom/intent/2026-10-02-fix-greet-docstring-typo.md`, asks for confirmation |

- Evidence: `<scratchpad>/at/cc-typo.jsonl`, `cc-rename.jsonl`, `cc-typo-useloom.jsonl`, `cx-typo.jsonl`, `cx-rename.jsonl`, `cx-typo-useloom.jsonl`.

## 3. On Claude Code, a request that is not software development (for example research or note-taking in a notes folder) does not start loom.

- How I tried it: a non-git folder `cc-notes/` holding `reading.md` and `ideas.md`; request 「幫我研究一下「刻意練習」這個概念，整理成一則筆記放在這個資料夾裡，並把它加到 ideas.md 的清單。」
- What came back: the loom session-start text was injected (hook outcome `success`), yet no Skill call at all; tool sequence `Bash ls/cat` → `Write deliberate-practice.md` → `Edit` → `Bash` append to `ideas.md` → `WebSearch` ×2 → `Edit`. No `docs/loom` created. `ideas.md` gained "- deliberate practice（刻意練習）→ deliberate-practice.md".
- Evidence: `<scratchpad>/at/cc-notes.jsonl`.

## 4. Antigravity CLI and OpenCode load the same session-start instruction as Claude Code, shown from the files each host loads.

- How I tried it: `hosts_compare.py` reads each host's own hook config from the clean copy and runs exactly that command:
  - Claude Code: `hooks/hooks.json` SessionStart → `"${CLAUDE_PLUGIN_ROOT}/hooks/session-start"`.
  - Codex: `hooks/hooks-codex.json` SessionStart → `"${PLUGIN_ROOT}/hooks/session-start"`.
  - Antigravity CLI: plugin-root `hooks.json` PreInvocation → `python3 ./hooks/agy_adapter.py pre-invocation` (cwd = plugin root, first-turn payload `invocationNum: 0`, `workspacePaths: [<repo>]`); text read from `injectSteps[].ephemeralMessage`.
  - OpenCode: `node` loads `loom-code/index.js` → `opencode/loader.js` with a stub ctx, fires the session `context` hook, which runs `hooks/hooks-opencode.json` SessionStart (`bash "${PLUGIN_ROOT}/hooks/session-start"`); text read from `ev.system`.
- What came back (repo without a loom folder; identical result in a repo with one):
  ```
  claude-code text words: 349 | routing line present: True
  claude-code: identical=True
  codex: identical=True
  agy: identical=True  (top-level keys: ['injectSteps'])
  opencode: identical=True
  ```
  All four exit 0 with empty stderr.
- Evidence: `<scratchpad>/at/hosts_noloom.txt`, `hosts_loom.txt`. Not a live agy or OpenCode session (not asked for; installing there would replace the user's installed copies).

## 5. On Codex, the session-start hook runs without being marked failed.

- How I tried it:
  - Ran the Codex command from `hooks-codex.json` directly → stdout is one JSON object with top-level keys `['hookSpecificOutput']` only (`hookEventName: SessionStart`, `additionalContext` = the 349-word text). With `LOOM_CODE_MODE=off`: `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":""}}` — same single key.
  - Live: all 7 `codex exec` sessions (A1/A2) have the session-start text as a `developer` message in their rollouts; Codex drops the context of a hook it marks failed, so delivery shows it was accepted.
  - Live interactive TUI (pty-driven, temp home, `--dangerously-bypass-hook-trust`, prompt "Reply with the single word: ok"): the screen showed "⚠ 2 warnings"; F2 showed warning 1 "Running without the shared background server: --dangerously-bypass-hook-trust requires embedded mode." The captured screen contains 0 occurrences of "failed"; the only "hook" text is that warning. That session's rollout also carries the session-start text.
- Evidence: `<scratchpad>/at/tui_probe.txt`, rollout `rollout-2026-10-02T11-31-31-01a0faaa-….jsonl`; covered in the suite by `loom-code/tests/test_session_start_words.py` and `loom-code/tests/test_hooks_json.py`.
- Accepted limitation (b) — no fallback when the installed plugin folder is stale — was not exercised (fresh install).

## 6. The three small issues left by PR #74 are fixed: the ship station no longer mentions a narrow-change line nothing produces, the verification status no longer takes a depth argument whose values behave the same, and the trailing blank line in its test file is removed.

- How I tried it / what came back:
  - `grep -rn "Skipped as a narrow change" loom-code loom-design loom-workflow` (py/md) → only CHANGELOG history lines; `loom-code/skills/ship/SKILL.md:92-93` now reads "The `Verification status:` line already arrives in that form from the checker." The two remaining "narrow-change simplification" sentences (`ship/SKILL.md:30`, `:84`) refer to the attestation's real simplification, not the removed line.
  - `inspect.signature(verification_status)` → `(repo, change_id, *, base=None, head='HEAD', manifest=None)`; `grep depth` over `verification.py` and `command_handlers/` → none; callers `land.py:965`, `publish.py:397`, `push.py:71`, `pr_floor.py:59` pass no depth.
  - `tail -c 80 loom-code/tests/test_selection_finalize.py | od -c` → file ends `dirty.stderr\n` (single newline, no blank line).
- Evidence: commands above, run in the clean copy.

## 7. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

- How I tried it: in the clean copy,
  `set -o pipefail; env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` and `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all`.
- What came back:
  - Suite exit 0 (run twice, both exit 0). pytest blocks total 3,045 passed, 6 skipped, 0 failed; every shell-test "Summary:" line reads `/ 0 FAIL`.
  - `sync_codex_manifests.py --check --all` exit 0.
  - loom-code 3.28.0 in `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json`, CHANGELOG top entry `## [3.28.0] — 2026-10-02`, README.md / README.ja.md / README.zh-TW.md and root README "Version 3.28.0".
  - loom-design 2.10.0 in the same four manifests, CHANGELOG top entry `## [2.10.0] — 2026-10-02`, its three READMEs and root README "Version 2.10.0".
  - loom-workflow: no file changed in `e89ee98d..HEAD`, stays 5.6.2 everywhere.
- Evidence: `<scratchpad>/at/suite-full.log` (tail: `exit=0`).

## Accepted limitation (a)

The form-feed character in KICKOFF-DEFAULTS making the session-start JSON invalid was not observed: none of the trial repos has a KICKOFF-DEFAULTS file.

## Re-run on 2026-10-02, at 7596b677

Fix range `6b791881..7596b677` (4 commits: fe5e65af, b62631ac, 0bb15eb5, 7596b677) changes the session-start routing paragraph, the maintain / capture-intent descriptions, the using-loom-code router row, write-plan step 1, `codex-first-contact.md`, READMEs, CHANGELOGs, plan W3-01 and three tests. It touches nothing under `loom-code/skills/ship`, `loom-code/scripts` or `loom-code/tests/test_selection_finalize.py`.

Setup (fresh, new directory `<scratchpad>/at2`; script `at2/setup.sh`):
- Clean copy: `git worktree add --detach <scratchpad>/at2/wt 7596b677` → `HEAD is now at 7596b677`. Installed and worktree `hooks/session-start` both contain the new sentence "even when it reads as a bug report".
- Claude Code: same `claude -p … --model opus --settings '{"enabledPlugins":{…loom@loom/@monkey-skills: false}}' --plugin-dir at2/wt/loom-{code,design,workflow}` command as before (`at2/run_cc.sh`). Every transcript's `init` lists `loom-code@inline 3.28.0`, `loom-design@inline 2.10.0`, `loom-workflow@inline 5.6.2`. `--disable-slash-commands` not used.
- Codex 0.158.0: new temporary `CODEX_HOME=at2/codexhome` (only `auth.json` and `~/.codex/AGENTS.md` copied in; `grep -ci loom AGENTS.md` → 0), `codex plugin marketplace add at2/wt`, `codex plugin add loom-{code,design,workflow}@loom` → installed 3.28.0 / 2.10.0 / 5.6.2, `[features] hooks = true`. Trial command `codex exec -m gpt-5.5 --json -s workspace-write --dangerously-bypass-hook-trust -C <repo> "<request>"` (`at2/run_cx.sh`). No `turn.failed` in any transcript; the only "400" strings are skill text ("Paul Nutt's study of 400 business decisions").
- Trial repos: fresh `git init` with the same `app.py` / `README.md` fixture; `*-loom` add `docs/loom/README.md`, `*-noloom` have no `docs/`. `cc-comment` adds the line `# build the greeting text` inside `greet`. Notes folder `cc-notes/` (not git) with `reading.md`, `ideas.md`.
- Summaries: `at/analyze.py` (Claude) and `at2/analyze_cx.py` (Codex; routing-line check switched to the new sentence). Transcripts `at2/<trial>.jsonl`, rollouts under `at2/codexhome/sessions/2026/10/02/`.

- 1: re-tested — 12 live sessions, none mentioning loom: feature (zh, loom folder) 「幫我加一個功能：greet 可以選擇用日文打招呼（傳入 lang='ja' 時回傳 こんにちは）。」; feature (en, no folder) "add a feature that lets greet() take an optional exclamation flag that appends '!' to the greeting"; bug "fix this bug: add(2, 3) returns -1 instead of 5" and bug-report phrasing "users report that add(2, 3) gives the wrong answer, please fix it", each in both repo kinds, on both hosts.

  | Host | Trial | First action | Files added | `git status` after |
  |---|---|---|---|---|
  | Claude Code | feat, loom folder | `Skill -> loom-design:capture-intent` | intent | `?? docs/loom/intent/` |
  | Claude Code | feat, no folder | `Skill -> loom-design:capture-intent` | intent | `?? docs/` |
  | Claude Code | bug, loom folder | `Skill -> loom-design:capture-intent` | intent (Write) | `?? docs/loom/intent/` |
  | Claude Code | bug, no folder | `Skill -> loom-design:capture-intent` | intent | `?? docs/` |
  | Claude Code | bug report, loom folder | `Skill -> loom-design:capture-intent` | intent | `?? docs/loom/intent/` |
  | Claude Code | bug report, no folder | `Skill -> loom-design:capture-intent` | intent | `?? docs/` |
  | Codex | feat, loom folder | msg "我會先走這個 repo 的變更流程…"; reads `loom-design/2.10.0/skills/capture-intent/SKILL.md`, `references/interview.md`, `templates/intent.md`, `templates/PRINCIPLES-interview.md` | `PRINCIPLES.md`, `docs/loom/intent/2026-10-02-japanese-greeting.md` | `?? PRINCIPLES.md; ?? docs/loom/intent/` |
  | Codex | feat, no folder | msg "我會先用 `loom-design:capture-intent`，因為這是新增功能…" | `PRINCIPLES.md`, intent | `?? PRINCIPLES.md; ?? docs/` |
  | Codex | bug, loom folder | msg "I'll use the Loom intent step first, because this is a bug fix…" | `…/2026-10-02-fix-add-returns-sum.md` | `?? docs/loom/intent/` |
  | Codex | bug, no folder | msg "I'll use the Loom intent step first because this is a bug fix…" | `…/2026-10-02-fix-addition-result.md` | `?? docs/` |
  | Codex | bug report, loom folder | msg "I'll use the Loom intent step first because this is a bug fix request…" | `…/2026-10-02-fix-add-wrong-answer.md` | `?? docs/loom/intent/` |
  | Codex | bug report, no folder | msg "I'll use `loom-design:capture-intent` because this is a bug-fix request…" | `…/2026-10-02-fix-add-wrong-answer.md` | `?? docs/` |

  `git diff --stat -- app.py` is empty in all 12 repos. All 12 end asking the user to confirm the restated intent. None routed the bug report to maintain. Every Claude transcript has the `SessionStart` hook response with the new routing paragraph (outcome `success`); every Codex rollout carries it as developer context. Codex drafted `PRINCIPLES.md` in both feature runs (neither repo had one); Claude Code wrote no `PRINCIPLES.md`.
- 2: re-tested — repos with a loom folder: "fix the typo in the greet docstring (greating)", "rename variable x to message in greet", "use loom: fix the typo in the greet docstring (greating)"; plus Claude Code boundary cases "reword the README description from 'A tiny greeting app.' to 'A small app that greets people by name.'" and "reword the comment in greet from 'build the greeting text' to 'join the salutation and the name'".

  | Host | Trial | Loom? | Result |
  |---|---|---|---|
  | Claude Code | typo | no Skill call; `grep` → `sed` | `M app.py`; "Because this was only a wording fix with no change in behaviour, I made the edit directly instead of running it through the loom steps." |
  | Claude Code | rename | no Skill call; Read → Edit | `M app.py`; ran `greet('kouko')` → `Hello, kouko` |
  | Claude Code | use loom + typo | `Skill -> loom-code:using-loom-code` → `Skill -> loom-design:capture-intent` | only `?? docs/loom/intent/`; app.py untouched; asks for confirmation |
  | Claude Code | doc wording | no Skill call; `sed` on README.md | `M README.md`; "It's a wording-only edit, so I made it directly without the full feature workflow." |
  | Claude Code | comment wording | no Skill call; `sed` on app.py line 3 | `M app.py`, comment only |
  | Codex | typo | no skill read; "I'll make the smallest doc-only edit…" | `M app.py`, `greating` → `greeting` |
  | Codex | rename | no skill read | `M app.py`, `x` → `message` |
  | Codex | use loom + typo | reads capture-intent SKILL.md; "我會走 Loom，因為你明確要求" | only `?? docs/loom/intent/` (`2026-10-02-fix-greet-docstring-typo.md`); asks for "yes" |
- 3: re-tested — `cc-notes/`, same request 「幫我研究一下「刻意練習」這個概念，整理成一則筆記放在這個資料夾裡，並把它加到 ideas.md 的清單。」. Session-start text injected (outcome `success`), no Skill call; tools: `Bash ls/cat` → `ToolSearch WebSearch` → `WebSearch` ×4 → `Write deliberate-practice.md` → `Bash` append to `ideas.md`. Folder afterwards: `deliberate-practice.md ideas.md reading.md`, no `docs/loom`; `ideas.md` gained "- deliberate practice".
- 4: re-tested — `at2/hosts_compare.py` (same script, base path changed) against fresh dirs `at2/host-noloom` and `at2/host-loom`, exit 0 both: all four hosts exit 0, empty stderr; `claude-code text words: 401 | routing line present: True`; `codex: identical=True`, `agy: identical=True` (keys `['injectSteps']`), `opencode: identical=True`; the printed routing paragraph contains "A user asking for a bug to be fixed starts there too, even when it reads as a bug report; maintain takes alerts, CI or regression failures and dogfood incidents…" and "(a typo, a rename that changes no behaviour, comment or doc wording)". Evidence `at2/hosts_noloom.txt`, `at2/hosts_loom.txt`. Still no live agy / OpenCode session.
- 5: re-tested — `PLUGIN_ROOT=at2/wt/loom-code bash -c '"${PLUGIN_ROOT}/hooks/session-start"'` → keys `['hookSpecificOutput']`, inner `['hookEventName', 'additionalContext']`, `SessionStart`, 401 words; with `LOOM_CODE_MODE=off` → `{"hookSpecificOutput":{"hookEventName":"SessionStart","additionalContext":""}}`, exit 0. Live: all 9 `codex exec` rollouts carry the new paragraph as developer context. TUI probe (`at2/tui_probe.py`, temp home, prompt "Reply with the single word: ok") → reply "ok", screen "⚠ 2 warnings", warning 1 "Running without the shared background server: --dangerously-bypass-hook-trust requires embedded mode."; `grep -ci failed tui_probe.txt` → 0; rollout `rollout-2026-10-02T11-56-36-01a0fac1-….jsonl` contains the new sentence (count 1).
- 6: carried over — `git diff --stat 6b791881..7596b677 -- loom-code/skills/ship loom-code/scripts loom-code/tests/test_selection_finalize.py` is empty; the three fixed spots are not in the fix range.
- 7: re-tested — in `at2/wt`: `set -o pipefail; env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` → `exit=0`; pytest blocks total 3,040 passed, 11 skipped, 0 failed; all 17 shell "Summary:" lines read `/ 0 FAIL`. The 5 skips more than last run are `loom-workflow/tests/loom-visualization/test_adversarial_probes.py:194` ("node or tests/mermaid/node_modules absent"): a fresh worktree has no `node_modules` until the suite's later `npm ci` step; re-running `pytest loom-workflow/tests/loom-visualization -q -rs` afterwards → 206 passed, 0 skipped. `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all` → exit 0. Versions: loom-code 3.28.0 in `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json`, CHANGELOG top `## [3.28.0] — 2026-10-02`, its three READMEs and root README; loom-design 2.10.0 likewise; loom-workflow unchanged in `e89ee98d..HEAD`, stays 5.6.2. Log `at2/suite.log`, `at2/sync.log`.
