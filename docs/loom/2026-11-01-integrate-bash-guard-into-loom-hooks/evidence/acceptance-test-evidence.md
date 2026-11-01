# Integrate the small bash guard into Loom hooks — acceptance test evidence

Tested on 2026-11-01 in a clean `git archive 3d5f64bd` extraction at `/private/tmp/loom-guard-acceptance-3d5f64bd`. The tree was exported from committed HEAD, with no working-tree files carried over. This is source and hook-command testing, not a live host installation.

## Setup

- README.md:177-279 documents host installation and `agy plugin validate ./loom-code`; README.md:275-279 documents the full package-suite command.
- Command: `agy plugin validate ./loom-code` from the clean copy.
- Result: exit 0; `[ok] ./loom-code`, 7 skills, 4 agents, 1 hooks bundle processed.
- Command: `UV_CACHE_DIR=/private/tmp/loom-guard-uv-cache uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_main_branch_hook.py loom-code/tests/test_agy_adapter.py loom-code/tests/test_publish_command_detection.py loom-code/tests/test_hooks_json.py`.
- Result: exit 2 before tests; failed to fetch `https://pypi.org/simple/mdurl/` because DNS lookup failed. An earlier attempt without `UV_CACHE_DIR` was blocked from writing the default uv cache (`Operation not permitted`).
- Fallback command: `/Users/kouko/.conda/envs/dbt-redshift/bin/python -m pytest -q loom-code/tests/test_main_branch_hook.py loom-code/tests/test_agy_adapter.py loom-code/tests/test_publish_command_detection.py loom-code/tests/test_hooks_json.py` from the clean copy.
- Result: exit 0, `132 passed in 25.09s`. This reused an existing local environment, so it does not establish a first-time dependency download.

## 1. loom-code 外掛啟用時，不論專案是否正在走 Loom 流程，執行前檢查都能阻止 main/master 上直接執行的 `git merge`、`git commit` 與 `git push`，並讓功能分支上的正常工作繼續；不宣稱能阻止複合指令、腳本或其他方式更新主分支。

- How I tried it: ran the four focused test modules above in the clean copy. `test_direct_git_mutation_denied_on_main_branches` creates main and master repositories, passes merge/commit/push commands to `push --hook`, and expects exit 2. `test_feature_branch_allows_git_mutation` expects exit 0. `test_prefixed_and_wrapped_commands_are_outside_guard` expects exit 0 for prefixed or wrapped commands. `test_shell_host_hook_blocks_direct_main_commit_only` invokes the manifest command for Claude, Codex, and OpenCode; `test_main_branch_git_commit_returns_deny` checks Antigravity's decision carrier.
- What came back: all these named tests passed in the 132-test run; main/master refusals include `main/master`, feature invocations return 0, and wrapper examples return 0.
- Evidence: `loom-code/tests/test_main_branch_hook.py:38-62`, `loom-code/tests/test_hooks_json.py:288-312`, `loom-code/tests/test_agy_adapter.py:107-113`; captured pytest result above. The guard intentionally recognizes a direct leading Git verb and does not cover all shell compositions (`loom-code/scripts/loom_checker/command_handlers/push.py:26,72-80`).

## 2. 在非 Git 目錄與 detached HEAD，`ls` 等一般 Bash 指令可照常執行；既有的破壞性指令檢查仍各自運作。

- How I tried it: the clean-copy test `test_non_git_and_detached_head_allow_ordinary_command` invokes `ls` in both states. Ran `bash tests/claude_settings_sync_test.sh` in the separate dotfiles cutover tree at commit `1838788`.
- What came back: the `ls` test passed. Dotfiles sync reported `claude settings sync tests: PASS`, including `template_owned_tool_command_not_duplicated | pass`, `real_template_reconciles_legacy_dcg | pass`, and `external_path_dcg | pass`. The cutover template still lists Bash deny permissions and a dcg command; I did not execute every destructive command through a live Claude host.
- Evidence: `loom-code/tests/test_main_branch_hook.py:64-69`; `/private/tmp/dotfiles-loom-bash-guard-cutover/claude/settings.template.json:25-46,98-107`; captured shell-test output above.

