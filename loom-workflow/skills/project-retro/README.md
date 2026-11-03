# project-retro

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-workflow](../../README.md) / project-retro

Review one coding session for source-backed improvements to the project’s development environment.

## When to use

Use this when you explicitly want a retrospective of the current session or one specified session. For a recap of where the current work stands, use recap-state instead.

## What you get

A read-only report separating ranked project recommendations from possible reusable-skill issues. Each recommendation connects an observed event to a concrete target, suggested outcome, uncertainty and a verification idea.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:project-retro to review this session for project development improvements.
Use loom-workflow:project-retro for this specified session transcript.
```

## Boundaries

- The skill reviews one session, not a collection of sessions, and does not modify files, create issues or send records to another agent or service.
- Incomplete source is labeled partial; missing events and time costs are not invented.
- A reusable-tool issue from one session remains a candidate. Recurring skill investigation belongs in a separately requested skill-retro.
- Accepting the recommendations does not authorize this skill to implement them.

## Related skills

- [loom-workflow:recap-state](../recap-state/README.md)
- [loom-workflow:skill-retro](../skill-retro/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
