---
name: independent-advisor
version: 0.1.0
description: |
  Route an explicitly requested outside coding-agent review of code, plan, or decision while preserving its review contract. Also get a second opinion from another model, higher effort, or vendor.
---

# Independent Advisor

Consult a **different executor** about the user's code, plan, or decision.
This changes WHO answers, not the critique lens. For a same-executor lens change,
use `loom-workflow:critique`. This skill spends money, sends material off the
machine, and may run repository setup, so those effects require approval.

For consultation comparisons, describe capability as model tier `economy` /
`standard` / `frontier` plus effort `low` / `medium` / `high`. The outside
execution record also needs the actual selected model ID and provider family.

## Explicit outside review

When the user explicitly requests an outside coding agent to review code, plan,
or decision, route that review through `loom-code:external-review` by skill
name. Keep the incumbent reviewer and its result separately attributable. The
owning review skill supplies its task packet, criteria, verdict format and
result checks; it accepts or rejects the returned verdict. The advisor does
not substitute its `explore`/`audit` comparison verdict or report template for
the owning review skill's contract. A failed or unverified outside execution
is a separately attributed failure, never a completed independent review.

Prepare the complete single checkpoint below and obtain a recorded consent
record before invoking `loom-code:external-review` for discovery, probe or
dispatch. Give that skill the consent record, authorized scope, requested
executor and review packet; it owns candidate selection, explicit model and
effort, bounded pre-review execution, CLI invocation and execution evidence.
Do not read or run a `loom-code` file from this plugin at runtime. Accept only
the named skill's JSON evidence/status and then apply the owning review skill's
checks to any review output. A changed executor, model, vendor family or
readable scope voids the consent record and requires the whole checkpoint
again. An unsolicited second-vendor notice remains a suggestion; it never
starts discovery, probe or dispatch without the user's request or consent.

For open-ended second-opinion consultations, continue with the `explore` and
`audit` modes below and their existing packet and report rules.

## Consultation mode routing

This section applies to open-ended consultations. An explicit outside review
uses the owning review skill's task type and verdict contract instead.

- `explore`: the solution space is open; run proposer, normalizer, and blind judge roles.
- `audit`: an incumbent exists; **a single leg with full context runs**, with
  **no `proposer` leg**.

Determine the mode from a verbatim, citable fact: a target-branch commit, PR
number and state, approval line, or the user's wording. Record that quotation as
`mode_basis`: **Record the verbatim fact you looked up**, then record `mode`. An implementing commit supports `audit`; an
approved brief without one supports `explore`. Never infer a stage or paraphrase
a basis. With no citable fact, ask the user which mode to run and record the
answer. **Do not synthesise a basis**. With conflicting facts, **record both facts** and **surface the conflict at the user checkpoint**. A user
override records `mode_override` as true but must **never erase the original `mode_basis`**.

No incumbent yet is valid in `explore` and **distinct from an incomplete packet**: record it as **not yet existing**, then
run a single blind proposal or state that this consultation shape does not apply.
An incumbent that exists but was not supplied is instead a missing packet section.

## Candidate selection

Use `references/executor-detection.md` for the named skill handoff and its
failure mapping. Local, non-network capability observations may inform the
checkpoint, but neither an installed binary nor credentials establish model
availability. The named skill owns selection and pre-review verification after
consent. Never present an unverified candidate as a verified capability.

The candidate set must support a genuinely independent opinion. No eligible
candidate means stop and report the failed precondition. A same-family option
requires an explicit checkpoint decision, never a silent fallback. In
`explore`, one eligible candidate cannot serve as both proposer and judge;
surface the degraded choices at the checkpoint.

## The single checkpoint

**Exactly one checkpoint exists**, after routing and any local capability observations and before
any network-backed discovery, probe, dispatch, transmission, or **any money is spent**. One ask carries
**the leg count**, **which executor runs which leg**, **the estimated cost**, and
**the egress disclosure** together, specifically:

- for consultations, `mode`, verbatim `mode_basis`, and any conflict or override;
  for explicit reviews, the owning task type and review skill;
- leg count and every executor-to-leg assignment;
- selected model, effort, provider family and readable scope for each outside
  leg, with any unknown choice resolved before recording consent;
- estimated cost per leg (`unknown, with the reason`, **never as zero and never omitted** when unknowable; a **genuinely zero** cost stays zero, not unknown); and
- the full egress and local-execution disclosure below.

Require recorded confirmation of all dimensions. **splitting** these into separate questions, dispatching **without a recorded user confirmation**, or treating a **partial answer as approval** are violations. Ask for each missing item and **never fill it with a default**. If the executor
set changes, **the prior approval is void**: repeat local observations and cost
estimation, then present the whole checkpoint again. **Never carry a previous observation or cost figure** into the changed set.

### The egress disclosure

For every leg, name **the vendor that receives material**, packet categories,
and **the file paths the executor will be authorised to read**. Approval of the
**cost only** never authorizes either data transfer
or local execution. Before accepting approval, say plainly:

1. The inspected packet is smaller than the readable scope: **`scope_boundary` is the larger of the two**. Always **enumerate what** the wider
   paths and what they cover: “I checked the text I am sending; the other model
   can additionally open files under `<paths>`.”
2. A no-hit scan may say **the packet was checked and nothing matched**; it is
   not a safety claim or wording that **carries that meaning** about the readable scope or what leaves.
3. Answering also runs **third-party code in the user's repository** on this
   machine—its **instructions, hooks, skills and MCP servers**—even if nobody
   read it first. If a pinned executor's setup is unknown, **state that it cannot be enumerated in advance**.
4. If the audit record retains **material verbatim rather than references and summaries**, **state its location at this checkpoint** and give it the **same restrictions as the dispatch packet**.

