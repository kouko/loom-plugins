# Keep the worktree when landing an accepted change — acceptance test evidence

Tried on 2026-11-23, in a clean copy of the project at cf7051a7.

## Re-run after trunk merge (863e5231..cf7051a7)

- Change since the last run: cf23dd5e (attestation only) and merge cf7051a7
  of origin/main fbb0e260 (#172/#174/#175/#176: docs, loom-workflow herdr
  skill, README sync; version-metadata conflicts resolved keeping loom-code
  3.88.0).
- `git diff --stat 863e5231 cf7051a7 -- loom-code/scripts loom-code/skills/ship
  loom-code/tests/test_land_cleanup.py loom-code/tests/test_land_merge.py
  loom-code/tests/test_ship_station_text.py loom-code/tests/test_loom_checker_cli.py`
  -> only `loom-code/scripts/check_mechanisms.py` (skill budget 27 -> 28 for
  loom-herdr). `land.py`, `loom_checker.py`, `ship/SKILL.md` and the
  land/ship/CLI tests are byte-identical to 863e5231.
- Every row was re-tested in full anyway, as the station asked.
- Clean copy: `git worktree add --detach <scratch>/at-merge cf7051a7` (no
  uncommitted files; removed with `git worktree remove` afterwards).
- Setup check at cf7051a7: `loom-code/scripts/loom-python --ready land
  --cleanup feat/x --keep-worktree` -> `land: --keep-worktree applies only to
  --accepted-by`, exit 2; `land --help` exit 0 with
  `Usage: land --accepted-by <name> [--keep-worktree]`, "When worktree
  preservation was requested, pass --keep-worktree to the accepted form and
  do not run cleanup.", and no "Do not run cleanup when worktree preservation
  was requested."
- Driver: rewritten in scratch (the earlier one was not kept) to the same
  outline as the appendix, run as
  `uv run ... python -I drive_keep.py <clean-copy> <scratch-base>`;
  `land module:` printed the clean copy's `land.py`. Results:
  - Row 1 (Scenario B): rc 0; stdout `Merged PR #7 as a1b2c3d` /
    `Trunk main fast-forwarded to 8826dae` / `Kept worktree .../B-keep-real/wt-x
    on branch feat/x; remove it later with: land --cleanup feat/x`; stderr
    `''`; cwd after = wt-x; worktree dir, local branch, remote branch all
    True; checked-out branch `feat/x`; HEAD, status, uncommitted edit and
    untracked file all unchanged; remove/push/update-ref git calls `[]`.
    Ship text re-read at cf7051a7: :311, :327-328, :331-335, :337-341,
    :349-351 read word for word as quoted under rows 1 and 5 below.
  - Row 2 (Scenario A, plain vs keep, `_land_accepted` keep kw
    `[False]`/`[True]`): happy, failing check, invalid PR body and foreign
    name each give identical rc/stdout/stderr/`Accepted-by:`/call order in
    both modes. Happy: `Accepted-by: kouko 2026-11-23` both; call order
    `repo view, api, pr view, pr checks, pr view, pr view, pr merge, pr view,
    fetch origin, cat-file commit`. Failing check: rc 1, `BLOCK land.merge:
    check lint: FAILURE; next: Inspect the named CI logs, fix the failure and
    rerun checks before retrying.`, merged False. Invalid body: rc 1,
    `BLOCK land.merge: PR body heading "Summary" is not one of the nine
    contextual headings; ...`, merged False. Foreign name: rc 1,
    `BLOCK land.merge: acceptance not recorded; ...`, merged False. Scenario B
    with keep: local main == merged True.
  - Row 3 (Scenario C): rc 0; the six lines `Merged PR #7 as a1b2c3d`,
    `Trunk main fast-forwarded to ebdb2e4`, `Removed worktree .../wt-x`,
    `Deleted local branch feat/x`, `Deleted remote branch feat/x`,
    `next: cd '.../C-default-real/repo'`; worktree, local and remote branch
    all False.
  - Row 4 (Scenario B2): dirty -> rc 1, `BLOCK land.cleanup: worktree
    .../wt-x has modified files`, all three still present; after reverting
    -> rc 0, `Worktree for feat/x: ...`, `Removed worktree ...`,
    `Deleted local branch feat/x`, `Deleted remote branch feat/x`,
    `next: cd '.../repo'`; all three gone. GitHub lookups scripted, as before.
  - Row 5: ship text and `land --help` as above; misuse forms covered by the
    passing usage-error tests.
