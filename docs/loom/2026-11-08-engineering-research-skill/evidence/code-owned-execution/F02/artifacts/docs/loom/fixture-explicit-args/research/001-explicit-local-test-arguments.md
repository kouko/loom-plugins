---
title: "Explicit local test arguments bypass the package preset exclusion"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
change: fixture-explicit-args
tags:
  - loom/research
---

# Explicit local test arguments bypass the package preset exclusion

## Question and scope

Does the earlier conclusion that ordinary `--loom-family` excludes `tests/local/` still apply when the caller omits that option and explicitly supplies `tests/local/test_example.py`? The pending decision is whether this caller can rely on the earlier exclusion.

This is a separate revalidation under changed invocation conditions. The [earlier decision](../../research/2026-11-08-package-test-roots.md) remains intact and applicable to its original preset scope. The active change is `fixture-explicit-args`. Scope is the supplied minimal source snapshot attributed by [provenance](../../../../provenance.json) to original revision `d5a7f0da247214bdb9c61fe90c550256432e5f76`. No tests, collection commands, sample commands, external models, network requests, or app operations were executed.

## Method and rationale

Static implementation inspection and applicability checking of the prior research. Trace the entry point through argument splitting to subprocess construction, compare the preset-only path, and inspect relevant test definitions as corroboration. This factual branch-selection question needs no comparative evaluation framework or experiment. Stop once the source establishes whether the explicit target receives the preset exclusion; runtime outcomes remain outside this investigation.

## Findings

1. **Source-supported:** The preset branch is entered only when the first argument is `--loom-family` ([runner](../../../../src/scripts/run_package_tests.py), lines 153–167). The new caller does not enter that branch.
2. **Source-supported:** `split_groups` preserves tokens except for splitting on `--then` and discarding empty groups (runner lines 58–65). For the single supplied target, the resulting group is `['tests/local/test_example.py']`.
3. **Source-supported:** The explicit branch constructs `[sys.executable, '-m', 'pytest', *group]` (runner lines 168–175). Therefore the derived subprocess argument list is `[sys.executable, '-m', 'pytest', 'tests/local/test_example.py']`. This is a static derivation, not an executed command or observed output. No `local/` ignore, `TEST_ROOTS` filter, or preset discovery helper is applied on this path. The target is relative to the caller's working directory; the subprocess call supplies no replacement `cwd`.
4. **Source-supported comparison:** The preset's code group calls `_tests_session`, which excludes each root's `local/` during discovery and appends a local ignore when present (runner lines 76–85, 124–128). Those operations are not shared with explicit mode. Preset nested-repository ignores are likewise constructed inside `loom_family_commands` (lines 123, 146–149), not the explicit branch.
5. **Decision inference:** The prior exclusion cannot justify assuming this explicit target will be skipped. The runner hands it to pytest for processing. This does not prove collection, execution, or success: file availability, pytest configuration, plugins, dependencies, and startup failures can still affect the outcome.

## Evidence

- **Primary implementation:** [runner source](../../../../src/scripts/run_package_tests.py), inspected at lines 47–65, 76–85, 116–176, and 179–180, including the script entry into `main(sys.argv[1:])`. The import chain through [repo_files](../../../../src/loom-code/scripts/repo_files.py) and [git_exec](../../../../src/loom-code/scripts/git_exec.py) was inspected for orientation; explicit mode does not call the nested-repository discovery functions. These are supplied source files, not a complete installation.
- **Test definitions, read only:** [runner tests](../../../../src/tests/test_run_package_tests.py), lines 16–19 define group-splitting expectations; lines 22–30 define explicit-directory execution and failure propagation checks; lines 222–235 define preset local-test exclusion. These definitions were not run and do not demonstrate an executed explicit-local-file case.
- **Prior evidence:** [existing research](../../research/2026-11-08-package-test-roots.md) already bounds the exclusion to preset mode and notes explicit forwarding. The new source trace confirms applicability to the changed caller. The supplied [original research snapshot](../../../../snapshots/original-research.md) was read without modification.
- **Snapshot identity check, actually performed:** `shasum -a 256 src/scripts/run_package_tests.py src/tests/test_run_package_tests.py` returned respectively `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` and `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28`, matching provenance. No external source checkout was inspected.
- **Executor receipt scope:** [sample-receipt.json](../../../../sample-receipt.json) reports an earlier executor exit code of zero, an added prior research file, and unchanged source. Its server-confirmed model is null. It does not prove this invocation's behavior, test results, installed plugin behavior, or deployment.
- **Fixture lifecycle only:** Local `git log --all --decorate --oneline -8` and `git show --no-patch --format=fuller 4959e620a78e15678a3cc2a8a0c18f79de58dc73` identify fixture `main` at that merge, with parents `3236024` and `00fa764`. The diff from `00fa764` to that merge for the earlier research file was empty. [fixture-cleanup.json](../../../../fixture-cleanup.json) reports a successful clean post-merge status, cleanup destination `.`, no linked worktree or generated temporary build artifact, and retention of the topic branch. Current initial `git status --short` instead showed untracked `fixture-cleanup.json` and `skill/`; the recorded cleanup is a historical fixture observation, not a claim that the present workspace is clean. This harness history is distinct from the original source revision and proves no real merge, release, host cleanup, or installed behavior. The newly retained research is not represented as merged or exported.

## Decision impact

Do not reuse the ordinary-package exclusion as a guarantee for this explicit invocation. Treat `tests/local/test_example.py` as an explicit pytest target forwarded by the runner, subject to pytest and environment behavior. Keep the earlier test-placement decision for ordinary preset coverage unchanged. No source change is required to answer this question, and no original record was replaced.

## Limitations and open questions

No runtime validation was permitted or performed, including collection-only execution. The target file and full pytest/CI environment are absent from the supplied minimal snapshot; actual collection, execution, and pass/fail remain unverified. The conclusion is limited to runner argument forwarding at the attributed source revision. Revalidate if the runner, wrapper arguments, working directory, or relevant pytest configuration changes. Fixture cleanup and executor receipts do not remove these limits. No Vault destination was supplied and no preservation copy was written; this active-change record remains local to the project fixture.
