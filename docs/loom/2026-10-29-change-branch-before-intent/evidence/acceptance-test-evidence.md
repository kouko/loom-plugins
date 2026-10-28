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
- Evidence: scratchpad `a45.log` sections A5a-A5e; `test_own_change_branch_reused`, `test_unrelated_branch_or_detached_head_resolved_before_commit`, `test_own_change_branch_reused_at_capture` passed; adversarial probe `test_probe_existing_change_branch.py` 4 passed (then under `docs/loom/2026-10-29-change-branch-before-intent/evidence/probes/`; graduated by f129421d to `loom-code/tests/test_probe_existing_change_branch.py`).

## Targeted tests per criterion
```
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
  python -m pytest -q -p no:cacheprovider loom-design/tests/spec/test_capture_intent_contract.py \
  loom-design/tests/spec/test_write_spec_contract.py loom-code/tests/test_write_plan_station_text.py \
  loom-code/tests/test_ship_station_text.py loom-code/tests/test_land_cleanup.py \
  docs/loom/2026-10-29-change-branch-before-intent/evidence/probes/test_probe_existing_change_branch.py
-> 116 passed in 14.71s   (at 52bf2842; the probe now lives at loom-code/tests/test_probe_existing_change_branch.py)
```

## Package suite (run once at the dispatcher's request; finalize-review runs it again and blocks on failure)
```
env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
  python scripts/run_package_tests.py --loom-family -q
-> exit 0; 14 pytest runs, 3767 passed, 11 skipped, 0 failed; 145 script checks PASS, 0 FAIL
```

## Re-run on 2026-10-29, at ea554bea
Fix range 4520f050..ea554bea: station text changed only in `loom-code/skills/write-plan/SKILL.md:51-66` (route sentence added at `:59-61`; "which becomes the trunk squash commit" and "At station entry, keep the full flow unless the user instructed a skip." removed) and `loom-design/skills/capture-intent/SKILL.md:336-340` (route sentence added). The rest is plan, tests, probe move, CHANGELOGs.

Setup check: `git worktree add --detach <scratch>/at/clean-r2 HEAD` (ea554bea). `claude plugin validate ./loom-code` -> `Validation passed`; `./loom-design` -> `Validation passed with warnings` (`requires-contract` unknown field; plugin-directory `ICON_MISSING`); `.` -> passed with warnings (`plugins[2]` `requires-contract`). No manifest changed since 52bf2842 (`git diff --stat 52bf2842..HEAD -- */.claude-plugin .claude-plugin` empty), so these warnings predate the fix. Versions `3.51.0` / `2.16.0`.

Sandboxes: script `at/r2.sh`, log `at/r2.log` (scratchpad, not committed); every case a local bare `origin.git` plus a clone, no remote. The tester acted as the agent following only the station text at ea554bea. For the route, per both stations: `git worktree add -b fix/<id> ../wt-change main`, then continue in `../wt-change`. capture-intent: "carry the uncommitted intent draft there" -> copied (not moved) the draft. write-plan: its sentence names no draft carry; the new worktree held no intent file (`intent draft present in new worktree before any carry: no`), so the tester copied the draft to make the confirmation commit possible. "Original checkout unchanged" compares HEAD sha, branch name, `git diff` hash and the untracked-file list before and after.

- 1: carried over — the capture-intent edit only appends to the unrelated-branch / detached-HEAD sentence; the trunk route ("on the trunk, create it", `git switch -c`) and `write-spec/SKILL.md` are byte-identical to 52bf2842.
- 2: carried over — fix touches neither `land.sync_trunk` nor `ship/SKILL.md`.
- 3: carried over — same as 2.
- 4: re-tested — fresh sandbox, HEAD on synced `main`; `write-plan/SKILL.md:43-61` (rule before every commit point; first commit point the skip record at `:71`), `references/confirm-intent.md` step 2, Step 6 at `SKILL.md:468`; then Step 3 (`SKILL.md:226-232`) from the trunk with the branch existing.
  ```
  trunk unchanged: yes | main..branch: plan / record skip / intent ... confirmed
  first change-owned commit's parent is the trunk tip: yes
  fatal: a branch named 'fix/2026-10-29-sandbox-change' already exists   (git switch -c, refused)
  Switched to branch 'fix/2026-10-29-sandbox-change'                    (git switch)
  fix commit on: fix/2026-10-29-sandbox-change | trunk unchanged: yes
  ```
