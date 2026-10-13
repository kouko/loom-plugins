# Complete runnerless probe graduation — acceptance test evidence

Tested 2026-10-13 in a clean `git worktree add --detach` copy of `1fb7f1504806916e1073f1968e7c7b4d78236dda`. The source checkout was clean before testing. The clean copy followed README.md:270-275 and used its isolated `uv` requirements environment. The sandbox initially denied access to the host uv cache; the identical targeted command succeeded with host approval. No full package suite was run. `finalize-review` will run the package suite before attestation; its declared command is `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

Targeted batch 1 command: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_suite_finalizes_a_collected_probe loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_refuses_uncollected_and_broken_suites loom-code/tests/test_selection_finalize.py::test_conda_pytest_suite_accepts_execution_and_refuses_noop loom-code/tests/test_selection_finalize.py::test_runner_collection_uses_declared_package_environment loom-code/tests/test_adversarial_probe_cap_coverage.py::test_runner_root_target_collects_tests_but_respects_ignore loom-code/tests/test_runner_ignored_refused.py`. Output: `6 passed in 10.86s`; exit 0.

Targeted batch 2 command: `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_selection_finalize.py::test_narrow_delta_finalizes_with_no_adversarial_artifact loom-code/tests/test_selection_finalize.py::test_finalize_accepts_a_graduated_program_the_suite_already_runs`. Output: `2 passed in 3.51s`; exit 0.

## 1. 沒有特定測試 runner、直接宣告 pytest 套件指令的專案，將抓到缺陷的對抗測試移入正式套件後，能把該檔案記為對抗執行並完成 finalization。

- How I tried it: In the clean copy, ran `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_suite_finalizes_a_collected_probe`.
- What came back: The targeted test passed. Its fixture declares `python3 -m pytest -q tests` directly, commits a `concern:` probe under `tests/`, calls finalization, asserts exit 0, and checks the adversarial execution contains `tests/test_graduated_probe.py` (test_selection_finalize.py:366-388).
- Evidence: First six-test targeted batch returned `6 passed in 10.86s` (exit 0).

## 2. 同樣的專案若將檔案移至正式套件未收集的位置，finalization 仍會拒絕該檔案。

- How I tried it: The same batch ran `loom-code/tests/test_selection_finalize.py::test_runnerless_pytest_refuses_uncollected_and_broken_suites`.
- What came back: The test passed. A non-test filename was refused with `BLOCK finalize.adversarial`; after renaming it to a collectible test, breaking collection in `conftest.py` again produced a refusal with `collection unavailable` and `collection broken` (test_selection_finalize.py:424-459).
- Evidence: First targeted batch returned `6 passed in 10.86s` (exit 0).

## 3. 已有測試 runner 的專案，在 runner 指向專案根目錄或既有測試目錄時，能正確判定正式套件是否收集該檔案。

- How I tried it: The first batch ran `loom-code/tests/test_adversarial_probe_cap_coverage.py::test_runner_root_target_collects_tests_but_respects_ignore`, `loom-code/tests/test_runner_ignored_refused.py`, and `loom-code/tests/test_selection_finalize.py::test_runner_collection_uses_declared_package_environment`.
- What came back: All passed. Root-target runner accepted a test under `tests/` and excluded `tests/local/` (test_adversarial_probe_cap_coverage.py:216-233); a configured pytest ignore excluded its target (test_runner_ignored_refused.py:13-45); a runner targeting `tests` accepted the kept test and excluded the ignored one inside its declared environment (test_selection_finalize.py:462-503).
- Evidence: First targeted batch returned `6 passed in 10.86s` (exit 0).

## 4. 透過既有 Conda 環境命令執行轉正測試的專案，能將實際執行該檔案的命令記為對抗執行；沒有執行該檔案的命令仍會被拒絕。

- How I tried it: The first batch ran `loom-code/tests/test_selection_finalize.py::test_conda_pytest_suite_accepts_execution_and_refuses_noop`. I then checked `conda run -n base python -m pytest --version`, which returned `pytest 9.1.1`, and built a temporary Git fixture with `package-tests: conda run -n base python -m pytest -q tests`. In that fixture I called finalization first with `conda run -n base python -c 0 tests/test_graduated_probe.py`, then with `conda run -n base python -m pytest -q tests/test_graduated_probe.py`.
- What came back: The test passed. In the real Conda run, the no-op returned exit 1 and `BLOCK finalize.adversarial`; the executing command returned exit 0 and the generated executions listed `tests/test_graduated_probe.py` as `adversarial`.
- Evidence: First targeted batch `6 passed in 10.86s`; real Conda fixture printed `noop: 1 True`, `executing: 0`, `adversarial: ['tests/test_graduated_probe.py']`. The official command form is documented at https://docs.conda.io/projects/conda/en/stable/commands/run.html. The real Conda test used an existing environment and installed no packages.

## 5. 環境命令的辨識依據可由官方文件查核，最終審查能對已驗證的修正產生與內容相符的證明。

- How I tried it: Opened the official uv CLI reference at https://docs.astral.sh/uv/reference/cli/#uv-run and the Conda reference above. Compared the uv options with the citation and parser at `loom-code/scripts/loom_checker/probes.py:89-103`. Called `_runner_launcher` on a declared command shaped as the repository's `uv run --isolated --with-requirements ... python scripts/run_package_tests.py`, then with an unsupported uv option. Ran two focused finalization tests: `test_narrow_delta_finalizes_with_no_adversarial_artifact` and `test_finalize_accepts_a_graduated_program_the_suite_already_runs`.
- What came back: The official uv reference says uv options precede the command, `--isolated` is a switch, and `--with-requirements` takes a requirements file. The parser returned `['uv', 'run', '--isolated', '--with-requirements', 'requirements-package-tests.lock', 'python']` for the supported form and `None` for the unsupported form. The two tests passed; the first validates the generated attestation against the fixture's committed HEAD (test_selection_finalize.py:120-131), and the second confirms an already collected adversarial program finalizes (test_selection_finalize.py:344-363).
- Evidence: Second targeted batch returned `2 passed in 3.51s` (exit 0). This is evidence that the proof mechanism works on fixtures. The actual change attestation is produced later by `finalize-review`, after the package suite and reviews; it did not yet exist during acceptance testing.
