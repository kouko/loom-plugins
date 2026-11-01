# Record repo lessons when the agent saves its own memory — acceptance test evidence

Tried on 2026-10-24, in a clean copy of the project at 5199797f
(`git worktree add --detach <scratchpad>/at/clean HEAD`; old plugin exported
with `git archive b1b8cd77 loom-workflow`, new with `git archive HEAD loom-workflow`).

## Setup

- README install path (`claude plugin install loom-workflow@loom`) would
  install into the user's real config, so each version was loaded per
  session with `--plugin-dir <export>/loom-workflow` instead.
- Isolation: `CLAUDE_CONFIG_DIR=<tmp>` cannot authenticate on this machine
  ("Not logged in · Please run /login"), so the real config was used with
  `--setting-sources ""` (no user settings, no user-installed plugins) and
  `--settings '{"autoMemoryEnabled":true,"autoMemoryDirectory":"<trial>/fakehome/.claude/projects/-trial-<tag>/memory"}'`.
  The fake path keeps the real shape `.claude/projects/<slug>/memory`, so the
  hook's path test is exercised as in production. Probe session confirmed:
  init `plugins` lists only `loom-workflow@inline` (5.15.0) plus builtins;
  the agent reported its memory dir as the fake path.
- Every trial: fresh copy of a throwaway git repo (`widget-kit`: README,
  `scripts/run_tests.py` with `TEST_ROOTS = ["tests", "plugin-a/tests"]`,
  two trivial tests, and an empty store created with
  `loom_memory.py init docs/loom/memory`), fresh fake memory dir, fresh
  `claude -p "Save this to your memory: <candidate text>"` with
  `--permission-mode bypassPermissions --output-format stream-json --verbose
  --include-hook-events --max-turns 40 --max-budget-usd 3`, never
  `--disable-slash-commands`. Model `claude-opus-5-5`.
- Runner: `<scratchpad>/at/trial.py`; per-trial stream-json in
  `<scratchpad>/at/logs/<arm>-c<case>-t<n>.jsonl`; summaries in
  `<scratchpad>/at/results.jsonl`. "Fired" = a `Skill` tool_use with
  `loom-workflow:loom-memory` in the transcript. Total cost of the 18-trial
  batch: USD 3.63.
