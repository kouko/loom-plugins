---
title: "Should Loom prioritize CLI consistency or recovery?"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
change: 2026-11-14-consume-readonly-json
tags:
  - loom/research
---

# Should Loom prioritize CLI consistency or recovery?

## Question and scope

Choose the current emphasis for the open sixteen-command rollout, without
changing its intent, proposal or implementation. Inspected source baseline:
`6fe61c99ea1981f238f8a8550abbd1e36e93cfab`, loom-code 3.76.0. Preserve existing
text/JSON behavior, authorization, host protocols and worktrees. The user wants
usable agent interfaces and continued work when Loom faults; neither requirement
authorizes bypassing a failed check or an ambiguous write.

## Method and rationale

Lightweight trade study supported by targeted source/test inspection. Compare
directly evidenced gaps, effect on the currently requested outcome, implementation
scope and maintenance exposure. Reuse applicable official guidance from the
preceding discussion; it informs trade-offs but cannot rank this project's
actual incidents. No numeric scores, incident-rate estimates or speed claims.
No private conversation-history census, new experiment or full suite is needed
to establish the inspected consumer gap. Tests read here establish designed
coverage, not a fresh passing execution.

## Findings

Observed: the write-plan station still invokes contract in text mode, and
closing-review still invokes reviewer-count in text mode. Their producer
already supports typed JSON. The existing result helper supports bounded
output/error rendering, but does not itself validate consumer observations.
This is a concrete remaining integration task, not proof that agents currently
misinterpret the output at a measured rate.

Observed: recovery is not absent. Land has a path that inspects merge state
after a failed merge response. Existing tests distinguish an OPEN result from
a later MERGED result. Publish documents one bounded retry for remote head
visibility lag. Existing JSON entry tests cover late data/stream cleanup.
These are scoped mechanisms, not complete arbitrary-fault recovery.

Unknown: the current frequency and cost of real Loom-caused task interruption,
the proportion caused by interface ambiguity, and the benefit of broad text
fallback or a generic retry layer. Absence of these measurements is not evidence
that faults are rare or harmless.

Inference: prioritize consistency and real adoption of the existing JSON
contracts, including essential failure semantics. Preserve existing recovery
and address demonstrated severe defects immediately. Broad automatic recovery
does not presently have evidence sufficient to displace that smaller primary
workstream. Safe recovery also needs reliable distinctions between rejection,
internal failure and uncertain operation completion.

## Evidence

- Source inspection: [write-plan](../../../../loom-code/skills/write-plan/SKILL.md),
  Step 0, invokes `contract --require 2.1` without JSON; its instructions already
  distinguish contract incompatibility from launcher failure.
- Source inspection: [closing-review](../../../../loom-code/skills/closing-review/SKILL.md),
  reviewer-depth step, invokes text reviewer-count and requires actual independent
  reviews; the number does not authorize skipping them.
- Source inspection: [result renderer](../../../../loom-code/scripts/loom_checker/preparation_output.py),
  new_result/report_result/error_result/write_result, and the selected JSON path
  in [main](../../../../loom-code/scripts/loom_checker.py), establish existing
  producer support and error cleanup.
- Source and test inspection: [land](../../../../loom-code/scripts/loom_checker/command_handlers/land.py),
  merge outcome verification, and [merge tests](../../../../loom-code/tests/test_land_merge.py),
  test_merge_timeout_still_open_blocks and
  test_merge_nonzero_but_reread_merged_continues_to_verify, distinguish uncertain
  responses from observed completion. No test was rerun in this assessment.
- Source inspection: [publish](../../../../loom-code/scripts/loom_checker/command_handlers/publish.py),
  existing PR identity comparison, limits the documented visibility-lag retry.
- Test inspection: [JSON entry tests](../../../../loom-code/tests/test_preparation_json.py)
  cover typed results, baseline parity, invalid selectors, repository errors and
  late partial-output failures. They do not establish consumer-side recovery
  or production incident frequency.
- Official MCP output-schema guidance:
  https://modelcontextprotocol.io/specification/2025-11-25/server/tools#output-schema
  supports declared output contracts and client validation; it does not mandate
  a Loom CLI design or prove effectiveness in this repository.
- Amazon engineering experience:
  https://aws.amazon.com/builders-library/avoiding-fallback-in-distributed-systems/
  warns that infrequently used fallback paths can be difficult to test and
  that improving the primary path can be a better investment. This is a
  reported engineering practice, not a universal ban on CLI fallback.

## Decision impact

### KEEP

- Interface consistency plus real consumers: GROUNDED / ESSENTIAL. Define the
  whole inventory and completion/error meanings, then adopt existing typed
  results in the two actual consumers with deterministic checks where needed.
- Essential failure boundaries and existing recovery: GROUNDED / ESSENTIAL.
  Preserve diagnostics and work, never convert rejection or unknown completion
  into success, and retain effect-specific outcome reconciliation.

### DEFER

- New automatic text fallback or generalized retries: recovery mechanisms are
  plausible, but their broad scope is not currently shown necessary. Re-trigger
  on a reproducible relevant incident that the smaller interface work and
  existing recovery cannot resolve, with an attributable cause and a testable
  alternative. A severe safety/data-loss/duplicate-write defect takes priority
  immediately; repeated incidents are not required to fix a severe defect.

### DROP

- Blanket guarantees that arbitrary Loom defects never interrupt progress, or
  a universal recovery engine introduced without concrete consumers and failure
  evidence. These add unbounded obligations without a checkable benefit.

This prioritization combines consistency with a small reliability baseline;
it does not postpone all failure handling. Keeping everything unchanged is
cheaper now but leaves the confirmed consumer gap. A recovery-first project is
credible when incident evidence shows that blocking faults dominate current
work, which this bounded inspection has not established.

If adopted, revise the [rollout proposal](../rollout-proposal.md) before
implementation: automatic text fallback should be conditional, not a required
feature of the first batch. This assessment itself makes no such edit and
does not confirm the open intent or authorize publication.

## Limitations and open questions

No fresh runtime tests, host reload checks, fault injection, timing benchmark,
incident-log sample, cost estimate or outside-model review was performed.
The recommendation is a bounded qualitative judgment. Revisit when actual
dogfood shows frequent blocking faults, a supported host regresses, or an
ambiguous write can cause duplicate effects or lost work. Do not substitute
passing mechanical tests for that operational evidence.
