---
title: "Package runner exclusion design and failure order"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---


# Evidence links (verbatim rows excerpted from the original note; no findings supplied)
| E1 | [runner](../../../src/scripts/run_package_tests.py#L153), lines 153–180; `split_groups`, lines 58–65 | Entry branch, `--only`, current-directory root, sequential execution, immediate failure return in both modes. |
| E2 | [repo_files](../../../src/loom-code/scripts/repo_files.py#L97), lines 97–146; ignored names, lines 59–61 and 171–172 | Opaque-directory inventory, symlink guard, bare/no-Git branches, Git listing flags, ignored path components. |
| E3 | [nested_worktrees](../../../src/loom-code/scripts/repo_files.py#L73), lines 73–94 | Independent worktree listing, strict descendant filter, empty list on failed query; docstring identifies Git >= 2.36 for NUL format. |
| E4 | [git_exec](../../../src/loom-code/scripts/git_exec.py#L50), lines 50–88 | `git -C`, UTF-8/surrogateescape handling, nonzero/OSError/timeout converted to `None` by default. |
| E5 | [command construction](../../../src/scripts/run_package_tests.py#L68), lines 68–150; roots, lines 51–55 | Discovery scope, local/node_modules rules, session ordering, foreign union, pytest ignores, shell filter and fixed Mermaid commands. |
| E6 | [test definitions](../../../src/tests/test_run_package_tests.py#L119), lines 119–184 and 314–331 | Definitions check worktree ignore tokens, real collect-only exclusion for a nested worktree and initialized nested repository, and omission of worktree/clone shell scripts. They were not executed here. |
| E7 | [ordering-related tests](../../../src/tests/test_run_package_tests.py#L22), lines 22–30, 76–84 and 260–277 | Definitions check later-group failure returns nonzero, Mermaid command order, and workflow session separation. The later-group test starts with a successful group; it does not verify that a failed first group prevents the second from running. |
