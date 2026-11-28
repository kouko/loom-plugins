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
against loom's stations. This is a discovery/evaluation record; no loom change
is proposed in this file.

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

## Decision impact

No decision yet. This record exists to feed one-at-a-time discussion of
whether each idea is referenceable into loom's stations. The highest-signal
candidates to discuss first, in my order:

1. `tdd`'s **tautological-assertion anti-pattern** (loom build/implementer
   instructions do not currently forbid it).
2. `codebase-design` as a **standalone vocabulary skill** referenced by others
   (matches the repo's Module Criteria locate rule; loom currently carries
   such vocabulary inline in per-skill prose).
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
