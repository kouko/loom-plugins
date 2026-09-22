# Make the loom plugins installable and usable under Antigravity CLI
originator: kouko
kind: engineering
needs-design: no — adds packaging and hook adapters for a third agent host; the only user-typed change is the review station's new name, which the user already fixed as closing-review, so there is no behaviour left to design
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
The three loom plugins (loom-code, loom-design, loom-workflow) only install on
Claude Code and Codex. People using Google's Antigravity CLI (`agy`) cannot run
the loom flow at all. A spike on agy 1.2.2 (2026-09-14) showed the gaps: agy
needs a root `plugin.json` per plugin; skill prose points at
`${CLAUDE_PLUGIN_ROOT}`, which agy does not substitute, so bundled checker
scripts cannot be found; agy has no SessionStart event and uses different tool
names and hook payloads; and agy de-duplicates skills by short name, so the
`review` station is silently hidden whenever another installed plugin also
ships a skill named `review` (observed with two common plugins).

## Proposed outcome
Anyone with Antigravity CLI can install all three loom plugins from the GitHub
repository and take a change through the whole loom flow, with the same gates
enforced, while Claude Code and Codex installs keep working exactly as before.

## Acceptance
1. On a machine with agy and no prior loom install, following the repository's written install steps from a fresh clone installs all three plugins, and agy's plugin validation passes for each.
2. After installing, every station and skill of the three plugins appears in agy's skill list, including when another installed plugin ships a skill with the same short name.
3. In agy, a small change in a throwaway repository is taken through capture-intent, write-plan, build, closing-review and ship; the loom checker accepts the intent, plan and attestation it produced, and its blind-run report is produced and committed on the change branch.
4. In agy, pushing a change branch that has no matching review attestation is blocked by the loom push gate, and the first reason shown says the review attestation is missing.
5. In agy, a new session receives loom's station order and the repository's kickoff defaults without the user asking.
6. In agy, after a loom skill is used in a Japanese or Chinese conversation, the language reminder that Claude Code gives also reaches the agent.
7. In agy, writing a nested subfolder inside a skill folder is rejected by the loom-workflow folder-structure rule.
8. The existing package test suite and the Codex manifest drift check still pass, so Claude Code and Codex installs are unchanged.
9. The repository's product principles name Antigravity CLI alongside Claude Code and Codex as a supported host.
10. On Claude Code, Codex and agy the review station is invoked as `closing-review`, and loom's own station order and guidance use that name.

## Constraints
- Claude Code and Codex install layout, skill names and behaviour must not change, except that the review station is renamed `closing-review` on every host (user-decided 2026-09-14; the old `review` name stops working and no alias is kept, because an alias named `review` would collide again on agy).
- When the push gate blocks a push that lacks a review attestation, the missing attestation is named first on every host; which pushes are blocked does not change (user-decided 2026-09-14 after the first blind run), except that publication commands are now recognised regardless of letter case (e.g. `GIT push`, `Gh pr create`), so those case variants are blocked on every host as well (user-decided 2026-09-14: closes a bypass on case-insensitive filesystems).
- Target is the Antigravity CLI (`agy`, verified on 1.2.2); hooks stay host-installed plugin hooks, never repository-local or git hooks.
- Skill folders stay flat (no nested subfolders), per the repository's skill structure rule.

## Out of scope
- The Antigravity desktop app (2.0) and Antigravity IDE, where plugin hooks are reported not to fire.
- Publishing to an Antigravity marketplace; installation is from a clone of the repository.
- distill-sessions and handoff reading Antigravity conversation transcripts.
- Using Antigravity as the second-vendor reviewer from Claude Code or Codex.

## Later changes
- PR #43 replaced Acceptance 4 and the Constraints bullet on which pushes the push gate blocks: in agy an unattested push is no longer blocked. `loom-code/hooks/agy_adapter.py` allows publication commands, with a reminder. It denies a command only when the checker exits 2 (the `selection.guard` refusal), when the payload has no CommandLine or cannot be read, or, when the checker is missing or fails, when the command names or runs inside the selection record store.
- Decision recorded in #43's PR body Decisions table and intent 2026-09-22-publication-floor-moves-to-github.

## Open questions
- none
