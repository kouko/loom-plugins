# Lenses — what each dimension means, and what it is scored against

One reviewer contract, eight lenses. This file is the dimension definition
for all of them; `agents/reviewer.md` names the dimensions and points here
for what each one is asking. General knowledge of Clean Code, SOLID, DRY,
TDD, F.I.R.S.T and OWASP is assumed — the citations below say which source
settles a disagreement, not what to read first.

Under every lens, read the whole artifact, not only the delta — the entire
file for prose, the changed functions plus their callers for code. The
delta says where to look hardest; it never bounds the review.

## Severity and verdict

Severity is decided by consequence, never by where a finding lands or how
literally wrong the text is:

- **fatal** — ships a defect: a wrong result, an exploitable hole, a lost
  guarantee, an instruction that makes an executor do the wrong thing.
- **important** — a reader following the text would act wrongly, or a
  fact the checker or CI relies on is wrong (a path, a command, a number a
  rule reads back).
- **nit** — everything else: wording, terminology, units, the same fact
  stated two ways, readability — a reader following it still does the
  right thing, and nothing mechanical reads it. A sentence can be
  literally incorrect and still a nit, if no reader or machine acts on the
  wrong part of it.
- Any fatal → `NEEDS_REVISION`. Two or more important → `NEEDS_REVISION`.
  One important → `PASS_WITH_NOTES`. Only nits, or nothing → `PASS`.
- **Nits do not trigger another formal review:** record nits in the closing
  verdict, and Ship may batch safe publication-only wording fixes.
- A finding with no anchor, or with no concrete fix, is opaque and flips
  the whole verdict to `NEEDS_REVISION` however small it is: "naming is off
  somewhere" cannot be located or fixed by anyone.
- In every round, reviewers never run the complete package suite or the
  adversarial programs still under `docs/loom/<change-id>/evidence/probes/`:
  both run mechanically at the end of Build, and
  `finalize-review` executes them again and records the result. Not having
  run them is not grounds for `PASS_WITH_NOTES`. A probe
  graduated out of `evidence/probes/` into the repository's tests (for
  example `loom-code/tests/`) is also an ordinary changed test file,
  which reviewers run. A dimension whose pass
  rests on a claim you could check — by reading a source or by running a
  changed test file — and did not, scores `PASS_WITH_NOTES`, naming what was
  not independently checked. Never "could not see it, so it is fine".
- A dimension with nothing to conform to — no `PRINCIPLES.md`, no
  `DESIGN.md`, no `ARCHITECTURE.md` — scores `N/A` with the reason. `N/A` is not a pass and is
  never given for convenience.

## Code — twelve dimensions

