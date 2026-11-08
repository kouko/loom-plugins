---
title: "Does the earlier tests/local exclusion apply to explicit-argument runs naming tests/local/test_example.py?"
type: loom-research
change: fixture-explicit-args
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Does the earlier tests/local exclusion apply to explicit-argument runs naming tests/local/test_example.py?

## Question and scope

The [earlier record](../../research/2026-11-08-package-test-roots.md) concluded that the ordinary `--loom-family` preset does not run `tests/local/`. The caller condition has changed: no `--loom-family`, and explicit arguments name `tests/local/test_example.py`. Can the earlier exclusion conclusion still be applied? The earlier record is retained unchanged as the basis for the `--loom-family` decision; this is a separately scoped revalidation for the active change `fixture-explicit-args`.

Scope: the supplied minimal source snapshot of the runner (attributed by [provenance](../../../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`). Not a complete checkout, CI, or deployment. No tests or runner commands were executed.

## Method and rationale

Reuse of the earlier record's evidence, with an applicability check, plus static inspection of the runner's `main` dispatch and `split_groups`, and the test definitions. This fits because the question is which code path handles the new invocation; no execution is needed or permitted.

## Findings

- **Observed in source:** the earlier exclusion does not carry over. `main` enters the preset branch only when `argv[0] == "--loom-family"`. Any other argv goes to `split_groups`, then each group runs as `[sys.executable, "-m", "pytest", *group]` ([runner](../../../../src/scripts/run_package_tests.py), lines 153–176). The `local/` exclusion lives in `_tests_session`, `_shell_tests` and `_workflow_sessions` (lines 76–113), which are reached only through `loom_family_commands` (lines 116–150), called only from the preset branch (line 163).
- **Inference:** so for `run_package_tests.py tests/local/test_example.py`, the runner adds no `--ignore` for `tests/local/` and does not consult `TEST_ROOTS`. The explicit path is passed straight to pytest, so pytest would normally collect it if the file exists and matches its collection rules. Pytest behavior is not verified here, only inferred from the runner forwarding the argument.
- **Also absent in this mode:** the nested-repository/worktree `--ignore` entries (lines 123, 146–149). Those apply only to the preset.
- **Docstring consistency:** the module docstring says `local/` is skipped for the `--loom-family` surface and that tests outside the roots do not run. That describes the preset's inventory, not explicit arguments (lines 4–11).
- **Test definitions:** the local-exclusion tests (lines 222–235, 285–310 in [tests](../../../../src/tests/test_run_package_tests.py)) target the discovery helpers and command lists. The explicit-mode tests (lines 17–35) cover only group splitting, exit codes and empty input. None asserts that an explicit `tests/local/...` path is excluded or included. These were read, not run.
- **Fixture state:** `tests/local/test_example.py` does not exist in this fixture, and only the minimal snapshot is present, so no collection claim about a real file is possible.
- **Harness observation (not run by me):** [fixture-observations.json](../../../../fixture-observations.json) records pre-run local git queries (`main` at `4959e62`, containing `research-fixture` at `00fa764`, no tags/remotes) and SHA256 values for the runner (`6730a53e…0d54`) and test file (`b7ed3d4e…da28`). These match provenance, so the inspected source is the same revision the earlier record analyzed. Git history was not otherwise mined.

## Evidence

| Claim | Source kind | Support |
|---|---|---|
| Preset only when first arg is `--loom-family` | Source, runner lines 153–167 | Source inspection |
| Explicit mode forwards groups to `pytest` unmodified | Source, runner lines 168–176; `split_groups` lines 58–65 | Source inspection |
| `local/` exclusion confined to preset helpers | Source, lines 76–113, 116–150, call site 163 | Source inspection |
| No test covers explicit `tests/local` targeting | [tests](../../../../src/tests/test_run_package_tests.py) | Only grep-matched lines were inspected (keywords `local`, `then`, `main(`, `subprocess`, `explicit`), not the whole file; the absence claim is therefore limited to those matches |
| Source revision same as earlier record | Harness observation, hashes vs. provenance | Reported observation, not rerun |

## Decision impact

The earlier "tests/local is not run" conclusion remains valid only for `--loom-family` and must not be applied to this invocation. For the explicit call naming `tests/local/test_example.py`, the runner source does not exclude it, so it would be passed to pytest, provided the file exists. Decisions that assume local tests are skipped here (for example, treating the call as safe because they are skipped) are unsupported. If the intent is to keep local-only tests out, the caller should not name them, or the runner would need a change, which this research does not authorize.

## Limitations and open questions

- Source-supported and inferential; nothing executed. Actual pytest collection of the file (config such as `pytest.ini`, `conftest.py`, markers) is untested and the file is absent from the fixture.
- Only the minimal snapshot is available; wrappers, CI, or a deployed runner version may differ.
- Revalidate if the runner changes, if the caller adds flags or wrappers, or if `--loom-family` is combined with explicit paths (the preset branch ignores trailing explicit paths in this source, but that was not separately studied).
