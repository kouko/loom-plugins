# closing-review

[Loom](https://github.com/kouko/loom-plugins/blob/main/README.md) / [loom-code](../../README.md) / closing-review

Independently review completed work and generate evidence tied to the content that was checked.

## When to use

Use this after Build finishes its required checks, or when functional changes have made earlier review evidence stale. The review uses the whole branch change, not just the last fix.

## What you get

Reviewer findings, an independent acceptance test report when needed, and generated `docs/loom/<change-id>/attestation.json` when the retained verification steps pass. The attestation records which content and evidence were reviewed.

## How to use

Install the plugin as described in its [README](../../README.md), then ask
your coding agent to use the skill. For example:

```text
Use loom-code:closing-review for the completed change 2026-11-03-export-history.
Re-run closing review after the functional fixes changed the reviewed content.
```

## Boundaries

- Review depth comes from the checker; acceptance testing is required when an acceptance condition cannot be settled mechanically.
- Functional fixes return to Build. Review proceeds within a bounded episode and stops with a non-convergence report when that limit is reached.
- The checker re-executes the package suite and adversarial programs during finalization. Agents never hand-edit the attestation.
- An authorized skip of required verification is disclosed as verification absent; it is not reported as a passing review.

## Related skills

- [loom-code:build](../build/README.md)
- [loom-code:external-review](../external-review/README.md)
- [loom-code:ship](../ship/README.md)

Runtime instructions: [SKILL.md](SKILL.md).
