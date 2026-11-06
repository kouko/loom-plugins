# Evidence-backed fields and computed readiness — tools-disabled pilot

## Outcome

The six-case pilot does not establish that this design meets the user's
factual/logical floor. Its computed state prevented ready-confirmation
language in the two incomplete cases and allowed four ready cases, but the
extractor introduced an additional unnecessary prerequisite in the incomplete
CSV case. Three ready drafts supplied an originator value not found in the
supplied prompts. A valid substring is not proof of correct interpretation;
program code cannot make model-supplied classifications true.

This is a component experiment, not an installed Loom skill, complete contract
implementation, integration test, blind audit, representative benchmark or
demonstration that output can be intercepted before display.

## Method

The user explicitly consented to transmitting nine named candidate skill and
reference files plus synthetic test data to first-party Anthropic Claude. All
nine paths and their hashes match the previously tested candidate manifest.
Six existing synthetic cases were each processed once by two separate calls:
one selected quoted evidence and missing fields, and a second wrote a user
reply and intent draft from the source, selected evidence, selected owner
guidance and computed state. Each call used `claude-sonnet-5-5` in modelUsage;
medium effort was requested, not independently verified. Tools, hooks and
session persistence were disabled. No plugins or actual project data were
loaded. CLI-estimated total for twelve calls: USD 0.9439405.

Python verified that selected nonempty quotes occur literally in their named
source and computed readiness from required field presence, product value-case
fields and the model's extra missing-fact list. The writer was instructed to
honor that state. This is not a complete implementation of all owner rules:
the model still selects kind, fields, additional missing facts and hold. The
prototype includes neither a decision override nor a host output gate. The
selected guidance does not encompass every referenced resource, host context,
live tool results or all decision branches. Cases were reused and no matched
baseline was run in this experiment. Outputs and receipts are in
`grounded-state-pilot-data.json`, with email-shaped originator values redacted.
That file contains exact scripts, owner source hashes, inputs and the complete
result except for that redaction.

## Observations

| Case | Computed state and observed output |
|---|---|
| Unknown release date | Not ready; reply distinguishes reported wrong date from observed placeholder and asks for evidence. The draft was empty. It also asserts that an observable acceptance condition cannot yet be defined; whether a conditional acceptance could already be written is a separate judgment. |
| Incomplete CSV | Not ready; no ready confirmation. The extractor and writer nonetheless ask about alternatives beyond the already supplied manual-copy workaround as a further missing prerequisite. The supplied known workaround already gives an existing alternative; no rule in the selected evidence establishes that a separate alternative must exist. |
| Complete CSV | Ready; reply retains the CSV qualifier, five sections, permissions, opt-out and separate merge. The saved draft gives an originator not supported by the supplied prompts. |
| Invoice, continuing publication hold | Ready; reply preserves the hold and provides a before/after diagram. A width-aware check reports no drift. The saved draft gives an unsupported originator value. |
| Invoice, ordinary publication default | Ready; reply describes both branch upload and reviewable PR after the two checks, opt-out and separate merge. The saved draft gives an unsupported originator value. |
| Setup command correction | Ready; reply retains the command and separates reported failure from inspected text. The fixture's instruction not to publish has ambiguous duration; do not claim a definite publication-consent failure solely from interpreting that wrapper differently. |

All extracted spans occurred literally in their designated sources. That
mechanical fact does not establish that every span supports its assigned field,
that the source list is complete, or that writer claims follow from it.
For example, the natural-default invoice selection places the user's statement
that amounts need not be identical among acceptance evidence. The writer did
not impose equal amounts, so that classification alone is not an output error.

The author directly inspected these cases; no independent fresh-context
reviewer judged them. Do not derive an overall success percentage or claim
an improvement over either earlier complex or small-template native trials.
The tool-free writer could not call the diagram generator or inspect real
files; its claimed behavior and saved intent are model output, not actions.
