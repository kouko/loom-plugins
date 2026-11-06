# Relative iteration 1 — candidate behavior

## Outcome

The two targeted regressions did not reproduce in their respective single
observations: normal publication consent was disclosed in the natural-default
invoice case, and the code-only ready case wrote an open intent before asking
for confirmation. However, two other candidate outputs contain newly observed
problems relative to the saved released-baseline samples: the complete CSV
intent is in English although the conversation language is Traditional Chinese,
and the natural-default invoice intent says the accounting team exports
invoices every day although the synthetic input supplies no such frequency.
Continue evaluation; these results neither prove causal repair nor establish an
overall release verdict.

## Test

Eight candidate sessions used the same synthetic cases as the prior sixteen-run
comparison and the frozen source overlay in `relative-iteration-1-test-packet.json`.
All eight returned `claude-sonnet-5-5` in modelUsage; medium effort was
requested. Seven hook checks and isolation preflight passed; no actor permission
denial, input mutation or fixture commit was observed. CLI-estimated cost was
USD 1.1683296. Outputs, saved drafts, receipts, source hashes and case inputs
are retained in `relative-iteration-1-data.json`, with email-shaped strings
redacted. The earlier baseline was executed in another batch, so this is a
noncontemporaneous single-observation comparison, not an error-rate estimate.

The author inspected replies and intent drafts. No independent reviewer or
human comprehension study was run. The complete locked package suite and 157
focused checks passed before these actor calls; they do not establish model
behavior. The requested explicitly held-invoice chart and the unsolicited
natural-default chart passed a width-aware alignment check. The held case
invoked the visualization skill and read its template; the natural-default
chart had no observed visualization-skill invocation.

## Findings

| Case | Observation and limitation |
|---|---|
| Natural-default invoice | Ready reply discloses both publication actions after both checks, opt-out and separate merge. The saved intent describes beneficiaries as exporting daily, which the inputs do not establish; the prior released-baseline draft did not make that daily claim. |
| Code-only setup | Actor writes the intent before the ready confirmation. As in the prior comparison, the wrapper's restriction on future publication has ambiguous duration and is not scored as an established consent error. |
| Complete CSV | Reply preserves the CSV qualifier and five headings, but the complete saved intent is English even though the requested conversation language is Traditional Chinese; the released-baseline draft for the same case was Chinese. The phrase that filtering currently affects only screen display may also overstate source evidence. |
| Incomplete CSV | Leaves required value-case facts open and does not ask for a current confirmation. It nevertheless states that without displaced work there is no real priority; that blanket explanation is not entailed by the inputs. |
| Unknown release date | Does not ask for ready confirmation and distinguishes the placeholder from a calendar date. It says no other project location contains a release-date record without an observed comprehensive search; only the fixture files it actually read are established. |
| Explicit publication hold | The reply retains the explicit ongoing hold and a framed chart. Its chart and draft imply invoice currency no longer requires per-invoice checking; that may overstate the effect beyond the reported defect. |
| New calendar setup | Writes the intent and presents the desired flag correction without an unnecessary diagram. The wrapper's future publication scope is ambiguous. |
| New inventory PDF | Retains supported context, filters, access and data-preservation boundaries, and writes an intent. The wrapper's future publication scope is ambiguous. |

No implementation, publication, merge or installed-host behavior is inferred
from these messages. Correct, source-grounded values, visible language and
the applicable consent branch remain separate checks; a relative improvement
does not convert a newly observed unsupported claim into an established fact.
