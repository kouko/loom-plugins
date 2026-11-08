---
title: "Package runner behavior when Git discovery fails"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Package runner behavior when Git discovery fails

## Question and scope

Does the runner stop safely or continue when Git is unavailable, denies access, or a discovery query fails? Is retaining that behavior sufficient for trusted projects containing foreign test trees?

Assessment date: 2026-11-08. The four supplied source files are attributed by [provenance](../../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; original paths were not accessed. The snapshot is not a checkout, execution record, or CI result. Remote freshness and deployed versions are unknown. Related question: [foreign-test exclusion boundaries](2026-11-08-package-runner-foreign-tests.md).

## Method and rationale

Static tracing from runner entry point through both discovery helpers to `run_git`, plus inspection of all supplied test definitions. This establishes return values and their propagation without manufacturing failures or executing tests. The bundled method/source guidance and research template were read. No network, external settings, Git operations, installs, tests, collection, or experiments were used.

## Findings

**Conclusion: handled Git failures reduce exclusions and permit execution to continue; they do not enforce a stop-before-tests policy.** Complete discovery failure and a successful discovery of no foreign trees are indistinguishable to the family runner. Partial query failure can retain partial protection. This is a source-supported control-flow conclusion, not a measured incident.

| Condition | Source return path | Runner consequence |
|---|---|---|
| Git executable missing or execution denied (`OSError`) | Default `run_git(check=False)` catches it and returns `None`. | Discovery helpers can return empty lists; family command generation continues. |
| Git rejects repository access, including ownership rejection, or any query exits nonzero | Captured subprocess output is discarded on nonzero status; `run_git` returns `None`. | No differentiated reason or runner warning is produced by this path. Failure is treated like missing discovery information. |
| Bare-repository probe fails alone | `_git_entries` continues to the top-level probe, because `None != "true"`. | Later successful queries may still provide repository exclusions. Failure of one probe does not imply all discovery failed. |
| Top-level probe fails or returns empty output | `_git_entries` returns `None`; `nested_repositories` returns `[]`. | `nested_worktrees` is still queried independently and may retain linked-worktree exclusions. |
| Top-level probe succeeds but `ls-files` fails | `_git_entries` returns `None`; `nested_repositories` returns `[]`. | Worktree exclusions may survive; clone/submodule discovery is lost through this path. |
| Worktree query fails | `nested_worktrees` returns `[]`. | Opaque directory entries from successful repository discovery may still protect some trees; ignored worktrees can lose the complementary coverage. |
| Both discovery paths provide nothing, including outside a repository | Both helpers return empty lists. | No foreign ignores or foreign shell filtering; filesystem-based target discovery still operates. Existing local exclusions remain separate. |
| Bare repository successfully identified | `_git_entries` returns `[]`. | No repository-directory exclusions from that helper; this is not itself a failure or a runner prohibition. |
| Git hangs | These calls omit `timeout`; `run_git` defaults to `None`. | No finite deadline is imposed here. Although the helper catches `TimeoutExpired`, this caller supplies no timeout that would normally trigger it. |

The runner does **not** call `repository_files` or `_walk_entries` as a fallback for foreign discovery. Those functions serve file inventory; their filesystem walk must not be confused with a fallback exclusion scan. `nested_repositories` explicitly returns `[]` on missing entries instead. Family target and shell discovery use their own filesystem traversal.

Once commands are built, `main` executes them sequentially and returns the first nonzero child status; if none fail, or there are no commands, it returns zero. Consequently a zero runner status does not certify successful Git discovery. In ordinary argument-group mode, neither discovery helper is called at all.

The handled cases above do not guarantee that every possible exception is swallowed: path traversal/resolution errors and exceptions outside `run_git`'s specified catch can propagate. No graceful diagnostic/status contract for those errors is established. Missing pytest/npm/bash is a separate child-launch issue and does not demonstrate safe Git handling.

## Evidence

All entries are inspected source at the commit above, with no runtime verification.

| Finding | Source and anchors |
|---|---|
| Error conversion, captured output, default deadline | [git_exec](../../../src/loom-code/scripts/git_exec.py): `run_git` L50–88, especially defaults L53–56, subprocess call L73–76, catch L77–80, nonzero branch L82–83. `check=True` propagates errors, but these discovery callers do not request it. |
| Worktree failures become empty exclusions | [repo_files](../../../src/loom-code/scripts/repo_files.py): `nested_worktrees` L73–94. |
| Probe/listing failures become empty repository exclusions | [repo_files](../../../src/loom-code/scripts/repo_files.py): `nested_repositories` L114–120 and `_git_entries` L132–146. |
| Inventory fallback is a separate API | [repo_files](../../../src/loom-code/scripts/repo_files.py): `repository_files` L64–70 and `_walk_entries` L149–168. |
| Execution proceeds without discovery status | [runner](../../../src/scripts/run_package_tests.py): foreign union L123, shell filtering L134–138, pytest ignores L146–149, family execution/status L153–167, ordinary mode L168–176. |
| Available test coverage | [test definitions](../../../src/tests/test_run_package_tests.py): L104–184 and L314–331 set up successful Git repositories and check exclusions. The complete supplied file contains no definitions simulating missing Git, denied access, failed discovery queries, or stalled Git. L22–30 checks a failing pytest group, not Git discovery failure. No tests were executed. |

Integrity command: `shasum -a 256 src/scripts/run_package_tests.py src/loom-code/scripts/repo_files.py src/loom-code/scripts/git_exec.py src/tests/test_run_package_tests.py`. All four digests matched provenance.json. This is a content check, not execution validation.

## Decision impact

Keeping current behavior is conditionally acceptable when a separately enforced workspace rule excludes foreign content from the test roots, or when a trusted preflight verifies complete relevant discovery and prevents execution if that verification fails. Merely having Git installed does not establish query success or complete coverage. Such external controls are not shown in this snapshot.

Where foreign trees may be present and accidental execution must be prevented, retaining the runner alone is insufficient: availability currently takes precedence over exclusion certainty on handled Git failure. Recommend explicit discovery success/error results, actionable diagnostics, a bounded Git query deadline, and stopping before any child test command on incomplete discovery in this context. If archive/no-Git operation remains necessary, define an explicit policy backed by isolated roots or a separately validated fallback. Do not silently substitute an empty exclusion set. These are proposed safeguards, not implemented changes or evidence of an existing control.

## Limitations and open questions

No failure was induced and no tests ran. Exact stderr, exit status, platform behavior and timing under missing/denied/stalled Git remain unmeasured. Future authorized validation should distinguish each probe/listing failure, partial success and total failure, and verify that the chosen policy starts no test process after discovery failure. Actual callers, CI/preflight controls, Git/pytest versions and complete checkout configuration are absent. Even successful queries leave layout gaps described in the related foreign-test record; better failure handling alone cannot settle them.
