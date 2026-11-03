# architecture-design

[Loom](../../../README.md) / [loom-design](../../README.md) / architecture-design

Agree on repository structure and dependency rules, with executable checks for the rules that can be tested.

## When to use

Use this on request to design a project’s architecture or revisit an affected part of its current architecture. Existing settled choices are not reopened without a reason.

## What you get

A ratified root `ARCHITECTURE.md` covering module boundaries, technology choices, file layout and CI stages, plus guard tests integrated into the project’s normal suite where rules are mechanically checkable.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-design:architecture-design to define module boundaries for this project.
Use loom-design:architecture-design to revisit only the dependency rules affected by this change.
```

## Boundaries

- Options and their trade-offs are discussed with you. Drafts and guards stay in a temporary copy until validation and ratification.
- Changes to a decision, its rule and its guard are installed together; active guards are not silently changed while a redesign is still a draft.
- Data models and API interfaces belong in change specs. Missing ARCHITECTURE.md never blocks a change.

## Further reading

- [Architecture document format](references/architecture-md-schema.md)

## Related skills

- [loom-design:product-principles](../product-principles/README.md)
- [loom-code:write-plan](../../../loom-code/skills/write-plan/README.md)
- [loom-workflow:loom-interactive-diagram](../../../loom-workflow/skills/loom-interactive-diagram/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
