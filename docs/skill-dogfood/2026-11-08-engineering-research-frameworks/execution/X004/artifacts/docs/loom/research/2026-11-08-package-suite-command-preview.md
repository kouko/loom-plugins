---
title: "Can callers preview package suite commands without running tests?"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Can callers preview package suite commands without running tests?

## Question and scope

Determine whether callers can preview the Loom package suite's commands without
starting pytest, npm, or shell tests and without duplicating discovery. This is
an isolated, local-source assessment dated 2026-11-08, with no active change.
The provided `src/` is a minimal snapshot, not a full checkout or CI/deployment
result. No runner implementation changes are authorized or made.

[Provenance](../../../provenance.json) identifies source commit
`d5a7f0da247214bdb9c61fe90c550256432e5f76` and the original repository path.
That path is provenance only; it was not accessed. Remote freshness is unknown.
SHA256 checks of all four provided source files matched their provenance entries.

## Method and rationale

Use direct implementation inspection, a small qualitative comparison, and the
single authorized feasibility experiment. Mandatory criteria are no test-command
execution and reuse of existing discovery. Trace the builder, its filesystem/Git
helpers, and the execution entry point; inspect relevant test definitions without
running them. The experiment asks only whether importing the actual runner and
calling its Mermaid builder on an empty temporary directory returns commands.
Keep source and selection fixed; supply only an empty directory as the repository
root, with no real-checkout comparison run. An import failure or attempt to execute the
returned commands would undermine the direct-call recommendation. Stop after
that observation; do not run tests, collect tests, install dependencies, or
consult external sources. This follows the invoked
[engineering-research skill](../../../skill/engineering-research/SKILL.md) and
its bundled method, source-policy, evaluation-selection, and record template.

## Findings

**Source-supported:** Existing `loom_family_commands(repo, verbosity="-q",
only=None) -> list[list[str]]` already separates command construction from
execution. It returns ordered argv lists and does not invoke pytest, npm, node,
or bash. `main()` calls the builder and then executes those lists using
`subprocess.call`; callers must use the builder directly for preview.

**Source-supported qualification:** Construction is not free of subprocesses.
It unconditionally discovers foreign subtrees using `nested_repositories` and
`nested_worktrees`, including for `only="workflow-mermaid"`. Those helpers invoke
read-only Git queries through `run_git`. Other groups also inspect filesystem
contents. Thus the existing function satisfies “do not launch tests,” but would
not satisfy a stricter “no subprocess or filesystem access” requirement.

**Observed:** The one permitted experiment imported the actual snapshot runner
and returned the three Mermaid argv lists below from an empty temporary directory.
The script printed them and never passed them to an executor. This establishes
the bounded construction result, not that any command can successfully run.

## Evidence

All implementation evidence below is local source inspection at the provenance
commit, verified against the supplied hashes, unless explicitly marked observed.
Line references identify the inspected definitions in the linked files.

| Claim | Evidence and verification status |
| --- | --- |
| One existing command builder can serve preview and execution | [run_package_tests.py](../../../src/scripts/run_package_tests.py), `loom_family_commands`, lines 116–150: creates and returns argv lists. `main`, lines 153–180: validates CLI selection, executes commands, and is protected by the `__main__` guard. Importing does not call `main`. |
| Preview need not replicate discovery | Same file, lines 51–55 and 68–149: `TEST_ROOTS`, Python filename detection, local/node_modules exclusions, separate workflow sessions, shell discovery, foreign-subtree filtering, pytest ignores, and the fixed Mermaid commands all live behind the builder. |
| Builder still launches Git probes | [repo_files.py](../../../src/loom-code/scripts/repo_files.py), `nested_repositories`, `nested_worktrees`, `_git_entries`, lines 73–146: `rev-parse`, `ls-files`, and `worktree list`; [git_exec.py](../../../src/loom-code/scripts/git_exec.py), `run_git`, lines 50–88: invokes `subprocess.run` with argv, captures output, returns `None` on default-mode failures. No Git query is a test command. |
| CLI is not an existing preview interface | [run_package_tests.py](../../../src/scripts/run_package_tests.py), lines 153–176: no preview branch; a valid family request executes commands. Extra family flags are not generally rejected, so adding an unsupported `--dry-run` flag does not safely request preview. |
| Mermaid command shape has a source-level test definition | [test_run_package_tests.py](../../../src/tests/test_run_package_tests.py), lines 76–84: expects npm ci, node validator, then bash negative check. This test was read, not executed; its assertions are not a passing CI result. |

