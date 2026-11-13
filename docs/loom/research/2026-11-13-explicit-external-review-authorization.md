---
title: Explicit external review requests and duplicate confirmation
type: loom-research
status: concluded
created: 2026-11-13
updated: 2026-11-13
tags:
  - loom/research
---

# Explicit external review requests and duplicate confirmation

## Question and scope

Does a named outside-agent review request require another data-transfer confirmation, and what should change? Inspected baseline fbdc29af3, loom-code 3.72.0 and loom-workflow 5.21.0, and relevant Codex installed files. This source-level record contains no session excerpts. Detailed local history assessment remains outside the publication packet.

## Method and rationale

Trace caller contracts and runner authorization checks, compare installed copies, and inspect focused tests. Local artifacts answer the implementation question without sending project data to a search service. Assess interruption, scope control and implementation cost; do not redesign an authorization schema that already accepts direct requests.

## Findings and evidence

- The [external-review contract](../../../loom-code/skills/external-review/SKILL.md#before-discovery) accepts a named direct request with an unambiguous target for one bounded review. Cost, vendor transfer and local-access facts must be shown; the disclosure is not another acknowledgment.
- Both [independent-advisor](../../../loom-workflow/skills/independent-advisor/SKILL.md#authorization-and-the-single-checkpoint) and [closing-review](../../../loom-code/skills/closing-review/SKILL.md) already carried the no-second-confirmation rule at baseline, but did not explicitly require same-turn continuation after disclosure.
- The [runner](../../../loom-code/scripts/external_review.py) validates quoted direct requests or accepted selections, executor/target binding and selection bounds. It contains no interactive yes/no prompt. Its consent record does not grant separate host execution approval.
- The runner supports codex, claude and agy. OpenCode as the caller host is distinct from adding OpenCode as a reviewer executor.
- Relevant installed Codex copies matched the checkout at inspection. This establishes file parity, not active-session routing or other hosts' state.
- Baseline focused tests (`test_external_review.py` and `test_external_review_adversarial.py`) passed with host Python: 144 tests in 43.28s. Locked isolated invocation could not fetch dependencies because DNS failed. Passing these tests does not establish uninterrupted host behavior.

## Decision impact

Preserve the authorization schema and bounded disclosure. Correct caller continuation instructions and test actual behavior, including optional context that can unnecessarily hold artifact reviews. Carry the original request, target, destination and minimized packet scope into an existing host execution request. Do not claim internal consent overrides the host, suppress a host decision or bypass a refusal.

Removing all consent checks adds scope-control regressions and does not establish host approval. Adding an executor is separate feature work. The active repair is defined by the confirmed [intent](../intent/2026-11-13-uninterrupted-external-review.md), not by a promise that every future host will approve.

## Limitations

File inspection and prose pins cannot prove same-turn execution or an external review result. A real call with explicitly approved test scope cannot prove that all future terse requests pass host approval. Report that distinction in acceptance evidence. No global approval configuration is changed.
