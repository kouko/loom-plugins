# Codex minimal template — first comparison

## Scope

The trial starts at released `41211a0b` and changes only the restatement
passage in each existing confirmation owner. The two existing files are
`loom-design/skills/capture-intent/SKILL.md` and
`loom-code/skills/write-plan/references/confirm-intent.md`; no new runtime
file, read, model call or station is added. The prototype and exact patch are
retained at `/private/tmp/loom-codex-relative-20261105/overlay` and
`/private/tmp/loom-codex-relative-20261105/minimal.patch`. Each file increases
by 584 bytes. This is a trial, not the existing working tree or a release.

## Method and validity

Six synthetic cases ran once each against baseline and small template, using
fresh Codex CLI sessions explicitly configured for `gpt-6.1-sol`, `openai`,
and medium effort. Actors were directly instructed to read the snapshot skill,
so this does not test installed-plugin discovery or automatic invocation.
The CLI did not provide an independent model/provider receipt. Pairs ran
concurrently, one pair at a time; only one observation per variant and case
is available, not a statistical comparison or independent blind audit.

All twelve sessions exited successfully, but the batch's strict snapshot
integrity check failed: the two source snapshots each gained 42 Python
bytecode files while actors ran existing scripts. Every original tracked file
retained its recorded hash. The test did not enforce a read-only source
snapshot and should not be presented as doing so. The full output, prompts,
receipts, original source manifests and integrity differences are retained in
`codex-minimal-round-1-data.json`.

The natural-default invoice pair is invalid for consent comparison: the test
wrapper accidentally forbade all publication, not just publication before
the user replied. The separate corrected pair in `codex-default-control-data.json`
uses the same original natural-default case, stops before the user's reply,
allows the skill to explain later authorization, and passed source-integrity
verification with Python bytecode disabled. Do not discard the invalid pair
or blend its results into consent conclusions.

## Observations

- In the incomplete CSV case both variants asked about an unanswered value
  question instead of requesting ready confirmation. The small template
  nonetheless presented five sections as a preview while the interview was
  incomplete. The source requires the five-section structure only for a
  ready confirmation.
- In the stock PDF case the small template presented the relevant direction,
  problem, requested behavior and acceptance in five sections; the baseline
  gave the outcome and acceptance more briefly without the same project
  background. Neither observed reply invented the former table's field claims.
- In the unknown-date case the baseline waited with the fact unresolved; the
  small-template actor additionally offered a temporary substitute label the
  user did not request. The actor did not load the modified confirmation
  reference in that unready phase, so this observation does not prove the
  template caused the suggestion, and a ready-template-only change cannot be
  assumed to repair that interview behavior.
- In the explicit ongoing-hold graph case both actors preserved the hold. The
  small template included labeled outer frames; the baseline did not. The
  small graph's lines have display widths of 51 and 52, so its right edges do
  not align. The visualization alignment oracle returned zero despite these
  differing ASCII line widths: a false negative for this graph. Neither actor
  visibly invoked the visualization skill or verifier. The small reply also
  says it will not change amount calculation, which is not explicitly fixed
  by the user's statement that amounts can differ.
- In the simple command case both variants wrote a draft and requested
  confirmation. The small actor's initial message said it would not modify
  files, then wrote a draft, a potentially confusing action statement.
- In the corrected natural-default pair both variants disclosed a later push
  and reviewable PR after checks, opt-out before publication and separate
  merge. The small template also presented five sections. No future action
  or publication was performed.

## Cost and decision

For the five valid cases from the first batch, CLI usage reported 833,415
input tokens (717,824 cached) and 8,454 output tokens for baseline, versus
861,462 input tokens (749,696 cached) and 8,709 output tokens for the small
template. Their total session times were 264.247 and 246.513 seconds,
respectively. Input includes cached input; do not add those counts. These
single samples do not establish a reliable percentage cost or latency change,
and no dollar estimate can be derived without applicable verified pricing.
The invalid natural-default pair is excluded from this calculation; the
corrected pair is recorded separately.

The five-section context is a visible benefit on the stock case and the
explicitly requested graph gains frames, but the graph has alignment errors
and the unready interview still previews the five-section structure. Refine
only the existing template wording, then retest those specific failure modes
against baseline. Do not infer a global pass or alter non-template workflows.
