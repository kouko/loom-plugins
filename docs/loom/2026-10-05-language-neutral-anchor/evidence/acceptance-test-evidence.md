# The language reminder no longer judges the user's language — acceptance test evidence

Tried on 2026-10-05, in a clean copy of the project at 1b5a7bcc; re-run
after the fix round at d48fa7ea (last section)
(`git worktree add <scratch>/at-clean 1b5a7bcc`; branch base 8f082f0e,
also checked out clean as `<scratch>/at-base` for before/after contrast).
`<scratch>` = `/Users/kouko/.claude/jobs/b66b8c5a/tmp`; nothing under it is
committed. Claude Code 2.1.289. Direct hook runs used
`/opt/homebrew/bin/python3`. Criterion tests ran in an ephemeral env:
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --no-project --python
/opt/homebrew/bin/python3 --with pytest --with pyyaml python -m pytest -q
-p no:cacheprovider <files>` (Homebrew python has no pytest; nothing was
installed into any shared env).

## Setup
- How I tried it: README "Install → Claude Code" names `claude plugin
  install loom-code@loom`. To leave the user's installed plugins
  untouched, live sessions loaded the clean copy per session with
  `claude -p --plugin-dir <scratch>/at-clean/loom-code --settings
  <scratch>/live/disable-installed-loom-code.json` (the settings file holds
  only `{"enabledPlugins":{"loom-code@loom":false}}`, so the installed
  loom-code 3.30.0, whose hook still carries the old zh/ja detector, cannot
  also fire). `claude plugin validate` on all three plugin directories.
- What came back: loom-code `✔ Validation passed`; loom-design and
  loom-workflow `✔ Validation passed with warnings` (loom-workflow's
  warning is an unquoted `${CLAUDE_PLUGIN_ROOT}` in its own
  `validate-skill-folder-structure.sh` hook — a file this change does not
  touch). Every live session's `system/init` lists
  `loom-code … source: loom-code@inline, version: 3.32.0`, so the clean
  copy's hooks were the ones running.
- Not run live: OpenCode and Antigravity. On this machine both `opencode`
  and `agy` are shell functions that first run an installer/updater for
  installed plugins (`launch-litellm.sh`, `install-antigravity-plugins.sh`),
  which the constraints forbid touching. Both hosts were driven directly
  instead (row 4).

## 1. 中文夾大量英文術語的對話，在每個既有觸發時機都會收到語言提醒。
- How I tried it (direct): synthetic 3-turn transcript `zh_terms.jsonl`
  whose turns are shaped like the miss the intent describes, e.g.
  「PostToolUse hook 跟 SessionStart matcher 的 additionalContext
  description 差別是？」. Piped every existing trigger into
  `at-clean/loom-code/hooks/language-anchor.py` and into the base copy's
  hook: SessionStart compact, SessionStart resume, PostToolUse Skill,
  PostToolUse Agent, UserPromptSubmit.
- What came back:

  | Trigger | HEAD | base 8f082f0e |
  |---|---|---|
  | SessionStart compact | anchor (`hookEventName: SessionStart`) | silent |
  | SessionStart resume | anchor | — (same detector path) |
  | PostToolUse Skill / Agent | anchor (`PostToolUse`) | — |
  | UserPromptSubmit | anchor (`UserPromptSubmit`) | — |

  The `additionalContext` is the identical string on every trigger (stdout
  sha prefixes differ only by `hookEventName`: 4fdcc45fa0 SessionStart,
  b70fc4a4d6 PostToolUse, b83106efa3 UserPromptSubmit — the same three
  hashes for every transcript in row 2).
- Live: session 979662cc (`<scratch>/live/zhTW_terms-default`), zh-TW
  prompt dense with English terms (Agent tool, background subagent,
  run_in_background, subagent_type, general-purpose, task notification,
  summarize, internal API service). Session transcript lines 19
  (UserPromptSubmit), 37 (PostToolUse:Agent), 49 (UserPromptSubmit on the
  completion turn) each carry the new anchor in
  `hook_additional_context`. Same prompt against the base copy (session
  cf5c3a9f, `zhTW_terms-base`): no language anchor in any of its five
  `hook_additional_context` entries (only the user's delegation hook, the
  ascii-graph card and the loom-workflow visualization card).
- Evidence: commands above; `test_language_anchor_hook.py`,
  `test_adversarial_language_anchor_compact_summary.py` (in the 221-pass
  run under row 6).

## 2. 任何語言的對話（含英文、韓文、法文）都會收到同一句提醒；提醒不指定、也不偏向任何一種語言或字體。
- How I tried it: same five triggers over transcripts in English, Korean,
  French, Russian, Japanese and zh-with-terms, plus no transcript at all
  (`transcript_path` pointing at a missing file). Read the emitted text.
- What came back: 35 runs (7 transcripts × 5 triggers), every one emitted;
  the stdout hash per trigger is identical across all 7, i.e. the text does
  not depend on the conversation. Base on the same compact trigger: en, ko,
  fr, ru, zh-terms silent; only ja emitted (its Japanese text). The text at
  HEAD (`language-anchor.py:18-22`, `ANCHOR_TEXT`):
  "Write every message to the user in the language and script the user
  writes in during this conversation; machine-facing artifacts
  (brief/verdict/commit) keep their own language." It names no language
  and no script. It is written in English, which the intent's Constraints
  record as the user's own decision.
- Negatives: PostToolUse Bash, Stop, `not json`, `[1]` → no output, exit 0.
- Evidence: commands above; live English pull is in row 3 (five sessions
  whose subagent answered in English).

## 3. 實際用繁體中文、簡體中文、日文、韓文各開一段對話，在背景 agent 做完的那一輪，回覆維持該對話的語言與字體。
- How I tried it: 14 live print-mode sessions (`claude -p --output-format
  stream-json --verbose`), cwd `<scratch>/live/<name>-<model>[-iso]`. Each
  prompt, written in the conversation's language, asks for a background
  Agent (`run_in_background: true`) that answers without tools, then asks
  for a summary and a recommendation after the completion notification.
  Three configurations: `default` (claude-opus-5-5, user's real setup with
  installed loom-design/loom-workflow), `haiku` (claude-haiku-4-5-20251001),
  `iso` (default model, installed loom-design and loom-workflow also
  disabled, so loom-workflow's visualization card — which itself says
  "Reply to the user in their language" — is absent). For each session the
  analyser (`<scratch>/live/analyze.py`) found the user-role
  `<task-notification>` line, the anchor entries in the session
  transcript, and the first assistant text after the notification, and
  counted characters by script (a 40-pair traditional/simplified list,
  kana, hangul, Han, Latin; inline code stripped).
- What came back:

  | Session | Lang | Config | Subagent answered in | Anchor on completion turn (line, event) | Reply script counts |
  |---|---|---|---|---|---|
  | 979662cc | zh-TW + terms | default | English | 49 UserPromptSubmit | trad 44 / simp 0 |
  | 33b51082 | zh-TW + terms | haiku | zh-TW | 51 UserPromptSubmit | trad 25 / simp 0 |
  | 2e8a7d22 | zh-TW + terms | iso | English | 50 UserPromptSubmit | trad 40 / simp 0 |
  | 7f31d3ed | zh-TW | default | zh-TW | 51 UserPromptSubmit | trad 64 / simp 0 |
  | 0923b53b | zh-TW | haiku | zh-TW | 51 UserPromptSubmit | trad 26 / simp 0 |
  | 35a54c51 | zh-CN | default | zh-CN | 50 UserPromptSubmit | trad 0 / simp 46 |
  | 8a7c8bff | zh-CN | haiku | zh-CN | 50 UserPromptSubmit | trad 0 / simp 28 |
  | c7712a44 | zh-CN | iso | zh-CN | 48 UserPromptSubmit | trad 0 / simp 60 |
  | 7a04582b | ja | default | ja | 50 UserPromptSubmit | kana 478, hangul 0 |
  | 3d1e43a3 | ja | haiku | ja | 51 UserPromptSubmit | kana 242, hangul 0 |
  | 7cd1ea52 | ja | iso | English | 48 UserPromptSubmit | kana 544, hangul 0 |
  | 58b9aa2b | ko | default | English | 50 UserPromptSubmit | hangul 604, kana 0, Han 0 |
  | e91e2a9b | ko | haiku | ko | 51 UserPromptSubmit | hangul 360, Han 0 |
  | 25f4099e | ko | iso | English | 48 UserPromptSubmit | hangul 734, Han 0 |

  Every session: the anchor also appeared at the first UserPromptSubmit
  (line 18/19) and at PostToolUse:Agent (line 36/37); old zh/ja anchor
  text 0 times; `hook_error`/`non_blocking_error` entries 0. The
  traditional/simplified pair counts are not meaningful for Japanese
  (shinjitai shares forms with both); kana dominance identifies the ja
  replies. Reply openings, e.g. 979662cc line 52 「**結論：做 internal API
  service，建議優先選 FastAPI；…」, 35a54c51 line 53 「**结论：读多写少的场景，
  默认选 B-Tree 索引。**」, 58b9aa2b line 53 「**주문 처리 시스템이라면
  RabbitMQ를 추천합니다.**」.
- Counts per language: zh-TW 5 (3 of them dense with English terms),
  zh-CN 3, ja 3, ko 3. 14 of 14 kept language and script.
- Limits: print mode only; interactive-mode background completion not
  tried. The user's global CLAUDE.md (match the message language) is loaded
  in every session, `iso` included, so no trial isolates the anchor as the
  sole cause; the trials show the outcome in the user's real setup and that
  the anchor reached the model on that turn. One trial per cell cannot show
  a reply never drifts (plan Risk 3).

## 4. 目前顯示語言提醒的每個工具（Claude Code、Antigravity、OpenCode）都改送同一句提醒。
- Claude Code: rows 1-3 (hook output and live transcripts).
- Antigravity: drove `at-clean/loom-code/hooks/agy_adapter.py
  pre-invocation` directly (`TMPDIR=<scratch>/agy`) with agy-shaped
  transcripts (a USER_INPUT `<USER_REQUEST>` step in zh-with-terms, en, ko
  or fr, then a MODEL `view_file` of `…/loom-code/skills/build/SKILL.md`).
  Invocation 1 injected one `ephemeralMessage`; for ko and fr it was
  compared with `language-anchor.py`'s `ANCHOR_TEXT` → `True`; invocation 2
  on the same read → no anchor (once-per-skill-read gate kept). The base
  copy's adapter on the same en, ko and zh-with-terms transcripts printed
  `{}` (no anchor) each time
  (`git diff 8f082f0e..HEAD -- loom-code/hooks/agy_adapter.py`: the
  detector block is replaced by `…LANGUAGE_ANCHOR).ANCHOR_TEXT`).
- OpenCode: `hooks-opencode.json` runs the same `language-anchor.py` on
  PostToolUse Skill. The loader (all four copies byte-identical:
  `shasum scripts/opencode/loader.js loom-*/opencode/loader.js` → 1 unique
  hash) was exercised by `test_opencode_loader.py`, which runs it under
  node: `language-anchor` case finds "in the language and script the user
  writes in" in the skill result; `test_prompt_file_never_written` passed.
- Codex: wires no anchor (`hooks-codex.json` has no `language-anchor`),
  out of scope per the intent.
- Evidence: `test_agy_adapter.py`, `test_adversarial_agy_anchor_turns.py`,
  `test_adversarial_agy_adapter.py`, `test_opencode_loader.py` in the
  221-pass run.

## 5. 既有的語言分工與各站說明不變。
- How I tried it: `git diff 8f082f0e..HEAD --name-only | grep -E
  "skills/|agents/|SKILL|references/"` → empty: no station, agent or
  reference text changed. Compared the reminder's division clause: base zh
  「機器面 artifact（brief/verdict/commit）維持原語言」 vs HEAD
  "machine-facing artifacts (brief/verdict/commit) keep their own
  language" — same three artifact kinds, same rule.
- Evidence: commands above; `test_language_anchor_hook.py` (machine-artifact
  clause case) passed.

## 6. 完整 package suite 全部通過，版號一致。
- How I tried it: per the role rules I did not run the full package suite;
  `finalize-review` runs it and refuses the attestation on failure. The
  suite command is `python3 scripts/run_package_tests.py --loom-family`.
  I ran the criterion's own tests and checks:
  - loom-code: `test_language_anchor_hook.py
    test_adversarial_language_anchor_compact_summary.py
    test_opencode_loader.py test_agy_adapter.py
    test_adversarial_agy_anchor_turns.py test_adversarial_agy_adapter.py
    test_hooks_json.py test_check_mechanisms.py
    test_write_plan_station_text.py` → `221 passed in 12.88s`.
  - loom-design `tests/spec/test_capture_intent_contract.py` → `18 passed`.
  - loom-workflow `tests/scripts/test_release_metadata.py` → `9 passed`.
  - `scripts/sync_codex_manifests.py --check --all` → exit 0.
  - Versions read from all four manifests per plugin (`plugin.json`,
    `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`,
    `package.json`): loom-code 3.32.0 ×4, loom-design 2.12.1 ×4,
    loom-workflow 5.6.3 ×4; root README table and each loom-code README
    show 3.32.0; `loom-code/CHANGELOG.md` top section `## [3.32.0] —
    2026-10-05`.
  - `git grep -n lang_detect -- ':!docs' ':!*CHANGELOG*'` → no hits.
- Evidence: outputs above.

## Data the user already had
- First run (1b5a7bcc): the OpenCode loader at base appended each user
  prompt to `<tmpdir>/loom-opencode/<session>.jsonl`; 1b5a7bcc no longer
  wrote it and did not delete existing files. On this machine
  `/var/folders/…/T/loom-opencode` holds 2 files (2,401 + 100 bytes;
  8 KB on disk).
- Re-run (d48fa7ea): the loader now removes `<tmpdir>/loom-opencode`
  (recursive, force, errors swallowed) every time any of the three
  plugins' OpenCode entry loads; a symlink there is unlinked, its target
  kept (re-run row 4). The user chose this on 2026-10-05 (「暫存檔一起清」,
  plan Questions asked ③). No backup is made; nothing reads these files.
  The user's real folder was never given to the loader during testing:
  before and after every run it still lists
  `ses_f0a837e6dffeTx1sWrCRca7fSC.jsonl` and
  `ses_f0a8554b9ffewhVulvYhw6bqjn.jsonl`; they go when the user's own
  OpenCode first loads the new version.
- Antigravity's per-conversation state files under the temp dir keep the
  same format and name (`loom-code-agy-anchor-<uid>/…`).

## Re-run on 2026-10-05, at d48fa7ea

Fix range 38d1d26c..d48fa7ea: `plan.md` (W1-05, two ③ answers), the four
byte-identical `opencode/loader.js` copies (+`rmSync(join(tmpdir(),
"loom-opencode"), {recursive, force})` in `setup`, wrapped in try/catch),
three CHANGELOGs, `test_opencode_loader.py` (+2 tests, autouse TMPDIR
fixture), `test_adversarial_agy_adapter.py` (one assertion tightened). No
hook script, hook wiring, station/agent/reference text or manifest changed
(`git diff --name-only 38d1d26c..d48fa7ea`).

Clean copy: `git worktree add <scratch>/at-rerun d48fa7ea`. Scratch
scripts live in `<scratch>/rerun/` (not committed). All four loader copies
hash `5a7a663a…` (`shasum`).

- Setup: re-tested — `claude plugin validate` in the clean copy: loom-code
  `✔ Validation passed`; loom-design, loom-workflow `✔ Validation passed
  with warnings` (same warning as the first run).
- 1: carried over — the fix changes only the OpenCode loader; the Claude
  Code hook (`language-anchor.py`), its triggers (`hooks.json`) and its
  text are byte-unchanged, so the first run's direct and live results
  stand. (The row-2 re-run below incidentally pushed the zh-with-terms
  transcript through all five triggers again: anchor every time.)
- 2: re-tested — `rerun/hosts/row2.py`: the 7 transcripts (en, fr, ja, ko,
  ru, zh_terms, missing file) × 5 triggers (SessionStart compact, resume;
  PostToolUse Skill, Agent; UserPromptSubmit) into the clean copy's hook:
  `runs=35 distinct_texts=1`; the one text is the `ANCHOR_TEXT` quoted in
  row 2 above — no language or script named. English wording confirmed by
  the user on 2026-10-05 (「英文提醒可以」, plan Questions asked ③), in
  addition to the intent's Constraints.
- 3: carried over — the live trials ran in Claude Code, whose hook,
  wiring and text the fix does not touch; nothing in the fix range runs
  in a Claude Code session.
- 4: re-tested on all three hosts.
  - Claude Code: `rerun/hosts/drive_hosts.py` sent zh_terms, en, ko, fr
    through UserPromptSubmit, PostToolUse Agent and SessionStart compact
    → `additionalContext == ANCHOR_TEXT` in all 12.
  - Antigravity: same script, `agy_adapter.py pre-invocation` with a
    USER_INPUT step then a `view_file` of a loom-code SKILL.md, TMPDIR in
    scratch → invocation 1 injects exactly one `ephemeralMessage` equal to
    `ANCHOR_TEXT`, invocation 2 none, for all four languages.
  - OpenCode: `rerun/run_loader.py` loads each plugin's `index.js` under
    node with a stub ctx (`rerun/harness.mjs`, same shape as
    `test_opencode_loader.py`), TMPDIR set to a fresh scratch folder and
    asserted (`os.tmpdir()` checked to start with the scratch path before
    each run):

    | Case | Plugin | Result |
    |---|---|---|
    | leftover `loom-opencode/ses_fake.jsonl` | loom-code | exit 0, 6 skills, Skill result carries the anchor, folder gone |
    | leftover | loom-design | exit 0, 6 skills, folder gone |
    | leftover | loom-workflow | exit 0, 12 skills, folder gone |
    | folder absent | loom-code | exit 0, anchor appended, temp folder still empty |
    | `loom-opencode` → symlink to `elsewhere/` | loom-code | exit 0, link gone, `elsewhere/keep.jsonl` still `keep me\n` |
    | folder present but mode 555 (unremovable) | loom-code | exit 0, anchor appended, file left in place, no stderr |

    Real `$TMPDIR/loom-opencode` before and after: the same 2 files.
  - Named tests: `test_load_removes_prompt_files_left_by_earlier_versions`,
    `test_load_removes_a_linked_prompt_folder_not_its_target`,
    `test_anchor_nonstring_user_content_anchors_not_crash` in the 223-pass
    run under row 6.
- 5: carried over — no station, agent or reference file in the fix range;
  the reminder's machine-artifact clause is unchanged (row 2 text above).
- 6: re-tested — same criterion files as the first run, in the clean copy
  with `TMPDIR=<scratch>/rerun/pytest-tmp/`: loom-code → `223 passed in
  13.62s` (221 + the 2 new loader tests); loom-design
  `test_capture_intent_contract.py` + loom-workflow
  `test_release_metadata.py` → `27 passed`; `sync_codex_manifests.py
  --check --all` → exit 0. Versions: loom-code 3.32.0 ×4, loom-design
  2.12.1 ×4, loom-workflow 5.6.3 ×4 (no bump in the fix range; the new
  CHANGELOG bullets sit under those unreleased sections). Full suite not
  run by me: `python3 scripts/run_package_tests.py --loom-family`, run by
  `finalize-review`, which refuses the attestation on failure.
- Guard note: two command shapes were refused by the shell guard (`rm -rf`
  on a variable path; redirect to a variable path); fixtures were then
  built inside `run_loader.py` with fresh `mkdtemp` folders instead.
