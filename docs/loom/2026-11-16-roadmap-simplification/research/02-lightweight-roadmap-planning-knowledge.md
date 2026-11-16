---
title: "Which compact planning knowledge should the roadmap skill contain?"
type: loom-research
status: concluded
created: 2026-11-17
updated: 2026-11-17
change: 2026-11-16-roadmap-simplification
tags:
  - loom/research
---

# Which compact planning knowledge should the roadmap skill contain?

## Question and scope

Identify small, directly usable planning heuristics that could improve the
quality of software roadmaps while preserving ordinary Markdown, selected
existing documents, optional creation and existing delivery authorization.
The user requested research, not implementation, publication or a new schema.
This is a local research draft; the reviewed skill and existing PR are unchanged.

Context: the 93-line [current skill](../../../../loom-workflow/skills/roadmap/SKILL.md)
already addresses goals, completion conditions, dependencies, minimum useful next
stages, estimates, evidence scope and execution boundaries. [Earlier research](01-roadmap-skill-ownership.md)
settled document ownership. This record does not reopen that decision.

## Method and rationale

Inspected the current skill and nine primary practitioner/official sources in
English and Japanese. Search engines supplied leads; findings below rely on
opened substantive pages, including IPA PDF section 3.1.13, printed pages 36-37
(PDF pages 41-42). No interviews, experiments, benchmarks or prototype trials
were conducted. No private finance excerpts were used.

Selection criteria: changes an actual planning decision; yields a short useful
answer; complements current instructions; works without population metrics or
team ceremonies; remains conditional when its source context does not transfer.
The six lenses are a synthesis for this skill, not a prescribed industry standard
or six mandatory questions that the user must answer on every invocation.

## Findings

### Proposed compact knowledge

| Lens | Direct instruction candidate | Increment over current skill | Basis |
|---|---|---|---|
| Intended improvement | State who benefits, what becomes possible or better, and what observation would support success. Reuse confirmed intent; never invent a numerical target. | Makes generic goals/completion conditions concrete; separates delivery from achieved benefit. | S1, S3 |
| Useful increments | Prefer the smallest end-to-end capability that can be used or checked independently. If foundational work or research must come first, name the capability it enables or consequential question it resolves. | Gives a splitting method beyond saying "smallest useful next stage". | S4; foundational exception is a local adaptation |
| Consequential uncertainty | Identify a weakly supported premise that could invalidate the next investment. Suggest a bounded evidence-gathering step only when its answer could change the decision. | Distinguishes unknowns that affect sequencing from a list of all unknowns. | S5 |
| Explain order | Compare relevant alternatives by contribution, evidence confidence, effort and real dependencies/constraints. State why the next stage precedes another or is deferred; retain unknown inputs. | Adds an auditable reason for ordering without mandatory scores. | S1, S6; qualitative adaptation is our recommendation |
| Appropriate detail and scope | Detail near-term work; keep distant stages provisional. Respect genuine deadlines and agreed spending/time limits; reduce optional scope rather than fabricate capacity or relax required quality. | Adds planning granularity and investment limits to existing estimate/commitment separation. | S2, S7 |
| Reconsider after evidence | Name the result or changed condition that would justify continuing, changing scope, deferring or stopping. Update only when that condition/evidence warrants it. | Makes plan maintenance responsive to learning, not just completion updates. | S1, S5; explicit stop wording is a synthesis |

These lenses guide reasoning; they do not require six new document fields,
separate ledgers, a scoring sheet, an interview or permission to run a study.
Detailed requirements and acceptance criteria remain with existing workflows.
Do not reopen settled intent or delay viable approved implementation to fill gaps
that cannot change the next decision.

### Conditional software-specific knowledge

For migrations, replacements and breaking changes only, identify affected
consumers/data, actual prerequisites, possible coexistence, safe exposure and
recovery limits. Record the decision needed before widening exposure or retiring
the old path. Do not promise reversibility of data changes, prescribe a universal
deployment pattern or design a migration inside the roadmap. Hand detailed design
and execution to the existing owners. S8 supports incremental replacement and
transitional costs; S9 supports staged exposure and recovery/data cautions.

Foundational security, reliability or infrastructure work may legitimately precede
visible features. Require a concrete outcome, constraint or blocker and a bounded
completion condition, not immediate user-visible delivery for every stage.
Avoid both speculative foundations and an absolute ban on infrastructure stages.

### Stress tests of the recommendation

- Known small repair: reuse the established problem and approved work; do not
  force a discovery exercise or new metrics. S5 explicitly limits risk-assumption
  prioritization in small, well-understood problem spaces.
- Technical enabler: a compatibility check or required data foundation can be
  a useful stage even before a visible feature. Say what it unlocks and why now.
- Fixed-date obligation: preserve the real date and mandatory scope. If capacity
  is unknown or insufficient, expose the conflict; do not silently reduce required
  safety/quality or turn an investment ceiling into a delivery guarantee.
- New unsupported feature idea: explain the intended improvement and the
  consequential premise before committing a large implementation phase.
- Old result without rerun: keep the attributed result and its limits. The new
  heuristics must not undo the recently repaired unknown-versus-unfinished rule.

