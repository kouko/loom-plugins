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

Which directories are explicitly listed in the package runner's `TEST_ROOTS` in the supplied source snapshot? Scope is the snapshot attributed to commit `d5a7f0da247214bdb9c61fe90c550256432e5f76`; no runner changes or plugin assessment.

## Method and rationale

Direct source inspection is sufficient for this constant-value question. Read the runner and its connected selection code, then verify its SHA256 against the supplied provenance. No experiments or tests were run.

## Findings

`TEST_ROOTS` contains exactly these four repository-relative directories, in order:

1. `tests`
2. `loom-code/tests`
3. `loom-design/tests`
4. `loom-workflow/tests`

## Evidence

Source inspection: [runner](../../../src/scripts/run_package_tests.py), line 53, defines `TEST_ROOTS = ("tests", "loom-code/tests", "loom-design/tests", "loom-workflow/tests")`. Lines 92 and 125–126 show consumers of this tuple; lines 153–170 connect family selection to the entry point.

[Provenance](../../../provenance.json) records the commit above. `shasum -a 256 src/scripts/run_package_tests.py` returned `6730a53e11d862d5d3d93eadcdafb2011b81f2595332e4a57ae49a504f660d54`, matching its recorded SHA256.

## Decision impact

The requested directory list is settled for this snapshot. No change is proposed.

## Limitations and open questions

No uncertainty remains about the tuple's contents in the inspected file. This minimal snapshot does not establish directory existence in the original repository, deployed behavior, CI results, or later revisions.
