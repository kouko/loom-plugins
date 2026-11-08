---
title: "Can callers preview package-suite commands without running tests?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Can callers preview package-suite commands without running tests?

## Question and scope

Determine the smallest way to preview the Loom package suite's commands without
starting pytest, npm, or shell tests, or duplicating discovery rules. This is
isolated research on the supplied minimal source snapshot, not an implementation
change, full checkout, installation, deployment, or CI validation. No active
change exists. Date: 2026-11-08.

[Provenance](../../../provenance.json) identifies source commit
`d5a7f0da247214bdb9c61fe90c550256432e5f76`; remote freshness was not checked.
Its original repository path is metadata only and was not accessed.

## Method and rationale

Inspect the command builder, its execution caller, connected Git helpers, and
relevant test definitions; then run the single authorized empty-directory
experiment. This directly distinguishes command construction from execution.
Stop once reuse feasibility and material limitations are established. No network,
apps, agents, installation, repository creation, commits, or test runs were used.
The bundled research methods, source policy, and template were read. Unrelated
sample trials were not needed as evidence for this question.

## Findings

**Source-supported answer: reuse the existing function; a runner rewrite is
unnecessary.** `loom_family_commands(repo, verbosity="-q", only=None)` returns
`list[list[str]]`, with each inner list an argv vector. It builds commands rather
than executing the returned pytest, npm, node, or bash commands. Import is guarded
from invoking `main()` by the `__name__ == "__main__"` check. The module does alter
`sys.path` to import its sibling-tree helpers.

The execution boundary is explicit: `main()` calls this same builder, then calls
`subprocess.call(command)` sequentially and stops at the first nonzero result.
Preview therefore represents the ordered plan; later commands may never run if
an earlier command fails.

**Observed in the permitted experiment:** importing the actual snapshot module
and calling the builder once with an empty temporary directory and
`only="workflow-mermaid"` returned exactly these three vectors:

```text
[['npm', 'ci', '--prefix', 'loom-workflow/tests/mermaid'], ['node', 'loom-workflow/tests/mermaid/validate_mermaid.mjs'], ['bash', 'loom-workflow/tests/mermaid-validator-negative.sh']]
```

The script printed this value and did not execute any returned vector. This also
shows that the Mermaid plan is unconditional: the empty fixture lacked those
target paths, yet the builder still returned them. It does not validate target
existence, installed tools, dependencies, or successful execution.

**Important boundary:** construction is not free of subprocesses. Before selecting
any group, the builder calls `nested_repositories()` and `nested_worktrees()`.
Those use `run_git()`, which invokes read-only Git queries via `subprocess.run()`.
Thus the existing API satisfies the requested prohibition on starting tests and
npm; it would not satisfy a stronger prohibition on all child processes. Git
failures can produce empty exclusion lists rather than a hard error. Do not
interpret a returned list as proof of complete foreign-repository exclusions
under unavailable or failing Git.

## Evidence

All implementation citations below refer to the supplied commit above. Source
inspection supports code behavior; test definitions were read but never run.

| Evidence | Inspected location and what it establishes |
| --- | --- |
| Builder and discovery | [run_package_tests.py](../../../src/scripts/run_package_tests.py), lines 51–55 and 68–150: shared roots, Python session partitioning, shell discovery, local/node_modules filtering, foreign-tree exclusions, group selection, argv construction and return. |
| Import and execution boundary | [run_package_tests.py](../../../src/scripts/run_package_tests.py), lines 43–49 and 153–180: import path change; CLI group validation; immediate execution in `main()`; guarded entry point. No CLI preview branch exists in this inspected implementation. |
| Git dependency and fallback | [repo_files.py](../../../src/loom-code/scripts/repo_files.py), lines 73–146: worktree listing, repository entries, rev-parse and ls-files queries; unavailable Git paths return empty exclusions. [git_exec.py](../../../src/loom-code/scripts/git_exec.py), lines 50–88: actual subprocess call and failure handling. |
| Defined expectations | [test_run_package_tests.py](../../../src/tests/test_run_package_tests.py), lines 49–84: consumers already call the builder and assert command contents; Mermaid vectors match the observed result. Lines 119–184 and 260–331 define exclusion, session and shell cases. These definitions are not passing-test evidence. |
| Local measurement | [scratch script](../../../scratch/preview_package_commands.py): one real import and one builder call, no mocks and no execution loop. Command: `python3 -I -B scratch/preview_package_commands.py`. Exit code 0; stdout is retained verbatim above. |

