---
title: "Exact package runner TEST_ROOTS"
type: loom-research
status: concluded
created: 2026-11-08
updated: 2026-11-08
tags:
  - loom/research
---

# Exact package runner TEST_ROOTS

## Question and scope

Which directories does the supplied package runner's `TEST_ROOTS` contain? Scope: the source snapshot attributed by [provenance](../../../provenance.json) to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; no active change.

## Method and rationale

Direct source inspection answers this constant-value question. Read the declaration and its consumers; check the runner's SHA256 against provenance. No experiments or tests were run.

## Findings

`TEST_ROOTS` contains exactly these four repository-relative directories, in order:

1. `tests`
2. `loom-code/tests`
3. `loom-design/tests`
4. `loom-workflow/tests`

## Evidence

Source evidence: [run_package_tests.py](../../../src/scripts/run_package_tests.py), line 53, declares `TEST_ROOTS = ("tests", "loom-code/tests", "loom-design/tests", "loom-workflow/tests")`. The consumers at lines 92 and 125–126 resolve entries relative to `repo` and select the code group's roots, respectively; they do not change this declaration.

Local integrity check: `shasum -a 256 src/scripts/run_package_tests.py` returned `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54`, matching provenance.

## Decision impact

The requested directory list is settled for this snapshot. No runner or plugin changes are proposed.

## Limitations and open questions

No uncertainty remains about the supplied declaration. This minimal snapshot does not establish a full checkout, actual test execution, deployment, CI results, or the state of another revision.