- Nothing written to the user's real memory: `find ~/.claude/projects -path
  "*at-trials*"` shows only the session-transcript `.jsonl` files Claude Code
  keeps for every session (20 files), no `memory/` folder. The repo worktree
  stayed clean apart from these two report files.

### Trigger counts (3 trials per case per version)

| Case | Version | loom-memory fired | Skill before the memory write | Repo store changed | validate OK | Host note saved | Hook reminder seen |
|---|---|---|---|---|---|---|---|
| 1 repo-wide (RECORD) | old | 3/3 | 3/3 | 3/3 | 3/3 | 0/3 | 0/3 (no hook) |
| 1 repo-wide (RECORD) | new | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 | 3/3 |
| 2 personal preference | old | 0/3 | — | 0/3 | — | 3/3 | 0/3 |
| 2 personal preference | new | 1/3 | 1/3 | 0/3 | — | 3/3 | 3/3 |
| 3 machine-specific | old | 0/3 | — | 0/3 | — | 3/3 | 0/3 |
| 3 machine-specific | new | 3/3 | 3/3 | 0/3 | — | 3/3 | 3/3 |

Event order (new): `new-c1-t1 SKILL > Bash:loom_memory > Write(store) >
Write(host note) > HOOK > Write(host MEMORY.md) > Bash:loom_memory`;
`new-c2-t1 Write(host note) > Write(host MEMORY.md) > HOOK` (no skill);
`new-c3-t1 SKILL > Bash>host > Write(host note) > HOOK > Write(MEMORY.md)`.
Old case 1 used loom-memory *instead of* host memory (0/3 host notes).
Counts are samples, not rates.

## 1. 在乾淨環境、裝了 loom-workflow 的 Claude Code session 裡，agent 把一條「任何人跑這個 repo 都會遇到」的教訓存進內建記憶後，同一個 session 內 `docs/loom/memory/` 多出對應的教訓檔，`index.md` 已重建且 `validate` 通過。
- How I tried it: case 1, new version, 3 trials (table above).
- What came back: 3/3 `git status` = ` M docs/loom/memory/index.md`, `?? docs/loom/memory/<lesson>.md`
  (`test-roots-must-list-new-plugin-folders.md`, `test-roots-must-be-registered.md`,
  `new-plugin-tests-need-test-root.md`); `loom_memory.py validate docs/loom/memory`
  exit 0 "OK — OKF v0.2-compatible Loom memory profile holds." 3/3; host note saved 3/3.
- Pilot `new-c1-t0` (repo with NO store): skill fired, store created at
  `docs/memory/` (README.md, index.md, lesson), not `docs/loom/memory/`;
  the host note was written with `cat > $M/<note>.md <<'EOF'` (Bash), and
  `grep -c "You just wrote a host memory note"` = 0. Neither
  `loom-workflow/skills/loom-memory/SKILL.md` nor `references/operations.md`
  (old or new) names `docs/loom/memory` (grep: no match).
- Limit: every save was asked for by the user ("Save this to your memory").
  A save the agent starts on its own, mid-task, was not tried.
- Evidence: `logs/new-c1-t{1,2,3}.jsonl`, `logs/new-c1-t0.jsonl`, `results.jsonl`.

## 2. 同樣的環境裡，agent 存一條使用者個人偏好、和一條只在使用者本機成立的事（例如本機某個指令指向特定環境），兩者都不會在 `docs/loom/memory/` 產生或修改任何檔案。
- How I tried it: cases 2 and 3, new version, 3 trials each.
- What came back: repo `git status --porcelain` empty in 6/6; host note saved 6/6.
  Final replies state the reason, e.g. new-c2-t1 "I didn't add it to the
  repository, because it's your own style, not a rule for other contributors";
  new-c3-t1 "this fact is only true on this machine".
- Evidence: `logs/new-c2-t*.jsonl`, `logs/new-c3-t*.jsonl`.

## 3. 裝了 loom-workflow 的 Claude Code 中，寫入內建記憶資料夾內任何筆記（不論 `type` 為何）都會出現一次提醒；寫入其他路徑、或 hook 收到格式異常的資料時，不出現提醒也不會讓 session 出錯。
- How I tried it: `python3 -I <scratchpad>/at/hook_probe.py <clean>/loom-workflow/hooks/memory-mirror-reminder`
  (21 PostToolUse payloads on stdin); live: `--include-hook-events` in 10 new-version sessions.
- What came back: `FAILS 0`. Reminder (one JSON line, `hookEventName: PostToolUse`,
  exit 0, no stderr) for note type user/feedback/project/reference, an Edit of a
  note, a note under `$CLAUDE_CONFIG_DIR`, a non-normalized `../` path. Silent,
  exit 0, no stderr for MEMORY.md, memory.md, repo `docs/loom/memory/lesson.md`,
  repo source file, `.json` in memory dir, subfolder of memory, custom dir with
  env unset, empty stdin, non-JSON, JSON array, missing tool_input,
  file_path null / number, invalid UTF-8.
- Live: reminder seen in 9/9 batch sessions, always right after the Write of the
  note and not after the MEMORY.md write; no hook error event.
- Gap: wiring is `loom-workflow/hooks/hooks.json:17` `"matcher": "Write|Edit"`.
  A note written by a shell command gets no reminder (pilot `new-c1-t0`: 0
  reminders). A shell command with a redirect that named the memory folder
  appeared in 10 of the 18 batch sessions (6 new, 4 old) plus the pilot,
  mostly for MEMORY.md or a listing; in the pilot and in old-c2-t1 the note
  itself went through the shell (no Write of a note at all).
- Wiring: `hooks/hooks.json:23-26` only; `hooks/hooks-codex.json` (UserPromptSubmit
  visualization-card only) and `.codex-plugin/plugin.json` (version bump only)
  carry no reminder; `git grep memory-mirror` hits no Codex/OpenCode manifest.

## 4. 在沒有這類 hook 事件的平台（例如 Codex 的檔案編輯），不出現錯誤，行為與現在相同；loom-memory 的 description 仍描述這個觸發時機。
- How I tried it: diffed the Codex-side files between b1b8cd77 and HEAD; read
  the new description and trigger section.
- What came back: `git diff --stat b1b8cd77 HEAD -- loom-workflow/.codex-plugin
  loom-workflow/plugin.json loom-workflow/index.js loom-workflow/opencode
  loom-workflow/hooks.json` = two one-line version bumps. Description: "Record
  repo-wide lessons when saving to your own memory or asked to remember; …";
  SKILL.md trigger 2 "Host memory save … on any agent host".
- Not tried: a live Codex or OpenCode session.

## 5. loom-memory 的規則文字與各 station 的規則文字裡，沒有任何一句話否定這個觸發；沒裝 loom-workflow 時，loom-code 的各站照常運作。
- How I tried it: `grep -rniE "two triggers only|no other condition activates|only two (passive )?triggers|not, by itself, a reason|never (invoke|call|run) loom-memory|do not (invoke|call|use) loom-memory"`
  over loom-code/{skills,agents}, loom-design/skills, loom-workflow/{skills,rules};
  live session with only `--plugin-dir <clean>/loom-code`.
- What came back: one hit, `loom-workflow/skills/loom-memory/SKILL.md:53-54`
  "Apart from the host memory save in trigger 2, reaching any particular point
  in a workflow is not, by itself, a reason to invoke it" (it excludes the trigger
  from the denial). Ship `loom-code/skills/ship/SKILL.md:125-128` routes to
  loom-memory and "When loom-workflow is not installed, this routing is silently
  skipped." `git diff --stat b1b8cd77 HEAD -- loom-code/skills loom-code/agents
  loom-code/scripts loom-code/hooks` is empty. Loom-code-only session: plugins
  `loom-code@inline` + builtins, 7 loom-code skills, no loom-workflow skill,
  `is_error: False`, no hook error, repo unchanged.
- Evidence: `logs/loomcode-alone.jsonl`.

## 6. 在 finalize-review 產生審查證明之後才發現的 repo 教訓，不會在同一個 branch 寫進 `docs/loom/memory/`（#109 的規則照舊），它留在內建記憶裡。
- How I tried it: read the new Record text and hook reminder; ran the criterion tests.
- What came back: SKILL.md Record adds "Such a lesson stays in host memory until
  the next change's branch records it."; hook REMINDER ends "If this branch's
  closing review already generated its attestation (finalize-review ran), do not
  write the repo store now; keep the lesson in host memory for the next change's
  branch."; Ship's memory-timing paragraph is unchanged.
  `evals/record-timing.md` sixth run (by the builder, not me): Exception PASS on both texts.
- Not tried: a live session on a branch whose attestation already exists.
- Known limitation (reported, not fixed): in that run both readers rejected
  candidate 4 (ground truth RECORD) and recorded candidate 2 (ground truth REJECT).

## 7. repo 內原本那支沒接上的 hook 與它的測試已移除，repo 裡沒有檔案再引用它。
- How I tried it: `ls .claude/hooks tests/hooks | grep -i mirror` (nothing);
  `git grep -n "remind-memory-mirror\|remind_memory_mirror"`.
- What came back: files absent. Remaining mentions are records only:
  `loom-code/CHANGELOG.md:1611,1613`, `docs/migration/extraction.json:82-83`,
  `docs/loom/2026-09-27-prose-pin-stock-cleanup/evidence/census-report.md:224`,
  this change's intent/spec/plan, and the guard test
  `loom-workflow/tests/loom-memory/test_memory_mirror_hook.py:107-119` that
  asserts absence. Kept by plan Risk 3 (agent-decided reading).

## 8. 套件測試（package suite）全部通過。
- How I tried it: criterion tests only, in the clean copy:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-workflow/tests/loom-memory/test_memory_mirror_hook.py loom-workflow/tests/loom-memory/test_skill_contract.py loom-workflow/tests/scripts/test_visualization_card_hook.py loom-workflow/tests/scripts/test_release_metadata.py tests/test_tests_folder_convention.py`
  plus `check_contract_citations.py` and `check_mechanisms.py`.
