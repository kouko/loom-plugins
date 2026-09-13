# Cumulative boundary reassessment — pending evidence

## Status

`PENDING` — W0 freezes the identities, fixtures, rubric, and admission oracle.
No baseline/candidate runner, auditor, or real implementation outcome has been
collected. This status is intentionally non-admitted and must not be described
as behavioral evidence for the proposed runtime contract.

## Frozen identities

| Resource | Identity |
|---|---|
| Baseline revision | `1973ff35c4919e4c40795808240249c7ee40f506` |
| Fixture specification SHA-256 | `a9c3448869bc73985b3219ffeeb53770beb16c09134c888489639caf1a0b1723` |
| Frozen rubric SHA-256 | `ea89194e8d5673e3eba94b016318ba4e76d1da8d4893947a3d517658b1256594` |
| Baseline Write Plan SHA-256 | `e4c249bae4a5badbd15c258fbfe6d4d2d920e9eba58329fa2ee05bfe573c0da4` |
| Candidate Write Plan SHA-256 | `PENDING` |
| Candidate detailed-reference SHA-256 | `PENDING` |
| L1 HEAD / tree | `45a097b6180c90a8dc68d2f057b03d8d4ae7687a` / `74e9c6734d9ebfd6f2a1920b99f461be253445bc` |
| L2 HEAD / tree | `397c8269299ab56144ef7a1445188f497beb078f` / `b723cb3b390d179d32274d4922d78005c9119a2d` |
| L3 HEAD / tree | `d3c9f45e8d85b162f8485f0dde7937bbc1bfe943` / `bbc3cff17e12cd61a7460f9cb88d75038d573604` |
| L4 HEAD / tree | `3ec35ed5137e550b45690f7d454f88796e8be3e0` / `3b4a97db3a058ee1d7f2fe3e6c4db23c88dfebdf` |

## Mechanical evidence

- Initial construction RED: 13 passed and 6 failed—four expected identity
  placeholders, the pending admission, and one oracle mutation diagnostic. The
  diagnostic was corrected before identities were frozen.
- Fixture specification, baseline identity, deterministic histories, and HEAD
  unit tests: 10 passed.
- Admission-oracle and mutation self-tests: 9 passed.
- Focused self-test command: `python3 -m pytest
  loom-code/scripts/test_probes_cumulative_boundary_reassessment.py -q -k
  'not observed_report_meets_admission_bar'` — 19 passed, 1 deselected.
- Full focused command: `python3 -m pytest
  loom-code/scripts/test_probes_cumulative_boundary_reassessment.py -q` —
  expected RED, 19 passed and 1 failed at the admission assertion.
- Overall admission: expected RED because candidate identity, matched runner
  outputs, two blind audits, costs, mechanism count, and L1/L2 real runs are
  absent.
- Runtime contract edits: none in W0.

## Normalized evidence

This JSON block is the machine-read carrier. `null` and empty collections mean
missing evidence; they must never be interpreted as zero-cost or a passing
result.

```json evidence
{
  "status": "PENDING",
  "identities": {
    "fixture_spec_sha256": "a9c3448869bc73985b3219ffeeb53770beb16c09134c888489639caf1a0b1723",
    "rubric_sha256": "ea89194e8d5673e3eba94b016318ba4e76d1da8d4893947a3d517658b1256594",
    "baseline_revision": "1973ff35c4919e4c40795808240249c7ee40f506",
    "baseline_contract_sha256": "e4c249bae4a5badbd15c258fbfe6d4d2d920e9eba58329fa2ee05bfe573c0da4",
    "candidate_contract_sha256": null,
    "candidate_reference_sha256": null,
    "candidate_changed_contract_paths": []
  },
  "fixtures": {
    "L1": {"head": "45a097b6180c90a8dc68d2f057b03d8d4ae7687a", "tree": "74e9c6734d9ebfd6f2a1920b99f461be253445bc"},
    "L2": {"head": "397c8269299ab56144ef7a1445188f497beb078f", "tree": "b723cb3b390d179d32274d4922d78005c9119a2d"},
    "L3": {"head": "d3c9f45e8d85b162f8485f0dde7937bbc1bfe943", "tree": "bbc3cff17e12cd61a7460f9cb88d75038d573604"},
    "L4": {"head": "3ec35ed5137e550b45690f7d454f88796e8be3e0", "tree": "3b4a97db3a058ee1d7f2fe3e6c4db23c88dfebdf"}
  },
  "runner_profile": null,
  "normalizer_sha256": null,
  "normalized_outputs": {},
  "auditors": [],
  "cases": {
    "L1": {"baseline": [], "candidate": []},
    "L2": {"baseline": [], "candidate": []},
    "L3": {"baseline": [], "candidate": []},
    "L4": {"baseline": [], "candidate": []}
  },
  "reference_loaded": {"L1": null, "L2": null, "L3": null, "L4": null},
  "cost": null,
  "mechanism_delta": null,
  "real_runs": {"L1": null, "L2": null},
  "claims_scope": "frozen-four-case-corpus-only"
}
```
