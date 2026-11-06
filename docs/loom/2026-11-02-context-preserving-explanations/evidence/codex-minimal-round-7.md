# Codex minimal template — new-case comparison

## Scope and method

This verification-only round repeats the inline second prototype, exactly
`codex-minimal-round-2.patch`: the two existing restatement passages change,
with no new runtime reference, workflow, station or model call. Five newly
authored synthetic cases ran once each against released `41211a0b` and the
prototype. They were not used in the prior rounds, although they deliberately
exercise similar failure classes. Actors were directly instructed to read
snapshot skill files in fresh Codex CLI sessions configured for
`gpt-6.1-sol`, `openai` and medium effort; installed-plugin triggering was
not tested and the CLI did not emit a separate model/provider receipt.

All ten sessions exited successfully; original source hashes and directory
inventories remained unchanged in both snapshots. Fixture inputs, prompts,
outputs, drafts, receipts, token usage and source hashes are retained in
`codex-minimal-round-7-data.json`. This is an author-read comparison with one
observation per case and variant, not independent blind review or a
population-level estimate.

## Results

- **Incomplete shipment export:** both actors asked a missing question rather
  than requesting ready confirmation. The small actor also described the
  already-supplied manual workaround as potentially requiring further
  clarification; that could lead to an unnecessary question.
- **Maintenance PDF:** the small reply presented the requested background,
  current problem, change, ordered fields and confirmation. It said the PDF
  contains the selected records but omitted the user's explicit `only`,
  weakening the exclusion boundary. The baseline reply said `only` but did
  not explicitly state the supplied order. A source-supported qualifier may
  not be discarded simply because a five-section layout is present.
- **Worker-group flow with continuing hold:** both replies preserved the hold
  and variability of random outcomes. The small reply supplied separately
  titled before/after outer frames; each nonblank ASCII line measured 44
  columns. The baseline supplied labeled flows without outer frames. The
  small diagram's labels were English despite the Traditional Chinese request.
- **Natural publication:** both explained the later branch push, PR, opt-out
  and separate merge. The baseline explicitly said the push was non-forced;
  the small reply said normal push without the same explicit qualification.
- **Simple setup correction:** both wrote an open intent and explained the
  one-flag change. The small reply used five short labeled portions; its
  broad claim that nothing had been modified should be read with the fact that
  it did write the intent draft.

Reported input totals were 816,464 tokens for baseline and 666,937 for the
small template, including cached input; output totals were 8,820 and 7,853.
Summed session durations were 260.247 and 237.314 seconds. These are five
single paired synthetic observations, not reliable ongoing cost or latency
estimates; prices were not inferred. The comparison shows useful context and
one aligned graph, alongside a weakened scope qualifier and less explicit
push qualification. Both positive and negative evidence must accompany any
relative-improvement decision.