- 5: re-tested — every surface, for both entries (ci = capture-intent `SKILL.md:330-343`, wp = write-plan `SKILL.md:51-61`):
  ```
  b-ci unrelated branch + tracked edit + untracked file + draft:
       original checkout unchanged: yes | main..fix: intent confirmed | first commit parent is trunk tip: yes
       trunk unchanged: yes, ahead of origin: 0 | commits on feat/other since start: 0
  c-ci detached HEAD with an unbranched commit + draft:
       original checkout unchanged: yes (still detached at 66328c1, no branch contains it — only the detached HEAD)
       main..fix: intent confirmed | first commit parent is trunk tip: yes | trunk ahead of origin: 0
  b-wp same as b-ci: unchanged: yes | main..fix: plan / record skip / intent confirmed | parent is trunk tip: yes
       commits on feat/other since start: 0
  c-wp same as c-ci: unchanged: yes (still detached at 7e0e0ae) | same three commits | parent is trunk tip: yes
  a-ci, a-wp own branch: branch count 2/2 | new commit parent is old tip: yes
  d-ci, d-wp branch exists, HEAD on trunk: `git switch -c` refused, `git switch` -> earlier commits kept: yes, trunk ahead: 0
  e-ci, e-wp branch in another worktree: fatal: '...' is already used by worktree at '.../wt-other'
       committed there -> commit on fix/<id> | trunk ahead of origin: 0
  ```
- Suite row: re-tested — targeted tests for 4 and 5 only; the package suite is left to finalize-review, which runs it and refuses the attestation on failure.
  ```
  env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
    python -m pytest -q -p no:cacheprovider loom-design/tests/spec/test_capture_intent_contract.py \
    loom-design/tests/spec/test_write_spec_contract.py loom-code/tests/test_write_plan_station_text.py \
    loom-code/tests/test_probe_existing_change_branch.py
  -> 89 passed in 0.37s
  ```
  Package suite command (not run in this re-run; finalize-review runs it):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- Observation (open reviewer question, not decided here): `write-plan/SKILL.md:59-61` does not say to carry an uncommitted intent draft into the new worktree, while `capture-intent/SKILL.md:338-339` does; with only write-plan's text the new worktree has no intent file to confirm. (Resolved by 66f30dd2; see the next re-run.)

## Re-run on 2026-10-29, at 66f30dd2
Fix range 224b7d4f..66f30dd2: `write-plan/SKILL.md:51-52` dropped "; use it in the PR title" (`ship/SKILL.md:180-181` still ties the PR title type to the branch prefix); `write-plan/SKILL.md:59-62` route now reads "..., move any uncommitted intent draft there and continue in that new worktree"; `capture-intent/SKILL.md:337-340` "carry" -> "move the uncommitted intent draft there". Plus test pins and CHANGELOGs.

Setup check: clean `git worktree add --detach <scratch>/at/clean-r3 HEAD` (66f30dd2): loom-code `Validation passed`; loom-design and marketplace `Validation passed with warnings` (same pre-existing warnings as before).

Sandboxes: script `at/r3.sh`, log `at/r3.log` (scratchpad, not committed); same cases as the ea554bea re-run, but for the route both stations now follow their own text: `git worktree add -b fix/<id> ../wt-change main`, then `mv` the draft into `../wt-change`, then continue there. "Unchanged minus the moved draft" compares HEAD sha, branch name, `git diff` hash and the untracked list with the draft path excluded.

- 1: carried over — 66f30dd2 changes only "carry" -> "move" inside the unrelated-branch / detached-HEAD sentence; the trunk route and `write-spec/SKILL.md` are unchanged.
- 2, 3: carried over — `land` and `ship/SKILL.md` untouched.
- 4: re-tested (the removed clause sits in the branch-rule paragraph) — same steps as before:
  ```
  trunk unchanged: yes | main..branch: plan / record skip / intent ... confirmed
  first change-owned commit's parent is the trunk tip: yes
  git switch -c refused (branch exists) -> git switch -> fix commit on fix/<id> | trunk unchanged: yes
  ```
