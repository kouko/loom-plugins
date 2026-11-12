---
title: Why unchanged timeout fixtures block research-routing verification
type: loom-research
status: concluded
created: 2026-11-12
updated: 2026-11-12
change: 2026-11-12-design-code-research-routing
tags:
  - loom/research
---

# Timeout fixture startup and verification

## Question and scope

Are the repeated timeout failures caused by this change, and can an environment
adjustment preserve the existing tests without a supporting fixture repair?
The pending decision is how to complete verification without changing production
external-review behavior or weakening its timeout/cleanup checks.

Scope: candidate `1ae5c6e6` and unchanged base `70a05fd7`, macOS, the repository's
hash-locked pytest 9.1.1/xdist 3.8.0 environment, and the five failing live CLI
tests in the existing external-review test files.

## Method and rationale

Use hypothesis-driven diagnosis: compare actual failures, inspect the connected
launch/deadline/cleanup source, reproduce against the untouched base, and measure
a minimal fresh CLI launch. Separate source equivalence, observed timing and
inference. Worker-count and interpreter changes are bounded alternatives to a
test repair, not evidence that a passing retry would establish causality.

## Findings

- Root/code integration previously passed once with four workers, but another
  four-worker run failed five unchanged live timeout cases. One-worker execution
  also failed those five: 2794 passed, 5 failed, 2 skipped in 1010.76s. Lowering
  worker count is not a sufficient remedy in the observed conditions.
- The same five selected cases failed on untouched base `70a05fd7` with one
  worker, in 20.44s. Neither production source nor those tests differed from
  that base before W3. This establishes a baseline failure, not a regression
  caused by the new research instructions.
- Candidate execution without xdist workers also failed all five in 9.59s.
  An earlier isolated pair had passed in 3.90s. Preserve that contradictory
  observation: timing is condition-dependent, not a uniform failure rate.
- A fresh executable containing only a shebang and `print(1)` took 2.826s using
  locked Python 3.12.8, exit 0, output `1`. The same construction using the other
  installed interpreter, Python 3.15.2, took 2.829s, also exit 0/output `1`.
  Each is one observation, not a latency distribution. Interpreter replacement
  did not remove the observed delay.
- Source inspection shows discovery calls `_run` with patched test deadlines;
  `_launch` creates the child, starts deadline/pipe handling and kills the group
  in `finally`. `execute` validates `probe_timeout < review_timeout`. A timeout
  result alone does not prove the intended review branch or blocked write ran.

## Evidence

- [Build chronology](../evidence/build-verification.md), including the initial
  mixed integration failures and the subsequent root/code pass.
- [Timeout fixture evidence](../evidence/timeout-fixture-evidence.md): actual
  RED/GREEN commands, source path observations and negative mutation outcomes.
- Source inspected: [external review](../../../../loom-code/scripts/external_review.py),
  `_launch`, `_run`, `_codex_candidates`, `_agy_candidates`, `discover`, `execute`;
  [ordinary tests](../../../../loom-code/tests/test_external_review.py), live
  fake CLI definitions and timeout cases; [blocked-input test](../../../../loom-code/tests/test_external_review_adversarial.py).
- Raw local outputs: `/private/tmp/loom-research-build-suite-serial.log`,
  `/private/tmp/loom-research-baseline-timeouts.log`,
  `/private/tmp/loom-research-no-worker-timeouts.log`. These are local receipts;
  the retained summaries above carry the relevant results.
- Worker override applicability was checked against the installed
  `xdist.plugin.pytest_xdist_auto_num_workers` source. No repository scheduler,
  production setting or installed plugin was changed for these experiments.
- Startup experiment: create a fresh executable in a new task-owned temporary
  directory with `#!<sys.executable>` and `print(1)`, run it through
  `subprocess.run(..., timeout=10)`, and measure the complete call with
  `time.monotonic`. The 3.15 run selected the existing Homebrew interpreter via
  `UV_PYTHON`; the locked dependency versions were retained.

## Decision impact

Environment-only attempts did not restore the five tests. A narrow supporting
test-fixture repair is justified: allow startup to reach the intended branch,
keep hangs longer than the test deadlines and elapsed bounds, prove process
death, and show parent-only termination still fails descendant-cleanup checks.
Production defaults and behavior remain outside this repair. W3 in the
[plan](../plan.md) records the new verification obligation without resetting
completed research implementation tasks or changing the confirmed requirements.

The repair's focused run passed all 144 tests; a parent-only-kill mutation
failed the three descendant cases specifically with `descendant still running`.
This supports the repaired fixture checks, not a claim that the complete suite
or research behavior has already passed. Those remain separate verification.

## Limitations and open questions

The underlying system cause of fresh CLI launch delay was not isolated. The
experiment measures a complete launch, not the portion before versus after
`Popen` returns. No OS/security setting was changed, no model comparison or
industry claim is inferred, and neither six-second fixtures nor one successful
run establish reliability under arbitrary load. Preserve the actual case/branch
evidence rather than treating a longer timeout or a green exit as sufficient.
