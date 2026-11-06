# Relaxed comparison — round 5

The missing-fact delivery export case from round 1 was repeated against the
updated optional-section candidate from round 3 and released `41211a0b`.
Candidate source hashes are recorded in the dispatch ledger. Two fresh Codex
CLI sessions were started with `gpt-6.1-sol` / `openai` / medium; no independent
provider receipt was emitted and installed-plugin discovery was not tested.

Both versions asked what work would be displaced and did not request ready
confirmation. The baseline wrote an open draft; the candidate did not write
a draft and read its ready template despite missing information. Candidate
retained the explicit `only` boundary and field order in its reply without
five headings. Its phrase about using a non-forced push to create a PR could
blur the two separate actions, so retain that wording concern. The baseline
stated both actions explicitly. This is one repeated case, not a general rate.

Baseline and candidate reported 254,345 and 143,796 input tokens (including
225,664 and 126,208 cached), and 2,545 and 1,228 output tokens. Usage depends
on the sessions and does not establish ordinary cost. Full fixture prompts,
commands, replies, drafts and usage are in `codex-relaxed-round-5-data.json`.
