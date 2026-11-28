---
title: "mattpocock/skills: candidate implementations to reference for loom improvements"
type: loom-research
status: in-progress
created: 2026-11-28
updated: 2026-11-28
tags:
  - loom/research
---

# mattpocock/skills — candidate implementations to reference for loom improvements

## Question and scope

The organization's Claude Code usage export (2026-11-01 to 2026-11-30) shows
the skills `codebase-design` (26 invocations) and `tdd` (24 invocations) in
use. Source attribution identified `mattpocock/skills` as the likely pack for
these two names plus related siblings (`grill-with-docs`, `writing-for-agents`,
`grilling`). This record inventories the pack and the two named skills in
detail, and lists candidate implementation ideas worth discussing one at a time
against loom's stations. This is a discovery/evaluation record; loom changes it
leads to go through their own intents.

## Method and evidence

- Cloned `https://github.com/mattpocock/skills` (depth 1, v1.3.2) to
  `/tmp/mattpocock-skills-research/skills` on 2026-11-27.
- Read in full: `skills/engineering/codebase-design/SKILL.md` (114 lines),
  `skills/engineering/tdd/SKILL.md` (38 lines), `README.md` (installation
  model, skills.sh).
- Enumerated all 38 SKILL.md files' frontmatter descriptions.
- Cross-referenced CHANGELOG head for the current release's behavior notes.

## Findings

### The pack

`mattpocock/skills` is an editable, composable engineering-workflow skill pack:
38 skills under `engineering/`, `productivity/`, `in-progress/`, `misc/`.
Distribution philosophy differs sharply from loom: **small, easy to adapt,
composable files copied into the project and owned by the user** (`npx
skills@latest add`), with no gate-checked stations. The README's own framing
rejects owning the process (GSD / BMAD / Spec-Kit style) in favor of
user-editable building blocks.

### codebase-design (114 lines)

A **vocabulary skill, not a process**: defines 6 exact terms and the rule that
they must not be substituted. It is referenced by `tdd` and
`improve-codebase-architecture`; its own description says "a reference to
consult, not a session to run".

| Term | Meaning (paraphrased) | Loom parallel |
|---|---|---|
| module | anything with an interface and implementation; scale-agnostic | task/module boundary concepts |
| interface | everything a caller must know (signature + invariants + errors + config + perf) | spec REQ surface |
| depth | leverage at the interface: behaviour per unit of interface learned | — |
| seam (Feathers) | place where behaviour can be altered without editing in place | test insertion point |
| adapter | concrete thing satisfying an interface at a seam; role not substance | — |
| locality | what maintainers get from depth; change concentrates | — |

Key rules worth discussing:
- **Deletion test**: if deleting a module makes complexity vanish it was a
  pass-through; if complexity reappears across N callers it earns its keep.
- **One adapter = hypothetical seam; two adapters = real one.** Do not
  introduce a seam unless something actually varies across it.
- **Testability design**: accept dependencies don't create them; return results
  don't produce side effects; small surface area.
- **Rejected framings**: depth-as-line-ratio (Ousterhout) is rejected in favor
  of depth-as-leverage; "interface" is not the TS keyword; "boundary" is
  rejected as DDD-overloaded.

### tdd (38 lines)

A **test-first discipline skill** that uses codebase-design's vocabulary:

- Tests live at **pre-agreed seams** only — before any test, list the seams and
  confirm with the user; no test at an unconfirmed seam.
- Three anti-patterns:
  1. **Implementation-coupled** — mocks internals, tests private methods,
     verifies through side channels. Tell: test breaks on refactor without
     behavior change.
  2. **Tautological** — assertion recomputes the expected value the same way
     the code does (`expect(add(a,b)).toBe(a+b)`), so it passes by
     construction and can never disagree with code. Expected values must come
     from an independent source of truth: known-good literal, worked example,
     spec.
  3. **Horizontal slicing** — all tests first, then all implementation; tests
     imagined behavior and commits to test structure before understanding the
     implementation. Work in vertical slices (one test → one implementation →
     repeat), each a tracer bullet.
- Loop rules: red before green; one slice at a time; **refactoring is not part
  of the loop** (belongs to code-review).

### Other pack skills with loom-relevant parallels

| mattpocock skill | looms parallel | worth noting |
|---|---|---|
| `code-review` (two axes: Standards + Design, sub-agents) | closing-review | two-axis reviewer split |
| `diagnosing-bugs` (mutation-diff RED verification) | adversary probes | verifies a forced mutation against a pristine copy before trusting the red |
| `to-spec` / `to-tickets` | capture-intent → write-plan | conversation → spec/tickets synthesis |
| `triage` / `wayfinder` (issue-tracker state machine) | maintain | issue-tracker routing |
| `grilling` / `grill-with-docs` | critique | relentless interview; words questions so "yes" accepts the recommended answer |
| `chief-of-staff` (dated wiki memory, commit-cited claims) | loom-memory | historical record discipline |

### Where codebase-design is used, mapped to loom stations

The original is consulted before and during code design, not after: `tdd`
calls it before writing tests when the interface shape is in question
(`tdd/SKILL.md:22-26`), users call it to design an interface, and
`improve-codebase-architecture` calls it to scan existing code for shallow
modules.

