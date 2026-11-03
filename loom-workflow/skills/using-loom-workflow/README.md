# using-loom-workflow

[Loom](../../../README.md) / [loom-workflow](../../README.md) / using-loom-workflow

Select a workflow tool from what you want to do without requiring you to memorize the toolbox.

## When to use

Use this when a request spans workflow tools or you are unsure which one fits. Each named tool remains directly invocable.

## What you get

A handoff to the selected tool, which retains its own procedure, permissions and output. It can route memory, critique, retrospective, handoff, second-opinion and visualization requests.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:using-loom-workflow to help me save state for the next session.
Use loom-workflow:using-loom-workflow to choose the right tool for this retrospective.
```

## Boundaries

- It does not implement the intent, spec, plan, build, review or publication stations.
- goal-create is selected only when explicitly named; an inferred need for a goal does not invoke it.
- A new critique lens belongs to critique; a different executor belongs to independent-advisor. A one-session recap differs from a retrospective or cross-session handoff.

## Related skills

- [loom-workflow:critique](../critique/README.md)
- [loom-workflow:handoff](../handoff/README.md)
- [loom-workflow:project-retro](../project-retro/README.md)
- [loom-workflow:decision-map](../decision-map/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
