# Probe C: fresh cold-reader questions and answers

## Run receipt

- Scope: static reading of the raw, uninstalled candidate skill and its directly bundled files. No execution of the candidate, network access, installation, external reference opening, or additional agents.
- Requested model: gpt-6.1-sol, medium effort. Immutable server revision: unconfirmed. This receipt does not independently verify the effective backend model.
- This is a reading interpretation, not behavioral or runtime validation, and does not issue a global PASS.
- Prior protocol, reports, history, other outputs, and old versions were not read.

## Q1. Is the skill self-contained, and can you act without asking its author?

Yes, for selecting and conducting a bounded investigation within an already authorized task. The instructions identify the decision and evidence gap, specify source treatment, provide a record template and storage rules, and state when to stop. The bundled material supplies enough guidance to begin without contacting the skill author.

It is not a standalone tutorial for every specialist method. A reader who lacks security, statistical experimentation, or performance investigation competence might need to consult its cited references or acquire relevant expertise. That is domain competence, not evidence that the workflow is impossible to follow. The skill also deliberately needs task inputs: applicable project artifacts, constraints, a pending decision, and sometimes user authorization. Missing user preference is a reason to ask the user, not the author.

Supporting text: SKILL.md, step 1: “Ask only when an unresolved ambiguity would change the work's direction or requires a user preference or authorization”. SKILL.md, “Without an active change” supplies a storage fallback, so lack of Loom change metadata does not prevent useful work.

## Q2. Which requests trigger it? Give two uncertain requests.

Clear matches include checking a version-specific capability before a design choice, comparing feasible alternatives whose differences change a plan, investigating contradictory project behavior, and diagnosing repeated failed build attempts. A routine fact lookup by itself is explicitly outside its normal scope.

Two uncertain requests:

1. “What version of library X added streaming?” Alone, this reads as a routine lookup and probably does not trigger. If the answer controls whether the current integration can proceed, the same surface wording can represent a consequential evidence gap and should trigger. The missing distinction is task context, not an unintelligible trigger.
2. “Review this refactor for maintainability.” As an ordinary code review, it belongs to the owning review task. If a disputed maintainability claim or design alternative prevents the pending engineering decision, this capability can support a focused investigation. The text permits that support but does not replace review.

Exact scope cues: description: “Use when capability, version, compatibility or feasibility assumptions could change an engineering decision.” SKILL.md, step 3: “Routine lookups do not require this capability”. references/evaluation-selection.md:40: “Respect existing project criteria; this research does not replace the owning review station.”

I would resolve those borderline requests from the available conversation first. These examples do not establish a confirmed trigger defect or an observed routing failure.

## Q3. Are the procedures executable as written?

Yes as agent instructions for a research workflow, assuming appropriate artifact access and authorized tools. The progression is actionable: establish the question, test evidence relevance, select a proportionate method, obtain missing support, stop at a bounded conclusion, save and read back a record, then return to the owning task. Experiments have observable targets and stopping conditions. Inaccessible evidence and unavailable tools have explicit inconclusive outcomes.

These are not runnable scripts or complete specialized experimental protocols. For example, online experimentation still requires judgment about allocation and sample size. I have not run a research task, validated the links, tested the record schema, rendered a diagram, or established that a model follows these instructions in practice.

The two method-selection documents overlap, but I can read them consistently: research-methods.md selects evidence-gathering methods, while evaluation-selection.md adds question-specific assessment structure. “Reading, external research, and measurement are alternatives or complements, not mandatory steps in order” (SKILL.md, step 3) prevents a compulsory all-method sequence.

## Q4. Which terms are undefined?

- Loom, station, active change, intent, spec, and human decision point are not introduced as a complete host-workflow glossary. Their practical role is partly explained by the final section and record paths. An outside reader can use the no-active-change fallback, but cannot reconstruct Loom's entire lifecycle from this package. That lifecycle is not required to select a research method.
- ATAM is not expanded, although its row provides a usable scenario recipe and warns that this is not the full process (evaluation-selection.md:39).
- STRIDE is not expanded as its canonical acronym, but the intended security concerns are paraphrased in the same row (line 45).
- SEEMS is not expanded letter by letter, but its resilience prompts are provided (line 46).
- Allocation unit, guardrail measures, sample-ratio checks, and independent population evidence are specialist terms not fully taught here (line 44; research-methods.md, controlled-comparison row). A causal experiment may require domain competence beyond the short guidance.
- USE is explicitly expanded as utilization, saturation and errors (line 42). Service-level objectives are spelled out (line 48).

