---
name: using-loom-code
description: |
  Route general Loom implementation or engineering research requests to the right skill. Use when asked to use Loom without naming a skill.
user-invocable: true
---

# Using Loom Code

Select the skill matching the request and existing artifacts, then read and
follow its linked SKILL.md. A directly named skill goes straight to that skill.

| Request or current state | Load |
|---|---|
| Plan or start a change; no implementation plan yet, including an absent or unconfirmed intent | [write-plan](../write-plan/SKILL.md) |
| Implement a committed plan with a confirmed intent | [build](../build/SKILL.md) |
| Build completed, or functional changes invalidated review evidence | [closing-review](../closing-review/SKILL.md) |
| Publish a branch, normally one with a matching review attestation | [ship](../ship/SKILL.md) |
| Alert, CI or regression failure, or dogfood incident outside an active unmerged change, arriving without a user's request to fix a bug | [maintain](../maintain/SKILL.md) |
| Run one consented outside review for an owning Loom review skill | [external-review](../external-review/SKILL.md) |
| Resolve a factual evidence gap that could change an engineering decision, in an existing task or standalone discussion, including a small capability/version check, or consider preserving research from a merged change | [engineering-research](../engineering-research/SKILL.md) |

For a change, the default is the full flow: skip a step only when the user tells
you to in plain words, then tell the user in one line which step is skipped and
continue.

The selected skill owns prerequisites, execution, and handoffs. Research is
optional, preserves the owning task and its authorization, and returns evidence
or uncertainty there; standalone research does not start a change. Routine
factual lookups without a consequential evidence gap need no research skill.
Requests only for product design or workflow tools belong to their available
skills, not this implementation router.
