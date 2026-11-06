# Codex continuation — scope and cost preflight

## User constraint

Continue with Codex only for up to ten further iterations. Confine the change
to the explanation template and necessary examples, avoid new workflow or
mechanisms, and do not substantially increase the stage's ongoing cost. Keep
the existing relative-improvement standard, consent obligations, failures,
and publication and merge holds.

## Current scope is not yet acceptable

The entire branch was compared with released ancestor `41211a0b`, not only
the uncommitted diff. It changes both station entry files, interview and
confirmation instructions, intent field templates, and Loom visualization
rules/cards in addition to adding explanation references and examples. Some
are clarification or preservation rather than a new stage, but the full
tree cannot be described as a template-only change. The two shared diagram
examples already merged in the baseline are outside this finding. A candidate
must separate the desired presentation improvement from these other changes;
do not delete or overwrite the existing work without preserving its evidence.

The candidate requires loading a grounding reference before intake replies
and, when ready, an additional format reference; examples are conditional.
In the previously retained paired native sample, tool traces showed the
candidate actor loading the grounding reference in all eight cases and the
format reference in seven. The baseline did not contain these files. The two
references contain 6,185 and 3,264 bytes respectively, before optional
examples. Static file size is not a direct token or latency measurement.

## Cost evidence and its limits

In the previously retained single eight-case paired Claude sample, the CLI
reported estimated costs totaling USD 0.9670553 for the baseline and USD
1.1732663 for the then-candidate, approximately 21.3% higher. Summing the
reported input, cached-input, cache-creation and output token counters yields
885,037 and 1,118,264 respectively, approximately 26.4% more for the
then-candidate. Median end-to-end session duration was 23.6 versus 25.3
seconds. These are aggregate counters for eight non-randomized synthetic
sessions, not an estimate of daily production cost, Codex pricing, independent
host comparison, or causal effect. The tested candidate is an earlier source
snapshot, not proof of costs on the final working tree. The user has not set a
numeric definition of substantial; this sample is evidence to investigate,
not an automatic cost acceptance or rejection.

The prior `small-template-trial.patch` is concrete but also changes entry
instructions to read an overview, and its Claude pilot did not establish a
behavioral improvement. It therefore cannot be declared a passing
template-only solution. Future Codex comparisons must name exact source
hashes, keep inputs and controls matched, report input/output usage and elapsed
time where available, and distinguish direct skill invocation from native
automatic triggering. Avoid installing plugins or altering the current host.
