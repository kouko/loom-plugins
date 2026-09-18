# Fix artifact-type pointer in the loom README — plan
intent: 2026-09-17-fix-artifact-types-pointer@dd091fae
charter: 1.0

## Current State Evidence
- Forward: `docs/loom/README.md:19-20` says the mapping lives in the change's
  concept model §6, which is not tracked in this repository.
- Reverse: `loom-code/contract/manifest.yaml` declares `artifact_types` and
  is the mapping the checker reads (`loom_checker.artifact_types`).
- Error: the pointer leads nowhere here; the adversary found the manifest
  itself was missing the `memory` row the README describes.
- Data: the mapping lists intent, spec, plan, standing, evidence, skill, gate,
  map, docs, code and, after this change, memory.
- Boundary: one line of prose in one internal document, plus one row in the
  manifest's `artifact_types` table.

## Task DAG

**W1-01 Point the README at the live mapping**  after: none  acceptance: 1, 2, 3
- Files: docs/loom/README.md
- Test: A1 positive: manifest-cited; negative: concept-model-absent. A2 positive: manifest-cited; negative: concept-model-absent. A3 positive: manifest-declares-artifact-types; negative: manifest-declares-no-artifact-types.
- Risk: None. agent-decided.

## Questions asked
- none

## Risks
- None.