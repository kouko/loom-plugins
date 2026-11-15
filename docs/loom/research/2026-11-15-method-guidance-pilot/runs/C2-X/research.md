---
title: "Does dispatch routing establish trust-boundary risk?"
type: loom-research
status: concluded
created: 2026-11-15
updated: 2026-11-15
tags:
  - loom/research
---

# Does dispatch routing establish trust-boundary risk?

## Question and scope

Does `dispatch_profile.py` independently establish a real trust-boundary risk, or route caller-supplied predicates? Sufficient evidence is the input schema, classification precedence, connected route computation, and what resolver tests actually assert. Scope is the current local source at HEAD `4d44cd3ce2889c552d46ca4687596bc4f5298a17`; no claim about an installed copy or historical execution.

## Method and rationale

Bounded source inspection answers this factual implementation question directly. Follow the initial-event entry point through validation, classification and profile selection; compare its contract and representative test definitions. No network or experiment is needed to establish which inputs the function consumes. Contradictory inputs below are source-derived predictions, not executed measurements.

## Findings

**The resolver accepts caller-supplied task predicates; it does not independently establish that a task has a real trust-boundary risk.** The contract assigns evidence-based classification to the calling station ([contract, lines 22–26](../../../../../../loom-code/references/dispatch-profile.md#L22)). The executable receives booleans, not task artifacts, security analysis or provenance sufficient to establish their truth ([classifier, lines 71–84](../../../../../../loom-code/scripts/dispatch_profile.py#L71)).

1. **Validation establishes packet shape.** `resolve` requires an object, rejects unknown top-level fields, validates event, boolean inheritance and an integer redispatch count in 0–2. For an initial event it validates the capability map and then calls `_initial`; `_initial` calls `_classify`. The classifier allows only the three mechanical and five complex predicate keys and requires actual booleans, rejecting strings or integer substitutes. None of these checks proves the predicates correspond to the real task ([entry point, lines 263–299](../../../../../../loom-code/scripts/dispatch_profile.py#L263), [classifier](../../../../../../loom-code/scripts/dispatch_profile.py#L71), [initial route](../../../../../../loom-code/scripts/dispatch_profile.py#L127)).

2. **Contradictory evidence is resolved by precedence, not investigated or rejected.** For a valid initial packet with observable `standard/medium` and supported targets:
   - `trust_boundary: true` alone produces `complex` and requests `frontier/medium`.
   - All of `exact_transformation`, `bounded_targets`, and `mechanical_oracle` true, together with `trust_boundary: true`, produces `mechanical` and requests `economy/medium`. Even adding `inconsistent_evidence: true` does not change that result: the all-mechanical branch returns first.
   - `trust_boundary: false`, or an empty evidence object, gives `ordinary` and preserves `standard/medium` unless some other complex predicate is true. The resolver cannot detect a real risk omitted by its caller.
   - Missing or null `task_evidence` gives `ordinary` with `insufficient-task-evidence`; an empty object instead gives ordinary with no uncertainty marker. A nonboolean predicate or unknown evidence key raises `InputError`.

   These are static deductions from [classification order, lines 71–84](../../../../../../loom-code/scripts/dispatch_profile.py#L71) and [profile arithmetic, lines 147–160](../../../../../../loom-code/scripts/dispatch_profile.py#L147). The contract explicitly specifies `mechanical > complex > ordinary`, so this overlap is not itself evidence of a code/contract mismatch ([classification contract, lines 139–160](../../../../../../loom-code/references/dispatch-profile.md#L139)). Whether such precedence is appropriate for a real security-sensitive task is a separate policy question.

3. **Routing remains conditional on the supplied profile and capabilities.** Unsupported target pairs produce an atomic override-free fallback, rather than prove host support; the resolver checks membership in the caller's capability map ([support/fallback decision, lines 102–124](../../../../../../loom-code/scripts/dispatch_profile.py#L102)). The CLI parses JSON, calls `resolve`, emits deterministic JSON on success, and reports JSON/InputError failures with exit code 2 ([CLI, lines 302–315](../../../../../../loom-code/scripts/dispatch_profile.py#L302)).

## Evidence and test meaning

The inspected test helper constructs `task_evidence` directly from keyword booleans, with a fixed capability table ([test setup, lines 20–35](../../../../../../loom-code/tests/test_dispatch_profile_resolver.py#L20)). The mechanical routing test asserts class, target tier and dispatch outcome for all three mechanical predicates; the missing-evidence test asserts ordinary classification and its uncertainty marker ([tests, lines 174–204](../../../../../../loom-code/tests/test_dispatch_profile_resolver.py#L174)). Feedback tests likewise construct typed success observations ([feedback helper, lines 39–49](../../../../../../loom-code/tests/test_dispatch_profile_resolver.py#L39)).

A successful resolver test would establish that the exercised implementation returns the asserted routing or rejection for those supplied packets in that test environment. A deliberately added overlap test could establish that mechanical precedence holds for a trust-boundary flag too. Neither result establishes that a real task crosses a trust boundary, that the station gathered truthful/complete evidence, that the host capability map is accurate, that a host actually spawned the requested model/effort, or that the resulting work satisfies acceptance conditions. In particular, successful feedback can return `routed` on caller-supplied completed/success/conforming booleans ([feedback success branch, lines 164–199](../../../../../../loom-code/scripts/dispatch_profile.py#L164)); this is not an independent acceptance evaluation.

## Decision impact

Use this resolver as a deterministic policy calculation and packet-validation component. Do not treat its successful output or passing unit tests as independent certification of task risk. Evidence assessment remains the caller's responsibility; evaluating that caller would require separate source and execution evidence. No implementation change is proposed by this investigation.

## Limitations and open questions

No resolver, test suite, host dispatch, or security scenario was executed. Test definitions are inspected evidence, not passing results. Only the relevant resolver, contract and selected test portions were read; no claim is made about repository-wide test coverage, caller compliance, installed versions or deployment. HEAD was recorded, but no clean-worktree claim is made. The real-world truth of any particular task predicate remains unresolved by design of this interface.
