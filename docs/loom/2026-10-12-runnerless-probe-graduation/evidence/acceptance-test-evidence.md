# Runnerless probe graduation — acceptance test evidence

Tried on 2026-10-12 in a clean local clone at `b744381d6635de98d080fa580dc06fe7be816e6a`.

## Setup

- Clean-copy command: `git clone --local --no-hardlinks /Users/kouko/GitHub/loom-plugins /private/tmp/loom-acceptance-runnerless`
- Output: `Cloning into '/private/tmp/loom-acceptance-runnerless'... done.`
- In the clone, `git rev-parse HEAD` returned `b744381d6635de98d080fa580dc06fe7be816e6a`; `git status --short` returned no entries.
- Project setup reference: `README.md:268-275` gives the isolated locked `uv` environment. The two focused commands below ran with `UV_CACHE_DIR=/private/tmp/loom-uv-cache UV_OFFLINE=1 uv run --offline --isolated --with-requirements requirements-package-tests.lock`. This confirmed the clean copy could load and execute its tests. No full package suite was run here. Finalize-review will run the full automated suite and block acceptance if it fails.

## 1. 沒有特定測試 runner、直接宣告 pytest 套件指令的專案，將抓到缺陷的對抗測試移入正式套件後，能把該檔案記為對抗執行並完成 finalization。

- How I tried it: Ran `UV_CACHE_DIR=/private/tmp/loom-uv-cache UV_OFFLINE=1 uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_suite_finalizes_a_collected_probe loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_refuses_uncollected_and_broken_suites loom-code/tests/test_selection_finalize.py::test_conda_pytest_suite_accepts_execution_and_refuses_noop loom-code/tests/test_adversarial_probe_cap_coverage.py::test_runner_root_target_collects_tests_but_respects_ignore loom-code/tests/test_runner_ignored_refused.py::test_runner_ignored_refused` in the clone.
- What came back: `..... [100%]` and `5 passed in 8.29s` (exit 0).
- Evidence: `test_runnerless_pytest_suite_finalizes_a_collected_probe` at `loom-code/tests/test_selection_finalize.py:366-383` creates a Git fixture with a direct pytest package command and no runner. It asserts finalize exit 0 and the graduated artifact in adversarial executions.

## 2. 同樣的專案若將檔案移至正式套件未收集的位置，finalization 仍會拒絕該檔案。

- How I tried it: Used the first focused command above and its `test_runnerless_pytest_refuses_uncollected_and_broken_suites` case.
- What came back: The shared command returned `5 passed in 8.29s` (exit 0).
- Evidence: `loom-code/tests/test_selection_finalize.py:419-452` asserts finalization refusal for an uncollected filename and for a pytest collection error, while confirming the test was collected before the collection error was introduced.

## 3. 已有測試 runner 的專案，在 runner 指向專案根目錄或既有測試目錄時，能正確判定正式套件是否收集該檔案。

- How I tried it: Used the first focused command above for the root runner and configured ignore cases. Then ran `UV_CACHE_DIR=/private/tmp/loom-uv-cache UV_OFFLINE=1 uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_selection_finalize.py::test_finalize_accepts_a_graduated_program_the_suite_already_runs loom-code/tests/test_adversarial_probe_cap_coverage.py::test_a_program_under_tests_local_is_not_graduated loom-code/tests/test_loom_attestation.py::test_conda_adversarial_attestation_revalidates_execution` in the clone.
- What came back: The first command returned `5 passed in 8.29s`; the second returned `... [100%]` and `3 passed in 3.79s` (both exit 0).
- Evidence: `test_runner_root_target_collects_tests_but_respects_ignore` at `loom-code/tests/test_adversarial_probe_cap_coverage.py:213-228` checks a root target and an ignored test. `test_runner_ignored_refused` at `loom-code/tests/test_runner_ignored_refused.py:15-45` checks a pytest.ini exclusion. `test_finalize_accepts_a_graduated_program_the_suite_already_runs` at `loom-code/tests/test_selection_finalize.py:344-363` finalizes a probe under the existing runner's test directory. `test_a_program_under_tests_local_is_not_graduated` at `loom-code/tests/test_adversarial_probe_cap_coverage.py:200-210` checks the runner's excluded local directory.

## 4. 透過既有 Conda 環境命令執行轉正測試的專案，能將實際執行該檔案的命令記為對抗執行；沒有執行該檔案的命令仍會被拒絕。

