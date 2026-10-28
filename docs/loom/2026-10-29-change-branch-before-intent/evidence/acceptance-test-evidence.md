# Change records start on the change branch, and a diverged trunk is never discarded unasked — acceptance test evidence

Tried on 2026-10-29, in a clean copy of the project at `52bf2842` (`git worktree add --detach <scratch>/clean HEAD`).

Setup check: the README installs from the GitHub marketplace, which would fetch `main`, not this branch, so the clean copy was validated in place instead:
`claude plugin validate ./loom-code` -> `Validation passed`; `./loom-design` -> `Validation passed`; `.` (marketplace) -> passed with one warning on `plugins[2]` (loom-workflow, `requires-contract` unknown field; untouched by this change). All eight loom-code / loom-design manifests read `3.51.0` / `2.16.0`.

Sandboxes: every scenario used a local bare `origin.git` plus a clone under the session scratchpad; no network, no real remote. The station steps below were performed by the tester acting as the agent, following only the station text at `52bf2842`; the git outcomes are real. Scripts: `a123.sh`, `a45.sh`, `sync.py` (scratchpad, not committed). `sync.py` calls the real `land.sync_trunk` (`loom-code/scripts/loom_checker/command_handlers/land.py:309`) through `loom-code/scripts/loom-python --repair --script`, with real git (no seam monkeypatching). The squash merge is simulated as GitHub does it: `git commit-tree <branch>^{tree} -p origin/main`, pushed to `origin/main`.

## 1. Running a change from a clean, synchronized trunk through `capture-intent` (and `write-spec` when it runs) adds no commit to the local trunk; the intent commit is on the change branch.
- How I tried it: fresh clone, `main` == `origin/main`. Followed `loom-design/skills/capture-intent/SKILL.md:330-339` (Step 4.2): HEAD on the trunk -> `git switch -c fix/<id>`, then `docs(loom): intent <id> confirmed`. Followed `loom-design/skills/write-spec/SKILL.md:282-284`: already on the change branch -> `docs(loom): spec <id>`. Then a later write-spec entry with HEAD back on `main`: `git switch -c` refused (`fatal: a branch named ... already exists`), `git switch fix/<id>` per the capture-intent rule.
- What came back:
  ```
  trunk before: 4857e24c... | origin/main: 4857e24c... | HEAD: main
  Switched to a new branch 'fix/2026-10-29-sandbox-change'
  trunk after:  4857e24c... (unchanged: yes)
  commits on main not on origin/main: 0
  f20bff8 docs(loom): spec ...   68fefdc docs(loom): intent ... confirmed   (main..fix/<id>)
  branch holding the intent commit: fix/2026-10-29-sandbox-change
  ```
- Evidence: scratchpad `a123.log` section A1/A1b; named tests `test_capture_intent_branches_before_confirmation_commit`, `test_trunk_commit_allowance_absent`, `test_write_spec_guard_defers_to_capture_intent_rule` passed (targeted run below).

## 2. Starting from a trunk synchronized with `origin` and receiving no independent local commits, after that change is merged through `land` the local trunk fast-forwards to the merge with no manual reconciliation.
- How I tried it: continued the A1 sandbox (variant a: change branch in the main clone, trunk checked out nowhere -> `fetch origin main:main` path), and a second sandbox (variant b: `main` checked out clean in the main clone, change in a linked worktree with intent, plan and code commits -> `merge --ff-only` path). Pushed the branch, squash-merged on origin, ran the real `sync_trunk`. Control: the pre-change flow (intent committed on the trunk, as in the dogfood).
- What came back:
  ```
  A2a  sync_trunk: Trunk main fast-forwarded to a8d5509   local main == merge: yes
  A2b  sync_trunk: Trunk main fast-forwarded to 6c16fbb   local main == merge: yes
  ctrl sync_trunk: trunk not updated: not a fast-forward  local main unchanged: yes
  ```
- Evidence: scratchpad `a123.log` sections A2; `test_clean_trunk_fast_forwards` and `test_no_trunk_checkout_fetches_trunk_ref` (`loom-code/tests/test_land_cleanup.py`) passed. `land`'s merge, PR checks and worktree cleanup were not run (they need GitHub); only `sync_trunk`, the step this line depends on.

## 3. Given a local-only sentinel commit on the trunk and `land` reporting `trunk not updated`, an agent following the station instructions reports it to the maintainer and leaves the trunk's commit identifier unchanged; merge acceptance does not count as permission to discard it.
- How I tried it: run — fresh sandbox, local-only commit `sentinel: local-only work` on `main` (checked out clean); change in a linked worktree from `origin/main`; squash-merged on origin; real `sync_trunk`. Read — `loom-code/skills/ship/SKILL.md:275-279` (§5) as the agent's next instruction: report the line, leave the trunk; no command was run. Grep of `loom-code/skills`, `loom-design/skills`, `loom-workflow/skills`, `loom-code/agents` for `reset --hard`, `git reset`, `branch -f`: only ship §5 (forbidding) and `closing-review/references/adversarial.md:125` (an unrelated forbidden-command list); nothing instructs a trunk reset.
- What came back:
  ```
  sentinel sha: dfb6b531...
  sync_trunk: trunk not updated: fatal: Not possible to fast-forward, aborting.
  sentinel sha after: dfb6b531... unchanged: yes   sentinel file still present: mine
  ```
  ship §5: "If land prints `trunk not updated`, report that line to the maintainer and leave the local trunk as it is. Never discard local trunk commits ... without the maintainer's explicit yes to that discard: the acceptance at decision point ③ is not that permission."
