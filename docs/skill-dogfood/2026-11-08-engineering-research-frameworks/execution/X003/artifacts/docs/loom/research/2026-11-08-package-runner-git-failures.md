---
title: "Package runner: Git discovery failure policy"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Package runner: Git discovery failure policy

## Question and scope

What does the package runner do when Git is unavailable, refuses repository access or a discovery query fails, and is retaining that behavior sufficient when foreign tests may exist under test roots?

Scope is static inspection of the supplied source snapshot at commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`, dated 2026-11-08. The original source location in [provenance](../../../provenance.json) was not accessed. This is not a complete checkout or evidence of CI/deployment success. No runtime failure was induced and no runner, tests, Git commands, network, apps or external models were invoked.

## Method and rationale

Use failure-mode/resilience analysis backed by direct source inspection: trace failure conversion, propagation, detection and containment from `run_git` through discovery to command execution. The decisive criterion is whether unknown repository ownership stops execution before foreign contents can run. A second criterion is whether operators can distinguish a discovery failure from a genuinely empty result. This method fits a dependency failure question; timing samples or a benchmark would not answer it. Stop at the supplied implementation and test definitions.

## Findings

**Git discovery failure is treated as absent exclusion data, not as a reason to stop.** It is fail-open with respect to foreign-test exclusion, subject to whatever exclusions the other query still discovers. This conclusion follows from source control flow; it is not a measured incident.

| Failure or result | Conversion in the inspected implementation | Consequence for family mode |
|---|---|---|
| Git executable absent or spawning denied (`OSError`) | `run_git`, using default `check=False`, returns `None`. | Affected detector supplies no foreign paths. If both detectors lose data, no foreign ignores or dynamic shell foreign filters are generated. |
| Git rejects access, including an ownership refusal that exits nonzero | Captures stdout/stderr; nonzero exit becomes `None`. | Failure reason is discarded by these callers; no dedicated runner warning or stop. The actual refusal/error text was not observed. |
| `rev-parse --show-toplevel` fails or yields empty output | `_git_entries` returns `None`; `nested_repositories` returns `[]`. | Worktree listing can still contribute paths independently. |
| `ls-files` fails after top-level discovery succeeds | `_git_entries` returns `None`; `nested_repositories` returns `[]`. | Same partial-discovery boundary; successful top-level discovery is insufficient. |
| `worktree list` fails, including an unsupported option returning nonzero | `nested_worktrees` returns `[]`. | Repository entries can still exclude some subtrees; ignored worktrees relying on this query lose that coverage. |
| Successful empty output / no matching paths | Empty exclusion list, indistinguishable to runner from detector failure. | Runner cannot establish whether the root is clean or discovery failed. No output schema/completeness validation is present. |
| Slow or hung Git | `run_git` accepts a timeout but callers omit it, leaving `None`. | No finite discovery timeout is configured here; command construction can wait indefinitely absent external limits. A caught `TimeoutExpired` would return `None`, but no caller deadline triggers it here. |
| Bare repository reported as `true` | `_git_entries` returns `[]` immediately. | No nested-repository paths from that detector; this special case does not constitute a runner-wide no-test rule. |

The runner **does not** call `repository_files` and **does not** use its filesystem-walk fallback. It calls `nested_repositories`, which returns an empty list on unavailable Git entries, plus `nested_worktrees`. Confusing the file-listing API with the exclusion API would produce the wrong explanation. Dynamic test discovery still walks configured test roots, independently of Git discovery, so missing exclusions can allow foreign test candidates to reach generated commands. Whether they actually collect or execute depends on their location, pytest behavior and configuration; see the [foreign-test assessment](2026-11-08-package-runner-foreign-tests.md).

Command construction computes the discovery union even for a single selected family group, including Mermaid. Dispatch then invokes generated commands sequentially and returns the first nonzero subprocess status. That is test-command failure propagation, not Git-discovery failure containment. If generated commands succeed, or no commands are generated for a selected dynamic group, family mode can return 0 despite Git discovery failure. A nonzero result from foreign tests would occur too late to prevent their execution. Missing test-command executables can raise an uncaught `OSError`; the Git wrapper's error handling does not wrap `subprocess.call` in the runner.

Generic path-group mode does not query Git at all and has no automatically generated foreign exclusions.

## Evidence

| Evidence at the scoped commit | Claim supported and verification status |
|---|---|
| [Git invocation helper](../../../src/loom-code/scripts/git_exec.py), lines 50–88 | Default timeout/check values, captured output, caught OS/timeout errors, nonzero-to-`None` conversion. Source inspected. No failure command was executed. |
| [Repository discovery](../../../src/loom-code/scripts/repo_files.py), lines 73–146 | Independent worktree query; empty-list handling; bare/top-level/listing branches. Source inspected. |
| [File-listing API](../../../src/loom-code/scripts/repo_files.py), lines 64–70, 149–168 | Filesystem fallback exists in a different API and is not used by the runner's exclusion helpers. Source inspected. |
| [Runner](../../../src/scripts/run_package_tests.py), lines 68–150, 153–176 | Filesystem target discovery, unconditional family union computation, no discovery status check, sequential dispatch and return behavior. Source inspected. |
| [Supplied tests](../../../src/tests/test_run_package_tests.py), lines 1–331 | Contains definitions for successful Git repository layouts, collection helpers and normal command failure propagation. No defined coverage for unavailable/refused Git, independent query failures, hung Git or warning/abort behavior was found in this supplied file. Definitions were read, not run; this is not a statement about tests absent from the full repository. |
| [Provenance](../../../provenance.json) | Snapshot revision and expected hashes; remote freshness not checked. All four source hashes matched using the `shasum -a 256` command recorded in the related assessment. This is the only measured source-integrity result, not behavioral verification. |

## Decision impact

Retaining this policy is conditionally acceptable if an independently enforced workflow prevents foreign contents under test roots, or establishes complete successful discovery before dispatch, and the resulting availability/diagnostic limitations are accepted. No such enforcement is demonstrated by the supplied snapshot. Merely having Git installed or seeing a green runner exit is insufficient.

If foreign clones/worktrees are allowed in those roots, recommend distinguishing successful-empty discovery from failure and stopping before execution on incomplete discovery. Preserve a diagnostic reason, impose a bounded query deadline, and avoid silent fallback to an empty exclusion set. This trades some archive/no-Git usability for a dependable ownership boundary; any archive mode would need an explicit trusted inventory or equivalent policy. Do not bypass ownership checks simply to make Git return success. These are proposed changes, not changes made in this research.

## Limitations and open questions

No runtime platform/version, actual safe-directory policy, permission behavior, outer timeout, preflight checks, wrapper policy or CI execution was established. User descriptions establish the intended use case, not deployment configuration. Standard subprocess exception/return paths are visible, but platform-specific timing and error messages remain unmeasured.

Future separately authorized validation should isolate missing executable, spawn denial, Git nonzero refusal, failed top-level/listing/worktree queries independently, successful-empty results and bounded slow queries. Check that no test process starts after a required discovery failure and that diagnostics distinguish the failure. The present task prohibits those experiments, so there is no reproduction or test-pass claim. Source evidence is sufficient to reject an unconditional safety recommendation without manufacturing an incident.
