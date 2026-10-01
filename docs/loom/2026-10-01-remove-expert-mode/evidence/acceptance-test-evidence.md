# Remove expert-mode and its typed skip confirmation — acceptance test evidence

Tried on 2026-10-01, in a clean copy of the project at 51ca2e87 (`git worktree add --detach <scratchpad>/at-wt HEAD`, removed afterwards). Python ran as `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python ...`. The base for comparisons is 96e6d0b8 (extracted with `git archive 96e6d0b8`).

## Setup — the change installs and loads in the clean copy
- How I tried it: README "Install" section. For Claude Code, instead of `claude plugin install` (which would overwrite the user's installed 3.26.1), I ran `claude plugin validate .` and `claude plugin validate ./loom-code|./loom-design|./loom-workflow`, then loaded the three plugins from the clean copy with `claude -p --plugin-dir <copy>/loom-code --plugin-dir <copy>/loom-design --plugin-dir <copy>/loom-workflow --settings '{"enabledPlugins":{"loom-code@loom":false,"loom-design@loom":false,"loom-workflow@loom":false}}'`, which turns the installed copies off for that run.
- What came back: every validation `✔ Validation passed` (warnings only: unknown field `requires-contract`, unquoted `${CLAUDE_PLUGIN_ROOT}` in loom-workflow's PostToolUse hook, no marketplace description; all present at base too). The session listed 6 loom-code, 6 loom-design and 12 loom-workflow skills.
- Evidence: captured output above. Codex, Antigravity CLI and OpenCode were not launched (cannot be started interactively here; the `codex`, `agy` and `opencode` shell functions also run the user's own update/launch scripts).

## 1. expert-mode is no longer offered on Claude Code, Codex, Antigravity CLI or OpenCode, as a skill or as a command.
- How I tried it:
  - Claude Code, live: in an empty scratch git repo, `claude -p --model sonnet --settings '<installed loom plugins off>' --plugin-dir <copy>/loom-code "/loom-code:expert-mode"`. Control: the same prompt with the user's installed loom-code 3.26.1.
  - OpenCode: drove the real loader `loom-code/index.js` → `opencode/loader.js` `setup(ctx)` under Node with a recording `ctx` (scratch `oc_probe.mjs`), for the clean copy and for the base copy.
  - Codex and Antigravity CLI: read the files each host loads. Codex `loom-code/.codex-plugin/plugin.json` → `"skills": "./skills/"`, `"hooks": "./hooks/hooks-codex.json"`; Antigravity `loom-code/hooks.json` → `agy_adapter.py push-gate` / `pre-invocation` and the plugin's `skills/` folder.
  - `ls loom-code/skills/` and `find . -iname '*expert*'`.
- What came back:
  - Claude Code (new): "`/loom-code:expert-mode` isn't available in this session, so it didn't run. … The loom-code commands that are available are `/loom-code:using-loom-code`, `/loom-code:write-plan`, `/loom-code:build`, `/loom-code:closing-review`, `/loom-code:ship` and `/loom-code:maintain`."
  - Claude Code control (installed 3.26.1): the skill ran and answered with its step table, ending "I'll then show a run/skip table and a confirmation code. The skip takes effect only after you type `/loom-code:expert-mode` with that code." — so the probe does tell the two apart.
  - OpenCode new: `{"skills":[build, closing-review, maintain, ship, using-loom-code, write-plan],"commands":["loom-code:using-loom-code"]}`; base: `"commands":["loom-code:expert-mode","loom-code:using-loom-code"]`.
  - `loom-code/skills/` holds build, closing-review, maintain, ship, using-loom-code, write-plan; the only `*expert*` paths are dated change folders, intents and one dated evidence probe under `docs/loom/2026-09-*`.
  - `hooks-codex.json` has one PreToolUse hook (`loom_checker.py push --hook`); `hooks.json` (Antigravity) has push-gate and pre-invocation only; `git grep -i selection` over `loom-code/hooks/` is empty, while base `agy_adapter.py:15,40-43` carried the selection-store guard.
- Evidence: captured outputs above. Codex and Antigravity are judged from installed-surface files only — not a live session.

## 2. A user can still skip any of the eight steps in plain words with the same outcome as before: reviewers, package suite and adversarial skips leave the change unattested and disclosed as `absent`; the other five lose nothing.
- How I tried it:
  - Read the plain-words skip rule in `loom-code/skills/build/SKILL.md:18-31`, `closing-review/SKILL.md:22-35`, `write-plan/SKILL.md:43-55`, `ship/SKILL.md:26-37`, `using-loom-code/SKILL.md:21-22`, and the diff against base for build (only the `selection show` / expert-mode routes were removed; the plain-words rule and record line are unchanged).
  - Spec and plan skips, live: see section 5 (`intake write-plan` passes once a dated record exists).
  - Reviewers / suite / adversarial: ran `loom-code/tests/test_selection_finalize.py` (incl. `test_reviewers_skipped_in_plain_words_leave_the_change_unattested`, `test_v2_without_selection_keeps_every_floor`, the `finalize.adversarial` / package-suite refusals) and `test_verification_status.py::test_absent_lists_missing_records`.
  - Live: `pr-floor` from the new checker on this branch (no attestation yet) — see section 4.
  - Removed route: `loom_checker.py selection show` → `unknown sub-command`, exit 2.
- What came back: `171 passed in 79.71s` for `test_verification_status.py test_selection_finalize.py test_loom_checker_intake.py`. With no reviewer verdicts finalize-review refuses with `finalize.verdicts`, writes no attestation, and the status is `absent`. Dropping the adversarial or package-tests execution from an attestation makes it invalid. Unattested branch → `::notice title=verification::absent`, exit 0 (CI does not block).
- Evidence: named tests above; command output. Implementer, tdd and acceptance-test skips are prose-only steps (no checker floor before or after); their prose is unchanged apart from the removed `selection show` alternative.

## 3. No loom skill, hook, checker command or rule, README, CHANGELOG-current section or standing loom doc still offers expert-mode or a typed skip confirmation code.
- How I tried it: `git grep -n -i -E 'expert[- _]?mode|expert_mode|エキスパート|專家模式' -- . ':!docs/loom/20*' ':!docs/loom/intent/'` (CHANGELOGs separately); `git grep -i -E 'selection (capture|show|confirm|record-failure|store)|confirmation code|four-character|typed (skip|code|confirm)|step selection|generated code|valid \(skipped'`; first section of each plugin CHANGELOG; `loom_checker.py --list-rules | grep -i -E 'select|expert|skip|confirm'`; the checker's usage text; ran `loom-code/tests/test_simplified_station_text.py` (pins `test_no_current_surface_offers_expert_mode`, `test_each_station_keeps_the_plain_words_skip_rule`).
- What came back:
  - Non-dated hits: `docs/loom/KICKOFF-DEFAULTS.md:14` (history line stating step selection was removed and plain words is the only skip route); test comments and docstrings; nothing that offers it.
  - CHANGELOG current sections (loom-code 3.27.0, loom-design 2.9.0, loom-workflow 5.6.2) mention expert-mode only as removed.
  - Checker usage lists no `selection` command; rule list has no selection/expert rule (hits are unrelated: `adversarial.proportionate`, `intake.confirmed`, `land.cleanup`, `plan.field-caps`).
  - Remaining `selection` words in checker code are the attestation field that must be null (`attestation.py:36-54`, `manifest.yaml:204`) and the historical delivery-witness reader (`intent_state.py:130`) that keeps old merged attestations readable; `selection-confirmed` belongs to the unrelated second-vendor reviewer choice.
  - Test fixture text in `loom-code/tests/test_adversarial_blocked_publish_routes.py:164,497` still says "propose a step selection"; it is forged input for a prose test, not a surface.
  - `50 passed in 0.73s` for the station-text and report-shape tests.
- Evidence: grep output above.

## 4. Pull requests and merges of changes made after the removal show the same verification statuses as today for runs without a typed confirmation.
- How I tried it: scratch script `floor_diff.sh` runs `loom_checker.py pr-floor --body-file <body with all nine headings and 'Verification status: valid'> --base <b> --head <h> --branch <n>` from the new checker and from the base checker against the same repository state. Ranges: this branch (96e6d0b8..51ca2e87, no attestation); PR #73 (668158f5..96e6d0b8); PR #71 (adafa838..d8e47b0a); a multi-change range (adafa838..96e6d0b8, branch `x`). Also ran the new `test_verification_status.py` against the base checker code.
- What came back:
  - This branch: new `absent`, base `absent`.
  - #73: new `valid`, base `valid`. #71: new `valid`, base `valid`.
  - Multi-change range: both `stale (change not identified: … the branch delta carries 3 intent files …)`.
  - All exit 0 on both.
  - New test file on base code: `1 failed, 15 passed`; the one difference is `test_claimed_selection_is_stale_at_both_depths[ci]`, an attestation carrying a typed selection (base `valid (skipped: adversarial)`, new `stale`) — the typed-confirmation case the line excludes.
- Evidence: captured output above. Merges were not exercised live (they go through GitHub); the merge gate is the same PR-floor check run above.

## 5. Every step skipped in plain words before Ship is recorded on the change's branch as skipped by the user's instruction, with its date, and a spec or plan skip recorded that way still waives the spec or plan.
- How I tried it: the record instruction in write-plan, build and closing-review (each appends `skipped-by-instruction: <step> <YYYY-MM-DD>` to the plan's `## Risks`, or the intent's `## Constraints` when plan is absent or skipped, and commits it). Live: scratch repo `a5repo` (branch `work`, `origin/HEAD` set), a confirmed product intent with `needs-design: yes` and no spec; ran `loom_checker.py intake write-plan demo` from the clean copy at each step.
- What came back:
  - A, no record: `BLOCK intake.spec-ready: needs-design: yes but no spec at docs/loom/demo/spec.md.` exit 1.
  - B, undated `skipped-by-instruction: spec` in Constraints: same BLOCK, exit 1.
  - C, `skipped-by-instruction: spec 2026-10-01` in Constraints: exit 0.
  - D, record moved to the plan's `## Risks`, plan deliberately malformed: no spec block; `BLOCK intake.test-case-pair` and `plan.field-caps` blocks, exit 1.
  - E, plus `skipped-by-instruction: plan 2026-10-01`: exit 0.
  - `test_loom_checker_intake.py` (in the 171 above) passes, including undated and fenced-example records that do not waive.
- Evidence: command output above. That an agent actually writes the line in a live session was not run; it is the station instruction, unchanged from base.

## 6. When the user is asked to accept a change, the acceptance test report lists every step skipped by the user's instruction; when acceptance testing itself was skipped, the user is told the skipped steps in the conversation instead.
- How I tried it: read the report template section "Steps you told me to skip" (`loom-code/skills/closing-review/references/acceptance-test-report.md:61-73`) and the charter must-list (`loom-code/contract/manifest.yaml:217`); wrote this change's own report from that template, reading the plan's `## Risks` and the intent's `## Constraints` (no `skipped-by-instruction:` lines). Read `closing-review/SKILL.md:218-223` for the skipped-acceptance-testing case. Ran `test_acceptance_test_report_shape.py` and `test_contract_charter.py` (in the 50 above).
- What came back: the template requires the section, one bullet per step in plain words with its date, or "Nothing — no step was skipped."; the charter lists it; the report for this change carries it. Closing-review says that when acceptance testing is skipped, the user is told in the conversation, before Ship, every step skipped by instruction, read from the committed lines and described in plain words.
- Evidence: file lines above; this change's report. Not run: a live closing-review session where acceptance testing is skipped (would need a full agent session through review). Also `loom-code/agents/acceptance-tester.md:74-80` lists the report's parts as four (rows, data paragraph, decisions, open questions) and does not name the skipped-steps section; it defers to "the structure … that the template specifies".

## 7. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.
- How I tried it: `git diff --stat 96e6d0b8..HEAD` by top folder (loom-code 52, loom-design 10, loom-workflow 9 files, plus root README, scripts, tests, docs); `"version"` in each plugin's `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, `plugin.json`, `package.json`; first CHANGELOG heading; README version strings (root table, each plugin README in en / zh-TW / ja); `scripts/sync_codex_manifests.py --check --all`; ran `loom-code/tests/test_adversarial_version_metadata_sync.py`, `loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`, `loom-workflow/tests/scripts/test_release_metadata.py`.
- What came back: loom-code 3.27.0 ×4 manifests, CHANGELOG `## [3.27.0] — 2026-10-01`, root README 3.27.0, loom-code README / README.zh-TW 3.27.0; loom-design 2.9.0 ×4, CHANGELOG 2.9.0, READMEs 2.9.0; loom-workflow 5.6.2 ×4, CHANGELOG 5.6.2, READMEs en/zh-TW/ja 5.6.2. Sync check exit 0. `14 passed`, `9 passed`.
- Evidence: output above. The full suite was not run here; finalize-review runs it and refuses the attestation on failure. Suite command (from `docs/loom/KICKOFF-DEFAULTS.md:8`): `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
