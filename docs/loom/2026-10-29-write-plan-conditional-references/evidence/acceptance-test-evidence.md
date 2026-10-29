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
