# Industry methods for source fidelity and workflow state

Research date: 2026-11-05. These are documented capabilities and research,
not measurements on Loom. No vendor service was invoked in this research.

## Source-grounding checks

[Amazon Bedrock contextual grounding](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html)
compares model text with supplied sources and a query, and uses thresholds for
grounding and relevance. This is a managed detection/filtering product, not
a guarantee that every unsupported claim is caught. Its documentation notes
that streamed text can reach a user before a relevance judgment is complete.
Standard and Classic tiers differ in supported use and language; AWS's tier
documentation and dedicated language list should be checked together before
making claims about Traditional Chinese for a specific region and tier.

[Microsoft groundedness detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness)
similarly compares generated text with a supplied source and offers an optional
correction feature. Its documented language optimization is English, and the
service page states retirement on 2027-04-30. Microsoft recommends evaluating
Foundry tooling or customer-owned validation for affected workloads. Neither
service has been tested against our fixtures or this conversation's hosts.

[AWS's service card](https://docs.aws.amazon.com/ai/responsible-ai/bedrock-guardrails/overview.html)
explicitly limits grounding to consistency with the supplied source: incomplete
or inaccurate sources and plausible but unsupported claims can still cause
errors. A detector therefore needs a representative evaluation set; it does
not establish an absolute correctness floor.

## Formal rule checks

[Amazon Bedrock Automated Reasoning](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-automated-reasoning-checks.html)
translates text into variables and checks those against a defined logical
policy. It returns findings for an application to act on; it does not itself
block content. The documented capability is currently English (US) only, does
not support streaming, and applies only to content captured by policy variables.
Its natural-language-to-variable translation uses models and can itself be
wrong or ambiguous. This resembles the source-selection/procedural split under
study, but is not the same implementation or proven suitable for Loom.

## Tracing and evaluation

[Microsoft Research VeriTrail](https://www.microsoft.com/en-us/research/blog/veritrail-detecting-hallucination-and-tracing-provenance-in-multi-step-ai-workflows/)
investigates tracing source support and error introduction across multi-step
generation. It is research, not evidence of a deployed solution to this use
case. [FActScore](https://aclanthology.org/2023.emnlp-main.741/) studies checking
separate assertions against evidence, but precision alone can favor responses
that omit needed context. Both factual coverage and support need evaluation.

## Implication for Loom

These products show that source checking and rule checking are implemented in
industry. They do not show that a plug-in can guarantee that every explanation
is correct or intercept every host's streaming UI. A managed integration would
add service dependencies, latency, cost, data transmission, and possibly
language/region constraints. No choice to add or buy one has been made.

For the active change, the smallest justified next decision is whether the
observed benefits of a narrow evidence/state prototype outweigh its remaining
incorrect classifications and integration cost. Do not market a probabilistic
detector or programmatically checked model flag as a zero-error guarantee.
