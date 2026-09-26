# Flow policy consistency — acceptance test evidence

Tried independently on 2026-09-26 at commit `52a714f8785234b67c41eeaa3fa993df9d065aae`.

## Clean setup and load

- Read the root README and used its Development validation entry points. A local clone with hardlinks was denied by the filesystem sandbox; `git clone --local --no-hardlinks` succeeded into a fresh temporary directory. `git rev-parse HEAD` returned the commit above.
- All commands below ran from that clone with `/Users/kouko/.conda/envs/dbt-redshift/bin/python3` (abbreviated `PY` below), an existing interpreter containing the test dependencies. No dependency installation or global plugin installation was performed.
- `PY scripts/sync_codex_manifests.py --check --all`: exit 0, no output.
- `PY scripts/check_plugin_boundaries.py loom-code`: exit 0, `OK: loom-code is filesystem-boundary clean.`
- `PY loom-code/scripts/check-skill-crossrefs.py`: exit 0, `OK: all relative skill cross-references resolve.`
- `PY loom-code/scripts/loom_checker.py --list-rules`: exit 0; checker imported and printed the rule inventory. This verifies local development loading, not installation into a host account.

## 1. Architecture-rule changes receive protected review and automatic-skip policy

- Ran a temporary independent probe named `test_architecture_committed_change_keeps_protected_checks`. For each path below it created a fresh Git repository on `main`, committed an empty base, branched to `change`, committed a plain rules document, and invoked `required_reviewer_count` and `auto_skipped_steps` against that committed delta. Assertions required two reviewers and no automatic skips for each protected document, versus one reviewer and automatic skips for ordinary prose.
- Captured output, exit 0:

```text
ARCHITECTURE.md: reviewers=2; automatic_skips=[]
docs/architecture.md: reviewers=2; automatic_skips=[]
DESIGN.md: reviewers=2; automatic_skips=[]
PRINCIPLES.md: reviewers=2; automatic_skips=[]
docs/guide.md: reviewers=1; automatic_skips=['acceptance-test', 'adversarial', 'plan', 'spec']
```

- Also ran `test_reviewer_floor_is_one_only_for_narrow_low_risk_paths` and `test_reviewer_floor_sees_both_sides_of_a_protected_file_rename` from `loom-code/tests/test_loom_attestation.py` in the 25-test command recorded below. Both passed.
- Compatibility disclosure was checked against the 3.20.0 CHANGELOG: weak architecture-only attestations may become stale and need new review, without claiming a universal publication block.

## 2. Both Python test filename patterns execute, propagate failures, and preserve inventory boundaries

- Ran the complete criterion-specific module `tests/test_run_package_tests.py`, not the package suite. Its `test_design_group_discovers_its_tests_folder` creates suffix-named tests, excludes a suffix-named local test, replaces the included test with a failing assertion, and runs the actual package runner's design group in that fixture. It requires exit 1 and the failing test name in stdout.
- The same module runs prefix-named discovery, per-skill workflow sessions with duplicate basenames, root inventory, local-folder exclusions, nested clone/worktree exclusions, shell-group exclusions, and later-group failure propagation.
- Command covering criteria 1–3:

```sh
PY -m pytest -q \
  loom-code/tests/test_loom_attestation.py::test_reviewer_floor_is_one_only_for_narrow_low_risk_paths \
  loom-code/tests/test_loom_attestation.py::test_reviewer_floor_sees_both_sides_of_a_protected_file_rename \
  loom-code/tests/test_selection_finalize.py::test_bound_kept_adversarial_required_on_narrow_delta \
  loom-code/tests/test_selection_finalize.py::test_narrow_delta_finalizes_with_no_adversarial_artifact \
  loom-code/tests/test_selection_finalize.py::test_bound_skip_of_reviewers_and_adversarial_validates \
  tests/test_run_package_tests.py
```

Captured output: `25 passed in 18.88s`, exit 0.

- Full package suite was deliberately not run by this tester. The station states package tests are not skipped and `finalize-review` will execute them and refuse an attestation on failure. README suite command: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. Build's reported results were not substituted for independent acceptance results.

## 3. Bound kept verification survives automatic skips in production and validation

- The parameterized `test_bound_kept_adversarial_required_on_narrow_delta` above passed both cases: skipping only reviewers and keeping every step. Real Git fixtures bind confirmed selections, then exercise finalization, local attestation validation, and claimed-selection validation. All three refuse missing retained adversarial evidence, with finalization reporting `BLOCK finalize.adversarial`.
- `test_narrow_delta_finalizes_with_no_adversarial_artifact` passed unbound automatic skipping and subsequently explicit adversarial skipping; both local and claimed-selection validation accept those results.
- `test_bound_skip_of_reviewers_and_adversarial_validates` passed the explicit-skip control, preserving the existing attestation format and delivery witness.
- Checked release metadata and directly relevant station guidance with:

```sh
PY -m pytest -q \
  loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized \
  loom-code/tests/test_expert_mode_skill.py \
  loom-code/tests/test_simplified_station_text.py
```

Captured output: `76 passed in 2.31s`, exit 0.

## Decisions and limits

- No product edits were made by this tester. The report discloses the plan's minimal extension of existing policy/data, no added helper or schema, compatibility impact, minor release, and deferred unrelated issues.
- No important/fatal findings were dismissed by the main agent according to the dispatch. This tester found none.
- This is first-run acceptance; no verdicts were carried over. There is no product UI flow or spec to test for this engineering intent.
