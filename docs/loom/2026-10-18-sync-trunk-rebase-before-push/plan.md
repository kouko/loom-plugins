# sync-trunk rebases a change branch that has never been pushed — plan
intent: 2026-10-18-sync-trunk-rebase-before-push@ee62f5ce
charter: 1.1

## Current State Evidence
- Forward: `loom-code/scripts/loom_checker/command_handlers/sync.py` `cmd_sync_trunk` merges the fetched trunk tip with `git merge --ff --no-edit -m "Merge origin/<trunk> into <branch>"`.
- Reverse: build/SKILL.md §3 step 1 and closing-review/SKILL.md §2 read only `up to date`, `content changed`, `WARN review.sync`, `BLOCK review.sync`; neither names merge.
- Error: conflicts are found by `_preflight_conflicts` (merge-tree) or by merge-then-`merge --abort`, then HEAD and a `--ignored` status snapshot prove the restore.
- Data: the module docstring states "Merge only -- never rebase, never force"; `loom-code/tests/test_sync_trunk.py` holds 15 tests, none with a pushed change branch.
- Boundary: refusals (detached HEAD, trunk checkout, dirty tree), fetch-failure WARN and untracked-collision BLOCK run before any history change.

## Task DAG
Wave 1 — one module boundary (`cmd_sync_trunk`), then release metadata.

**W1-01 Rebase a never-pushed branch, merge a pushed one**  after: none  acceptance: 1, 2, 3, 4
- Files: loom-code/scripts/loom_checker/command_handlers/sync.py (entry: `cmd_sync_trunk`), loom-code/tests/test_sync_trunk.py
- Test: A1 positive: unpushed_behind_rebases_linear; negative: test_current_branch_adds_no_commit. A2 positive: pushed_behind_merges_then_plain_push_accepted; boundary: commits_pushed_under_other_name_merge. A3 positive: unpushed_conflict_names_paths_restores; negative: unpushed_with_prior_merge_commit_merges. A4 positive: test_branch_ahead_of_trunk_adds_no_commit; negative: test_dirty_worktree_or_trunk_checkout_refused_untouched.
- Risk: agent-decided: pushed = origin lists branch, a branch commit on any remote-tracking ref, or an upstream/pushRemote other than origin's trunk; a merge commit, a local ignored/untracked path the branch touches, or failed lookup also merges. Collision guard runs first.

**W1-02 Release 3.42.1**  after: W1-01  acceptance: 4
- Files: loom-code/plugin.json (+ .claude-plugin, .codex-plugin copies), loom-code/package.json, loom-code/CHANGELOG.md, README.md, loom-code/README.md (+ ja, zh-TW), loom-code/tests/test_write_plan_station_text.py
- Test: A4 positive: test_current_release_metadata_is_synchronized at 3.42.1; negative: same test fails if any manifest stays 3.42.0.
- Risk: agent-decided patch bump: no station guidance, field, rule id or manifest change; pin test rewrite and CHANGELOG entry are deliverables.

**W1-03 Graduate the adversarial programs into the suite**  after: W1-01  acceptance: 1, 2
- Files: loom-code/tests/test_adversarial_sync_trunk_rebase.py, docs/loom/2026-10-18-sync-trunk-rebase-before-push/evidence/probes/
- Test: A1 positive: test_sync_ignoredhistory_succeeds; boundary: test_rebase_failing_without_conflict_falls_back_to_merge[old-git-no-update-refs]. A2 positive: test_sync_otherremote_keepscommits; negative: test_branch_with_configured_upstream_merges.
- Risk: agent-decided: move the three red-then-green probes unchanged in behaviour so every later change runs them; the probe store keeps no copy.

## Simplicity check
- reuse existing up-to-date, refusal and fetch-failure tests instead of four new duplicates — taken

## Questions asked
① — what — 「這樣對嗎？」 (restated intent incl. automatic publication; answered after the rebase/force-push discussion with 「先做 A，之後再看」)
① — consequence — rebase gives the unpushed commits new ids, the old ones stay in the reflog, a conflict changes nothing (no fork)

## Risks
1. Rebase rewrites local commits; abort on any failure and prove HEAD plus status snapshot restored, as the merge path does today.
2. A stale local remote-tracking view could miss a push from another clone; the live remote branch lookup covers it, and failure falls back to merge.
3. Complexity check returned PROCEED-WITH-CAVEAT: about +50 code and +100 test lines, no deletions; the user chose this over the zero-line status quo.
