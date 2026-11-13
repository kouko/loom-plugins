# Canonical confirmation provenance correction

Round-1 finalization passed the complete package suite and adversarial execution,
then failed `intake.intent-version`; prior reports remain unchanged. No successful
finalization or attestation is claimed by this correction.

The defect class was stale canonical provenance after agreed scope narrowing.
Commit `16d9157b` used a noncanonical subject, leaving `01d73c1a` selected as the
JSON-scope baseline. The user had already answered 好 to help-only delivery.
Canonical confirmation `2f29db8ab63a49c5b69decf2973d201112e63f59` records that consent and changes only the
excluded pin presentation to twelve characters. Semantic identity and Acceptance
content are unchanged; no new consent, code, runtime or release change occurs.
Current spec/plan headers now name that canonical confirmation.

Searched current intent, spec/plan headers, cumulative changed-file confirmation
references and help evidence; historical baseline references and failed/passing
reports remain intact. Existing plan field-cap failures were corrected by
compressing release file notation and two Risk lines without changing tasks.

## Actual existing-checker verification

Read `loom-code/scripts/loom_checker/rule_checks/intent_version.py`; invoked its
existing functions with the bundled manifest and selected committed tree using
the already installed Loom Python runtime:

- `pinned_confirmation` selected `2f29db8ab63a49c5b69decf2973d201112e63f59`.
- `intent_identity` remained `66583a51db46b4517f692cab4dcf61318fc19b21`.
- `check_intent_version` with that full identity returned `[]`.

This bounded input is not attestation evidence or a reviewer verdict. The first
attempt with system Python lacked PyYAML; no installation was performed.
Parent reruns the full suite and same adversary, then fresh acceptance and the
same closing reviewers for the corrected committed content.
