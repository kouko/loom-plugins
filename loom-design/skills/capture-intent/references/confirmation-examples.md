# Optional confirmation illustrations

Read the primary `confirmation-template.md` first. Use only the relevant section
when an illustration is needed; these examples supply no facts for another case.


## Unknown date

Context: release notes show an incorrect date; only that date should change,
and the actual release date is unknown.

Good:
> The displayed release date is incorrect. I need the actual release date or a
> release record before correcting that date alone. What evidence or date can
> you provide?

Bad:
> I created an open engineering intent with needs-design: no. Confirm today's
> date as the fallback, then choose whether I should publish. Next I will run
> planning, build and closing-review. Is this plan technically correct?

The bad reply invents a date, serializes bookkeeping and adds a publication
choice and implementation judgment. The good reply asks only for a missing fact;
it is an interview, not a confirmation. The normal same-yes publication disclosure
belongs in the eventual confirmation after the required fact is established.

## Known correction

Context: release notes show an old date and make the latest release look outdated.
The user supplies the verified release date, 2 November; only that date may change.

Good:
> ### Background and current direction
> The release notes describe when the software shipped. This correction concerns the displayed release date.
>
> ### Current problem and impact
> The incorrect date makes the latest release look outdated.
>
> ### What changes
> Replace the displayed date with the verified 2 November.
>
> ### Scope and acceptance
> Check that this date is correct and the rest of the release notes remain unchanged.
>
> ### Please confirm
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Is that the correction you want?

Bad:
> ### Background and current direction
> The release notes describe when the software shipped. This correction concerns the displayed release date.
>
> ### Current problem and impact
> The incorrect date makes the latest release look outdated.
>
> ### What changes
> Replace the displayed date with the verified 2 November.
>
> ### Scope and acceptance
> Check that this date is correct and the rest of the release notes remain unchanged.
>
> ### Please confirm
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Is that the correction you want?
> The intent is open and engineering with no design needed. Standing-document
> checks passed. The current branch has no commits, both handoff lists are empty,
> and review defaults are unchanged. Next I will commit the intent, plan and
> implement; the intent commit message will follow the station's naming rule.

Both replies preserve identical facts, scope and necessary authorization. Only
the bad reply appends internal work inventory: its extra sentences add no help
understanding the correction or deciding what to authorize.

## Multiple problems

Context: a worker is whoever executes a background job. Jobs borrow another
job's worker-selection rule; failed jobs retry forever and block the queue.
Each should use its own rule and stop at its configured retry limit, preserving
successful jobs and the existing interface.

Good:
> ### Background and current direction
> Background jobs run work through workers. This change concerns their selection rules and configured retry limits.
>
> ### Current problem and impact
> Jobs borrow another job's selection rule; failed jobs retry forever and block the queue.
>
> ### What changes
> Each job should use its own rule for choosing who executes it, and failed jobs should stop at their configured retry limit.
>
> ### Scope and acceptance
> Check rule ownership and retry stopping separately. Successful jobs and the existing interface stay unchanged.
>
> ### Please confirm
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Is this the scope you want?

Bad:
> Fix dispatch profile and retry policy. Every job will always choose the same
> worker and produce the same result. Please also choose a new default-worker
> policy and approve the retry implementation before confirming.

The bad reply replaces explanation with labels, adds guarantees and turns an
unestablished edge case into an additional outcome choice.

## Repairing shorthand

Context: the user already explained worker selection as the rule choosing who
runs each job. The assistant called it "profile" without explanation; the user
asks for detail after reporting borrowed rules and inconsistent results.

Good:
> ### Background and current direction
> Worker selection is the rule choosing who runs each job. I used "profile" as shorthand for that supplied role, not a verified application object.
>
> ### Current problem and impact
> My shorthand omitted that connection. You reported that jobs borrow another job's rule and get inconsistent results.
>
> ### What changes
> The correction is to use each job's own selection rule.
>
> ### Scope and acceptance
> Check which rule each job uses. This alone promises neither the same worker nor identical results on every run.
>
> ### Please confirm
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Does that match your request?

Bad:
> I cannot explain profile because you never defined it. Tell me its exact
> meaning. I will require the same job to pick the same worker and return an
> identical result every time, and leave publication for another question.

The good reply repairs the assistant's wording using supplied context without
pretending to have verified an application object with that name. The bad reply
returns the omission to the user and strengthens the requested outcome.

## Interface boundary

Context: jobs randomly choose workers from their own eligible lists but sometimes
use another job's list. Random selection must remain, with no new interface.

Good:
> ### Background and current direction
> Jobs randomly choose workers from their own eligible lists. This correction concerns which list each job uses.
>
> ### Current problem and impact
> Jobs sometimes use another job's list.
>
> ### What changes
> Each job should randomly select from its own eligible workers.
>
> ### Scope and acceptance
> Check list ownership while preserving randomness and the existing interface.
>
> ### Please confirm
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Is that the change you want?

Bad:
> Confirm that every job always chooses the same worker, and that no functions,
> options, settings or commands may be added anywhere. Would you prefer a new
> interface for jobs with no list? Publication is off unless you separately opt in.

The bad reply contradicts randomness, expands an interface constraint into an
implementation prohibition, invents an additional scope choice and reverses the
publication default.

## Invoice currency correction

Context: accounting staff export invoices; the supplied priority is customer-setting isolation with the current format retained. Exports sometimes borrow the previous customer's currency. Amounts can differ, format stays unchanged, and existing files must remain untouched.

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
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Is that the correction you want?

Bad:
> Fix currency profile. All future invoice amounts will be identical; regenerate every existing export.

The bad reply hides the setting's role and invents amount and historical-data guarantees. The good diagram illustrates the failing path, not every export.


## Filtered CSV export

Context: accounting staff inspect filtered invoice rows; the supplied direction is offline use of that same view. They request CSV export containing only visible filtered rows, with invoice number, customer, currency and amount columns, retaining current permissions.

Good:
> ### Background and current direction
> Accounting staff inspect filtered invoice rows. The stated direction is to make that same view available for offline accounting.
>
> ### Current problem and impact
> They currently cannot download the filtered view as a CSV file.
>
> ### What changes
> Add CSV export for the current filtered view.
>
> ### Scope and acceptance
> The download contains only the visible filtered rows, with invoice number, customer, currency and amount columns. Existing access permissions stay unchanged.
>
> ### Please confirm
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate.
> Is that the capability you want?

Bad:
> We are modernizing the entire accounting platform. Approve a background export service and a new permission model.

The bad reply invents a project direction and implementation decision. The good reply ties the supplied direction to the requested capability and its boundaries.
