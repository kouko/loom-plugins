# Stop feedback — acceptance test evidence

Tried on 2026-11-11, in a clean copy of the project at 0c65e553637bf7924cb16b24a28017ab85a14a67.

## Clean setup and scope

- Independent tester; no implementation changes. `git worktree add --detach /private/tmp/loom-stop-acceptance-clean 0c65e553637bf7924cb16b24a28017ab85a14a67` failed because the sandbox prohibited writing the shared Git worktree directory. Used `git clone --no-hardlinks /Users/kouko/GitHub/loom-plugins /private/tmp/loom-stop-acceptance-clean` then `git checkout --detach 0c65e553637bf7924cb16b24a28017ab85a14a67`. `git status --porcelain` was empty and `git rev-parse HEAD` matched the exact requested SHA.
- Read README Install and Development instructions. Marketplace installation into the user's normal hosts was excluded by the task; no installed plugin adoption claim is made. Used the documented isolated dependency environment and the actual plugin launcher in the clean copy.
- First offline pytest attempt could not lock the default uv cache under sandbox. Authorized escalation allowed existing offline cache access. First temporary runtime provisioning with only `XDG_CACHE_HOME` redirected uv into an empty cache, producing `pyyaml was not found in the cache`; no code was changed. Retried with the real cache explicitly selected:
  `env XDG_CACHE_HOME=/private/tmp/loom-stop-acceptance-runtime UV_CACHE_DIR=/Users/kouko/.cache/uv UV_OFFLINE=1 loom-code/scripts/loom-python --repair --help`.
- Setup result: exit 0; isolated Python 3.11.14 runtime with PyYAML 6.0.2 installed; checker command help rendered. This validates local launcher setup, not host marketplace installation.
- Focused command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_delivery_stop.py loom-code/tests/test_delivery.py loom-code/tests/test_loom_publish.py loom-code/tests/test_hook_recovery_literal_path.py loom-code/tests/test_hooks_json.py`.
- Captured result: `182 passed in 108.80s (0:01:48)`; exit 0. These are local controlled tests, including mocked remote observers, not actual remote publication or installed host execution.
- Full package suite was NOT run by this tester. The station will run `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` through finalize-review; that automated check blocks acceptance on failure. No committed `skipped-by-instruction` records were found in this change's intent or plan.

## 1. Quiet work and human waits

- Executed the exact `Stop[0].hooks[0].command` read from each packaged hook JSON using `subprocess.run(..., shell=True, input=json.dumps(payload), text=True, capture_output=True, env=env)`, with clean-clone plugin root and isolated runtime cache. Payload included `hook_event_name: Stop`, the clean clone cwd and `stop_hook_active: true`.
- Claude used `CLAUDE_PLUGIN_ROOT`; Codex used `PLUGIN_ROOT`. Both returned exit 0, stdout `''`, stderr `''`. Claude with `background_tasks: [{id: running}]` also returned exit 0 with both streams empty.
- An initial Codex invocation incorrectly supplied `CODEX_PLUGIN_ROOT`, so the shell tried `/scripts/loom-python` and emitted the wrapper's explicit runtime failure warning. Correcting the tester environment to the manifest's `PLUGIN_ROOT` produced the silent result. This demonstrates an actual launch failure and is not attributed to the product repair.
- `test_pause_metadata_only_suppresses_valid_pauses`, `test_unready_work_stops_before_remote` and `test_premature_stop_and_repeat_disclose_actual_incompletion` passed across their host/state parameters. The last test confirms conditional human-wait guidance, not detection of pending human questions. A valid committed review while waiting for a human can still produce one initial continuation. No real host UI pass is claimed.

## 2. Preserve incomplete, unconfirmed and completed delivery

- Passed focused `test_delivery.py` tests: `test_matching_remote_pr`, `test_newer_local_head`, `test_missing_authorization`, `test_checks_pass`, `test_failed_json`, `test_unavailable_remote`, and the other tests in that module.
- Passed `test_single_total_deadline_is_unconfirmed_and_does_not_continue`, `test_changed_head_cannot_continue` and publication tests. Missing evidence remained unconfirmed; no absence was accepted as success. The automated full suite is a later blocking check, not a result asserted here.

## 3. Host distinction and unverified boundaries

- Reviewed committed `host-framing.md`, the readiness research and the existing native probe receipts under `/private/tmp/stop-host-probe`. Did not rerun accounts, switch providers, bypass trust or modify settings.
- Actual saved Codex `block-events.jsonl`: first Stop `stop_hook_active: false`, last message `FIRST`; second Stop `true`, last message `SECOND`; same turn ID. `feedback-events.jsonl`: one Stop `false`, last message `FIRST`. This is the earlier synthetic protocol experiment on Codex 0.167.0, not this repaired plugin end to end, and not interactive UI validation.
- Actual saved Claude result: `type: result`, `subtype: success`, `is_error: true`, result `You've hit your 5-hour limit · resets 4:20pm (Asia/Taipei)`, `total_cost_usd: 0`. The outer subtype does not negate the explicit error; no Stop event executed. Claude 2.1.322 repaired-plugin behavior remains unverified.
- Distinction: the tester's wrong-variable launch above is an execution failure; Codex block is intentional continuation; the Claude display correction is source-contract supported but not natively observed. No important-or-worse dismissed findings were supplied by the station.

