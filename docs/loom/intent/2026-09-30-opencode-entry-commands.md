# Start loom's entry skills from OpenCode's command list
originator: kouko
kind: engineering
needs-design: no — six existing skills gain a second entry point in OpenCode's slash-command list under the naming pattern expert-mode already uses; no skill name, skill content or behaviour changes, and the README gains a usage note, so there is no new behaviour to design
status: confirmed 2026-09-30
publication: automatic — authorized 2026-09-30 by kouko

## Problem
After installing loom in OpenCode v2, the only loom entry in the `/` command
list is `loom-code:expert-mode`. A user who wants to start loom — the
`using-*` entry skills of the three plugins — or run `handoff`, `recap-state`
or `goal-create` does not see them there, and has to know to open the skill
list or ask the model in words. The README's OpenCode section does not say how
to start loom once it is installed, so a new OpenCode user is left guessing
which of loom's many skills to begin with.

## Proposed outcome
In OpenCode, the three `using-*` entry skills and `handoff`, `recap-state`
and `goal-create` can be started from the `/` command list and still work as
skills the model loads; `expert-mode` stays a command only. The README tells
an OpenCode user how to start loom.

## Acceptance
1. In OpenCode v2 with loom installed, the `/` command list offers loom-code:using-loom-code, loom-design:using-loom-design, loom-workflow:using-loom-workflow, loom-workflow:handoff, loom-workflow:recap-state and loom-workflow:goal-create, and running each one starts that skill's workflow.
2. The same six remain available as skills the model can load in OpenCode, as before.
3. loom-code:expert-mode is still offered as a command and is still not offered as a skill.
4. The README's OpenCode section tells a user how to start loom after installing it, including these commands.
5. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

## Constraints
- Claude Code, Codex, Antigravity CLI and OpenCode keep the same install layout and skill names; only OpenCode's command list changes.
- Command names follow the existing `/<plugin>:<skill>` form expert-mode uses.

## Out of scope
- Registering any other loom skill as an OpenCode command.
- Changing how any skill behaves once started.
- Command lists on Claude Code, Codex or Antigravity CLI.

## Open questions
- none
