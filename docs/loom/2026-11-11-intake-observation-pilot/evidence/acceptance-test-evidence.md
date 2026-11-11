# Intake observation pilot — acceptance test evidence

Tried on 2026-11-11, in clean clone `/private/tmp/intake-acceptance-clean2` at `7da5d59bbf49f415dc61fbedcaeb6e494bddc006`. Tester did not implement this change. No important dismissed findings were supplied. This is the first acceptance run.

## Setup and provenance

- Read root README Development and loom-code README runtime instructions. A local clone using hardlinks failed with Operation not permitted; `git clone --local --no-hardlinks /private/tmp/loom-intake-observation-pilot /private/tmp/intake-acceptance-clean2` succeeded, followed by `git checkout --detach 7da5d59bbf49f415dc61fbedcaeb6e494bddc006`.
- `loom-code/scripts/loom-python --ready intake write-plan 2026-11-11-intake-observation-pilot --json` loaded the source launcher and its ready runtime and returned exit 0, state passed, checks_complete true, failures empty, error null. This tests source runtime loading, not installation into another host.
- Initial unprivileged locked uv invocation failed to acquire the user's cache lock. A fresh temporary cache lacked execnet offline. Host Python pytest also failed (pytest unavailable in the clean-checkout interpreter). The authorized escalated uv invocation uses the existing cache and the README's isolated locked requirements; these environment failures are not product failures. No base environment was modified.
- Focused command: `uv run --offline --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_loom_checker_intake.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_intake_repeated_json.py loom-code/tests/test_dispatch_profile_resolver.py loom-code/tests/test_delivery.py`. Result: **377 passed in 58.57s**, exit 0. Captured output: `acceptance-focused.log`.
- The complete package suite was not run by this tester. It is not skipped: `finalize-review` executes `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q` before acceptance and blocks attestation on failure. Build's earlier full-suite and adversary results were supplied by the parent and are not claimed as independently witnessed here.

## 1. Faithful intake observations

- Replayed the exact Python recipe from `comparison.md` in the clean clone, with only its output directory changed to `/private/tmp/intake-acceptance-replay` to preserve original packets. Executed the extracted temporary script using the locked uv environment. No executable probe is committed.
- Result: 5 real CLI pairs, 1 injected control, 6 cases per packet, 7 dispatch inputs. All assertions passed: matched exit codes, blocker rules, JSON states and completeness, and unchanged fixture content. See `acceptance-replay.log` and `replay-*.json`.
- Both supported stations, unavailable inputs, confirmation early exit and repeated flag errors are covered by the focused intake and repeated-option tests. Source-launcher actual invocation passed separately (`acceptance-launcher.json`).
- The crash control is manually injected partial stdout and exit 2, not an executed runtime crash; it establishes the consumer's safe recovery response only.

## 2. Read-only scope and preserved decisions

- Snapshotted SHA-256 bytes for all 3,946 files in the clean clone, including `.git`, immediately before and after the source-launcher intake invocation. No changed, added or removed file was found (`acceptance-launcher.json`). The snapshot itself was written outside the clone.
- The replay additionally checks fixture contents before/after each text/JSON pair. `test_intake_json_readonly` covers fixture Git bytes and changed-input re-evaluation; `test_intake_json_earlyexit` covers incomplete checks on confirmation failure. No station advancement, publication or acceptance command was invoked.
- Actual consumer answers explicitly withhold downstream authority. The research correctly treats a confirmed status field as a record, not independent proof of human consent.

## 3. Actual consumption, costs and adoption decision

Before receiving implementation, fixtures, intent, spec, research or answer key, this tester read only the acceptance role and `packet-text.json`, saved actual answers, then read guided text and saved answers, then JSON and saved answers. The three originals are retained byte-for-byte as `consumer-answer-{text,guided_text,json}.json`; packets, key, initial metrics and dispatch inputs are retained as `consumer-*.json`. They were not overwritten by replay or scoring.

This is **one consumer in a sequential crossover**, in order text → guided text → JSON. Prior guidance can influence the JSON arm. It is not three independent consumers, randomized evaluation, a semantic accuracy benchmark or a causal estimate of format benefit.

Scoring is retained in `consumer-scoring.json`. All arms preserve readiness safety, observed blockers and recovery across six cases. On the five real cases, text resolves completeness in three and correctly leaves two unknown; guided text and JSON resolve all five. Those two unknowns are information limits, not wrong answers. Operational errors mean readiness unknown, even though the construction key encodes not-ready as false. All three answers set crash completeness false; the control key accepts it, but actual crash completion would remain unknown without additional evidence. This is shared uncertainty, not a JSON advantage.

**No consumption or error-handling benefit over guidance-only was observed.** JSON supplies deterministic fields, but that inspectability is not measured consumer improvement. Guidance-only and JSON gave equivalent decisions here. REQ-3 explicitly prefers guidance-only when JSON shows no demonstrable benefit. Retaining the production integration therefore does not meet its adoption condition; recommendation: use guidance-only and retain this no-benefit evidence.

Original packet bytes: text 1,765; guided text 2,236; JSON 2,681. JSON costs 445 more packet bytes than guidance and 916 more than text. Original real CLI output totals: text 650 bytes; JSON 1,435 bytes. No model-token count, total parent-model turns, end-to-end model latency or monetary cost was supplied. Local process durations are single sequential observations with startup/Git effects; no savings is established.

Implementation cost at tested HEAD versus intent commit `241362a4`: handler +44/-2 lines (net 42), checker help +2/-2, station guidance +12/-3 (net 9), intake tests +73, repeated-option tests +24. These are extra maintenance surfaces, not a direct operational-cost conversion. The research's W1-only 40/67/9 counts are explicitly historical and exclude the later duplicate-option repair.

## 4. Input evidence and research scope

- Independently replayed seven synthetic dispatch inputs. Missing → ordinary with insufficient-task-evidence; empty/explicit-negative → ordinary with null uncertainty; risk → complex; mechanical/mixed → mechanical; field null rejected. `replay-input-reproduction.json` matches the original supplied input reproduction exactly.
- Inspected `dispatch_profile.py:71` classification and capabilities validation: missing fields default false, mechanical predicates take precedence, caller booleans are type checked but not corroborated. Read initial and feedback paths; execution success remains caller input.
- Inspected intake confirmation source (`rule_checks/intake.py:802`), interface/path and intent-pin sources referenced by the research, and publication authorization (`command_handlers/publish.py:163`): canonical artifacts/Git observations differ from semantic dispatch assertions; publication checks committed authorization and working-copy revocation.
- Both research records separate source inspection, synthetic execution, inference and unverified host behavior. The seven-case replay supports handling/precedence only, not real-task label accuracy or actual host dispatch. No external video, service or model was executed by this acceptance tester. External architectural claims remain the research's cited documentation claims, not fresh runtime verification.
- Both records require actual incremental benefit before adoption. The original research's pending-consumption wording describes W2 collection; the comparison now links this witnessed result. No research or product source was edited by this tester.

## Finding and recommendation

Important, spec conformance: REQ-3 adoption condition is unmet. The observed guided-text and JSON decisions are equivalent while JSON adds bytes and production/test surface. Prefer guidance-only; do not infer efficiency or consumer benefit from a structured schema. Acceptance 3 is partly satisfied: comparison and honest limitations exist, but the retained implementation does not follow the agreed no-benefit choice. Other acceptance lines work within the explicitly bounded evidence above.
