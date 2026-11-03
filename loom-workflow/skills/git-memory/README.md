# git-memory

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-workflow](../../README.md) / git-memory

Record why a particular Git change was made and retrieve that rationale when it becomes relevant again.

## When to use

Use this before each commit, PR creation or merge, and when you need the reason behind a past Git decision. Classification runs even when the correct result is no memory content.

## What you get

A normal commit or PR message for routine work, or concise Decision, Learning or Gotcha content when a non-obvious choice, discovery or recognizable trap deserves capture. Recall produces a bounded, source-linked answer from Git history.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-workflow:git-memory before committing this change.
Use loom-workflow:git-memory to find why we chose the current parser.
```

## Boundaries

- Git messages are change-bound context. Durable repository lessons belong in loom-memory’s committed store.
- The skill does not require a trailer on every commit and does not write generic advice just to fill fields.
- Publication text passes its privacy checks. A request to classify memory is not permission to push or merge.
- Squash merges can move trailers out of Git’s structured footer; recall therefore supports text-based retrieval.

## Further reading

- [Commit protocol](protocols/compose-commit.md)
- [PR protocol](protocols/compose-pr.md)
- [Recall protocol](protocols/recall.md)

## Related skills

- [loom-workflow:loom-memory](../loom-memory/README.md)
- [loom-code:ship](https://github.com/kouko/loom-plugins/blob/main/loom-code/skills/ship/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