## Evidence

All sources inspected on 2026-11-17. Guidance and practitioner reports support
plausible heuristics, not a measured causal improvement for Loom or all teams.

| ID | Inspected source and date | Relevant support and transfer limit |
|---|---|---|
| S1 | [GDS: Developing a roadmap](https://www.gov.uk/service-manual/agile-delivery/developing-a-roadmap), 2017 | Connect iterations to user value, objectives and progress measures; make priority explicit and revise intent as learning changes. Government service guidance also prescribes calendar periods; do not copy those periods as universal requirements. |
| S2 | [GDS: Planning in agile](https://www.gov.uk/service-manual/agile-delivery/planning-agile), updated 2026-03-31 | Near work deserves detail, distant work high-level planning; account for dependencies and genuine deadlines. Its suggested annual objectives and 6-12 month horizon are context-specific. |
| S3 | [Moore/Cagan: Changing How You Decide Which Problems To Solve](https://www.svpg.com/changing-how-you-decide-which-problems-to-solve/), 2022-09-23 | Reframe features/projects as problems and success measures. Product-company advice; useful for framing, not proof every engineering investment has direct business telemetry. |
| S4 | [IPA: Agile practice guide](https://www.ipa.go.jp/archive/files/000026849.pdf#page=42), 2013-03-19, section 3.1.13 | Describe who/what/why, satisfaction conditions and value-oriented splitting rather than screen/database layers. Story-level guidance is adapted to larger stages; its dated case adoption rates are not used as current evidence. |
| S5 | [Harry Vos/GDS: The value of testing riskiest assumptions](https://services.blog.gov.uk/2022/11/29/the-value-of-testing-riskiest-assumptions/), 2022-11-29 | Risk/evidence discussion helps uncertain exploration; the author explicitly says it has less value in small, well-understood problem spaces. Practitioner examples, not a controlled study. |
| S6 | [Intercom: RICE](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers), 2018-01-05 | Considers reach, impact, confidence and effort; recommends real inputs and permits dependency-driven ordering over score order. We retain prompts but do not adopt the formula or scales; this is a deliberate adaptation, not a finding that RICE is ineffective. |
| S7 | [Basecamp: Set Boundaries](https://basecamp.com/shapeup/1.2-chapter-03), page date not verified | Distinguishes an investment/time appetite from an estimate and narrows scope. Its team sizes and fixed cycles are Basecamp-specific; adopt the distinction, not its complete operating model. |
| S8 | [Fowler: Strangler Fig](https://martinfowler.com/bliki/StranglerFigApplication.html), 2024-08-22 | Incremental legacy replacement can deliver value/learning while old/new coexist; temporary architecture has costs. Legacy modernization guidance, not a universal rule against replacement. |
| S9 | [Microsoft: Safe deployment practices](https://learn.microsoft.com/en-us/azure/well-architected/operational-excellence/safe-deployments), page date not verified | Small staged releases, health-based continuation and recovery; stateful/data rollback can be difficult. Azure production guidance: extract relevant questions only, not Azure tooling, autonomous rollout or blanket new gates. |

## Decision impact

| Option | Planning depth | Added burden | Assessment |
|---|---|---|---|
| Keep current guidance / defer | Relies on model knowledge for concrete methods | None | Viable if document maintenance alone is sufficient; does not address the requested gap. |
| Add only outcome and useful-increment prompts | Improves framing and splitting | Very small | A viable smaller pilot; leaves ordering and learning decisions less explicit. |
| Combine six short lenses and conditional migration questions | Covers framing, splitting, ordering, uncertainty and adaptation | Small if applied selectively | Recommended candidate; reuse existing paragraphs instead of duplicating them. |
| Import complete frameworks and fixed templates | Broad terminology and procedures | High and context-sensitive | Not justified for the lightweight owner; additional mandatory machinery is unnecessary. |

Recommended candidate: refine the existing planning paragraph with compact
decision prompts and one illustrative software example. Keep source provenance
portable if incorporated into runtime guidance: do not cite this repository's
development record from a shipped skill. No new skill, parser, mandatory schema,
scheduler or recurring ceremony is needed. A bundled reference should be added
only if examples actually outgrow the short instruction, not preemptively.

Illustration (invented, not observed user/project data): an import roadmap can
start with one supported file type producing a usable result with clear failure
handling; broader format support can follow. If feasibility is genuinely unknown,
first resolve that specific premise. A successful technical check supports only
its tested scope, not adoption, user benefit or whole-stage acceptance.

## Limitations and open questions

- No variant has been implemented or behaviorally compared. The recommendation
  is a source-backed design proposal, not an improved skill or dogfood result.
- The proposed combination has not been established as universally superior;
  transfer from teams to individual coding agents remains unmeasured.
- Six lenses are reasoning aids, not a universal priority ordering. Dependencies,
  required fixes and genuine constraints may override apparent impact/effort.
- Quantitative outcome metrics may be unavailable. Describe observable success
  and unknown evidence rather than manufacturing baselines, targets or confidence.
- This record is uncommitted research only. It does not change the confirmed
  requirements, current reviewed content, acceptance, attestation or merge consent.
