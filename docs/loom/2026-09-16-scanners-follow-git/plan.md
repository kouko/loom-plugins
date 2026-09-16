# Loom asks git which files belong to the repository it is running in — plan
intent: 2026-09-16-scanners-follow-git@8390868c
spec: docs/loom/2026-09-16-scanners-follow-git/spec.md@032dde7b
charter: 1.0

## Task DAG

Wave 1 ships the mechanism. Wave 2 moves each consumer onto it; W2-02 runs
after W2-01 because Acceptance 2 and 6 are stated over all six scanners and
can only be proven once every one of them uses the module.

**W1-01 Ship the repository file list module**  after: —  acceptance: 4, 5
- Files: loom-code/scripts/repo_files.py, loom-code/scripts/test_repo_files.py
- Test: A4 positive: test_repo_files.py::test_walks_when_git_is_absent; boundary: test_repo_files.py::test_archive_copy_listing_matches_git_checkout. A5 positive: test_repo_files.py::test_untracked_unignored_file_is_listed; negative: test_repo_files.py::test_gitignored_file_is_absent.
- Risk: agent-decided — `-z` is mandatory, and entries that are not existing regular files are dropped: `--others` emits a nested worktree as one directory entry and `--cached` lists staged-but-deleted paths.

**W2-01 loom-code scanners use the module**  after: W1-01  acceptance: 1
- Files: loom-code/scripts/loom_checker/probes.py, loom-code/scripts/check_doc_citations.py, loom-code/scripts/rehearse_probes.py, loom-code/scripts/test_check_doc_citations.py, loom-code/scripts/test_rehearse_probes.py, loom-code/scripts/test_loom_attestation.py
- Test: A1 positive: test_loom_attestation.py::test_test_command_ignores_nested_worktree; negative: test_loom_attestation.py::test_test_command_still_detects_own_tests.
- Risk: agent-decided — a smaller candidate set can change check_doc_citations verdicts; its rule is untouched and its docstring rationale is rewritten in this task.

**W2-02 loom-workflow and root scanners use the module**  after: W2-01  acceptance: 2, 6
- Files: loom-workflow/scripts/test_no_live_cot_explain_references.py, scripts/check_plugin_boundaries.py, scripts/test_state_anchor_carrier_inventory.py
- Test: A2 positive: test_no_live_cot_explain_references.py::test_nested_worktree_produces_no_hits; negative: test_no_live_cot_explain_references.py::test_own_violation_still_reported. A6 positive: test_state_anchor_carrier_inventory.py::test_gitignored_dir_not_counted; boundary: test_check_plugin_boundaries.py::test_ignored_markdown_not_scanned.
- Risk: agent-decided — these three import a loom-code module across trees, following loom-design/scripts/spec/test_write_spec_contract.py:11-16.

**W2-03 Package tests skip nested worktrees**  after: W1-01  acceptance: 3
- Files: scripts/run_package_tests.py, scripts/test_run_package_tests.py
- Test: A3 positive: test_run_package_tests.py::test_nested_worktree_is_ignored; negative: test_run_package_tests.py::test_targets_unchanged_without_nested_worktree.
- Risk: agent-decided — adds --ignore from git worktree list rather than a root pytest.ini, which a bare root pytest run would also pick up.

## Questions asked
decision point ① — what — 範圍要 A（只修上次炸掉的那一支）／B（六支 repo 根掃描器 + pytest 收集）／C（連單一 plugin 子樹的十支也統一）？ → B
decision point ① — consequence — git archive 的退路要不要保留？保留則有 git／無 git 兩條路徑都要測、都要維護；不保留則 test_write_plan_station_text.py 在無 .git 的副本裡會失敗 → 保留
decision point ① — what — 共用機制放 loom-code／loom-workflow／repo 根 scripts/？ → loom-code 出貨樹內一份，六支全用；理由是使用者要的是給 loom 機制用、在採用 loom 的 repo 裡也生效，不只是本 repo 的開發工具
decision point ① — what — 要不要做成讓採用 repo 自己呼叫的公開介面？ → 不特意開放也不特意阻擋；不寫文件、不承諾穩定
decision point ① — done — 這些驗收條件可以嗎？ → 可以
closing review — consequence — 第 4 條驗收條件寫「六支掃描器在沒有 git 的副本裡都要跑出相同判定」，但其中一支（rehearse_probes）靠複製 repo 運作，沒有 git 就什麼都做不了——這條對它本質上不可能成立，是我當初寫太寬。怎麼處理？ → 兩個都做
closing review — consequence — 你確認的「不在範圍內」寫著「不改變任何掃描器對違規的判定」，但引用檢查的判定實際上兩個方向都變了：以前因重複而跳過的引用現在會被檢查、以前能解析的被忽略檔案現在變成不檢查。本 repo 實測 15 條引用、前後都是 0 個發現，但這個模組會裝到別人的 repo。怎麼處理？ → 修正措辭（推薦）
closing review — what — 確認修訂後的第 4 條驗收條件與「不在範圍內」措辭 → 可以
decision point ③ — done — 第 1 條驗收條件只在「採用 loom 的專案有把工作副本位置加進 gitignore」時成立；沒加的話，一道既有的「請先提交」檢查會擋住。你要怎麼處理這次改動？ → 接受，寫回文件再合併（推薦）
decision point ③ — what — 確認修訂後的第 1 條驗收條件與新增的限制 → 可以

## Risks
1. Only three of the six scanners walk from the repository root and reach a nested worktree today; the other three gain ignore-awareness within their own scope. Acceptance 2 holds trivially for those three.
2. check_doc_citations currently over-includes on purpose, arguing an extra candidate can only make a match ambiguous. Dropping ignored files can turn ambiguous matches unique and change its verdicts.
3. The module ships with loom-code, so its behaviour reaches every adopting repository. Reverting later is a plugin release, not a local edit.
4. Three consumers import a loom-code module from another tree. The precedent is test-only; a future packaging change that isolates plugin trees would break them.
5. A worktree nested inside a scanned subtree is excluded by git, but the fixed ignore list alone would not catch it if git is unavailable in the archive fallback path.
6. `git ls-files --others` emits a nested repository or linked worktree as one opaque directory entry, not its files. That is how its contents stay out, and also a crash source if handed to a file reader unfiltered.
7. Submodule contents are never listed: `--recurse-submodules` is documented as incompatible with `--others`. No consumer in scope scans a submodule, and the repository already recorded this limitation.
8. The no-git fallback deliberately does not honour a `.gitignore` that is present. ripgrep, fd and ruff behave the same way by default; a reader expecting the file to be honoured would find this surprising.
