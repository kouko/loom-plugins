---
title: "Should roadmap maintenance and planning have a dedicated skill?"
type: loom-research
status: concluded
created: 2026-11-16
updated: 2026-11-16
change: 2026-11-16-roadmap-simplification
tags:
  - loom/research
---

# Should roadmap maintenance and planning have a dedicated skill?

## Question and scope

The user now asks whether a roadmap skill should own document management and
scheduling control. Evaluate this proposal without creating a skill or changing
the confirmed intent/spec. Scheduling is ambiguous: priorities/dependencies and
dates, authorized foreground dispatch, or unattended timed/background execution.
An asynchronous clarification was requested; no answer has been received at the
time of this record. Conclusions below are conditional on that distinction.

## Method and rationale

Reuse the current branch's source and earlier source/session research. Apply a
small trade study and critique complexity lens, Design is taking apart: separate
durable program planning, next-action advice, session restart and execution.
No external-practice or scheduling-platform claims are needed. Source inspection
supports ownership boundaries, not agent compliance or comparative adoption.

Evidence conditions: identify the existing owners; compare a small single owner
against distributed guidance on the same planning outcomes; cost the new surface;
identify lost/redundant responsibilities. Do not pretend a Markdown skill can
guarantee a timed process is launched or that changing priority grants authority.

## Findings

- [whats-next](../../../../loom-workflow/skills/whats-next/SKILL.md) recommends
  the most useful next action, preserves the existing owner and authorization,
  and explicitly makes no background or every-turn trigger promise. Owning an
  entire mutable program document would broaden this responsibility.
- [handoff](../../../../loom-workflow/skills/handoff/SKILL.md) owns operational
  session continuity. Its restart artifact is not the program's enduring status
  owner. Copying plan state into handoffs creates a second maintenance surface.
- [capture-intent](../../../../loom-design/skills/capture-intent/SKILL.md)
  captures one confirmed change. Long-term multi-change reordering does not
  cleanly belong to it. It can identify/hand off a planning request rather than
  become a second program-management workflow.
- The [current spec](../spec.md) deliberately assigns contextual guidance to
  these three skills but does not name a single planning-rule owner. This is a
  concrete maintenance concern, not evidence of an observed runtime failure.
- Earlier finance session evidence demonstrates request-driven ordinary document
  creation and manual updates, not a need for a scheduler. Its recurring stage
  and decision summaries do support a program-document responsibility.

## Decision impact

| Alternative | Maintenance owner | Planning scope | Assessment |
|---|---|---|---|
| Distributed short guidance | Existing skills independently | Read/write summaries as needed | Smallest if only incidental document edits are needed |
| Shared reference owned by whats-next | One reference, existing entry points | Current goal and modest document upkeep | Smaller alternative; broad program revision changes whats-next's remit |
| Thin roadmap skill plus existing advice/delivery | Roadmap owns durable plan; callers link | Multi-goal ordering, dependencies, milestones and evidence-backed updates | Prefer if the requested planning responsibility is confirmed |
| Roadmap skill plus timed executor | Split planning/runtime required | Unattended scheduled work | Separate scope; no runtime authorization or feasibility established |
| Keep the prior spec pending observation | Existing proposed arrangement | No new capability | Valid if the user only needs occasional edits; no reason to force a new skill |

Critique Q1: the smallest end state for ongoing multi-goal planning is one short
owner of roadmap creation/review/reordering/updating, with references from existing
entry points and no new persistent store. Minimum document content stays ordinary
Markdown, not required IDs, ticket types, claim protocol, terminal immutability or
automated completion gates. Dates are user constraints or labeled forecasts,
never invented commitments. Unknown effort stays unknown.

Critique Q2: compared with the unimplemented no-new-skill spec, this adds one skill
and its own behavior evaluation. Approximate design budget, not measured output:
about 60-100 skill instruction lines, 5-15 total routing lines, and a focused
semantic evaluation set; test/evaluation volume is not yet estimable. No new
executable scheduling function is justified. The retirement of map's 37 dedicated
files / 13,460 lines is shared by both alternatives and therefore cannot justify
the incremental skill by itself. No comparative task result yet shows either
alternative is better. If replacing one skill with one skill, family counts stay
30 overall and 15 in loom-workflow; source remains unchanged now.

Critique Q3: remove duplicated planned roadmap-authoring/update instructions
from capture-intent, whats-next and handoff, replacing them with short ownership
pointers. These instructions are not yet implemented, so do not report them as
actual deleted code. Preserve whats-next's advice and handoff's restart behavior.
Map and ARC retirement remain the existing shared proposal, not extra savings.

Verdict: PROCEED-WITH-CAVEAT for a thin planning/document owner if priority and
milestone maintenance are intended. It costs an additional entry point and
evaluation surface compared with shared guidance, justified by explicit ownership;
effectiveness remains untested. Retain the smaller distributed/shared-reference
alternative for incidental editing only. Do not bundle timed/background execution.

The earlier recommendation that a dedicated skill necessarily recreates map's
complexity was too broad: a skill is an instruction entry point, while the
retired map adds a specialized data model and executable lifecycle. The new
planning scope makes the distinction consequential. This qualifies the earlier
recommendation rather than silently rewriting its evidence or approved spec.

## Limitations and open questions

- Meaning of scheduling control remains pending; do not infer background-work,
  cost, publication or automatic execution authorization from the evaluation ask.
- This is conditional design advice, not a new approved behavior or implementation.
- A changed scope would require updating/reconfirming the affected intent and
  spec and replacing the prior spec review evidence before proceeding to Build.
- No tests, installed-host trials or scheduling experiments ran. Skills cannot
  establish timed execution without an actual host/runtime and observed results.
