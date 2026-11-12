---
name: design-research
description: |
  Resolve consequential evidence gaps about user problems, usage context, outcome priorities, behavior alternatives or architecture decisions. Return bounded findings to the design task; adequate evidence needs no new study.
---

# Design research

Use enough evidence to support the pending design decision, preserving the
user's established outcome, decisions and authorization. This is an on-demand
capability, not a station or an additional confirmation point.

Acquire new evidence only through online research and dialogue with the current
user; use supplied existing materials as context. Do not recruit or contact
other participants, collect survey responses, convene groups or workshops,
conduct field observation, operate a product walkthrough, build or test a
prototype, run participant usability/accessibility tests, or run experiments
or benchmarks. These activities are outside this skill, not options awaiting
an authorization question. Published studies of them may be read and attributed;
reading a study does not mean conducting it.

## Bound the question

Identify what decision could change and the missing evidence. Inspect the
conversation, supplied artifacts and existing research first. Reuse adequate,
applicable evidence; routine facts and immaterial uncertainty need no new
investigation. An invocation still retains its bounded finding as described
below. Do not reopen settled preferences or impose an interview quota.

Own questions about affected people, workflow, outcome priorities, behavior
options and design-owned architecture tradeoffs. Classify by the question,
not the station or whether code appears in it. Architecture research may inspect
technical sources to assess boundaries and consequences. A question about an
implementation's actual capability, compatibility, execution feasibility or
security controls belongs to engineering: separate it from the design question and identify a
bounded handoff for the host's code-owned research skill selection by skill name
at the task boundary. Do not relabel it design, read another plugin's internal
files or automatically delegate. Reuse existing applicable records for mixed
questions rather than repeating research.

## Choose the smallest useful investigation

After reuse, choose only an approach that can resolve the consequential gap.
Use these reasoning aids when useful, not as mandatory phases or a checklist:

| Pending question | Smallest useful source/dialogue approach |
|---|---|
| What problem or progress matters? | Separate problem from solution (Double Diamond); ask about a concrete past/current episode, desired progress, barriers and alternatives (Jobs to Be Done). |
| Which option serves the outcome? | Connect outcome, need and option (Opportunity Solution Tree reasoning); label unsupported needs/links as hypotheses, not validated opportunities. |
| Which premise could reverse the choice? | Identify the important weakly supported assumption; seek supporting and contradicting sources or a current-user fact, not an experiment. |
| Where might a handoff fail? | Describe steps, roles and exceptions with the user (journey/service-blueprint reasoning); a map is a described workflow, not observed performance. |
| Which quality or architecture consequence matters? | Ask what should happen under a concrete condition (quality-scenario reasoning inspired by QAW/ATAM); no workshop, formal evaluation or runtime proof is implied. |
| Does usability/accessibility guidance or a reported improvement apply? | Read original guidance/studies; compare population, task and conditions with the described design, without claiming a local test, audit or causal improvement. |

Frameworks supply questions and organization, not evidence or required outputs.
The quality-scenario prompts adapt the Quality Attribute Workshop (QAW) and
Architecture Tradeoff Analysis Method (ATAM); they do not execute those formal
methods. Use a plain focused question or source comparison when it is sufficient.

Inspect supplied workflow descriptions, observations, feedback and architecture
documents relevant to the gap. Where external evidence matters, read original
studies, official documentation or applicable firsthand reports. Retain the
inspected source's population, context, date/version and transfer limits. Search
results and inaccessible sources are leads, not inspected evidence; reconcile
contradictory accounts against their conditions instead of averaging certainty.

Ask the current user only for a missing preference or fact that cannot be
resolved independently and would change direction. Use neutral questions about
concrete experience; do not lead them toward the preferred solution or ask them
to decide technical matters answerable from evidence. Separate source claims,
user accounts/preferences, inference and unknowns. Current-user dialogue may
establish that person's stated needs, not behavior or demand across a population.
Do not invent participants or fill absent population evidence with simulated
answers. A reported preference is not observed behavior; inference is neither
consent nor feasibility evidence. Stop when support is sufficient; otherwise
return the consequential unknown, even when resolving it needs excluded work.

