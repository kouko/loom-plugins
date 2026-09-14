# Add a loom-visualization skill for coding-harness conversations
originator: kouko
kind: engineering
needs-design: yes — multi-object selection behaviour (information shape × client × output mode) with no spec
status: confirmed 2026-09-14
publication: automatic — authorized 2026-09-14 by kouko

## Problem
When an agent in a coding harness explains option comparisons, reasoning,
decisions, or execution flows, it mostly writes prose. When it does draw, the
result often breaks for the reader: Mermaid source appears raw in terminals,
tables with CJK labels misalign, and hand-drawn ASCII boxes drift. The rules
that used to push agents toward tables and diagrams were deleted in the loom
1.0 cutover, and the remaining pieces live in separate places
(`cot-explain` in this repo, `ascii-graph-toolkit` outside it) that a loom-only
install cannot rely on. Guidance written only as prose was measured to change
agent behaviour rarely.

## Proposed outcome
`loom-workflow` ships one self-contained visualization skill for conversational
output in coding harnesses (Claude Code, Claude Desktop/claude.ai, Codex,
Antigravity). It carries a curated template library organised by information
shape, picks a presentation form that the current client can actually display,
generates CJK-safe ASCII diagrams, and absorbs `cot-explain`'s reasoning page as
one of its modes. It is explicitly separate from Obsidian note diagrams.

## Acceptance
1. `loom-workflow` provides a `loom-visualization` skill and no longer provides `cot-explain`; the plugin installs on Claude Code and Codex, and references to `cot-explain` elsewhere in the repository point to the new skill.
2. The skill provides templates for 11 information shapes — option comparison, linear steps, branching decision, reasoning/causal chain, state/lifecycle, actor interaction sequence, hierarchy, system architecture, data model, timeline, quantity — each with a markdown-table form, an ASCII form (or a stated table substitute), and a Mermaid form.
3. Given the environment of a Claude Code terminal session, a Codex CLI session, and an unrecognised environment, the skill's client check chooses the documented form for each, and never chooses Mermaid for a client not confirmed to render it.
4. ASCII diagrams with Chinese or Japanese labels produced through the skill pass its alignment check on a machine with no third-party Python packages installed.
5. Every Mermaid template in the skill parses without error under Mermaid's own parser.
6. Documented reasoning can still be turned into a standalone reasoning page, as `cot-explain` did before.
7. When the requested output is a note inside an Obsidian vault, the skill declines and points to the Obsidian visualizer, and no template contains Obsidian-only syntax.
8. In a fresh session with only the loom plugins installed, asking the agent to compare several options or to explain a multi-step flow produces a table or diagram following the skill, without the user naming the skill.
9. With `ascii-graph-toolkit` also installed, a session start shows one diagram trigger instruction, not two conflicting ones.
10. The repository's package test suite passes.

## Constraints
- The skill works with `loom-workflow` installed alone: no dependency on `ascii-graph-toolkit`, the `obsidian` plugin, or any third-party Python package at run time.
- Coding-harness templates and Obsidian templates are never shared or mixed.
- Third-party material is copied or adapted only under MIT-compatible licences, with attribution kept in the skill.
- Repository skill conventions hold: flat skill folder, SKILL.md size cap, no runtime citation of this repository's development records.
- `cot-explain` is removed without a compatibility alias, and the removal is recorded as a breaking change (user-decided 2026-09-14).
- Committed artifacts stay in English.

## Out of scope
- Diagrams inside Obsidian notes, and editing the `obsidian-mermaid-visualizer` skill or its description.
- Diagram rules for commit messages, pull requests, and committed repository docs (owned by `git-memory`, `ship`, and `write-spec`).
- Retiring, changing, or syncing `ascii-graph-toolkit` in the monkey-skills repository.
- Making the reasoning page render offline.

## Open questions
- none
