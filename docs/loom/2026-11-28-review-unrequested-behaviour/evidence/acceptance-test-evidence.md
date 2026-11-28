# Final review raises behaviour nobody asked for — acceptance test evidence

Tested on 2026-11-28, in a clean copy of the project at commit 9526763628c8e19749d79f0e3bc8d42094610082
(`git worktree add --detach <scratchpad>/at-clean4 952676362…`; `git status --short` empty before and after every step).
The first run was at ac1157f893b89d4ee8e9e198f3238690007599dd, the second at
bafa1da6665063ec059eb836dee1d672f0a59ca1 and the third at
6efbf4f04cc1ab966fc2503ffef01245d4d71f17; their results are kept in the notes below.
Latest fix range re-tested: e00357697f3111b6fa204f3f0d351c3d1c415dc0..9526763628c8e19749d79f0e3bc8d42094610082
(`git diff --stat` touches only loom-code/tests/test_reviewer_mechanical_evidence.py, 7+/1-: the
allowlist regex is now `\bexcess\w*|\bunrequest\w*|\bout[\s-]+of[\s-]+scope\W+exclu\w*`,
case-insensitive, plus three Out-of-scope carve-outs asserted to match and one bare
"out of scope" sentence asserted not to match in `test_excess_rule_has_no_carve_out`).

## 0. Setup (README install path) — repeated on the re-run

- How I tried it: the README installs from the published GitHub marketplace
  (`claude plugin marketplace add https://github.com/kouko/loom-plugins.git`),
  which cannot reach this unmerged commit. Instead I validated the clean copy
  with the host's own plugin validator, and checked the derived manifests.
  - `claude plugin validate <clean>/loom-code`
  - `claude plugin validate <clean>` (marketplace root)
  - `python3 -I scripts/sync_codex_manifests.py --check --all`
- What came back: `✔ Validation passed` for loom-code; `✔ Validation passed
  with warnings` for the marketplace (pre-existing unquoted
  `${CLAUDE_PLUGIN_ROOT}` in loom-workflow hooks, not touched by this
  change); sync check exit 0.

## 1. 最後審查的 reviewer 共用指引寫明：交付了 intent 沒要求的行為，或 intent 的 Out of scope 排除的行為，必須當作 finding 提出；沒有 spec 的改動同樣適用。

- How I tried it: read `loom-code/agents/reviewer.md` in the clean copy. The
  rule sits at lines 17-21, the new filing sentence at lines 22-23, both in
  the opening reconciliation paragraph that precedes `## Your input` and
  applies to every lens
  (`lens: code | docs | spec | spec+adversarial | design | principles | skill | plan`, line 41).
  Checked the filing sentence against the lens table (reviewer.md:58-66):
  `deletion-first` is a dimension of code, docs, spec/spec+adversarial (via
  "docs +"), skill and plan; `design` and `principles` each score one
  dimension (design-conformance, principles-conformance).
- What came back (verbatim):
  reviewer.md:17-21 "Reconciliation also runs a fourth direction, excess:
  behaviour the change delivers that the intent leaves unrequested, or that
  the intent's Out of scope excludes, is a finding you must raise, and this
  applies to every change, including one that skipped the spec."
  reviewer.md:22-23 "File an excess finding under deletion-first, or under
  your lens's only dimension when your lens is `design` or `principles`."
- Constraint check: `loom-code/skills/closing-review/references/lenses.md`
  is not in the base..HEAD diff (`git diff --stat 3879464..HEAD -- lenses.md`
  empty); its spec-conformance row ("Unbuilt requirements and unrequired
  behaviour are both defects") is unchanged.
- Evidence: reviewer.md:17-23, :41, :58-66.

## 2. 把這條規則刪掉、或改成可以略過時，package suite 會有測試失敗。

Scope (user-decided, plan Risks 3, answer 「Ａ」): the suite blocks edits to
the rule sentence and carve-outs naming the rule's words (excess,
unrequested, "Out of scope excludes"); carve-outs reworded without those
words elsewhere in reviewer.md are a known limit left to reviewers.

