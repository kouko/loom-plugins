# capture-intent

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-design](../../README.md) / capture-intent

Confirm the problem to solve and the observable conditions that will prove the change worked.

## When to use

Use this before implementing a new software feature or bug fix, even when Loom was not named or the project has no Loom store. Requests inside an active change continue in that change’s current station.

## What you get

A `docs/loom/intent/<change-id>.md` covering the problem, proposed outcome, acceptance conditions, constraints, exclusions and open questions. It records your confirmation and whether the change needs a design spec.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-design:capture-intent for a feature that lets users export their saved searches.
Use loom-design:capture-intent for this bug: saved filters disappear after restart.
```

## Boundaries

- You confirm the outcome in plain words; this station does not ask you to choose implementation details or grade document quality.
- Missing product principles and applicable hard-to-reverse choices are handled within the intent conversation.
- A confirmed intent goes to write-spec when design is needed, otherwise to loom-code:write-plan.
- Non-software work and behavior-preserving typos or renames go directly unless you explicitly ask for Loom.

## Further reading

- [Intent template](templates/intent.md)
- [Interview guidance](references/interview.md)

## Related skills

- [loom-design:write-spec](../write-spec/README.md)
- [loom-design:product-principles](../product-principles/README.md)
- [loom-code:write-plan](https://github.com/kouko/loom-plugins/blob/main/loom-code/skills/write-plan/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
