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

  - `app.py` is unmodified in all eight repos; every session ends asking the user to confirm the restated intent (decision point ①). Example (Claude, bug, no folder): "I've found the cause and written down what the fix needs to do. I need your yes before I change any code."
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
