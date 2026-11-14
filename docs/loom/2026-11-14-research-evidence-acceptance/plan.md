# Evidence conditions for engineering research — plan
intent: 2026-11-14-research-evidence-acceptance@4dc4d7daf
spec: docs/loom/2026-11-14-research-evidence-acceptance/spec.md@dbff5bb0d
charter: 1.1

Current-state evidence and agent decisions are in the [spec](spec.md). Its
required independent pre-build review passed before this draft. This engineering
change is exempt from decision point ②. No ratified `ARCHITECTURE.md` exists.

## Task DAG

### Wave 1 — Freeze comparison inputs and collect the unchanged baseline

**W1-01 Freeze behavioral cases and run baseline actors**  after: none  acceptance: 7
- Files: `docs/loom/2026-11-14-research-evidence-acceptance/evidence/`
- Test: A7 positive: baseline-actual-receipts; negative: missing-output-not-success.
- Risk: REQ-7; agent-decided reuse framework C01/C02/C04/C06 and genuine artifacts, add only recommendation-follow-up and bidirectional-complexity cases. Freeze cases, rubric, baseline bytes and environment before actors. Existing package/routing cases remain unchanged; no activation benchmark.

Reuse case definitions at
`docs/skill-dogfood/2026-11-08-engineering-research-frameworks/execution/cases.json`
and inspect the corresponding real `execution/X001/artifacts/src/` and
`execution/X012/artifacts/samples/timing/` inputs. Do not assume an `input/`
directory exists. The unchanged skill snapshot is at
`/private/tmp/loom-research-acceptance-eval/baseline-skill`; preserve it and its
hashes. A frozen change-local case packet references the existing cases by revision/hash
and retains the added follow-up/complexity prompts and common assessment criteria.
It is retained behavioral evidence, not an unused permanent test fixture or a
test asserting that particular prose strings exist.

Launch every baseline actor before any candidate actor and complete baseline
observations before changing runtime instructions. Retain actual prompts, allowed
tools, outputs and record contents. An unchanged baseline may already satisfy
conditions; retain that finding rather than manufacture a RED or improvement.

### Wave 2 — Revise the existing instruction and record surfaces

**W2-01 Apply evidence-condition and justified-complexity guidance**  after: W1-01  acceptance: 1, 2, 3, 4, 5, 6
- Files: `loom-code/skills/engineering-research/SKILL.md`, `loom-code/skills/engineering-research/references/evaluation-selection.md`, `loom-code/skills/engineering-research/templates/research.md`
- Test: A1 positive: concrete-conditions; negative: generic-completion. A2 positive: simple-existing-evidence; negative: forced-eight-workflows. A3 positive: condition-support; negative: source-runtime-confusion. A4 positive: honest-unresolved; negative: lowered-standard. A5 positive: justified-complexity; negative: unnecessary-addition. A6 positive: supported-update; negative: unsupported-reversal.
- Risk: REQ-1–6; agent-decided replace overlapping prose within existing sections, preserve description and metadata, require no new fields or runtime scripts. Existing `test_package.py` coverage is preserved; semantic outcomes are assessed through cases, not wording-pin assertions.

The three edited Markdown files currently total 349 lines. Prefer replacement
and consolidation, with any modest net growth justified by the added behavior;
this is an estimate/complexity check, not a new hard cap. Do not expand optional
purpose prompts into eight separate workflows. Record final instruction size
separately from case evidence and release metadata.

### Wave 3 — Observe candidate behavior and challenge conclusions independently

**W3-01 Run matched candidate cases and independent assessments**  after: W2-01  acceptance: 1, 2, 3, 4, 5, 6, 7
- Files: `docs/loom/2026-11-14-research-evidence-acceptance/evidence/`
- Test: A1 positive: concrete-conditions; negative: generic-completion. A2 positive: simple-existing-evidence; negative: forced-eight-workflows. A3 positive: condition-support; negative: source-runtime-confusion. A4 positive: honest-unresolved; negative: lowered-standard. A5 positive: justified-complexity; negative: unsafe-simplification. A6 positive: supported-update; negative: unsupported-reversal. A7 positive: independent-assessment; negative: semantic-overclaim.
- Risk: REQ-1–7; agent-decided match tasks/model/configuration/tools across arms where observable, preserve deviations, failures and partial results. Independent assessors inspect actual evidence and saved conclusions. No superiority, fixed improvement threshold, host parity or trigger-rate claim follows from case completion.

Use inherited model/effort unless the resolved dispatch policy requires otherwise;
do not invent a served-model identity absent from receipts. The follow-up case
must check both refusal to reverse without support and a supported revision that
updates the saved conclusion. Complexity cases cover unnecessary additions and a
smaller option that fails a mandatory condition. Reuse adequate package checks;
an independent adversary supplies and executes actual abuse/boundary programs
before Build completes. Retain its program and results in the change evidence.

### Wave 4 — Release packet and complete integration verification

**W4-01 Synchronize the minor release and verify the final tree**  after: W3-01  acceptance: 7
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README*.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A7 positive: synchronized-release-and-package-suite; negative: stale-pin-or-regression.
- Risk: REQ-7; agent-decided minor 3.80.0 after integrating origin/main 3bf50711f (3.79.0). Edit SSOT only, regenerate exported manifests, add dated CHANGELOG entry, synchronize all README versions and rewrite CURRENT_VERSION pin. Preserve historical changelog/test assertions before attestation.

Integrate the fetched trunk before Build and retain the actual execution revision;
the earlier source baseline remains historical provenance. Run
`python3 scripts/sync_codex_manifests.py --all` after the SSOT bump. The complete
package suite is
`uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
Run it at Build completion and again through finalization, alongside the retained
adversarial programs. Closing review and independent acceptance testing use the
final committed tree; generated attestation precedes the authorized Ready PR.

## Simplicity check

- Keep the frozen case packet in change-local evidence, reusing historical case definitions instead of adding an unconsumed permanent test JSON — taken

## Questions asked

① — what — 以上是否就是你要實作的範圍？

## Risks

1. The description remains unchanged. Existing routing fixtures are controls, not evidence of improved activation. Actual semantic evidence owns Acceptance #7; package invariants alone cannot establish it.
2. Baseline/candidate variation can confound effects. Preserve source hashes, actual environments, permitted actions and failures; disclose unavailable identity or missing observations instead of inferring equivalence or benefit.
3. Parent source baseline contains 3.78.0; fetched origin/main 3bf50711f contains 3.79.0. Integrate without discarding historical evidence, then release 3.80.0; recompute the release packet if trunk advances again.
4. Earlier private historical-session content is not input for external services. Use bounded genuine-source fixtures and ordinary inherited-host agents; method selection grants no new data-transfer, payment or installation authority.
5. User confirmed automatic non-forced push and Ready PR after required checks. Merge is separate. Keep existing authorization, no-write drafts, frozen-record preservation and linked revalidation behavior; no additional user checkpoint.