Experiment artifact: [preview_package_commands.py](../../../scratch/preview_package_commands.py).
Executed exactly once from the workspace root:

```sh
python3 -I -B scratch/preview_package_commands.py
```

The script uses `importlib` to import `src/scripts/run_package_tests.py`, creates
an empty temporary directory under `scratch/`, and prints
`loom_family_commands(Path(empty), only="workflow-mermaid")`. It does not call
`main`, patch discovery, or execute any returned argv. Python bytecode writes
are disabled. For the builder's Git probes, the script clears inherited
environment overrides, disables global/system Git configuration, and sets a
scratch discovery ceiling to avoid accessing ancestor repositories or real user
settings. The temporary empty directory is removed afterward. No repository was
created. The command exited 0 with this actual stdout:

```text
[['npm', 'ci', '--prefix', 'loom-workflow/tests/mermaid'], ['node', 'loom-workflow/tests/mermaid/validate_mermaid.mjs'], ['bash', 'loom-workflow/tests/mermaid-validator-negative.sh']]
```

## Decision impact

**Recommend direct builder reuse; no runner rewrite is needed.** A Python caller
can import the existing module, validate `only` against its exported `GROUPS`,
call `loom_family_commands` with an absolute repository root and the intended
verbosity/selection, and display or serialize the returned argv lists. This is
the minimum viable option and requires no runner changes or second discovery
implementation. Import requires the sibling `loom-code/scripts` helpers; the
module itself inserts that location into `sys.path`, so this is an in-repository
Python integration rather than a separately packaged stable API.

If a command-line preview is required, the smallest proposed change is an
explicit preview flag in the family CLI: retain its existing validation, call
the same builder once, serialize its result, and return before the execution
loop. Normal execution should consume the same builder result. This is a
recommendation only, not an implemented or runtime-verified CLI feature.
Rewriting the runner or independently scanning tests adds change surface and
risks divergent discovery without addressing a gap in the existing builder.

Preserve argv boundaries, preferably as JSON arrays; joining with spaces is
ambiguous for paths containing spaces or special characters. Include the
intended working directory in the preview presentation: Python/Mermaid targets
include repository-relative paths, and `main` builds for `Path.cwd()`. A later
executor must use the matching repository cwd. No executor is part of this
research.

## Limitations and open questions

- This is a plan of suite commands, not a list of pytest-collected test cases.
  The builder selects targets without running pytest collection or test modules.
- Direct API calls do not validate `only` as `main` does: an unknown string can
  return an empty list after Git discovery. Reuse `GROUPS` for validation; do not
  interpret an empty result as proof of a valid selection.
- The Mermaid branch emits its fixed commands even when their target files and
  dependencies do not exist, as the empty-directory observation illustrates.
  Preview does not install npm dependencies or validate executable availability.
- `sys.executable`, absolute ignore paths, discovered files, and Git metadata
  make plans environment-dependent. Git failure/missing Git can yield empty
  foreign-subtree exclusions rather than a preview error. No real nested-repo
  exclusion behavior was measured here.
- Later filesystem or Git changes can alter a regenerated plan. `main` stops at
  the first nonzero command, so the list describes intended order, not a promise
  that every listed command will run. Keeping the same list avoids rediscovery
  drift but cannot freeze the files or dependency state.
- Only the authorized empty-directory Mermaid construction ran. Full-family
  discovery, ordinary `--then` mode, collection, execution, CI, deployment,
  dependency readiness, and other revisions remain unverified. Some referenced
  test definitions require artifacts absent from this minimal snapshot.
- If the contract later prohibits all subprocesses, or requires a stable public
  API or identical future execution despite repository changes, reassess those
  requirements. They are not established by this experiment and may need a
  focused API change, rather than a wholesale runner rewrite.

The saved record was read back against the source excerpts and actual experiment
output. No pytest/npm/shell test, network access, app, external model, installation,
commit, or publication was used.
