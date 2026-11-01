# Simple hooks without checker package checks — acceptance test evidence

Tested on 2026-10-30 in a fresh local clone at `f488d6c29010180dce164ae30f2b19c09b34370c`.

## Clean-copy setup and scope

- Source: `git clone --quiet --no-local --no-hardlinks /private/tmp/loom-simple-hooks-python-dependencies /private/tmp/loom-simple-hooks-acceptance-f488d6c2`. `git worktree add` first failed because the shared Git metadata was outside the writable sandbox; the clone did not reuse the worked tree or its uncommitted artifacts.
- Verification: `git rev-parse HEAD` returned `f488d6c29010180dce164ae30f2b19c09b34370c`; `git status --short` returned no lines. `python3 --version` returned `Python 3.15.0`; `uv --version` returned `uv 0.13.1`. All four host hook JSON files parsed with `python3 -m json.tool` (exit 0).
- The README's end-user instructions install plugins into Claude Code, Codex, Antigravity, or OpenCode. This test invoked the committed hook commands from the clean clone under `/bin/sh` and `/bin/zsh`; it did not alter any live host installation or user project. Tests set `XDG_CACHE_HOME` and, where applicable, `TMPDIR` to pytest temporary directories. Thus host CLI integration itself was not exercised.
- The first focused `uv run` was blocked from writing its default cache by the sandbox (`Could not acquire lock ... Operation not permitted`). The same command was then run with approved cache access. This was a test-environment access issue, not a hook failure.

## 1. Standard-library hooks work without a Loom runtime

- How I tried it: in the clean clone, ran `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -v loom-code/tests/test_hooks_json.py -k 'test_stdlib_hooks_keep_context_with_cold_cache or test_publication_hooks_keep_checker_refusal_in_zsh or test_missing_ready_runtime_reports_repair_without_checker_refusal or test_json_hosts_return_failure_diagnostic_when_runtime_missing or test_hook_exit_code_capture_avoids_readonly_shell_name'`.
- What came back: the five `test_stdlib_hooks_keep_context_with_cold_cache` cases passed for Claude Code's three anchor events, OpenCode's skill event, and Antigravity's pre-invocation event. Each case used an empty `XDG_CACHE_HOME`, required exit 0, checked the prior context in JSON output, and rejected the `loom-python: checker runtime is missing or invalid` diagnostic. The same test also checked the ready-runtime fallback when host Python was unavailable.
- Evidence: the focused run returned `30 passed, 24 deselected in 2.61s` (exit 0); case implementation and assertions are at `loom-code/tests/test_hooks_json.py:389-435`. `test_broken_host_python_uses_ready_runtime` additionally passed in the 127-test focused run, proving that a broken host Python does not suppress a usable cached runtime (`loom-code/tests/test_broken_host_python_fallback.py:24-53`).

## 2. Checker-backed publication hooks retain their failure policy

- How I tried it: used the same named focused run to execute the publication commands for Claude Code, Codex, OpenCode, and Antigravity under `/bin/zsh`, with a temporary checker that exits 17. I also exercised missing-runtime cases with an empty temporary cache and publication payload.
- What came back: `test_publication_hooks_keep_checker_refusal_in_zsh` passed for all four hosts; each command propagated exit 17. `test_missing_ready_runtime_reports_repair_without_checker_refusal` passed for Claude Code: exit 0 plus a publication-hook failure and `--repair` diagnostic. `test_json_hosts_return_failure_diagnostic_when_runtime_missing` passed for OpenCode and Antigravity: exit 0 and a JSON diagnostic containing `--repair`.
- Evidence: named `PASSED` lines and the final `30 passed` result in the focused run; assertions at `loom-code/tests/test_hooks_json.py:328-386`. The existing Claude/Codex checker routing assertions also passed in the 127-test focused run (`loom-code/tests/test_hooks_json.py:103-146`). The tests sent payload strings to hooks; they did not execute a real `git push`.

## 3. Host events, output, exit status, and package tests remain intact

- How I tried it: ran `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_hooks_json.py loom-code/tests/test_broken_host_python_fallback.py loom-code/tests/test_check_mechanisms.py` in the clean clone. The named focused run above also covered both `/bin/sh` and `/bin/zsh` with a readonly `status` variable for Claude Code, Codex, OpenCode, and Antigravity hook commands.
- What came back: the focused file set returned `127 passed in 9.99s` (exit 0). All 18 named readonly-shell host/event cases passed. Manifest event and matcher assertions, hook JSON output assertions, cached-runtime fallback cases, and mechanism identity checks were included in the 127 tests.
- Evidence: `loom-code/tests/test_hooks_json.py:66-100,214-255,268-435`, `loom-code/tests/test_broken_host_python_fallback.py:24-53`, and `loom-code/tests/test_check_mechanisms.py`. The closing-review station separately reported that the complete Loom-family package suite was run after the final functional commit at this HEAD, using `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`, and exited 0. Its visible code group was `2468 passed, 2 skipped`; the design group was `204 passed, 1 skipped`; remaining groups exited 0. The complete suite was not rerun by this acceptance tester, as the acceptance-tester contract assigns it to `finalize-review`.

## Findings and data handling

- No acceptance failure or important finding was observed. The closing-review station reported no dismissed finding of important severity or higher. The package suite and finalization were not omitted; the suite result above includes individual skipped test cases.
- The probes used a clean clone and temporary directories. No user project data, real hook installation, or user map was changed.
