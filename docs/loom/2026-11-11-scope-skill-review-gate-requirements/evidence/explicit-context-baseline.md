# Baseline provenance

Independent cold reviewer output captured before the Skill lens edit. The explicit-contract cases already produced the intended results before the edit; this is control evidence, not a behavioral failure.

# Current Skill lens execution

Reviewed only the supplied reviewer contract, current lens definitions, and six synthetic cases. No intent, plan, diff, history, tool installation, or suite was inspected. This is a standalone behavioral review, not a branch-end attestation; no commit identifiers were supplied or invented.

## Interpretation

The supplied case contract and acceptance condition are ground truth. The current Skill lens at `loom-code/skills/closing-review/references/lenses.md:127-129` literally describes any rule paragraph without a marker as an omission, without naming an adoption condition. I do not turn that wording into a project obligation where the case expressly says no such contract exists. Consequently the results below represent contextual execution of the current lens, not a literal marker-presence scan. This tension is a limitation of the review instructions, not a finding against the external targets.

In every case ambiguity, inconsistency, missing-population, and user-judgment-leak score PASS: there are no competing execution readings, contradictory target instructions, measured claims, or questions for the user. Deletion-first is N/A: these are complete standalone targets with no proposed additions or delta supplied. The minimal version command and dirty-tree check also offer no concrete smaller shape achieving the supplied acceptance condition.

## external-clean

Verdict: PASS. No finding.

Omission and incorrect-fact: PASS. The target specifies the trigger, supported command, reporting behavior, and no-install boundary. The case's manual supports `quill version`; its project expressly has no gate-registration contract. Requiring registration would add an obligation absent from this ground truth.

Source: `docs/loom/2026-11-11-scope-skill-review-gate-requirements/evidence/skill-lens-cases.md:11-23`; docs omission and incorrect-fact definitions in the supplied lens.

## workflow-only-adoption

Verdict: PASS. No finding.

Omission and incorrect-fact: PASS. The command and instructions meet acceptance. The project explicitly distinguishes using the development workflow from adopting artifact registration; nothing in the target or supplied contract makes marker insertion a required action.

Source: `docs/loom/2026-11-11-scope-skill-review-gate-requirements/evidence/skill-lens-cases.md:28-41`; docs omission and incorrect-fact definitions in the supplied lens.

## governed-missing-marker

Verdict: PASS_WITH_NOTES. One important omission.

Anchor: `release-helper/SKILL.md:2-3` within this case (case source lines 59-60).

Finding: issue (blocking): The clean-tree blocking rule lacks the registered marker required by this project's explicit contract and acceptance condition. Its execution instructions alone do not fulfill the required registration form.

Fix: Surround the two instruction lines with `<!-- gate: release.clean-tree -->` and `<!-- /gate -->`.

Omission: PASS_WITH_NOTES. Incorrect-fact: PASS. The command, root context, and stop condition are correct; no evidence shows publication would actually bypass the independently described checker, so a fatal bypass claim would be unsupported. One important finding yields PASS_WITH_NOTES under the supplied severity mapping.

Source: `docs/loom/2026-11-11-scope-skill-review-gate-requirements/evidence/skill-lens-cases.md:46-60`; current Skill lens marker sharpening at `loom-code/skills/closing-review/references/lenses.md:127-129` and its severity rules.

## governed-marked

Verdict: PASS. No finding.

Omission and incorrect-fact: PASS. The target carries the exact registered ID, names the repository-root check, and stops publication on any entries. Both behavioral and marker requirements are met.

Source: `docs/loom/2026-11-11-scope-skill-review-gate-requirements/evidence/skill-lens-cases.md:65-81`; current Skill lens marker sharpening.

## real-command-error

Verdict: NEEDS_REVISION. One fatal incorrect-fact finding.

Anchor: `quill-guide/SKILL.md:2` within this case (case source line 98), `run quill --version`.

Finding: issue (blocking): The instructed command is explicitly unsupported by the supplied manual. Following the skill produces an unknown-option error instead of displaying the installed version.

Fix: Replace `quill --version` with `quill version`.

Incorrect-fact: NEEDS_REVISION. Omission: PASS. No marker finding, because this project expressly has no registration contract. Fatal is warranted by the lens definition of an instruction that makes an executor do the wrong thing.

Source: `docs/loom/2026-11-11-scope-skill-review-gate-requirements/evidence/skill-lens-cases.md:86-99`; docs incorrect-fact and fatal-severity definitions in the supplied lens.

## correct-command

Verdict: PASS. No finding.

Omission and incorrect-fact: PASS. The target invokes the supported command and reports its output. The unsupported alternative in the manual is not used. No gate-registration obligation exists in the project contract.

Source: `docs/loom/2026-11-11-scope-skill-review-gate-requirements/evidence/skill-lens-cases.md:104-117`; docs omission and incorrect-fact definitions in the supplied lens.
