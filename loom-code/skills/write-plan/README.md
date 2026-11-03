# write-plan

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-code](../../README.md) / write-plan

Turn a confirmed change request into an implementation plan with bounded tasks, tests and risks.

## When to use

Use this after the intent is confirmed and any required design is ready. With loom-code installed alone, this is also the entry for a new feature or bug-fix request: it captures and confirms the intent first.

## What you get

A committed `docs/loom/<change-id>/plan.md` names the files, acceptance conditions, positive and negative or boundary tests, dependencies and risks for each task. A fresh reviewer checks the plan before implementation.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-code:write-plan for the confirmed intent 2026-11-03-export-history.
Use loom-code:write-plan to plan this bug fix; loom-design is not installed.
```

## Boundaries

- The agent decides task splitting and implementation details; you confirm the wanted outcome rather than grade the plan.
- Without loom-design, this skill handles intent confirmation and a minimal spec when needed. It does not silently skip those prerequisites.
- Planning does not implement the change. Ready work is handed to build on the change branch.

## Further reading

- [Plan template](../../contract/templates/plan.md)

## Related skills

- [loom-design:capture-intent](https://github.com/kouko/loom-plugins/blob/main/loom-design/skills/capture-intent/README.md)
- [loom-design:write-spec](https://github.com/kouko/loom-plugins/blob/main/loom-design/skills/write-spec/README.md)
- [loom-code:build](../build/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
