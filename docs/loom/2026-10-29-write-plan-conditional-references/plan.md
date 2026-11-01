# write-plan keeps conditional paths out of its always-read body — plan
intent: 2026-10-29-write-plan-conditional-references@1d9df277
charter: 1.1

## Current State Evidence

- Forward — `loom-code/skills/write-plan/SKILL.md` body is 3749 words; `test_write_plan_shape_text.py::test_writePlanBody_under3750Words` caps it below 3750.
- Reverse — Step 1 no-intent bullet (`SKILL.md:146-159`), gate intake rules (`:167-194`) and diagram paragraph (`:197-200`) serve only intents this station writes or confirms.
- Error — Step 4 spec rules (`SKILL.md:257-268`, `:276-323`) also serve a `needs-design: no` change needing a spec, so loom-design runs can reach them.
- Data — `check_mechanisms.recompute_prose_gates` scans `skills/**/*.md`, so gate markers inside `references/` still register (`loom-code/scripts/check_mechanisms.py:268-279`).
- Boundary — scratch prototype of the move: body 2763 words; full loom suite 5 failed, 2565 passed; failures only in `test_write_plan_shape_text.py` and `test_adversarial_no_reask_pin_flipped_polarity.py`.

## Task DAG

### Wave 1 — move the two conditional paths

**W1-01 Move the no-intent interview to `references/no-intent-interview.md` and the intent-writing rules to `references/confirm-intent.md`**  after: none  acceptance: 1, 2, 3
- Files: `loom-code/skills/write-plan/SKILL.md` (entry: Step 1), `loom-code/skills/write-plan/references/no-intent-interview.md`, `loom-code/skills/write-plan/references/confirm-intent.md`, `loom-code/tests/test_write_plan_shape_text.py`
- Test: A2 positive: references-hold-moved-rules-verbatim; negative: body-no-longer-holds-moved-rules. A3 positive: pointer-only-on-loom-design-absent-bullet; negative: installed-bullet-and-confirm-intent-never-name-interview-file.
- Risk: agent-decided — intake rules move into `confirm-intent.md` under their own gate marker, so hand-written intents keep them; interview file adds one line applying those rules; body keeps the gate's first paragraph.

**W1-02 Move the self-written spec path and product gate to `references/self-written-spec.md`**  after: W1-01  acceptance: 1, 2, 3, 4
- Files: `loom-code/skills/write-plan/SKILL.md` (entry: Step 4), `loom-code/skills/write-plan/references/self-written-spec.md`, `loom-code/tests/test_write_plan_shape_text.py`, `loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py`
- Test: A4 positive: product-gate-tests-read-reference-and-pass; negative: reask-rewrite-in-reference-fails. A3 positive: spec-pointer-on-no-and-absent-branches; negative: installed-yes-branch-has-no-pointer.
- Risk: agent-decided — retargets 5 failing tests from SKILL.md Step 4 to the reference; preserves what they cover (product gate doors, no-reask, no Mermaid); "below" cross-references stay valid because order is kept.

### Wave 2 — release

**W2-01 Release loom-code 3.52.1**  after: W1-02  acceptance: 1
- Files: `loom-code/.claude-plugin/plugin.json`, `loom-code/plugin.json`, `loom-code/.codex-plugin/plugin.json`, `loom-code/package.json`, `loom-code/CHANGELOG.md`, `README.md`, `loom-code/README*.md`, `loom-code/tests/test_write_plan_station_text.py`
- Test: A1 positive: every loom-code manifest and README reads 3.52.1; negative: an unsynchronized derived manifest fails the pin.
- Risk: bump `.claude-plugin/plugin.json`, then `sync_codex_manifests.py --all`; patch bump because no rule changes; lands before finalize-review.

### Wave 3 — probe graduation

**W3-01 Graduate the spec-exists resume probe into the loom-code suite**  after: W2-01  acceptance: 2
- Files: `docs/loom/2026-10-29-write-plan-conditional-references/evidence/probes/test_abuse_spec_exists_product_gate.py`, `loom-code/tests/test_probe_spec_exists_product_gate.py`
- Test: A2 positive: the moved probe passes at its suite path and keeps its `concern:` line; negative: the store path no longer exists.
- Risk: the probe caught a defect on this change (fixed in 3d8a6978), so closing review requires it in the suite before finalize-review; content unchanged except paths it resolves.

## Simplicity check
- Put the intent-writing rules in `confirm-intent.md`, which step 3 already loads with the interview file pointing to them — taken
- One combined reference for both paths — declined: a loom-design run writing a `no`-branch spec would then be told to read the interview file (Acceptance 3)

## Questions asked
① — what — C intent 重述：把兩段只在沒裝 loom-design 時用到的段落搬到 references/，3750 上限不變，自動發布 — 對嗎？
① — consequence — C 的 intent 要改哪一條？（A：改第 3 條，本體約 2780 字；B：改第 1 條，上限放寬到 3200）

## Risks
1. An agent may skip the pointer and miss moved rules; mitigated by pointers at each branch that needs them and acceptance testing walking both loom-design-absent paths.
2. Moved wording must stay verbatim; the implementer copies blocks mechanically and the reviewer diffs moved text against `129bac7e`.
3. Acceptance 1 (2800 words) has no permanent test; adding one would tighten the cap, which the intent keeps at 3750.
