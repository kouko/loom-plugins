# Point plugin manifest URLs at loom-plugins
originator: kouko
kind: engineering
needs-design: no — this changes manifest metadata links only; it changes no plugin behavior, CLI, or interface surface
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
The three plugins' Claude Code and Codex manifests still give
`kouko/monkey-skills` as their homepage, repository, and website. Marketplace
and plugin pages built from these manifests send users to the old repository
instead of the public `kouko/loom-plugins` repository.

## Proposed outcome
Every manifest link for the three plugins points to `kouko/loom-plugins`.

## Acceptance
1. No `.claude-plugin/plugin.json` or `.codex-plugin/plugin.json` under `loom-code`, `loom-design`, or `loom-workflow` contains `kouko/monkey-skills`; each homepage, repository, and website link points to `kouko/loom-plugins`.
2. The Codex manifest sync check and the repository's existing package test suite pass.

## Constraints
- Only link values change; names, versions, descriptions, and every other manifest field stay unchanged.

## Out of scope
- READMEs, skill files, and any plugin behavior.

## Open questions
- none
