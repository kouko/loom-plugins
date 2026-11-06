# Codex minimal template — fourth comparison

## Candidate and test

The fourth prototype starts from the smaller second version, omits the
unproven embedded diagram example, and replaces its general grounding sentence
with a concise instruction covering supported facts, requirements, boundaries
and guarantees. It changes only the same two existing restatement passages,
adds 744 bytes to each released-baseline file, and adds no file, required read,
model call, station or workflow. The exact patch is
`codex-minimal-round-4.patch`.

Six reused synthetic cases ran once per variant in fresh Codex CLI sessions,
configured for `gpt-6.1-sol`, `openai`, medium effort. The helpdesk case was
new in round 3 but is no longer a holdout here. Actors were told to load the
snapshot skill directly; installed-plugin triggering was not tested. All
twelve sessions exited successfully. Original tracked source hashes remained
unchanged; the small snapshot gained 42 Python bytecode files and baseline
gained none. `codex-minimal-round-4-data.json` retains prompts, replies,
drafts, usage, manifests and integrity details. The CLI supplied no separate
model/provider receipt. This author-read, one-sample-per-variant comparison is
not a general error-rate estimate or independent blind assessment.

## Observations

- For incomplete CSV both asked for a missing answer rather than a ready
  confirmation, and both identified two missing value questions. The small
  reply did not use five sections before readiness.
- For the held invoice graph, the small reply retained the ongoing hold and
  drew titled outer frames, but again added `do not change amount calculation`,
  an unsupported restriction. The user allowed amounts to differ, which is not
  the same constraint. This repeated the earlier failure despite the added
  general instruction. The baseline did not add that restriction in this
  observation. The small graph's ASCII line lengths also need not be assumed
  aligned without a width check.
- For the natural-default invoice, the small reply did not add the amount
  calculation restriction in this observation; both variants disclosed later
  push and PR after checks, opt-out and separate merge. The small reply says
  staff check and re-export without preserving the user's condition that
  re-export happens on error.
- For stock PDF, both replies listed the field names but did not restate their
  specified order; the small reply deferred that known requirement to the
  later specification. In the repeated helpdesk case both included the
  specified field order. No broad completeness conclusion follows.
- The simple setup case must be judged from its retained output and draft;
  this comparison cannot establish other hosts or later workflow behavior.

The reported input totals were 993,819 tokens baseline and 939,488 small,
including cached input. Output totals were 11,537 and 10,579. Summed session
times were 329.353 and 303.227 seconds. Single synthetic observations do not
reliably establish cost, latency or causation, and no dollar pricing was
assumed. The unsupported constraint survived a substantive template wording
change, so simply repeating a general prohibition has not established a fix.
