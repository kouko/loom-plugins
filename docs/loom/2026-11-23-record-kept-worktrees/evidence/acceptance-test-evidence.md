# Record kept worktrees so sweep never removes them — acceptance test evidence

Tried on 2026-11-23, in a clean copy of the project at 2e024f7a.

## Setup

- Clean copy: `git worktree add <scratch>/at-wt 2e024f7a` (detached HEAD, nothing
  else in it). Baseline for Acceptance 4: `git worktree add <scratch>/at-main main`
  (5ee4814f, the merge base of this branch).
- Setup check: `python3 loom-code/scripts/loom_checker.py land --help` with the
  machine's plain `python3` fails with `ModuleNotFoundError: No module named 'yaml'`.
  This is pre-existing (the intent lists "PyYAML 底層 Python" as a separate pending
  item) and not caused by this change. With the project's locked environment
  (`UV_PYTHON=.../envs/dbt-redshift/bin/python uv run --isolated
  --with-requirements requirements-package-tests.lock python
  loom-code/scripts/loom_checker.py land --help`) the help prints, exit 0, and
  contains the new paragraph: "The keep form records the keep, so a later sweep
  shows that change on a kept line it never removes; land --cleanup <branch>
  removes a kept change and its record."
- Harness, same shape as the repo's own land tests
  (`loom-code/tests/test_land_cleanup.py`, `test_land_sweep.py`): throwaway
  repositories built by `<scratch>/drv/setup.py` — a bare `origin.git`, a main
  checkout `repo` on `main`, and one linked worktree per change, each pushed and
  listed as a merged PR. Each `land` call runs through `<scratch>/drv/driver.py`
  **as its own Python process** (a new "session": no memory shared between calls
  except what is on disk in the repository). Real: git, worktrees, refs, pushes,
  `cmd_land`, `_merged_prs`, `plan_cleanup`, `execute_cleanup`, `_sweep_list`.
  Stubbed: `gh` answers (from `prs.json`), the GitHub-origin identity check
  (`_cleanup_context`, since origin is a local bare repo), and for
  `--accepted-by` the remote merge stages `_merge_preconditions`,
  `_squash_merge`, `_verify_merge` — the same seams the repo's land tests stub.
  Scenario script: `<scratch>/drv/scenario.sh`; `$R` below is its run directory.

## 1. 用 `--keep-worktree` 合併後，在一個完全不知道先前對話的新 session 裡，loom 能指出這個變更是被刻意保留的。
- How I tried it: session 1 (process 1) ran `land --accepted-by kouko --keep-worktree`
  from inside `$R/wt-keep`; session 2 did the same for `feat/dirty`. Then separate
  fresh processes ran `land --sweep` from the main checkout (session 4), from inside
  the kept worktree `wt-keep` (session 5), and from inside the dirty kept worktree
  `wt-dirty` (session 6).
- What came back:
  ```
  $ land --accepted-by kouko --keep-worktree   (cwd=$R/wt-keep)
  Merged PR #1 as eddb60c
  Trunk main fast-forwarded to e31e84b
  Kept worktree $R/wt-keep on branch feat/keep; remove it later with: land --cleanup feat/keep
  [exit 0]
  $ git -C $R/repo config --show-origin --get-regexp loomKept
  file:.git/config  branch.feat/keep.loomkept 2026-11-23
  file:.git/config  branch.feat/dirty.loomkept 2026-11-23
  $ git -C $R/wt-keep status --porcelain --ignored
  (empty — the record is not in the kept worktree)
  $ land --sweep   (cwd=$R/repo)            # session 4, fresh process
  kept feat/dirty — worktree $R/wt-dirty has modified files; remove with: land --cleanup feat/dirty
  kept feat/keep — worktree $R/wt-keep; remove with: land --cleanup feat/keep
  remove feat/plain 8796af8 — worktree $R/wt-plain, local, remote
  confirm with: land --sweep --confirm f40ae61416d5
  [exit 0]
  ```
  Session 5 (cwd `$R/wt-keep`) and session 6 (cwd `$R/wt-dirty`) printed the
  identical four lines and the same token: the kept branch is shown `kept` even
  when sweep runs inside it (an unkept branch there prints
  `skip <branch> — current working directory`, see §4).
