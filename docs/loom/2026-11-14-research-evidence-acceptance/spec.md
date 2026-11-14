# Evidence conditions for engineering research — spec
intent: 2026-11-14-research-evidence-acceptance@f1e9299c4
pre-build-review: required — Changes the portable runtime research contract and its retained-record template; proportionality and evidence-sufficiency behavior need an independent check before implementation.

## Requirements

REQ-1 — Decision-relevant evidence conditions
  WHEN an engineering-research question is established, the capability shall identify the concrete decision-relevant unknowns and the evidence sufficient to answer each under the user's established outcomes and constraints. → Acceptance #1

REQ-2 — Proportionate method selection
  WHEN choosing research activities, the capability shall use only methods and depth warranted by consequential evidence gaps, including simple facts, sufficient existing evidence and mixed questions, without requiring a category selection, fixed workflow or additional user confirmation. → Acceptance #2

REQ-3 — Results answer the evidence conditions
  WHEN returning research findings, the capability shall relate each material evidence condition to supported, unsupported or unresolved findings and their actual evidence, including applicable versions, environments and decision-relevant limits. → Acceptance #3

REQ-4 — Honest unresolved completion
  IF an evidence condition cannot be resolved within permitted investigation THEN the capability shall identify the missing evidence and affected decisions without counting the condition as met or weakening it to claim completion. → Acceptance #4

REQ-5 — Necessary complexity in recommendations
  WHEN recommending a material engineering solution, the capability shall fairly compare credible smaller alternatives under the same outcomes and mandatory constraints, justify important additions and their consequential burdens, and retain necessary complexity when smaller alternatives fail a mandatory condition. → Acceptance #5

REQ-6 — Consistent condition and recommendation changes
  WHEN research conditions or recommendations change, the capability shall explain the evidentiary basis or correction and synchronize the delivered findings and retained record before returning the changed recommendation, without treating a follow-up challenge alone as sufficient evidence. → Acceptance #6

REQ-7 — Observable behavior and preserved boundaries
  WHEN the revised capability is validated, the change shall retain actual case outputs and independent assessments with explicit limits, preserve established source-quality, authorization and general-research behavior, and distinguish semantic observations from mechanical package checks. → Acceptance #7

## Design decision

- **REQ-1, agent-decided:** Refine the existing premise/evidence checks in `SKILL.md`; express the unknown, sufficient observation and decision consequence in ordinary prose within the existing record. This supplies an operational target without adding metadata, identifiers or a new artifact.
- **REQ-2, user-decided:** Keep the single `engineering-research` entry. The eight purposes are optional prompts for deriving evidence conditions, not required labels, eight execution paths or a claim of exhaustive coverage.
- **REQ-2, agent-decided:** Integrate question-purpose prompts into the existing `references/evaluation-selection.md` guidance rather than append a second overlapping taxonomy. Distinguish source location, research object and evidence method; select methods only after the concrete question and sufficient evidence are understood. A simple question may have a single sentence of conditions and findings.
- **REQ-3/REQ-4, agent-decided:** Reuse `Question and scope`, `Method and rationale`, `Findings`, `Evidence`, `Decision impact` and `Limitations and open questions` in the existing template. Conditions belong with the question/constraints; findings explain their disposition, and decision impact explains what remains conditional. Prose or a compact table is allowed; neither a table nor fixed status fields are compulsory.
- **REQ-4, agent-decided:** Keep `status: concluded` as work status, including a candid inconclusive investigation. Completion of permitted research does not imply all conditions passed. State missing observations and which conclusions must remain conditional; do not search indefinitely or silently lower the standard.
- **REQ-5, agent-decided:** Strengthen the existing smaller-alternative comparison rather than add a complexity gate or numeric score. Each important added tool, dependency, process or abstraction must trace to a current need and material operating/maintenance/failure/reversal burden. Keeping the current approach, narrowing scope, reuse and combinations remain candidates where viable; no alternative/deletion quota is introduced.
- **REQ-5, agent-decided:** Compare alternatives at equivalent correctness, security and compatibility obligations. A toy alternative is not a valid simplicity win. An option failing a mandatory condition is excluded rather than compensated by its small size; unsupported superiority remains conditional instead of becoming a recommendation.
- **REQ-6, agent-decided:** Extend the existing record-consistency rule to condition changes. New evidence or correction may refine conditions, with the reason and affected conclusions retained; inability to satisfy a condition is not itself grounds to relax it. Withdraw an unsupported earlier recommendation explicitly. Preserve existing linked revalidation for materially changed versions/environments, frozen-record and no-write handling.
- **REQ-7, agent-decided:** Use bounded actual research cases with independent assessment for evidence conditions, proportionality, recommendation changes and complexity in both directions. Mechanical tests protect package/resource invariants only. Preserve unsuccessful/partial observations; do not claim general efficacy or cross-host support from these cases.
- **Scope, agent-decided:** No new search service, index, runtime script, persistent store, mandatory classification field, user checkpoint or checker gate. Existing source policy, reference-read timing, readback/link verification, source pinning and authorization rules continue to apply. Necessary release metadata updates belong to the implementation plan.

