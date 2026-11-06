# Relaxed Codex iterations — retained observations

Ten sequential rounds compared the released baseline with scoped candidates;
no Claude sessions were used. The 21 starts include one failed sandboxed
initialization and 20 completed sessions. Each round stayed within the
eight-start limit (round 1: three; rounds 2–10: two each). The 20 completed
receipts report 3,533,578 input tokens including 2,988,032 cached and 33,226
output tokens. Those counters are not a bill and no dollar price is inferred.
The previous 116-session continuation, its over-limit rounds, its failures,
and all earlier records remain separate and are not reset.

The final candidate makes the five sections optional. It exactly matches the
source hashes in ledger round 3: capture entry
`247471e6b4b79ab6bd0de3043b2355076b2b6a29a4976f3045ab2780278d1af3`,
capture ready reference
`a08176ba13159395b92a62a79bef5eaa736849a461ab60aefcf7738663131d21`,
and code-only confirmation
`18347430de550b4609c0873b1cac2754d729928494ceff6af75c8ae3792f4f42`.
Rounds 3–7 observed this exact source. Rounds 1–2 used the prior fixed-five
candidate; rounds 8–10 used a different candidate with an additional reminder.
Do not attribute observations across versions as if they were identical.

Two different simple code-only cases in rounds 4 and 7 omitted the supplied
person and problem from the candidate's reply, whereas the baseline explained
the user's preview purpose. Round 8's attempted explicit reminder was actually
read but did not prevent omission in its repeat. It was removed after round 10
to avoid retaining an extra unproven instruction; the final source is the exact
round 3–7 candidate, not a newly invented version. The released four focused
modules pass (96 tests) after that restoration; these mechanical checks do not
prove semantic equivalence, and prior loss of drafting-fidelity assertions
remains documented in `prescope-test-coverage-audit.md`.

Round 5's exact final candidate asked for a missing required answer without
claiming confirmation, but still read the ready template before facts were
settled. Round 6 offered an unrequested choice about how to display an unknown
date and made an overbroad evidence-absence claim; baseline also offered an
unrequested display option. Round 3 preserved an explicit ongoing publication
hold and showed titled frames but misaligned their ASCII edges. Round 10's
different candidate produced aligned frames in its single repeat; that result
does not transfer to final source. The additional template read remains a real
cost, and one repeatedly unready case loaded it. Comparison samples do not
establish whether day-to-day costs rise substantially.

The actors were explicitly directed to read skill paths in synthetic isolated
fixtures; they were configured `gpt-6.1-sol` / `openai` / medium. There was
no independent provider receipt, no installed-plugin trigger test, no blind
assessment and no general error-rate or causal inference. Relative benefits
and material regressions are preserved in individual round reports and data.
No independent review or acceptance verdict is implied; publication and merge
remain held.

After restoring the final tested source, the full Loom package suite completed
with exit code 0 using the locked offline environment. The three runtime file
hashes were checked against the values above before the suite. This mechanical
result does not resolve the behavioral findings or establish release readiness.
