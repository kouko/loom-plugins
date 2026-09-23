# Make acceptance testing lighter without losing what only it catches — acceptance test evidence

Tried on 2026-09-23, in a clean copy of the project at e43b6b11.

## Setup check (every run)
- How I tried it: `git worktree add --detach <scratchpad>/at-wt HEAD` (HEAD e43b6b11, `git status --short` empty); followed the root README "Install" section. Installing into the user's real Claude Code would replace their installed copy, so I loaded the plugin from the clean copy instead: `claude plugin validate ./loom-code`, then `python3 loom-code/scripts/loom_checker.py --list-rules`, `reviewer-count 2026-09-23-lighter-acceptance-testing`, `selection show 2026-09-23-lighter-acceptance-testing`.
- What came back: `✔ Validation passed` (exit 0); the checker listed its rules; `reviewer-count` printed `2` (exit 0); `selection show` printed the selection JSON (exit 0).
- Evidence: captured output above. Worktree removed afterwards (`git worktree remove --force`); `git worktree list` no longer shows it.

## 1. The acceptance tester does not run the full package suite; a criterion the suite settles cites the finalize-review result instead. A setup check from a fresh clone still runs every time.
- How I tried it: dogfood — ran this acceptance test under the branch's contract (`loom-code/agents/acceptance-tester.md` steps 1, 2, 6). Did not run the package suite; ran only the tests covering this line: `python3 -m pytest -q loom-code/scripts/test_acceptance_test_report_shape.py "loom-code/scripts/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized"`. Read `acceptance-tester.md:39-51` (step 6) and `closing-review/SKILL.md:218-221`.
- What came back: `24 passed in 0.22s`. Step 6 says "Never run the full package suite", and a suite-settled row "cites the suite command and says `finalize-review` executes it and refuses the attestation when it fails". Step 2 says the setup check "happens on every run, re-runs included". Following it was practical: the full suite was never needed to reach a verdict here.
- Evidence: the pytest output; `test_suite_criterion_cites_finalize_review_command`, `test_no_full_suite_run_instruction`. Suite command for the full package: the repository's declared test command, which `finalize-review` executes (`command_handlers/finalize.py:132-136`) and refuses the attestation on failure; the orchestrator reports it exited 0 at e43b6b11.
- Gap: the intent says "cites the finalize-review result"; the contract (and plan Risk 1) has the row cite the check instead, because the report is committed before finalize-review runs. Also the contract allows a worktree where the intent says "fresh clone".
- Verdict basis: `works`.

## 2. The report the user reads holds one row per criterion (verdict and one plain sentence), the decisions made on the user's behalf, and the open questions; the evidence behind each row lives in a separate file under the change's evidence directory.
- How I tried it: wrote this change's own report from `references/acceptance-test-report.md` (template lines 22-68, evidence shape lines 72-95), with the evidence in this file. Committed a plain `.md` file at `docs/loom/2026-09-23-lighter-acceptance-testing/evidence/acceptance-test-evidence.md` in the scratch worktree and ran `check_adversarial_proportionate` + `committed_probe_programs` (scratchpad `prop.py`). Negative control: same path with `#!/bin/sh` as first line. Read `land.py:_acceptance_line` (reads only the report path) and `reviewers.py:59-72` (paths under `docs/loom/<change-id>/` are low risk).
- What came back: plain `.md`: `stored programs: []`, `findings: []`. `#!` control: `adversarial.proportionate` refuses it as "a program in this change's store outside .../evidence/probes/" — which matches the template's "never starting with `#!`". The report came out at 48 lines (including three sections the template lacks, see below) versus about 100 lines median before.
- Evidence: captured output above; `test_template_has_one_row_per_criterion_and_evidence_file_path`, `test_evidence_file_shape_is_given_and_is_plain_markdown`, `test_template_row_carries_no_how_or_evidence_cell` passed in the run under line 1.
- Not tried: a full `finalize-review` and `land` run — finalize-review needs reviewer verdicts not yet produced and executes the package suite; land merges a PR. Their behaviour on the evidence file is from the code read and the proportionate check above.
- Friction found while writing (see report "I decided for you"): (a) the contract says the report's section list is the manifest charter's `must` column (`contract/manifest.yaml:211-216`: adds "Review summary" and "Questions I asked you"), which the template lacks; (b) the contract requires a list of whether the English rule held per artifact, and the template has no section for it; (c) step 6 says a suite-settled row "cites the suite command", while the template forbids commands in the report.
- Verdict basis: `works`.

## 3. A re-run after a fix tests only the criteria the fix could affect, marks every other verdict as carried over from the earlier run, and gives a one-line reason for each carried-over verdict. A criterion that is re-tested is re-tested in full — every surface the Acceptance line names — never only the part the fix touched.
- How I tried it: this is a first run, so no real re-run happened. Read step 7 (`acceptance-tester.md:52-57`), the dispatch inputs (`:17-19`), `closing-review/SKILL.md:222-226`, template Re-run column and the evidence file's re-run section. Read as a cold tester: which rows to re-test (those the fix could affect, judged against the fix diff), how far (every surface the line names), what to write for the rest (`carried over — <reason>`), and what to do when unsure (re-test in full). Ran the covering tests in the run under line 1.
- What came back: the rule reads unambiguously for criteria rows. Two small gaps: it speaks of "criteria" while the template also puts spec UI-flow rows in the table (a product change's UI-flow row on a re-run is not named); and "the setup check" is not a row, but step 2 covers it on every run.
- Evidence: `test_rerun_retests_every_named_surface`, `test_partial_surface_retest_forbidden`, `test_rerun_dispatch_passes_earlier_report_evidence_and_fix_range`, `test_row_has_carried_over_marker_with_reason`, `test_retested_row_has_no_carry_reason` passed.
- Verdict basis: `partly` — the rules and structure are in place and tested, but no real re-run after a fix has been exercised.

## 4. These rules are carried by the acceptance tester's contract and the report template's own structure, and the checker's rule list does not grow.
- How I tried it: `python3 loom-code/scripts/loom_checker.py --list-rules | grep -c .` in the clean copy at e43b6b11 and in a second clean worktree at `main` (6fe96189); `git diff --stat main...HEAD -- loom-code/scripts/loom_checker loom-code/contract`; `git diff main...HEAD | grep -n 'gate:'`.
- What came back: 26 rules on both; no diff under the checker or the contract; the only `gate:` hits are inside the new test asserting no new gate marker (diff lines 605-608).
- Evidence: captured counts; `test_rules_live_in_contract_and_template`, `test_no_new_gate_marker` passed.
- Verdict basis: `works`.

## English rule and naming, per artifact
- Plan: English, apart from the two user answers quoted verbatim under "Questions asked" (`plan.md:42-43`).
- Spec: none (`needs-design: no`); EARS `REQ-<n>` rule not applicable.
- Reviewer findings: none handed to me; Conventional Comments label not checkable yet.
- Evidence: this file, English.
- Test docstrings: English (`test_acceptance_test_report_shape.py` checked for CJK: none).
- Test names: the 10 graduated probes follow `test_<unit>_<state>_<expected>` (e.g. `test_suitecheck_pytestoverwholepackage_turnsred`); the 13 plan tests are sentence-style (e.g. `test_template_has_one_row_per_criterion_and_evidence_file_path`) without a clear state/expected split.
- Commit messages: 9 commits `main..HEAD`, English Conventional Commits, no CJK.
