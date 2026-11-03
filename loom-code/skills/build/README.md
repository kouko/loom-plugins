# build

[Loom](../../../README.md) / [loom-code](../../README.md) / build

Implement an agreed change and test the resulting behavior before closing review.

## When to use

Use this when a confirmed intent and committed plan are ready, or when closing review returns findings that require a functional fix. Explicitly omitted steps are recorded and do not silently waive the remaining checks.

## What you get

Commits on the change branch, focused test results, integration results, and an end-of-Build handoff with the complete package-suite result and adversarial-program results or a reason no program was written.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-code:build to implement the committed plan for 2026-11-03-export-history.
Return this review finding to loom-code:build and fix every matching instance within the change.
```

## Boundaries

- Behavior changes follow a failing-test, implementation, passing-test cycle unless the user has explicitly instructed a supported skip.
- Implementers write the change; a separate adversary tries to break it. Closing reviewers do not review their own implementation.
- Build never creates or edits the review attestation. Required failing checks are resolved before handoff to closing-review.

## Related skills

- [loom-code:write-plan](../write-plan/README.md)
- [loom-code:closing-review](../closing-review/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
