# product-principles

[Loom](../../../README.md) / [loom-design](../../README.md) / product-principles

Write the priorities and limits that should govern a product’s future trade-offs.

## When to use

Use this when starting a product or when you want to establish what product, design and engineering decisions must respect. Intent capture can conduct the same interview when a product change lacks ratified principles.

## What you get

A root `PRINCIPLES.md` naming the audience, ordered non-negotiables, excluded work, the failure to avoid and fixed choices. Your confirmation adds the ratification line.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-design:product-principles for this offline-first personal finance app.
```

## Boundaries

- The agent does not invent principles or ratify them on your behalf.
- Principles describe the product, not one feature’s implementation plan.
- Product changes need ratified principles; engineering work is not blocked merely because no product principles exist.

## Related skills

- [loom-design:capture-intent](../capture-intent/README.md)
- [loom-design:design-system](../design-system/README.md)
- [loom-design:architecture-design](../architecture-design/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
