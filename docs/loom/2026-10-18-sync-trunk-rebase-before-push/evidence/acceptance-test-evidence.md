# sync-trunk rebases a change branch that has never been pushed — acceptance test evidence

Tried on 2026-10-19, in a clean copy of the project at 50799c24, and re-run after a fix at 7ea44a94 (see "Re-run on 2026-10-19, at 7ea44a94" at the end). First run: (`git worktree add --detach <scratch>/at-clean 50799c24`; `git status --short` empty). The pre-change behaviour was measured from a second clean copy at the branch base ba092534 (`<scratch>/at-base`).

## Setup

- The checker needs no install step: `python3 loom-code/scripts/loom_checker.py --list-rules` printed the rule list from the clean copy, and `python3 loom-code/scripts/loom_checker.py sync-trunk extra` printed `sync-trunk takes no arguments; run it from the change worktree.` (exit 2). Setup works.
- Every scenario is a fresh set of real git repositories in the scratch directory: a bare `origin.git` whose default branch is `trunk`, a clone `me` (the change worktree, where the checker runs) and a clone `other` (someone else pushing to trunk). Clones get `origin/HEAD -> origin/trunk`, which is how the checker names the trunk.
- The trunk is called `trunk`, not `main`: this machine's command guard refuses any command line that pushes to `main`, and the scratch scenarios must push trunk commits from `other`. The checker resolves the trunk from `origin/HEAD` either way (`command_handlers/sync.py:71-84`).
- The user's own global git config was left in effect: `pull.rebase=true`, `rebase.autostash=true`, `rebase.updaterefs=true`, `rebase.autosquash=true`, `push.autosetupremote=true`, `merge.autostash=true`, `merge.conflictstyle=zdiff3`, `rerere.enabled=true`.
- Fixed `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE`, so equal scenarios produce equal commit ids across runs and versions.
- Scenario scripts: `<scratch>/lib.sh`, `a1.sh`, `a2.sh`, `a3.sh`, `a4.sh`, `extra.sh`; their full logs `a1.log` … `extra.log` (scratch is `/private/tmp/claude-501/-Users-kouko--herdr-worktrees-loom-plugins-fix-codex-review/4b6eb79e-1676-4024-aba6-69e57382f069/scratchpad`, not committed).

## 1. On a never-pushed change branch that is behind trunk with no conflict, `sync-trunk` leaves the branch's own commits sitting directly on the trunk tip with no merge commit, and reports that content changed.

- How I tried it: two variants — branch started from `origin/trunk` (so git records `origin/trunk` as its upstream) and branch started from local `trunk` (no upstream). Two own commits (`feat: add c`, `feat: add d`); `other` pushes `trunk: change b`; then `python3 <clean>/loom-code/scripts/loom_checker.py sync-trunk` in `me`.
- What came back (both variants identical):

```
sync-trunk: rebased feat onto origin/trunk (cbbacebd44f7ee77a7c6ab9648296faa4a12d6ff); HEAD is now b247dc7e85fbe2cc283c065f5d7914efe60b60ae.
sync-trunk: content changed -- re-run the package suite and adversarial programs before dispatching reviewers.
exit=0
* b247dc7 e1f3286 feat: add d
* e1f3286 cbbaceb feat: add c
* cbbaceb 9247056 trunk: change b (by someone else)
* 9247056  trunk: initial
merge commits in branch: 0
first own commit's parent: cbbaceb ; trunk tip: cbbaceb
worktree status: []; rebase in progress: no
```