- Evidence: scenario output above; tests `test_keep_worktree_flag_keeps_all_then_cleanup_removes_all`,
  `test_sweep_marks_invoking_kept_worktree_kept`,
  `test_sweep_kept_branch_checked_out_in_main_marks_kept`,
  `test_keep_land_config_lock_held_exits_nonzero` passed (see "Tests run").

## 2. 批次清理的清單會把保留的變更另外列出並標明是保留的；確認批次清理後，保留的變更（worktree、本機分支、遠端分支）都還在。
- How I tried it: mixed listing (two kept — one clean, one with a modified tracked
  file and an untracked `notes.txt` — plus one unkept `feat/plain`), then
  `land --sweep --confirm <token>` with the printed token (session 7), then checked
  worktrees, local refs, origin refs and the kept worktree's files, then swept again
  (session 8).
- What came back:
  ```
  $ land --sweep --confirm f40ae61416d5   (cwd=$R/repo)
  Removed worktree $R/wt-plain
  Deleted local branch feat/plain
  Deleted remote branch feat/plain
  next: cd '$R/repo'
  [exit 0]
  $ git worktree list
  $R/repo      e31e84b [main]
  $R/wt-dirty  86ff65b [feat/dirty]
  $R/wt-keep   7e28eba [feat/keep]
  feat/keep        local=yes remote=yes record=2026-11-23
  feat/dirty       local=yes remote=yes record=2026-11-23
  feat/plain       local=no remote=no record=none
  $ ls $R/wt-dirty ; cat wt-dirty.txt   ->  file.txt notes.txt wt-dirty.txt / "feat/dirty\nedited"
  $ land --sweep                          # session 8
  kept feat/dirty — worktree $R/wt-dirty has modified files; remove with: land --cleanup feat/dirty
  kept feat/keep — worktree $R/wt-keep; remove with: land --cleanup feat/keep
  No merged changes to clean up
  ```
  The token covers only `remove` lines, so with only kept changes left no token is
  printed and nothing can be confirmed.
- Evidence: scenario output above; test `test_sweep_lists_kept_apart_and_confirm_spares_it` passed.

## 3. 維護者明確要求清理某個保留的變更時，用 loom 既有的清理方式可以把它清掉，而且清完之後不再留有它的保留紀錄。
- How I tried it: session 9 `land --cleanup feat/keep` from the main checkout, then
  checked refs, the directory and every `branch.feat/keep.*` config key; session 10
  `land --cleanup feat/dirty` (kept, with unsaved work); session 11 sweep.
