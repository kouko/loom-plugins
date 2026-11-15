---
title: "Does the dispatch resolver establish trust-boundary risk?"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags:
  - loom/research
---

# Does the dispatch resolver establish trust-boundary risk?

## Question and scope

Does `dispatch_profile.py` independently establish a real task's trust-boundary risk, or accept caller classifications? Trace validation and contradictory evidence, and distinguish resolver-test success from real risk assessment. Sufficient evidence is the complete input-to-classification-to-profile path, its documented caller responsibility, and relevant test assertions. Scope is the current local source snapshot at HEAD `4d44cd3ce2889c552d46ca4687596bc4f5298a17`; no installed-host or historical-execution claim is made.

## Method and rationale

Bounded static source tracing fits this factual implementation question. Read the resolver, its shared contract, and relevant resolver tests; source conditions are explicit enough that executing a suite would not resolve an additional consequential uncertainty. No external search, installation, resolver execution, or test execution was performed. No evaluation framework or relationship diagram is needed.

## Findings

**The resolver accepts caller-supplied classifications; it does not independently establish that a task crosses a trust boundary.** Its input is a JSON packet, with no task text, artifact evidence, provenance field, repository inspection, or security analysis in the classification path. The station must classify from evidence before invoking the resolver ([contract, lines 22–26](../../../../../../loom-code/references/dispatch-profile.md#L22)); the resolver checks the supplied predicate names and boolean types ([implementation, lines 71–84](../../../../../../loom-code/scripts/dispatch_profile.py#L71)). This supports a separation between the caller's assessment and the resolver's deterministic routing, rather than independent corroboration.

Validation has real but limited force. `resolve` rejects unknown top-level fields, invalid event names, non-boolean inheritance, and redispatch counts outside integer 0–2. Initial events validate the capabilities map and main-profile shape. `_classify` rejects unknown task-evidence keys and values whose exact type is not `bool`, so strings such as `"true"` and integers such as `1` are invalid. It does not require all predicates, inspect supporting artifacts, or cross-check combinations. Missing predicates default false; null or absent `task_evidence` yields ordinary plus `insufficient-task-evidence`, while an empty object yields ordinary without that uncertainty ([classification](../../../../../../loom-code/scripts/dispatch_profile.py#L71), [event/input boundary](../../../../../../loom-code/scripts/dispatch_profile.py#L260), [initial profile validation](../../../../../../loom-code/scripts/dispatch_profile.py#L127)).

Contradictory classifications are accepted and resolved by precedence, not investigated. If `exact_transformation`, `bounded_targets`, and `mechanical_oracle` are all true, `_classify` returns mechanical immediately, even when `trust_boundary: true` and `inconsistent_evidence: true` are also present. If any mechanical prerequisite is false or omitted, a true trust-boundary or inconsistent-evidence predicate yields complex. `inconsistent_evidence` is itself only a supplied boolean; the function does not discover inconsistency. This matches the documented `mechanical > complex > ordinary` precedence ([implementation](../../../../../../loom-code/scripts/dispatch_profile.py#L80), [contract, lines 136–161](../../../../../../loom-code/references/dispatch-profile.md#L136)). These outputs are source-derived deductions, not measured executions.

For a concrete standard/medium baseline and capabilities supporting economy/medium and frontier/medium, the contradictory all-mechanical-plus-risk packet requests economy/medium; removing one mechanical prerequisite requests frontier/medium. The initial route lowers one model tier for mechanical, raises one for complex below frontier, and preserves ordinary; unsupported target pairs produce atomic fallback instead. Thus a risk flag is not an unconditional safeguard against lowering the model ([initial routing](../../../../../../loom-code/scripts/dispatch_profile.py#L147), [capability/fallback decision](../../../../../../loom-code/scripts/dispatch_profile.py#L87)). At frontier, complex low or medium resolves to medium; inherited high and higher values remain unchanged.

## Evidence and test meaning

The test helper supplies classifications directly as keyword booleans, along with a fixed capabilities map ([tests, lines 20–35](../../../../../../loom-code/tests/test_dispatch_profile_resolver.py#L20)). Mechanical-route tests assert expected tier arithmetic; the insufficient-evidence test asserts ordinary fallback ([tests, lines 176–204](../../../../../../loom-code/tests/test_dispatch_profile_resolver.py#L176)). The CLI test checks successful JSON output equals `resolve(payload)` and malformed JSON returns code 2 with empty stdout ([tests, lines 559–580](../../../../../../loom-code/tests/test_dispatch_profile_resolver.py#L559)). Its expected result partly comes from the same resolver, so it establishes CLI/function agreement rather than independent semantic correctness.

If successfully executed, those tests would establish the listed assertions for their supplied fixtures in that execution environment. A focused contradictory-input test could additionally establish the actual precedence for that synthetic packet. Neither would establish that a real task's boolean labels are true, that a genuine trust boundary was discovered, that the caller retained supporting evidence, that host capabilities were actually verified, that the requested model was actually invoked, or that the resulting work met acceptance conditions. Even `execution-succeeded` follows caller-supplied completed/success/conforming booleans ([feedback handling](../../../../../../loom-code/scripts/dispatch_profile.py#L164)); that result is not an independent acceptance test. Reading these test definitions does not establish that any test ran or passed.

## Decision impact

Treat a successful resolver result as validated packet processing and routing under supplied classifications, not as evidence that a task really has a trust-boundary risk. The existing division assigns risk assessment to the caller. The apparent contradiction does not establish a contract violation: mechanical precedence is explicitly documented. Whether that precedence should change is a separate policy/design decision requiring intended outcomes and authorized change scope; this investigation does not recommend or implement a change.

## Limitations and open questions

No runtime probe, host integration, complete suite, or historical test output was inspected. The study establishes this resolver's source behavior, not the quality of every station's upstream risk assessment or adapter verification. The inspected working files may include local changes; the HEAD identifier locates repository history but is not a claim of a clean tree or commit-exact file identity. Revalidate if these files or the precedence policy change. Local links were checked to resolve to the intended files and valid line anchors; no rendered Markdown UI check was performed.
