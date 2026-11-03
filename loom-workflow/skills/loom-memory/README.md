# loom-memory

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-workflow](../../README.md) / loom-memory

Keep reusable repository lessons in versioned files that other contributors can retrieve and verify.

## When to use

Use this to remember, recall, reconcile or retire a repository lesson, when prior experience is concretely needed, or when saving a lesson to host-managed memory requires classifying whether it also belongs in the repository.

## What you get

A bounded recall answer or a validated update to the repository memory store, normally `docs/loom/memory/`. Each concept has its own file, provenance and a generated index entry.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:loom-memory to recall lessons relevant to changing the publication hooks.
Use loom-workflow:loom-memory to reconcile this finding with the existing lesson.
```

## Boundaries

- Most observations do not qualify: open tasks, one-off test results, personal preferences and machine-specific facts are not durable repository lessons.
- Recall is on demand; the skill does not preload the whole store or run merely because a workflow reached a particular station.
- Equivalent or contradictory knowledge is reconciled with the existing entry rather than stored as a conflicting sibling.
- A broken or populated legacy store is reported for repair or explicit migration, never silently reinitialized.

## Further reading

- [Store operations](references/operations.md)
- [Concept format](references/okf-profile.md)

## Related skills

- [loom-workflow:git-memory](../git-memory/README.md)
- [loom-workflow:handoff](../handoff/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
