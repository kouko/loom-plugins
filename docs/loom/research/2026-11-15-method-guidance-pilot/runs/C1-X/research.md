---
title: "Scope of a successful Loom package suite"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags:
  - loom/research
---

# Scope of a successful Loom package suite

## Question and scope

Can the package runner justify “every repository test, including local-CLI tests, ran”? No. The sufficient evidence is the implemented selection, exclusion, grouping and exit behavior of the current runner. This is an offline source inspection at HEAD `4d44cd3ce2889c552d46ca4687596bc4f5298a17`; no full suite or individual test was executed.

## Method and rationale

Read the runner and its connected repository-discovery helpers, then inspect focused test definitions for contradictory boundaries. This implementation question needs no external research or experiment: explicit exclusions already refute the universal claim. The dependency lock is relevant to reproducibility, not proof of execution.

## Findings and evidence

1. **The family suite has four roots, not the entire repository.** `TEST_ROOTS` contains `tests`, `loom-code/tests`, `loom-design/tests` and `loom-workflow/tests`. Python presence discovery recognizes `test_*.py` and `*_test.py`; shell discovery recognizes `test-*.sh`. Python directories are passed to pytest, so its collection configuration and test-level skips still matter. [Runner, lines 51–95](../../../../../../scripts/run_package_tests.py#L51).
2. **Root-level `local/` tests are deliberately excluded.** Python sessions add `--ignore` for each root's `local` directory; workflow splits also exclude its root `local`. Shell discovery filters descendants of the root's `local`. This is an exact root-relative exclusion, not a blanket filter on every directory named `local`. Concrete existing excluded CLI scripts include `loom-code/tests/local/test-superpowers-mode-on.sh` and `test-git-memory-delegation.sh`. [Python/shell discovery, lines 76–113](../../../../../../scripts/run_package_tests.py#L76); [local script](../../../../../../loom-code/tests/local/test-superpowers-mode-on.sh). Focused tests define expected local exclusions for all group types, but were read rather than run. [Tests, lines 222–298](../../../../../../tests/test_run_package_tests.py#L222).
3. **Foreign nested repositories are excluded separately.** The union of `nested_repositories` and `nested_worktrees` becomes pytest `--ignore` arguments and filters shell commands. The helper uses Git's collapsed directory entries and registered worktrees strictly below the repository root. Missing/unusable Git discovery can return an empty list, so the source does not guarantee all foreign trees are identified in every environment. [Runner, lines 123–149](../../../../../../scripts/run_package_tests.py#L123); [helpers, lines 73–147](../../../../../../loom-code/scripts/repo_files.py#L73).
4. **Grouping changes the claim.** Code roots run together with xdist; design gets a separate session; workflow Python gets top-level and qualifying immediate-subdirectory sessions. Immediate workflow subfolders beginning with `.` or `_`, and `node_modules`, do not become separate sessions; only selected subfolders are ignored from a possible top-level session, so that selection rule alone does not establish universal exclusion of dotted/underscored descendants. Shell discovery filters `node_modules`. [Session construction, lines 68–145](../../../../../../scripts/run_package_tests.py#L68).
5. **A complete family invocation also includes Mermaid commands.** The runner invokes `npm ci`, the Node validator and a negative shell check; this is not purely a Python suite and would install dependencies if executed. These commands were not executed here. [Mermaid group, lines 139–145](../../../../../../scripts/run_package_tests.py#L139).
6. **Exit zero has bounded meaning.** `--loom-family` without `--only` runs all generated groups and returns at the first nonzero subprocess result. `--only` runs just one named group. Ordinary `--then` mode runs user-supplied pytest argument groups and does not apply family inventory/exclusions automatically. Zero means all generated subprocesses returned zero, not that every possible repository test executed or every collected case passed without skips. [Main, lines 153–176](../../../../../../scripts/run_package_tests.py#L153).
7. **Pinned dependencies do not prove installed or executed versions.** The lock specifies pytest 9.1.1 and pytest-xdist 3.8.0, among other packages. No installation or environment parity was checked. [Lock, lines 35–43](../../../../../../requirements-package-tests.lock#L35).

## Decision impact

A defensible report after an actually observed successful run is: “The Loom package suite (`python3 scripts/run_package_tests.py --loom-family`, no `--only`) completed successfully for this checkout and environment: all generated package-suite commands returned zero. It covers the configured roots and Mermaid checks, with root-local CLI tests and detected nested repositories excluded; pytest collection rules and reported skips still apply.” Attach actual output and skip counts before claiming individual cases ran. For a selected group or explicit pytest arguments, name that narrower scope instead. Reject “every repository test, including local-CLI tests, ran.”

## Limitations and open questions

This investigation establishes implementation behavior, not a historical or current successful execution. No full suite, collection run, npm command, CLI script or focused test was run. No exhaustive repository inventory or test-level skip audit was attempted; the universal claim is already disproved by explicit local exclusions. Source links refer to current working-tree files at the recorded HEAD and may drift after edits. Two attempted pytest configuration paths and three optional local directories were absent; those missing paths were not treated as evidence of broader absence. The lock's package versions are source observations only.
