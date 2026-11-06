# Relaxed comparison — round 1

The released `41211a0b` and unchanged sixth prototype were compared on the
previous delivery-export fixture with missing displaced work. Both actors were
directed to read their snapshot skill in fresh isolated Codex CLI sessions,
configured for `gpt-6.1-sol`, `openai` and medium. No independent provider
receipt was returned. Direct skill invocation is not installed-plugin testing.

Both replies explicitly asked the missing question without requesting ready
confirmation; both drafts retained it as an open question. The candidate read
the ready template before the fact was settled and presented five labeled
sections; five sections in an interview are no longer themselves a failure.
It also discussed a private complexity check. Both described the relevant
future publication controls. The candidate reply described records matching
the filters and permissions but did not explicitly say *only* those records;
its draft did include the restriction. Whether the reply wording weakens that
boundary in context needs judgment; retain it as a possible regression rather
than claiming either an improvement or causal failure.

The baseline and candidate reported respectively 144,715 and 204,313 input
tokens (including 114,944 and 174,080 cached) and 1,710 and 2,246 output
tokens. One paired sample cannot establish ongoing cost. The first baseline
start failed to initialize inside the sandbox with `Operation not permitted`
and had no usage receipt; one explicitly approved sandbox-external retry and
the candidate completed. Three starts count against this round's eight-call
limit, including the failure. No Claude session was used.

Full prompts, messages, commands, drafts and usage are retained in
`codex-relaxed-round-1-data.json`; reservations and failed starts are in
`codex-relaxed-dispatch-ledger.json`. Earlier 116 starts and all earlier
failures remain retained. This single repeated synthetic case is not a blind
review, population estimate, release acceptance, or proof that the template
caused the observed differences.