- What came back: `154 passed in 2.59s`; citations "OK"; mechanisms "all clear".
- Full suite: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
  — not run by me; finalize-review runs it and blocks on failure (build reported exit 0 on 5199797f).

## Re-run on 2026-10-24, at aa3e1b22

Fix range c175e64a..aa3e1b22: 30de4b71 (hook matcher `Write|Edit|Bash`,
`hooks.json:26`; Bash commands split into path tokens,
`memory-mirror-reminder:53`) and aa3e1b22 (default store `docs/loom/memory/`
named in SKILL.md, operations.md and the reminder text; test/doc tidy-ups).
Clean copy: `git worktree add --detach <scratchpad>/at/clean2 HEAD`; new plugin
export `<scratchpad>/at/new2` from `git archive HEAD loom-workflow`. Runner
`<scratchpad>/at/trial2.py` = `trial.py` with template `template2` (same
throwaway repo, **no** `docs/loom/memory/`) and an optional heredoc instruction
appended to the prompt: "Write the memory note file with a single Bash command
using a heredoc (cat > <full path of the note> <<'EOF' ... EOF), not with the
Write or Edit tool." Results in `<scratchpad>/at/results2.jsonl`, logs
`logs/r2-*.jsonl`. 10 sessions, USD 2.12, model claude-opus-5-5. Setup check
repeated: init lists only `loom-workflow@inline` 5.15.0 plus builtins.

