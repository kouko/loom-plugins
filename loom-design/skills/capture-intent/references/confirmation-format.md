# Ready confirmation layout

Read only at the confirmation composer after required facts are settled.
If a required fact is missing, return to `confirmation-template.md` and stop
before confirmation preparation; the layout and ready examples do not apply.
The grounding and interview rules remain in `confirmation-template.md`.

Use five sections in this order, translating headings and replacing bracketed
guidance with only necessary, evidence-backed content. A brief sentence can
suffice for a section; no paragraph or filled purpose/direction/impact/benefit
slot is required. Keep critical scope, authorization, constraints, consequences
and required questions even in a short reply:

```markdown
## Background and current direction
[Known project or function context connected to this request; broader direction only when evidenced and needed.]

## Current problem and impact
[The supported problem or limitation; include affected people, situation and impact as needed and evidenced. Define necessary unfamiliar terms by their role.]

## What changes
[Wanted behavior and its difference from today; include a useful diagram checked for alignment here.]

## Scope and acceptance
[Observable completion conditions and source-scoped preservation/exclusion boundaries.]

## Please confirm
[Requirement scope and the applicable consent branch below. Ask the necessary question and wait.]
```

Keep the whole public reply for a ready confirmation inside these five sections,
excluding private prefaces and postscripts. Required WARN notices, cost/egress,
one-way-door consequences, principles and carried details belong in the applicable section.

Invoke `loom-workflow:loom-visualization` before composing a diagram when available.
For a before/after flow, read its `templates/02-linear-steps.md` and use
"Reproduce the titled comparison" to generate both complete outer frames,
with titles inside and unverified changes labeled expected. Preserve actual
steps and branches. Generate with width-aware tools and run final alignment
on the complete composition, including titled frames; invoking the skill
alone does not load its template.
If the optional skill is unavailable, use verified host tools or readable
table/text fallback. A wording correction needs no flowchart.

Honor a prior publication hold or opt-out until the user explicitly lifts it.
Under that restriction, confirmation covers requirements only; omit the default grant.
Otherwise retain the normal automatic-publication default.
Disclose automatic publication, opt-out and the separate merge decision in the same yes when publication is enabled.
Explain, when publication is enabled, that only after review AND publication checks pass does yes authorize
BOTH uploading the change branch (non-forced push) AND opening a pull request ready for review,
with opt-out available anytime before publication and a separate merge decision.

When an illustration is needed, read the relevant Invoice currency correction
or Filtered CSV export section in `confirmation-examples.md`. Adapt information
connections only; example facts apply only to their stated case.
