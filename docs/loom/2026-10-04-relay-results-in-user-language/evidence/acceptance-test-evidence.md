# loom relays results in the user's conversation language — acceptance test evidence

Tried on 2026-10-04, in a clean copy of the project at a5d7235b
(`git worktree add .git/loom-scratch/at-relay a5d7235b`; base 26ff838e).
Claude Code 2.1.289. Interpreter for direct hook runs: bare `python3`, as
the installed hook command uses it. Scratch transcripts lived under
`.git/loom-scratch/at-tx/` and `/tmp/at-relay/`; nothing from them is
committed. A re-run after the fix (da74a343..22042c50) is the last
section of this file.

## Setup
- How I tried it: README "Install" section names `claude plugin install
  loom-code@loom`. To leave the user's installed plugins untouched I loaded
  the clean copy per session with `claude -p --plugin-dir
  <clean copy>/loom-code` instead, and ran `claude plugin validate
  <clean copy>/loom-code` plus `json.load` on `loom-code/hooks/hooks.json`.
- What came back: `✔ Validation passed`; `hooks.json parses`. All three
  live sessions below loaded the clean copy's hooks (the reminder text in
  their transcripts is the new wording, which no installed version carries).
- Evidence: commands above; live transcripts cited under rows 3 and 4.

## 1. build 與 closing-review 說明：把 agent 的結果轉述給使用者時用使用者對話使用的語言，包括沒有使用者新訊息、由背景 agent 完成或對話接續開始的那一輪。
- How I tried it: read the diff and the station text at HEAD; ran the
  criterion's own test.
- What came back:
  - `loom-code/skills/build/SKILL.md:91-94`: "Every message to the user,
    including a relayed implementer, adversary or reviewer result, is
    written in the user's conversation language, even on a turn with no new
    user message, such as a background agent's completion or a resume after
    compaction."
  - `loom-code/skills/closing-review/SKILL.md:11-14`: the same sentence
    naming reviewer and acceptance-tester results.
  - `test_simplified_station_text.py::test_build_and_review_relay_results_in_the_users_language`
    passed (part of the 129-pass run under row 6).
- Evidence: file:line above. Not tried live: whether a model actually obeys
  the prose on a background-completion turn (prose cannot be proven by one
  trial; plan Risk 2 says the same).

## 2. ship 說明：PR body 以及給使用者的每則訊息（含決策點 ③ 的結果與驗收問題）用使用者對話使用的語言。
- How I tried it: read the diff and `loom-code/skills/ship/SKILL.md` at HEAD.
- What came back: `ship/SKILL.md:12-17`: "Write the PR body and every
  message to the user, including the decision point ③ result and acceptance
  question, in the user's conversation language when the host can establish
  it from the confirmed intent or active conversation. Repository
  conventions still govern committed artifacts. Internal publication reports
  remain English."
  `test_ship_language_sentence_covers_every_user_message` passed.
- Evidence: file:line above.

## 3. 自動語言提醒除了載入 skill 之後，也在對話壓縮後接續時、以及 subagent 結果回來時出現；Claude Code 沒有可用觸發時機的情況，acceptance test report 寫明哪些時機沒有涵蓋。
- How I tried it (direct hook runs): piped payloads into
  `python3 loom-code/hooks/language-anchor.py` against synthetic transcripts
  (3 user turns each) in Traditional Chinese, Simplified Chinese, Japanese,
  English, Korean.
- What came back (direct):

  | Payload | Transcript | Output |
  |---|---|---|
  | SessionStart compact | zh-TW, zh-CN, ja | anchor emitted, `hookEventName: SessionStart` |
  | SessionStart compact | en, ko | silent, exit 0 |
  | SessionStart compact | zh-TW + 3 English compaction summaries flagged `isCompactSummary: true` | zh anchor |
  | SessionStart compact | same summaries without the flag (text prefix only) | zh anchor |
  | SessionStart compact | zh-TW + 3 `isMeta` re-invocation echoes | zh anchor |
  | SessionStart compact | zh-CN + 3 flagged summaries | zh anchor |
  | SessionStart resume | zh-TW | zh anchor |
  | PostToolUse Skill / Agent | zh-TW | zh anchor, `hookEventName: PostToolUse` |
  | PostToolUse Bash / Task | zh-TW | silent |
  | no `hook_event_name`, tool Agent | zh-TW | zh anchor (defaults to PostToolUse) |
  | Stop / SubagentStop event | zh-TW | silent |
  | `hook_event_name` is a list; malformed JSON; missing transcript | — | silent, exit 0 |