| Trial | Skill fired | Repo changes | validate | Note written by | Reminder |
|---|---|---|---|---|---|
| natural c1 t1-t3 | 3/3 | `?? docs/loom/memory/{README.md,index.md,<lesson>.md}` 3/3 | exit 0 "valid" 3/3 | Bash `M=<dir>` then `cat > $M/<note>.md` 3/3 | 0/3 |
| heredoc c1 t1 | 1/1 | same, 1/1 | exit 0 1/1 | Bash, path through a shell variable | 0/1 |
| heredoc c3 t1-t2 | 1/2 | none 2/2 | — | Bash `D=<dir>` then `cat > "$D/<note>.md"` 2/2 | 0/2 |
| natural c2 t1-t2 | 1/2 | none 2/2 | — | Write tool 2/2 | 2/2 |
| natural c3 t1-t2 | 1/2 | none 2/2 | — | Write tool 2/2 | 2/2 |

- With `--include-hook-events`, every shell note write shows `hook_response
  PostToolUse:Bash … "stdout": "", "exit_code": 0` — the hook ran and stayed
  silent. Shell note writes through a literal path: 0 of 10 sessions; through
  a variable: 6 of 6 shell-written notes (also the round-1 pilot, `$M`).
- Spec records this as the ceiling: spec.md:26 "a write through an indirect
  path (a variable or a script file) is not seen … the loom-memory
  description remains the fallback." The fallback fired before the write in
  5 of those 6; the sixth (heredoc c3 t2) was a machine-only fact, kept out
  of the repo correctly.

- 1: re-tested — 4 sessions in a repo with no store (3 natural, 1 heredoc):
  store created at `docs/loom/memory/` 4/4 with README.md, index.md and the
  lesson; `loom_memory.py validate docs/loom/memory` exit 0 4/4; host note
  saved 4/4. Still user-requested saves only.
- 2: re-tested — cases 2 and 3, 6 sessions (2 of them heredoc), no store
  present: `git status --porcelain` empty 6/6 (no store folder created);
  host note saved 6/6.
- 3: re-tested — payload drive `python3 -I <scratchpad>/at/hook_probe.py
  <clean2>/loom-workflow/hooks/memory-mirror-reminder`, 37 payloads, `FAILS 0`:
  the 21 earlier ones unchanged, plus Bash heredoc note (unquoted, double-,
  single-quoted path), `echo >>`, `tee`, `mkdir -p && cat >`, `~` path, custom
  `CLAUDE_CONFIG_DIR` → reminder; Bash MEMORY.md, repo store write, unrelated
  command, `ls` of memory dir, command not a string, empty command → silent;
  `M=<dir>; cat > $M/a.md` → silent (ceiling); `cat <note>` → reminder (stated
  side effect). All exit 0, no stderr. Live: Write-tool notes 4/4 reminded;
  shell notes 0/6 (table above). Wiring: `hooks/hooks.json:17` Write|Edit for
  the folder validator, `:26` Write|Edit|Bash for the reminder; Codex and
  OpenCode hook files unchanged.
- 4: carried over — `git diff --stat c175e64a..aa3e1b22 --
  loom-workflow/.codex-plugin loom-workflow/hooks/hooks-codex.json
  loom-workflow/opencode loom-workflow/index.js` is empty and the SKILL.md
  frontmatter description line is unchanged.
- 5: re-tested — same grep at aa3e1b22: one hit, SKILL.md:55-56 (the same
  exempting sentence); using-loom-workflow routing row now adds "or you are
  saving a lesson to your own host memory". Loom-code-only session
  (`logs/r2-loomcode-alone.jsonl`): `loom-code@inline` + builtins, 7 loom-code
  skills, 0 loom-workflow skills, `is_error: False`, no hook error, repo unchanged.
- 6: re-tested — SKILL.md:100 "Such a lesson stays in host memory until the
  next change's branch records it."; reminder text still ends with the
  finalize-review clause (`memory-mirror-reminder:25`); Ship "Memory write
  timing" (ship/SKILL.md:130) unchanged. Not tried live.
