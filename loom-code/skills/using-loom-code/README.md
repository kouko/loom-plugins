# using-loom-code

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-code](../../README.md) / using-loom-code

Select the appropriate implementation station from the request and the work already completed.

## When to use

Use this when you want Loom to handle implementation work but are unsure which station to name. You can call any station directly instead.

## What you get

A handoff to write-plan, build, closing-review, ship, maintain or external-review. The chosen skill owns its prerequisites, execution, permissions and output.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-code:using-loom-code to continue this change from its current state.
```

## Boundaries

- The router does not replace the selected station or produce a separate plan or approval.
- Product-definition requests belong to loom-design; workflow-tool requests belong to loom-workflow.
- A directly named station goes straight to that skill. The full flow remains the default unless the user explicitly skips a supported step.

## Related skills

- [loom-code:write-plan](../write-plan/README.md)
- [loom-code:build](../build/README.md)
- [loom-code:closing-review](../closing-review/README.md)
- [loom-code:ship](../ship/README.md)
- [loom-code:maintain](../maintain/README.md)
- [loom-code:external-review](../external-review/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
