# Ready confirmation layout

Read only at the confirmation composer after required facts are settled.
The grounding and interview rules remain in `confirmation-template.md`.

Use five sections in this order, translating headings and replacing bracketed
guidance with natural paragraphs, lists or tables:

```markdown
## Background and current direction
[Relevant project or function purpose and current direction connected to this request.]

## Current problem and impact
[Who encounters what problem or limitation, in which situation, with its supplied impact? Define unfamiliar terms by their role.]

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
Follow its relevant diagram template: generate with width-aware tools and run
final alignment on the complete composition, including titled frames.
Use the titled-panel template for comparisons, with titles inside frames and
unverified changes labeled expected. Preserve actual steps and branches.
If the optional skill is unavailable, use verified host tools or readable
table/text fallback. A wording correction needs no flowchart.

Honor a prior publication hold or opt-out until the user explicitly lifts it.
Under that restriction, confirmation covers requirements only; omit the default grant.
Otherwise retain the normal automatic-publication default.
Disclose automatic publication, opt-out and the separate merge decision in the same yes when publication is enabled.
Explain, when publication is enabled, that only after review AND publication checks pass does yes authorize
BOTH uploading the change branch (non-forced push) AND opening a pull request ready for review,
with opt-out available anytime before publication and a separate merge decision.