- 7: re-tested — `.claude/hooks` / `tests/hooks` contain no mirror file;
  `git grep -l "remind-memory-mirror\|remind_memory_mirror"`: census-report.md,
  this change's evidence file, plan.md, spec.md, intent, docs/migration/extraction.json,
  loom-code/CHANGELOG.md, and the absence-guard test.
- 8: re-tested — same criterion test command in clean2: `152 passed in 2.60s`;
  `check_contract_citations.py` "OK"; `check_mechanisms.py` "all clear".
  Full suite left to finalize-review (build reported exit 0 on aa3e1b22).

## Re-run on 2026-10-24, at e3dd1645

Fix range eaf08848..e3dd1645 (one commit): the hook's Bash branch no longer
parses the command; it derives `<config>/projects` from `transcript_path`
and reminds when a non-MEMORY.md `*.md` directly inside any
`<config>/projects/*/memory/` was modified in the last 10 s
(`memory-mirror-reminder` `WINDOW = 10`, `recent_note_exists`). Write/Edit
unchanged. Files changed: the hook, its test, spec.md, loom-workflow/CHANGELOG.md.
Clean copy `git worktree add --detach <scratchpad>/at/clean3 HEAD`; plugin
export `<scratchpad>/at/new3`.

### Payload drive
`python3 -I <scratchpad>/at/hook_probe3.py <clean3>/loom-workflow/hooks/memory-mirror-reminder <scratchpad>/at`
— 32 payloads, `FAILS 0`, all exit 0, no stderr. Bash cases use a fake
`<tmp>/home/.claude/projects/<slug>/memory/` tree with set mtimes:
- reminder: own-slug note 1 s and 9 s old; another slug's note 1 s old
  (concurrent session, stated side effect); Bash payload with no `tool_input`;
  scan still succeeds when another slug's memory folder is unreadable (chmod 0).
- silent: note 11 s old; only MEMORY.md fresh; fresh `.json` in memory;
  fresh note in `memory/sub/`; fresh `.md` outside `memory/`; read-only `cat`
  of a 1-hour-old note; no `transcript_path`; `transcript_path` null;
  transcript outside a config dir; transcript slug dir missing.
- Write/Edit and malformed-input cases from earlier rounds: unchanged results.
- Latency on the real `~/.claude/projects` (206 slugs; stat only): 0.01–0.02 s
  real time over 5 runs, no reminder.

### Live, real memory layout
Runner `<scratchpad>/at/trial3.py`: same throwaway repo (`template2`, no
store), no `autoMemoryDirectory` override (`--settings '{"autoMemoryEnabled":true}'`),
so host memory is `~/.claude/projects/<slug>/memory/`. The slug is the
repo's real path with non-alphanumerics replaced by `-`; the runner refuses
to start if that directory already exists. Trials run one at a time so one
trial's write cannot remind another. 7 sessions, USD 1.17, model claude-opus-5-5.
Results `<scratchpad>/at/results3.jsonl`, logs `logs/r3-*.jsonl`.

| Trial | Prompt | Event order | Reminders | Repo changes |
|---|---|---|---|---|
| shellvar c3 t1 | note via one Bash command, folder in a shell variable, `cat > "$VAR/<name>.md"` | Bash(host) > Bash(host) > REMINDER<PostToolUse:Bash> | 1 | none |
| shellvar c3 t2 | same | Bash(host) > Bash(host) > REMINDER<PostToolUse:Bash> | 1 | none |
| shellvar c1 t1 | same, repo-wide lesson | SKILL > Bash(host `MEM=…`) > Bash(host) > REMINDER > Bash(`ls scripts tests plugin-a`) > REMINDER > Bash(host) > REMINDER > Bash(repo) | 3 | `?? docs/loom/memory/{README.md,index.md,test-roots-must-be-registered.md}`; `validate docs/loom/memory` "OK" |
| write c2 t1 | note via Write tool | Bash(host) > Write(note) > REMINDER<PostToolUse:Write> > Write(MEMORY.md) | 1 | none |
| write c2 t2 | same | Write(note) > Bash(host) > REMINDER<PostToolUse:Write> > Write(MEMORY.md) | 1 | none |
| readonly c2 t1 | pre-seeded note + MEMORY.md, mtime set 1 h back; "show the note with one read-only `cat`" | Bash(host) | 0 | none |
| readonly c2 t2 | same | Bash(host) | 0 | none |

