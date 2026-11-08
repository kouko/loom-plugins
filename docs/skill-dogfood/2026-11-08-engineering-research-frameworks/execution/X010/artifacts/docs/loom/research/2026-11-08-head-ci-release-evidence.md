---
title: "Does the package-runner snapshot justify HEAD CI and release approval?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Does the package-runner snapshot justify HEAD CI and release approval?

## Question and scope

Can the presence of `--loom-family` and coverage definitions in `tests/test_run_package_tests.py` justify approving all CI as passed and releasing current HEAD? **No.** These artifacts support bounded implementation claims, not a successful CI run or release readiness. This does not establish that CI failed or that the release is defective; the proposed approval lacks the necessary evidence.

The assessed revision is `d5a7f0da247214bdb9c61fe90c550256432e5f76`, as recorded in [provenance](../../../provenance.json). `src/` is a four-file source snapshot, not a checkout. The same locally recorded `origin/main` value is provenance metadata; remote freshness is explicitly unchecked. It does not independently establish the present remote branch or a release candidate's identity. The original repository path is attribution only and was not accessed.

No active change is known. Research used only supplied workspace files. No tests (including collection), runner imports/execution, Git commands, repository creation, installs, network, apps, external models, delegation, publishing, or acceptance actions were performed. No scratch experiment was needed or run. Protected inputs were not edited.

## Method and rationale

Static implementation and test-definition inspection, following the explicitly invoked [skill](../../../skill/engineering-research/SKILL.md), [research methods](../../../skill/engineering-research/references/research-methods.md), and [source policy](../../../skill/engineering-research/references/source-policy.md). Trace entry point → discovery and command construction → Git exclusion helpers → subprocess failure handling. Inspect what the tests actually assert and identify missing connections to CI and release artifacts. Hash inspection checks snapshot identity, not program behavior.

Stop once the proposed inference can be assessed and decision-changing evidence gaps identified. Runtime validation would need evidence unavailable here and is prohibited in this task; static analysis cannot replace it.

## Findings

### Source-supported facts, not runtime observations

