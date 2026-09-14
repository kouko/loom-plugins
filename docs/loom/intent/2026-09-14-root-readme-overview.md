# Rewrite the root README as a public overview of the Loom plugins
originator: kouko
kind: engineering
needs-design: no — this rewrites repository documentation only; it changes no plugin behavior, CLI, or interface surface
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
The root `README.md` still describes the repository as a local extraction
candidate. A first-time reader of the soon-public repository cannot learn
what each of the three plugins does or how a Loom change flows from idea to
merged pull request without opening several plugin READMEs and internal docs.

## Proposed outcome
The root README is a self-contained entry point: it explains the three
plugins and shows the main Loom flow as a Mermaid diagram, while keeping the
development commands and migration provenance that remain true.

## Acceptance
1. The root README describes `loom-code`, `loom-design`, and `loom-workflow`, each with its purpose and main skills, consistent with the plugin manifests.
2. The root README contains a Mermaid flowchart of the main Loom flow (capture-intent → write-spec → write-plan → build → review → ship, maintain feeding back) including the three user decision points, and it renders on GitHub.
3. The root README gives install instructions that work against this repository's own marketplace.
4. Development commands and migration provenance remain present, and no statement in the README contradicts the repository being published.

## Constraints
- Plugin manifests, plugin READMEs, and plugin versions stay unchanged.
- The README stays in English, matching the repository's documentation language.

## Out of scope
- Changing plugin-level READMEs or their install URLs.
- Changing repository visibility, branch cleanup, or marketplace cutover inside the change itself.

## Open questions
- none
