# ship

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-code](../../README.md) / ship

Publish a change branch, prepare its pull request and observe the required CI checks.

## When to use

Use this after closing review, normally with a matching committed attestation. Publication must be explicitly authorized, either by the intent’s recorded authorization or by a publication decision for a legacy intent.

## What you get

A pushed branch, an opened or reused PR, a disclosure of locally computed verification status, and the observed CI result. At acceptance, the user sees the result and the acceptance test report when one exists.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-code:ship to publish the reviewed change and watch its required checks.
Use loom-code:ship to correct this PR body without changing committed content.
```

## Boundaries

- Ship does not rerun functional tests or adversarial programs. Absent or stale verification is disclosed rather than invented.
- Publishing never authorizes merge. Only after explicit maintainer acceptance may the flow use the separate land command; it never substitutes a direct gh pr merge.
- Functional or test fixes return to Build and the same bounded review episode. Publication-only text fixes can reuse matching evidence.
- GitHub protection changes and destructive cleanup need their own applicable authorization.

## Related skills

- [loom-code:closing-review](../closing-review/README.md)
- [loom-workflow:git-memory](https://github.com/kouko/loom-plugins/blob/main/loom-workflow/skills/git-memory/README.md)
- [loom-code:maintain](../maintain/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