- Criterion tests at cf7051a7: the same 13 node ids listed under "Criterion
  tests run" -> `13 passed in 17.91s`.

## Re-run after fix (43d90db3..863e5231)

- Fix diff: `loom-code/skills/ship/SKILL.md` (§5 post-merge BLOCK paragraph
  now states the `--keep-worktree` case first and "otherwise run
  `land --cleanup <branch>`"; the earlier-work cleanup sentence gains
  "except a change landed with `--keep-worktree`: its worktree stays until
  the maintainer asks for it to be removed"), plus test-only additions in
  `test_land_merge.py` (bare `--keep-worktree` usage error) and
  `test_ship_station_text.py` (new
  `test_ship_earlier_work_cleanup_spares_kept_worktree`, affirmative case in
  the keep-block matcher test). No `land.py` change.
- Rows re-tested in full: 1 and 5 (ship text governs them). Rows 2-4 were
  not touched by the diff but the whole driver (Scenarios A, B, B2, C) was
  re-run at 863e5231 anyway; every observation below matches the earlier
  run except fresh scratch SHAs and temp paths.
- Clean copy: `git worktree add <scratch>/at-rerun2 863e5231` (detached,
  no uncommitted files; removed with `git worktree remove` afterwards).
- Setup check at 863e5231: `loom-code/scripts/loom-python --ready land
  --keep-worktree` -> `land: --keep-worktree applies only to --accepted-by`,
  exit 2; `land --help` exit 0, text unchanged from the earlier run.

## Setup (original run, 278f801d)

- Clean copy: `git worktree add --detach <scratch>/at-wt 278f801d` (no
  uncommitted files; removed with `git worktree remove` afterwards).
- Plain `python3 loom-code/scripts/loom_checker.py land --help` fails with
  `ModuleNotFoundError: No module named 'yaml'`. This is not this change:
  `import yaml` is already on `main` at
  `loom-code/scripts/loom_checker/helpers.py:11`, and the installed plugin is
  meant to be run through its launcher, which provides the runtime.
- Through the launcher the change loads and is usable:
  `loom-code/scripts/loom-python --ready land --cleanup feat/x --keep-worktree`
  printed `land: --keep-worktree applies only to --accepted-by`, exit 2.
- Every other run below used the locked environment:
  `UV_PYTHON=/usr/local/Caskroom/miniconda/base/envs/dbt-redshift/bin/python uv run --isolated --with-requirements requirements-package-tests.lock python ...`

### How land was exercised

`land` talks to GitHub, so it was driven the same way the repository's own
land tests drive it: a scratch driver (kept outside the repo, reproduced in
the appendix) imports the fixtures of `loom-code/tests/test_land_cleanup.py`
and `loom-code/tests/test_land_merge.py` and calls `land.cmd_land` with the
real argument lists.

- Scenario A (pre-merge gates): `test_land_merge.invoke` — a real local git
  repo with a confirmed intent (`originator: kouko`), every `gh` call
  scripted (PR lookup, live PR body, checks, merge, merge verification).
  `_merge_preconditions`, the checks wait, the PR-body validator, the
  `Accepted-by:` line and `_verify_merge` run for real; only the post-merge
  trunk sync / cleanup step is stubbed by that fixture.
- Scenarios B, C (post-merge): `test_land_cleanup.Layout` — a real bare
  `origin.git`, a main checkout `repo` and a linked worktree `wt-x` on
  `feat/x`, pushed to origin; origin's `main` already carries the squash
  merge. Every git command (fetch, ff-merge, worktree remove, branch delete,
  remote push-delete) runs for real; the merge stages and the `gh` PR-state
  lookup are scripted.

Full driver output: captured to a scratch file at run time; the lines that
back each verdict are quoted below.

## 1. 維護者驗收時要求保留 worktree，合併完成後，該變更的 worktree 還在原來的位置，裡面的檔案與 checkout 的分支都沒有被動到，遠端分支也還在。

- How I tried it: Scenario B. Before landing, wrote an uncommitted edit to
  `wt-x/feature.txt` and an untracked `wt-x/scratch-notes.txt`, recorded
  `git status --porcelain` and `HEAD`. Ran
  `land --accepted-by kouko --keep-worktree` with cwd = the change worktree.
- What came back:

  ```text
  rc: 0
  stdout:
    Merged PR #7 as a1b2c3d
    Trunk main fast-forwarded to 114a915
    Kept worktree .../B-keep-real/wt-x on branch feat/x; remove it later with: land --cleanup feat/x
  stderr: ''
  cwd after: .../B-keep-real/wt-x
  worktree dir exists: True
  local branch feat/x: True
  remote branch feat/x: True
  worktree checked-out branch: feat/x
  worktree HEAD unchanged: True
  worktree status unchanged: True
  uncommitted edit intact: True
  untracked file intact: True
  git calls that remove/push: []
  ```

- Re-run at 863e5231: identical observations (`Trunk main fast-forwarded
  to c5ec3e0`; all booleans as above; remove/push calls `[]`).
- Ship text after merge (re-read at 863e5231, `ship/SKILL.md`):
  :337-341 "If land prints `Merged PR` and then a BLOCK, do not rerun
  `--accepted-by`; resolve the named state. When the land that printed the
  BLOCK carried `--keep-worktree`, keep the worktree for a later
  `land --cleanup <branch>` once the maintainer wants it removed; otherwise
  run `land --cleanup <branch>`."; :349-351 "For one merged change left from
  earlier work, run `land --cleanup <branch>` through the same command,
  except a change landed with `--keep-worktree`: its worktree stays until
  the maintainer asks for it to be removed." Neither cleanup instruction now
  reaches a kept worktree without the maintainer asking.
- Caveat (stated by the new help text itself): land deletes neither
  branch, "but a hosting setting that deletes head branches on merge can
  still remove the remote one". A GitHub repository with "Automatically
  delete head branches" on would lose the remote branch regardless; not
  reproducible locally.
- Evidence: driver Scenario B; tests
  `test_land_cleanup.py::test_keep_worktree_flag_keeps_all_then_cleanup_removes_all`,
  `test_land_cleanup.py::test_keep_worktree_output_names_cleanup_command` passed.

## 2. 要求保留的這次合併，仍然經過和一般合併相同的檢查與驗收紀錄，主幹也照常同步；任一檢查不過時，一樣拒絕合併。

- How I tried it: Scenario A, each case run twice — once with
  `--accepted-by kouko`, once with `--accepted-by kouko --keep-worktree` —
  and compared: happy path, a failing check, a foreign acceptor name, an
  invalid live PR body. Trunk sync with the flag observed in Scenario B.
- What came back:

  ```text
  plain stdout: 'All checks registered on PR #7 passed\nMerged PR #7 as a1b2c3d\nloom: verification absent (missing: attestation); merged anyway.\n'
  keep  stdout: (identical)
  plain Accepted-by line in merge body: ['Accepted-by: kouko 2026-11-21']
  keep  Accepted-by line in merge body: ['Accepted-by: kouko 2026-11-21']
  external call order, both: repo view, api (pulls), pr view, pr checks, pr view, pr view, pr merge, pr view, fetch origin main, cat-file commit
  only differing argv: --match-head-commit <sha> and the temp --body-file path
    (two separate scratch repos, so different head commits; not a behaviour difference)
  plain+failing check rc 1 'BLOCK land.merge: check lint: FAILURE; ...' merged? False
  keep+failing check  rc 1 (identical message)                        merged? False
  plain+foreign name  rc 1 'BLOCK land.merge: acceptance not recorded; ...' merged? False
  keep+foreign name   rc 1 (identical message)                        merged? False
  plain+invalid PR body rc 1 'BLOCK land.merge: PR body heading "Summary" is not one of the nine contextual headings; ...' merged? False
  keep+invalid PR body  rc 1 (identical message)                      merged? False
  Scenario B (keep): 'Trunk main fast-forwarded to 114a915'; local main == merged: True
  ```

- Evidence: driver Scenario A and B; test
  `test_land_merge.py::test_keep_worktree_failing_check_refuses_merge` passed.
  Code path: `land.py` `_land_accepted` runs `_merge_preconditions`,
  `_squash_merge`, `_verify_merge` unchanged and only passes `keep` to
  `_sync_and_clean`, which calls `sync_trunk` before the keep branch.

## 3. 沒有要求保留時，合併後的結果和現在相同：worktree 與本機、遠端分支都被移除。

- How I tried it: Scenario C, `land --accepted-by kouko` with cwd = the
  change worktree, clean tree.
- What came back:

  ```text
  rc: 0
  stdout:
    Merged PR #7 as a1b2c3d
    Trunk main fast-forwarded to 38f21e3
    Removed worktree .../C-default-real/wt-x
    Deleted local branch feat/x
    Deleted remote branch feat/x
    next: cd '.../C-default-real/repo'
  worktree dir exists: False
  local branch feat/x: False
  remote branch feat/x: False
  ```

- Evidence: driver Scenario C; existing test
  `test_land_cleanup.py::test_merged_change_refs_worktree_removed` (asserts
  the exact same six output lines) passed.

## 4. 保留下來的變更，之後用 loom 既有的清理方式可以把 worktree 與分支清掉。

- How I tried it: Scenario B2, on the worktree kept in Scenario B, ran the
  command land printed: `land --cleanup feat/x`. First with the scratch
  edits still in the worktree, then again after reverting them (as the
  maintainer would after finishing their post-merge work).
- What came back:

  ```text
  rc (worktree still dirty): 1
  stderr: BLOCK land.cleanup: worktree .../B-keep-real/wt-x has modified files
  worktree / local branch / remote branch: all still present
  rc (after worktree cleaned by maintainer): 0
  stdout:
    Worktree for feat/x: .../B-keep-real/wt-x
    Removed worktree .../B-keep-real/wt-x
    Deleted local branch feat/x
    Deleted remote branch feat/x
    next: cd '.../B-keep-real/repo'
  worktree dir exists: False
  local branch feat/x: False
  remote branch feat/x: False
  ```

- Limit: the cleanup's GitHub lookups (`_cleanup_context`, `_merged_prs`)
  were scripted, as in the repo's own test; a real GitHub round trip was not
  run.
- Evidence: driver Scenario B2; test
  `test_land_cleanup.py::test_keep_worktree_flag_keeps_all_then_cleanup_removes_all` passed.

## 5. 照 ship 的流程文字，維護者要求保留 worktree 時，agent 有一條不需要自己打 `gh pr merge` 的做法；`land` 的說明文字不再要求一件合併形式做不到的事。

- How I tried it: read `loom-code/skills/ship/SKILL.md` §5 in the clean
  copy as the agent would; ran `land --help`; ran the misuse forms.
- What came back:
  - ship SKILL.md:311 "Never type `gh pr merge` yourself: merge through land";
    :327-328 "When the maintainer asks to keep the worktree, add
    `--keep-worktree` to that land command."; :333-335 kept worktree stays
    until a later `land --cleanup <branch>`, no `next:` line, stay in the
    kept worktree; :339-341 a post-merge BLOCK on a keep land keeps the
    worktree for a later cleanup.
  - `land --help` (exit 0): `Usage: land --accepted-by <name> [--keep-worktree]`;
    "When worktree preservation was requested, pass --keep-worktree to the
    accepted form and do not run cleanup."; the old sentence "Do not run
    cleanup when worktree preservation was requested." is gone.
  - `land --cleanup feat/x --keep-worktree` / `land --keep-worktree --sweep`
    → `land: --keep-worktree applies only to --accepted-by`, exit 2;
    `land --accepted-by kouko --keep-worktree --keep-worktree` →
    `land: --keep-worktree may appear only once`, exit 2.
  - Earlier wording nit (ship :337-338 met the cleanup instruction before
    the keep carve-out) is resolved at 863e5231: the keep case now comes
    first and cleanup is the "otherwise" branch (quoted under row 1).
  - Re-run at 863e5231: bare `land --keep-worktree` and
    `land --cleanup feat/x --keep-worktree` -> `land: --keep-worktree
    applies only to --accepted-by`, exit 2.
- Evidence: tests passed —
  `test_ship_station_text.py::test_ship_text_has_no_direct_gh_pr_merge`,
  `::test_ship_text_adds_keep_worktree_when_maintainer_asks`,
  `::test_ship_keep_block_recovery_keeps_worktree`,
  `::test_keep_block_matcher_negated_sentence_rejected`,
  `test_loom_checker_cli.py::test_land_is_a_declared_cli_command`,
  `::test_land_help_names_keep_worktree_for_preservation`,
  `test_land_merge.py::test_keep_worktree_with_cleanup_or_sweep_usage_error`,
  `::test_keep_worktree_twice_usage_error`.

## Criterion tests run

```text
UV_PYTHON=/usr/local/Caskroom/miniconda/base/envs/dbt-redshift/bin/python uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider \
  loom-code/tests/test_land_cleanup.py::test_keep_worktree_flag_keeps_all_then_cleanup_removes_all \
  loom-code/tests/test_land_cleanup.py::test_keep_worktree_output_names_cleanup_command \
  loom-code/tests/test_land_cleanup.py::test_merged_change_refs_worktree_removed \
  loom-code/tests/test_land_merge.py::test_keep_worktree_failing_check_refuses_merge \
  loom-code/tests/test_land_merge.py::test_keep_worktree_with_cleanup_or_sweep_usage_error \
  loom-code/tests/test_land_merge.py::test_keep_worktree_twice_usage_error \
  loom-code/tests/test_loom_checker_cli.py::test_land_is_a_declared_cli_command \
  loom-code/tests/test_loom_checker_cli.py::test_land_help_names_keep_worktree_for_preservation \
  loom-code/tests/test_ship_station_text.py::test_ship_text_has_no_direct_gh_pr_merge \
  loom-code/tests/test_ship_station_text.py::test_ship_text_adds_keep_worktree_when_maintainer_asks \
  loom-code/tests/test_ship_station_text.py::test_ship_keep_block_recovery_keeps_worktree \
  loom-code/tests/test_ship_station_text.py::test_keep_block_matcher_negated_sentence_rejected
12 passed in 17.91s
```

Re-run at 863e5231 (same list plus the new earlier-work test):

```text
... same 12 node ids ... \
  loom-code/tests/test_ship_station_text.py::test_ship_earlier_work_cleanup_spares_kept_worktree
13 passed in 14.47s
```

The complete package suite (`uv run --isolated --with-requirements
requirements-package-tests.lock python scripts/run_package_tests.py
--loom-family -q`) was not run here; finalize-review runs it and refuses the
attestation when it fails.

## Appendix — driver outline

`drive_keep.py <clean-copy>` puts `loom-code/scripts` and `loom-code/tests`
on `sys.path`, imports `test_land_cleanup as C`, `test_land_merge as M` and
`land`, then:

- Scenario A: for each case, `M.invoke(base/<name>, MonkeyPatch(), *args,
  configure=...)` with and without `--keep-worktree`; a spy on
  `land._land_accepted` records the `keep` keyword it receives
  (`[False, True]`); compares stdout, stderr, the `Accepted-by:` line of the
  squash body file and the scripted external-call argv lists. Failing-check
  configure: `checks = [[PASS, {"name": "lint", "state": "FAILURE",
  "bucket": "fail"}]]`, `check_returncodes = [1]`; invalid body:
  `pr_body = "## Summary\nonly one heading\n"`; foreign name: `stranger`.
- Scenario B: `C.Layout(base/"B-keep-real")`, dirty the worktree, then
  `C.run_land(mp, layout, cwd=layout.wt, args=("--accepted-by", "kouko",
  "--keep-worktree"))`, then inspect the worktree, refs on `repo` and on
  `origin.git`, and the recorded git argv.
- Scenario B2: new MonkeyPatch with `run_land_external = C.Calls(layout)`
  (git real, gh scripted), `_cleanup_context` returning a `LandTarget` on
  `layout.repo`, `_merged_prs` returning PR #7 at `layout.head`; call
  `land.cmd_land(["--cleanup", "feat/x"])` before and after reverting the
  scratch edits.
- Scenario C: `C.Layout(base/"C-default-real")`, `C.run_land(mp, layout,
  cwd=layout.wt)` with the default `--accepted-by kouko`.