- Repeat reminders: in shellvar c1 t1 one note produced 3 reminders, the
  2nd after an unrelated `ls` that ran inside the 10 s window, the 3rd after
  a MEMORY.md update. Nothing failed; the agent recorded the lesson once.
- write c2 t2: a Bash call within the window after the Write gave no second
  reminder in the stream (1 total).

### Cleanup of trial-created folders — BLOCKED, pending the user
Each trial created exactly one directory under `~/.claude/projects/`, holding
one `<uuid>.jsonl` session transcript and a `memory/` folder of throwaway
notes. Deleting them was blocked by the shell guard:
`BLOCKED by dcg … Rule: heredoc.python:shutil_rmtree … To permit this single
command once, the user can approve it with: dcg allow-once 913948`. I did not
retry by another route. The 7 directories still to delete:

- `~/.claude/projects/-private-tmp-claude-501--Users-kouko-GitHub-loom-plugins--claude-worktrees-memory-trigger-e65ab225-2760-441a-9215-379dd5acb7e5-scratchpad-at-trials3-r3-shellvar-c3-t1-repo`
- `~/.claude/projects/-private-tmp-claude-501--Users-kouko-GitHub-loom-plugins--claude-worktrees-memory-trigger-e65ab225-2760-441a-9215-379dd5acb7e5-scratchpad-at-trials3-r3-shellvar-c3-t2-repo`
- `~/.claude/projects/-private-tmp-claude-501--Users-kouko-GitHub-loom-plugins--claude-worktrees-memory-trigger-e65ab225-2760-441a-9215-379dd5acb7e5-scratchpad-at-trials3-r3-shellvar-c1-t1-repo`
- `~/.claude/projects/-private-tmp-claude-501--Users-kouko-GitHub-loom-plugins--claude-worktrees-memory-trigger-e65ab225-2760-441a-9215-379dd5acb7e5-scratchpad-at-trials3-r3-write-c2-t1-repo`
- `~/.claude/projects/-private-tmp-claude-501--Users-kouko-GitHub-loom-plugins--claude-worktrees-memory-trigger-e65ab225-2760-441a-9215-379dd5acb7e5-scratchpad-at-trials3-r3-write-c2-t2-repo`
- `~/.claude/projects/-private-tmp-claude-501--Users-kouko-GitHub-loom-plugins--claude-worktrees-memory-trigger-e65ab225-2760-441a-9215-379dd5acb7e5-scratchpad-at-trials3-r3-readonly-c2-t1-repo`
- `~/.claude/projects/-private-tmp-claude-501--Users-kouko-GitHub-loom-plugins--claude-worktrees-memory-trigger-e65ab225-2760-441a-9215-379dd5acb7e5-scratchpad-at-trials3-r3-readonly-c2-t2-repo`

No other project's memory folder was written. The session-transcript
folders from rounds 1 and 2 (`…-scratchpad-at-trials-*-repo`, 20 transcripts,
no `memory/`) also remain.

### Rows
- 1: re-tested — shellvar c1 t1 in a repo with no store, real memory
  layout: store created at `docs/loom/memory/`, `validate` "OK", host note
  saved. Together with round 2: 5/5.
- 2: re-tested — shellvar c3 ×2, write c2 ×2, readonly c2 ×2: `git status
  --porcelain` empty 6/6.
- 3: re-tested — payload drive and live table above: shell-variable writes
  3/3 reminded, Write-tool writes 2/2, read-only `cat` 0/2; malformed input
  silent, exit 0.
- 4: carried over — `git diff --stat eaf08848..e3dd1645` over the Codex and
  OpenCode manifests and hook files, `hooks.json` and `loom-workflow/skills`
  is empty.
- 5: carried over — the same diff over `loom-workflow/skills`,
  `loom-workflow/rules`, `loom-code` and `loom-design` is empty.
- 6: carried over — rule text unchanged (same diff) and the `REMINDER`
  string is untouched in the hook diff.
- 7: carried over — no file added or removed; `git diff eaf08848..e3dd1645 |
  grep -c "remind-memory-mirror\|remind_memory_mirror"` = 0.
- 8: re-tested — criterion test command in clean3: `158 passed in 2.17s`;
  `check_mechanisms.py` "all clear"; `check_contract_citations.py` "OK".
  Full suite left to finalize-review (build reported exit 0 on e3dd1645).
