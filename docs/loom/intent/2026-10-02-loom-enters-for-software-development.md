# Loom enters for software development without outside rules
originator: kouko
kind: engineering
needs-design: no — changes which requests the agent routes into loom through skill descriptions and the session-start text, both skill/gate artifacts rather than a user interface; no new state, command or output format
evidence: [loom-code/hooks/session-start, loom-code/hooks/hooks-codex.json, loom-design/skills/capture-intent/SKILL.md, loom-code/skills/using-loom-code/SKILL.md, loom-code/skills/write-plan/SKILL.md]
status: confirmed 2026-10-02
publication: automatic — authorized 2026-10-02 by kouko

## Problem
kouko removed every loom line from their personal rules to check whether loom works on its own. Without those lines, a plain request such as "add a feature" or "fix this bug" does not reliably start loom: the skill descriptions only claim requests that name loom or that already have an intent, the session-start text describes the stations without saying which requests belong to them, and Codex receives no session-start text at all. Anyone who installs loom without such personal rules gets the same result, so changes are made without an intent, review or acceptance report.

## Proposed outcome
On every host loom supports, a software-development request to add a feature or fix a bug starts loom's intent capture before any file is edited, whether or not the request mentions loom and whether or not the repository already uses loom. Small edits, and work that is not software development, proceed without loom unless the user asks for it.

## Acceptance
1. On Claude Code and on Codex, in a live session with no loom lines in the user's personal rules, a request to add a feature or fix a bug that does not mention loom starts loom's intent capture before any file is edited — both in a repository that already has a loom folder and in one that does not.
2. On Claude Code and on Codex, a small edit request (a typo fix or a rename) is made directly without starting loom, and starts loom when the user asks for loom.
3. On Claude Code, a request that is not software development (for example research or note-taking in a notes folder) does not start loom.
4. Antigravity CLI and OpenCode load the same session-start instruction as Claude Code, shown from the files each host loads.
5. On Codex, the session-start hook runs without being marked failed.
6. The three small issues left by PR #74 are fixed: the ship station no longer mentions a narrow-change line nothing produces, the verification status no longer takes a depth argument whose values behave the same, and the trailing blank line in its test file is removed.
7. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

## Constraints
- No new per-user or per-repository switch; the existing switch that turns off loom's session-start text stays the only opt-out.
- The stations' flow and the three decision points stay as they are.

## Out of scope
- A place to keep ideas that are not being worked on yet.
- Codex IDE extensions and apps, and other hosts that do not run plugin hooks.
- Changing what happens inside a station once loom has started.

## Open questions
- none