When proposing or materially restructuring an important design solution,
actively check for a smaller alternative that preserves the same confirmed
outcomes and mandatory constraints, including applicable correctness, security,
accessibility and compatibility requirements. Compare keeping the current
approach, narrowing user steps or roles, removing unnecessary elements, or
combining overlapping responsibilities where applicable; do not require a quota
of alternatives or deletion. For this and other material choices, identify
credible alternatives, including the current approach where viable. Choose
common criteria relevant to the outcome: for
example affected users' effort, accessibility, reversibility, operational
burden or architectural boundaries. Separate mandatory constraints from
preferences and source-supported facts from inference and unknowns. Apply the
same conditions and criteria to alternatives; no fixed matrix, dimension count
or numerical score is required. A user's preferred option is a preference,
not proof that it performs better. Support every material nested choice
separately; evidence for an overall architecture does not settle a component
choice. Disclose decision-critical unverified context before recommending. If a
preference reverses with an unknown condition, give conditional alternatives or
leave it unresolved; investigation tools do not establish the target caller,
workflow or runtime. Missing comparative evidence does not prove superiority.
Explain the smaller shape and burden removed, or the concrete reason complexity
is necessary, in the retained findings and decision impact. Revisit research
only when a consequential unresolved premise could change this comparison;
stop with adequate support or return the explicit unknown when permitted inquiry
cannot settle it. No fixed rounds are required; routine facts and reuse of
adequate evidence still return directly.

## Retain and continue the conclusion

Use [the self-contained research template](templates/research.md). Every
invocation creates or updates a Markdown record, including inconclusive work
or reuse of sufficient evidence. Use existing project-local research paths:
`docs/loom/<change-id>/research/<sequence>-<topic>.md` for an active change,
otherwise `docs/loom/research/<YYYY-MM-DD>-<topic>.md`. Read existing records
before choosing the next unused sequence or a collision suffix; do not invent
an intent to obtain a directory. Resolve links from the saved record's directory.

Split independently answerable questions. For the same question and conditions,
read and update its existing record's findings, conclusion, limitations and
`updated` date, preserving `created`. A follow-up challenge calls for reassessing
support; it is not new factual evidence or an instruction to agree. Before
delivering a changed recommendation, update the matching saved conclusion and
explain the evidence or reasoning change. Explicitly withdraw an unsupported
earlier recommendation when necessary; do not fabricate a justification.
When conditions materially change, preserve the earlier decision's basis and
create a linked revalidation under the new conditions. Respect frozen records
and explicit no-edit boundaries.

Keep flat metadata: `title`, `type: loom-research`, `status`, `created`, `updated`
and `tags: [loom/research]`; add `change` only for a known active change.
Dates use YYYY-MM-DD. Status is `in-progress`, `concluded` or `superseded`;
concluded may mean the question remains unsettled, not acceptance or certainty.
Retain source paths/URLs, inspected content and relevant conditions, commands
and actual results for measurements, decision impact and limitations. Summarize
evidence rather than copying private documents or complete transcripts.

Before reporting completion, read back the saved substantive question,
conditions, evidence, findings and limitations; inspect changed content and
affected claims for a longer update. Verify local Markdown targets identify
the intended evidence. File existence, a header or a successful write alone
does not verify content. If saving is prohibited or unavailable, return an
explicitly unsaved draft and identify the missing retained record.

## Return to design

Return findings, the actual record path (or unsaved status) and remaining
material uncertainty to the original task. Preserve confirmed goals, user
decisions and scope. Research does not grant consent, establish implementation
feasibility without evidence, ratify documents or advance a human decision
point. Resume only work already authorized by the owning task.
