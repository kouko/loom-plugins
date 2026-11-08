---
title: "Does the package-runner snapshot justify HEAD CI approval and release?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Does the package-runner snapshot justify HEAD CI approval and release?

## Question and scope

Can the presence of `--loom-family` and coverage definitions in `tests/test_run_package_tests.py` justify declaring all CI successful and releasing the recorded HEAD? **No.** The snapshot supports bounded implementation and test-definition claims; actual CI success and release readiness remain unresolved. This is an evidence assessment, not acceptance or release authorization. It also does not establish that CI failed.

The supplied [provenance](../../../provenance.json) records HEAD and locally recorded origin/main as `d5a7f0da247214bdb9c61fe90c550256432e5f76`, with remote freshness explicitly “not checked.” The original repository path is provenance text only; it was not accessed. Four source files constitute a partial snapshot, not a checkout. No active change exists.

Only supplied workspace evidence was read. No tests (including collect-only), runner/import execution, installation, network, apps, external models, agents, Git repository creation, commits, publication or acceptance actions were performed. Writes are limited to this research record.

## Method and rationale

Direct source, connected-call-path and artifact inspection fits a capability/completion claim. The decision criteria are revision identity, actual CI integration, completeness of executed coverage, successful results, and linkage to the intended release artifact. No score or benchmark can replace missing run evidence. The stopping condition is establishing which premises are supported and which missing observations could change the release decision; obtaining those observations is outside this task.

The explicitly invoked [skill](../../../skill/engineering-research/SKILL.md), its [methods](../../../skill/engineering-research/references/research-methods.md), [source policy](../../../skill/engineering-research/references/source-policy.md), [evaluation selection](../../../skill/engineering-research/references/evaluation-selection.md), and [template](../../../skill/engineering-research/templates/research.md) were read and applied. External reference links were not opened. Samples were checked only for applicability; they do not supply CI results.

## Findings

### Source-supported behavior, not observed execution

- The family branch is selected only when `--loom-family` is the first argument. It uses `Path.cwd()` as the target repository, validates a missing/unknown `--only` value, and constructs commands for all groups or one selected group. It executes sequentially and returns immediately on a nonzero child result. Later commands therefore need not have run after a failure. A returned zero means the generated command list completed without a nonzero result; there is no independent completeness check (E1).
- Five group names exist: `code`, `design`, `workflow-python`, `workflow-shell`, and `workflow-mermaid`. Code uses one pytest session with `-n auto`; design uses its own session; workflow Python splits the top level and eligible immediate subfolders into sessions. Discovery is bounded by four configured roots and supported filename patterns. Root-level `local/` exclusions and discovery filters exist; this is not proof that every release-required test is inside those boundaries or collected under the missing pytest configuration (E2).
- Python sessions receive ignores for the union of nested repositories and nested worktrees; discovered shell tests under that union are omitted. Mermaid adds fixed npm installation, Node validation and negative-check commands. Those command definitions do not establish dependency installation or validator success (E2).
- The exclusion path depends on Git queries. `nested_repositories` derives real, non-symlink directory entries from `_git_entries`; `nested_worktrees` filters strict descendant worktrees. Git failures can become `None`, then empty exclusion lists. In particular, Git availability/query failure can remove exclusion information without making command construction fail. The no-Git file-walk fallback does not supply exclusions through `nested_repositories`. This is a source-supported boundary, not an observed failure in the intended CI environment (E3–E4).
- In family mode, absent Python roots or roots with no recognized test files can produce no Python command; an empty shell inventory can likewise produce no shell commands. With `--only`, an empty generated list reaches return zero. Full family mode still adds fixed Mermaid commands. Thus even a hypothetical zero exit would require inventory and scope evidence before being interpreted as complete CI success (E1–E2).

### What the tests do and do not establish

The test source defines checks for grouping, argument errors, later-group failure, command surfaces, Mermaid ordering, relocated memory tests, discovery/local exclusions, workflow session isolation, nested worktree/clone collection exclusions, and shell exclusions (E5). Some definitions call real subprocesses and collection when executed; none were executed here. Their presence proves definitions exist, not that those assertions passed at HEAD.

The CI/kickoff test at lines 187–197 only searches for a command substring in three workflow files and a kickoff document. Even a pass would not establish workflow triggers, job conditions, all group selections, dependencies, matrix coverage or successful execution. Those workflow files and kickoff document are absent from this snapshot (E6).

There are specific limits to the test evidence: `_collect_with_runner_ignores` returns stdout without asserting the collection subprocess exit status, and its two callers check only that foreign test names are absent. Collection failure could also yield absence. By contrast, `_collected` asserts a zero status, but removes `-n auto`, so those checks do not exercise the actual xdist invocation. The later-group-failure test begins with a successful group and does not demonstrate that a failed first group prevents the next from running. These are limits to the definitions, not reported test failures (E5).

### Artifact observations

All four source SHA256 values match the supplied provenance (E7). This verifies byte consistency with the local manifest; it does not independently authenticate the commit, remote branch state, CI run or released artifact.

The timing receipts describe source-only research tasks with different scopes. Their successful process exit codes concern those research processes, not package tests or CI. The extracted migration note contains evidence-link rows, not complete findings or execution logs. None upgrades the source assessment to runtime verification (E8).

## Evidence

All source anchors below refer to supplied bytes attributed by the manifest to the recorded HEAD. Evidence type is static inspection unless explicitly stated otherwise.

