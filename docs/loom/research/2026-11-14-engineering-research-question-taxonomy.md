---
title: "Question classification for a single engineering-research entry"
type: loom-research
status: concluded
created: 2026-11-14
updated: 2026-11-14
tags:
  - loom/research
---

# Question classification for a single engineering-research entry

## Question and scope

The user prefers a single entry. Are external research, implementation investigation
and execution verification an adequate classification, or are important situations missing?

This refines the [industry tools assessment](2026-11-14-engineering-research-evidence-modes.md).
The single-entry preference is user-decided. The classification below is an
agent-proposed synthesis, not an industry standard, ratified design or implemented
dispatcher. No runtime skill, test, manifest or installation is changed.
Local source baseline: `3b1a9972644517911454530dc1876f88525b1f37`.

## Method and rationale

Compare primary engineering-method guidance with the existing research contract,
its thirteen evaluation-selection rows, six retained framework-trial prompts and
selected historical research records. Test the proposed distinctions against
mixed and misleading cases on paper. This is manual analytical mapping, not a
new blind actor experiment, a frequency survey or a measured routing benchmark.

Initial English/Japanese queries explored question/method distinctions. Primary
method sources, rather than general product lists, resolve this question. Read
the relevant substantive sections of the sources below. No repository-behavior
claim about a new external tool is made, so no new tool source audit is needed.
Stop when the framework distinguishes decisions requiring different evidence,
handles mixed questions and states its boundaries without requiring a larger taxonomy.

## Findings

### The previous three names mix different classification dimensions

| Previous label | What it mostly identifies | Counterexample |
|---|---|---|
| External research | Evidence location / discovery activity | Upstream source outside the project still needs connected implementation inspection |
| Implementation investigation | Research object / a source-inspection activity | The same local code may support explanation, risk assessment or a comparison |
| Execution verification | A method combined with a confirmation purpose | Running code may instead diagnose a failure, measure throughput or test a causal hypothesis |

They remain useful shorthand for available activities. They should not be the
complete, mutually exclusive list of questions. In particular, verification
does not always require new execution: NASA's verification guidance explicitly
includes analysis, demonstration, inspection and testing. An existing valid run
can also settle a completion claim without rerunning it.

### A practical question catalog: eight distinguishable purposes

These are prompts for choosing evidence, not eight mandatory workflows or a
closed enumeration. A question may have a primary purpose and a consequential
secondary question; do not force it into one bucket or apply every row.

| Purpose | Plain question / expected answer | Evidence and stopping condition | Common overclaim to prevent |
|---|---|---|---|
| 1. Discover and understand facts | What exists, how does it work, what changed, what options are available? | Applicable documents/source/history and an explicit scope; stop when the requested fact, mechanism or bounded inventory is supported | A few examples are not all options or representative industry prevalence |
| 2. Explain causes or past decisions | Why did this fail, or why was this design chosen? | Competing explanations and distinguishing observations for failures; contemporaneous decisions/discussions for rationale; stop at supported explanation or explicit unresolved hypotheses | Code behavior or a commit's timing does not establish the author's intent; symptom relief is not root cause |
| 3. Compare and recommend | Which approach fits our constraints and why? | Credible alternatives, common relevant criteria, support and recommendation-changing unknowns; stop at a supported or conditional recommendation | Capability, popularity or fewer tools do not establish superiority |
| 4. Establish feasibility | Can this work under these particular constraints? | Applicable guarantees, implementation evidence or the smallest permitted prototype; stop at a bounded yes/no/conditional result | A happy-path prototype is not production readiness or comprehensive conformance |
| 5. Assess prospective impact and risk | What could change or fail if we do this, and how would we recover? | Dependencies, interfaces, trust/failure boundaries, scenarios and mitigations; stop when decision-relevant impacts and residual unknowns are identified | A plausible threat is not a reproduced vulnerability; a static reference list is not complete runtime impact |
| 6. Measure or estimate magnitude | How fast, how much, how many, how expensive, or how uncertain? | Defined quantity, scope/denominator, workload, observations or an explicit estimation model; stop with result, uncertainty and validity limits | A timing value is not quality; tokens are not money; estimates are not measurements |
| 7. Assess a change's causal effect | Did this change cause the improvement or regression? | Matched counterfactual/comparison, controlled intervention where warranted, confounder checks and outcome measures; stop at a bounded causal conclusion or explicit insufficiency | Before/after, activation frequency or unequal task timings do not establish causal improvement |
| 8. Check a claim against requirements or evidence | Does this meet the stated condition, did this actually run, does the cited evidence support it, is the old result still applicable? | Stated criterion plus applicable artifact/receipt/content inspection or execution; stop at supported/not-supported/unconfirmed with exact scope | Passing a process or reference-existence check does not prove the intended outcome or grant acceptance/publication authority |