- 5: re-tested — every surface, both entries:
  ```
  b-ci, b-wp unrelated branch + tracked edit + untracked file + draft:
       draft in new worktree: yes, same content: yes | draft left in original: no
       original checkout unchanged minus the moved draft: yes (untracked.txt still there, diff hash 958f24817478)
       main..fix: intent confirmed (wp: + record skip, plan) | first commit parent is trunk tip: yes
       trunk ahead of origin: 0 | commits on feat/other since start: 0
  c-ci, c-wp detached HEAD with an unbranched commit + draft:
       draft moved: yes, same content: yes | unchanged minus draft: yes | still detached at its commit: yes
       first commit parent is trunk tip: yes | trunk ahead of origin: 0
  a own branch reused (branch count 2/2); d `git switch -c` refused, `git switch`, earlier commits kept;
  e branch in another worktree -> committed there; trunk ahead of origin: 0   (ci and wp)
  ```
- Suite row: re-tested — same targeted command as the ea554bea re-run -> `89 passed in 0.33s`. Package suite left to finalize-review (command above).

## 6. When the change moves to another worktree — a new one, or the one where its branch is already checked out — every uncommitted file the change produced so far (the intent draft, a spec, a `PRINCIPLES.md` edit) ends up committed on the change branch there, and the original checkout keeps exactly its own earlier work. A spec is never left in a checkout the change has left.
Added by the intent re-confirmation in 30c08e61; first tried in the re-run below.

## Re-run on 2026-10-29, at 910034de
Fix range 382f0561..910034de (functional: 30c08e61 intent + Acceptance 6, 8f31d1ab plan wave 4, 37f349c5, c1f09203, 910034de changelogs). Prose: `capture-intent/SKILL.md:336-343` (route paragraph rewrapped; "on this or any move to another worktree, first move every uncommitted file this change produced (the intent draft, a `PRINCIPLES.md` edit) there ... so the original checkout keeps exactly its own earlier work"); `write-plan/SKILL.md:51-61` (dropped "Task commits keep their implementer contract type; `docs(loom):` intent and plan commits keep their fixed form."; same move sentence at `:59-61`); `write-spec/SKILL.md:68-71` (Step 1 settles the branch before Step 2 writes, moving uncommitted change files first). Also `attestation.json` and `ae9bd6a2` (reviewer record), not station prose.

Setup check: clean `git worktree add --detach <scratch>/at/clean-r4 HEAD` (910034de): loom-code `Validation passed`; loom-design and marketplace `Validation passed with warnings` (pre-existing warnings, as before).

Sandboxes: `at/r4.sh` -> `at/r4.log`, follow-ups `at/r4b.sh` -> `at/r4b.log` (scratchpad, not committed). Each sandbox starts from `main` holding `app.txt` and `PRINCIPLES.md`. The original checkout's own earlier work is a tracked edit to `app.txt` plus an untracked `notes.txt`. Byte-level fingerprint `fp` = HEAD sha, branch name, `git diff --binary` hash, `git diff --cached --binary` hash, and each untracked file's path + content hash, taken before the change produced anything and again at the end. "Move every uncommitted file this change produced": untracked draft/spec -> `mv`; the `PRINCIPLES.md` ratified-by edit (a tracked file) -> its diff applied in the target worktree, then `git restore -- PRINCIPLES.md` in the original.

- 1: re-tested — write-spec's branch step moved to Step 1 (`write-spec/SKILL.md:68-71`).
  ```
  A1  trunk unchanged: yes | ahead of origin: 0 | main..fix: spec | intent confirmed
  A1b write-spec from the trunk: `git switch -c` refused (exists) -> `git switch fix/<id>` in Step 1, then spec written and committed
      spec commit on: fix/<id> | trunk unchanged: yes
  ```
- 2, 3: carried over — `land` and `ship/SKILL.md` untouched in 382f0561..910034de.
- 4: re-tested (the branch-rule paragraph lost a sentence) —
  ```
  trunk unchanged: yes | main..fix: plan | record skip | intent confirmed | first commit parent is trunk tip: yes
  A4b `git switch -c` refused -> `git switch` -> fix commit on fix/<id> | trunk unchanged: yes
  ```
