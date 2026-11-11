---
title: "Where Loom mechanical decisions still depend on input judgment"
type: loom-research
status: concluded
created: 2026-11-11
updated: 2026-11-11
tags:
  - loom/research
---

# Where Loom mechanical decisions still depend on input judgment

## Question and scope

Which inputs are independently observed, which are caller assertions, and what does that imply for a small integration of existing checks? This extends the [RDM assessment](2026-11-11-recursive-decision-models-for-loom.md) with a distinct input-evidence question. Applicable source: checkout `91ee36100708f73af5d1df33107dbf98b91ac44f`, loom-code 3.65.0. The proposed [intake pilot](../intent/2026-11-11-intake-observation-pilot.md) is still open; no implementation is authorized by this record.

## Method and rationale

Trace producers, consumers and corroborating checks in local code; vary one input packet at a time in the existing pure resolver. This addresses the actual Loom boundary more directly than another generic model benchmark. No new external search was needed for these local implementation claims. No historical private sessions were read, no external model called, and no production policy changed.

Evidence levels are kept separate: schema validity, source/content identity, independently observed fact, and semantic correctness. A hash answers identity, not truth; a boolean answers shape, not whether the right evidence was considered.

## Findings

### Input provenance and its limits

| Input | Producer / actual validation | What remains unproved | Suitable treatment |
|---|---|---|---|
| `exact_transformation`, `bounded_targets`, `mechanical_oracle` | Calling station supplies booleans; resolver checks field names/types | That the transformation is exact, the target set complete, and the oracle sufficient | Keep semantic classification explicit; an executable oracle plus tested scope can support but not universally prove these predicates |
| `trust_boundary`, `multiple_plausible_causes`, `irreversible_decision`, `inconsistent_evidence` | Calling station supplies booleans | Whether a relevant boundary, competing cause or conflicting evidence was missed | Evidence-backed judgment; distinguish unknown from a supported negative in any future policy proposal |
| `changed_consumed_interface` | Caller assertion in dispatch; separate intake logic can inspect declared interface-path globs | A path match is not proof of changed semantics or actual downstream consumption | Use Git facts as supporting observations, not an automatic semantic equivalence |
| `capabilities`, `main_profile`, inheritance | Host adapter/caller supplies observations; resolver checks supported portable combinations | Actual host model/effort and freshness of reported support | Prefer actual host responses/receipts; preserve unverified fallback instead of guessing |
| `completed`, `success`, `conforming`, failure kind, retry count | Caller feedback; resolver checks shape and legal transitions | That acceptance was really met or past attempts were accurately counted | Retain execution evidence; separate process completion, usable output and accepted behavior |
| Intake confirmation/status | Parses canonical files and examines Git delivery history | A recorded user confirmation is not an independently authenticated transcript of consent | Preserve the human confirmation process; do not treat a valid status string as permission to invent consent |
| Interface changes and content identity | Git-derived paths/hashes, evaluated against manifest declarations | Semantic coverage outside declared paths; changes after observation | Record observation scope and recheck when relevant inputs change |
| Publication authority | Canonical committed intent field plus working-copy revocation check | Whether the original field truthfully represented consent | Existing consent contract remains authoritative; a prediction or high confidence cannot manufacture authority |

Source anchors: [dispatch resolver](../../../loom-code/scripts/dispatch_profile.py) `_classify`, `_capabilities`, `_initial`, `_after_execution`; [dispatch contract](../../../loom-code/references/dispatch-profile.md) Inputs and record / Executable resolver; [intake checks](../../../loom-code/scripts/loom_checker/rule_checks/intake.py) `check_confirmed`; [interface checks](../../../loom-code/scripts/loom_checker/rule_checks/intent.py) `touched_interface_surfaces`, `check_kind_recompute`; [intent content pin](../../../loom-code/scripts/loom_checker/rule_checks/intent_version.py) `pinned_confirmation`, `check_intent_version`; [content digest](../../../loom-code/scripts/loom_checker/digest.py) `functional_content_digest`; [publication](../../../loom-code/scripts/loom_checker/command_handlers/publish.py) `_intent_authorizes_publication`.

### Executed input perturbation

Common input: initial dispatch, standard/medium parent, all three tiers supporting medium, inherited settings guaranteed, zero completed redispatches. Only `task_evidence` changes. Seven cases ran against the checked-out module with Python; no network or repository mutation.

| Case | Supplied evidence | Observed result |
|---|---|---|
| Missing | `null` | ordinary, standard/medium, `insufficient-task-evidence` |
| Empty | `{}` | ordinary, standard/medium, uncertainty `null` |
| Explicit negative | `trust_boundary: false` only | ordinary, standard/medium, uncertainty `null` |
| Risk assertion | `trust_boundary: true` only | complex, frontier/medium |
| Mechanical assertions | all three mechanical fields true | mechanical, economy/medium |
| Mixed assertions | all three mechanical fields true plus `trust_boundary: true` | mechanical, economy/medium |
| Field-level unknown | `trust_boundary: null` | rejected: task evidence values must be booleans |

Reproduction, from repository root:

