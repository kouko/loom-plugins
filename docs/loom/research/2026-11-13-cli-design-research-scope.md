---
title: "Should Loom research CLI and agent-operated CLI guidance before defining a common result contract?"
type: loom-research
status: concluded
created: 2026-11-13
updated: 2026-11-13
tags:
  - loom/research
---

# Research before the common CLI result contract

## Question and scope

Assess whether a bounded investigation should precede the unconfirmed
[common-result intent](../intent/2026-11-13-cli-result-contract.md).
Current installed code is 3.72.0; the completed optional JSON pilot covers
plan/intake and preserves delivery's separate existing format. This record
decides research value and scope, not the final contract or implementation.

## Method and rationale

Lightweight trade study: compare immediate implementation, bounded research
combined with local inventory, and a broad standalone survey. Criteria are
decision impact, compatibility risk and avoidable implementation burden.
Read applicable first-party guidance and project-authored documentation;
reuse the pilot's actual comparison. English/Japanese exploratory searches
were used to locate leads. Stop once there is enough support to decide whether
research is worthwhile; implementation verification belongs to the subsequent
bounded study, not this scoping assessment.

## Findings

- Research first is justified because several unresolved choices affect a
  published contract: discovery, representation selection, errors versus
  exit codes, progress versus final results, partial writes and retry safety,
  and schema evolution. Merely adding the same flag cannot settle these.
- Existing guidance offers useful constraints but not a single universal
  agent-CLI standard. Traditional human-oriented guidance and agent-oriented
  project proposals have different priorities; product examples are not
  representative prevalence evidence or proof of LLM performance benefits.
- A smaller investigation combined with the sixteen-command local inventory
  can answer these questions without building a universal output framework.
  Research need not require repeating the completed format experiment.

## Evidence

1. [Command Line Interface Guidelines](https://clig.dev/), inspected
   2026-11-13: practitioner-authored guidance on help, stdout/stderr, exit
   codes, explicit JSON output, noninteractive operation and compatibility.
   Its human-first framing is explicit. This is guidance, not a formal
   certification standard or agent performance experiment.
2. [GitHub CLI exit codes](https://cli.github.com/manual/gh_help_exit-codes),
   official documentation inspected 2026-11-13: success 0, failure 1,
   cancellation 2, authentication 4; commands may have additional meanings.
   This demonstrates why adopting another CLI's code numbers blindly would
   conflict with Loom's current meanings. No gh implementation was audited.
3. [AWS CLI output formats](https://docs.aws.amazon.com/cli/latest/userguide/cli-usage-output-format.html),
   official documentation inspected 2026-11-13: multiple output formats and
   selectors, JSON default, and different query/pagination behavior depending
   on format. Formatting can affect operational semantics and requires
   explicit investigation. No AWS runtime was exercised.
4. [googleworkspace/cli README](https://raw.githubusercontent.com/googleworkspace/cli/main/README.md),
   project-authored documentation inspected 2026-11-13: describes human/agent
   use, schema discovery, structured responses and dry-run; explicitly states
   it is not an officially supported Google product and expects breaking
   changes. These are documented examples, not source/runtime verification
   or an industry-wide rule. The moving main revision was not pinned here.
5. [Agent-First CLI about](https://agentfirstcli.github.io/about/), inspected
   2026-11-13: a named-maintainer community proposal, useful as a hypothesis
   source, not an established consensus or independently validated standard.
6. [Loom pilot comparison](../2026-11-12-cli-json-pilot/evidence/comparison-r2-results.md):
   retained actual small-sample comparison, each mode 31 task tool calls,
   20 checks and 8 corrections; JSON check bytes 4,446 versus text 3,074.
   No observed operation-efficiency benefit; informed operators and capture
   repair limit inference. This local evidence argues against assuming that
   universal JSON adoption itself improves agent outcomes.

## Decision impact

Recommend bounded research before ratifying the result contract. Combine it
with the existing proposed local inventory rather than create a separate
unbounded standards project. Study discovery/help and naming, input and
noninteractive behavior, results/errors/streams, lifecycle/recovery safety,
and versioning/testing. For every recommended rule, retain source strength,
Loom applicability, compatibility cost, exceptions and a concrete validation
scenario. Return adopt/adapt/defer/reject decisions and the smallest first
implementation batch. Keep all existing text/JSON contracts compatible.

Immediate implementation has lower initial cost but risks publishing a
premature cross-command contract. A broad literature survey adds cost without
an identified decision benefit. No new framework, MCP migration, launcher
rename, provider call, installation or external publication is authorized by
this assessment. The intent remains open; no implementation proceeds here.

## Limitations and open questions

This is a decision to investigate, not a completed comparative design study.
Agent-oriented proposals are emerging and lack demonstrated universal
benefits. No upstream source paths were traced or products installed; claims
above are documentation-only. A follow-up should inspect selected source
paths or run small permitted probes only where documented behavior would
change Loom's contract. No messages or project artifacts were sent to vendors.
