# Native comparison against released baseline

## Disposition

Both the released baseline and current unreleased candidate exhibit material
problems. The candidate supplies more context in the sampled ready cases and
handles the unknown-date interview more cautiously, but it also omits required
publication disclosure in the ordinary-default invoice case and seeks
confirmation before writing the required intent in a code-only case. Do not
interpret this small, author-reviewed sample as proof of overall superiority
or infer that a publication actually occurred. The results support repairing
the observed confirmation-boundary regressions before recommending release,
without requiring an unattainable zero-error guarantee.

## Protocol

Frozen preregistration is in `relative-test-packet.json`: source snapshots
`41211a0b` (baseline) and `9b9c7d87` (candidate); identical requests and
synthetic fixtures for each arm; six reused cases and two newly authored cases;
one run per arm per case. The model was native first-party
`claude-sonnet-5-5` in all sixteen returned modelUsage records; medium effort
was requested, not independently verified. The user explicitly authorized the
two listed resource inventories, eight cases and sixteen model calls.

Both snapshot hook sets passed seven local preflight checks. Synthetic private
reads, network bind and snapshot writes were denied. The runs used isolated
fixtures, retained the original hooks via isolation wrappers, and verified the
requested skill, session context, visualization card, untouched snapshots and
absence of fixture commits. All sixteen sessions finished successfully with
no permission denials. CLI-estimated cost totals USD 2.1403216.

Case order is fixed, with arm ordering alternated deterministically and up to
three calls running concurrently. These are single observations, not a blind
or representative trial, and several cases were used while tuning the
candidate. The newly authored cases are locally designed rather than an
independent holdout sample. Author adjudication compared replies and draft
contents with source fixtures, the recorded stop/consent wrapper and existing
contract; ambiguous wording is not counted as a proven action or error.
All outputs and source fixtures, receipts and hashes are retained in
`relative-native-comparison-data.json`; email-shaped strings are redacted.

## Findings by case

| Case | Released baseline | Unreleased candidate |
|---|---|---|
| Unknown date | Asks for confirmation despite unavailable required date; draft broadens the user having no record to no record existing, and rules out looking for unsupplied sources. | Distinguishes the placeholder from a wrong calendar date and waits for evidence without a ready confirmation; no draft written. |
| Incomplete CSV | Says required facts are missing but asks for intent confirmation; also offers a pagination choice whose necessity is not established by the request. | Says required facts are missing and asks for one, with a preview of later confirmation rather than requesting a current yes. The preview adds workflow detail. |
| Complete CSV | Produces a ready confirmation with the core fields and describes automatic publication. | Produces the requested five sections and core boundaries; its phrase that filters affect only screen display may overstate the source. Both outputs make some scope claims needing care. |
| Currency, explicit ongoing hold and graph | Preserves the hold, but says staff will no longer need to inspect each invoice and uses an unframed text comparison. | Preserves the hold, gives a titled framed graph and avoids the general inspection claim. The chart passed the width checker. The saved intent was English despite the user-facing language requirement. |
| Currency, normal publication default | States that confirmation authorizes later publication after checks, opt-out and a separate merge decision. | Requests confirmation but does not disclose any publication consequence, opt-out, or separate merge. This is a message-level consent defect, not evidence that anything was pushed. |
| Existing setup command | Drafts an intent before asking for confirmation and gives the correct command. | Gives the correct command and five sections but explicitly says no intent file exists while asking the user to confirm. The fixture wrapper's publication-hold duration is ambiguous, so do not count that separately as a proven consent error. |
| New calendar command fixture | Gives the correct flag correction, without a diagram. | Gives the correct flag correction in five sections but adds a diagram to a simple text change. Both interpret the prompt's temporary nonpublication instruction differently; duration is ambiguous. |
| New inventory PDF fixture | Gives a ready confirmation with permissions and scope. | Adds project background and a concise flow, and retains scope. The wrapper's nonpublication duration remains ambiguous; do not equate differing interpretations with proven unauthorized action. |

The baseline's plain-text graph does not contain a framed comparison; an
alignment checker returning no drift on plain text is not proof that it meets
the requested framed style. The candidate chart is framed and verified with
the width-aware checker. No human comprehension study was run. Testing used
the actual native CLI with synthetic fixtures, not an installed host session,
other hosts, actual publication or post-confirmation behavior.

## Decision implications

The relative standard permits known residual errors, but material consent and
workflow regressions should not be silently traded away for a better layout.
Target the two observed candidate failures, then compare the affected cases
and representative controls on the changed source; retain this entire run and
its baseline. The existing closing review, acceptance report and user-controlled
release/merge decisions remain separate. No change, PR or release was made by
this experiment.
