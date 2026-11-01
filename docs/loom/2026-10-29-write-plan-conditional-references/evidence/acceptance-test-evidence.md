# write-plan keeps conditional paths out of its always-read body — acceptance test evidence

Tried on 2026-10-29, in a clean copy of the project at 3eb08254
(`git worktree add --detach <scratchpad>/at-clean HEAD`, outside the repo tree).
Base for "same meaning" comparisons: 129bac7e.

Test runner used for every pytest line below:
`env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider <files>`

## Setup

- How I tried it: README `## Install` installs from the marketplace into a live host
  (`claude plugin install loom-code@loom`). I did not install the branch into the
  user's host — that would change the user's plugin configuration. Instead I ran the
  CI's structural checks that decide whether the plugin loads as shipped, in the clean copy:
  `scripts/check_plugin_boundaries.py loom-code`, `scripts/sync_codex_manifests.py --check --all`,
  `loom-code/scripts/check_mechanisms.py --baseline 129bac7e`,
  `loom-code/scripts/check_contract_citations.py`, `loom-code/scripts/check-skill-crossrefs.py`.
- What came back: all exit 0 — "OK: loom-code is filesystem-boundary clean.",
  manifests in sync, "all clear" (gate markers inside `references/` register),
  "no new contract citations", "OK: all relative skill cross-references resolve."
- Evidence: the outputs above; `ls loom-code/skills/write-plan/references/` lists
  `confirm-intent.md`, `no-intent-interview.md`, `self-written-spec.md`.

## 1. write-plan's SKILL.md body is at most 2800 words, under an unchanged 3750-word cap.

- How I tried it: counted words after the YAML frontmatter with `str.split` (the same
  rule as `_body_words` in `loom-code/tests/test_write_plan_shape_text.py:44`) on the
  base file (`git show 129bac7e:loom-code/skills/write-plan/SKILL.md`), the release
  commit 2681cfd9, and HEAD. Looked for the cap in the base and HEAD trees with
  `git grep -n 3750 -- '*.py' '*.yaml'`.
- What came back: base 3749, release commit 2763, HEAD 2780 (the fix 3d8a6978 added
  17 words). Cap: `assert _body_words(...) < 3750` at
  `loom-code/tests/test_write_plan_shape_text.py:54`, identical to the base's line 45.
  No other cap for this file exists.
- Evidence: counts above; `test_writePlanBody_under3750Words` passes (see 4).
- Side note: `loom-code/CHANGELOG.md:8` says "drops from 3749 to 2763 words"; the
  shipped body is 2780.

## 2. A run without loom-design still reaches the no-intent interview and the self-written minimal spec path, and each rule those paths state today is still stated, with the same meaning, in the file the run is sent to.

- How I tried it: read `loom-code/skills/write-plan/SKILL.md` at HEAD as a cold agent
  and followed each loom-design-absent path to the file it names:
  - no intent: Step 1 bullet `SKILL.md:146` → `references/no-intent-interview.md`
    (holds the whole old bullet; its line 7-8 sends intent-writing rules to
    `confirm-intent.md`) → Step 3 `SKILL.md:188` → `references/confirm-intent.md`.
  - hand-written unconfirmed intent: Step 1 "intent exists" → Step 2 → Step 3
    `SKILL.md:188` → `references/confirm-intent.md:9-43` (the moved intake rules and the
    diagram paragraph, under the gate marker).
  - `yes`, spec missing: `SKILL.md:223-224` → `references/self-written-spec.md`
    (section "needs-design: yes without loom-design" plus the product gate at :60).
  - spec-exists resume: `SKILL.md:215-218` → `references/self-written-spec.md`
    "finish what it still requires", then the intake check.
- Verbatim check: a script (`<scratchpad>/verbatim_check.py`) split the base SKILL.md
  into 312 sentences (whitespace-flattened, split after `.`, `;`, `:`) and looked for
  each one in HEAD's SKILL.md or one of the three references.
- What came back: 311 of 312 found word for word. The single miss is the cross-reference
  sentence "**`yes`, and `docs/loom/<change-id>/spec.md` already exists** — go to the
  intake check below.", rewritten by 3d8a6978 to add the pointer (the intent's
  Constraints allow a change where a cross-reference has to).
