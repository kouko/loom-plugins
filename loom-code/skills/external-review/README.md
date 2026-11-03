# external-review

[Loom](../../../README.md) / [loom-code](../../README.md) / external-review

Run one authorized review through an outside coding-agent CLI while keeping the caller’s review criteria.

## When to use

Use this when a review owner needs an independently executed review through Codex, Claude Code or Antigravity CLI. For a user-facing request to get another opinion, independent-advisor handles routing and disclosure.

## What you get

One structured execution result with the requested executor, explicit model and effort, preflight outcome, review text or failure reason, and the strength of the observed execution evidence.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-code:external-review for this authorized packet, executor and review root, keeping the owning review criteria.
```

## Boundaries

- A direct request naming the outside agent and an unambiguous target can authorize one bounded review; a suggestion alone cannot.
- Cost, vendor data transfer, local execution and filesystem limits are disclosed before network-backed discovery or review.
- The starting directory is not a general filesystem sandbox. Claude’s restricted model file tools have a narrower boundary; startup and caches can still write elsewhere.
- A completed process is not an accepted review verdict. The owner validates the result, and a failed leg is reported separately without a silent retry or provider switch.

## Related skills

- [loom-workflow:independent-advisor](../../../loom-workflow/skills/independent-advisor/README.md)
- [loom-code:closing-review](../closing-review/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