- Evidence: scratchpad `a123.log` section A3; `test_ship_reports_trunk_not_updated_to_the_maintainer`, `test_merge_acceptance_is_not_permission_to_discard_trunk`, `test_trunk_not_fast_forward_message_has_no_rebase_advice` passed. The "reports to the maintainer" half is the text an agent reads, not an observed live-agent session.

## 4. A change entered at `write-plan` (loom-design absent) branches before its first change-owned commit, including the intent-confirmation commit.
- How I tried it: followed `loom-code/skills/write-plan/SKILL.md:43-59` (rule placed before every commit point; first commit point in the file is the skip record at `:71`), `references/confirm-intent.md:114-115` (step 2), Step 6 at `SKILL.md:467`. HEAD on synced `main` -> `git switch -c fix/<id>` -> intent confirmation, skip-record, plan commits. Then Step 3 (`SKILL.md:227-231`) from a new session on the trunk with the branch existing -> `git switch fix/<id>` -> `needs-design:` fix commit.
- What came back:
  ```
  trunk unchanged: yes | main..branch: plan / record skip / intent ... confirmed
  first change-owned commit's parent is the trunk tip: yes
  fatal: a branch named 'fix/...' already exists      (git switch -c, refused)
  Switched to branch 'fix/...'                        (git switch)
  fix commit on: fix/2026-10-29-sandbox-change | trunk unchanged: yes
  ```
- Evidence: scratchpad `a45.log` sections A4/A4b; `test_branch_rule_precedes_confirmation_and_skip_record_commits`, `test_intent_on_trunk_allowance_absent` passed.

## 5. When HEAD is already on the branch belonging to this change, the station reuses it; on an unrelated branch or a detached HEAD it does not commit there before that is resolved, and existing work is preserved.
- How I tried it (rule text: `write-plan/SKILL.md:54-59`, `capture-intent/SKILL.md:333-337`):
  - a) HEAD on `fix/<id>` -> committed there, no new branch.
  - b) HEAD on `feat/other` with a tracked edit and an untracked file -> did not commit there; resolved by leaving that checkout untouched and `git worktree add -b fix/<id> ../wt-change main`; intent committed in the new worktree.
  - c) detached HEAD carrying a commit no branch holds -> same resolution.
  - d) branch exists, HEAD on trunk -> `git switch -c` refused, `git switch fix/<id>`, spec committed on top.
  - e) branch checked out in another worktree -> `git switch` refused, committed in that worktree ("work there").
- What came back:
  ```
  a) branch count before/after: 2/2 | new commit parent is old tip: yes
  b) after: HEAD=feat/other, feat/other unchanged: yes, diff-hash 958f24817478 == before, untracked: scratch
     intent commit on: fix/<id> | on feat/other: 0
  c) original checkout still detached at 8f55950: yes | main unchanged: yes
  d) earlier intent commit kept under the spec: yes | trunk ahead of origin: 0
  e) fatal: 'fix/...' is already used by worktree at '.../wt-other'
     plan commit on: fix/<id> | trunk ahead of origin: 0
  ```
  Side observation (b, not the route taken): in a separate sandbox, `git switch -c fix/alt-demo main` from the dirty unrelated branch succeeds and carries ` M app.txt` and `?? untracked.txt` onto the change branch's working tree — preserved, but now sitting in the change's checkout. The station text says "resolve that first and preserve existing work, no reset, no discard" and names no route.
- Evidence: scratchpad `a45.log` sections A5a-A5e; `test_own_change_branch_reused`, `test_unrelated_branch_or_detached_head_resolved_before_commit`, `test_own_change_branch_reused_at_capture` passed; adversarial probe `docs/loom/2026-10-29-change-branch-before-intent/evidence/probes/test_probe_existing_change_branch.py` 4 passed.

## Targeted tests per criterion
```
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
  python -m pytest -q -p no:cacheprovider loom-design/tests/spec/test_capture_intent_contract.py \
  loom-design/tests/spec/test_write_spec_contract.py loom-code/tests/test_write_plan_station_text.py \
  loom-code/tests/test_ship_station_text.py loom-code/tests/test_land_cleanup.py \
  docs/loom/2026-10-29-change-branch-before-intent/evidence/probes/test_probe_existing_change_branch.py
-> 116 passed in 14.71s
```

## Package suite (run once at the dispatcher's request; finalize-review runs it again and blocks on failure)
```
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
  python scripts/run_package_tests.py --loom-family -q
-> exit 0; 14 pytest runs, 3767 passed, 11 skipped, 0 failed; 145 script checks PASS, 0 FAIL
```
