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

Which inputs are independently observed, which are caller assertions, and what does that imply for a small integration of existing checks? This extends the [RDM assessment](2026-11-11-recursive-decision-models-for-loom.md) with a distinct input-evidence question. Initial source: checkout `91ee36100708f73af5d1df33107dbf98b91ac44f`, loom-code 3.65.0. The [intake pilot](../intent/2026-11-11-intake-observation-pilot.md) was confirmed on 2026-11-11. Its JSON candidate (`26f3049d`, repaired in `7da5d59`) was subsequently withdrawn after independent consumption showed no benefit over guided text. The final design retains guidance for the existing text interface. Authorization comes from the confirmed intent, not this record. The [comparison](../2026-11-11-intake-observation-pilot/evidence/comparison.md) preserves candidate replay, actual answers and costs.

## Method and rationale

Trace producers, consumers and corroborating checks in local code; vary one input packet at a time in the existing pure resolver. This addresses the actual Loom boundary more directly than another generic model benchmark. No new external search was needed for these local implementation claims. No historical private sessions were read, no external model called, and no production policy changed.

Evidence levels are kept separate: schema validity, source/content identity, independently observed fact, and semantic correctness. A hash answers identity, not truth; a boolean answers shape, not whether the right evidence was considered.

The dispatch resolver is a model/effort policy helper, not a readiness, acceptance or authorization gate. Its caller-supplied classification predicates must not be generalized to every checker input: intake reads canonical artifacts and Git observations, while publication has its own authority checks. These surfaces share a need for trustworthy inputs but perform different jobs.

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

Common input: initial dispatch, standard/medium parent, all three tiers supporting medium, inherited settings guaranteed, zero completed redispatches. Only `task_evidence` changes. Seven synthetic packets ran against the checked-out module with Python; the W2 comparison recipe repeats them. The observed classifications are actual resolver outputs, but their input predicates are constructed assertions, not independently labeled real tasks. No network or production policy mutation is involved.

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

The chosen pilot surface is planning intake, because it already recomputes some facts from artifacts. The unchanged [command](../../../loom-code/scripts/loom_checker/command_handlers/intake.py) accumulates rule/reason pairs; [report](../../../loom-code/scripts/loom_checker/helpers.py) renders blocking lines plus an exit code. The [planning skill](../../../loom-code/skills/write-plan/SKILL.md) now clarifies how to consume that text before and after planning. The JSON trial added in `26f3049d` is historical and removed from the final design. No classifier, second policy engine or new observation format remains.

Important boundary: `cmd_intake` returns early when confirmation fails. A result must not imply that later checks ran. Nor can an intake pass mean that review, acceptance or publication passed: those checks occur elsewhere. Any structured observation should preserve these distinctions and report operational failures distinctly from a successful observation.

The witnessed guided-text and JSON decisions were equivalent on all six controlled cases; JSON added 445 packet bytes and no observed consumption/error-handling benefit. Guidance-only is therefore selected under the original condition. The sequential single-consumer design does not establish universal equivalence, reduced model calls or faster total execution.

### Historical complexity estimate and final choice

Mode: complexity. Mindset: Data over abstractions, favoring ordinary result data over a new controller.

1. Smallest end state: one existing intake observation supplies the results the calling station needs, using the same check functions. No global scheduler, classifier service, durable result database or second rule table. Keep existing text consumers compatible.
2. The initial baseline intake handler was 101 lines and its test module 2,012 lines. The initial estimate was 30–80 net production lines, 60–140 test lines, 5–20 guidance lines, 0–1 helpers and no new production module. Historical W1 (`26f3049d`) added 40 net handler lines, 67 test lines and 9 guidance lines, plus two helpers. The duplicate-option repair later added 2 net handler and 6 regression lines, with a 24-line adversarial probe. The final guidance-only choice removes the trial handler/help and implementer-owned tests; the independent adversary re-evaluates its probe. Historical work is a sunk implementation/verification cost, not erased by removing the candidate. Release metadata is separate.
3. At the initial assessment no safe deletion was identified. The final choice removes only this trial's format implementation and its owned tests, restoring the previous checker bytes. It does not remove unrelated existing behavior or introduce a duplicate parser of `BLOCK` strings.

The initial research recommendation was **PROCEED-WITH-CAVEAT** for a bounded comparison. The measured no-benefit result now selects guidance-only; inspectability alone did not justify retaining added reporting/test surface. This design decision is not a fresh acceptance verdict for the revised tree.

## Decision impact

Recommend provenance appropriate to each input, not a universal evidence wrapper:

- Derivable facts: obtain them from their actual source and reuse existing validators.
- Semantic predicates: retain judgment and its supporting artifacts; do not quietly turn absence into a proven negative in new observations.
- Execution results: distinguish process return code, structural validity and semantic acceptance.
- User authority: preserve explicit consent; neither source hashes nor classifier scores prove it.

Changing dispatch unknown-handling or mechanical precedence is a separate policy change and is not smuggled into the intake pilot. The research supports targeted future evaluation of those predicates, with independent task labels, held-out cases, abstention/unknown behavior and false-negative risk metrics. Synthetic packet perturbations alone are insufficient evidence to change model routing.

## Limitations and open questions

No task corpus was labeled and no actual agent classification accuracy was measured. The [independent candidate acceptance](../2026-11-11-intake-observation-pilot/evidence/acceptance-test-evidence.md) replayed all seven synthetic inputs, inspected the research's local source claims and consumed all three output arms; it found no JSON benefit. No exploit, missed consent or production misroute was demonstrated. The seven cases validate packet handling, not truth. Historical W1's 206 focused passes and candidate acceptance's 377 passes are not semantic accuracy results. The revised guidance requires fresh acceptance; this record claims no latency/token savings or actual host dispatch. Keep input quality, rule correctness, output consumption and host execution separate.
