# design-system

[Loom](../../../README.md) / [loom-design](../../README.md) / design-system

Agree on a product’s visual rules so later interfaces use consistent colors, type and components.

## When to use

Use this for a product with a UI when you want a visual system, before or during specification. Existing principles constrain the proposed visual direction.

## What you get

A root `DESIGN.md` with visual direction, palette, typography, spacing, shape and component tokens. The agent validates its structure and contrast before presenting it for your confirmation.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-design:design-system to define a compact, accessible visual system for this dashboard.
```

## Boundaries

- This document governs visual tokens, not navigation, screens or interaction flows; those belong in a change’s spec.
- An absent or unratified DESIGN.md never blocks a change.
- The ratification line is written only after you confirm the visual direction.

## Further reading

- [Visual-system document format](references/design-md-schema.md)

## Related skills

- [loom-design:product-principles](../product-principles/README.md)
- [loom-design:write-spec](../write-spec/README.md)
- [loom-design:architecture-design](../architecture-design/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
