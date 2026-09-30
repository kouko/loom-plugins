# Start loom's entry skills from OpenCode's command list — acceptance test evidence

Tried on 2026-09-30, in a clean copy of the project at `433c2ebe` (a detached
`git worktree` in the tester's scratch area, removed afterwards).

Environment used for every line (same method as the 2026-09-29 OpenCode v2 run):

- Binary `/Users/kouko/.opencode/bin/opencode`, called by absolute path; it reports
  `opencode v2.0.20`. The shell function `opencode` (litellm launcher) was not used.
- Isolated scratch tree `oc-at4/` with its own `XDG_CONFIG_HOME`, `XDG_DATA_HOME`,
  `XDG_CACHE_HOME`, `XDG_STATE_HOME`, `OPENCODE_CONFIG_DIR`, plus
  `OPENCODE_DISABLE_AUTOUPDATE=1` and `OPENCODE_DISABLE_PROJECT_CONFIG=1`. Every
  `CLAUDE*`, `CODEX*`, `ANTHROPIC*` and other `OPENCODE*` variable unset (count 0
  checked). `gh` isolated (`GH_CONFIG_DIR` in the scratch tree, tokens unset).
- Service port 49641, set with `opencode service set port 49641` before anything else.
- Model: the `litellm` provider block copied from the earlier run's isolated config
  (its `apiKey` is an `{env:...}` reference); default `litellm/hyper-coding-group`
  (free third-party routes). Only `OPENCODE_LITELLM_API_KEY` is exported, read in a
  subshell from the litellm secrets file; it was never printed or written.
- Session directory: an empty throwaway `git init` repo `oc-at4/proj`.
- Install: README.md:246-254 steps, with a pinned local spec in place of
  `github:...#main` (the branch head is not what `main` carries yet):
  `opencode plugin add 'git+file:///Users/kouko/GitHub/loom-plugins#433c2ebe::path:<plugin>'`
  for `loom-code`, `loom-design`, `loom-workflow`, then `opencode service restart`.
- TUI driven in a private tmux server (`tmux -L ocat4`, 160x50). Permission prompts:
  only `external_directory` reads of loom's installed plugin cache
  (`oc-at4/xdg/cache/opencode/...`) were answered "Always allow" (helper
  `oc-at4/drive.sh`); any other prompt would have stopped the run (none came).
- Registries read from the isolated service's HTTP API directly (`oc-at4/reg.py`),
  because `opencode api` cuts output near 256 KiB; the isolated service password
  is read from its own `service.json`.
- The user's `~/.config/opencode` and the user's OpenCode services on 49374
  (pid 91480) and 57148 (pid 71492) were not touched; both were still listening
  at the end.

Setup check (step 2):
- `opencode plugin list` before install → `No plugins found`.
- Each `plugin add` → `Plugin "<spec>" installed and added to …/oc-at4/cfg/opencode.json`.
- After `service restart`: +8 s `No plugins found`; +16 s `loom-code`, `loom-design`,
  `loom-workflow`, version `433c2eb` (README's restart note covers the delay).

## 1. In OpenCode v2 with loom installed, the `/` command list offers loom-code:using-loom-code, loom-design:using-loom-design, loom-workflow:using-loom-workflow, loom-workflow:handoff, loom-workflow:recap-state and loom-workflow:goal-create, and running each one starts that skill's workflow.

- How I tried it:
  1. `GET /api/command` (log `oc-at4/logs/commands.json`, `registry.json`).
  2. TUI: typed `/loom`, `/`, `/using`, `/expert`, `/build` in the prompt and captured
     the menu (logs `tui-slash-loom.txt`, `tui-slash-all.txt`, `tui-slash-using.txt`).
  3. TUI: for each command, a new session (`/clear`), typed `/<id>`, Tab, the text
     below, Enter; drove until idle (logs `tui-<name>.txt`, `msgs-<session>.json`).
- What came back:
  - `/api/command`: `init`, `review`, and exactly seven loom commands:
    `loom-code:using-loom-code`, `loom-code:expert-mode`, `loom-design:using-loom-design`,
    `loom-workflow:using-loom-workflow`, `loom-workflow:handoff`,
    `loom-workflow:goal-create`, `loom-workflow:recap-state`.
  - TUI `/loom` menu: the same seven entries, each once, with their descriptions.
    `/using` → the three `using-*` entries once each. `/build` → no `loom-code:build`
    entry (skills are not listed in the `/` menu).
  - Runs (each stored user message is `/<id> <text>` followed by
    `Base directory for this skill: …/node_modules/<plugin>/skills/<skill>` and that
    skill's body):
    - `/loom-workflow:recap-state` (no text) → read the skill's
      `references/seven-block-schema.md`, inspected git, answered with the recap
      sections (必要背景, 差距與目前評估, 為什麼現在需要你確認, 待辦工作, 對齊目的與下一步).
      Session `ses_f0df72082…`.
    - `/loom-code:using-loom-code 幫這個空專案加一個會印出 hello 的 hello.py` → read
      loom-design capture-intent material, classified the change as product, and
      opened the principles interview questions for decision point ①.
      Session `ses_f0df453f5…`.
    - `/loom-design:using-loom-design 我想為一個小型待辦清單 app 定義要做什麼` →
      checked `docs/loom`, started the PRINCIPLES interview with a question form
      ("這個待辦清單 app 是給誰用的？"). Dismissed by the tester. Session `ses_f0def3411…`.
    - `/loom-workflow:using-loom-workflow 我想保存這次工作的狀態，明天接著做，該用哪個工具？`
      → loaded `loom-workflow:loom-visualization`, recommended `loom-workflow:handoff`
      in a comparison table and offered to run it. Session `ses_f0dee1f16…`.
    - `/loom-workflow:handoff 今天先到這裡，幫我把狀態存起來` → wrote
      `proj/.claude/handoffs/HANDOFF-2026-09-30-192953-session-save.md` (5860 bytes)
      and printed the Resume Launcher. Session `ses_f0dec5a20…`.
    - `/loom-workflow:goal-create 為這個 session 建一個目標：在這個專案加一個會印出 hello 的 hello.py`
      → ran the goal check (`exit=0`), produced the four-field goal
      (Outcome / Constraints / Verification / Stop-when) and said no native goal tool
      exists on this host, so the goal was not activated. Session `ses_f0de9f7bb…`.
- Adversary finding fixed in `78b3ba6c` (language anchor), checked live:
  - Session `ses_f0df453f5…`: Chinese prompt, then `/loom-code:using-loom-code …`,
    then a request to load a skill. loom's per-session transcript
    (`$TMPDIR/loom-opencode/ses_f0df453f5ffeSqO5N9IqvGaVTS.jsonl`) holds three user
    lines: the Chinese prompt, `/loom-code:using-loom-code 幫這個空專案加一個會印出 hello 的 hello.py`
    (typed text only, no skill body), and the Chinese request. The skill tool result
    carried `對使用者的敘述一律使用會話語言（繁體中文）；…`.
  - Session `ses_f0dee1f16…` (command is the only user turn): transcript holds only
    `/loom-workflow:using-loom-workflow 我想保存這次工作的狀態，…`; the model's own
    `loom-workflow:loom-visualization` load carried the 繁體中文 reminder.
  - Transcripts for recap-state and handoff sessions likewise hold only the typed text.
- Plan Risk 1 (command and skill with the same id side by side): the `/` menu shows
  each of the seven once and no skills at all. The registries do carry the six ids in
  both `/api/command` and `/api/skill`, which is the intended "command and skill" state;
  no duplicate entry is visible to the user.
- Evidence: `oc-at4/logs/commands.json`, `registry.json`, `tui-slash-*.txt`,
  `tui-recap-state.txt`, `tui-using-loom-design.txt`, `tui-using-loom-workflow.txt`,
  `tui-handoff.txt`, `tui-goal-create.txt`, `msgs-ses_*.json`, `sessions.txt`.
- Verdict: works.

## 2. The same six remain available as skills the model can load in OpenCode, as before.

- How I tried it:
  1. `GET /api/skill` (full, via direct HTTP) → `logs/registry.json`.
  2. New TUI session: asked the model to load, with the skill tool, each of the six ids
     and `loom-code:expert-mode`, without following them (log `tui-skill-load.txt`,
     `msgs-skill-load.json`); compared each loaded body with the clean copy's
     `SKILL.md` (`oc-at4/skillcheck.py`).
- What came back:
  - `/api/skill`: 24 `loom-*:` ids, the same count as the 2026-09-29 run; the six are
    present (`loom-code:using-loom-code`, `loom-design:using-loom-design`,
    `loom-workflow:using-loom-workflow`, `loom-workflow:handoff`,
    `loom-workflow:recap-state`, `loom-workflow:goal-create`), each with a path under the
    installed `node_modules/<plugin>/skills/<skill>/SKILL.md`.
  - All six skill-tool loads succeeded; each loaded from the installed plugin cache and
    its body matched the clean copy's `SKILL.md` (`body matches clean copy: True` ×6).
  - Diff `d8e47b0a..433c2ebe` over `*/SKILL.md`: only six added lines
    `user-invocable: true`; no skill renamed or removed.
- Side note: `/api/skill` also holds 17 non-loom entries: OpenCode's 2 built-ins and
  15 from the user's own Claude skill folders (`~/.claude/skills` and similar), which
  OpenCode reads by itself even in the isolated config. Read-only, unrelated to this
  change.
- Verdict: works.

## 3. loom-code:expert-mode is still offered as a command and is still not offered as a skill.

- How I tried it: the same `/api/command`, `/api/skill`, TUI `/loom` and `/expert`
  menus and the skill-tool load as in 1 and 2.
- What came back:
  - `/api/command` and the TUI menu list `loom-code:expert-mode`
    ("Skip chosen Loom steps for one change. Only for the user typ…").
  - `/api/skill` has no `loom-code:expert-mode`.
  - Skill tool `{"id": "loom-code:expert-mode"}` → `Unable to load skill loom-code:expert-mode`.
- The expert-mode command itself was not run (not asked by the line; it would propose
  skipping steps).
- Verdict: works.

## 4. The README's OpenCode section tells a user how to start loom after installing it, including these commands.

- How I tried it: read the OpenCode sections of `README.md` and the nine plugin READMEs
  in the clean copy.
- What came back:
  - README.md:258: "Start loom with `/loom-code:using-loom-code`,
    `/loom-design:using-loom-design` or `/loom-workflow:using-loom-workflow`;
    `/loom-workflow:handoff`, `/loom-workflow:recap-state` and `/loom-workflow:goal-create`
    are also commands, and each of these stays a skill too." expert-mode is named on the
    same line as the command `/loom-code:expert-mode`.
  - loom-code/README.md:227, README.ja.md:226, README.zh-TW.md:206 → `/loom-code:using-loom-code`.
  - loom-design/README.md:166, README.ja.md:165, README.zh-TW.md:157 → `/loom-design:using-loom-design`.
  - loom-workflow/README.md:229, README.ja.md:219, README.zh-TW.md:212 →
    `/loom-workflow:using-loom-workflow` plus handoff, recap-state, goal-create.
  - Each sentence sits right after the install steps in the OpenCode section, and the
    names match the registry in 1 exactly.
- Verdict: works.

## 5. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

- How I tried it, in the clean worktree:
  - The tests covering this change:
    `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_opencode_loader.py loom-code/tests/test_adversarial_opencode_command_language.py tests/test_agy_install_docs.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized"`
  - `/opt/homebrew/bin/python3 scripts/sync_codex_manifests.py --check --all`
  - `git diff --name-only d8e47b0a..HEAD` grouped by top folder; version greps in
    `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `package.json`,
    `plugin.json`, CHANGELOG top sections and all READMEs.
- What came back:
  - `31 passed in 2.02s`.
  - Drift check exit 0.
  - Changed plugins: loom-code (13 files), loom-design (11), loom-workflow (14).
  - loom-code 3.25.0 → 3.26.0, loom-design 2.7.2 → 2.8.0, loom-workflow 5.5.7 → 5.6.0 in
    all four manifest files each; CHANGELOG tops `## [3.26.0] — 2026-09-30`,
    `## [2.8.0] — 2026-09-30`, `## [5.6.0] — 2026-09-30`; READMEs carry only the new
    strings (5 × each), no old version string left.
- Full suite command, run by `finalize-review` (which refuses the attestation when it
  fails): `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
  Not run by the tester.
- Verdict: works.

## Cleanup

- tmux server `ocat4` killed; `opencode service stop` in the isolated tree; nothing
  listens on 49641. The user's services on 49374 and 57148 still listening.
- Worktree removed with `git worktree remove`; the real repo is clean at `433c2ebe`
  apart from this report and evidence.
- Left behind outside the scratch area: loom's own per-session language transcripts
  written by the plugin under test in the system temp folder
  (`$TMPDIR/loom-opencode/ses_f0de*.jsonl`, `ses_f0df*.jsonl`, 7 small files). They
  hold only the test prompts.
- Cost: seven short sessions on free routes (largest context 53.9K tokens).