| Claim supported by inspected source | Evidence and boundary |
| --- | --- |
| The family mode is selected when the first argument is `--loom-family`; `--only` accepts five named groups and rejects missing/unknown group values. The repository root used for discovery is `Path.cwd()`. | [Runner](../../../src/scripts/run_package_tests.py#L153), lines 153–167; group names at lines 51–55. Merely having the flag in a file does not establish CI invoked this branch, used the correct working directory, or selected every group. |
| Python discovery considers four explicit roots: `tests`, `loom-code/tests`, `loom-design/tests`, `loom-workflow/tests`. Code roots share an xdist session; design has a separate session; workflow has a top-level session when needed and sessions for eligible immediate subfolders. | [Discovery and construction](../../../src/scripts/run_package_tests.py#L68), lines 68–133. Detection uses `test_*.py` and `*_test.py`; actual collection also depends on absent pytest configuration, plugins and fixtures. Roots without detected tests can produce no Python command. An empty selected command list reaches return 0; that is not proof of coverage. |
| Root-level `local/` directories are excluded from the general Python/root shell discovery; `node_modules` is filtered during discovery. Workflow subfolder selection has additional name filters. Shell discovery searches `test-*.sh` under the four roots. | [Runner](../../../src/scripts/run_package_tests.py#L76), lines 76–113 and 134–138. This is an explicit inventory boundary, not evidence that every required repository or release check lies within it. Directory targets are handed to pytest, so discovery predicates alone do not establish every eventual collection exclusion. |
| Foreign subtree handling unions nested-repository and nested-worktree results, appends absolute ignores to family pytest commands, and filters discovered shell scripts by resolved ancestry. | [Runner](../../../src/scripts/run_package_tests.py#L116), lines 116–150; [repository helper](../../../src/loom-code/scripts/repo_files.py#L73), lines 73–146. Worktree listing can cover ignored linked worktrees; opaque Git entries can cover clones/submodules. These are conditional mechanisms, not observed exclusion success. |
| The exclusion mechanism can lose evidence silently when Git queries fail. | [Git wrapper](../../../src/loom-code/scripts/git_exec.py#L50), lines 50–88, returns `None` on default nonzero/OSError/timeout paths. [Helpers](../../../src/loom-code/scripts/repo_files.py#L73), lines 73–146, can return empty foreign lists on failures/no Git. They do not fail the family run simply because exclusion discovery failed. An ignored clone is not guaranteed to be exposed by either query. Applicability depends on the actual Git environment and repository layout. |
| The Mermaid group constructs three fixed commands: npm installation, Node validation, then a Bash negative check. Family execution is sequential and returns immediately at the first nonzero subprocess result. | [Runner](../../../src/scripts/run_package_tests.py#L139), lines 139–167. Missing executables can raise rather than produce a normal returned status. The fixed Mermaid commands are separate from discovered-shell filtering. No command was run here; later commands may never be reached after a failure. |

The docstring describes intended session-isolation reasons (pytest import mode and duplicate test basenames), but the corresponding configurations and full trees are absent. Those explanations were read as design statements, not independently verified environment facts. Ordinary `--then` mode invokes pytest directly and does not use the family discovery/exclusion path (runner lines 168–176).

### What the test file establishes

The file contains meaningful checks, but their definitions are not pass results:

- [Lines 49–73](../../../src/tests/test_run_package_tests.py#L49) inspect generated command tokens and expected workflow subdirectories. The name “covers every CI test surface” does not establish an exhaustive CI inventory or actual execution of those commands.
- [Lines 76–101](../../../src/tests/test_run_package_tests.py#L76) define Mermaid command-order assertions and execution of one relocated memory-test command. Command-list membership does not prove the validator ran; the memory test, if passed, would support that subset under its environment, not all groups.
- [Lines 119–184](../../../src/tests/test_run_package_tests.py#L119) define nested-worktree ignore checks and real pytest collection checks for worktree/clone fixtures. The collection helper returns only stdout and does not assert subprocess success, so absence of a test name alone can also occur after a collection failure. [Lines 208–277](../../../src/tests/test_run_package_tests.py#L208) contain other collection helpers that do assert success, plus discovery, local exclusion, session separation, and a failing design-test propagation scenario.
- [Lines 187–197](../../../src/tests/test_run_package_tests.py#L187) read kickoff documentation and three CI workflow files and assert a runner-command substring. Those files are absent from this snapshot. Even a successful substring assertion would not establish enabled jobs, matrix coverage, conditions, runtime success, or the absence of other required checks.
- [Lines 285–331](../../../src/tests/test_run_package_tests.py#L285) define shell-command discovery and foreign-tree omission assertions; these do not execute the selected shell scripts. [Lines 22–30](../../../src/tests/test_run_package_tests.py#L22) check a successful ordinary group followed by a failing group; they do not test that a failed first group prevents a later group from executing. Fail-fast control flow is supported by reading the implementation instead.

There is no supplied result showing this test module ran or passed at the assessed revision. Several definitions require absent repository content; running this minimal snapshot would not reproduce the complete repository's CI environment even if execution were permitted.

## Evidence

All implementation/test citations above refer to the four snapshot files attributed to the recorded commit. Files were read with line numbers; no upstream permalink or remote state was verified. Source links resolve locally; line fragments identify inspected anchors.

Executed identity check:

```text
shasum -a 256 src/scripts/run_package_tests.py src/loom-code/scripts/repo_files.py src/loom-code/scripts/git_exec.py src/tests/test_run_package_tests.py
```

Observed output, in that order:

```text
6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54
62333168fb9eacabb6877d0f185f08081175d8681444465173b18d712ca26399
9c721b8e2f8fae0e4c31da5d6ab41b42e0ae4eeb8cecbf164a36fce7dd61e7c7
b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28
```

All four match `provenance.json`. This verifies supplied bytes against the supplied manifest, not independent authenticity of the original commit, completeness, CI status, or artifact identity.

The supplied [B01](../../../samples/timing/B01.json) and [B02](../../../samples/timing/B02.json) receipts report successful research-process exits. Their [task summary](../../../samples/timing/task-summary.json) describes source-only investigations, not package-test runs; those exit codes and timing/token data are not CI evidence. The [migration excerpt](../../../samples/migration/docs/loom/research/2026-11-08-package-runner-exclusions.md) contains evidence-link rows without original findings. It supplies no execution result and was not substituted for current source inspection. Its duplicate snapshot was unnecessary to this decision and was not used to establish implementation behavior.

## Decision impact

The snapshot supports “the recorded source implements a bounded family runner and defines tests for several important behaviors.” It does **not** support “all CI at current HEAD passed,” “the test surface is complete,” or “the release candidate is ready.” Do not use these two source-presence observations as the basis for that approval. This research neither accepts nor rejects a release on the user's behalf.

The following missing evidence could change the release decision; these are evidence requests for an authorized owner, not actions performed or newly authorized here:

| Decision-changing gap | Evidence needed and why it matters |
| --- | --- |
| Which exact revision is being approved? | Candidate source identity and CI checkout SHA tied to the recorded commit, including any merge/test SHA distinction and relevant source changes. Locally recorded branch equality and matching four-file hashes cannot bind a new HEAD or built artifact to the assessed source. |
| What constitutes the whole required CI surface? | Actual workflow files at that revision, job/matrix definitions, triggers, conditions, working directories, selected `--only` groups, required checks, and release criteria. Compare the full test/check inventory and relevant pytest configuration with runner roots and intentional exclusions. Missing content here is a snapshot limit, not proof it is absent upstream. |
| Did the required work actually execute successfully? | Revision-bound run/job records and logs for every required job/matrix entry, with collection/execution counts, failures, skips, cancellations, and allowed-failure handling. Include Python, shell, Mermaid positive/negative checks and other required CI checks. Establish that green status did not come from omitted jobs or an empty command list and that later stages were reached. |
| Were runtime conditions applicable? | Runner environment/tool versions, dependency manifests/locks and installation evidence, pytest plugins/configuration, Node/npm/Bash availability, and relevant Git-query success/layout. These affect imports, discovery, isolation, foreign-tree exclusion and validator execution. A synthetic test definition does not establish these conditions in CI. |
| Is the tested source the release candidate? | Candidate package/build identity and digest tied to that source and successful required checks, packaging contents, applicable release validation and acceptance criteria. Runner success alone cannot establish correct packaging or release suitability. Existing verifiable records may suffice; this report does not require rerunning everything or executing a deployment. |

## Limitations and open questions

No CI definitions, full test inventory, dependency/configuration set, execution logs, complete repository history, or release artifact were supplied. Consequently actual CI success, coverage completeness, exclusion behavior in the target environment, and release-candidate equivalence remain unresolved. Static failure paths identify possible limits, not observed failures. A later source revision, changed workflow, environment, or artifact requires evidence matched to those conditions.

The saved record was read back in full, and its relative file targets were checked for existence. This verifies the retained research artifact and links; it does not validate the software or authorize publication.
