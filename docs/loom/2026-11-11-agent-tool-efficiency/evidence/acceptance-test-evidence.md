# Agent tool efficiency — acceptance test evidence

Test date: 2026-11-12. Tested commit: `0dcaa4bda4bc2ed44e567e883ab0f357ed1c64b8`.
Independent tester used `/private/tmp/loom-efficiency-acceptance-clean`, cloned with `git clone --no-hardlinks /private/tmp/loom-agent-tool-efficiency /private/tmp/loom-efficiency-acceptance-clean` and checked out detached at the exact commit. `git status --short` was empty before and after testing. Source worktree HEAD remained identical when the report was written.
Functional content digest: `58ad98b9d6a93338be10dc1c022a3767c47859e2`, recomputed using `loom_checker.digest.functional_content_digest` for the tested commit and this change ID.
Lock SHA-256: `cf3ab93fbdf6b745f4ab42e9866d1e5e78cc5f013021293c59d6bce4b680143a`.

## Clean setup and source load

Followed README Development dependency instructions, with the full package suite reserved for finalization. Initial sandboxed uv attempts could not write the user cache; an empty temporary cache could not resolve PyPI DNS. An approved escalated invocation using the existing cache succeeded. This was a clean source checkout using a shared locked dependency cache, not a fresh dependency download or installed-host update.

Commands, all from the clean checkout:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python loom-code/scripts/loom_checker.py --list-rules
python3 scripts/sync_codex_manifests.py --check --all
python3 scripts/check_plugin_boundaries.py loom-code
python3 scripts/check_plugin_boundaries.py loom-design
python3 loom-code/scripts/check-skill-crossrefs.py
```

All exited 0. The actual CLI loaded and printed rules beginning with `adversarial.proportionate`, `ci.pr-floor`, and `contract.charter-complete`. Boundary checks printed `OK: loom-code is filesystem-boundary clean.`, `OK: loom-design is filesystem-boundary clean.`, and `OK: all relative skill cross-references resolve.` Manifest synchronization exited 0 silently. CLI output retained at `/private/tmp/loom-acceptance-load.log`.

## 1. Progress, result compatibility and truthful terminal states

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_publish.py loom-code/tests/test_selection_finalize.py -k 'progress or stdout_unchanged or exit_zero_invalid_evidence or observes_required_ci or stops_on_required or registration or initial_empty or initial_successful or unexpected_ci or malformed_json or permanent_pending' -v
```

Captured result: `32 passed, 110 deselected in 15.89s`; log `/private/tmp/loom-acceptance-a1.log`.

- `test_finalize_progress_before_child_exit` ran the actual source CLI in a separate process with stdout/stderr pipes and a child blocked on a release file. `select` observed `finalize-review: package-tests started\n` while `process.poll()` remained `None`; only then did the test release the child. Final stdout began `wrote `; exit was 0; package/adversarial started/passed records matched exactly. This is real process/pipe timing, not a mocked flush claim.
- `test_finalize_exit_zero_invalid_evidence` ran an actual skipped pytest child: the command returned 1, emitted adversarial failed (never passed), and wrote no attestation.
- Publish tests controlled external GitHub responses and the monotonic clock. They verified registration/pending transitions, elapsed 60/120-second notices, success/no-checks/failure/unknown terminal states, unchanged stdout and exit codes, immediate observation plus ten-second polling, and the existing timeout limit. They did not contact GitHub or prove live remote behavior.
- Broken write/flush cases preserved failure and exactly one push/create attempt. Finalization write/flush failures covered success, nonzero exit, timeout and execution error. Progress is not used as verification evidence.

## 2. Concern-first collection and retained exceptional cases

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_selection_finalize.py loom-code/tests/test_probe_language_suite_collection.py -k 'collection or graduated or ordinary or collected or concern or uncollected' -v
```

Captured result: `45 passed, 45 deselected in 15.42s`; log `/private/tmp/loom-acceptance-a2.log`.

`test_ordinary_files_skip_collection` checks zero collection calls for ineligible files. `test_marked_moved_unknown_collection` checks marked/moved paths and true/false/unknown collection decisions. Actual finalizer and suite-discovery cases cover collected and uncollected programs, configured pytest file names, declared environments, unmarked executed probes, probe caps, Cargo manifest errors and Go package selection. These are exercised tests, not conclusions inferred only from predicate order.

## 3. Exact documented conversion replay

Executed both commands from the comparison document verbatim, after the progress and collection test invocations:

```sh
python3 -c 'from pathlib import Path; p=Path("docs/loom/2026-11-11-agent-tool-efficiency/evidence/conversion-comparison.md"); Path("/private/tmp/loom-conversion-replay.py").write_text(p.read_text().split("```python\n",1)[1].split("\n```",1)[0]+"\n")'
uv run --isolated --with-requirements requirements-package-tests.lock python /private/tmp/loom-conversion-replay.py --replay > /private/tmp/loom-conversion-replayed.json
```

Both exited 0. A separate comparison asserted exact equality of `case`, `arm`, `exit_code`, `stdout`, `stderr`, and `passes_finalizer_verdict_predicate_only` against committed `conversion-results.json`, for all 16 records. Output: `Exact semantic replay: 16 runs; 0dcaa4bda4bc2ed44e567e883ab0f357ed1c64b8`. Function footprint: baseline 6 lines, candidate 15 lines (including blanks/comments as documented).

Both methods convert valid and matching-identity data and retain rejected verdicts. Both reject malformed YAML/shape; candidate additionally rejects duplicates, missing identity and conflicting identity. Baseline duplicate behavior keeps the last rejected verdict. Context and provenance retention assertions passed. Interpreter paths/HEAD metadata were intentionally excluded from equality. No conversion is a complete finalization acceptance proof. Five semantic caller tasks remain in both arms; model time/token savings were not measured. The retained recommendation against production integration is consistent with the replay.

## 4. Authorization, independent-review and acceptance floors

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_loom_publish.py loom-code/tests/test_selection_finalize.py loom-code/tests/test_ship_station_text.py -k 'authorization or revalidates or refuses or refused or skipped or floors or binds_the_report or accepted or usage_error or ship' -v
```

Captured result: `39 passed, 113 deselected in 18.20s`; log `/private/tmp/loom-acceptance-a4.log`.

Explicit floor follow-up (the broad selector did not name these two functions):

```sh
uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_selection_finalize.py::test_v2_without_selection_keeps_every_floor loom-code/tests/test_selection_finalize.py::test_mechanical_verification_without_a_report_keeps_evidence_boundaries -q
```

Captured result: `4 passed in 7.32s` (parameterized cases), for 43 A4 checks total. This verifies the no-selection floors and the distinction between mechanically verified and independently accepted evidence explicitly.

Cases exercised publication authorization, live identity/head/remote revalidation with controlled external responses, acceptance report verdict binding, skipped-reviewer refusal, retained verification floors, usage/dirty-tree refusal, and Ship station guidance. A1 additionally exercised broken-progress mutation counts and false-success rejection; A2 exercised probe caps and unmarked executed-program refusal. No production fixes or remote mutations were performed. No important-or-higher dismissed findings were supplied to this tester.

The package suite was deliberately not run by this acceptance role. The station confirmed finalization will execute the unskipped full suite and block on failure:

```sh
uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q
```

This report claims the focused results above, not a future package-suite result, installed-host update, real GitHub validation, or end-to-end model cost improvement. No executable probe was added to the repository.