The experiment held the imported snapshot and default verbosity constant, selected
only the Mermaid group, and supplied an empty temporary directory under `scratch/`.
It created no Git repository. Python isolated mode and disabled bytecode writing
kept the run separate from Python user configuration and avoided source writes.
The script disabled system/global Git configuration and set a Git ceiling at
`scratch/` to prevent ancestor-repository discovery. The temporary fixture was
removed by its context manager. A construction failure or execution of a returned
command would have changed the reuse assessment; neither occurred on this path.
No subprocess trace was collected; the execution distinction rests on the script
and inspected connected source, not an assertion that zero subprocesses ran.

SHA256 checks using `shasum -a 256` matched every entry in `provenance.json`:

| Source path under `src/` | Observed SHA256 |
| --- | --- |
| `scripts/run_package_tests.py` | `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54` |
| `loom-code/scripts/repo_files.py` | `62333168fb9eacabb6877d0f185f08081175d8681444465173b18d712ca26399` |
| `loom-code/scripts/git_exec.py` | `9c721b8e2f8fae0e4c31da5d6ab41b42e0ae4eeb8cecbf164a36fce7dd61e7c7` |
| `tests/test_run_package_tests.py` | `b7ed3d4e19fd4d03c68df5d8ca796d03442a859874745564c20ddaeb7780da28` |

## Decision impact

1. **Minimum for a Python caller: no runner changes.** Import the existing
   builder and render or serialize `loom_family_commands(repo.resolve(),
   verbosity="-q", only=group)`. Validate a supplied group against the existing
   `GROUPS` constant: validation currently lives in `main()`, and an invalid
   direct-call group can silently yield an empty list. Preserve argv arrays
   (for example as JSON), their order, and the intended repository working
   directory. Formatting must not add discovery logic or execute commands.
2. **If a CLI preview is required: add a small preview branch.** In a future
   authorized implementation, retain the existing validation, build the list once,
   print it and return before the execution loop when preview is selected. Both
   preview and execution should consume the same builder. This is a localized
   addition, not a new runner or copied discovery implementation. No such change
   was made in this research.

Calling `main()` is unsuitable for preview. Neither passing a made-up `--dry-run`
flag nor using pytest `--collect-only` meets this requirement: the inspected CLI
has no preview handling, and collection still starts pytest. A separate scanner
or hard-coded command inventory would violate the shared-discovery requirement.

## Limitations and open questions

- Only the Mermaid builder path on an empty directory was measured. Full-suite
  discovery, nested-repository behavior, successful command execution, CI and
  deployment remain untested. The partial snapshot cannot establish the actual
  full-checkout command inventory or missing workflow/configuration behavior.
- Discovery depends on filesystem and Git state at preview time. A later builder
  call can differ after changes; the current API provides no frozen-plan or
  approval/execution binding. Pytest directory targets also do not enumerate
  individual collected tests.
- Several vectors contain repository-relative paths. The caller must supply the
  intended root for discovery and retain that working directory for any later
  execution; `repo` does not set execution cwd. Python commands use the preview
  process's `sys.executable`, so interpreter identity also matters.
- This script function is a demonstrated local reuse point, not evidence of a
  versioned public library API. It requires the sibling `loom-code/scripts`
  helpers and a compatible Python interpreter. Python/Git versions were not
  inventoried; npm/node/pytest availability was not probed.
- A future requirement for zero subprocesses or guaranteed exclusion diagnostics
  would require additional design and validation. Neither is established here.

The saved record was read back in full and its local link targets checked before
delivery; this verifies the retained research artifact, not the unexecuted suite.