## Alternatives considered

- **Template-only change:** Smaller authored change, but leaves the main instruction and method-selection behavior disconnected from the evidence conditions. Insufficient for the confirmed behavior goals.
- **Append eight mandatory categories/workflows:** Makes labels explicit but duplicates existing question guidance and imposes work on simple/mixed questions. Rejected by the single-entry/proportionality constraints.
- **Add machine-readable condition IDs and a new research gate:** Creates schema and enforcement surfaces without evidence that they can establish semantic support. Outside the confirmed scope.
- **Adopt SourceAtlas or another research dependency:** Improves some retrieval/navigation capabilities without establishing the missing recommendation/readback behavior; introduces unrelated operating and host costs.
- **Leave existing wording unchanged:** Valid comparison baseline. Existing guidance contains the principles, but the recorded unsupported nested recommendation and stale retained conclusion justify testing a concrete application change.

## Current state evidence

- Forward: `loom-code/skills/engineering-research/SKILL.md:11-36` establishes the premise, applicability and evidence gathering but does not explicitly bind concrete unknowns to sufficient observations before selecting methods.
- Reverse: `loom-code/tests/engineering-research/test_package.py:59-74` protects the sole code-owned discoverable package and caller routing; `loom-code/contract/manifest.yaml:34` identifies the existing capability owner.
- Error: `docs/loom/research/2026-11-12-recommendation-evidence-gap.md`, Historical observations, records unsupported nested selection, an unsupported follow-up reversal and a stale retained recommendation despite existing comparison rules. This is historical evidence, not a current failure-rate claim.
- Data: `loom-code/skills/engineering-research/templates/research.md:13-64` already carries question, method, findings, evidence, decision impact and limitations; `SKILL.md:153-159` defines flat metadata and work-status semantics.
- Boundary: `loom-code/skills/engineering-research/SKILL.md:173-187` preserves the owning task, no-new-goal/installation/publication boundary and evidence-versus-execution distinction; `references/evaluation-selection.md:70-72` preserves authorization independently of method selection.

## UI flows

The existing research-record surface remains Markdown; no new command, screen,
API or user decision point is introduced.

- Ask a bounded research question → receive findings that identify what needed clarification, the evidence sufficient to answer it and what the actual evidence permits concluding; the record may stay brief.
- Ask a question already answered by applicable evidence → receive a concise supported answer and retained record without additional searches, experiments or category selection.
- Ask a question whose decisive evidence cannot be obtained → receive the unresolved condition, missing evidence and the decision that must remain conditional; completed investigation is not presented as a satisfied condition.
- Challenge a recommendation or supply changed conditions → receive its supported reaffirmation or an explained correction; a changed conclusion agrees with the updated research record, or links a separately scoped revalidation where required.
- Prohibit saving or lack write access → receive an explicitly unsaved draft with the same substantive findings and limitations, without a false saved-record claim.

In-progress: the existing `in-progress` work status remains available; no new
waiting interaction or progress presentation is specified. Empty/no-evidence is
covered by the unresolved case rather than a fabricated successful finding.