- How I tried it: script `<scratchpad>/mut/run_mutations2.py` copies the
  pristine reviewer.md, applies each mutation only after asserting its anchor
  matches exactly once, prints the `git diff` lines to prove it landed, runs
  the reviewer-reading modules, then restores the file (final `git status`
  empty). "elsewhere" = a new paragraph after "never `important` or `fatal`
  on style alone."; "adjacent" = appended to the rule sentence's line.
  Command per mutation:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider <modules>`
  Module set (9): test_reviewer_mechanical_evidence,
  test_review_convergence_contract, test_docs_standard_text,
  test_architecture_doc_consumers, test_agy_tool_mapping,
  test_check_contract_citations, test_lenses_deletion_first,
  test_check_skill_crossrefs, test_probes_language_policy.
- Pristine run: `107 passed`.
- Results (every mutation's diff landed, see output file):

| Mutation | Landed diff | Result | Failing test |
|---|---|---|---|
| M1 delete the rule sentence | -5 lines | 1 failed | test_reviewer_raises_unrequested_behaviour |
| M1b delete rule + filing sentence | -7 lines | 1 failed | test_reviewer_raises_unrequested_behaviour |
| M1c delete the filing sentence | -2 lines | 1 failed | test_reviewer_raises_unrequested_behaviour |
| M1d filing "as a nit under deletion-first" | 1 line | 2 failed | test_reviewer_raises_unrequested_behaviour, test_excess_rule_has_no_carve_out |
| M2 "must raise" → "may raise" | 1 line | 2 failed | both |
| M3 drop "applies to every change, including one that skipped the spec" | 2 lines → 1 | 2 failed | both |
| M4 adjacent: "You may skip the excess direction when the change is small." | 1 line | 1 failed | test_excess_rule_has_no_carve_out |
| C1 adjacent (Codex): "Excess findings may be waived." | 1 line | 1 failed | test_excess_rule_has_no_carve_out |
| C2 elsewhere (Codex): "Excess findings may be waived." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| M5 elsewhere: "Raise no excess finding for a change that has no spec; the spec lens owns that direction." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| M6 elsewhere: "Under the docs lens, reporting unrequested behaviour is optional." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| C3 elsewhere: "What the intent's Out of scope excludes is a nit at most." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| C4 elsewhere: "Excess is reported at the author's discretion." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| C5 elsewhere heading: "### Excess is optional for docs" | +3 lines | 1 failed | test_excess_rule_has_no_carve_out |
| C6 elsewhere: "UNREQUESTED BEHAVIOUR IS NOT A FINDING." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| C7 elsewhere: "Excess? Optional!" | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| C8 elsewhere: "Excess-direction findings are nits only." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B1 elsewhere: "Excessive behaviour need not be raised." | +2 lines | 1 failed (at bafa1da66: 107 passed) | test_excess_rule_has_no_carve_out |
| B2 elsewhere: "Excesses need not be raised for a change without a spec." | +2 lines | 1 failed (at bafa1da66: 107 passed) | test_excess_rule_has_no_carve_out |
| B3 elsewhere: "Unrequestedness is never a finding." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B4 elsewhere: "EXCESSIVE BEHAVIOUR NEED NOT BE RAISED." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B5 adjacent: "Changes that do excessively much may be passed." | 1 line | 1 failed | test_excess_rule_has_no_carve_out |
| B6 elsewhere: "An author unrequesting a behaviour makes it optional to raise." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B7 elsewhere: "Excessiveness alone is a nit." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B8 elsewhere heading: "### Excesses are optional" | +3 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B10 elsewhere: "WHAT THE INTENT'S OUT OF SCOPE EXCLUDES IS A NIT AT MOST." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B12 elsewhere: "What the intent's out-of-scope excludes is a nit at most." | +2 lines | 1 failed (at 6efbf4f04: 107 passed) | test_excess_rule_has_no_carve_out |
| B13 elsewhere: "Behaviour the intent's Out of scope excluded is a nit at most." | +2 lines | 1 failed (at 6efbf4f04: 107 passed) | test_excess_rule_has_no_carve_out |
| B14 elsewhere: "An Out of scope exclusion need not be raised." | +2 lines | 1 failed (at 6efbf4f04: 107 passed) | test_excess_rule_has_no_carve_out |
| B15 elsewhere (new at 952676362): "OUT-OF-SCOPE EXCLUSIONS NEED NOT BE RAISED." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B16 elsewhere (new at 952676362): "Out of scope: excluding behaviour from review is fine." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| B9 elsewhere: "What the intent's out-of-scope list excludes is a nit at most." | +2 lines | 107 passed (judged reworded, known limit; re-run at 952676362, still passes) | none |
| B11 elsewhere: "Unrequired behaviour need not be raised." | +2 lines | 107 passed (different word, known limit) | none |
| M7 elsewhere: "For a change without a spec, skip the fourth direction." | +2 lines | 107 passed (known limit) | none |
| M8 elsewhere: "When the change skipped the spec, ignore the fourth reconciliation direction above." | +2 lines | 107 passed (known limit) | none |
| M9 elsewhere: "Extra behaviour the intent did not request is not a finding when no spec exists." | +2 lines | 107 passed (known limit) | none |

- At bafa1da66, B1/B2 survived because the regex was `\bexcess\b|\bunrequested\b|...`.
  At 6efbf4f04 the regex is
  `_EXCESS = re.compile(r"\bexcess\w*|\bunrequest\w*|Out of scope excludes", re.IGNORECASE)`
  (loom-code/tests/test_reviewer_mechanical_evidence.py:58), so every
  inflection of "excess" and "unrequest-" is now checked (B1-B8 fail).
- At 6efbf4f04, B12-B14 survived because the third vocabulary item was the
  literal phrase `Out of scope excludes`. At 952676362 it is
  `\bout[\s-]+of[\s-]+scope\W+exclu\w*` (case-insensitive), so hyphenated,
  inflected, upper-case and punctuation-separated forms (B12-B16) are checked
  against the allowlist and fail. A bare "out of scope" without an `exclu-`
  word is deliberately not matched (the test asserts "Leave out of scope work
  for a later change." is not a carve-out); B9, with "list" between "scope"
  and "excludes", still passes.
- Call on the user-decided scope: inflections and spelling variants of the
  rule's own words count as the rule's words (same call as the earlier runs).
  All such variants tried now fail a test, so Acceptance 2 is works. B9 (an
  extra word between the rule's words) and B11 (a different word) are judged
  rewordings, in the known limit, as are M7-M9.
- M7-M9 are the user-decided known limit (no rule word); in the first run
  they also passed 342 tests across 12 wider modules.
- The full package suite was not run (left to finalize-review).
- Evidence: script output `<scratchpad>/mut/out3.txt` (bafa1da66);
  `<scratchpad>/mut/out4.txt` and `out5.txt` (6efbf4f04, script
  `<scratchpad>/mut/run_mutations3.py`, same command and module set;
  pristine `107 passed`; every mutation's diff printed as landed; final
  `git status` empty); `<scratchpad>/mut/out6.txt` (952676362, script
  `<scratchpad>/mut/run_mutations4.py` = run_mutations3.py plus B15/B16, same
  command and module set; run on PRISTINE, B12-B16 and B9; pristine
  `107 passed`; B12-B16 each `1 failed, 106 passed`; B9 `107 passed`; final
  `git status` empty).

## 3. loom-code 發布新版號，CHANGELOG 寫明這條規則。

- How I tried it: grep of version strings; main's version via
  `git show main:loom-code/.claude-plugin/plugin.json`;
  `sync_codex_manifests.py --check --all`; ran
  `loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`
  with `loom-code/tests/test_reviewer_mechanical_evidence.py`.
- What came back: 3.93.0 in `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json`, `plugin.json`, `package.json`, the three
  loom-code READMEs and root README (lines 17, 105); main is 3.92.0.
  CHANGELOG.md:3 `## [3.93.0] — 2026-11-28 — Reviewer raises behaviour the
  intent did not ask for`; its bullet states the excess direction, the Out
  of scope case, "every change, including one that skipped the spec",
  "under every lens", and now "An excess finding is filed under
  `deletion-first`, or under the lens's only dimension for the `design` and
  `principles` lenses." Tests: `10 passed`. The full package suite, which
  finalize-review runs before accepting the change, also contains this pin.

## Re-run on 2026-11-28, at bafa1da66

- 0 setup: repeated in the clean copy, as above.
- 1: re-tested — rule and filing sentence read in place; filing sentence
  checked against every lens's dimensions; lenses.md still untouched.
- 2: re-tested — the nine first-run mutations (M1-M9) re-applied with new
  anchors, plus filing-sentence edits (M1b-M1d), Codex's waiver sentence
  adjacent and elsewhere (C1, C2), and further carve-outs naming the rule's
  words in other forms (C3-C8, B1, B2). All edits to the rule or filing
  sentence and every carve-out using the exact words fail a test; plural /
  adjective forms (B1, B2) pass; reworded M7-M9 pass as the accepted limit.
- 3: re-tested — CHANGELOG line now names the filing; versions unchanged
  at 3.93.0 and consistent; pin test passes.

## Re-run on 2026-11-28, at 6efbf4f04

- 0 setup: repeated in the clean copy — `claude plugin validate <clean>/loom-code`
  `✔ Validation passed`; `sync_codex_manifests.py --check --all` exit 0.
- 1: carried over — the fix diff touches only the test file; reviewer.md is
  unchanged since bafa1da66.
- 2: re-tested in full — all 22 earlier mutations re-applied (M1-M9, M1b-M1d,
  C1-C8, B1, B2) plus 12 new (B3-B14): 26 fail a test, B12-B14 pass (Out of
  scope phrase variants), B9, B11 and M7-M9 pass as the accepted reworded limit.
  Result stays partly.
- 3: carried over — the fix diff touches no version string, CHANGELOG or README.

## Re-run on 2026-11-28, at 952676362

- 0 setup: repeated in the clean copy — `claude plugin validate <clean>/loom-code`
  `✔ Validation passed`; `python3 -I scripts/sync_codex_manifests.py --check --all` exit 0.
- 1: carried over — the fix diff (e00357697..952676362) touches only
  loom-code/tests/test_reviewer_mechanical_evidence.py; reviewer.md is
  unchanged.
- 2: re-tested — the fix widens only the Out-of-scope vocabulary item, so the
  affected rows are the Out-of-scope carve-outs: B12-B14 re-applied, two new
  variants B15 (upper case + hyphens + plural noun) and B16 (colon between
  "scope" and "excluding") added, and B9 re-run as the boundary. Every
  mutation's diff landed; B12-B16 fail
  `test_excess_rule_has_no_carve_out`; B9 passes (known limit). The other
  29 rows (rule/filing edits and excess/unrequested carve-outs) are carried
  over: the `\bexcess\w*` and `\bunrequest\w*` alternatives and the assertions
  that exercise them are unchanged in the diff, and an added regex
  alternative can only add matches, never remove one. Result: works.
- 3: carried over — the fix diff touches no version string, CHANGELOG or README.

First run (at ac1157f89) for comparison: Acceptance 2 was partly — M1-M6
failed a test, M7-M9 passed; the keyword-plus-waiver-word test then let
"Excess findings may be waived." through (found by Codex), which C1/C2 now
show is blocked.
