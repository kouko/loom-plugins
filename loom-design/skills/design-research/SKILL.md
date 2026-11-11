---
name: design-research
description: |
  Resolve consequential evidence gaps about user problems, usage context, outcome priorities, behavior alternatives or architecture decisions. Return bounded findings to the design task; adequate evidence needs no new study.
---

# Design research

Use enough evidence to support the pending design decision, preserving the
user's established outcome, decisions and authorization. This is an on-demand
capability, not a station or an additional confirmation point.

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
implementation's actual capability, compatibility or execution feasibility
belongs to engineering: separate it from the design question and identify a
bounded handoff for the host's code-owned research skill selection by skill name
at the task boundary. Do not relabel it design, read another plugin's internal
files or automatically delegate. Reuse existing applicable records for mixed
questions rather than repeating research.

## Choose the smallest useful investigation

Inspect the actual workflow description, observations, feedback, existing
product behavior or architecture documents relevant to the gap. Where external
evidence matters, read original studies, official documentation or applicable
firsthand reports. Record population, context, date/version and limits of
transfer. A reported preference is not observed behavior; an agent's inference
is neither user consent nor feasibility evidence. Search results and inaccessible
sources are leads, not inspected evidence. Reconcile contradictory accounts
against their conditions instead of averaging them into certainty.

Use a bounded walkthrough, existing observation, source comparison or permitted
prototype check when it answers the question. Ask only for a missing preference
or fact that cannot be resolved independently and would change direction.
Contacting people, collecting new personal data or running consequential
experiments requires the owning task's authorization. Stop when the decision
has sufficient support; report consequential unknowns when it does not.

For a material choice, identify credible alternatives, including the current
approach where viable. Choose common criteria relevant to the outcome: for
example affected users' effort, accessibility, reversibility, operational
burden or architectural boundaries. Separate mandatory constraints from
preferences and source-supported facts from inference and unknowns. Apply the
same conditions and criteria to alternatives; no fixed matrix, dimension count
or numerical score is required. A user's preferred option is a preference,
not proof that it performs better. Support every material nested choice
separately; evidence for an overall architecture does not settle a component
choice. Missing comparative evidence permits a tentative choice or unresolved
comparison, not a claim of demonstrated superiority.

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
