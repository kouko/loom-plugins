# The probe-program cap counts only probes a change adds, not tests it moves — acceptance test evidence

Tried on 2026-09-25, in a clean copy of the project at 7a19c5a9 (a fresh
`git worktree add --detach <scratch>/at 7a19c5a9`; Python 3.12.11, git 2.50.1).

Setup: this change is checker logic, so there is nothing to install; the
clean copy's checker imported and ran directly (`--list-rules`,
`check_mechanisms.py`, and the probe count imported from
`loom-code/scripts/loom_checker/probes.py`). No `claude -p` trial was run, as
the dispatch directed.

Throwaway repositories (both moved to the scratch trash afterwards):

- `repo` — `git clone --no-checkout` of the project, `origin` removed, `main`
  at 7a19c5a9; each scenario is a branch off `main`, one commit, then
  `graduated_probe_programs(repo, head, change_id)` and
  `check_adversarial_proportionate(repo, head, change_id, [])` (the rule
  finalize-review calls, `loom-code/scripts/loom_checker/command_handlers/finalize.py:167`)
  from the clean copy at 7a19c5a9. Driver: a scratch `drive.py`; change id
  `2026-09-25-acceptance-scratch`.
- `r52` — `git clone --no-checkout` of the project; `refs/heads/main` and
  `refs/remotes/origin/main` set to 23dad634 (= d10223e3^); branch `pr52`
  checked out at d10223e3 (PR #52's merge); change id
  `2026-09-25-tests-live-in-tests-folders`.

A new probe in the scenarios is a file whose docstring holds `concern: boundary`
and one passing test.

## 1. A change that moves or renames test files carrying a `concern:` line, and adds no probe of its own, passes the probe-program cap in finalize-review.
- How I tried it: in `repo`, confirmed five suite tests carry a `concern:`
  line at the base (`_carries_concern` → True for
  `loom-code/tests/test_acceptance_test_report_shape.py`,
  `test_adversarial_change_store_programs.py`, `test_fix_handoff_text.py`,
  `test_fix_scope_text.py`, `tests/test_tests_folder_convention.py`). Branch
  `a1-move-rename`: `git mv` the four loom-code ones into
  `loom-code/tests/moved/`, renamed the fifth to
  `tests/test_tests_folder_convention_renamed.py`, committed.
  Then replayed PR #52 in `r52` with the checker at 7a19c5a9 and, for
  contrast, with the checker at d10223e3 (the code PR #52 shipped with).
- What came back:
  ```
  == a1-move-rename
    counted (0): []
    cap rule: passes
  checker from at: HEAD d10223e3 counted 1
     tests/test_tests_folder_convention.py
    cap rule: passes
  checker from r52: HEAD d10223e3 counted 9
     loom-code/tests/test_acceptance_test_report_shape.py
     loom-code/tests/test_adversarial_auto_skip_portability.py
     loom-code/tests/test_adversarial_case_count_scan.py
     loom-code/tests/test_adversarial_change_store_programs.py
     loom-code/tests/test_adversarial_narrow_delta_waiver.py
     loom-code/tests/test_adversarial_probe_cap_coverage.py
     loom-code/tests/test_fix_handoff_text.py
     loom-code/tests/test_fix_scope_text.py
     tests/test_tests_folder_convention.py
    cap rule: [('adversarial.proportionate', '9 probe programs for this change (...); at most 5 are allowed')]
  ```
- Evidence: PR #52 replay count 1 (expected 1), was 9 before the fix. Covering
  tests `loom-code/tests/test_adversarial_probe_cap_coverage.py::test_moved_concern_tests_are_not_counted`
  and `::test_moved_with_a_small_edit_is_still_a_move` passed (run below).

## 2. A change that adds a new probe program into the suite, including one copied from an existing probe under a new name, is still counted, and more than five still makes finalize-review refuse it.
- How I tried it: branches in `repo`: `a2-new-probe` (one new probe at
  `loom-code/tests/test_zz_new_probe.py`); `a2-copy` (copied
  `test_fix_handoff_text.py` to `test_fix_handoff_text_copy.py`, original
  kept); `a2-rename-plain` (`git mv` of `test_adversarial_agy_adapter.py`,
  which carries no `concern:` at the base, to `test_zz_renamed_plain.py`, with
  `# concern: boundary` prepended); `a2-six` (six new probes); `a2-five` (five
  new probes, the limit).
- What came back:
  ```
  == a2-new-probe     counted (1): ['loom-code/tests/test_zz_new_probe.py']            cap rule: passes
  == a2-copy          counted (1): ['loom-code/tests/test_fix_handoff_text_copy.py']   cap rule: passes
  == a2-rename-plain  counted (1): ['loom-code/tests/test_zz_renamed_plain.py']        cap rule: passes
  == a2-six           counted (6): [test_zz_six_0..5.py]
                      cap rule: [('adversarial.proportionate', '6 probe programs for this change (...); at most 5 are allowed')]
  == a2-five          counted (5): [test_zz_five_0..4.py]                              cap rule: passes
  ```
- Evidence: the output above; covering tests
  `::test_new_probes_are_counted_and_over_the_cap_refused`,
  `::test_a_copied_probe_under_a_new_name_is_counted`,
  `::test_a_rename_from_a_plain_test_is_counted`,
  `::test_moved_and_rewritten_into_a_new_probe_is_counted`,
  `::test_the_move_pairing_ignores_the_local_rename_limit` passed.

## 3. A program placed under a `tests/local/` folder is not counted as graduated into the package suite.
- How I tried it: branches in `repo`: `a3-local` (one new probe at
  `loom-code/tests/local/test_zz_local_probe.py`); `a3-six-local` (six new
  probes under `loom-code/tests/local/`). Contrast: the same probe at
  `loom-code/tests/` is counted (`a2-new-probe` above).
- What came back:
  ```
  == a3-local       counted (0): []   cap rule: passes
  == a3-six-local   counted (0): []   cap rule: passes
  ```
- Evidence: the output above; covering test
  `::test_a_program_under_tests_local_is_not_graduated` passed. The symlink
  case (a committed symlink into `tests/local/`) was not tested: plan Risk 3
  records it as a user-decided known limitation (2026-09-25), and
  `probes.py` `suite_collects` docstring states it.

## 4. The repository memory store records that moving graduated probes used to trip the cap and why PR #52 shipped unattested.
- How I tried it: read
  `docs/loom/memory/moving-graduated-probes-used-to-trip-the-probe-cap.md`;
  `grep -n moving-graduated-probes docs/loom/memory/index.md`;
  `python3 loom-workflow/skills/loom-memory/scripts/loom_memory.py validate docs/loom/memory`;
  `git cat-file -t d4dbb19c` (the fix commit the entry cites).
- What came back: the entry exists (type `gotcha`); its body says PR #52's
  finalize-review counted 9 against a cap of 5, 8 being renamed graduated
  probes and 1 new, because the branch delta is read with `--no-renames`, and
  that the review episode had used its three digests so the PR shipped with
  "Verification status: absent"; it also records the symlink known
  limitation. Index line 152 lists it. Validate:
  `loom_memory validate: OK — OKF v0.2-compatible Loom memory profile holds.`
  (exit 0). `d4dbb19c` is a commit on this branch.
- Evidence: the file, `docs/loom/memory/index.md:152`, the validate output.

## 5. The checker's rule list does not grow and no new step, reviewer or dispatch is added.
- How I tried it: `python3 loom-code/scripts/loom_checker.py --list-rules` in
  the clean copy and in a checkout of d10223e3, then `diff`;
  `python3 loom-code/scripts/check_mechanisms.py --baseline main` (main =
  d10223e3); `git diff d10223e3...HEAD -- loom-code/scripts/loom_checker/reviewers.py | wc -l`;
  `git diff --stat d10223e3...HEAD` for any SKILL.md, agent or skill file.
- What came back: 26 lines both, `diff` empty (IDENTICAL). check_mechanisms:
  skill 22/22, checker-rule 26/26, hook 10/9 (the exempt
  `PostToolUse:Skill:language-anchor.py`), contract 63/63, prose-gate 20/20,
  net 140 vs baseline 140, `all clear`, exit 0. reviewers.py diff: 0 lines.
  The branch diff touches no SKILL.md, agent or skill file (15 files:
  `probes.py`, one test module, the station-text version pin, manifests,
  CHANGELOG, READMEs, intent, plan, memory entry and index).
- Evidence: the outputs above.

## Covering tests (the package suite itself is left to finalize-review)
- Command: `python3 -m pytest -q -p no:cacheprovider loom-code/tests/test_adversarial_probe_cap_coverage.py "loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized"`
- Result: `13 passed in 4.47s`.
- Package suite command, run by finalize-review before acceptance:
  `python3 scripts/run_package_tests.py --loom-family`.