- What came back:
  ```
  $ land --cleanup feat/keep   (cwd=$R/repo)
  Worktree for feat/keep: $R/wt-keep
  Removed worktree $R/wt-keep
  Deleted local branch feat/keep
  Deleted remote branch feat/keep
  next: cd '$R/repo'
  [exit 0]
  feat/keep  local=no remote=no record=none
  ls $R/wt-keep -> No such file or directory
  git config --get-regexp 'branch\.feat/keep' -> (nothing)
  $ land --cleanup feat/dirty
  BLOCK land.cleanup: worktree $R/wt-dirty has modified files
  [exit 1]
  feat/dirty local=yes remote=yes record=2026-11-23
  $ land --sweep                          # session 11
  kept feat/dirty — worktree $R/wt-dirty has modified files; remove with: land --cleanup feat/dirty
  No merged changes to clean up
  ```
  A clean kept change is fully removed with its record. A kept change with unsaved
  work is refused exactly like an unkept one with unsaved work (§4 shows the
  same refusal on main's code); nothing is deleted and its record stays.
- Evidence: scenario output above; tests
  `test_keep_worktree_flag_keeps_all_then_cleanup_removes_all` and
  `test_cleanup_without_local_branch_clears_record` passed.

## 4. 沒有用 `--keep-worktree` 合併的變更，批次清理和清理的行為與現在相同。
- How I tried it: `<scratch>/drv/unkept.sh` — one scenario with no keep at all: plain
  `land --accepted-by kouko` (no keep), named `land --cleanup` of a clean change,
  named cleanup of a change with an untracked file, `land --sweep` from the main
  checkout and from inside an unkept change's worktree, `--sweep --confirm`, then
  the final worktrees, local/origin refs and `branch.*` config. Ran it once against
  `main` (5ee4814f, before this change) and once against 2e024f7a, same run
  directory, fixed `GIT_AUTHOR_DATE`/`GIT_COMMITTER_DATE` so commit ids and tokens
  match, sequentially.
- What came back: `diff -s unkept-main.txt unkept-head.txt` →
  `Files ... are identical`. Key lines (both runs):
  ```
  skip feat/dirtyplain — worktree $RUN/wt-dirtyplain has untracked files
  remove feat/plain 9886822 — worktree $RUN/wt-plain, local, remote
  confirm with: land --sweep --confirm d4aa0255277a
  (from wt-plain) skip feat/plain — current working directory
  BLOCK land.cleanup: worktree $RUN/wt-dirtyplain has untracked files
  ```
  Also seen in the main scenario: the unkept `land --accepted-by kouko` of
  `feat/landplain` removed its worktree, local and remote branch, no record written.
- Not visible in output: on HEAD, `land --cleanup` now removes the
  `branch.<branch>` config section even when no local branch exists
  (`land.py` `execute_cleanup`, the `--remove-section` call moved out of the
  `if plan.local` block). Before, it ran only after deleting the local branch,
  which already drops that section in git, so the outcome differs only when a
  config section outlived its local branch.
- Evidence: `<scratch>/unkept-main.txt`, `<scratch>/unkept-head.txt` (identical);
  test `test_sweep_lists_kept_apart_and_confirm_spares_it` (unkept half) and the
  pre-existing sweep/cleanup tests in the two files passed.

## 5. 照 ship 的流程文字，agent 只清理沒有保留紀錄的已合併變更；分不出是否保留時，先問維護者，不會自行清理。
- How I tried it: read `loom-code/skills/ship/SKILL.md` §5 (lines 307-355) and
  `land --help` in the clean copy; then gave a fresh-context agent (sonnet, no
  other context, told not to run anything) only that §5 text and the mixed sweep
  listing (two `kept`, two `remove`) and asked what it would clean without asking,
  what it does with kept lines, and what it runs after the maintainer's yes.
- What came back: §5 lines 349-355: "For merged changes left from earlier work, run
  `land --sweep` ... Leave every change on a `kept` line alone ... Clean any other
  listed change — `land --cleanup <branch>` for one, or pass
  `--sweep --confirm <token>` — only after the maintainer answers yes to the
  printed list, never on your own judgement." The text no longer lets the agent
  clean any earlier-work change alone, recorded or not; a 3.88.0-era keep without a
  record shows as a `remove` line and so also waits for the maintainer's yes.
  `land --help`: "Removable sweep listings ... review the list and obtain approval
  before deliberately using its token. Listing is not consent." Cold-reader result:
  see "Cold reader" below.
- Evidence: SKILL.md:349-355 at 2e024f7a; test file
  `loom-code/tests/test_ship_station_text.py` passed.

## Cold reader (Acceptance 5)

Fresh-context sonnet agent, given only ship SKILL.md §5 and this listing:
`kept feat/dirty …`, `kept feat/keep …`, `remove feat/plain …`, `remove feat/old …`,
`confirm with: land --sweep --confirm f40ae61416d5`; maintainer silent.

- Cleans now without asking: "none" (cites 353-355 "only after the maintainer
  answers yes ... never on your own judgement").
- `kept` lines: leaves both alone, shows them to the maintainer (cites 350-352).
- `remove` lines (including `feat/old`, which it knows nothing about): asks first.
- After "yes, clean the listed ones": `land --sweep --confirm f40ae61416d5`, or one
  `land --cleanup` per `remove` line; neither targets a kept change.
- Ambiguity it raised: "yes to the printed list" — the printed list includes the
  `kept` lines, and the text does not say outright that `--confirm` skips them. It
  resolved this from line 352. The tool side settles it regardless: session 7 above
  shows a confirmed sweep never removes a kept change.

## Tests run (criterion tests only, not the package suite)

```
UV_PYTHON=/usr/local/Caskroom/miniconda/base/envs/dbt-redshift/bin/python \
  uv run --isolated --with-requirements requirements-package-tests.lock \
  python -m pytest loom-code/tests/test_land_sweep.py \
  loom-code/tests/test_land_cleanup.py loom-code/tests/test_ship_station_text.py -q
51 passed in 90.72s
```

The full package suite (`scripts/run_package_tests.py --loom-family`) was not run
here; finalize-review runs it and refuses the attestation when it fails.
