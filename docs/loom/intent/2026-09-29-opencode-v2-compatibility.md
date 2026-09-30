# Make the loom plugins installable and usable under OpenCode v2
originator: kouko
kind: engineering
needs-design: no — adds packaging and adapters for a fourth agent host; installation uses OpenCode's own plugin command and dialog, and no loom command, skill name or output changes, so there is no behaviour left to design
status: confirmed 2026-09-29
publication: automatic — authorized 2026-09-29 by kouko

## Problem
The three loom plugins (loom-code, loom-design, loom-workflow) install on
Claude Code, Codex and Antigravity CLI, but not on OpenCode v2. People using
the OpenCode CLI/TUI with third-party cloud models cannot run the loom flow
at all. A spike on OpenCode v2.0.18 (2026-09-29) showed why: OpenCode installs
a plugin only as a package (`opencode plugin add <npm or git spec>`, or the
TUI's plugin dialog) that registers its skills and agents in code; it does
not read `.claude-plugin/plugin.json`, does not discover a plugin's `skills/`
folder on its own, names subagents by bare file name (no `loom-code:`
prefix) and dispatches them through a `subagent` tool, and its v2 plugin API
declares no lifecycle hooks — whether the older hook events still fire on
v2 is unverified.

## Proposed outcome
Anyone with the OpenCode v2 CLI/TUI can install all three loom plugins from
the GitHub repository with OpenCode's own plugin command or TUI dialog and
take a change through the whole loom flow, as on Claude Code, Codex and
Antigravity CLI, while those three hosts keep working exactly as before.

## Acceptance
1. On a machine with OpenCode v2 and no prior loom install, each of the three plugins installs from the GitHub repository with OpenCode's official plugin command, and also from the TUI's plugin dialog, and OpenCode's plugin list shows all three.
2. In a new OpenCode session every station and skill of the three plugins is offered and loads its full instructions, including when another installed plugin ships a skill with the same short name.
3. In OpenCode, a small change in a throwaway repository, run on a third-party cloud model through the user's existing model setup, is taken through capture-intent, write-plan, build, closing-review and ship; the loom checker accepts the intent, plan and attestation it produced, the acceptance test report is committed on the change branch, and the pull request is opened.
4. During that run, loom's implementer, reviewer, adversary and acceptance-tester roles each run as separate OpenCode subagents.
5. Each behaviour that loom's hooks give on the other hosts — the session-start station order and kickoff defaults, the publication reminder, the language reminder, the skill folder-structure rule and the selection-record guard — either works in OpenCode, or OpenCode's install instructions name it as unavailable with the reason.
6. The existing package test suite and the Codex manifest drift check still pass, so Claude Code, Codex and Antigravity CLI installs are unchanged.
7. The repository's product principles name OpenCode v2 alongside Claude Code, Codex and Antigravity CLI as a supported host.
8. The three plugins each carry a new version, consistent across manifests, CHANGELOGs and READMEs.

## Constraints
- No new loom capability specific to OpenCode: existing stations, skills, agents and gates are made to run there, nothing is added (user-decided 2026-09-29).
- Target is the OpenCode v2 CLI/TUI (verified on 2.0.18) with third-party cloud models; installation goes through OpenCode's official plugin command and TUI dialog, pointing at this repository (user-decided 2026-09-29).
- Claude Code, Codex and Antigravity CLI install layout, skill names and behaviour must not change.
- Hooks stay host-installed plugin hooks, never repository-local or git hooks.
- A hook behaviour OpenCode v2 cannot provide is listed as unavailable in OpenCode's install instructions and the rest of the flow still ships; full hook parity is not a condition of done (user-decided 2026-09-29, option A).
- Skill folders stay flat (no nested subfolders), per the repository's skill structure rule.

## Out of scope
- OpenCode v1, the OpenCode desktop app and IDE integrations.
- Publishing to npm or any OpenCode registry; installation is from the GitHub repository.
- distill-sessions and handoff reading OpenCode conversation transcripts.
- Using OpenCode as the second-vendor reviewer from another host.

## Open questions
- none
