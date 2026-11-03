# write-spec

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-design](../../README.md) / write-spec

Describe what a confirmed change must do and what users will see before implementation is planned.

## When to use

Use this for a requested specification, or a confirmed intent marked `needs-design: yes` that has no spec yet.

## What you get

A committed `docs/loom/<change-id>/spec.md` with requirements mapped to acceptance conditions, design decisions, alternatives, current-state evidence and interface flows where applicable.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-design:write-spec for the confirmed export-history intent.
```

## Boundaries

- For a product change, you confirm visible behavior and applicable irreversible consequences. Engineering changes do not stop for this behavior confirmation.
- The agent decides technical design from evidence and records why; it does not ask you to judge the spec’s quality.
- High-risk specs receive an independent pre-build review. Routine specs go directly to loom-code:write-plan.
- This station neither plans tasks nor implements the change.

## Further reading

- [Spec template](templates/spec-minimal.md)
- [Interface-flow requirements](references/ui-flows.md)

## Related skills

- [loom-design:capture-intent](../capture-intent/README.md)
- [loom-code:write-plan](https://github.com/kouko/loom-plugins/blob/main/loom-code/skills/write-plan/README.md)
- [loom-design:design-system](../design-system/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
