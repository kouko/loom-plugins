---
title: "Which phase stalls in the fake CLI preflight?"
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
tags: [loom/research]
change: 2026-11-12-design-research-method-selection
---

# Fake CLI preflight phase diagnosis

## Question and scope

Why does an existing five-second fake-Claude preflight time out in the full
parallel code suite, including after its Python fake was replaced by shell?
The decision is whether another fixture change is supported or whether the
execution environment remains the consequential unknown. Research requirements,
production runner behavior, deadlines and package worker settings stay fixed.

## Method and rationale

Hypothesis-driven local diagnosis. Inspect the real launch path and retained
failure artifacts, then add phase markers only in an isolated clone and run
the same code group with the declared lock and default `-n auto` behavior.
No external search is needed for this project execution question. Stop after
the bounded diagnostic run and inspect actual marker/output evidence before
choosing another implementation; a passing diagnostic does not recover missing
historical timing data.

## Findings

- Observed: first Build passed; successive finalizations and the latest Build
  failed either the blocked-input test or a shared descendant-output test in
  preflight (5s) rather than review (6s).
- Observed: the latest failed blocked-input fixture at commit `34d8e977` was
  already native shell. Its retained temporary script used `/bin/sh`, a bounded
  `dd` read and the correct model-usage JSON. The review-start marker was absent.
- Source fact: `external_review._launch` starts its monotonic deadline after
  `Popen`, then starts output readers and an input-writer thread. The writer
  closes stdin for this non-JSON-RPC execution. Probe and review are separate
  real CLI processes.
- Unresolved: absence of the review marker cannot distinguish failure to start
  the shell, a delayed `dd`/input read, or a later preflight step. It does not
  prove interpreter startup is the sole cause. Withdraw that sole-cause
  interpretation; native shell has not yet established complete repair.
- Observed diagnostic result: the isolated instrumented code-group invocation
  exited 0, with 2833 passed and 2 skipped in 222.19s. It did not reproduce the
  failure and therefore does not settle which preflight step sometimes stalls.

## Evidence

- Actual failure: `/private/tmp/design-research-build-suite-r3.log`, exit 1;
  `test_unreadPromptOverPipeBuffer_timesOutAtLimit`, expected 6s, observed 5s;
  1 failed, 2832 passed, 2 skipped in 204.81s.
- Failed fixture inspected at
  `/private/var/folders/pv/m7y9m2v56lg68nl8wtxkbm0c0000gn/T/pytest-of-kouko/pytest-3792/popen-gw6/test_unreadPromptOverPipeBuffe0/bin/claude`;
  the sibling `review-started` file was absent. Its printf format contains one
  backslash, so the actual acknowledgement uses a newline, not a literal escape.
- Source: [external_review.py](../../../../loom-code/scripts/external_review.py),
  `_launch`, `_run`, `execute`;
  [run_package_tests.py](../../../../scripts/run_package_tests.py),
  `loom_family_commands` fixes the code group to
  `-n auto`. `/bin/dd` and `/bin/cat` are the observed host utilities.
- Diagnostic clone: `/private/tmp/loom-preflight-phase-diagnostic`, extracted
  from the actual committed branch without uncommitted implementation changes.
  Only the blocked-input fixture adds shell-start, completed-read and
  acknowledgement marker files plus failure output containing those markers.
  The source worktree is unchanged by this instrumentation.
- Diagnostic command:
  `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family --only code -q`.
  Output: `/private/tmp/design-preflight-phase-diagnostic.log`; exit 0,
  `2833 passed, 2 skipped in 222.19s`.
- A shell-scripted instrumentation edit was blocked by the command guard before
  execution; the same non-executable file edit was made through apply_patch.
  No guard setting or allowlist was changed.

## Decision impact

Do not apply another language/startup fix solely from the previous hypothesis.
The native rewrites have no demonstrated reliability advantage and add fixture
complexity beyond the requested research change. Withdraw those incidental
rewrites, restore the two exact original test files, and preserve all deadlines,
assertions and failure history. This does not resolve the pre-existing timing
uncertainty or authorize skipping checks. The minimal candidate must still pass
the complete suite, independent terminal review and finalization. Existing
design-trial evidence remains applicable.

## Limitations and open questions

The added file writes perturb timing slightly. This is a local parallel-code
workload, not a universal scheduler benchmark. Earlier failures lack these
phase markers and cannot be reconstructed. The diagnostic passed without
capturing the intermittent failure; the exact cause and a reliable repair
remain unknown. A passing future verification is an observed run, not proof
that this pre-existing timing issue was fixed by the research change.
