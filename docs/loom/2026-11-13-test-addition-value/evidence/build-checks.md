# Build checks before behavioral dogfood

Tested functional commit: `992a3048de769c2a65132cd3de54bba2cd9ae0a7`.
Baseline: `fbdc29af358413bc9d55b599231b2a6cbcb4524d`.

## Implemented scope

Three existing guidance files were changed; their net word additions are 59
(write-plan), 20 (implementer) and 30 (tests review lens), totaling 109.
The existing test file changed only its release-version constant. No permanent
test functions or executable production functions were added or removed.
The required ten-file release packet is synchronized to loom-code 3.73.0.

## Observed executions

- Task-focused checks: 43, 49 and 12 passing tests for the three guidance tasks;
  the release task ran 43 passing metadata/contract tests and the manifest
  synchronizer's `--all --check` successfully.
- Fresh adversary: five attack points, zero attacks earning a new program,
  zero programs committed, no findings. It reused the existing concern-marked
  `loom-code/tests/test_test_budget_text.py`; its combined focused run reported
  63 passed. Its temptation reading was source inspection, not an actor trial.
- Complete package command, exit 0:
  `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
  Across 15 pytest sessions: 4,263 passed and 11 skipped. The same inventory's
  shell tests and Mermaid checks completed successfully, including parsing all
  13 example blocks and rejecting the deliberate invalid block.
- Portable replay of the reused adversarial artifact, exit 0, 2 passed:
  `uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest loom-code/tests/test_test_budget_text.py -q`.
- Standard `sync-trunk` observed the feature branch already containing the
  fetched origin/main at the baseline revision, without adding a commit.
- Read-only GitHub protection check confirmed main requires a PR and
  `loom-pr-floor / PR floor`, including for administrators. No rules were changed.

## Historical checkpoint before dogfood consent

Actual behavioral dogfood has not started. Automatic approval rejected the
initial native Codex harness call before execution because explicit consent
for the concrete unpublished instruction packet and OpenAI destination was
missing. A bounded consent question remains pending. It must not be bypassed
through another executor or indirect invocation. No model call from that
blocked harness attempt ran.

The prior one-time Claude plan review is separate, completed evidence and does
not authorize any additional Claude call. Its non-conforming formal verdict
does not replace the required closing review.

Independent acceptance testing, final content reviews, finalization, publication
and merge remain pending. The local checks above do not establish actual agent
behavior, installed-host behavior, or the user's conditional merge prerequisite.
No attestation or dogfood-pass claim is made here.

## Subsequent progress

The user subsequently consented to the bounded OpenAI dogfood allocation.
All 65 CLI attempts, including environment and argument failures, are accounted
for in `dogfood.md`; no additional Claude review ran. That report distinguishes
observable behavior, unverified narratives and incomplete station boundaries.

Main advanced to `01fa41b35` during dogfood. Its 3.72.1 test-environment fixes
were merged in `07c8b75b1`, preserving both changelog sections and the feature's
3.73.0 version packet. All ten conflicts were version strings except the
changelog, where both entries were retained. The three behavior-guidance
files were unchanged. The portable reused adversarial command passed again
(2 passed) after integration. The complete package command then exited zero
on that integrated content: 15 pytest sessions totaled 4,273 passed, with
no skips reported; the discovered shell suites passed, all 13 Mermaid blocks
parsed and the deliberate invalid block was rejected. Local combined output:
`/private/tmp/loom-test-addition-package-after-sync.log` (not a portable dependency).
The subsequent `sync-trunk` observation was up to date at origin/main
`01fa41b35501644637262639517e7cb54e5d5e7b`; write-plan intake also passed.