## 4. UI flow: No applicable change

- `test_user_boundaries_and_irrelevant_hooks_can_stop` passed: irrelevant events, withdrawn authorization and product confirmation boundaries remain silent without a success claim.

## 5. UI flow: Work in progress

- Exact Claude packaged command with a valid background-task payload returned silent exit 0. `test_pause_metadata_only_suppresses_valid_pauses` passed scheduled wakeups, malformed metadata and Codex-specific treatment. Native Claude presentation remains unverified.

## 6. UI flow: Unverified or pending work

- `test_unready_work_stops_before_remote` passed absent, stale and locally pending states for both hosts and asserted zero remote calls. `test_changed_head_cannot_continue` passed concurrency variants.

## 7. UI flow: Explicit skip without verification

- `test_unready_work_stops_before_remote` skip variants passed for both hosts. `test_good_body_without_attestation_publishes_with_reminder`, `test_status_and_skip_lines_in_body_publish` and `test_skipped_steps_line_not_enforced` passed in the publication module. No new explicit-publication restriction was introduced; missing/stale verification still requires existing disclosure. These use controlled Git/remote fixtures, not an actual publish.

## 8. UI flow: First premature finish

- `test_premature_stop_and_repeat_disclose_actual_incompletion` passed Claude additionalContext and Codex/legacy block responses with user-wait/withdrawal guidance. Actual repaired-plugin continuation remains unverified on both hosts; the pre-repair synthetic Codex protocol is supporting evidence only.

## 9. UI flow: Continued turn or human wait

- Both packaged commands returned silent exit 0 on repeated Stop. Tests ensure no further observer lookup. No live model was used to verify that an agent explains a pending decision, nor that the first eligible continuation is absent while waiting.

## 10. UI flow: Evidence unavailable

- `test_single_total_deadline_is_unconfirmed_and_does_not_continue` passed deadline, unavailable-result and observer-exception cases on both hosts: systemMessage only, no continuation, recovery command retained. Literal recovery and packaged hook tests passed. Native warning presentation remains unverified.

## 11. UI flow: Published

- `test_user_boundaries_and_irrelevant_hooks_can_stop`, `test_matching_remote_pr`, `test_checks_pass` and publication tests passed exact publication/CI fixtures and silent published Stop behavior. No real remote was changed or merged.

## 12. UI flow: Actual host execution blocked

- Re-read the saved Claude quota result described in section 3. Classified as account availability failure before Stop, not a repaired-hook pass or failure. No quota retry or alternative provider was attempted.

## Findings and limits

- Important validation gap: native Claude repaired-plugin display and both hosts' repaired-plugin end-to-end continuation remain unverified. Close with an authorized fresh-session run after account availability permits, preserving real settings and normal trust.
- Human-wait limit is retained by design: valid repository evidence cannot prove no pending human question. This report does not claim that first reminders are universally eliminated.
