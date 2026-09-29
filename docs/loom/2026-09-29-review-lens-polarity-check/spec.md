# Review lens compares rule direction against the base — spec
intent: 2026-09-29-review-lens-polarity-check@3bbeec3e
pre-build-review: not-required — one reviewer-instruction paragraph and a release bump; no security, data, public contract or cross-system risk

## Requirements
REQ-1 — Lens states the polarity comparison
  WHEN a diff deletes or rewrites a sentence carrying a polarity word (never, must not, only, always, 不得 and their kin), the docs and skill lenses shall require the reviewer to compare that sentence with its base version and raise a finding when its direction is reversed or dropped → Acceptance #1
REQ-2 — A cold reviewer applies it
  WHEN a fresh reviewer reads a diff that buries one reversed rule among unrelated edits, the reviewer shall report it; WHEN the diff only rewords a rule without changing its direction, the reviewer shall raise no polarity finding → Acceptance #2
REQ-3 — Generic, not list-driven
  The comparison shall be triggered by the polarity words in the diff alone and shall name no rule, skill or file list → Acceptance #3
REQ-4 — Patch release bump
  The three plugins' versions shall each rise one patch, consistent across manifests, CHANGELOGs, READMEs and pin tests → Acceptance #4

## Design decision
- Carried detail (user-agreed, "做 C 吧"): add one check to the LLM reviewer's skill and docs lenses: when a diff deletes or rewrites a sentence containing never / must not / only / always / 不得, compare it with the old version sentence by sentence for a changed direction.
- agent-decided: write it as a sharpening of the existing docs `inconsistency` dimension (changed against base) in `lenses.md`, not a new dimension, so `reviewer.md`'s lens rows and their structural tests stay unchanged; the skill lens already scores the five docs dimensions.
- agent-decided: no `gate:` marker, because a marker registers a new mechanism and the intent fixes the mechanism count; lens rows are executed by reviewers, per `lenses.md`'s own carve-out.
- agent-decided: no new executable test; a prose-only lens change needs none (`lenses.md` tests row), and wording pins are barred by the prose-evidence-class policy. Acceptance #2 is proven by acceptance testing with a cold reviewer.
- agent-decided: the base version is read with `git show <base>:<path>`, the base the reviewer already receives.

## Alternatives considered
- Per-rule gate markers with fixed polarity tests (option B) — rejected by the user; reintroduces wording pins.
- A named checklist of 8-10 rules (option A) — rejected by the user; misses rules written later.
- A new `polarity` dimension — rejected; changes the lens rows, reviewer.md and its structural tests for no gain over `inconsistency`.

## Current state evidence
- Forward: `loom-code/skills/closing-review/references/lenses.md` "## Docs — five dimensions, plus deletion-first"; the `inconsistency` row covers changed-against-unchanged, not changed-against-base.
- Reverse: `loom-code/agents/reviewer.md:52` lists the docs dimensions; `loom-code/tests/test_lenses_deletion_first.py` pins only each row's last token.
- Error: `docs/loom/memory/a-compaction-test-written-from-the-compacted-file-cannot-see-what-left.md` — the real guard is a before/after rule diff against the base, which no lens tells a reviewer to run.
- Data: batch 4 hands 65 of 73 removed checks to review lenses (`docs/loom/2026-09-29-prose-pin-stock-cleanup-batch-4/evidence/census-report.md`).
- Boundary: versions 3.22.3 / 2.6.2 / 5.5.3 in the manifests, CHANGELOGs, READMEs and pin tests.

## UI flows
N/A
