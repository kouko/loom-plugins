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
> The release notes make the latest release look outdated. I will correct only
> the displayed date to the verified 2 November, leaving the rest unchanged.
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate. Is that the correction you want?

Bad:
> The release notes make the latest release look outdated. I will correct only
> the displayed date to the verified 2 November, leaving the rest unchanged.
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate. Is that the correction you want?
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
> Each background job should use its own rule for choosing who executes it.
> Failed jobs should stop retrying at their configured limit so they stop
> blocking the queue. Successful jobs and the existing interface stay unchanged.
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate. Is this the scope you want?

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
> I used "profile" as shorthand for the selection rule you described and left
> out that connection. Each job has its own rule for choosing who runs it;
> you reported that jobs are using another job's rule and getting inconsistent
> results. The requested correction is to use each job's own rule. That alone
> does not promise the same worker or identical results on every run.
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate. Does that match your request?

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
> Each job should randomly select from its own eligible workers, preserving
> randomness and the existing interface. The correction is which list it uses.
> Only after review and publication checks pass does saying yes authorize
> both a non-forced branch upload and a pull request ready for review. You may
> opt out anytime before publication; merging remains separate. Is that the change you want?

Bad:
> Confirm that every job always chooses the same worker, and that no functions,
> options, settings or commands may be added anywhere. Would you prefer a new
> interface for jobs with no list? Publication is off unless you separately opt in.

The bad reply contradicts randomness, expands an interface constraint into an
implementation prohibition, invents an additional scope choice and reverses the
publication default.