```python
import sys
sys.path.insert(0, "loom-code/scripts")
import dispatch_profile as d
base = {
    "event": "initial", "main_profile": {"model": "standard", "effort": "medium"},
    "capabilities": {tier: ["medium"] for tier in d.MODELS},
    "inheritance_guaranteed": True, "completed_redispatches": 0,
}
mechanical = dict.fromkeys(d.MECHANICAL_FIELDS, True)
for evidence in (None, {}, {"trust_boundary": False}, {"trust_boundary": True},
                 mechanical, {**mechanical, "trust_boundary": True}, {"trust_boundary": None}):
    try:
        result = d.resolve({**base, "task_evidence": evidence})
        print(evidence, result["task_class"], result["uncertainty"], result["effective_profile"])
    except d.InputError as error:
        print(evidence, str(error))
```

Interpretation:

- Omitting all evidence and supplying an empty object select the same profile but expose different uncertainty. Missing fields in an object act as false, so the result cannot distinguish unexamined predicates from examined negatives. This is a confirmed representation limitation, not a measurement of real-world misrouting.
- Mixed mechanical/risk assertions select the cheaper model by **documented precedence** (`mechanical > complex > ordinary`). This is not an implementation/contract mismatch. A bounded, exactly checkable transformation may legitimately touch a trust boundary. Whether precedence is appropriate depends on the strength of the claimed oracle; this experiment does not settle that policy question.
- A caller can obtain a different profile by changing uncorroborated booleans. That demonstrates reliance on the caller; it does not establish an exploitable security vulnerability or that current agents routinely supply bad data.
- The same reasoning applies to post-execution `success`: the resolver trusts the typed observation. It is not itself an acceptance evaluator.

## Implications for the pilot

The best first surface is the planning intake observation, because it already recomputes some facts from artifacts. [Current command](../../../loom-code/scripts/loom_checker/command_handlers/intake.py) accumulates rule/reason pairs, but [report](../../../loom-code/scripts/loom_checker/helpers.py) renders only blocking lines plus an exit code. The [planning skill](../../../loom-code/skills/write-plan/SKILL.md) already requires intake before and after planning. The proposed integration therefore reuses an existing call path, rather than adding a classifier or a second policy engine.

Important boundary: `cmd_intake` returns early when confirmation fails. A result must not imply that later checks ran. Nor can an intake pass mean that review, acceptance or publication passed: those checks occur elsewhere. Any structured observation should preserve these distinctions and report operational failures distinctly from a successful observation.

Potential benefit is more reliable consumption and less reinterpretation of check output. Neither a reduction in parent-model calls nor faster total execution has been established. A text-only caller guidance change with zero production-code growth is a valid comparison arm; structured output earns its cost only if it improves the measured result or error handling.

### Complexity review of the proposed scope

Mode: complexity. Mindset: Data over abstractions, favoring ordinary result data over a new controller.

1. Smallest end state: one existing intake observation supplies the results the calling station needs, using the same check functions. No global scheduler, classifier service, durable result database or second rule table. Keep existing text consumers compatible.
2. Baseline production intake handler is 101 lines; the existing intake test module is 2,012 lines. No patch exists yet, so final counts are unknown. Rough planning allowance, not a measured diff: 30–80 net production lines, 60–140 test lines, 5–20 guidance lines, 0–1 new production helper functions, no new production module. Count release metadata separately. A wrapper/controller would add avoidable surface; the 0-production-line guidance-only alternative must be tested too. Revisit if the estimate expands materially.
3. Verified safe deletions now: none. No claim of net simplification by LOC. A new duplicate parser of `BLOCK` strings should not be introduced; redundant caller instructions may be removable only after consumer inspection.

Verdict: **PROCEED-WITH-CAVEAT** for a bounded existing-command integration and comparison, not a new orchestration framework. Added reporting/test surface buys inspectable evidence consumption; measured benefit is still pending. If guidance-only performs equally well, prefer it or record no-benefit rather than expand scope.

## Decision impact

Recommend provenance appropriate to each input, not a universal evidence wrapper:

- Derivable facts: obtain them from their actual source and reuse existing validators.
- Semantic predicates: retain judgment and its supporting artifacts; do not quietly turn absence into a proven negative in new observations.
- Execution results: distinguish process return code, structural validity and semantic acceptance.
- User authority: preserve explicit consent; neither source hashes nor classifier scores prove it.

Changing dispatch unknown-handling or mechanical precedence is a separate policy change and is not smuggled into the intake pilot. The research supports targeted future evaluation of those predicates, with independent task labels, held-out cases, abstention/unknown behavior and false-negative risk metrics. Synthetic packet perturbations alone are insufficient evidence to change model routing.

## Limitations and open questions

No task corpus was labeled, no actual agent classification accuracy measured, and no independent reviewer assessed these conclusions in this research pass. No exploit, actual missed consent or production misroute was demonstrated. The seven cases validate the resolver's handling of supplied packets, not their truth. No latency/token savings, full package test run, host dispatch execution or pilot end-to-end result is claimed. A future benchmark must separate input quality, rule correctness, output consumption and host execution instead of reporting a single success rate.
