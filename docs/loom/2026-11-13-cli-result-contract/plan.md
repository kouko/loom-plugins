# Help-first CLI result consistency — plan
intent: 2026-11-13-cli-result-contract@16d9157b027c53df8b82c4b5707024f19bc9a1ee
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
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README.md`, `loom-code/README.ja.md`, `loom-code/README.zh-TW.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A3 positive: release-metadata-synchronized; negative: stale-release-pin-detected.
- Risk: REQ-3 compatibility decision; agent-decided bump loom-code to 3.73.0 in final fix before attestation. Add dated CHANGELOG section describing all-command help and compatibility, sync derived manifests with scripts/sync_codex_manifests.py --all, rewrite version-pin test and README strings. Existing test_readme_version_matches_manifest checks all three language READMEs, so Japanese and Traditional Chinese version strings are included for release parity; their other content stays unchanged.

**W3-02 Adversarial and integration evidence**  after: W3-01  acceptance: 1, 2, 3, 4
- Files: `docs/loom/2026-11-13-cli-result-contract/evidence/probes/`, `docs/loom/2026-11-13-cli-result-contract/evidence/build-verification.md`
- Test: A1 positive: inventory-current; boundary: effects-caveats. A2 positive: help-source-accuracy; negative: operational-overclaim. A3 positive: package-suite; negative: legacy-regression. A4 positive: safe-discovery; negative: execution-tripwire.
- Risk: REQ-1/2/3/4 verification decision; independent adversary writes and executes bounded probes, respecting five-program ceiling and concern headers. Run complete scripts/run_package_tests.py --loom-family after final fixes; no live writer/cleanup or paid calls. Finalization reruns declared checks later.

**W3-03 Correct superseded discovery documentation**  after: W3-02  acceptance: 1, 4
- Files: `README.md`, `docs/loom/research/2026-11-13-cli-agent-design-guidelines.md`, `docs/loom/2026-11-13-cli-result-contract/plan.md`
- Test: A1 positive: historical-inventory-labelled; boundary: current-versus-retained-snapshot. A4 positive: all-command-help-discovery; negative: superseded-six-help-guidance.
- Risk: REQ-1/4 acceptance finding; agent-decided update current README discovery to all sixteen exact-help pairs while keeping the original six failure hints and runtime-readiness boundary. Label the research's retained pre-implementation snapshot and narrowed confirmed intent without rewriting historical rows or prior acceptance reports. Parent reruns integration checks and independent acceptance after this prose-only fix.

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
