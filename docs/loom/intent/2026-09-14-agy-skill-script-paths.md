# loom-workflow skills find their scripts on every host, and the visualization trigger card reaches agy
originator: kouko
kind: engineering
needs-design: no — rewrites skill instructions, adds a lint and routes an existing trigger card to another host; no user-typed surface or multi-state behaviour to design
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
After Antigravity CLI support merged, two gaps remain in loom-workflow. First,
loom-visualization and goal-create tell the agent to run bundled scripts as bare
`python3 scripts/...` commands, which resolve against the agent's current
directory rather than the skill folder; the cross-host path spike showed this
form failing on Claude Code (0/2) and agy (1/2), so diagram generation, client
detection and goal linting can fail depending on where the agent happens to be.
The repository lint added for plugin-root paths does not catch this form, so new
skills can reintroduce it. Second, loom-workflow's SessionStart hook that injects
the loom-visualization trigger card has no equivalent on agy, which has no
SessionStart event, and loom-workflow ships no hook for Codex at all, so agy and
Codex sessions never receive the instruction to lead with a table or diagram;
the agent only uses loom-visualization when the user explicitly asks for a
visual.

## Proposed outcome
loom-visualization and goal-create locate and run their bundled scripts
regardless of host or working directory, the repository rejects new bare script
paths in skill instructions, and agy and Codex sessions receive the same
loom-visualization trigger card that Claude Code sessions receive, without
changing what Claude Code users get today.

## Acceptance
1. On Claude Code and on agy, from a working directory outside the skill folder, loom-visualization runs its bundled scripts successfully when producing a diagram, and goal-create runs its bundled lint script.
2. A skill instruction that contains a bare `python3 scripts/...` style command is rejected by the repository's contract lint, and the current loom-workflow skills pass it.
3. A new agy session and a new Codex session with loom-workflow installed each receive the loom-visualization trigger card text without the user asking for it.
4. Claude Code sessions still receive the trigger card exactly once, and the existing package test suite passes.

## Constraints
- Reuse the cross-host path wording already adopted for plugin roots (Claude Code variable, other hosts derive from the file's own location); do not introduce install-time path rewriting.
- The trigger card text keeps a single source; host routing must not create a second hand-maintained copy.
- Target Antigravity CLI 1.2.2 (`agy`); the Antigravity desktop app and IDE stay out of scope.
- Codex also receives the trigger card in this change (user-decided 2026-09-14).

## Out of scope
- Changing what the trigger card says or when loom-visualization chooses a diagram.
- Other loom-workflow skills' behaviour beyond their bundled-script paths.
- agy second-vendor review and the other follow-ups listed on PR #8.

## Open questions
- none