- How I tried it (live, Claude Code 2.1.289, `claude -p --model haiku
  --plugin-dir <clean copy>/loom-code`, cwd under `/tmp/at-relay/`):
  1. Chinese prompt asking for a foreground `Agent` call
     (session dab76457). Transcript line 34-35: `hook_success
     PostToolUse:Agent` then `hook_additional_context` carrying the zh
     anchor, right after the Agent tool_result.
  2. `--resume dab76457` with a Chinese follow-up. Lines 49-51:
     `SessionStart:resume` hooks and the zh anchor in additionalContext.
  3. `--resume dab76457 "/compact"`. Line 69 `isCompactSummary: true`
     (the English summary), line 80 `hook_success SessionStart:compact`
     whose stdout is the zh anchor, line 81 `hook_additional_context`
     with three entries, entry 2 = the zh anchor. So the reminder reached
     the model after compaction even though the newest user-role entry is
     the English summary.
  4. Chinese prompt asking for a background Agent (`run_in_background:
     true`, session 8d705164). Line 32 Agent tool_use at 14:49:52.506Z;
     line 34-35 `PostToolUse:Agent` + zh anchor at 14:49:52.556Z (at
     launch); the completion arrived at 14:50:00.382Z as a user-role
     `<task-notification>` turn (line 46). No PostToolUse/SessionStart
     anchor accompanies that turn. **But `UserPromptSubmit` hooks did fire
     on it** (lines 47-48: the user's own delegation hook and the
     loom-workflow visualization card were injected at 14:50:00.392Z /
     .403Z). So in this Claude Code version (print mode) a trigger exists
     on the background-completion turn; the change does not use it.
     Interactive-mode behaviour on that turn was not tried.
- Real transcripts (read-only): the 51 transcripts under
  `~/.claude/projects/` that contain `"isCompactSummary":true`, voted with
  the base detector (`git show 26ff838e:loom-code/hooks/lang_detect.py`)
  and the HEAD detector over the whole file:

  | base → HEAD | count |
  |---|---|
  | zh → zh | 26 |
  | en → en | 7 |
  | en → zh | 15 |
  | en → None | 2 |
  | None → zh | 1 |

  Against a reference vote over all of each file's genuine user turns:
  4 transcripts whose turns are mostly Chinese still resolve to `en` at
  HEAD, so no reminder would be given. In all 4 the last three detectable
  turns are Chinese questions carrying several English technical terms
  (shape: 「X 跟 Y description 的差別是？」 with X, Y English identifiers);
  `detect_script` counts every ASCII letter against every Han character, so
  Han falls under 50% and the turn votes `en`. Reproduced on a synthetic
  three-turn file of that shape: SessionStart compact → silent. One
  transcript went zh at HEAD where the reference said en (recent turns
  Chinese, older English) — correct for a last-three-turns vote.
  This detector rule predates the change (`lang_detect.py` threshold
  `_MAJORITY_SCRIPT_RATIO`, unchanged in the diff).
- Not covered, and why:
  - background agent completion turn: PostToolUse(Agent) fires at launch,
    not at completion (live trial 4); no SessionStart/PostToolUse fires on
    the completion turn; `SubagentStop` was not wired (plan W1-02 Risk);
    UserPromptSubmit does fire there in print mode (see above) but is not
    wired.
  - Codex and OpenCode hosts: their hook files were not rewired (plan Risk
    3); not tried.
  - English, Korean or any language other than zh/ja: no reminder by
    design.
- Evidence: commands above; criterion tests
  `test_language_anchor_hook.py`, `test_hooks_json.py`,
  `test_lang_detect.py`, `test_adversarial_language_anchor_compact_summary.py`
  passed (row 6 run).

## 4. 自動語言提醒要求的是使用者對話使用的語言，不寫死任何一種語言；用簡體中文對話時，提醒不會要求改用繁體中文。
- How I tried it: read `_ANCHOR_TEXT` at HEAD; direct hook runs on zh-CN;
  live Simplified-Chinese session.
- What came back:
  - zh text now: 「對使用者的敘述一律使用使用者在對話中所用的語言與文字；機器面
    artifact（brief/verdict/commit）維持原語言。」 — no 繁體中文 (the base text
    was 「會話語言（繁體中文）」). ja text names 日本語 only as the detected
    language: 「ユーザーの会話言語（日本語）」. The text is chosen by the
    detected language; there is no default language.
  - Live (session in `/tmp/at-relay/live3`): Simplified-Chinese prompt,
    foreground Agent; transcript has 2 `PostToolUse:Agent` hook entries and
    the zh anchor; final reply was in Simplified Chinese
    (「前台子代理已派出并成功返回「完成」…」).
  - The zh reminder itself is written in Traditional characters; it asks
    for the user's own script and did not pull the reply into Traditional.