Refuse dispatch until the user acknowledges cost, egress, readable scope, and
local setup. If cancellation follows an external call, report that material was
already transmitted to the named vendor and cannot be recalled.

## External execution evidence

After complete approval, hand each selected leg to `loom-code:external-review`
using the same consent record and authorized scope. That named skill owns
candidate discovery, explicit model and effort selection, pre-review execution,
CLI-specific evidence levels and failure status. Record its JSON evidence and
never turn an unavailable, mismatched, timed-out or unverified result into a
completed leg. A materially different profile returns to the complete
checkpoint. A frontier request cannot silently downgrade.

The blind judge and proposer must differ, and both opposite-order judge runs
use identical accepted executor, model and effort settings. Each run uses a
fresh process and is verified separately.

## Three roles and blind judging

In `explore`, use three distinct roles:

- `proposer`: sees the problem, constraints, and rejected options with reasons,
  but never the incumbent;
- `normalizer`: compresses both answers into matching cards without changing either claim; and
- `blind judge`: compares the anonymized cards without origin labels.

The exact packet sections and shared-card template live in
`references/dispatch-protocol.md`; load and follow it before dispatch. **Hold the request until every required section is present**, naming each missing section
rather than filling it in. An unreadable evidence path **counts as a missing section**; never infer or silently drop it. Mark genuinely empty sections. If
the material cannot exist, the run **ends before any spending path** and retains
the partial packet.

Normalisation **compresses; it never rewrites**: it **may not change what** either
proposal claims. Reject and redraft a card that adds a source claim. When the
normalizer authored the incumbent, that is **disclosed in the report unsoftened**.

The proposer **never sees the incumbent solution** in its packet—not quoted,
summarized, or paraphrased. Any leak means **that leg is void**. Retry an empty
output with the same blind packet, incumbent-free and with **no prior challenger output**.

### Both bias controls are mandatory

- **Anonymisation** treats identity bias: remove direct origin labels and
  indirect tells such as register, length, and first person.
- **Order counterbalancing** treats position bias: judge the same pair in **two runs in opposite presentation orders**, each in a **fresh executor process** with no shared transcript, session, or
  cache, and record that isolation.

These are **two separate controls** and **either one alone is insufficient**.
Neither substitutes for the other or for the second run: **a prompt reminder is not a substitute for a second run**. **Reusing one session for both orders** invalidates the pair. Reject a pair **anonymised but judged in a single order**; one **judged in both orders with the origins visible**; one where **only the forward run carries a verdict**; or a judge learning the incumbent, which **voids every verdict from that leg**. De-anonymize **only after every scheduled swap run has a verdict**. Opposite verdicts are **recorded as inconclusive rather than averaged**.

After normalisation, if both cards make substantially the same claim, **degrade to a single leg**, skip blind judging, and disclose that result. This is available **never before normalisation**.

## The report

Load `references/report-contract.md` for field order, rejection keys, and worked
wording. The rules below remain binding wherever the report is stored.

- Lead with `divergence_points`: the **divergence points are the body** and
  agreement never opens the report. With none, write that **no divergence point was found** and allow `inconclusive` without inventing support.
- Every divergence or finding says whether it is **a factual error or a judgement call**, gives confidence and **the concrete change proposed**, and records resolution.
- The report is a **read-only record**: later adoption changes only an item's
  resolution, not verdict, findings, or actual cost. Editing the target is
  **outside this consultation's scope**.
- Mechanically check every leg; its **own claim of completion** proves nothing.
  Reject each under its own **distinguishable reason**: empty output; **a refusal**;
  **a missing template field**; output that **restates its own input**; an
  unchecked claim marked **fabrication suspect**; or no reasoning trace. A
  **missing template field is not retried blind**; only the empty-output retry
  described above is permitted.
- Put `degraded_legs` and failure attribution in the report body. If **no leg produced usable output**, deliver a failure report naming every leg's failure.
  Record unprobed tiers as having **no verification evidence**; independent
  defects are **listed separately**; report actual `leg_count` and `early_stopped`.
- `corroborated_by` names legs; their count is **not an input to `confidence`**.
  Agreement **measures the sample, not the world**. `known_weaknesses` must state that ensembling and order reversal do not
  detect a blind spot **shared by all reviewers**.
- Completeness claims **never appear in the report**, **in any language the report is written in**. Without a `coverage_disclaimer`, **delivery is refused**.
  `actual_cost` includes probes and failed/cancelled legs;
  when unknowable, write **unknown with its reason**, never zero or the estimate.
- Mark every **externally authored and untrusted** passage, including findings
  and divergences; that marking **travels with the report** to downstream agents.

## What the report may claim

Blindness concerns the **packet**, not everything the proposer could read. Before
claiming it, ask whether `scope_boundary` could contain the incumbent. If yes or
unknown, make no **unconditional blindness claim**; qualify it in place: the packet omitted the incumbent, but the
authorized paths may describe it, so the answer is not guaranteed blind. Claim
full blindness only when that boundary cannot reach incumbent material and state
the basis. Wherever this applies, **state the qualification** where blindness is claimed.

A no-hit pre-dispatch scan reports only **what the scan checked** and its
non-matches; it is **never a safety verdict**, never a claim that content was
safe or nothing sensitive left. Every report states on its own line that the
guarantee **covered the dispatch packet** and material readable within
`scope_boundary` **was not subject to it**; without this and the
coverage disclaimer, refuse delivery.

A pinned revision is only where the packet was extracted from; it is **not what was reviewed**. Never say the executor reviewed that commit, branch, or tree; it reviewed the packet. State if
the target moved after pinning.
