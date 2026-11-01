# Independent review request — plan for the five skill/checker consistency defects

You are the second independent reviewer (OpenAI Codex, provider family different from the plan-lens reviewer that already PASS_WITH_NOTES'd this plan). Your job: adversarially review the implementation plan for a confirmed loom change, checking that every task is necessary and minimal, that its Files lists are complete and exact, and that nothing smaller still satisfies the intent's Acceptance lines. Do not trust this packet's framing — read every cited file yourself.

Repository root (your working directory): the review root. All paths below are relative to it. Current branch `consistence-review-2`, HEAD `bfbd7285` (clean tree).

Ground truth:
- Intent (confirmed 2026-10-26): `docs/loom/2026-10-26-five-skill-consistency-defects.md` — six numbered Acceptance lines under `## Acceptance`.
- Plan under review: `docs/loom/2026-10-26-five-skill-consistency-defects/plan.md` — six tasks in two waves.
- Evidence that confirmed the five defects: `docs/loom/2026-10-26-five-skill-consistency-defects/evidence/` (first-review-packet.md, first-review-result.json, second-review-result.md).

## Your task

For each task W1-01..W2-02, return:
1. `verdict` — exactly one of:
   - `necessary-and-correct` — the task is needed and minimal for its Acceptance lines;
   - `correct-with-smaller-repair` — a smaller or different shape is better (name it);
   - `wrong-direction` — the repair would weaken a rule or fix prose by changing behavior;
   - `not-needed` — the task or a named part of it can be deleted and its Acceptance lines still hold.
2. `why` — 1-3 sentences citing file:line you actually read.
3. `files-issues` — any entry in the task's Files line that is (a) missing (a consumer the change must touch that the line does not name) or (b) surplus (a file the task can complete without). Verify against the actual code, not the plan's description.
4. `test-issues` — is the Test pair observable against the real checker (for W1-01) or against the pinned prose tests (W1-02..W1-04)? Name any test the repair must change that the plan's Files line omits.
5. `new-conflict` — any contradiction the repair would create with unmodified text, named file:line.

Then two short sections:
- `Missed scope` — anything the plan should touch to satisfy an Acceptance line but does not (e.g. a consumer of the attestation execution-kind list, a second file pinning the same prose).
- `Cross-fix interactions` — fixes that must land together or touch the same contract.

Report in English. Be adversarial: the value is finding where the plan is wrong, not agreeing with it.

## Points of particular doubt (check these, do not accept the plan's claim)

1. **W1-01's marker execution row.** The plan chooses a `no-program` marker execution row (kind `adversarial-no-program`, no artifact, carries `reason`) over a new attestation schema version, claiming it is smaller. Verify against `loom-code/scripts/loom_checker/attestation.py` (exact key-set schema check at line ~132, execution-kind branch at ~170), `loom-code/scripts/loom_checker/intent_state.py:148` (delivery-witness kind allowlist), and `loom-code/contract/manifest.yaml:202` (executions grammar). Is the marker-row read smaller than schema v3 when the contract manifest grammar, the attestation template, `test_contract_manifest.py::test_manifest_declares_generated_attestation`, and `test_loom_attestation.py` are all in scope either way? Is there a third path that is smaller still?
2. **W1-04 includes template 08's subgraph heading.** Acceptance 4 says "every loom-visualization chat template that draws a node-label separator uses exactly six U+2501 characters". Template 08's separator sits in a `subgraph P[...]` heading label, not a node label. Is including 08 justified (read `loom-workflow/skills/loom-visualization/references/node-structure.md:51-63` and `references/mermaid-cot-spec.md:190-208`), or is it scope creep the acceptance does not cover?
3. **W1-02's prose rewording.** The intent's constraint says the adversarial protocol must gain no case-count floor (enforced by `loom-code/tests/test_adversary_protocol.py`). Check the planned prose changes against `loom-code/skills/closing-review/references/adversarial.md:49-52, 72-78, 145-147` and the scan grammar in `test_adversary_protocol.py` (case/probe/program head nouns only). Does any natural rewording of "spends nothing against the ceiling" risk tripping the floor scan or the one-home scan?
4. **W2-01/W2-02 bump scope.** The attestation executions grammar changes (W1-01) and station guidance changes (W1-02, W1-03). Repo policy requires minor bumps for both affected plugins. Is loom-workflow 5.16.0 and loom-code 3.50.0 right, or does anything else (loom-design? the contract manifest version at `loom-code/contract/manifest.yaml:1`?) also need a bump the plan omits?
5. **W1-03 equivalence outcome.** The plan records the equivalence outcome only in prose plus a pin test. Is extending Reconcile's trigger (SKILL.md:143-145, operations.md:90-95) the smallest repair that satisfies Acceptance 3, or does the Record step's own routing text also need to change?