- Extra (X3, `extra.log`): with the user's `rebase.autosquash=true`, a `fixup! feat: add c` commit stayed a separate commit after the sync — the user's rebase settings did not leak in.
- Note: after the rebase `.git/AUTO_MERGE` and an empty `.git/MERGE_RR` remain; a manual `git rebase --merge origin/trunk` in an identical repo leaves the same two files (git's own bookkeeping, `rerere.enabled=true`); `git status` is clean and `git rebase --continue` says `no rebase in progress`.
- Evidence: `a1.log`; tests `test_unpushed_behind_rebases_linear`, `test_sync_ignoredhistory_succeeds`, `test_sync_oldgit_succeeds` passed (see "Tests run"); the last one was folded into `test_rebase_failing_without_conflict_falls_back_to_merge[old-git-no-update-refs]` by the fix.

## 2. On a change branch that has already been pushed and is behind trunk, `sync-trunk` merges as today: the pushed commits are still in the branch unchanged, and the next non-forced publish of the branch is accepted by the remote.

- How I tried it: variant `pushed-all` — two commits, `git push origin feat`, trunk advances, sync, then plain `git push origin feat` (no `--force`). Variant `pushed-then-more` — same, plus one more local commit after the push. Variant X2 (`extra.log`) — the branch was pushed from the *other* clone; `me` never pushed it and has no `origin/feat` in its local view.
- What came back (`pushed-then-more`; `pushed-all` is the same without commit `ac54bb8`):

```
sync-trunk: merged origin/trunk (cbbacebd44f7ee77a7c6ab9648296faa4a12d6ff) into feat; HEAD is now ab6346448c7363c9ab7cafb7a390cf31d2ba418d.
sync-trunk: content changed -- re-run the package suite and adversarial programs before dispatching reviewers.
exit=0
*   ab63464 Merge origin/trunk into feat
|\
| * cbbaceb trunk: change b (by someone else)
* | ac54bb8 feat: add e (not yet pushed)
* | 8052b49 feat: add d
* | caec8d0 feat: add c
|/
* 9247056 trunk: initial
pushed caec8d08595521801ed26bbcb937f4030cf12c95 is still in the branch with the same id
pushed 8052b498b2ef0b95f884aa517672dd5c6ba4d21b is still in the branch with the same id
$ git push origin feat   (plain, no --force)
   8052b49..ab63464  feat -> feat
push exit=0
remote feat: ab6346448c7363c9ab7cafb7a390cf31d2ba418d ; local HEAD: ab6346448c7363c9ab7cafb7a390cf31d2ba418d
```

- X2: `local view of remote feat: []` and the checker still merged (`Merge origin/trunk into feat`), and the plain push was accepted (`caec8d0..06c1528  feat -> feat`, exit 0).
- Evidence: `a2.log`, `extra.log`; tests `test_pushed_behind_merges_then_plain_push_accepted`, `test_commits_pushed_under_other_name_merge`, `test_branch_with_configured_upstream_merges`, `test_sync_otherremote_keepscommits` passed.

## 3. When replaying a never-pushed branch would conflict, `sync-trunk` names the conflicting paths and leaves the branch, its commits and the working tree exactly as they were before the command.

- How I tried it: a never-pushed branch with an ignored private file `notes.local` (via `.git/info/exclude`). Snapshot before and after: HEAD, branch name, every own commit id, `git status --porcelain --ignored --untracked-files=all`, the contents of `a.txt` and `notes.local`, `git stash list`, and whether a rebase/merge is in progress. Variant 1: the branch as a whole changes line 2 of `a.txt`, trunk changes the same line. Variant 2: only replaying conflicts — one own commit changes line 2, a later one changes it back, trunk changes line 2.
- What came back:

```
# variant 1 (whole-branch conflict)
BLOCK review.sync: conflict: a.txt
BLOCK review.sync: the merge was not attempted; feat is still at 55953d7bfbe22369aab02e57273eadeb46642a44 and the worktree is untouched.
BLOCK review.sync: Conflicts are never resolved automatically -- resolve them in a new build round.
exit=1
-- before/after snapshot diff: (identical)

# variant 2 (replay-only conflict)
BLOCK review.sync: conflict: a.txt
BLOCK review.sync: the rebase was aborted; feat is back at 496b95abbf69f176ac7b559f8da399acd6dbb6da with a clean worktree. Conflicts are never resolved automatically -- resolve them in a new build round.
exit=1
-- before/after snapshot diff: (identical)
```

- Both after-snapshots show the same three (resp. two) own commit ids, `!! notes.local` with `my private notes`, empty stash list, `no operation in progress`.
- Comparison X1 (`extra.log`): the same variant-2 repository with the checker from before the change merged successfully (`merged origin/trunk ... into feat`, exit 0). Raised under "Things I am not sure you want" in the report.
- Wording: in variant 1 the message says "the merge was not attempted" although on this never-pushed branch a rebase would have been the step; recorded as a nit finding.
- Evidence: `a3.log`, `<scratch>/a3-*.before|after`; tests `test_unpushed_conflict_names_paths_restores`, `test_conflict_names_every_file_and_restores_head` passed.

## 4. Every other `sync-trunk` outcome (already up to date, warnings, refusals) is unchanged, and the complete package suite passes.

- How I tried it: for each case, built the same repository twice and ran the checker from before the change (ba092534) and after it (50799c24); compared stdout+stderr, exit code, HEAD and `git status --porcelain --ignored` byte for byte (`a4.sh`).
- What came back — all 12 identical:

| case | output (new version) |
|---|---|
| up_to_date | `sync-trunk: up to date -- feat (...) already contains origin/trunk (...); no commit added.` exit 0 |
| ahead_only | same "up to date" line, exit 0 |
| pushed_up_to_date | same "up to date" line, exit 0 |
| dirty_tree | `BLOCK review.sync: the worktree has uncommitted or untracked changes (c.txt); commit or remove them first.` exit 1 |
| untracked_file | same BLOCK naming `scratch.txt`, exit 1 |
| detached | `BLOCK review.sync: HEAD is detached; switch to the change branch before syncing.` exit 1 |
| on_trunk | `BLOCK review.sync: HEAD is the trunk branch 'trunk'; sync runs on a change branch, never the trunk.` exit 1 |
| fetch_fails | `WARN review.sync: could not fetch origin/trunk, ... continuing without syncing.` exit 0 |
| ignored_collision | `BLOCK ... ignored or untracked path new.cfg collides with a path origin/trunk tracks; ...` + `the merge was not attempted; ...` exit 1, `!! new.cfg` kept |
| conflict_unpushed | `BLOCK review.sync: conflict: a.txt` + not attempted + never resolved, exit 1 |
| conflict_pushed | same as conflict_unpushed |
| extra_argument | `sync-trunk takes no arguments; run it from the change worktree.` exit 2 |

- A first run of this comparison showed one difference (`on_trunk`, worktree `D a.txt; D b.txt`); it came from my script deleting the directory it stood in, so a clone's checkout failed. Fixed the script (`cd $S` before rebuilding) and re-ran; all 12 identical, no clone errors in `a4.log`.
- Package suite: not run here. It is executed by finalize-review, which refuses the attestation when it fails. Suite command: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- Evidence: `a4.log`, `<scratch>/a4-<case>.OLD|NEW`; tests listed below passed.

## Tests run (only those covering these criteria)

```
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
  python -m pytest loom-code/tests/test_sync_trunk.py loom-code/tests/test_adversarial_sync_trunk_rebase.py \
  "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized" -q -p no:cacheprovider
33 passed in 36.80s
```

Included: test_current_branch_adds_no_commit, test_branch_ahead_of_trunk_adds_no_commit, test_behind_branch_merges_fetched_trunk_tip_and_says_content_changed, test_unpushed_behind_rebases_linear, test_pushed_behind_merges_then_plain_push_accepted, test_commits_pushed_under_other_name_merge, test_branch_with_configured_upstream_merges, test_unpushed_conflict_names_paths_restores, test_rebase_failing_without_conflict_falls_back_to_merge, test_unpushed_with_prior_merge_commit_merges, test_trunk_name_resolves_without_origin_head, test_conflict_names_every_file_and_restores_head, test_ref_named_origin_trunk_does_not_shadow_fetched_tip (4), test_ignored_file_trunk_starts_tracking_is_refused_and_kept, test_untracked_collision_check_failure_blocks_before_merge (2), test_control_character_conflict_path_cannot_forge_a_block_line, test_merge_tree_unavailable_falls_back_to_merge_then_abort, test_merge_ff_only_config_does_not_block_clean_merge, test_dirty_worktree_or_trunk_checkout_refused_untouched (4), test_control_character_untracked_path_cannot_forge_a_warn_line, test_unreachable_remote_warns_exit_zero, test_unreachable_remote_creates_no_commit, test_sync_ignoredhistory_succeeds, test_sync_oldgit_succeeds, test_sync_otherremote_keepscommits, test_current_release_metadata_is_synchronized. The clean copy's `git status --short` stayed empty afterwards.

## Re-run on 2026-10-19, at 7ea44a94

Fix range 89802d0d..7ea44a94: (1) a never-pushed branch whose own commits touch a path that exists locally as an ignored or untracked file takes the merge path (`command_handlers/sync.py` `_history_touches_local`, called last in `_may_rebase`); (2) after a rebase, one extra output line says commit ids changed and commit-sha references must be re-pinned; (3) test folding, CHANGELOG and plan wording.

Setup, re-checked: fresh `git worktree add --detach <scratch>/at-clean 7ea44a94` (`git status --short` empty); `--list-rules` printed the rule list; `sync-trunk extra` printed `sync-trunk takes no arguments; run it from the change worktree.` exit 2. Also `<scratch>/at-base` (ba092534, before the change) and `<scratch>/at-prefix` (89802d0d, before the fix). Same user global git config as the first run (git 2.54.0). Scripts `r2-a1.sh`, `r2-extra.sh` (new), `a3.sh`, `a4.sh` (unchanged, now pointing at 7ea44a94); logs `r2-a1.log`, `r2-extra.log`, `r2-a3.log`, `r2-a4.log`.

- 1: re-tested — every surface of the line (own commits directly on the trunk tip, zero merge commits, "content changed" reported):
  - Both first-run variants (branch from `origin/trunk`, branch from local `trunk`): same linear graph and same ids as the first run (`b247dc7` on `e1f3286` on trunk tip `cbbaceb`), merge commits 0, clean worktree, no rebase in progress. Output is now three lines, the new one between the two old ones:

    ```
    sync-trunk: rebased feat onto origin/trunk (cbbacebd44f7ee77a7c6ab9648296faa4a12d6ff); HEAD is now b247dc7e85fbe2cc283c065f5d7914efe60b60ae.
    sync-trunk: the branch's commit ids changed -- re-pin any commit-sha reference recorded on this branch (for example a plan's intent: line).
    sync-trunk: content changed -- re-run the package suite and adversarial programs before dispatching reviewers.
    exit=0
    ```
  - Ignored local `.env` the branch never touched (branch only adds `.gitignore` with `.env`): still rebased, merge commits 0, `.env` still `SECRET=keep-me`, `!! .env`. The new guard does not over-trigger on an ignored file outside the branch's history.
  - The `.env` scenario with a real local ignored file: branch commits `.gitignore` (`.env`), force-adds `.env` (`git add -f`), then `git rm --cached .env` and commits, then `feat: add c`; local `.env` = `SECRET=hunter2`, status `!! .env`; trunk advances.
    - Before the fix (89802d0d): `rebased feat onto origin/trunk ...`, exit 0, and afterwards `cat: .env: No such file or directory`, status empty — the replay deleted the user's file.
    - After the fix (7ea44a94): `merged origin/trunk (cbbaceb...) into feat; HEAD is now ddc79b3...`, `content changed`, exit 0, no re-pin line; merge commits 1; `.env` still `SECRET=hunter2`, `!! .env`; no operation in progress.
    - Pre-change version (ba092534) on the same repository: byte-identical output, exit, HEAD and status to the fixed version (`r2y1.OLD` vs `r2y1.NEW`).
  - Verdict stays works: a branch whose history touches a local ignored file is a deliberate exception that merges to protect the file (listed as a decision in the report).
  - Tests: `test_unpushed_behind_rebases_linear`, `test_unpushed_branch_touching_local_ignored_file_merges_and_keeps_it`, `test_sync_ignoredhistory_succeeds`, `test_rebase_failing_without_conflict_falls_back_to_merge[not-a-conflict|old-git-no-update-refs]` passed.
- 2: carried over — the fix's new condition runs inside `_may_rebase` only after every pushed check has already answered "merge", and the new output line is written only on the rebase branch of `cmd_sync_trunk`; the merge path and its output are untouched by 89802d0d..7ea44a94. Its tests (`test_pushed_behind_merges_then_plain_push_accepted`, `test_commits_pushed_under_other_name_merge`, `test_branch_with_configured_upstream_merges`, `test_sync_otherremote_keepscommits`) passed again at 7ea44a94.
- 3: re-tested — the fix changes which path a never-pushed branch takes, so both first-run variants were re-run in full (named paths, HEAD, every own commit id, `git status --porcelain --ignored --untracked-files=all`, `a.txt` and ignored `notes.local` contents, stash list, operation in progress). Whole-branch conflict: `conflict: a.txt`, "the merge was not attempted", exit 1, snapshots identical. Replay-only conflict: `conflict: a.txt`, "the rebase was aborted; feat is back at 496b95a...", exit 1, snapshots identical. New variant Y2 (`r2-extra.log`): the `.env` branch plus a line-2 conflict with trunk: `conflict: a.txt`, "the merge was not attempted; feat is still at fdc7490...", exit 1; HEAD, all four own commit ids, `.env` = `SECRET=hunter2`, `!! .env` and empty stash identical before and after; no operation in progress. Tests `test_unpushed_conflict_names_paths_restores`, `test_conflict_names_every_file_and_restores_head` passed.
- 4: re-tested — `a4.sh` re-run: all 12 cases (up_to_date, ahead_only, pushed_up_to_date, dirty_tree, untracked_file, detached, on_trunk, fetch_fails, ignored_collision, conflict_unpushed, conflict_pushed, extra_argument) give byte-identical output, exit code, HEAD and `git status --porcelain --ignored` between ba092534 and 7ea44a94. Plus Y1 above (`.env` branch, now merge) identical to the pre-change version. Package suite: not run here; finalize-review executes it and refuses the attestation when it fails. Suite command: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

Tests run at 7ea44a94 (only those covering these criteria), in `<scratch>/at-clean`:

```
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
  python -m pytest loom-code/tests/test_sync_trunk.py loom-code/tests/test_adversarial_sync_trunk_rebase.py \
  "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized" -q -p no:cacheprovider
34 passed in 36.84s
```

The 33 of the first run, minus `test_sync_oldgit_succeeds`, plus its replacement case `test_rebase_failing_without_conflict_falls_back_to_merge[old-git-no-update-refs]` (the old single case is now `[not-a-conflict]`) and the new `test_unpushed_branch_touching_local_ignored_file_merges_and_keeps_it`: 33 - 1 + 1 + 1 = 34. The clean copy's `git status --short` stayed empty afterwards.
