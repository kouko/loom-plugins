# Build fix — stale active mechanism-census records

Date: 2026-11-16

## Defect and bounded repair

The integration run recorded in `/private/tmp/roadmap-package-tests.log` had
2855 passes and two mechanism-census failures. The active census had not been
updated when the skill, contract tool and optional intent field retired.

Actual recomputation before editing, `python3 loom-code/scripts/check_mechanisms.py`,
returned exit 1 with six findings:

- R1: roadmap skill and tool:roadmap recomputed but unregistered.
- R2: decision-map skill, tool:decision-map and artifact:intent.map stale.
- R4: decision-map eval points to deleted test_start_delivery.py.

Updated only those census records: register roadmap with its real structural
regression file, point the contract tool to the existing owner-inventory test,
and remove the retired optional-field row. This is replacement accounting,
not a claim that roadmap implements the old map behavior. No checker or test
was weakened; the skill eval covers packaging, not semantic compliance.

W3-01's bounded path list now names `docs/loom/` instead of enumerating its
guide/memory subpaths, bringing the active census into scope with seven entries
(cap eight). Existing historical accounting remains unchanged.

## Verification

```text
python3 loom-code/scripts/check_mechanisms.py
exit 0; all clear
skill: 27 recomputed / 27 registered
contract: 73 recomputed / 73 registered
net mechanism count excluding host-hygiene: 165

python3 -m pytest loom-code/tests/test_check_mechanisms.py loom-workflow/tests/roadmap/test_skill_structure.py loom-code/tests/test_contract_manifest.py -q
93 passed in 12.77s

git diff --check
exit 0
```

Scanned the active `docs/loom/evidence/mechanisms.yaml`, `loom-code/contract`,
`loom-code/scripts`, `loom-workflow/skills` and `loom-design/skills` for
decision-map, deleted skill/test paths and artifact:intent.map; no remaining
active hits in that bounded scan (READMEs were excluded, having been checked
in W3-01). Main's cumulative changed-file scan separately identified only
historical plan/spec/research/changelog/citation-accounting mentions. Those are
history, not live census rows or runtime instructions, and were preserved.

Re-read all changed rows for identifiers, obligations, numbers and references.
No adversarial concern/report, unrelated product, installed cache or user data
was edited. No commit or full package rerun was performed by this worker;
main owns the resumed integration run and remaining independent checkpoints.
