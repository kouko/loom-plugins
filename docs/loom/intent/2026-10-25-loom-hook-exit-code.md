# Fix Loom hook exit-code handling across hosts
change_id: 2026-10-25-loom-hook-exit-code
originator: kouko
kind: engineering
needs-design: no — existing hook behavior only; no new interface surface
status: confirmed 2026-10-25

## Problem
The Loom hooks can fail during ordinary commands in a zsh-based host because their shell commands assign the previous command's exit code to a read-only shell variable. Codex users see repeated hook failures even when the requested commands run successfully. The same variable name appears in the other host integrations.

## Proposed outcome
All four host integrations retain their existing hook behavior without colliding with a shell-reserved variable.

## Acceptance
1. The Codex command hook completes without a hook failure for an ordinary command under zsh.
2. The Claude Code, OpenCode, and AGY hook commands continue to return their intended results under their configured shells.
3. The affected hook commands also complete under zsh without a read-only variable error.

## Constraints
- Use the same Loom-prefixed exit-code variable in the affected hooks for all four hosts.
- Preserve the existing checker-result handling and runtime-unavailable fallback behavior.

## Out of scope
- Other hook behavior or host integrations without this variable assignment.

## Open questions
- none
