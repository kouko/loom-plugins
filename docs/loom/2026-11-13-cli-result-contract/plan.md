# Help-first CLI result consistency — plan
intent: 2026-11-13-cli-result-contract@01d73c1a44e889c61c841a055f4dc2aa1158c1c4
spec: docs/loom/2026-11-13-cli-result-contract/spec.md@ddf3959f
charter: 1.1

Current-state evidence and design decisions are in the [spec](spec.md).
The [corrected sixteen-command baseline](evidence/help-conformance.md) and
[retained research](../research/2026-11-13-cli-agent-design-guidelines.md)
are development evidence. No ratified ARCHITECTURE.md exists in this checkout.

## Task DAG

### Wave 1 — All-command help before new JSON

**W1-01 Accurate exact help at the public entry**  after: none  acceptance: 1, 3, 4
- Files: `loom-code/scripts/loom_checker.py` (entry: main), `loom-code/tests/test_loom_checker_cli.py`, `loom-code/tests/test_loom_python_runtime.py`, `docs/loom/2026-11-13-cli-result-contract/evidence/help-conformance.md`
- Test: A1 positive: help-source-conformance; boundary: advisory-and-partial-effects. A3 positive: six-help-preserved; negative: nonexact-help-ordinary-parsing. A4 positive: sixteen-help-pairs; negative: handler-stdin-subprocess-tripwires.
- Risk: REQ-1/3/4 discovery decisions; agent-decided reuse COMMAND_HELP without another registry. Preserve existing CLI/runtime tests' exercised behavior, including exact-only matching and startup exit 86. Add failing public-entry tests before changing help.

**W1-02 Independent help-content checkpoint**  after: W1-01  acceptance: 1, 4
- Files: `docs/loom/2026-11-13-cli-result-contract/evidence/help-checkpoint.md`, `docs/loom/2026-11-13-cli-result-contract/evidence/help-conformance.md`
- Test: A1 positive: sixteen-source-readback; negative: misleading-effect-or-exit. A4 positive: two-spellings-ready-discovery; boundary: outside-repository-no-runtime-repair.
- Risk: REQ-1/4 help-first decision; agent-decided independent verifier compares all pages with handlers and authentic outputs. This is the specified content checkpoint, not another formal closing review. Correct failures before W2 starts; retain failed evidence.

### Wave 2 — Document semantics and add the two read-only data results

W2 starts only after W1-02 independently confirms all sixteen pages. Implementers
must receive its actual evidence, not infer success from passing unit tests.

**W2-01 Shared meanings and supported-mode documentation**  after: W1-02  acceptance: 1, 3
- Files: `loom-code/README.md`, `docs/loom/2026-11-13-cli-result-contract/evidence/help-conformance.md`
- Test: A1 positive: result-family-inventory; boundary: process-versus-domain-success. A3 positive: supported-mode-disclosure; negative: writer-json-overclaim.
- Risk: REQ-1/3 shared-semantics decision; agent-decided use existing README and evidence, not a new runtime registry. Distinguish preparation-v1, delivery, command-data, hooks, CI and text writers; document current support accurately without promising unavailable flags.

**W2-02 Opt-in typed results for contract and reviewer-count**  after: W2-01  acceptance: 2, 3
- Files: `loom-code/scripts/loom_checker.py` (entry: main), `loom-code/scripts/loom_checker/command_handlers/contract.py`, `loom-code/scripts/loom_checker/command_handlers/reviewer_count.py`, `loom-code/scripts/loom_checker/command_data_output.py`, `loom-code/tests/test_command_data_json.py`, `loom-code/tests/test_preparation_json.py`, `loom-code/tests/test_loom_checker_cli.py`, `loom-code/README.md`
- Test: A2 positive: typed-version-and-floor; negative: blocked-usage-internal-json. A3 positive: legacy-text-and-json-parity; boundary: selector-and-hook-isolation.
- Risk: REQ-2/3 later-family decision; agent-decided one small serializer for two handlers, no framework/prose parser. Preserve existing CLI/preparation tests' scope. Test complete stdout and actual computation once; retain dirty-tree exit 2 and conservative floor semantics.

### Wave 3 — Release packet and branch-end verification

**W3-01 Complete minor release metadata packet**  after: W2-02  acceptance: 3
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A3 positive: release-metadata-synchronized; negative: stale-release-pin-detected.
- Risk: REQ-3 compatibility decision; agent-decided bump loom-code to 3.73.0 in final fix before attestation. Add dated CHANGELOG section describing help and bounded JSON, sync derived manifests with scripts/sync_codex_manifests.py --all, rewrite version-pin test and README strings.

**W3-02 Adversarial and integration evidence**  after: W3-01  acceptance: 1, 2, 3, 4
- Files: `docs/loom/2026-11-13-cli-result-contract/evidence/probes/`, `docs/loom/2026-11-13-cli-result-contract/evidence/build-verification.md`
- Test: A1 positive: inventory-current; boundary: effects-caveats. A2 positive: parse-domain-data; negative: fault-contamination. A3 positive: package-suite; negative: legacy-regression. A4 positive: safe-discovery; negative: execution-tripwire.
- Risk: REQ-1/2/3/4 verification decision; independent adversary writes and executes bounded probes, respecting five-program ceiling and concern headers. Run complete scripts/run_package_tests.py --loom-family after final fixes; no live writer/cleanup or paid calls. Finalization reruns declared checks later.

Implementer dispatch applies to every implementation task. Shared dispatcher,
tests and mirrored documentation keep the tasks sequential. W1-02 uses an
independent verifier; W3-02 uses the independent adversary. Build proceeds once
to branch-end closing review after all tasks, adversarial probes and package
suite pass; closing review obtains the required fresh reviewers and authentic
Acceptance evidence, then generates attestation on final committed content.

## Simplicity check
- none found

## Questions asked
1 — what — 按這個更新範圍進行嗎？

## Risks
1. User confirmed help-first ordering. W2 cannot begin until the independent sixteen-command content checkpoint passes; any new factual mismatch returns to W1 correction without disguising it as a green structural test.
2. Engineering change: decision point ② is exempt and must not be reopened. Plan structure is agent-decided. Automatic publication is already authorized; merge remains separate. Preserve every existing worktree.
3. No runtime provisioning redesign or new write-command JSON. Ready-runtime discovery does not imply --repair is offline. Existing delivery/preparation consumers and hook host responses retain their published contracts.
4. Release metadata, changelog, README strings and pin tests must agree before closing-review finalization. Later functional corrections invalidate prior attestation; never bump the version after attestation and call it current.
5. No JSON performance benefit is claimed. Acceptance must expose limitations and actual failed evidence; source inspection and package success alone cannot prove help explains the real operational consequences.