- Paths a confirmed-intent run no longer reads: the intake rules (incl. "Visible effects
  with an unknown surface ... `needs-design: yes` with a surface-neutral reason") are
  now read only when Step 3 confirms. A confirmed run still has Step 4's
  `needs-design:` rule (`SKILL.md:194-203`), and capture-intent carries the same sentence
  (`loom-design/skills/capture-intent/SKILL.md:307`).
- Evidence: `test_intakeReferences_holdMovedRules_bodyDoesNot`,
  `test_probe_spec_exists_product_gate.py` (the adversary's program) pass (see 4).

## 3. A run with loom-design installed is never told to read the no-intent interview file, and is told to read the self-written spec file only when it writes a spec itself.

- How I tried it: same cold read, loom-design-installed paths, and
  `grep -n "no-intent-interview\|self-written-spec\|confirm-intent" SKILL.md`:
  - no intent: Step 1 bullet `SKILL.md:144-145` → "starts at `capture-intent`, and stop"; no pointer.
  - `no`, no spec needed: `SKILL.md:210` "go to step 5"; pointer at :212-213 fires only
    when "a task's rationale outgrows its Risk line, or a carried-details list is non-empty" —
    the two old triggers for this station writing the spec itself.
  - `no`, spec needed: same pointer → `self-written-spec.md` (station writes the spec).
  - `yes`, spec missing: `SKILL.md:220-221` hands to `write-spec` and stops; no pointer.
  - `yes`, spec exists written by write-spec: pointer at :215-218 is conditioned on
    "when this station wrote that spec (`loom-design` absent)"; skipped.
- What came back: `no-intent-interview` appears once in SKILL.md (line 146, absent
  bullet only) and nowhere in `confirm-intent.md`; `self-written-spec` appears three
  times (lines 213, 217, 224), none on the installed `yes` branch.
- Evidence: `test_interviewPointer_onlyOnLoomDesignAbsentBullet`,
  `test_specPointer_onNoAndAbsentBranches_notInstalledYes` pass (see 4).

## 4. Every existing check that pins those rules still runs and passes against the file that now holds them.

- How I tried it: `git grep` over `*.py` at HEAD for 29 distinctive phrases from the moved
  text, plus the list of tests that read write-plan's SKILL.md at base; read each hit to see
  which file it reads. Retargeted pins: `test_write_plan_shape_text.py` (`_product_gate()`
  now reads `SELF_WRITTEN_SPEC`; Mermaid check also reads it) and
  `test_adversarial_no_reask_pin_flipped_polarity.py` (`"WRITE_PLAN"` → `"SELF_WRITTEN_SPEC"`).
  `test_adversarial_product_one_way_door_without_spec.py` already reads `confirm-intent.md`
  (its docstring still says the carried-details sentence is in SKILL.md step 4).
  Gate markers: `check_mechanisms.py` scans `skills/**/*.md` and reported "all clear".
- Ran in the clean copy:
  `loom-code/tests/test_write_plan_shape_text.py loom-code/tests/test_adversarial_no_reask_pin_flipped_polarity.py loom-code/tests/test_probe_spec_exists_product_gate.py loom-code/tests/test_write_plan_station_text.py loom-code/tests/test_check_mechanisms.py loom-code/tests/test_adversarial_product_one_way_door_without_spec.py loom-code/tests/test_one_way_door_copies.py loom-code/tests/test_write_plan_entry_definition.py loom-code/tests/test_probes_language_policy.py loom-design/tests/spec/test_write_spec_contract.py loom-design/tests/spec/test_capture_intent_contract.py`
- What came back: `234 passed in 3.43s`.
- Full package suite: not run by me; `finalize-review` executes the declared
  `package-tests` command (docs/loom/KICKOFF-DEFAULTS.md) and refuses the attestation on
  failure. Build reported it passed at 3eb08254.

## Re-run on 2026-10-29, at 7ffa7e4f

Fix range c8dd93cb..7ffa7e4f: two `##` headings removed from
`loom-code/skills/write-plan/references/self-written-spec.md`; Step 4 `no`-branch pointer
in `loom-code/skills/write-plan/SKILL.md:212-214` gains "or this station already wrote
`docs/loom/<change-id>/spec.md`"; CHANGELOG 2780 → 2785; two new tests in
`loom-code/tests/test_write_plan_shape_text.py`. Clean copy:
`git worktree add --detach <scratchpad>/at-rerun 7ffa7e4f` (0 untracked/modified files).
The fix touches the reference, SKILL.md and the pinning tests, so every row is re-tested.

- Setup: re-ran in the clean copy `scripts/check_plugin_boundaries.py loom-code`
  ("OK: loom-code is filesystem-boundary clean."), `scripts/sync_codex_manifests.py --check --all`
  (exit 0), `loom-code/scripts/check_mechanisms.py --baseline 129bac7e` ("all clear"),
  `loom-code/scripts/check_contract_citations.py` ("no new contract citations"),
  `loom-code/scripts/check-skill-crossrefs.py` ("all relative skill cross-references resolve").
  All exit 0.
- 1: re-tested — body words (`str.split` after frontmatter, same rule as `_body_words`):
  129bac7e 3749, c8dd93cb 2780, 7ffa7e4f 2785 (≤ 2800). Cap assertion `< 3750` unchanged in
  `test_writePlanBody_under3750Words` (passes). `loom-code/CHANGELOG.md:8` now says
  "drops from 3749 to 2785 words", matching the shipped body.
- 2: re-tested — cold read of every loom-design-absent path at 7ffa7e4f:
  no intent → `SKILL.md:146` → `no-intent-interview.md` → Step 3 → `confirm-intent.md`;
  unconfirmed intent → Step 3 → `confirm-intent.md`; `yes`, spec missing →
  `SKILL.md:224-225` → `self-written-spec.md`; `yes`, spec exists (this station wrote it)
  → `SKILL.md:216-219` "finish what it still requires"; `no`, spec needed →
  `SKILL.md:212-214` → `self-written-spec.md`; `no`, resumed with this station's
  `spec.md` already on disk → the new third clause of `SKILL.md:212-214` fires →
  `self-written-spec.md`, whose last line returns to the intake check.
  Reference read top to bottom from the `no` branch: `grep -c '^##'` = 0 headings;
  `diff` of base 129bac7e Step 4 text (from "When a task's rationale outgrows its Risk
  line, write" to the intake-check heading) against the reference body (after its 5-line
  preamble) shows only: the two `yes` paragraphs that stay in SKILL.md (spec exists; spec
  missing with loom-design installed) removed, a leading blank line, and the closing line
  "When done, return to step 4's intake check." added. So the review-dispatch paragraph and
  the product gate follow the `no` rules in their 129bac7e order, under no `yes`-only heading.
  `verbatim_check.py` (base file byte-identical to `git show 129bac7e:...SKILL.md`):
  "old sentences: 312 missing verbatim: 1" — the same rewritten cross-reference sentence
  as before.
- 3: re-tested — `grep -n "no-intent-interview\|self-written-spec" SKILL.md`: lines 146
  (absent bullet only), 214 (`no` pointer), 218 (spec-exists, "when this station wrote
  that spec (`loom-design` absent)"), 225 (`yes`, not installed). `no-intent-interview`
  appears 0 times in `confirm-intent.md` and `self-written-spec.md`. With loom-design
  installed, the `no` pointer fires only when the station writes or already wrote the spec
  itself; `yes`, spec missing (`SKILL.md:221-222`) hands to `write-spec` with no pointer.
- 4: re-tested — same 11 files as row 4 above, in the clean copy: `236 passed in 3.69s`
  (234 earlier + `test_noBranchSpecPointer_firesOnAlreadyWrittenSpec` and
  `test_selfWrittenSpec_hasNoBranchHeadings`). Those two plus
  `test_writePlanBody_under3750Words` and
  `test_specPointer_onNoAndAbsentBranches_notInstalledYes` run alone: `4 passed`.
  Full package suite: run by orchestrator at 7ffa7e4f, result pending; `finalize-review`
  executes it and refuses the attestation on failure.
