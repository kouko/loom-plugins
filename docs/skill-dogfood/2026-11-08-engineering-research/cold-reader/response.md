# Probe C — raw cold-reader response

Scope: cold usability audit of the uninstalled skill, without execution or external queries. Only the target skill and its directly bundled files listed in `receipt.md` were read. No passing verdict is issued. Finding candidates below are advisory, not observed runtime failures.

## Fixed question: Is it self-contained (could you act without asking the author)?

Yes, for a bounded engineering question with an established task context. I can identify the question, select a method, inspect appropriate evidence, save a record using the bundled template, read it back, and return to the original task. The no-active-change destination lets me proceed without knowing Loom's full workflow. Evidence that cannot be obtained has an explicit inconclusive exit. The authorization boundaries are sufficiently clear for this audit reader to avoid treating research as permission to install, publish, contact people, or advance a user decision.

I would not need to ask the author how to conduct the ordinary procedure. Two boundaries remain open to interpretation: when a small factual lookup becomes a skill invocation, and whether build failures outside the expressly named stages belong to the trigger scope. These affect routing and the obligation to retain a record, rather than preventing the procedure after invocation.

## Fixed question: Which requests trigger it—give 2 you're unsure about?

Clear triggers include:

- “Before we choose this integration, check whether its installed version supports the capability we need.”
- “The build has failed three times despite the documented configuration; identify which assumption is wrong before we keep changing it.”
- “Compare these feasible implementations against our latency and compatibility constraints before committing the plan.”

Two uncertain requests:

1. “Does version 4 support feature X? This determines whether we keep the current design.” This may be a one-page official documentation lookup, but its impact is consequential. The description suggests invocation; the routine-lookup exclusion may suggest otherwise. I would lean toward invoking because the decision impact is explicit, but another reader could reasonably treat this as routine.
2. “Production started failing after yesterday's upgrade; investigate the compatibility assumption before we decide what to change.” This fits the capability/version/compatibility sentence and the diagnosis method, but it is neither intent/spec/planning nor a failure during build. I would lean toward using the capability while preserving the owning incident task, but its description does not explicitly settle that scope.

## Fixed question: Is each mode/procedure executable as written?

The skill has one main procedure and a selectable method catalog, rather than formal modes.

| Procedure or method | Can I execute it from these files? | Practical limits |
| --- | --- | --- |
| Premise and evidence checks | Yes | Requires the actual conversation/artifacts; unavailable facts can be reported. |
| Documents, implementation and history inspection | Yes | Repository tracing and revision requirements are explicit. Inaccessible source has a defined partial-source outcome. |
| Hypothesis-driven diagnosis | Yes | It supplies hypotheses, distinguishing observations and disconfirmation; the actual task supplies the concrete failure. |
| Feasibility spike | Yes | Learning target, stopping condition and authorization limits are explicit. |
| Trade study | Yes | Project-specific criteria precede comparison; no invented scoring is required. |
| Profiling/benchmarking | Yes, with ordinary measurement competence | Workload, matched conditions, commands, versions and variability are specified. It is guidance, not a profiler manual. |
| Controlled comparison/A/B experiment | Yes for a bounded offline comparison; conditional for online work | Online sample size and bias checks require experiment-design knowledge absent from the bundle. The procedure allows stopping inconclusively if the necessary resources or knowledge are unavailable. |
| Targeted expert inquiry | Yes through preparation | Sending the inquiry requires user authorization; this is an intentional boundary, not an execution defect. |
| Existing-evidence sufficient/inconclusive branches | Yes | Both retain a record and return with limitations. |
| Optional structural representation | Yes | Selection, evidence labels, readback and unavailable-renderer fallback are specified. |
| Record creation/update/revalidation | Yes in a normal single-writer task | Paths, metadata, continuation versus revalidation, and no-write fallback are specified. The meaning of an active change depends on the owning context. |
| Return to owning task | Yes with existing context | The skill preserves authorization instead of defining the owning workflow itself. |

No missing required operational step rose to a universal blocker in this read. I did not run any of these procedures, so this is a readability assessment, not behavioral verification.

## Fixed question: Which terms are undefined?

