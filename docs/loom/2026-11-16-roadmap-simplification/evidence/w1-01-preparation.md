# W1-01 — roadmap preparation and structural verification

Date: 2026-11-16

## Scope and pre-creation decisions

- Source: confirmed intent, approved spec and W1-01 plan task.
- Worth-it: one user-selected owner replaces distributed authoring rules and
  the dedicated map mechanism. The demonstrated problem and ownership decision
  are already recorded in intent/spec; no new user interview was needed.
- Smallest end state: SKILL.md plus a human README, no runtime, schema,
  scheduler, bundled templates or executable helpers. Removal of the old
  mechanism and inventory changes belong to later tasks; W1-01 alone adds files.
- User input: only missing outcome/document selection or unresolved user
  direction conflicts. Explain the consequence, ask narrowly and wait for a
  required answer; routine evidence-backed maintenance adds no approval loop.
- Layout disclosed by orchestrator before writing: skill SKILL.md + README.md;
  evaluations in loom-workflow/tests/roadmap/, development evidence here.
- Authoring reference: installed skill-creator-advance SKILL.md plus
  pre-creation-gates, eval-protocol, description-design, skill-writing-guide
  and asking-user-questions references. Repository conventions take precedence
  over that reference's generic command/package layout.

## Evaluation preparation

The full evaluation path applies because document selection, evidence and
authorization involve multiple behaviors. Ten behavior cases and a 20-query
description-selection corpus were written before the skill draft. The
behavior cases were frozen and handed to the orchestrator before drafting;
the orchestrator launched a no-skill baseline before the candidate arm.
Native matched-profile trials are owned by the orchestrator. No external CLI
or network model run was launched by this worker.

Behavior fixtures cover plain new plans, existing documents, verified-result
updates, contradictory evidence, approved continuation, planning-only
authority, missing plans, ambiguous/unreadable documents and recent user edits.
Assertions judge actual output/files/tool observations, not exact prose.
The baseline and candidate must receive identical fixture inputs with checks
withheld. Capture failures and limited evidence even when the baseline is good;
do not tune cases merely to force a comparative gain. Initial single runs are
bounded observations, not statistical evidence of improvement or host activation.

## Actual RED / GREEN

Command (both runs):

```text
python3 -m pytest loom-workflow/tests/roadmap/test_skill_structure.py -q
```

RED, before SKILL.md / README.md existed, exit 1:

```text
FAILED ...::test_independent_skill_identity_and_instruction_only_layout
FileNotFoundError: .../loom-workflow/skills/roadmap/SKILL.md
FAILED ...::test_packaged_markdown_local_links_resolve
AssertionError: assert source.is_file()
2 failed in 0.14s
```

GREEN, after adding the instruction-only skill, exit 0:

```text
..                                                                       [100%]
2 passed in 0.08s
```

These two tests verify packaged identity, the two-file instruction-only layout
and relative Markdown link resolution. They do not prove any agent follows the
instructions. The RED demonstrates absent packaging, not semantic failure.

Additional actual checks, exit 0:

```text
python3 -m json.tool loom-workflow/tests/roadmap/behavior_cases.json > /private/tmp/roadmap-cases-validated.json
python3 -m json.tool loom-workflow/tests/roadmap/trigger_queries.json > /private/tmp/roadmap-triggers-validated.json
wc -l loom-workflow/skills/roadmap/SKILL.md
85 loom-workflow/skills/roadmap/SKILL.md
```

## Limits and self-review

- Semantic trial results, description-selection results and comparative gain
  are pending; no semantic pass, installed-host trigger or adoption claim.
- No full package suite, release metadata, routing or map removal is part of
  W1-01; those remain with subsequent tasks and final verification.
- Re-read every new skill and README paragraph for dropped sentences, changed
  names/numbers/obligation words and broken cross-references. In particular,
  preserved optional creation, the selected existing document, unchanged user
  scope, unknown estimates, failed evidence and separate acceptance authority.
- No commit was made, following the task-specific orchestrator instruction.
