---
title: "Package runner: boundaries against foreign test execution"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Package runner: boundaries against foreign test execution

## Question and scope

Is retaining the runner sufficient when a trusted project's test roots can contain other people's clones or linked worktrees? The required property is avoiding accidental execution of their tests. This is a static assessment of the four supplied source files at commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`, not a complete checkout, installed package, deployment or CI assessment. No active change exists.

The original location is provenance data only; it was not accessed. No network, apps, agents, installations, Git operations, runner invocations or tests (including collection) were used. Frozen samples were not used as evidence for current behavior.

## Method and rationale

Use a bounded trust-boundary review through direct implementation and test-definition inspection. Trace discovery, foreign-path identification, command construction and dispatch. The asset is the trusted test process; the boundary is between project tests and foreign repository contents under the same filesystem roots. Accidental placement is enough to create exposure; no malicious repository or incident reproduction is needed. Criteria are exclusion coverage, applicability to every entry mode and evidence of actual collection behavior. This answers the decision without executing untrusted contents. Stop at the available connected call paths and identify runtime gaps explicitly.

## Findings

**The current mechanism is conditional protection, not a general guarantee.** These are source-supported facts, with runtime implications identified separately:

| Path or condition | Source-supported behavior | Boundary / implication |
|---|---|---|
| `--loom-family` | Computes resolved union of `nested_repositories` and `nested_worktrees`; appends absolute `--ignore` arguments to all generated pytest commands. | Protection depends on complete Git discovery and pytest honoring these ignores for the actual target arrangement. |
| Repository discovery | `_git_entries` asks Git for cached and nonignored other entries. `nested_repositories` keeps real directory entries, excluding symlinks. | It identifies directories Git represents as opaque entries; it does not recursively identify every `.git` marker. Git's exact treatment of unusual layouts is not independently established here. |
| Linked-worktree discovery | Parses `git worktree list --porcelain -z`, keeping worktrees strictly below the resolved root. | Can supplement an ignored worktree omitted by `ls-files`, when it belongs to the queried repository. Another repository's worktree registry is not queried. An ignored clone or ignored worktree belonging to another repository is therefore not guaranteed detectable by this union. |
| Family shell discovery | Recursively finds `test-*.sh` under the four roots, excluding root `local/` descendants and `node_modules`; rejects candidates whose resolved parents include a foreign root. | A detected foreign shell subtree is filtered before a command is created. This is source logic, not an executed result. |
| Workflow Python | Each eligible immediate subdirectory holding Python tests becomes its own explicit target. Foreign paths do not participate in `_holds_tests` or subfolder selection. | A foreign directory can be both an explicit pytest target and an ignore path, or contain an explicit target. Actual pytest collection/import behavior for these combinations remains unverified. |
| Ordinary path groups | Outside `--loom-family`, forwards caller groups to pytest with no foreign discovery or added ignores. | The family exclusion mechanism does not protect this mode. |
| Mermaid family group | Adds three fixed npm/node/bash commands, independently of the foreign list. | It is outside the dynamic shell filter and pytest ignores. Keep these fixed paths project-owned; replacement by a foreign subtree is not blocked here. |

The four dynamic roots are `tests`, `loom-code/tests`, `loom-design/tests`, and `loom-workflow/tests`. Discovery passes directories to pytest rather than enumerating trusted files. The `node_modules` check in `_holds_tests` only influences whether a target exists; it does not generate a Python collection ignore for that directory. Root `local/` ignores are a separate convenience, not repository ownership validation.

This is not a sandbox: discovered shell scripts and pytest run with the runner's process environment and permissions. It does not constrain imports, pytest configuration/plugins, subprocesses or paths referenced by trusted tests. Filesystem changes between discovery and execution are also not guarded. These are boundaries of the mechanism, not observed incidents.

## Evidence

All implementation citations refer to the supplied snapshot and commit above. Relative links point to the evidence actually inspected; line spans below are textual anchors.

| Evidence | Claim supported and verification status |
|---|---|
| [Provenance](../../../provenance.json) | Supplies original source paths, commit and SHA256 values; remote freshness explicitly not checked. |
| [Runner](../../../src/scripts/run_package_tests.py), lines 47–55, 68–150 | Imports both discovery helpers, defines roots, recursively discovers targets, filters dynamic shell commands, leaves fixed Mermaid commands separate, and adds pytest ignores. Source inspected. |
| [Runner dispatch](../../../src/scripts/run_package_tests.py), lines 153–176 | Family mode uses cwd; generic groups directly invoke pytest without generated exclusions. Source inspected. |
| [Repository helpers](../../../src/loom-code/scripts/repo_files.py), lines 73–146 | Worktree parser, strict descendant check, directory/symlink selection and Git listing arguments. Implementation inspected; comments about Git semantics are not runtime verification. |
| [Test definitions](../../../src/tests/test_run_package_tests.py), lines 128–184 | Defines ignore-token and clone/worktree collection checks under `loom-code/tests`. The helper at 142–156 checks returned stdout only, without asserting collection return code or a positive trusted-test result; absence of the intruder name alone is weaker than verified successful collection. Not run. |
| [Further test definitions](../../../src/tests/test_run_package_tests.py), lines 260–277, 314–331 | Defines normal workflow session splitting and command-list exclusion for a clone and worktree in the shell group. Does not combine a foreign workflow Python directory with explicit-target collection. Not run. |

Integrity check performed: `shasum -a 256 src/scripts/run_package_tests.py src/loom-code/scripts/repo_files.py src/loom-code/scripts/git_exec.py src/tests/test_run_package_tests.py`. All four outputs exactly matched the corresponding entries in `provenance.json`. This verifies snapshot consistency with that manifest, not independent authenticity or runtime correctness.

## Decision impact

Retaining the implementation can be reasonable for a controlled layout using family mode from the intended repository root, successful complete Git discovery, project-owned fixed Mermaid paths and stable directories, provided actual pytest exclusion behavior for the deployed version and target arrangements has already been established elsewhere. This snapshot does not establish those operational conditions.

For the broader stated use case, retaining it without additional controls is insufficient evidence of safety. A practical immediate restriction is keeping foreign checkouts outside test roots and using family mode. If foreign directories must remain, prioritize explicit trusted-target selection or pruning foreign paths before creating targets, complete handling of ignored/unregistered repositories, and the failure policy in the [Git failure assessment](2026-11-08-package-runner-git-failures.md). These are recommendations only; no implementation was changed.

## Limitations and open questions

No installed Python/pytest/Git versions, complete pytest configuration, CI workflows, wrapper scripts or execution records were supplied. A test that references CI files does not establish their current content or deployment use.

Future authorized validation should distinguish: normal clone and same-repository worktree; ignored clone and another repository's ignored worktree; foreign workflow directory as an explicit target (including an ancestor of that target); symlink aliases; and fixed-path replacement. Require successful collection, positive trusted-test collection, and zero foreign collection/imports, rather than merely an ignore token or missing stdout name. None of these validations ran here. There is no claim that foreign tests actually executed.
