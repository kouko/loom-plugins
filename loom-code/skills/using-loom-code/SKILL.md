---
name: using-loom-code
description: |
  Route general Loom implementation requests to the right station. Use when asked to use Loom for a change without naming a station.
user-invocable: true
---

# Using Loom Code

Select the station matching the request and existing artifacts, then read and
follow its linked SKILL.md. A directly named station goes straight to that skill.

| Request or current state | Load |
|---|---|
| Plan or start a change; no implementation plan yet, including an absent or unconfirmed intent | [write-plan](../write-plan/SKILL.md) |
| Implement a committed plan with a confirmed intent | [build](../build/SKILL.md) |
| Build completed, or functional changes invalidated review evidence | [closing-review](../closing-review/SKILL.md) |
| Publish a branch, normally one with a matching review attestation | [ship](../ship/SKILL.md) |
| Alert, CI or regression failure, or dogfood incident outside an active unmerged change, arriving without a user's request to fix a bug | [maintain](../maintain/SKILL.md) |
| Run one consented outside review for an owning Loom review skill | [external-review](../external-review/SKILL.md) |

The default is the full flow: skip a step only when the user tells you to in
plain words, then tell the user in one line which step is skipped and continue.

The selected station owns prerequisites, execution, and handoffs. Requests only
for product design or workflow tools belong to their available skills, not this
implementation router.
