# maintain

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-code](../../README.md) / maintain

Turn an incident into a reproducible, scoped change request without duplicating existing work.

## When to use

Use this for an alert, CI or regression failure, or dogfood incident outside an active unmerged change when it arrives without a user’s request to fix a bug.

## What you get

Evidence attached to a matching open intent, or a new `docs/loom/intent/<change-id>.md` marked `originator: maintenance-loop`, followed by handoff of the confirmed intent to write-plan.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-code:maintain to investigate this regression alert and find its matching intent.
```

## Boundaries

- A user asking for a bug fix starts at capture-intent, or write-plan without loom-design.
- CI failures in an active unmerged change stay with that change and its publication flow.
- Reuse an existing reproducing test when possible. Incident intake does not create review rounds or publication evidence.

## Related skills

- [loom-design:capture-intent](https://github.com/kouko/loom-plugins/blob/main/loom-design/skills/capture-intent/README.md)
- [loom-code:write-plan](../write-plan/README.md)
- [loom-code:ship](../ship/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
