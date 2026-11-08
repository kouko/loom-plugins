---
title: "Does the --loom-family local-test exclusion apply to explicit arguments naming tests/local/test_example.py?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
change: fixture-explicit-args
tags:
  - loom/research
---

# Does the --loom-family local-test exclusion apply to explicit arguments naming tests/local/test_example.py?

## Question and scope

The earlier record, [package test roots](../../research/2026-11-08-package-test-roots.md), concluded that the ordinary `--loom-family` preset does not run `tests/local/`. That record is retained unchanged. The calling condition is now different: no `--loom-family`; the caller passes explicit arguments that name `tests/local/test_example.py`. Question: can the earlier exclusion conclusion be applied to this call?

Scope: the minimal source snapshot attributed by [provenance](../../../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76` (remote freshness not checked). It is not a full checkout, CI proof or deployment. Nothing was executed, and `tests/local/test_example.py` does not exist in the snapshot.

## Method and rationale

Static source inspection of `main()` and `split_groups` in the runner, with its test definitions as corroboration. The question is about the code path taken under a different argument condition, so reading the dispatch is the smallest sufficient method. Running pytest was forbidden and is not needed to see which branch is taken. The earlier evidence is reused only where its conditions match.

## Findings

- **Observed in source:** `main()` enters the preset only when `argv[0] == "--loom-family"` ([runner](../../../../src/scripts/run_package_tests.py), lines 153–167). Without it, control reaches the explicit-argument branch, lines 168–176.
- **Observed in source:** that branch splits argv on `--then` (`split_groups`, lines 58–65) and runs `[sys.executable, "-m", "pytest", *group]` per group (line 173). It does not call `loom_family_commands`, `_tests_session`, `_holds_tests` or `_shell_tests`. Those are the only places that skip `local/` (lines 68–96, 99–113) and add `--ignore=<local>`. The explicit path adds no `--ignore` of any kind.
- **Inference:** the runner therefore does not exclude `tests/local/test_example.py` when it is named explicitly. The target is passed to pytest as given, so the earlier exclusion conclusion does not carry over to this condition. Whether pytest then collects it also depends on pytest and its configuration, which are not in the snapshot (see limitations).
- **Corroboration (definitions only, not run):** [the runner tests](../../../../src/tests/test_run_package_tests.py) line 29 invoke the runner with explicit paths and per-group pytest arguments. Lines 222–235 and 285–298 assert the `local/` skip only for the preset commands. No test definition asserts exclusion for explicit arguments.
- **Not covered by the earlier conclusion:** the module docstring (lines 1–10) places the `local/` skip under the `--loom-family` description. The earlier record's last bullet already flagged that explicit-target behavior was not established.
- **Side effect worth noting:** explicit mode also omits the nested-repository `--ignore` entries that the preset adds (lines 123, 146–149). This is not relevant to the asked path unless the named path lies inside a nested repo.

## Evidence

| Claim | Source kind | Inspected | Status |
|---|---|---|---|
| Preset gate is `argv[0] == "--loom-family"` | Project source, snapshot of `d5a7f0d` | `run_package_tests.py` 153–167 | Source observation |
| Explicit mode forwards groups straight to pytest, no ignores | Project source | `run_package_tests.py` 58–65, 168–176 | Source observation |
| `local/` exclusion lives only in preset helpers | Project source | lines 68–96, 99–113, 124–132 | Source observation |
| Tests assert `local/` skip only for preset | Test definitions | `test_run_package_tests.py` 222–235, 285–298; explicit use at 29 | Read, not run |
| File integrity | Measurement | `shasum -a 256` on both files matched provenance: runner `6730a53e…0d54`, tests `b7ed3d4e…da28` | Observed |

No pytest invocation, runner command or test was executed.

## Decision impact

Do not reuse "tests/local/ is excluded" for explicit-argument calls. Under this condition the runner itself provides no exclusion, so the named local test is expected to be handed to pytest and run, unless pytest configuration outside the snapshot prevents it. If the intent is that local tests must never run through this runner, the explicit-argument path would need a guard. That is a design decision for the change owner and is not made here. If the intent is that a developer can deliberately run a local test by naming it, the current behavior matches.

## Limitations and open questions

- Source-supported only; no runtime observation. Collection of the named file by pytest was not tested.
- Pytest version and any `pytest.ini`, `conftest.py` or `addopts` in the real repository are not in the snapshot. The `loom-design` ini is mentioned in the docstring and could affect the real result.
- `tests/local/test_example.py` is hypothetical here; the file was not present to inspect.
- CI and deployed or installed versions are out of scope. Remote freshness of commit `d5a7f0d` was not checked.
- Revalidate if the runner changes, or if the caller adds `--loom-family` or other preset flags.
