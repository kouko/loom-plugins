# Relative assessment against the released implementation

The user has reconsidered an absolute zero-error release threshold and said
that an improvement over the prior implementation may be sufficient, given the
cost of seeking 100% correctness. This is a change in evaluation framing, not
authorization to publish, merge, waive acceptance, or erase failures. The
existing intent and release hold remain unchanged pending normal workflow.

## Candidate and comparison

This note compares the released baseline `41211a0b` with the current unreleased
runtime `9b9c7d87` (the later HEAD has no changes in the three Loom plugin trees).
It does not evaluate the separate small-template overlay as the release
candidate. Four existing native Claude Code cases have byte-identical prompt,
request and fixture files across the baseline run in
`small-template-trial-data.json` and the current candidate's final run in
`five-round-continuation-data.json`. Both used the explicitly requested
`claude-sonnet-5-5` and requested medium effort, with isolation and original
hooks as recorded in their respective reports.

This is a retrospective author comparison, not a preregistered randomized or
independent blind evaluation. Each variant was run once for each of four cases;
the runs occurred in different experiment rounds and the changed plugin
instructions are visible to the actor. The evidence supports observations on
these outputs, not a general error rate, statistical improvement, absence of
regressions, or proof of causation.

## Observations

| Same case | Released baseline | Current candidate | Comparison |
|---|---|---|---|
| Unknown date | Draft says no release record exists, and reply offers a temporary label not requested. | Reply keeps the correction blocked without offering that label, but says nobody knows the date and incorrectly treats a guess as certainly false. | The extra option disappeared in this sample; both produce unsupported claims. |
| Incomplete CSV | Draft changes no CSV download into no download of any kind; reply states required facts remain open and nevertheless seeks confirmation. | Draft retains the CSV qualifier; reply still seeks confirmation while required facts remain open. | One source-scope error disappeared in this sample; the confirmation-timing defect remains. |
| Setup correction | Gives the correct command and confirmation with limited context. | Gives the correct command in the five sections with preview context. | Candidate supplies more context in this sample; neither output alone proves general comprehension. The no-publication wrapper has an ambiguous duration. |
| Currency fix with explicit hold and requested graph | Draft adds an unsupported daily-frequency claim and both reply/draft imply currency checks cease; hold is disclosed. | Draft omits the daily-frequency assertion, reply uses a framed before/after graph and preserves the hold. | Candidate avoids those baseline additions in this sample; both need scrutiny of whether acceptance covers every invoice rather than only a multi-customer batch. |

The four outputs show concrete local improvements relevant to the original
request, alongside remaining errors. They are not enough by themselves to
establish that the whole change is better across representative requests or
that serious regressions are absent. Earlier final-source evidence also records
ten candidate cases, conflicting auditor classifications, and a failed CSV
graph alignment. Those cases had no matching original-source run in this
assessment; do not manufacture a baseline comparison from them.

## Next assessment

For a defensible relative release decision, compare the released baseline and
the actual chosen candidate on the same representative cases in comparable
fresh sessions, and assess factual accuracy, logical consistency, preserved
context, consent, and required formatting together. Include cases that are new
to the tuning process, and retain all outputs and failures. Report both benefits
and regressions instead of requiring perfect scores. No specific statistical
confidence or number of calls is claimed here. Package tests and the existing
closing-review/acceptance flow remain necessary for a release; the user's
revised quality framing does not itself authorize publication or merge.
