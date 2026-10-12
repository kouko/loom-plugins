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
1. Dispatch implementers for each task in the plan (W1-01 through W2-05)
2. Run focused tests after each task
3. Execute integration checks (package suite, adversarial programs)
4. Hand off to closing-review for final verification

## Implementation Summary
This loom mechanism change addresses six identified drift guards (reshaped per complexity feedback):
1. Acceptance test report coverage enforcement
2. Tested/reviewed commit identity verification  
3. Intent version frozen-at-confirmation check
4. Plan Risk → boundary test template hint (separate proposal for full enforcement)
5. Verdict filing in change directory with attestation link
6. Evidence checks re-run in finalize-review

The mechanism follows Design-Is-Taking-Apart principles:
- Separates three independent drift checks (what was tested, what version tested, requirements still confirmed)
- Each check uses a single source of truth (direct commit recording, not report parsing)
- Eliminates duplicate storage (acceptance status stored once in attestation)
- Precise evidence file whitelist (only necessary output files excluded)
- Clear intent confirmation definition (excludes status line, matches spec pattern)
- Checker rules share only helper utilities, not entire station flow understanding

All implementation details are specified in the plan, ready for the build station to execute.