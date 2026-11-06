# Codex minimal template — tenth comparison

## Scope and method

This final comparison repeats the exact eighth prototype, recorded in
`codex-minimal-round-8.patch`. It changes the two existing restatement
passages against released `41211a0b`, with no new runtime file, required
read, workflow, station or model call. Four newly authored synthetic cases
were run once per variant. The two product fixtures contain the skill's
ratification line and three `Non-negotiables`; the natural-default case has
no publication-hold instruction. Actors stopped before the user response.

Fresh Codex CLI sessions were explicitly configured for `gpt-6.1-sol`,
`openai`, medium effort, and told to read snapshot skill files; this does not
test installed-plugin triggering. All eight sessions exited successfully.
Original source hashes remained unchanged; Python bytecode additions are
listed in the integrity data. The CLI supplied no independent model/provider
receipt. Inputs, replies, drafts, receipts, usage and hashes are retained in
`codex-minimal-round-10-data.json`. This is an author-read comparison, not an
independent review or statistical estimate.

## Results

- **Incomplete delivery export:** baseline asked for confirmation while also
  asking for missing displaced work. Small stated that urgency and displaced
  work were missing and asked a clarification instead. This is one favorable
  sample; the fifth small prototype had shown the opposite behavior on a
  different case, so readiness is not guaranteed.
- **Ready order JSON and normal publication:** baseline omitted the specified
  four fields from its reply. Small supplied the project background, present
  problem, filtered scope and ordered field list. Both disclosed push after
  review and publication checks, reviewable PR, opt-out and separate merge.
  The small reply's `only four fields` wording may be a stronger exclusion
  than the user's ordered field list, depending on interpretation.
- **Report-title flow and ongoing hold:** both preserved the hold. Baseline
  showed labeled lines without outer frames. Small used titled outer frames,
  marked the after state expected, and every nonblank ASCII line measured 46
  columns. Earlier small-version graphs were sometimes misaligned, so this
  single clean result does not prove consistent alignment.
- **Unknown release date:** neither variant invented a date; both offered to
  wait and asked a question rather than simply leaving the missing evidence
  unresolved. The code-only actor need not read the ready-confirmation
  template in this phase, so this trial does not establish that the small
  template changes that behavior.

Reported input totals were 732,389 baseline and 649,075 small, including
cached input; output totals were 7,926 and 6,291. Summed session times were
255.096 and 212.383 seconds. Four single paired synthetic observations cannot
establish ongoing cost, latency, accuracy or causation. No dollar price was
inferred. The evidence supports useful context and acceptance improvements
in selected cases while retaining known limitations and the separate review,
publication and merge decisions.