- How I tried it: Used the first focused command above for `test_conda_pytest_suite_accepts_execution_and_refuses_noop`, and the second for `test_conda_adversarial_attestation_revalidates_execution`.
- What came back: The commands returned `5 passed in 8.29s` and `3 passed in 3.79s`, respectively (exit 0).
- Evidence: `loom-code/tests/test_selection_finalize.py:386-416` creates a `conda` executable shim, refuses `python3 -c 0` even with the artifact argument, accepts `python3 -m pytest` for that artifact, and checks its adversarial execution record. `loom-code/tests/test_loom_attestation.py:887-905` checks attestation revalidation. The actual iCHEF repository and Conda environment were unavailable; this evidence is for the command shape and fixture behavior only.

## Full suite check reserved for finalize-review

- Project command from `README.md:274`: `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
- Expected station action: finalize-review runs the package suite on committed content and refuses the attestation on failure. This acceptance tester did not run that full command.

## Re-run on 2026-10-12, at `4e9878c8e187b4bbb89e91db1c9012a294f34e2d`

- Fix delta inspected: `git diff 5fb9ecb2..4e9878c8 -- loom-code/scripts/loom_checker/probes.py loom-code/tests`. The shared pytest collection path changed from parsing quiet stdout to a temporary pytest plugin that records selected item paths. All four Acceptance lines depend on this path, so all were re-tested in full.
- Clean-copy command: `git clone --local --no-hardlinks /Users/kouko/GitHub/loom-plugins /private/tmp/loom-acceptance-runnerless-rerun`.
- Output: `Cloning into '/private/tmp/loom-acceptance-runnerless-rerun'... done.` In that clone, `git rev-parse HEAD` returned `4e9878c8e187b4bbb89e91db1c9012a294f34e2d`; `git status --short` returned no entries.
- Setup and focused test command, run in that clone: `UV_CACHE_DIR=/private/tmp/loom-uv-cache UV_OFFLINE=1 uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_suite_finalizes_a_collected_probe loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_refuses_uncollected_and_broken_suites loom-code/tests/test_selection_finalize.py::test_conda_pytest_suite_accepts_execution_and_refuses_noop loom-code/tests/test_selection_finalize.py::test_finalize_accepts_a_graduated_program_the_suite_already_runs loom-code/tests/test_adversarial_probe_cap_coverage.py::test_runner_root_target_collects_tests_but_respects_ignore loom-code/tests/test_adversarial_probe_cap_coverage.py::test_a_program_under_tests_local_is_not_graduated loom-code/tests/test_runner_ignored_refused.py::test_runner_ignored_refused loom-code/tests/test_loom_attestation.py::test_conda_adversarial_attestation_revalidates_execution`.
- Output: `........ [100%]`; `8 passed in 13.31s`; exit 0. This also confirms the clean copy loaded the project's locked test environment. The full package suite was not run; finalize-review will run it before acceptance and block on failure.
- 1: re-tested — `test_runnerless_pytest_suite_finalizes_a_collected_probe` (`loom-code/tests/test_selection_finalize.py:366-387`) declares a direct pytest suite without a runner, sets `-q` in both pytest.ini and `PYTEST_ADDOPTS`, then asserts finalization succeeds and the artifact appears in adversarial executions.
- 2: re-tested — `test_runnerless_pytest_refuses_uncollected_and_broken_suites` (`loom-code/tests/test_selection_finalize.py:424-457`) asserts an uncollected neighbor is refused, then a selected file is recognized, and then collection failure makes finalization refuse it.
- 3: re-tested — `test_runner_root_target_collects_tests_but_respects_ignore` (`loom-code/tests/test_adversarial_probe_cap_coverage.py:213-228`) checks a root target; `test_runner_ignored_refused` (`loom-code/tests/test_runner_ignored_refused.py:15-45`) checks both selected and ignored files with pytest.ini `addopts = -q --ignore=...`; `test_finalize_accepts_a_graduated_program_the_suite_already_runs` (`loom-code/tests/test_selection_finalize.py:344-363`) checks successful finalization under the existing test-directory runner; `test_a_program_under_tests_local_is_not_graduated` (`loom-code/tests/test_adversarial_probe_cap_coverage.py:200-210`) checks its excluded directory.
- 4: re-tested — `test_conda_pytest_suite_accepts_execution_and_refuses_noop` (`loom-code/tests/test_selection_finalize.py:390-421`) sets pytest.ini `-q`, accepts a shimmed Conda pytest command that executes the artifact and records the execution, and refuses a `python3 -c 0` command with the artifact merely appended. `test_conda_adversarial_attestation_revalidates_execution` (`loom-code/tests/test_loom_attestation.py:887-905`) checks later validation. No live iCHEF repository or Conda environment was available.