| Dimension | What it asks | Settled by |
|---|---|---|
| security | Injection, authn/authz, secrets, unsafe deserialization, encoding confusion in every changed path | OWASP ASVS; 徳丸本 Ch.6 for character-encoding attacks |
| architecture | Does the shape the change produces hold — responsibilities, dependency direction, boundaries; module depth, the deletion test and code a test can drive are judged against `../../../references/code-design-standard.md` §5–6 | SOLID (Martin) |
| correctness | Does it do what it claims, at the boundaries as well as the middle; is there RED→GREEN evidence in the history | the changed test files, run by the reviewer |
| naming | Names and function length, judged against `../../../references/code-design-standard.md` §1 | Clean Code Ch.2–3 (Martin) |
| tests | Every shipped behaviour has focused RED→GREEN evidence; the reviewer runs the test files the change added or changed, except the adversarial programs still under `docs/loom/<change-id>/evidence/probes/` (a probe graduated into the repository's tests is a changed test file the reviewer runs), and a test in a changed test file the reviewer ran that is skipped or never actually executes is a finding, since a green exit code does not show that it ran; committed tests and adversarial artifacts must exercise the changed behavior rather than merely exit successfully; every rule in `../../../references/tests-standard.md` — tests that cannot fail for the behaviour they name, tautological assertions, tests coupled to the implementation, module entry versus internal-function tests, prose-pin tests, new tests against existing cases — is judged here, and a breach of it is a finding; an adversarial artifact whose command is a shell builtin (`true`, `:`), or whose command never names it, exits 0 for unrelated reasons — score `tests` `NEEDS_REVISION` and raise a finding naming that artifact; duplicate findings name surviving protection and a smaller shape; prose artifacts' qualified evidence = the checker's recomputed rules, fresh-context review, and — only when behavior changes — independent acceptance testing; a prose-only change needs no new executable test file. the carve-out: lens definition rows in this file are executed by closing-review reviewers, not recomputed by checker rules; only paragraphs carrying `<!-- gate: <id> -->` are checker-recomputed. | Beck, *Test-Driven Development* (2002) |
| refactoring | Duplication, smells and extraction, judged against `../../../references/code-design-standard.md` §4 | Fowler, *Refactoring*; the Pragmatic Programmer's DRY |
| cross-task-coherence | Only a whole-delta reviewer can see this: abstractions that disagree between tasks, logic duplicated because each task saw one slice, a task that quietly did more than its title | — |
| external-surface-grounding | Every call into a surface the author does not own — HTTP API, SDK package, MCP tool, CLI flag, a sibling team's contract — carries a grounding citation. Missing on the first four is fatal; missing on a sibling contract is important; two tasks calling the same surface with conflicting shapes is important | — |
| principles-conformance | Does the change violate a falsifiable clause of the repo's `PRINCIPLES.md`? Scored only when that file exists, else `N/A` | the consumer's own `PRINCIPLES.md` |
| architecture-conformance | Does the diff follow the repo's ratified `ARCHITECTURE.md` rules and decisions — file placement, module boundaries and dependency direction, file size, CI stages? A violation is a finding whose fix is concrete: conform to the rule, or change the rule and its guard together. A violation of a ratified `ARCHITECTURE.md` rule is at least `important`, so the round sends it back to Build. Scored only for ratified rules in a document carrying `ratified-by: <name> <date>`; an absent document or unratified draft is `N/A`, with the draft advisory only | the consumer's own ratified `ARCHITECTURE.md` |
| deliberate-simplification | A shortcut taken on purpose, judged against `../../../references/code-design-standard.md` §7 | — |
| deletion-first | Every new abstraction, flag, config or extension point, and every new module or function that only forwards, judged against `../../../references/code-design-standard.md` §2–3 | — |

## Docs — five dimensions, plus deletion-first

| Dimension | What fires it |
|---|---|
| omission | A missing obligation or referent, judged against `../../../references/docs-standard.md` §1 |
| ambiguity | An unsupported absolute or a forking reading, judged against `../../../references/docs-standard.md` §2 |
| inconsistency | Contradicting passages, judged against `../../../references/docs-standard.md` §3 |
| incorrect-fact | A wrong citation, number or path, judged against `../../../references/docs-standard.md` §4 — open the source and read the cited span before scoring |
| missing-population | A number with no population, judged against `../../../references/docs-standard.md` §5 |
| deletion-first | New station text or contract machinery, judged against `../../../references/docs-standard.md` §7, severity by consequence as in the code lens's `deletion-first` |

**Polarity against the base.** This sharpens `inconsistency` for changed
against base, in the docs lens and so in the skill lens that scores these
five dimensions: every changed sentence carrying a polarity word is judged
against `../../../references/docs-standard.md` §6, severity by consequence.

<!-- gate: charter.plan-omission-narrow -->
**Plan omission, narrowed by the charter.** Omission on a `plan` is
exactly one thing: a task whose Files, Test or Risk line leaves the
implementer unable to start. A REQ left unrestated, a scenario left
unlisted, or a rationale left unwritten is complete, because the plan
charter's `must_not` column (`contract/manifest.yaml`,
`artifacts.plan.charter`) sends each of those to `spec`. Content
matching that `must_not` column found inside a plan scores
`inconsistency`, the finding citing the charter row and its `goes_to`.
A REQ missing task coverage is `cross-task-coherence` against the
spec's REQ list, scored by the code lens.
<!-- /gate -->

## Conformance and question lenses

| Dimension | What it asks |
|---|---|
| spec-conformance | Does the change do what the spec's `REQ-<n>` lines require, and only that? Every requirement is either satisfied, explicitly out of scope, or a finding. Unbuilt requirements and unrequired behaviour are both defects |
| design-conformance | Against `DESIGN.md` and the spec's UI flows: does every screen, state and transition the change touches exist in the design, and does a user reach it and get back out? `N/A` with the reason when there is no `DESIGN.md` |
| principles-conformance | As in the code lens, applied to any artifact type |
| user-judgment-leak | Fires when the change asks the user a technical question that existing decisions, project evidence, tests, or applicable external sources can answer. A question is legitimate only if it asks *what do you want*, *is this the behaviour you will see*, *is it done*, or for an unresolved outcome preference or missing authorization in consequence form. A class label, hard-to-swap choice, quality ceiling, or count of trade-offs alone does not justify a question. A question about spec quality, task splitting, or review verdicts is a leak and yields `NEEDS_REVISION`. This lens also checks that a material choice discloses the user consequences even when agent-decided, and that a pinned user choice is not asked again. A `Design decision` introducing a paid service, an account the user must hold, or existing data leaving the machine without explicit consent yields `NEEDS_REVISION`; an `agent-decided` mark settles it only when the option carries zero obligation, is reversible, and touches no existing data. |

## Skill lens

A `SKILL.md` or an agent contract is prose that an agent executes, so it is
scored on the five docs dimensions plus `user-judgment-leak` and
`deletion-first` (judged against `../../../references/docs-standard.md` §7), with two
sharpenings: a step whose input the reader must guess is an omission; a rule
subject to Loom's gate-registration contract that lacks its required
`<!-- gate: <id> -->` comment or registration is an omission too — an
unregistered gate is a mechanism nobody recomputes. Establish applicability
from the target's governing contract, not its location or use of the Loom
development workflow. Other skills retain their own requirements; substantive
usage errors and unmet acceptance conditions remain findings in either case.

## Plan lens

write-plan dispatches this lens on a draft plan before Build, with the
intent and the draft plan as ground truth. It scores `deletion-first` only:
can the same Acceptance lines be met with a simpler shape — fewer tasks,
files or mechanisms, or less code? Return each concrete smaller shape as one
`deletion-first` finding whose `fix` names the shape and the tasks or files
it removes. With none, return PASS with no findings and the note "no simpler
shape". The plan lens has no fix round.
