---
title: "Package runner foreign-test exclusion boundaries"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Package runner foreign-test exclusion boundaries

## Question and scope

Is the existing package runner sufficient to prevent accidental execution of tests from other people's clones or linked worktrees inside trusted test roots?

This is a static assessment of the four-file source snapshot at commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`, identified by [provenance](../../../provenance.json). The original repository path is provenance only; it was not accessed. Remote freshness is unknown. There is no active change. This snapshot is neither a full checkout nor deployment/CI evidence.

## Method and rationale

Inspect implementation, connected Git helpers, and test definitions; compare retaining the current approach against bounded safeguards. Static inspection answers command construction and failure handling without executing foreign code. Stop at source-supported boundaries and identify runtime-dependent questions. No tests, collection, Git operations, installs, network requests, or experiments were run. Bundled research methods, source policy, and template were read; unrelated samples were not needed.

## Findings

**Conclusion: conditional protection, not a general foreign-code execution boundary.** In `--loom-family` mode, discovered foreign paths become absolute pytest ignores and filter discovered shell scripts. Whether every foreign subtree is discovered, and whether all pytest targets honor those ignores, is not established for all relevant layouts.

| Boundary | Source-supported behavior | Consequence / evidence limit |
|---|---|---|
| Entry mode | Only leading `--loom-family` calls `loom_family_commands`; ordinary `--then` groups go directly to pytest. | Ordinary mode adds no automatic foreign exclusions. Calling a trusted runner alone is insufficient. |
| Discovery | Union of `nested_repositories` and `nested_worktrees`, resolved and deduplicated. | Protection depends on Git successfully returning relevant paths. See the separate [Git-failure assessment](2026-11-08-package-runner-git-failures.md). |
| Nested repositories | `_git_entries` uses `ls-files --cached --others --exclude-standard -z`; existing directory entries, excluding symlinks, become exclusions. | Covers directories Git exposes as opaque entries, including the intended ordinary clone/submodule cases. This is not a recursive scan for every `.git` marker. |
| Linked worktrees | Parses `worktree list --porcelain -z` and keeps paths strictly below the resolved root. | Can recover ignored linked worktrees listed for the queried repository. No source establishes that this lists worktrees belonging to an unrelated repository. |
| Python commands | Every generated pytest command receives `--ignore=<resolved foreign path>`. | Proven command construction; actual pytest behavior depends on collection, configuration, plugins, and explicit targets. |
| Shell discovery | `test-*.sh` under the four roots is filtered if a foreign path is in the resolved script's parents. | Proven filtering for discovered foreign ancestors. This does not sandbox shell execution. |
| Mermaid group | Fixed npm, node and bash commands bypass the discovered shell-script filter. | Fixed paths are not checked against the foreign set. A foreign replacement of that fixture directory is outside the demonstrated protection. |

Important unresolved layouts:

- An ignored clone is not necessarily represented by `ls-files --exclude-standard`, and the queried repository's worktree list does not establish discovery of that clone. An ignored worktree belonging to another repository has the same gap. These are plausible uncovered cases, not observed executions.
- `_workflow_sessions` selects immediate subdirectories with tests without consulting `foreign`. A foreign directory there can become an explicit pytest target while also receiving an ignore. The supplied definitions do not establish how the installed pytest handles that combination, or a foreign ancestor above that target. Do not infer safety from token presence.
- Symlink directories are deliberately excluded from `nested_repositories`; resolved shell paths and pytest traversal may behave differently. Symlink aliases, test roots that themselves point elsewhere, and filesystem changes after discovery remain unverified.
- A trusted parent test, conftest, or plugin can import or invoke other code. These path filters govern discovery, not arbitrary code executed by trusted tests.

## Evidence

All behavior below is supported by source inspection, not runtime observation. Paths refer to the immutable snapshot at the commit above; line numbers are navigation anchors in the supplied files.

| Claim | Inspected source and anchors |
|---|---|
| Modes, roots, command construction, execution | [runner](../../../src/scripts/run_package_tests.py): `TEST_ROOTS` L51–55; `_holds_tests` / `_tests_session` L68–85; `_workflow_sessions` L98–113; `loom_family_commands` L116–150; `main` L153–176. |
| Git inventory and worktree membership boundaries | [repo_files](../../../src/loom-code/scripts/repo_files.py): `nested_worktrees` L73–94; `nested_repositories` L97–120; `_git_entries` L123–146. Comments describe intended coverage; the implementation conditions above bound that intent. |
| Defined positive cases and their limits | [test definitions](../../../src/tests/test_run_package_tests.py): L128–139 asserts ignore tokens; L142–184 defines collection checks for a same-repository worktree and ordinary clone under `loom-code/tests`; L260–277 defines workflow sessions with ordinary subdirectories; L314–331 asserts no shell commands for a worktree and clone. |
| Weakness of collection evidence | The L142–156 helper returns stdout without asserting collection return status; L167 and L184 only assert absence of a test name. Even a reported pass would need context to exclude a collection failure. Here no result is provided or claimed. |
| Missing deployment evidence | L187–197 defines checks against CI and kickoff files, but those files are absent from this snapshot. This is not verification of actual CI invocation. |

Integrity check performed: `shasum -a 256 src/scripts/run_package_tests.py src/loom-code/scripts/repo_files.py src/loom-code/scripts/git_exec.py src/tests/test_run_package_tests.py`. All four output digests matched their entries in provenance.json. This verifies snapshot consistency only.

## Decision impact

Retaining the current approach is reasonable only where callers use family mode from the intended repository root, Git queries succeed with adequate supported output, and the allowed foreign layouts are limited to directories actually returned by those queries. Explicit workflow targets, ignored foreign repositories, aliases, and fixed Mermaid paths must be absent or separately validated. If the environment guarantees no foreign content under test roots, Git-independent isolation can make the discovery gaps irrelevant.

For the stated setting where test roots may contain arbitrary other clones or linked worktrees, current evidence is insufficient to accept the status quo as a reliable exclusion guarantee. Prefer keeping foreign checkouts outside test roots, or strengthening discovery and pruning foreign targets before constructing commands; pair this with the Git failure policy in the related record. These are recommendations only; no implementation or project settings were changed.

## Limitations and open questions

No test ran or passed in this investigation. Installed Python/pytest/Git versions, real wrappers and configuration, CI, and current repository state are unavailable. Future authorized verification should cover ignored clones and unrelated worktrees, direct workflow targets, symlink aliases, submodules and fixed Mermaid paths. Collection checks must assert successful collection and a positive trusted-test control as well as absence of foreign test names. Exact pytest handling of explicit ignored targets remains material; do not resolve it by assumption.