- **Loom**, **station**, **active change**, **change-id**, and **human decision point** are not formally defined in the bundle. The context implies an existing workflow and its current unit of work. The fallback location and instruction not to invent a goal make this survivable for a reader outside that workflow. An unfamiliar reader could use the fallback rather than confidently identifying a current change.
- **Consequential**, **sufficient support**, **adequate verification**, and **routine lookup** have no objective threshold. The first three are reasonable judgment terms for a general research capability; “routine lookup” is more consequential to usability because it decides whether the retention contract activates.
- **Time-boxed**, **spike**, **guardrail measures**, **allocation unit**, **sample size**, and **bias checks** are not explicitly defined. Method descriptions partially explain their intent. The online-experiment terms assume relevant prior competence; the text does not prescribe a statistical design.
- **Flat metadata** is illustrated by the template, so the example supplies a usable definition even without prose explanation.
- **Frozen trial records** has no local marker or detection rule. I read it as an instruction to respect an existing explicit boundary; it does not require inventing one or searching unrelated trial history.

## Fixed question: Separate confirmed ambiguities from subjective style; quote exact relevant text and path/section, explain practical ambiguity and suggest edit class (do not edit).

### Advisory candidate C1 — routine lookup versus consequential question

Location: `input/engineering-research/SKILL.md`, frontmatter description and numbered step 3.

Exact text:

> “Use when capability, version, compatibility or feasibility assumptions could change an engineering decision.”

> “Routine lookups do not require this capability; once invoked, retain the bounded research record required below.”

Confirmed textual ambiguity: the same small lookup can satisfy both descriptions. The text does not say whether “routine” describes low effort, low decision impact, or absence of uncertainty requiring investigation.

Practical effect: two competent readers can disagree about whether to invoke and therefore whether to retain a Markdown record. It does not block an explicitly invoked skill.

Suggested edit class: trigger-boundary clarification, ideally one short example distinguishing a low-impact lookup from a simple but decision-critical check. No added mandatory research step is needed.

### Advisory candidate C2 — stage-limited trigger versus broader question-limited trigger

Location: `input/engineering-research/SKILL.md`, frontmatter description; `references/research-methods.md`, diagnosis row.

Exact text:

> “Resolve consequential evidence gaps during Loom intent, spec or planning, and contradictions or repeated failures during build.”

> “Use when capability, version, compatibility or feasibility assumptions could change an engineering decision.”

> “Behavior contradicts expectations or attempts repeatedly fail”

Confirmed textual ambiguity: the first description sentence names stages while the second and diagnosis method express a general engineering-question criterion. The text does not explicitly state whether the named stages bound use or exemplify common use.

Practical effect: incident diagnosis or maintenance outside build may be routed differently by different readers. Once invoked in such a task, the body offers a workable procedure and preserves the task's authorization.

Suggested edit class: scope clarification in the description; state whether use outside the named stages is included. This is a product-scope choice, not a demonstrated inability to research.

### Nonblocking prerequisite, not a confirmed defect

Location: `input/engineering-research/references/research-methods.md`, controlled comparison row.

Exact text:

> “Online experiments need an appropriate allocation unit, sample size and bias checks.”

The bundle does not teach how to determine these. A novice cannot design a valid online experiment from this sentence alone. However, a general engineering skill may reasonably assume method competence and the instructions explicitly permit an inconclusive record. I therefore do not elevate this to a mandatory addition. If novice online experimentation is an intended audience, an optional design checklist or prerequisite note would be the edit class.

### Subjective style observations — not findings

- The method catalog and evidence table are dense but sufficiently organized for a technical reader. Shorter prose would be a preference, not a demonstrated usability repair.
- “Consequential” and “sufficient” require judgment. Replacing them with arbitrary source counts or quotas would reduce the useful proportionality of the procedure.
- A glossary for Loom vocabulary could help unfamiliar readers, but the fallback and preservation rules already allow bounded action without asking the author.
- Optional version metadata is not a defect established by these files. I used no external packaging convention to judge it.

## Overall limitations of this response

This audit establishes only what one cold reader can infer from the five files. It does not establish automatic routing frequency, record-writing success, external research quality, statistical competence, or any host/install behavior. No external links were opened, no implementation was changed, and no research procedure was executed.
