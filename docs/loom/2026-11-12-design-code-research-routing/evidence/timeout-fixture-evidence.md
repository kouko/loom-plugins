# Timeout fixture verification

W3-01 supports package verification; it does not change research behavior or
production external-review behavior. Only the two existing test files changed.

## Diagnosis and bounds

The orchestrator measured cold fake-CLI Python startup at 2.826s (locked Python
3.12.8) and 2.829s (installed Python 3.15.2). Its untouched-base reproduction
is in `/private/tmp/loom-research-baseline-timeouts.log`; the serial and no-worker
reproductions are `/private/tmp/loom-research-build-suite-serial.log` and
`/private/tmp/loom-research-no-worker-timeouts.log`.

Reading `external_review.py::_launch` confirmed that deadlines begin after
Popen, cover asynchronous stdin writes, and finally kill the process group,
wait for the parent and join pipe threads. Normal parent exit receives pipe
reader grace rather than becoming a discovery timeout.

The revised live fixtures allow 6s for discovery/review and 5s for the probe
(the existing profile requires probe < review). These exceed measured startup;
60s fixture hangs outlast every elapsed assertion. Descendants use `/bin/sleep`
to avoid a second interpreter startup. Elapsed bounds remain 9s for discovery
timeout, 8s for normal exit, and 15s for probe plus review. Existing PID assertions
prove timeout fixtures actually started and descendants died. The large-prompt
test additionally records its review-branch PID after reading only 4096 bytes,
proves that branch ran with the rest of the 1MiB input blocked, and checks death.

Full-file sweep retained exact mocked timeout assertions. The remaining live
1s timeout checks only the printed timeout closing line, for which a startup
timeout exercises the stated behavior. The adversarial 2s discovery fixture uses
`/bin/sh`, so it has no fake-Python startup dependency.

## Commands and observations

Working directory: `/private/tmp/loom-design-code-research`.

RED:
```sh
uv run --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py -k 'times_out_when_app_server_never_answers or agy_discovery_times_out or lingering_descendant_is_not_timeout or review_stage_times_out or unreadPrompt'
```
Result: all five named cases failed; 139 deselected, 10.50s.
Log: `/private/tmp/loom-timeout-fixture-red.log`.

An initial revised full-file run had 142 passes and two invalid-explicit-profile
failures because probe and review limits were both 6s. Correcting the test-only
probe to 5s preserved the existing production validation.

GREEN:
```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_external_review.py loom-code/tests/test_external_review_adversarial.py
```
Result: **144 passed in 72.31s**.
Log: `/private/tmp/loom-timeout-fixture-green.log`.

## Negative sensitivity

Copied existing scripts/tests to `/private/tmp/loom-timeout-mutation/loom-code/`.
The sole production mutation in that throwaway copy replaced
`os.killpg(proc.pid, signal.SIGKILL)` with
`os.kill(proc.pid, signal.SIGKILL)`. Revised tests were copied unchanged.

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q --basetemp=/private/tmp/loom-timeout-mutation-final /private/tmp/loom-timeout-mutation/loom-code/tests/test_external_review.py -k 'agy_discovery_times_out or lingering_descendant_is_not_timeout or review_stage_times_out'
```

Result: **3 failed, 132 deselected in 34.64s**, each specifically
`Failed: descendant still running`:

- `test_agy_discovery_times_out_when_descendant_holds_stdout`
- `test_agy_discovery_exit_with_lingering_descendant_is_not_timeout`
- `test_review_stage_times_out_when_descendant_holds_stdout`

Log: `/private/tmp/loom-timeout-fixture-mutation-final.log`. This proves descendant
cleanup sensitivity; it does not claim the descendant-free Codex fixture or
blocked-input fixture detects parent-only termination. An earlier mutation run
before correcting equal profile limits is retained in
`/private/tmp/loom-timeout-fixture-mutation.log` and is not the final evidence.

Only PID-file-owned descendants were inspected and cleaned. Initial recorded
PIDs 64605/64737 had already exited. Final PIDs 65089/65202/65324 were confirmed
as `/bin/sleep 60`; after targeted cleanup `ps` returned no remaining entries.
Sandbox-required inspection/kill retries used escalation; no broad process kill.

Production defaults and real-tree scripts remain unchanged. Full package-suite
verification remains the orchestrator's integration step.
