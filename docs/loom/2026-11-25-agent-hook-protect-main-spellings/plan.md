# Agent hook blocks common spellings that commit, merge or push to main — plan
intent: 2026-11-25-agent-hook-protect-main-spellings@8928da057
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/loom_checker/command_handlers/push.py` `_protect_main` matches only `^\s*git (merge|commit|push)` on the whole command and checks the hook cwd's branch.
- Reverse: `loom-code/hooks/hooks.json`, `hooks-codex.json`, `hooks-opencode.json` (via `opencode/loader.js`) and `hooks/agy_adapter.py` `push_gate` all call `push --hook`.
- Error: `cmd_push` writes the "direct git merge, commit, or push on main/master is blocked" line to stderr and returns 2.
- Data: `git config --local --bool loom.protectMain` false disables the guard; `current_branch(cwd)` supplies the branch.
- Boundary: `loom-code/tests/test_main_branch_hook.py::test_prefixed_and_wrapped_commands_are_outside_guard` pins `cd x && git push origin main` and `true; git commit` as allowed.

## Task DAG

### Wave 1

**W1-01 Guard reads cd, git -C and push destinations**  after: none  acceptance: 1, 2, 3, 4, 5, 6
- Files: loom-code/scripts/loom_checker/command_handlers/push.py, loom-code/tests/test_main_branch_hook.py, loom-code/tests/test_opencode_loader.py, loom-code/tests/test_agy_adapter.py
- Test: A1 positive: cd-main-commit-denied; negative: cd-feature-commit-allowed. A2 positive: git-C-main-merge-denied; negative: git-C-feature-commit-allowed. A3 positive: feature-push-head-to-main-denied; negative: feature-push-to-feature-allowed. A4 positive: existing-denials-kept; negative: opt-out-allows-cd-main-commit. A5 positive: no-native-hooks-repo-denies; boundary: bash-c-still-outside-guard. A6 positive: opencode-and-agy-refuse-three-spellings; negative: opencode-and-agy-allow-feature-push.
- Risk: rewrites `test_prefixed_and_wrapped_commands_are_outside_guard` (narrows it): `cd`/`;` segments become guarded, `bash -c` stays outside. Host files get one parametrized case each. Reuse `_operator_segments`/`_tokenise`; agent-decided.

**W1-02 Release metadata for loom-code 3.90.1**  after: W1-01  acceptance: 4
- Files: loom-code/.claude-plugin/plugin.json, loom-code/CHANGELOG.md, loom-code/README.md, loom-code/README.ja.md, loom-code/README.zh-TW.md, README.md, loom-code/tests/test_write_plan_station_text.py
- Test: A4 positive: release_sync; boundary: release_stale_pin. Existing pin `test_current_release_metadata_is_synchronized` covers it.
- Risk: A4 ownership is nominal (installed copies only get the kept behaviour after a bump); patch 3.90.0 → 3.90.1 via SSOT then `sync_codex_manifests.py --all`; agent-decided.

**W1-03 Graduate adversarial probes into loom-code suite**  after: W1-01  acceptance: 4
- Files: docs/loom/2026-11-25-agent-hook-protect-main-spellings/evidence/probes/test_abuse_main_guard_overblocks.py, docs/loom/2026-11-25-agent-hook-protect-main-spellings/evidence/probes/test_abuse_main_guard_slips.py, loom-code/tests/test_abuse_main_guard_overblocks.py, loom-code/tests/test_abuse_main_guard_slips.py
- Test: A4 positive: overblock-probes-pass; boundary: slip-probes-pass
- Risk: probe content unchanged; only location

## Simplicity check
- Patch only the existing `_protect_main` instead of adding a new module or rule id — taken
- Track `cd` targets and `git -C` paths per operator segment, without a full shell parser — taken
- Skip host-wrapper tests and rely on the shared checker — declined: user asked for acceptance line 6
- One parametrized refusal test per host file (three spellings plus one feature-push allow); full matrix only in `test_main_branch_hook.py` — taken
- Fold W1-02 release bump into W1-01 — declined: intake requires a task per file set and repo history keeps release metadata as its own last task

## Questions asked
① — what — Should Claude Code, Codex and OpenCode all be fixed? (user asked; answered: all four hosts share one checker; user then asked to add acceptance line 6 for OpenCode loader + Antigravity adapter)
① — consequence — Confirm scope plus authorization to auto push and open a PR after closing-review (user: yes)

## Risks
1. user-decided — Close the `cd &&`, `git -C` and feature-to-main push spellings now; wrappers (`sh -c`, scripts, aliases) stay outside the host hook.
2. Over-blocking risk: a push whose destination is a tag or non-main branch must stay allowed; covered by W1-01 negative cases.
3. Codex host refusal is not exercised end to end; the acceptance report states it as not verified.
