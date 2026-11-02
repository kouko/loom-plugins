# Loom evidence drift guards — spec
intent: 2026-10-12-loom-evidence-drift-guards@71bb82d9
confirmed-behavior: 2026-11-02 @ad99dbe
pre-build-review: required — the generated evidence format is a public contract used by publication and delivery checks

## Requirements

REQ-1 — Complete acceptance coverage
WHEN a report omits, duplicates, or cannot identify the result of an Acceptance line, the checker shall fail and identify the affected numbers; a complete report shall preserve each recorded result without treating unverified results as passing → Acceptance #1

REQ-2 — Tested and reviewed content identity
WHEN a new verification record is generated or validated, the checker shall require the tested and reviewed commit identities and reject functional differences between them while permitting the specified evidence-only differences → Acceptance #2

REQ-3 — Confirmed intent identity
WHEN an intent covered by the new confirmation protocol differs from its confirmed content, including a complete rollback that removes or restores an older pin, the checker shall fail, identify the potentially affected Acceptance lines, and require reconfirmation → Acceptance #3

REQ-4 — Named boundary programs
WHEN an implemented change names a concrete boundary or probe test that is absent, the checker shall fail and name the missing program; planning shall not require unwritten programs to exist before implementation → Acceptance #4

REQ-5 — Persisted review verdicts
WHEN closing review finishes, the generated verification record in the change directory shall persist the authoritative verdicts, and the workflow shall distinguish that record from temporary reviewer input → Acceptance #5

REQ-6 — Publication revalidation
WHEN publication evaluates verification evidence, the checker shall recompute the applicable coverage, commit, intent, and boundary-program invariants against the selected committed tree and disclose invalid evidence rather than continuing to label it valid → Acceptance #6

REQ-7 — New defaults and compatibility
WHEN a new change enters the workflow, the templates and confirmation steps shall supply the evidence fields by default while preserving historical verification records and supported mechanical verification without mandatory independent acceptance testing → Acceptance #7

## Design decision

- agent-decided — extend the existing verification record and rule modules because the confirmed constraints reject a parallel evidence store.
- agent-decided — preserve exact historical v1 and v2 shapes and their original digest policy; updating Loom must not require rewriting historical evidence.
- agent-decided — keep reports and direct evidence files outside the functional digest, but keep executable probes inside it; revalidate current evidence semantics at finalization and publication.
- agent-decided — derive new intent applicability from the existing canonical confirmation commit in the selected ancestry, so restoring a complete older file cannot erase the baseline. Confirmations predating pin support remain exempt.
- agent-decided — validate named task references before implementation and concrete named program files afterwards; use the selected commit for publication checks.
- agent-decided — finalization requires the report's canonical tested-commit line instead of substituting HEAD. Publication checks recorded identities and declared provenance; manually supplied headerless evidence does not prove when testing occurred.
- agent-decided — a mechanically narrow change without a report records its actual verified HEAD and does not claim independent acceptance testing.
- agent-decided — publication retains its existing ability to disclose stale or absent verification; this change does not silently turn publication authorization into merge acceptance.
- agent-decided — correct the inherited needs-design classification because the JSON evidence template matches the existing interface policy. The confirmed outcomes and automatic-publication authorization are unchanged.

## Alternatives considered

- A second evidence ledger was rejected because it duplicates identity and coverage state already owned by the generated record.
- Comparing only the current file's pin was rejected after an actual finalizer trial accepted a full rollback that removed the pin.
- Treating all evidence files as functional content was rejected because the confirmed constraints permit evidence-only differences between tested and reviewed commits.
- Migrating historical evidence was rejected because the confirmed scope explicitly excludes historical conversion.

## Current state evidence

- Forward: `loom-code/scripts/loom_checker/command_handlers/finalize.py` `_finalize` generates the record after executing functional verification.
- Reverse: `loom-code/scripts/loom_checker/attestation.py` `check_attestation_evidence` is shared by finalization and publication validation.
- Error: `loom-code/scripts/loom_checker/rule_checks/intent_version.py` `check_intent_version` originally trusted only current mutable pins; a clean actual-finalizer trial accepted a full rollback and emitted a null pin.
- Data: `loom-code/contract/templates/attestation.json` carries confirmed intent identity, tested and reviewed commits, and per-Acceptance results.
- Boundary: `loom-code/contract/manifest.yaml` `publication_only_paths` excludes direct evidence while retaining executable probes; historical schema handling remains in the existing validator.

## UI flows

| Case | What the user does | What they see |
|---|---|---|
| Empty evidence | Finalize a change requiring a report without its required acceptance rows | Exit 1, a coverage error naming missing numbers, and a need to complete the report and retry. |
| In progress | Finalize a change with complete evidence | The existing test execution runs before a verification record is written; no new progress control is introduced. |
| Invalid coverage | Finalize a report containing duplicate or unreadable results | Exit 1 with the affected numbers; correct those rows and retry. |
| Mismatched content | Finalize evidence from different functional code or an altered confirmed intent | Exit 1 identifying the mismatched versions or affected requirements; retest the current code or reconfirm the intended requirements before retrying. |
| Missing boundary program | Finalize an implemented change with a named missing test file | Exit 1 naming the missing program; implement or correct the named test and retry. |
| Success | Finalize matching content with complete evidence and passing review/tests | Exit 0 and a generated verification record containing the verdicts and evidence identities. |
| Publication | Publish after a report-only edit | Verification is recomputed; valid evidence remains valid and invalid evidence is disclosed as stale. Existing publication and separate merge-acceptance behavior remain in force. |
| Historical evidence | Validate an unchanged historical record | The historical shape and content-identity policy remain supported without migration. |
| Mechanical verification | Finalize a mechanically narrow change that needs no independent acceptance report | Verification can finish using the actual functional execution without claiming independent acceptance testing. |

After any failed finalization, the user repairs the named evidence or content and reruns the existing command. A failed attempt does not create a replacement verification record. Revalidating another committed version reads that version's artifacts, preserving the checkout. No adopting repository's existing user data is migrated or rewritten.
