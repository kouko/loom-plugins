# Behavioral evidence archive

The complete behavioral packet moved byte-identically from this directory to
the [dated dogfood archive](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/).
For any former `evidence/<relative-path>#<anchor>`, use
`docs/skill-dogfood/2026-11-14-research-evidence-acceptance/<relative-path>#<anchor>`;
all inner paths and anchors are unchanged.

- [Frozen inputs](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/frozen-inputs.json), [cases](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/cases.json) and [run map](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/run-map.json)
- [Baseline observations](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/baseline-observations.json) and [candidate observations](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/candidate-observations.json)
- [Behavior assessment](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/behavior-assessor.md), [evidence assessment](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/evidence-assessor.md) and [adversary report](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/adversary-report.md)
- [Candidate skill hashes](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/candidate-skill-hashes.json) and [all run artifacts](../../../skill-dogfood/2026-11-14-research-evidence-acceptance/runs/)

This placement correction keeps executable source/trial snapshots out of the
change store's non-probe directories. It changes no requirements, evidence or
judgments and reruns no trials. Absolute scratch paths in raw records remain
historical provenance. Acceptance reports and future acceptance-test evidence
remain at their canonical change-store locations.

Relocation verification: all 165 original archived files, including 46 Python
files, retain their original SHA-256 hashes. Two contextual copies complete the
R02 turn2 snapshot's missing scratch targets: `preview_commands.py` and
`preview_commands.stdout.txt`, copied byte-identically from R02 project scratch.
The originals were produced in turn1 and unchanged later; no frozen record was
edited and no experiment rerun. All 76 relative Markdown links inspected
(archive plus this pointer) resolve. Nineteen absolute scratch links remain
historical provenance, excluded from portable-link validation; anchor semantics
were not reassessed by this placement check.