I do not treat missing acronym expansions alone as a practical ambiguity. I found no instruction whose next authorized step depended on asking the author to define one of these terms.

## Q5. How do you read conditional method choice for a simple problem?

Reading-only example: “Our installed v2.4 package is claimed to support feature F. Can the plan rely on it?”

I read this as one capability question. Start with applicable source/configuration/artifact inspection, matching the installed version and relevant flags. If that establishes only an implementation path and the decision depends on actual environment execution, add the smallest permitted feasibility check. Do not automatically conduct a trade study, security review, benchmark, diagram, or named-framework exercise. Record findings and the remaining distinction between implementation and execution.

Exact support: evaluation-selection.md:12–14: “A fact or completion claim can be settled by direct applicable evidence without a named framework. Reuse adequate evidence; do not turn every lookup into a trade study or force a method label, matrix, diagram or new experiment.” Line 36 supplies the direct-inspection row. This is an interpretation, not a completed investigation of any package.

## Q6. How do you read conditional method choice for a mixed problem?

Reading-only example: “Should we replace queue library A with B to reduce delays, while preserving compatibility and recovery behavior?”

The pending choice suggests a trade study as the primary assessment, using compatibility and recovery requirements as mandatory conditions and delay reduction as a measured criterion. If current delays have an unknown cause, diagnose or profile that distinct gap before attributing them to A. If the alternatives' performance difference remains decision-critical, use a representative matched benchmark. Examine migration/read-write paths and failure/recovery scenarios only to the extent those are consequential gaps in this actual change. The text does not require every listed framework.

If “what causes today's delays?” can be answered independently of “which queue should we adopt?”, retain a separate question record and link it from the comparison. If limited profiling is merely evidence for the same bounded choice, it can be a complementary method in the choice's record. This requires judgment about question scope but is not contradictory.

Exact support: evaluation-selection.md:30–32: “Choose a primary approach per independently answerable question. Add a complementary method only for a distinct consequential gap. A mixed question may need more than one method; unrelated questions retain separate records.” Lines 16–18 require mandatory conditions to be considered before weighted preferences. Relevant starting rows are lines 38, 41–43, 46–47.

No diagnosis, comparison, benchmark, migration test, or recovery test was executed for this example.

## Advisory finding candidates

No confirmed practical readability defect was found in this static pass. The following is an optional improvement candidate, not a failure or requirement to revise:

- Severity: informational.
- Category: domain-term accessibility / subjective preference.
- Prompt: “Choose an approach for architecture tradeoffs under load.”
- Expected: a reader can choose a bounded scenario assessment and understand the limits of a larger named process.
- Actual: the row gives an actionable recipe but leaves the acronym ATAM unexplained; a novice may need the linked reference for the method's full identity.
- Exact quote: “Concrete quality scenarios informed by ATAM” and “A few scenarios are not a completed ATAM; major cross-team decisions may need the full facilitated process.”
- Section/location: references/evaluation-selection.md, “Match the question to the approach”, line 39.
- Suggested edit class: optional first-use acronym expansion; no procedural rewrite.
- Qualification: this is not a confirmed blocker. The local instructions suffice for the bounded scenario reading, and specialist proficiency cannot be inferred from static readability.

## Files read

All paths below are relative to docs/skill-dogfood/2026-11-08-engineering-research-frameworks/input/new/engineering-research/:

1. SKILL.md — full file.
2. references/research-methods.md — full file.
3. references/source-policy.md — full file.
4. references/evaluation-selection.md — full file, numbered for exact locations.
5. references/structured-relations.md — full file.
6. templates/research.md — full file.

No cited external URL was opened. No files outside the allowed candidate tree were read for the assessment. This output file was created in the authorized cold-reader directory; the candidate was not edited.
