# decision-map

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-workflow](../../README.md) / decision-map

Keep a long-running outcome and its unresolved questions explicit across sessions and several delivered changes.

## When to use

Use this when the whole route to an outcome cannot yet be listed. If all work is already known and there is no genuine uncertainty, start one intent and plan instead.

## What you get

A persistent `docs/loom/maps/<map-id>/MAP.md` and `tickets/` store. Tickets close a decision through discussion, answer a factual question through research, or test a direction through a prototype. A ready delivery slice creates an intent linked to the map.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:decision-map to chart a map for reducing onboarding abandonment.
Use loom-workflow:decision-map to resume the onboarding map and identify the next unblocked ticket.
```

## Boundaries

- The map requires your ratification before activation. It tracks outcome knowledge; intents, plans, Git and PRs own delivery progress.
- Charting and working tickets use loom-workflow alone. Starting a delivery requires loom-code, then hands off to capture-intent when available or write-plan otherwise.
- One completed ticket or merged PR does not complete the map: all destination acceptance conditions need evidence, uncertainty must be resolved and all tickets must be closed or withdrawn.
- Completed and archived maps remain immutable history; renewed work uses a successor.

## Further reading

- [Map format and operations](references/map-format.md)
- [Prototype boundaries](references/prototype-contract.md)

## Related skills

- [loom-design:capture-intent](https://github.com/kouko/loom-plugins/blob/main/loom-design/skills/capture-intent/README.md)
- [loom-code:write-plan](https://github.com/kouko/loom-plugins/blob/main/loom-code/skills/write-plan/README.md)
- [loom-workflow:handoff](../handoff/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
