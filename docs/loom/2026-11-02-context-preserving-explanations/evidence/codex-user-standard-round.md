# User-standard confirmation round

Two new synthetic cases were each compared once against released `41211a0b`
and the current candidate: a simple documentation-preview flag correction,
and a CSV export with unresolved product-value information. Four starts were
reserved and completed; no retry or Claude session occurred. Actors were
directed to read isolated snapshot skills in fresh Codex CLI sessions configured
for `gpt-6.1-sol` / `openai` / medium. There is no independent provider receipt,
installed-plugin trigger test or blind assessment. All four exited zero and
returned usage, but each stderr reported a model-list refresh timeout; this is
retained in the data and prevents treating the requested model as an independently
verified receipt. Tracked snapshot content matched the source snapshots after
the runs. The supervisor's elapsed fields are upper bounds because it collected
completions sequentially, so do not use them as precise latency.

In the simple case both actors wrote unconfirmed drafts, described the exact
flag change and boundaries, and disclosed review and publication checks,
non-forced push, PR, opt-out and separate merge. Baseline named the affected
editors and explained that they needed to start a documentation preview;
candidate referred to colleagues and the preview command but did not name
editors or explicitly restate the failure. Candidate did not demonstrate a
clear background improvement over baseline in this case.

In the incomplete CSV case neither actor requested ready confirmation. Both
asked why the work should be prioritized now. Baseline mentioned the current
weekly manual copying; candidate restated the filtered-only boundary, field
order, no-change and no-scheduling constraints but did not mention the manual
copying burden in its final answer. Candidate did not write a draft and read
the ready template despite the missing information; baseline wrote an open
draft. This round does not demonstrate a new material authorization or scope
failure, but these trade-offs, the extra read and prior observations must not be
erased by the small sample.

The four receipts total 587,375 input tokens including 476,928 cached, and
5,379 output tokens. They do not establish normal cost or latency. Full fixture
prompts, messages, commands, drafts, stderr, usage, source integrity and receipts
are in `codex-user-standard-round-data.json`; the reservation and source hash
ledger is `codex-user-standard-round-ledger.json`. Earlier 116 and 21 starts,
including failures and prior over-limit rounds, remain separately retained.
This single author-read round does not establish rates, causality, independent
review or acceptance. It supports no claim of a demonstrated broad improvement
or of no material regressions outside these cases.
