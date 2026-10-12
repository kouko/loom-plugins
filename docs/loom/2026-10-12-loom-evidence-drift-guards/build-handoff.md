# Loom evidence drift guards — build handoff

The plan has been successfully created and checked:

## Status
- Intent confirmed: `docs/loom/intent/2026-10-12-loom-evidence-drift-guards.md`
- Plan committed: `docs/loom/2026-10-12-loom-evidence-drift-guards/plan.md`
- All intake checks pass
- All plan checks pass
- Second-vendor evaluation obtained and recommendation added to Risks

## Next Station: Build
The change is now ready for the build station (`loom-code:build`), which will:
1. Dispatch implementers for each task in the plan (W1-01 through W2-01)
2. Run focused tests after each task
3. Execute integration checks (package suite, adversarial programs)
4. Hand off to closing-review for final verification

## Implementation Summary
This loom mechanism change addresses six identified drift guards:
1. Acceptance test report coverage enforcement
2. Tested/reviewed commit identity verification  
3. Intent version frozen-at-confirmation check
4. Plan Risk → boundary test mapping enforcement
5. Verdict filing in change directory with attestation link
6. Evidence checks re-run in finalize-review

The mechanism reuses existing attestation schema and publication_only_paths
mechanism, extending attestation with tracking fields and adding checker rules
to validate evidence integrity at various stages of the loom flow.

All implementation details are specified in the plan, ready for the build station
to execute.