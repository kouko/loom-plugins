---
title: "Does the ordinary-preset exclusion of tests/local/ apply to explicit-argument invocation?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
change: fixture-explicit-args
tags:
  - loom/research
---

# Does the ordinary-preset exclusion of tests/local/ apply to explicit-argument invocation?

## Question and scope

The earlier record, [Package runner test roots and local-test exclusion](../../research/2026-11-08-package-test-roots.md), concluded that `--loom-family` does not run `tests/local/`. The caller's condition has changed: no `--loom-family`; instead explicit arguments name `tests/local/test_example.py`. Can the earlier exclusion conclusion be applied to this call?

Scope: the minimal source snapshot in [provenance](../../../../provenance.json) (recorded commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; remote freshness not checked). It is not a full checkout, deployment or CI evidence. The earlier record is preserved unchanged; this is a separately scoped revalidation for different invocation conditions. No tests or runner commands were executed.

## Method and rationale

Static inspection of the runner's `main()` branch selection and the explicit-argument path, plus the test definitions for any coverage of that path. This is a single-source behavior question, so a direct source read suffices. Pytest's own collection semantics were not checked against documentation (no network access) and are flagged below as unverified background.

## Findings

- **Observed in source:** the exclusion is not applied on the explicit path. `main()` enters the preset only when `argv[0] == "--loom-family"` ([runner](../../../../src/scripts/run_package_tests.py), lines 153–167). Otherwise it calls `split_groups(argv)` (lines 58–65, 168) and runs `subprocess.call([sys.executable, "-m", "pytest", *group])` per group (lines 172–175). The tokens, including `tests/local/test_example.py`, are forwarded verbatim.
- The `local/` skipping lives only in `_tests_session` (lines 76–86, adds `--ignore=<local>`), `_shell_tests` (lines 88–95) and `_workflow_sessions` (lines 98–113). All are reached only through `loom_family_commands`, which the explicit path never calls. The nested-repository `--ignore` tokens (lines 123, 146–149) are likewise preset-only.
- The module docstring (lines 1–6, 7–9) describes `local/` skipping as a property of `--loom-family`, consistent with this reading.
- **Test definitions:** the `local` exclusion tests in [test_run_package_tests.py](../../../../src/tests/test_run_package_tests.py) (lines 222–235, 285–298) use `loom_family_commands`/`only=` and therefore cover the preset only. The explicit-path tests (lines 16–36) check group splitting, exit codes and empty-argument handling; none targets a `local/` path. Read, not run.
- **Inference (not verified here):** with the runner adding no ignore, whether pytest collects the named file depends on pytest's behavior for explicitly given file arguments and on any pytest.ini/conftest in the real repository. From general pytest knowledge, an explicitly named file path is collected and `local` has no special meaning to pytest, so the file would most likely run. This was not confirmed against documentation or by execution.
- **Not established:** `tests/local/test_example.py` does not exist in the snapshot (only four source files were supplied), so its content, markers, skips or fixtures are unknown.

## Evidence

| Claim | Source | Kind / conditions |
|---|---|---|
| Explicit mode forwards groups to pytest with no `local` ignore | [runner lines 153–175](../../../../src/scripts/run_package_tests.py) | Source inspection, snapshot at the commit recorded in provenance |
| `local` exclusion is implemented only inside preset helpers | runner lines 76–113, 123–149 | Source inspection; call graph traced from `main()` |
| No test covers explicit-path `local/` handling | [tests](../../../../src/tests/test_run_package_tests.py) lines 16–36, 222–298 | Test definitions read, not run |
| Snapshot integrity | `fixture-observations.json` (harness observation, not my command): runner and test sha256 equal the values in provenance (`6730a53e…0d54`, `b7ed3d4e…da28`) | I did not recompute hashes |
| Fixture git state | Same file: `main` = `4959e62`, `research-fixture` = `00fa764` is an ancestor of `main`, no tags, no remotes | Harness observation of a temporary fixture only |

## Decision impact

The earlier conclusion does **not** transfer. Its own limitation already said the exclusion is preset-specific and does not cover explicitly targeted local tests. For this change: do not rely on the runner to keep `tests/local/test_example.py` out of an explicit-argument call. By source, the runner would pass it to pytest, which (inference) would collect it. If the intent is to prevent local tests from running, the caller must not name them, or must add its own exclusion; if the intent is to run a local test deliberately, explicit arguments appear to be the route. The earlier decision (do not place tests meant for ordinary package coverage in `tests/local/`) is unaffected, since it concerns the preset.

## Limitations and open questions

- No execution: whether pytest actually collects and runs the file is untested here, and pytest documentation was not consulted.
- Real repository ini/conftest settings, CI configuration, and deployed versions are outside the snapshot.
- The target file is absent from the fixture; its behavior is unknown.
- Explicit mode also lacks the nested-repository ignores; only relevant if an argument names a directory containing nested repositories.
- Revalidate if the runner source changes or if different arguments (e.g. caller-supplied `--ignore`, directory targets) are used.
