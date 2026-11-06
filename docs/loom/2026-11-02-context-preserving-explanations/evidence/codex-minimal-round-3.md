# Codex minimal template — third comparison

## Scope and test

The third prototype adds a short generic two-panel example to the same two
existing restatement passages. Relative to released `41211a0b`, only those two
files change, by 1,015 bytes each; there is no new required file, tool call,
model call, station or workflow. The exact proposed patch is
`codex-minimal-round-3.patch`. The example itself has equal 20-column lines in
each panel; this is not proof an actor will reproduce aligned frames.

The first attempted batch was stopped after a nested macOS sandbox prevented
Codex from applying its own command sandbox. Two actors returned text without
reading the skill; two more had started. These are invalid behavioral
observations, retained in `codex-minimal-round-3-preflight-failure.json`.
The repeat used Codex's normal workspace sandbox, checked source hashes and
recorded added bytecode rather than claiming a read-only snapshot.

Six synthetic cases ran once per variant in fresh Codex CLI sessions,
configured for `gpt-6.1-sol`, `openai`, medium effort. One helpdesk case was
new; the other five were reused. Actors were instructed to read the specified
snapshot skill, not tested for installed-plugin discovery. All twelve sessions
exited successfully, original source hashes remained unchanged, and both
snapshots gained Python bytecode. `codex-minimal-round-3-data.json` retains
the prompts, outputs, drafts, usage, manifests and integrity details. Model
and provider were explicitly selected; no independent model/provider receipt
was emitted. This is an author-read, small non-blind sample.

## Observations

- In the new helpdesk CSV case the small version described project direction,
  current manual work and all four requested columns in its five sections.
  The baseline reply omitted the requested column list. The same omission
  occurred in the baseline stock PDF reply while the small version included
  its four fields. These are two observations, not a general error rate.
- In the requested held-invoice graph, both variants retained the ongoing
  publication hold. Neither generated the requested outer frames in this run,
  despite the small template's example. A previous small-template sample
  generated frames with misaligned edges. The example did not demonstrate a
  reliable graph improvement.
- The natural-default invoice small reply asserted that amount calculation
  would not change. The user said amounts could differ between exports and
  limited the repair to currency-setting ownership; a separate ban on changing
  the amount calculation is not explicitly supported. A similar assertion
  appeared in a prior small-template result. The baseline reply did not make
  that assertion in this run. Both natural-default replies described later
  push and reviewable PR after checks, opt-out and separate merge.
- For incomplete CSV, both variants asked for displaced work and did not ask
  for ready confirmation; neither separately asked why now. For the setup
  command, inspect the retained replies and drafts rather than extrapolating
  from other cases.

Total reported input was 976,231 tokens for baseline and 892,605 for small,
including cached input; output was 11,452 and 10,742. Summed session duration
was 320.642 and 301.318 seconds. One observation per case cannot reliably
establish cost, latency, causation or behavior elsewhere; no dollar pricing
was assumed. The visual example did not earn a demonstrated benefit in this
sample and adds text, so the next prototype removes it and tests a concise
clarification of unsupported constraints within the existing template.
