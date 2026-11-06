# Codex minimal template — sixth comparison

The sixth prototype moves the capture-intent restatement into one 1,159-byte
reference, with a pointer at the existing confirmation step; code-only
confirmation remains inline. Relative to released `41211a0b`, it changes the
two existing confirmation owners and adds only this one template file. It
adds no station or model call, but ready capture-intent now requires an
additional template read. Its exact patch is `codex-minimal-round-6.patch`.

Six repeated synthetic cases ran once per variant in fresh Codex CLI sessions,
configured for `gpt-6.1-sol`, `openai`, and medium effort. Actors were told
to read the snapshot skill; installed-plugin triggering was not tested. All
twelve sessions exited successfully; original tracked source hashes remained
unchanged, baseline gained 42 Python bytecode files, and the small snapshot
gained none. The CLI did not emit an independent model/provider receipt.
`codex-minimal-round-6-data.json` retains prompts, replies, drafts, usage,
source hashes and observed template-read commands. These author-read single
samples are not independent review or general error rates.

The incomplete CSV actor under the small variant had identified an unanswered
required fact, yet read the ready template and presented five sections before
asking about displaced work. The baseline also requested confirmation in the
same reply as the missing-fact question in this observation. Moving the
template therefore did not enforce the intended readiness boundary; it does
not follow that the reference caused the behavior. The template was observed
as read in all five capture-intent small sessions, including the incomplete
case; the code-only case used the existing inline reference.

The held-invoice small reply retained the explicit hold and included framed
before/after diagrams, but one ASCII line had display width 41 while the
remaining nonblank lines were 40. It did not add the prior unsupported
amount-method restriction in this sample. Both natural-default replies
disclosed later push and reviewable PR after checks, opt-out and separate
merge. The stock PDF and notice cases included their known field/behavior
details in the small replies; the repeated notice case is not a holdout here.

Reported input totals were 898,031 tokens baseline and 938,953 small,
including cached input; output totals were 9,976 and 10,562. Summed session
times were 299.403 and 322.700 seconds. These single paired synthetic
observations do not prove a cost or latency increase or its cause; no dollar
pricing was inferred. The required additional reference read is a real
structural cost, while this sample did not show that it prevents premature
loading. Prefer the simpler inline prototype for further evaluation unless
new evidence changes that tradeoff.