## 3. Loom 原有的發佈提醒與其他執行前行為仍可正常運作。

- How I tried it: the focused run included `test_pr_merge_keeps_reminder_policy_on_main`, the publication reminder tests, host hook schema and runtime tests, and Antigravity adapter tests.
- What came back: the named tests passed. The PR merge command is allowed and emits `merging anyway.`; publication tests check reminder delivery through stdout and stderr and allow-on-error behavior.
- Evidence: `loom-code/tests/test_main_branch_hook.py:79-83`, `loom-code/tests/test_publish_command_detection.py:98-146`, `loom-code/tests/test_hooks_json.py:58-263`, `loom-code/tests/test_agy_adapter.py:94-113`; captured 132-test result above.

## 4. 切換到已安裝的新版本後，同一個 Git 保護規則只執行一次；dotfiles 不再註冊獨立的 bash-guard。

- How I tried it: inspected the committed cutover template and ran its sync test in the cutover tree. Read the current live dotfiles template and installed Codex plugin version without changing either.
- What came back: the cutover test reported one `Bash|PowerShell` dcg, stale Bash guard removed, and foreign hooks retained. The cutover template has no `executable_bash-guard.sh` command. The current live dotfiles template still has that command at line 108, while the installed Codex cache reports version `3.55.0`; the new source is `3.55.1`. I could not observe the post-install, post-sync single-run state.
- Evidence: `bash tests/claude_settings_sync_test.sh` output above; `/private/tmp/dotfiles-loom-bash-guard-cutover/claude/settings.template.json:98-107`; `/Users/kouko/dotfiles/claude/settings.template.json:108`; `loom-code/.claude-plugin/plugin.json:3`; `/Users/kouko/.codex/plugins/cache/loom/loom-code/3.55.0/.claude-plugin/plugin.json:3`.

## 5. 相關測試與 Loom 完整套件測試通過，並能在乾淨環境重現保護與放行結果。

- How I tried it: exported the exact committed tree, validated the plugin with agy, and ran the four focused test modules in that clean copy. Separately, the closing-review owner ran the documented full-suite command, `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`, on the same committed functional HEAD.
- What came back: clean-copy plugin validation passed and 132 focused tests passed. The closing-review owner's full-suite rerun exited 0; its Python group summaries were `2517 passed, 2 skipped in 92.11s`, `209 passed, 1 skipped in 15.88s`, and `125 passed, 3 skipped in 2.66s`; the remaining discovered checks also completed. My own isolated dependency setup could not reach PyPI, so first-time dependency download was not established by my clean-copy run.
- Evidence: Setup section above; README.md:275-279; closing-review full-suite capture at `/private/tmp/merge-hooks-suite-rerun.log` (lines 39, 43, 63 and final check output). The full suite is an automated pre-acceptance gate; its result was supplied by the closing-review owner, not reproduced by this tester.

## 6. dotfiles 與個人 Obsidian vault 仍能在主分支工作，且這兩個例外不會套用到其他使用者的專案。

- How I tried it: the clean-copy `test_repo_local_opt_out_allows_main_branch` sets `loom.protectMain=false` in a temporary repository and invokes `git commit` through the checker. The main-branch denial test uses another temporary repository without this local setting. Read-only `git -C /Users/kouko/dotfiles config --local --get loom.protectMain` and the corresponding vault command were run on the real repositories.
- What came back: the temporary opt-out allows the command while ordinary main repositories are denied. Both real `git config --local --get` calls exited 1 with no value, so neither personal exception is active. The parent agent reported automatic approval review rejected the two actual local config writes; I did not retry or bypass those writes.
- Evidence: `loom-code/tests/test_main_branch_hook.py:38-47,72-76`, `loom-code/scripts/loom_checker/command_handlers/push.py:72-80`; captured 132-test result above; read-only local config checks exited 1.
