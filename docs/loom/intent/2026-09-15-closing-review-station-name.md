# Use the closing-review station name everywhere
originator: kouko
kind: engineering
needs-design: no — this rewords station references in skill, reference and agent prose; it changes no plugin behavior, CLI, or interface surface
status: confirmed 2026-09-15

## Problem
The review station was renamed to `closing-review`, but skill instructions,
references and agent contracts in `loom-code` and `loom-design` still call it
"the review station". Agents that read these instructions meet a station name
that no longer exists, so they may look for the wrong station or treat the two
names as different steps.

## Proposed outcome
Every instruction, reference and agent contract that names the station uses
`closing-review`.

## Acceptance
1. No skill, skill reference, or agent contract in `loom-code` or `loom-design` refers to "the review station" or to a `review` station; each such reference names `closing-review`.
2. The meaning of every reworded sentence is unchanged apart from the station name.
3. The repository's existing package test suite passes.

## Constraints
- Only the station name changes; no rule, gate marker, dimension name, or verdict wording changes.
- Generic uses of the word "review" that do not name the station stay as they are.

## Out of scope
- CHANGELOGs, historical plans, memory entries, and other development records.
- `loom-workflow` and the plugin READMEs.

## Open questions
- none
