# Modular adversary recipes

originator: kouko
kind: engineering
needs-design: no — internal agent contracts and reference files only, no surface a user reads or types into
status: confirmed 2026-09-18
publication: automatic — authorized 2026-09-18 by kouko

## Problem

Every attack recipe the adversary works from sits in one 120-line file: the recipes for code, for a spec, and for a skill or gate, together with the protocol shared by all of them (reuse first, mutation evidence, how a probe is recorded). Nothing in the layout says where one capability starts and the next ends, so all three kinds of work are harder than they should be.

Changing one kind means editing the file every other kind depends on, and the diff cannot show which kinds were affected. The tests repeat the coupling: the sentences of all three recipes are pinned inside test files covering the whole document, so a change to the code recipe can turn a test about the spec recipe red. Adding a kind means appending to the same file again. Removing one means deleting passages out of the middle of a shared document and then hunting for the pinned sentences and cross-references left behind, with no list saying what belonged to it.

Filing works against separation too: the file lives under the closing-review station, while the station that triggers it is build and its reader is the adversary agent, which points at it with a path that only resolves while this repository is the working directory.

## Proposed outcome

Each kind of artifact has its attack recipe in one file that carries everything specific to that kind, so the three lifecycle operations are each confined to it: changing a kind touches its file and its own test, adding a kind adds a file and a routing line without editing any existing recipe, and removing a kind deletes its file and its routing line and leaves nothing dangling. The protocol every kind shares is the one part whose change is meant to affect all of them.

## Acceptance

1. Each attack recipe that exists today (code, spec, skill and gate) is its own file, and the protocol shared by all of them is a separate file; all of them sit in the plugin's own top-level reference directory, with no station folder holding any of them.
2. Everything specific to one kind of artifact is in that kind's file: no rule that applies to only one kind lives in the shared file or in another kind's file.
3. Changing one recipe produces a diff confined to that recipe's file and its own test file; the other recipe files and their tests are untouched and still pass.
4. Adding a recipe for a new kind consists of adding one file and one routing entry, with zero edits to any existing recipe file; a reader can follow the routing table and do it once without guessing.
5. Removing one kind consists of deleting its file and its routing entry: after the deletion no reference anywhere names the removed file, and every remaining test passes.
6. Each recipe file has its own test file, so a failure names the recipe that broke.
7. Given the kinds of artifact a change touched, reading the shared protocol plus the matching recipes yields a complete, executable procedure without opening any station folder.
8. Every rule present before the split is still present after it, and none was added: a line-by-line correspondence list shows where each rule now lives.
9. The four properties this split is judged by — change, add, remove, locate — are written down in the repository's own conventions in a form the next part of loom can be held to, and the repository's roadmap records that the rest of loom is to be brought to the same shape one part per change.
10. In a clean environment, the complete package suite passes.

## Constraints

- The content of the recipes does not change: this change separates them, it does not rewrite what they say.
- No subfolder inside a subfolder: the repository's flat skill-folder rule stays in force.
- Paths the agent contracts use must resolve on Claude Code, Codex CLI and Antigravity CLI; only Claude Code substitutes `${CLAUDE_PLUGIN_ROOT}`, so the host-neutral `<loom-code>` form the repository already uses is the one to use.
- The checker's deterministic rules are not touched.

## Out of scope

- Splitting the adversary into several subagents, one per kind of artifact.
- Writing recipes for kinds that have none today (plan, docs, memory, intent, map, standing, evidence).
- Anything on the execution side: how `finalize-review` runs adversarial programs, and the uncommitted work in this worktree that addresses it.
- Repairing resource paths in agent contracts whose target this change does not move.
- Restructuring any other loom reference or station file along the same lines.

## Open questions

- none
