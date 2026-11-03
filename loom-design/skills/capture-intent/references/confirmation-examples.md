# Connected intent explanations

Use this outline as content connections, with optional grouping, headings and
length chosen for the situation. These are reasoning aids, not output sections
or fill-in scripts. Write in the user's conversation language. A familiar
request may need one short paragraph; a requested detailed repair may need more.
Borrow only information connections from examples, keeping their dates, roles,
impacts and constraints as case-specific facts. Example facts are not live-case
defaults. Require actual-request support or evidence for every date, role, impact
and constraint; leave unsupported details unresolved rather than importing them.

Connect the subject and its role to the reported problem and its impact, then
to the wanted outcome, preservation boundary and what confirmation authorizes.
Use only supplied facts and supported consequences. Keep unknown facts open.
Compare each proposed outcome and Acceptance line with the request before
writing it: explanation adds understanding, not new guarantees or scope.
Observed inconsistent results establish a symptom, not a deterministic target.
An unmentioned edge case is not automatically a new Acceptance line or user
choice; first check whether the requested change actually leaves it unresolved.

Repair assistant shorthand using the already supplied role, acknowledging the
earlier omission. Distinguish that conversational meaning from a verified name
or implementation inside the application. Asking the user to define your own
unexplained label creates work without repairing the explanation.
Preserve the interface boundary while leaving private helpers to implementation
choices. An unchanged user-facing interface says nothing about whether internal
functions may be added.

The station's procedural items guide work; they are not a message checklist.
Omit empty or inapplicable items, status values, paths, default settings and
narration of skipped checks. Retain material consequences, required disclosures
and unresolved user decisions, expressed through their effects. Never ask the
user to approve implementation or review quality.

Choose the existing phase before composing a reply. Missing required facts
belong to the interview: ask for the needed fact and explain its relevance.
Once ready, privately prepare applicable disclosures, then compose the connected
outcome confirmation. Private records and after-answer actions stay outside that
message. Show the user the outcome and applicable consequences, not the intent
document's schema or a report of the station's work.

Disclose in the same yes the automatic publication consequence, the opt-out
before publication and the separate merge decision, in concrete language.
That yes authorizes a later non-forced branch upload and a pull request ready
for review after review and publication checks pass. It is not a second
publication question. Record authorization only after informed yes; an opt-out
leaves the publication field absent. An unresolved interview remains open;
neither an example nor a provisional agreement supplies its missing facts.

The examples below assume no additional unresolved one-way-door consequence or
other applicable disclosure. Include such consequences when present in the
real request; examples never waive the owner's conditional obligations.

## Final-message check

Check each sentence for help understanding scope or outcome, or a required
decision or consent. Delete pure private progress, checks, status, settings,
commit-message and handoff inventories unless the user asked for them. Remove
repeated facts under several field labels. Retain required disclosures, including
verbatim WARN notices, cost/egress, one-way-door consequences, principles and
carried details whenever applicable. A correct scope and authorization paragraph
does not make an appended internal work inventory relevant. Apply this edit to
the existing reply, without another stage, review loop or user stop; finish the
actual confirmation question and wait instead of appending private work.

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
> Saying yes confirms this scope and authorizes a non-forced branch upload and
> pull request for review after checks pass; you may opt out before publication,
> and merging remains separate. Is that the correction you want?

Bad:
> The release notes make the latest release look outdated. I will correct only
> the displayed date to the verified 2 November, leaving the rest unchanged.
> Saying yes confirms this scope and authorizes a non-forced branch upload and
> pull request for review after checks pass; you may opt out before publication,
> and merging remains separate. Is that the correction you want?
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
> Saying yes confirms those outcomes and authorizes a non-forced branch upload
> and pull request for review after checks pass; you may opt out before
> publication, and merging is separate. Is this the scope you want?

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
> Saying yes confirms this correction and authorizes a non-forced branch upload
> and pull request for review after checks pass; you may opt out before
> publication, and merging remains separate. Does that match your request?

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
> Saying yes confirms that scope and authorizes a non-forced branch upload and
> pull request for review after checks pass; you may opt out before publication,
> and merging remains separate. Is that the change you want?

Bad:
> Confirm that every job always chooses the same worker, and that no functions,
> options, settings or commands may be added anywhere. Would you prefer a new
> interface for jobs with no list? Publication is off unless you separately opt in.

The bad reply contradicts randomness, expands an interface constraint into an
implementation prohibition, invents an additional scope choice and reverses the
publication default.
