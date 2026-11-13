# Help-first CLI result consistency — plan
intent: 2026-11-13-cli-result-contract@2f29db8ab63a49c5b69decf2973d201112e63f59
spec: docs/loom/2026-11-13-cli-result-contract/spec.md (current narrowed revision)
charter: 1.1

Current-state evidence and design decisions are in the [spec](spec.md).
The [corrected sixteen-command baseline](evidence/help-conformance.md) and
[retained research](../research/2026-11-13-cli-agent-design-guidelines.md)
are development evidence. No ratified ARCHITECTURE.md exists in this checkout.

## Task DAG

### Wave 1 — Completed help and retained independent checkpoint

**W1-01 Accurate exact help at the public entry**  after: none  acceptance: 1, 3, 4
- Files: `loom-code/scripts/loom_checker.py` (entry: main), `loom-code/tests/test_loom_checker_cli.py`, `loom-code/tests/test_loom_python_runtime.py`, `docs/loom/2026-11-13-cli-result-contract/evidence/help-conformance.md`
- Test: A1 positive: help-source-conformance; boundary: advisory-and-partial-effects. A3 positive: six-help-preserved; negative: nonexact-help-ordinary-parsing. A4 positive: sixteen-help-pairs; negative: handler-stdin-subprocess-tripwires.
- Risk: REQ-1/3/4 discovery decisions; agent-decided reuse COMMAND_HELP without another registry. Preserve existing CLI/runtime tests' exercised behavior, including exact-only matching and startup exit 86. Add failing public-entry tests before changing help.

**W1-02 Independent help-content checkpoint**  after: W1-01  acceptance: 1, 2, 4
- Files: `docs/loom/2026-11-13-cli-result-contract/evidence/help-checkpoint.md`, `docs/loom/2026-11-13-cli-result-contract/evidence/help-conformance.md`
- Test: A1 positive: sixteen-source-readback; negative: misleading-effect-or-exit. A2 positive: source-accurate-guidance; negative: operational-overclaim. A4 positive: two-spellings-ready-discovery; boundary: outside-repository-no-runtime-repair.
- Risk: REQ-1/4 help-first decision; agent-decided independent verifier compares all pages with handlers and authentic outputs. This is the specified content checkpoint, not another formal closing review. Completed correction/recheck evidence is retained; do not relabel the initial failure.

Wave 1 implementation and corrections are committed through `380792416`.
The initial failed checkpoint and passing correction/recheck remain unchanged.
The later two-command JSON tasks W2-01/W2-02 are retired by the user's narrowed
scope, not completed or skipped verification. No replacement JSON task exists.

### Wave 3 — Release packet and branch-end verification

**W3-01 Complete minor release metadata packet**  after: W1-02  acceptance: 3
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A3 positive: release-metadata-synchronized; negative: stale-release-pin-detected.
- Risk: REQ-3 compatibility; agent-decided release 3.73.0 before attestation. Update dated CHANGELOG, sync derived manifests via scripts/sync_codex_manifests.py --all, rewrite version pin and root plus three-language README versions. Preserve other localized content; test_readme_version_matches_manifest covers language parity.

**W3-02 Adversarial and integration evidence**  after: W3-01  acceptance: 1, 2, 3, 4
- Files: `docs/loom/2026-11-13-cli-result-contract/evidence/probes/`, `docs/loom/2026-11-13-cli-result-contract/evidence/build-verification.md`
- Test: A1 positive: inventory-current; boundary: effects-caveats. A2 positive: help-source-accuracy; negative: operational-overclaim. A3 positive: package-suite; negative: legacy-regression. A4 positive: safe-discovery; negative: execution-tripwire.
- Risk: REQ-1/2/3/4 verification; agent-decided independent adversary reuses qualified tests without green-padding. Rerun complete package suite and declared probes after fixes; preserve failures. No live writers or paid calls.

**W3-03 Correct superseded discovery documentation**  after: W3-02  acceptance: 1, 4
- Files: `README.md`, `docs/loom/research/2026-11-13-cli-agent-design-guidelines.md`, `docs/loom/2026-11-13-cli-result-contract/plan.md`
- Test: A1 positive: historical-inventory-labelled; boundary: current-versus-retained-snapshot. A4 positive: all-command-help-discovery; negative: superseded-six-help-guidance.
- Risk: REQ-1/4 acceptance finding; agent-decided advertise all sixteen exact-help pairs while preserving six failure hints and readiness limits. Label historical research snapshots without rewriting original rows or acceptance reports. Rerun integration and independent acceptance after correction.

**W3-04 Repair canonical confirmation provenance**  after: W3-03  acceptance: 1, 2, 3, 4
- Files: `docs/loom/intent/2026-11-13-cli-result-contract.md`, `docs/loom/2026-11-13-cli-result-contract/spec.md`, `docs/loom/2026-11-13-cli-result-contract/plan.md`, `docs/loom/2026-11-13-cli-result-contract/evidence/confirmation-provenance-fix.md`
- Test: A1 positive: canonical-scope-resolution; boundary: historical-baseline-preserved. A2 positive: unchanged-help-requirements; negative: superseded-json-scope. A3 positive: identical-intent-identity; boundary: pin-prefix-equivalence. A4 positive: current-scope-check; negative: stale-confirmation-selection.
- Risk: REQ-1/2/3/4 provenance; agent-decided canonical confirmation records existing user consent without changing scope. Verify equivalent pin identity, current references and confirmation ancestry; preserve historical reports and prior failed evidence.

**W3-05 Retained localized release-version parity**  after: W3-01  acceptance: 3
- Files: `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`
- Test: A3 positive: localized-release-version-parity; negative: stale-localized-version.
- Risk: REQ-3 retained completed release work; agent-decided split localized README ownership from W3-01 to keep exact file inventory within field caps. Existing test_readme_version_matches_manifest covers parity; preserve non-version localized text.

W3-01, W3-02, W3-03 and W3-05 describe already implemented release,
verification and documentation work retained in history. W3-04 is the current
provenance repair. The complete suite/adversary and acceptance/review must run
again on this corrected content; prior success is not finalization success.

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

The user answered 好 to the proposal “先把 help 整理獨立交付，JSON 留下一輪”; original publication authority remains. The prior bounded Claude audit is consumed evidence, not formal outside-review selection or new execution consent.

## Risks
1. User confirmed help-only delivery on 2026-11-13. JSON work is deferred to a separate unconfirmed future change. Remaining work is release packet, adversarial/full-suite verification, acceptance, closing review and authorized publication.
2. Engineering change: decision point ② is exempt and must not be reopened. Plan structure is agent-decided. Automatic publication is already authorized; merge remains separate. Preserve every existing worktree.
3. No runtime provisioning redesign or new JSON for any command. Ready-runtime discovery does not imply --repair is offline. Existing delivery/preparation consumers and hook host responses retain their published contracts.
4. Release metadata, changelog, README strings and pin tests must agree before closing-review finalization. Later functional corrections invalidate prior attestation; never bump the version after attestation and call it current.
5. No JSON performance benefit is claimed. Acceptance must expose limitations and actual failed evidence; source inspection and package success alone cannot prove help explains the real operational consequences.