- 5: re-tested — every surface, ci and wp (r4.log 6b-wp, 6b-ci2 in r4b.log, 5a/5c/5d/5e):
  ```
  unrelated branch + own edits (+ draft; ci also PRINCIPLES edit): original byte-identical: yes | feat/other commits since start: 0
  detached HEAD + unbranched commit + own edits + draft:         original byte-identical: yes | still detached at its commit: yes
  own branch reused (2/2 branches); branch exists -> `git switch`, earlier commits kept; branch in another worktree -> committed there
  every case: first change commit's parent is trunk tip: yes | trunk ahead of origin: 0
  ```
  Gap (not one of the line's named cases, see finding 1): unrelated branch AND change branch already exists, checked out nowhere (r4.log A6c-2, r4b.log):
  ```
  git worktree add -b fix/<id> ../wt-change main  -> fatal: a branch named 'fix/2026-10-29-sandbox-change' already exists (exit 255, no worktree)
  git switch fix/<id> (the "already exists" sentence) -> Switched; HEAD now fix/<id>; own edits now in the change checkout: M app.txt ?? notes.txt
  git worktree add ../wt-change fix/<id> (not named by the text) -> spec committed there; original byte-identical: yes
  ```
- 6: re-tested —
  ```
  6a-ci branch checked out in ../wt-change, original on main with own work + draft + PRINCIPLES ratified-by edit
        moved draft, moved PRINCIPLES.md edit -> commit on fix/<id>: PRINCIPLES.md + intent draft | ratified-by on branch: 1
        original byte-identical: yes | change files left in original: draft=no spec=no PRINCIPLES-diff=no
  6a-wp same, draft only -> intent confirmed, record skip, plan on fix/<id> | original byte-identical: yes
  6b-ci unrelated branch + own edits, new-worktree route, draft + PRINCIPLES edit (r4b.log)
        commit on fix/<id>: PRINCIPLES.md + draft | original byte-identical: yes | nothing left behind | feat/other commits: 0
  6b-wp same, draft only -> three commits on fix/<id> | original byte-identical: yes
  6c-1 write-spec, original on feat/other with own edits, fix/<id> checked out in ../wt-change
        Step 1: "checked out in another worktree, work in that worktree" -> Step 2 writes the spec there -> `docs(loom): spec` on fix/<id>
        original byte-identical: yes | spec left in original: no
  every case: first change commit's parent is trunk tip: yes | trunk ahead of origin: 0
  ```
  Probe (finding 2): feat/other has its own committed `PRINCIPLES.md` line, then the ratified-by edit. Moving the edit: `git apply` -> `patch does not apply`; `git apply -3` -> `Applied patch to 'PRINCIPLES.md' with conflicts` (exit 1). Moving the whole file (cp + restore) -> branch's `PRINCIPLES.md` has ratified-by=1 AND the unrelated branch's `other line`=1.
- Suite row: re-tested — targeted:
  ```
  env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock \
    python -m pytest -q -p no:cacheprovider loom-design/tests/spec/test_capture_intent_contract.py \
    loom-design/tests/spec/test_write_spec_contract.py loom-code/tests/test_write_plan_station_text.py \
    loom-code/tests/test_probe_existing_change_branch.py
  -> 92 passed in 0.33s
  ```
  Package suite left to finalize-review: `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- Finding 1 (important): `capture-intent/SKILL.md:333-343`, `write-plan/SKILL.md:54-61`, and `write-spec/SKILL.md:68-71` by reference: unrelated branch or detached HEAD while `<type>/<change-id>` already exists and is checked out nowhere. The route `git worktree add -b` is refused; the "already exists -> `git switch`" sentence moves the original checkout and its own uncommitted edits onto the change branch. Fix: name `git worktree add <path> <type>/<change-id>` (no `-b`) for an existing branch.
- Finding 2 (nit): `capture-intent/SKILL.md:340-342`: "move every uncommitted file ... (a `PRINCIPLES.md` edit)" leaves open whole-file vs edit; when the original's base `PRINCIPLES.md` differs from the trunk's, whole-file carries unrelated content and edit-only conflicts. Fix: say to move the edit and stop to ask on conflict.
