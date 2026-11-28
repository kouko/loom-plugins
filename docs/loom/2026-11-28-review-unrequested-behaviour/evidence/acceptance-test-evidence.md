# Final review raises behaviour nobody asked for — acceptance test evidence

Tried on 2026-11-28, in a clean copy of the project at bafa1da6665063ec059eb836dee1d672f0a59ca1
(`git worktree add --detach <scratchpad>/at-clean2 bafa1da66…`; `git status --short` empty before and after every step).
The first run was at ac1157f893b89d4ee8e9e198f3238690007599dd; its results are kept in the "First run" notes below.
Fix range re-tested: 6bae065f6de5fd2f8d457dae507f96c8fb301af6..bafa1da6665063ec059eb836dee1d672f0a59ca1
(reviewer.md filing sentence, test_reviewer_mechanical_evidence.py allowlist, CHANGELOG line, plan Risks 3).

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
| B1 elsewhere: "Excessive behaviour need not be raised." | +2 lines | **107 passed** | none |
| B2 elsewhere: "Excesses need not be raised for a change without a spec." | +2 lines | **107 passed** | none |
| M7 elsewhere: "For a change without a spec, skip the fourth direction." | +2 lines | 107 passed (known limit) | none |
| M8 elsewhere: "When the change skipped the spec, ignore the fourth reconciliation direction above." | +2 lines | 107 passed (known limit) | none |
| M9 elsewhere: "Extra behaviour the intent did not request is not a finding when no spec exists." | +2 lines | 107 passed (known limit) | none |

- Why B1/B2 survive: `_EXCESS = re.compile(r"\bexcess\b|\bunrequested\b|Out of scope excludes", re.IGNORECASE)`
  (loom-code/tests/test_reviewer_mechanical_evidence.py:58). `\bexcess\b`
  does not match the plural "Excesses" or the adjective "Excessive", so
  those sentences are never checked against the allowlist. Matching
  `\bexcess(?:es|ive)?\b` (and the same for "unrequested") would close it.
- M7-M9 are the user-decided known limit (no rule word); in the first run
  they also passed 342 tests across 12 wider modules.
- The full package suite was not run (left to finalize-review).
- Evidence: script output `<scratchpad>/mut/out3.txt`.

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

First run (at ac1157f89) for comparison: Acceptance 2 was partly — M1-M6
failed a test, M7-M9 passed; the keyword-plus-waiver-word test then let
"Excess findings may be waived." through (found by Codex), which C1/C2 now
show is blocked.
