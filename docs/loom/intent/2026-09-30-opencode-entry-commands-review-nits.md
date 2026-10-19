# Clear the reviewer nits left from the OpenCode entry-commands change
originator: kouko
kind: engineering
needs-design: no — wording fixes in changelogs, a README label, loader comments and a test name, plus narrowing when the OpenCode prompt hook trims a recorded message; no new surface or multi-state behaviour
evidence: [https://github.com/kouko/loom-plugins/pull/72]
status: confirmed 2026-09-30
publication: automatic — authorized 2026-09-30 by kouko

## Problem
PR #72's two closing reviewers left nine non-blocking findings that were not fixed, because any edit after review would have invalidated the attestation. Readers are left with gaps. The changelogs never mention that the OpenCode transcript fix shipped. The loom-code README's "1 user-invoked" label reads as if only one skill can be run as a command. The zh-TW acceptance report uses three terms it never explains. The OpenCode prompt hook trims any user message that contains the skill-body separator, not only messages a command built. Maintainers also meet a duplicated separator literal, an unclear loader header comment, a test name that no longer matches its body, and two wrong details in the merged plan.

## Proposed outcome
All nine findings from PR #72 are resolved. The OpenCode transcript trims only the prompts that a loom command built; every other message is recorded whole.

## Acceptance
1. The loom-code, loom-design and loom-workflow changelogs state that on OpenCode a command's skill body is no longer recorded as the user's words.
2. On OpenCode, a message the user types that contains "Base directory for this skill:" is recorded in full, while a loom command's prompt is still recorded as only the typed command text.
3. The loom-code README (en, ja, zh-TW) no longer labels expert-mode "user-invoked" in a way that clashes with the entry skills now also runnable as commands.
4. The 2026-09-30-opencode-entry-commands acceptance report explains or replaces "important", "Build 階段" and "上次測試" in plain words, and that change's plan gives the correct edited test line range and the full W2-01 file list.
5. The loader keeps the skill-body separator in one place, its header comment says a skill with both keys stays command-only, and the renamed loader test says what it checks.
6. The existing package test suite passes, and each plugin whose files change carries a new version consistent across manifests, CHANGELOGs and READMEs.

## Constraints
- Skill names, command names and which skills are commands stay as PR #72 shipped them.
- Claude Code, Codex and Antigravity CLI behaviour is unchanged.

## Out of scope
- Removing expert-mode.
- Any other loom skill or loader behaviour.

## Open questions
- none