| ID | Inspected evidence and anchors | Supported scope and verification status |
|---|---|---|
| E1 | [Runner entry point](../../../src/scripts/run_package_tests.py#L153), lines 153–180; argument splitting at 58–65 | Branch selection, cwd, validation, sequential dispatch and failure propagation; source only. |
| E2 | [Runner discovery and construction](../../../src/scripts/run_package_tests.py#L51), lines 51–150 | Four roots; discovery helpers, grouping, exclusions, fixed Mermaid commands; source only. |
| E3 | [Repository helpers](../../../src/loom-code/scripts/repo_files.py#L73), lines 73–146; fallback at 149–168 | Worktree listing, opaque-directory exclusions, symlink guard, bare/no-Git branches. The worktree docstring states Git >= 2.36 for its NUL format; no runtime compatibility check occurred. |
| E4 | [Git wrapper](../../../src/loom-code/scripts/git_exec.py#L50), lines 50–88 | UTF-8/surrogateescape arguments/output; default nonzero/OSError/timeout-to-None behavior; source only. |
| E5 | [Test definitions](../../../src/tests/test_run_package_tests.py#L16), lines 16–184 and 203–331 | Assertions and subprocess helpers were read, including collection-status limitations at 142–156 and xdist removal at 208–219; no tests run. |
| E6 | [CI substring assertions](../../../src/tests/test_run_package_tests.py#L187), lines 187–197 | Refers to three workflows and kickoff document; their actual content is unavailable. |
| E7 | [Provenance](../../../provenance.json) and four source files linked above | `shasum -a 256` on the four files returned the four manifest hashes exactly. `rg --files --hidden src` listed only those four source files. Explicit path checks found no `src/.github`, design/workflow/code test trees or kickoff document. These are local hash/path observations, not test execution. |
| E8 | [Task scopes](../../../samples/timing/task-summary.json), [B01 receipt](../../../samples/timing/B01.json), [B02 receipt](../../../samples/timing/B02.json), [excerpt](../../../samples/migration/docs/loom/research/2026-11-08-package-runner-exclusions.md), [sample provenance](../../../samples/migration/provenance.json) | Inspected supplied extracts only. Research receipts report exit 0 and no timeout; no CI run, package-test result or release verification is supplied. Original receipt hashes cannot be verified against full originals because only extracts are available. |

Hash command actually used:

```text
shasum -a 256 src/scripts/run_package_tests.py src/loom-code/scripts/repo_files.py src/loom-code/scripts/git_exec.py src/tests/test_run_package_tests.py
```

Actual output, in that order:

```text
6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54
62333168fb9eacabb6877d0f185f08081175d8681444465173b18d712ca26399
9c721b8e2f8fae0e4c31da5d6ab41b42e0ae4eeb8cecbf164a36fce7dd61e7c7
b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28
```

## Decision impact

The proposed justification is insufficient. Retain the narrow conclusion that the recorded source implements a family runner and defines relevant tests. Leave “all CI passed” and “ready to release” unverified. The following evidence could change that assessment; this list identifies evidence to obtain through the owning process, not actions performed or authorized here.

| Missing evidence | Why it could change the decision |
|---|---|
| Exact target revision and release candidate identity, including any differences from the recorded HEAD | A green result for another revision or different artifact does not substantiate this release. Locally equal HEAD/origin-main values do not establish current remote state. |
| Complete workflows at that revision, required-check/release policy, triggers, paths, conditions, matrix, cwd, wrappers and group arguments | CI may select only some groups, skip jobs, mask failures or run other required checks absent from this snapshot. No supplied policy defines the full release gate. |
| Complete test inventory, pytest configuration/conftest, manifests/locks, validators and relevant implementation, mapped to required behavior | Determines whether roots, patterns and exclusions cover the intended surface; missing configuration may alter collection. This snapshot cannot validate the full suite's collection or integration. |
| Inspectable CI run records tied to that exact revision, with every required job's status, executed commands, collection counts/skips and failure output | Distinguishes actual execution and complete success from definitions, skipped/cancelled work, empty inventories or a successful wrapper. Needed for code, design, workflow Python, shell, Mermaid and any additional required checks. |
| Applicable runtime/environment records: Python/pytest/xdist, Git, Node/npm, dependencies, OS and repository layout | Could expose missing dependencies, Git-query/exclusion gaps, collection conflicts or environment-specific failures. Source comments cannot establish installed versions or compatibility. |
| Applicable packaging/release checks and artifact-to-revision linkage; deployment/recovery evidence if the intended release includes deployment | CI success alone does not prove the intended artifact was built correctly or satisfies the actual release contract. The release mechanism, targets and acceptance criteria are not supplied; no universal deployment checklist is assumed. |

## Limitations and open questions

This concluded research has an unresolved release-readiness result. No actual runtime behavior, historical CI success, remote freshness, complete repository correctness or deployment outcome was established. Snapshot omissions do not prove files are absent from the original repository. The manifest attribution is supplied evidence, not independently verified Git history.

The material open questions are: What exactly constitutes required CI and the intended release? Did every required check actually run and pass for this exact candidate with the intended inventory/environment? Does the release artifact correspond to that candidate and meet the applicable release checks? New revision, configuration, environment or release-scope evidence requires revalidation. Approval and release remain with the owning human process.