- Evidence: `loom-code/hooks/language-anchor.py:27-36`; live transcript
  above; `test_language_anchor_hook.py` passed.

## 5. 既有的語言分工不變：plan、spec、verdict、evidence、commit 仍是英文；acceptance test report 與 PR body 仍用使用者的語言。
- How I tried it: grep of the English-artifact sentences at HEAD and diff
  of untouched files.
- What came back: `build/SKILL.md:90` "Internal plans, commits, and
  verification evidence are written in English." and
  `closing-review/SKILL.md:10` "Reviewer findings and generated evidence
  are written in English." are unchanged lines; ship keeps "Repository
  conventions still govern committed artifacts. Internal publication
  reports remain English."; PR body still in the user's language
  (ship:12). `git diff 26ff838e...HEAD -- loom-code/skills/write-plan
  loom-code/agents contract` is empty, so the acceptance-tester's
  user-language report rule and write-plan's English plan rule are
  untouched. `test_english_artifact_sentences_unchanged` passed.
- Evidence: file:line above.

## 6. 完整 package suite 全部通過，版號一致。
- How I tried it: ran only the criterion's own tests and the manifest check
  (the full suite is `finalize-review`'s job and was not run here).
  - `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --no-project
    --python /opt/homebrew/bin/python3 --with pytest --with pyyaml python -m
    pytest loom-code/tests/test_simplified_station_text.py
    loom-code/tests/test_language_anchor_hook.py
    loom-code/tests/test_hooks_json.py loom-code/tests/test_lang_detect.py
    loom-code/tests/test_adversarial_language_anchor_compact_summary.py
    loom-code/tests/test_agy_adapter.py loom-code/tests/test_opencode_loader.py
    loom-code/tests/test_adversarial_opencode_command_language.py
    "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized" -q`
  - `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all`
- What came back: `129 passed in 6.14s`; manifest check exit 0. Version
  3.31.0 in `loom-code/plugin.json`, `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json`, `package.json`, root README (2 places),
  the three loom-code READMEs, and CHANGELOG `## [3.31.0] — 2026-10-04`.
- Full package suite command (run by `finalize-review`, which refuses the
  attestation on failure): `scripts/run_package_tests.py --loom-family`.

## Re-run on 2026-10-04, at 22042c50
Fix range da74a343..22042c50: plan W1-04; `language-anchor.py` accepts
`UserPromptSubmit` (tool_name check now only for PostToolUse); `hooks.json`
gains a matcher-less `UserPromptSubmit` entry; `mechanisms.yaml` registers
it; CHANGELOG bullet; tests. `git diff da74a343..22042c50 --
loom-code/skills loom-code/agents contract` is empty (0 lines).

- Setup: re-tested — fresh clean copy `git worktree add
  .git/loom-scratch/at-relay2 22042c50`; `claude plugin validate
  <clean copy>/loom-code` → `✔ Validation passed`; `hooks.json parses`.
  Live sessions used `claude -p --model haiku --plugin-dir <clean
  copy>/loom-code`, cwd under `/tmp/at-relay2/`. The installed loom-code is
  3.30.0, whose hooks.json has no UserPromptSubmit language anchor and
  whose zh text still says 繁體中文, so the new zh wording on a
  `UserPromptSubmit` entry can only come from the clean copy.
- 1: carried over — the fix changes no station text (empty diff above).
- 2: carried over — the fix changes no station text (empty diff above).
- 3: re-tested — every surface the line names (after compaction, after
  resume, subagent result return foreground and background), plus the
  English-silent negative.
  - Direct hook runs (`python3 <clean copy>/loom-code/hooks/language-anchor.py`,
    synthetic transcripts of 3 user turns, files under `/tmp/at-relay2/direct/`):

    | Payload | Transcript | Output |
    |---|---|---|
    | UserPromptSubmit | zh-TW, zh-CN | zh anchor, `hookEventName: UserPromptSubmit` |
    | UserPromptSubmit | ja | ja anchor, `hookEventName: UserPromptSubmit` |
    | UserPromptSubmit | en, ko | silent, exit 0 |
    | UserPromptSubmit | 3 zh-TW turns + 3 `<task-notification>` turns (English result text) | zh anchor |
    | UserPromptSubmit | empty file; payload without transcript_path | silent, exit 0 |
    | PostToolUse Bash; Stop | zh-TW | silent, exit 0 |
    | SessionStart compact | zh-TW | zh anchor, `hookEventName: SessionStart` |

  - Live A (session 5986cd83, `/tmp/at-relay2/live-bg`): Chinese prompt
    asking for a background Agent, written with many English identifiers
    (`run_in_background: true`, `subagent_type`, `general-purpose`). No
    language anchor anywhere in the transcript — not at launch, not on the
    completion turn. `lang_detect.conversation_language(<transcript>)` →
    `en`; piping the transcript to the hook as UserPromptSubmit → silent.
    This is the pre-existing per-letter weighting (deferred follow-up), not
    the fix; the earlier run's trial 4 used a plainer prompt.
  - Live B (session 923deecf, `/tmp/at-relay2/live-bg2`): plain Chinese
    prompt 「請派一個在背景執行的子代理（背景模式要打開）…」.
    Line 32 Agent tool_use with `run_in_background`; lines 34-35
    `PostToolUse:Agent` + zh anchor at launch (15:01:08.498Z); line 47 the
    user-role `<task-notification>` completion turn (15:01:11.728Z);
    lines 48-50 UserPromptSubmit additionalContext entries, line 50 = the zh
    anchor 「對使用者的敘述一律使用使用者在對話中所用的語言與文字；…」
    (15:01:11.761Z); line 52 reply in Chinese. So the anchor now reaches
    the model on the background completion turn.
  - Live C, English negative (session 80c6ff97, `/tmp/at-relay2/live-en`):
    English prompt for a background Agent. Lines 17-18 and 45-46 are the
    only UserPromptSubmit additionalContext entries (user's delegation hook
    and the loom-workflow card); `grep -c` for the zh/ja anchor text → 0;
    no `hook_error` / `non_blocking_error` entries in either B or C.
  - Resume: Live D (session 7f37281e, `/tmp/at-relay2/live-cn`) line 41-43
    `SessionStart:resume` + zh anchor; line 48 UserPromptSubmit zh anchor
    on the resumed turn.
  - Compaction: unchanged code path (`SessionStart` branch untouched by the
    diff); direct run above still emits; the earlier live trial 3 stands.
  - First message of a session gets no anchor: in Live B the first
    UserPromptSubmit (lines 17-18) carried none. The hook reads the
    transcript, which does not yet hold the prompt being submitted:
    `conversation_language(head -8)` → `None`, `(head -16)` (prompt
    written) → `zh`. The hook does not read the payload's `prompt` field.
  - Still not covered: Codex and OpenCode hosts (not rewired, plan Risk 3);
    the first message of a session (above); interactive-mode background
    completion (print mode only tried); zh dense with English terms
    (deferred follow-up, disclosed at PR and decision point ③); languages
    other than zh/ja (out of scope, no Acceptance line requires them).
    `SubagentStop` remains unwired.
- 4: re-tested — the anchor now fires on every user turn, so exposure of a
  Simplified-Chinese user to the Traditional-script anchor text grew.
  - `_ANCHOR_TEXT` unchanged in the diff; zh text names no script variant.
  - Two-turn zh-CN sessions (turn 1 「你好，请用一句话介绍一下你自己。」, turn 2
    via `--resume` 「请用两三句话说明为什么写测试很重要。」), script
    `/tmp/at-relay2/trial.sh`, counting a fixed set of Traditional-only vs
    Simplified-only characters in the turn-2 reply:

    | Run | Clean copy loaded | Anchor entries | Turn-2 reply script |
    |---|---|---|---|
    | 7f37281e | yes | 2 (resume + UserPromptSubmit) | Traditional (「測試讓你在改動代碼時有信心…」) |
    | 6c8ef1d3, 4a4bb1b8, 609a8527, b4a06609, 4c5a32b6, 2d025911, e9a96091 | yes | 2 each | Simplified (7–15 Simplified-only chars, 0 Traditional-only) |
    | 232591a9, 0d230739, 236ca93f | no (control) | 0 | Simplified |

    1 of 8 with the anchor flipped to Traditional; 0 of 3 without. The
    sample cannot separate the anchor from chance; the user's own
    Traditional-Chinese delegation card is present in every run, both arms.
- 5: carried over — the fix changes no station or agent text (empty diff
  above); the English-artifact sentences are in skill files outside the
  fix range.
- 6: re-tested.
  - Same criterion command as row 6 above, run in the clean copy at
    22042c50 → `132 passed in 6.16s` (3 more than before: the two new
    UserPromptSubmit anchor tests and the hooks.json UserPromptSubmit test).
  - Registry touched by the fix: `pytest loom-code/tests/test_check_mechanisms.py -q`
    → `66 passed in 3.49s`.
  - `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all`
    → exit 0. Version 3.31.0 in the four loom-code manifests, root README
    (2 places), the three loom-code READMEs and CHANGELOG
    `## [3.31.0] — 2026-10-04`.
  - Full package suite (`scripts/run_package_tests.py --loom-family`) not
    run here; `finalize-review` runs it on committed content and refuses
    the attestation on failure.
