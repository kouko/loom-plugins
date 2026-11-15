---
title: "Planning intake JSON: reuse the bounded comparison"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags:
  - loom/research
---

# Planning intake JSON: reuse the bounded comparison

## Question and scope

Should Loom add JSON planning intake to reduce orchestration overhead? The sufficient evidence conditions are (1) an applicable comparison of JSON against the smaller guided-text alternative, (2) evidence of incremental benefit and costs, and (3) current implementation applicability. Scope is offline inspection at checkout `4d44cd3ce2889c552d46ca4687596bc4f5298a17`; no models, services or checker executions were rerun.

## Method and rationale

Reuse the existing controlled comparison and its witnessed acceptance record, with a lightweight qualitative comparison of current behavior and guided text. Inspect the connected CLI → intake → renderer path to check applicability. Existing records answer the historical bounded choice; new benchmarking would exceed authorization and is unnecessary to restate that result. No external search or language expansion is needed for this local evidence question.

## Findings

1. **The recorded comparison does not justify adding JSON for overhead reduction.** One sequential consumer saw equivalent guided-text and JSON decisions across six cases (five real CLI cases plus one synthetic partial-output crash control). JSON packet size was 2,681 bytes versus guided text 2,236: **445 additional bytes**, recomputed by subtraction. The original adoption condition therefore selected guidance-only. This is historical reported evidence inspected here, not a new performance measurement. [Comparison](../../../../2026-11-11-intake-observation-pilot/evidence/comparison.md#final-adoption-and-continuity), [witnessed consumption](../../../../2026-11-11-intake-observation-pilot/evidence/acceptance-test-evidence.md#3-actual-consumption-costs-and-adoption-decision).
2. **General efficiency remains unresolved.** No model-token count, parent-model turn count, monetary cost or end-to-end model latency was supplied. Sequential order text → guidance → JSON allows learning effects; the injected crash is not a measured checker failure. Byte differences cannot establish token/cost/latency differences. The recorded final acceptance corrects crash completeness to unknown. [Experiment boundary](../../../../2026-11-11-intake-observation-pilot/evidence/comparison.md#experiment-boundary), [final acceptance](../../../../2026-11-11-intake-observation-pilot/evidence/acceptance-test-evidence.md#1-faithful-observations--re-tested).
3. **Current source differs materially from the historical guidance-only conclusion.** At the inspected HEAD, the CLI already recognizes trailing `--json` for intake, creates a result, removes the selector, invokes the intake handler with that result and serializes it. The handler returns early on failed confirmation and otherwise accumulates applicable checks; `report_result` emits status/diagnostics into the supplied object. Thus “add JSON” is no longer the literal current implementation choice, and the historical statement that the JSON interface was removed is not a current-tree inventory. [CLI `main`, lines 576–621](../../../../../../loom-code/scripts/loom_checker.py#L576), [handler `cmd_intake`, lines 28–48 and final return](../../../../../../loom-code/scripts/loom_checker/command_handlers/intake.py#L28), [renderer `report_result`](../../../../../../loom-code/scripts/loom_checker/preparation_output.py#L23). This is source-path verification, not runtime/deployment verification.
4. Existing planning guidance still explains exit codes, confirmation early exit, crash uncertainty and rerun boundaries. These provide the smaller interpretation aid without a new format requirement. The historical comparison supports that alternative under its original conditions. [Planning guidance, lines 238–255](../../../../../../loom-code/skills/write-plan/SKILL.md#L238).

## Evidence

Starting records were inspected in full: [RDM assessment](../../../2026-11-11-recursive-decision-models-for-loom.md) and [input-evidence assessment](../../../2026-11-11-mechanical-decision-input-evidence.md). Their initial source revision was `91ee3610`, JSON candidate `26f3049d` repaired at `7da5d59`; the independent final guidance re-test records `ede4db79`. These are historical conditions, distinct from this checkout.

The comparison and acceptance report were read, including the final re-test. Their reported test counts and historical observations are not claimed as runs performed here. The current CLI source, intake handler, preparation renderer, text report helper and focused planning guidance were inspected. `git rev-parse HEAD` returned the revision above. `rg` against a guessed `loom_checker/cli.py` path failed because it does not exist; locating the actual `loom_checker.py` entry point resolved this inspection gap. No full suite or installations ran.

## Decision impact

Do **not** claim that adding JSON reduces overhead on this evidence. The smaller guided-text alternative met the same bounded decision-consumption outcome and avoided the historical candidate’s extra maintenance surface. Original candidate costs included 42 net handler lines plus format/help/tests and a duplicate-option repair; these are historical sunk costs, not current marginal costs or measured operational savings.

Keep the current implementation decision separate: JSON already exists in this tree. The old comparison alone neither justifies a new interface addition nor authorizes removing today’s shared JSON pathway, which may serve additional callers. Retaining current behavior avoids an unassessed compatibility change; guided text remains the supported smaller choice for the original use case. If a current consumer requires machine-readable fields, or representative matched measurements demonstrate a benefit unavailable through guidance, re-evaluate that concrete use case. Neither requirement nor benefit is established here.

## Limitations and open questions

The existing six-case comparison is sufficient for its original conditional no-benefit choice, not universal format equivalence. No representative task corpus, multiple independent consumers or causal performance estimate was obtained. This run did not inspect the full raw packet/scoring inventory or reconstruct historical executions; numerical outcomes are attributed to the inspected retained reports. Current JSON runtime correctness, all callers, installed-host behavior and the reason it was reintroduced remain unverified. Those gaps prevent concluding that current JSON should be removed; they do not supply missing evidence for overhead savings.
