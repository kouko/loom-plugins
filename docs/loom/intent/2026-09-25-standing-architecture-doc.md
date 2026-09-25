# A standing ARCHITECTURE.md that agents are held to, the way DESIGN.md is
originator: kouko
kind: engineering
needs-design: no — a new loom-design skill plus skill, lens and standing-check text in loom-code; skill/gate artifacts, not interface surfaces under the manifest globs
status: confirmed 2026-09-25
publication: automatic — authorized 2026-09-25 by kouko

## Problem
Projects built through loom have no standing record of their architecture:
which modules exist and what each may depend on, where new files go, how
large a file may grow, and which CI stages every change must pass. Each
change's spec or plan rediscovers the structure from the code, and nothing
holds an agent to a structural rule across changes.

Evidence from three local projects (2026-09-25 audit):
- komado-Viewfinder: agents dropped new files flat into `Views/`,
  `Utilities/` and `Services/`, then four same-day reorg commits regrouped
  them (`9543495`, `d37a8e7`, `aa3ac5b`, `bcb4b86`); two files grew to 1,248
  and 1,757 lines under 109 and 52 edits. Its CLAUDE.md already told agents
  to read per-folder READMEs before editing; six of nine folders have none.
- komado-Refs: AppDelegate was split reactively into nine files over 15
  commits, ImageReaderView over 13; the repo has no CI.
- kumiko-zaiku-app-icons: structure is clean because its PRINCIPLES.md pins
  one module boundary with a check; it has no CI.

Prose rules alone were not followed; rules with a check were.

## Proposed outcome
A project can hold one standing ARCHITECTURE.md. When a project has none, a
loom-design tool designs the engineering architecture and folder structure
with the user: it reads the project's requirements and existing code, proposes
options with trade-offs, and records what the user chooses as design decisions
with reasons plus structural rules. loom then holds each change to that
document at the same level it holds changes to DESIGN.md: planning reads it,
closing review checks conformance, a missing file is a warning and never a
block. Rules that can be checked mechanically also get a guard test that the
package suite runs, so a violation fails the build.

## Acceptance
1. In a repository without ARCHITECTURE.md, a loom-design tool reads the project's requirements and existing code and proposes an architecture covering module split and dependency direction, main technology choices, folder structure and required CI stages, giving at least two options with their trade-offs for each open choice, and the user picks.
2. The chosen design is written as a user-ratified ARCHITECTURE.md at the repository root holding the design decisions with their reasons and the structural rules, with no project overview and no data models or API interfaces.
3. Every rule in that file that can be checked mechanically comes with a guard test that the repository's package suite runs.
4. When a change breaks a checkable rule, the package suite fails with a message that names the rule, the offending file, and the two ways out: conform to the rule, or change the rule and its guard together.
5. When ARCHITECTURE.md exists, the plan for a change that adds or moves files places them by its rules and names the rule it followed.
6. When ARCHITECTURE.md exists, closing review reports whether the change conforms to it, and a violation is a finding that sends the change back; this uses the existing reviewers, with no reviewer added.
7. When ARCHITECTURE.md is absent, every change shows a warning line alongside the existing standing-document warnings, never blocks, and the existing waiver silences it; review scores that conformance check as not applicable.
8. When a change alters the structure, the same tool re-designs the affected part and updates its design decisions, rules and guards together.

## Constraints
- A missing ARCHITECTURE.md never blocks a change, matching DESIGN.md.
- No new station, no extra reviewer or dispatch per change.
- Prose is not a gate: only a guard test or a reviewer finding holds a change to a rule.
- The file is `ARCHITECTURE.md` at the repository root, beside PRINCIPLES.md and DESIGN.md (user-decided 2026-09-25).

## Out of scope
- Writing CI workflow files for a project; the document names required CI stages only.
- A per-change architecture planning station.
- Adding ARCHITECTURE.md to komado-Refs, komado-Viewfinder, kumiko-zaiku-app-icons or this repository.
- Having write-spec read ARCHITECTURE.md.
- Splitting visual design out of loom-design.
- Data models and API interfaces; they stay in each change's spec.

## Open questions
- none
