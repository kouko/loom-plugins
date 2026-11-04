# Ready confirmation layout

Read only at the confirmation composer after required facts are settled.
If a required fact is missing, return to `confirmation-template.md` and stop
before confirmation preparation; the layout and ready examples do not apply.
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

## Ready examples

Adapt only the information connections, never the case facts. Read the applicable
example below before composing; use the five-section layout above for other cases.

## Invoice currency correction

Context: accounting staff export invoices; the supplied priority is customer-setting isolation with the current format retained. Exports sometimes borrow the previous customer's currency. Amounts can differ, format stays unchanged, and existing files must remain untouched. The user explicitly asked to capture requirements only and not publish.

Good:
> ### Background and current direction
> The accounting team exports invoices. The stated priority is to isolate customer settings while preserving the export format.
>
> ### Current problem and impact
> An export sometimes uses the previous customer's currency setting, so the invoice shows the wrong currency.
>
> ### What changes
> Use the invoice customer's own currency setting. The comparison shows the reported failing case and the expected correction:
>
> ```text
> ┌──────────────────────────────┐  ┌──────────────────────────────┐
> │    Before (reported bug)     │  │        Expected after        │
> ├──────────────────────────────┤  ├──────────────────────────────┤
> │  ┌────────────────────────┐  │  │  ┌──────────────────┐        │
> │  │     Export invoice     │  │  │  │  Export invoice  │        │
> │  └────────────────────────┘  │  │  └──────────────────┘        │
> │               │              │  │            │                 │
> │               ▼              │  │            ▼                 │
> │  ┌────────────────────────┐  │  │  ┌──────────────────┐        │
> │  │ May use prior currency │  │  │  │ Use own currency │        │
> │  └────────────────────────┘  │  │  └──────────────────┘        │
> │               │              │  │            │                 │
> │               ▼              │  │            ▼                 │
> │  ┌────────────────────────┐  │  │  ┌──────────────────┐        │
> │  │     Wrong currency     │  │  │  │ Correct currency │        │
> │  └────────────────────────┘  │  │  └──────────────────┘        │
> └──────────────────────────────┘  └──────────────────────────────┘
> ```
>
> ### Scope and acceptance
> Check exports for customers with different currencies. Keep the format unchanged and existing export files untouched. Amounts may legitimately differ between exports; identical amounts are not required.
>
> ### Please confirm
> Your confirmation covers these requirements only. You asked not to publish;
> I will keep that restriction unless you explicitly lift it.
> Is that the correction you want?

Bad:
> Fix currency profile. All future invoice amounts will be identical; regenerate every existing export.
> Your yes also permits publication despite your restriction.
> Keep every existing datum untouched and prohibit changes to how customer settings are entered or stored.
> No per-invoice inspection will be needed for any reason.

The bad reply hides the setting's role, broadens named export-file preservation to all data, invents method restrictions, and overrides existing publication restrictions. The good diagram illustrates the failing path, not every export; a result boundary does not ban an unrequested internal fix method. When the request supplies checking for wrong currency, preserve that reason: correcting currency does not eliminate every other reason to inspect an invoice.

## Filtered CSV export

Context: accounting staff inspect filtered invoices; the supplied direction is offline use of that same result. They request CSV export of the current filtered result, with invoice number, customer, currency and amount columns, retaining current permissions.

Good:
> ### Background and current direction
> Accounting staff inspect filtered invoices. The stated direction is to make that same result available for offline accounting.
>
> ### Current problem and impact
> They currently cannot download the filtered result as a CSV file.
>
> ### What changes
> Add CSV export for the current filtered result.
>
> ### Scope and acceptance
> The download uses the current filtered result, with invoice number, customer, currency and amount columns. Existing access permissions stay unchanged.
>
> ### Please confirm
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Is that the capability you want?

Bad:
> We are modernizing the entire accounting platform. Approve a background export service and a new permission model.
> There is no CSV download, so there are no download actions at all.

The bad reply invents a project direction and implementation decision, and expands the absence of one capability into the absence of all downloads. The good reply retains the supplied CSV qualifier and permission boundary.