| Moment | Loom station | Current state |
|---|---|---|
| Before code | write-plan — each task owns "one module boundary" and marks the entry other modules call (`loom-code/skills/write-plan/SKILL.md:263-268`) | no criterion for whether the boundary is well cut |
| While coding | build — implementer reads `loom-code/references/engineering-baseline.md` | §5 has short versions of some rules |
| After code | closing-review — reviewer reads `loom-code/skills/closing-review/references/lenses.md` | `deletion-first`, `architecture`, `refactoring` already cover the one-adapter rule and pass-through modules; no "shallow" criterion |
| Periodic scan of existing code | none | no loom entry point |

`loom-design:architecture-design` was considered and rejected as the home: it
runs on request only, at repo level (module split, folder layout, CI), and
never blocks a change.

### Writer and judge read different texts of the same rule

| Rule | Writer (`engineering-baseline.md` §5) | Judge (`lenses.md`) |
|---|---|---|
| Abstraction | "no abstraction for a single use" | `deletion-first`: two concrete users now, **or** an explicit request, **or** a visible motivation |
| Tests | "A test that cannot fail when the logic changes is not a test" | `tests` asks only for RED→GREEN evidence |
| Pass-through modules | absent | `deletion-first`: a forward-only module or function is a finding |

The abstraction threshold disagrees: the writer is forbidden what the judge
accepts.

### Shared file vs reference-only skill (research 2026-11-28)

Two research passes, official docs and practitioner sources. No source
compares the two forms head to head.

Official documentation:
- Both forms are supported; neither is prescribed. A reference-only skill has
  direct support: `user-invocable: false` "for background knowledge that isn't
  actionable as a command" (https://code.claude.com/docs/en/skills).
- A shared file under the plugin root is copied with the plugin; only files
  above the plugin root are not ("Files outside the plugin directory aren't
  copied", https://code.claude.com/docs/en/plugins/loading.md). Loom-code
  already ships `references/engineering-baseline.md` and the reviewer's
  `lenses.md` read this way.
- Anthropic's example repo duplicates shared scripts per skill
  (`skills/{docx,pptx,xlsx}/scripts/office/`), https://github.com/anthropics/skills.
- Skill-to-skill invocation is undocumented; plugin-level `dependencies`
  exist (https://code.claude.com/docs/en/plugins/dependencies.md).
- Every skill's description is in context every turn; the listing budget is
  1% of the context window, least-used descriptions dropped first
  (https://code.claude.com/docs/en/skills); Codex uses at most 2%
  (https://learn.chatgpt.com/docs/build-skills). A file costs nothing until
  read (https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices).
- Subagents do not inherit skills; an agent's `skills:` field preloads full
  content, or the agent calls the Skill tool itself
  (https://code.claude.com/docs/en/sub-agents). Whether `skills:` works for
  plugin agents is unverified.

Practitioner sources:
- Least-invoked skills lose their description first under the listing
  budget; superpowers 4.0 merged rarely used skills to save it
  (https://blog.fsck.com/2025/12/17/claude-code-skills-not-triggering).
- One author measured skill firing rising from 15% to 62% after adding a
  session-start hook (single source,
  https://towardsdatascience.com/a-session-start-hook-raised-claude-code-skill-firing-from-15-to-62/).
- mattpocock moved `LANGUAGE.md` and `deep-modules.md` out of `tdd` and
  `improve-codebase-architecture` into `codebase-design` and marked it
  **Breaking** because users must install it too
  (https://github.com/mattpocock/skills/blob/main/CHANGELOG.md).
- Both forms share one weakness: a "read this file" or "call this skill" line
  is still a model decision; each consumer must say when to read it.

| Criterion | Shared file | Reference-only skill |
|---|---|---|
| Loom's own stations and agents reliably read it | yes, by path; already in use | preload unverified for plugin agents, else a model decision |
| Context cost per turn | 0 | ~100 tokens, competes for the listing budget |
| Codex and other hosts | any host that reads files | depends on the Skill tool and its budget |
| Usable outside loom stations | no | yes |
| User can invoke by name | no | yes |

## Decision impact

Decisions so far (2026-11-28):

1. **Adopted** — `tdd`'s tautological-assertion anti-pattern goes into the
   writer's and judge's test standard.
2. **Adopted, reshaped (user-decided: option B, three files)** — no
   standalone `codebase-design` skill. Extract three plugin-level shared
   standard files under `loom-code/references/`: tests, code design, and
   docs/skill text. `engineering-baseline.md`, `lenses.md` and write-plan's
   task-size rule cite them, so writer and judge read one text. Item 1 and a
   "shallow module" criterion land in these files; the abstraction-threshold
   disagreement above is resolved there. The docs/skill-text file takes the
   docs-lens dimensions (omission, ambiguity, polarity against the base,
   deletion-first for docs and skill), which today only the judge reads. A
   `user-invocable: false` skill pointing at the same files can be added later
   if a consumer outside loom stations appears; nothing now depends on it.
   The periodic-scan entry point is deferred.

Not yet discussed:

3. `diagnosing-bugs`' **mutation-diff RED verification** (adversary already
   does mutation; the diff-against-pristine step may be borrowable).
4. `code-review`'s **two-axis reviewer split** (closing-review lens design).

## Limitations

- Attribution of the usage-export names to this pack is plausible but not
  confirmed (name collisions exist in the public ecosystem); the value of this
  record does not depend on that attribution — it stands as a candidate-source
  inventory.
- Clone is depth-1 at a point in time; pack evolves weekly.
- Only codebase-design, tdd and the enumerated frontmatter were read in full;
  other skills were judged on one-line descriptions.
