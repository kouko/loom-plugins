# Rewrite the three plugin READMEs with flow diagrams
originator: kouko
kind: engineering
needs-design: no — this rewrites plugin documentation only; it changes no plugin behavior, CLI, or interface surface
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
Now that the repository is public, each plugin's README is still written for
the old `monkey-skills` home: install commands and repository links point
there, and none of the READMEs shows how the plugin's skills run together.
A reader who lands on a plugin page cannot see its execution flow at a glance
and may install from the wrong place.

## Proposed outcome
Every plugin README (`loom-code`, `loom-design`, `loom-workflow`), in English,
Japanese, and Traditional Chinese, is rewritten as a clear entry page for that
plugin, with a Mermaid diagram of its rough execution flow and install and
repository references that point to this repository.

## Acceptance
1. Each of the nine plugin READMEs (three plugins × English, Japanese, Traditional Chinese) is rewritten and describes its plugin's purpose and skills consistently with the plugin manifest and skills directory.
2. Each of the nine READMEs contains a Mermaid diagram of that plugin's rough execution flow that renders on GitHub, with labels in the README's language where they are prose.
3. The three language versions of each plugin README carry the same facts and the same diagram structure.
4. Install commands and repository links in all nine READMEs point to this repository's `loom` marketplace; none tells readers to install from `monkey-skills`.
5. The repository's existing package test suite passes with the rewritten READMEs.

## Constraints
- Plugin manifests, skill files, and plugin versions stay unchanged.
- Tests that pin README content are satisfied by the READMEs, not weakened or edited.
- The root README is not changed.

## Out of scope
- Changing plugin behavior, skill contracts, or the root README.
- Historical provenance mentions of `monkey-skills` that describe where the code came from, as long as they do not direct installation there.

## Open questions
- none