The exact number is a design choice. Eight preserves several consequential
distinctions that a very broad catalog can hide: feasibility versus conformance,
measurement versus causal effect, and diagnosis versus recommendation. Split a
subtype further only when it changes evidence, failure handling or stopping rules.
No source inspected prescribes this exact eight-item catalog.

### Why these distinctions have practical support

| Primary source inspected | Relevant distinction | Limit of applying it here |
|---|---|---|
| [Google SRE troubleshooting](https://sre.google/sre-book/effective-troubleshooting/), Theory and Diagnose | Diagnose by comparing hypotheses with observations or controlled changes; check confounders | Supports purpose 2, not an all-purpose research taxonomy |
| [NASA decision analysis](https://www.nasa.gov/reference/6-8-decision-analysis/), process description and alternative evaluation | Compare alternatives using decision criteria; investigate uncertainty when it could change the ranking; scale rigor | Supports purpose 3 and proportionality; no mandate to adopt NASA process artifacts |
| [Microsoft feasibility spikes](https://microsoft.github.io/code-with-engineering-playbook/design/design-reviews/recipes/engineering-feasibility-spikes/), introduction and feedback loop | Bounded learning addresses technical unknowns before full engineering commitment | Supports purpose 4; not a requirement to prototype when existing evidence suffices |
| [OWASP threat modeling](https://cheatsheetseries.owasp.org/cheatsheets/Threat_Modeling_Cheat_Sheet.html), process and system modeling | Examine what can go wrong using system/data-flow/trust understanding | Supports the security subtype of purpose 5, not complete coverage of all operational risks |
| [Brendan Gregg active benchmarking](https://www.brendangregg.com/activebenchmarking.html), summary and active benchmarking | Inspect what a benchmark is actually measuring and its limiting factor | Supports purpose 6's validity checks; not a requirement to run hours-long benchmarks for every question |
| [Microsoft trustworthy experimentation](https://www.microsoft.com/en-us/research/articles/patterns-of-trustworthy-experimentation-pre-experiment-stage/), hypothesis/metrics and bias | Effects need suitable hypothesis, outcome measures, allocation and bias consideration | Supports purpose 7; production user A/B machinery is not compulsory for local deterministic questions |
| [NASA verification](https://www.nasa.gov/reference/5-3-product-verification/), Methods of Verification | Analysis, demonstration, inspection and tests can establish specified conformance | Supports purpose 8; source inspection still cannot establish a historical runtime event |
| [NASA validation](https://www.nasa.gov/reference/5-4-product-validation/), process activities | Intended use and operational environment matter separately from specified conformance | Flags usefulness as distinct from test pass; Loom user acceptance and design ownership remain unchanged |
| [Microsoft decision records](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record), introductory and record sections | Historical context, alternatives and reasons are recorded evidence; changed decisions link to earlier ones | Supports historical-rationale handling; does not require a new ADR for every research note |

The synthesis is supported by differences between these methods, not by an
industry-wide consensus about category names. Historical explanation and causal
effect evaluation overlap in reasoning, but the latter explicitly requires a
comparison against what would have happened without the change. Knowing why a
specific failure occurred is not a population effect estimate.

### Choose evidence separately from the question purpose

| Dimension | What to retain when material | Why it cannot replace purpose |
|---|---|---|
| Source / object | Local code/configuration; upstream code; specifications; field reports; records; telemetry | The same source supports several different questions |
| Method | Inspect/retrieve; trace relationships/history; calculate/model; reproduce/prototype; benchmark/controlled comparison; authorized expert inquiry | A single method can contribute to several purposes; no fixed source or execution sequence |
| Conditions | Revision, installed version, environment, workload, relevant time and freshness | Correct evidence for another condition may not answer this question |
| Authority | Read/write, execution, cost, transfer and decision ownership | Classification cannot grant permission or replace the owning workflow |

These are reasoning aids using existing record sections, not proposed required
metadata or a new state store. Sources are not a hierarchy of increasing quality:
the right source depends on the exact claim. Static analysis and new execution
are alternatives or complements, not steps every investigation must perform.

### Manual mapping against retained cases

The first six rows below use the actual [framework trial prompts](../../skill-dogfood/2026-11-08-engineering-research-frameworks/execution/cases.json).
This study reclassifies their questions; it does not rerun the actors or change
the old judgments. Other rows identify retained studies or explicitly constructed
boundary examples. Multi-purpose mappings are expected, not classification failures.

| Case / provenance | Primary purpose and material companion | Why the old three are insufficient |
|---|---|---|
| C01: exact TEST_ROOTS | 1 facts | No execution or external search needed |
| C02: reuse command construction without running tests | 4 feasibility + 3 recommendation | A tiny execution answers a constraint-specific possibility, not full suite verification |
| C03: foreign test roots / Git unavailable | 5 risk + 1 mechanism | Read-only code supports prospective failure scenarios; no incident need be manufactured |
| C04: unequal timing receipts allegedly prove a better workflow | 7 causal effect + 6 measurement validity | Actual runs still do not support the claimed causal improvement |
| C05: moving Markdown without losing provenance | 5 impact + 4 feasibility | Path calculation can resolve part of a migration question without moving anything |
| C06: source/tests allegedly prove current full CI success | 8 evidence sufficiency | Inspecting existing receipts can answer whether support exists; tests must not be fabricated |
| [ZIP recommendation incident](2026-11-12-recommendation-evidence-gap.md) | 2 diagnosis of recommendation drift; original task included 3 selection | The investigation is about a failed decision process, not simply archive implementation |
| [Launcher argument incident](2026-11-11-planning-launcher-argument-mismatch.md) | 2 diagnosis + 1 version/history | Reproduction identifies a local mechanism, not the cause of an unobserved remote incident |
| [Project/session count investigation](2026-11-11-skill-retro-project-count.md) | 2 diagnosis + 6 counting + 5 downstream impact | A correct count and a changed ranking are distinct conclusions |
| [CLI research-scoping assessment](2026-11-13-cli-design-research-scope.md) | 3 compare immediate change, bounded research and broad survey | Whether more research is worthwhile can itself be a bounded decision question |
| Current SourceAtlas/industry discussion | 3 applicable approach + 1 discovery | A list of tools does not choose a tool or justify an architecture |
| Constructed: why callback instead of polling was chosen | 2 historical rationale | Current code cannot reconstruct absent author reasoning; inspect contemporaneous records |
| Constructed: latest docs support X, installed release does not | 8 applicability + 1 facts | External/local distinction does not enforce version compatibility |
| Constructed: new skill loaded more often | 6 activation measurement; 7 if claiming quality improvement | Correct loading counts do not prove better research |
| Constructed: restart appeared to fix a timeout | 2 diagnosis | Recovery alone does not distinguish the causal hypotheses |
| Constructed: faster build also omitted tests | 6 measurement + 8 conformance | Lower elapsed time may reflect changed work, not a performance improvement |
| Constructed: migration can start but rollback loses writes | 5 risk + 4 feasibility | Feasibility of starting is different from safe cutover/recovery |
| Constructed: report links exist but sources do not support it | 8 semantic support | Reference validation is not claim validation |

This sample finds useful distinctions, but was selected by the author and includes
familiar development cases. It cannot establish exhaustive coverage, unbiased
classification accuracy or improved agent behavior. No percentage is reported.

### Situations that do not justify more question categories

- Security, performance, reliability, migration, architecture and compatibility
  are subject areas. A security question can ask about facts, risk, feasibility,
  cause or conformance; use its specialist method without making every domain a
  new top-level purpose.
- Historical tracing is a time/evidence requirement: describe what changed under
  purpose 1, explain a recorded rationale under 2, or evaluate an effect under 7.
  It does not need a separate mandatory workflow for all Git-related questions.
- Contradictory sources and stale evidence affect support/applicability across
  purposes. Investigate why conditions differ, or leave the contradiction unresolved.
- Reuse, inconclusive results, insufficient access and sufficient evidence are
  possible outcomes across purposes, not extra problem types. Exhaustive source
  collection is not a stopping rule.
- A missing user preference, desired visible behavior or authorization goes back
  to the owner/user. Research can reveal consequences; it cannot decide consent.
  User research/product discovery and writing an implementation plan retain their
  existing owners.
- Formal closing review, acceptance and release approval retain their own workflow
  responsibilities. Research may check a factual premise without issuing their
  verdicts. Routine implementation tests do not all need a research invocation.
- Classification should be revisable when findings change the question. Prefer
  ordinary language over demanding that users label a purpose at intake. An
  unusual question should remain answerable without adding an enum member first.

## Decision impact

| Alternative | Benefit | Limitation / recommendation |
|---|---|---|
| Keep the previous three as an exhaustive classification | Short and easy to remember | Mixes dimensions; loses evidence obligations for selection, causal effects and risk |
| One entry, purpose-led questions with independently selected evidence methods | Distinguishes consequential proof requirements and supports mixed tasks | Recommended analytical model; eight examples are an open catalog, not mandatory labels |
| Expand to a fixed category for every domain/tool | Makes specialist names visible | Duplicates shared reasoning and creates overlapping routing; not justified |
| Keep broad current wording unchanged and defer | No new instructions or maintenance | Valid baseline; less concrete selection guidance |

Preserve the user's single entry. It should first identify the unanswered question
and the observation that could settle it. Use the purpose catalog only to select
the relevant reasoning/evidence requirements, and load specialist guidance only
when the question needs it. A one-line factual answer can remain small.

Before any skill rewrite, a bounded behavioral trial should challenge selection
and stopping behavior with mixed and negative cases: simple lookup, old execution
receipt, missing historical rationale, source/runtime discrepancy, feasibility
without full build, confounded performance claims, recommendation reversal and
inadequate release evidence. Compare supported conclusions and saved-record
consistency as well as overhead. The present manual mapping does not establish
that adding eight labels will improve the skill.

## Evidence and limitations

Sources above were actually opened, including substantive method sections rather
than only navigation/search excerpts. The Microsoft ADR page displays an access
banner, but the quoted subject matter was present in the returned public body;
no inaccessible remainder or authenticated access is claimed. Prior local reports
are historical evidence, not claims about current failure frequency.

The [current methods](../../../loom-code/skills/engineering-research/references/research-methods.md)
already include inspection/history, diagnosis, spikes, trade studies, benchmarks,
controlled comparisons and expert inquiry. The [evaluation guide](../../../loom-code/skills/engineering-research/references/evaluation-selection.md)
already covers thirteen question patterns; this proposal groups them rather than
inventing missing capabilities. No conformance to a standard, exhaustive industry
survey, new independent review or agent routing improvement is claimed.
