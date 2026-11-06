# Ten context-example iterations — assessment

Ten sequential rounds compared the prior current candidate with the same
isolated short example, using paired synthetic fixtures. Twenty sessions were
started and completed, two per round, without retries or Claude calls. All
were configured for `gpt-6.1-sol` / `openai` / medium; no independent provider
receipt, installed-plugin trigger test, blind assessment or statistical
estimate is available. Receipts total 3,233,721 input tokens including
2,746,624 cached, and 29,208 output tokens. These are counters, not a bill.
All stderr files were empty. Source hashes and per-round reservations and
starts are in `codex-ten-context-ledger.json`; all prompts, events, drafts,
receipts and usage are in the ten `codex-ten-context-round-*-data.json` files.
The three relevant source hashes were verified; a full snapshot inventory
check is not claimed. Supervisor elapsed fields are upper bounds, not precise
latency, because it collects the processes sequentially.

In round 5 the example connected the accountant, occasional wrong currency and
re-export, while current omitted the affected person and re-export. In round 4
it mentioned manual correction and re-export while current did not. In several
other rounds both versions provided the context, both omitted some, or their
wording differed only slightly. Both versions had misaligned ASCII frames in
round 4; both proposed an unrequested date-display alternative in round 7.
Examples and variations from previous rounds remain evidence; notably the
earlier isolated example trial's incomplete CSV reply did not explicitly say
`only`, though its draft did. Round 3 of this series retained `only`; neither
observation establishes a reliable rate or causal relationship.

Given the user's criterion—better connected necessary context without an
obvious new negative effect, not 100% correctness or a significant statistical
advantage—the short abstract example was applied to the two existing templates
as tested. It adds no new step, reference read, model call or fixed-heading
requirement. The two modified files match the tested example hashes
`5768fe7ad21fe93956aaa1e3ee8ba88c491e06e7fa51adeae0a54ac0bee877f0` and
`b36840eb9393e74bf26d17472dd34f29da9cd805ddfdd6f0e7814cea97bfb6aa`;
the capture entry remains
`247471e6b4b79ab6bd0de3043b2355076b2b6a29a4976f3045ab2780278d1af3`.
The existing four focused modules pass (96 tests), manifest sync and diff
checks pass. These are mechanical checks, not behavioral guarantees, a blind
review or acceptance.

Known uncertainty remains: the example was not consistently better, one prior
reply weakened an explicit exclusion, code-only simple cases still omitted
affected users, the ready capture template may be read before readiness, ASCII
alignment remains variable, and unnecessary date alternatives remain possible.
The baseline and candidate comparisons, prior 116, 21, 4 and 4 starts and all
failures remain retained. Publication and merge remain held; final independent
review and acceptance are separate.

The full locked offline Loom package suite subsequently completed with exit
code 0 on the applied example. The checked template hashes above match the
tested snapshot. The suite does not replace behavioral review or acceptance.
