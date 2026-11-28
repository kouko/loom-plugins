# Final review raises behaviour nobody asked for — acceptance test evidence

Tried on 2026-11-28, in a clean copy of the project at ac1157f893b89d4ee8e9e198f3238690007599dd
(`git worktree add --detach <scratchpad>/at-clean ac1157f89…`; `git status --short` empty before and after every step).

## 0. Setup (README install path)

- How I tried it: the README installs from the published GitHub marketplace
  (`claude plugin marketplace add https://github.com/kouko/loom-plugins.git`),
  which cannot reach this unmerged commit. Instead I validated the clean copy
  with the host's own plugin validator, and checked the derived manifests.
  - `claude plugin validate <clean>/loom-code`
  - `claude plugin validate <clean>` (marketplace root)
  - `python3 -I scripts/sync_codex_manifests.py --check --all`
- What came back: `✔ Validation passed` for loom-code (one catalog-only
  warning: no icon); `✔ Validation passed with warnings` for the marketplace
  (pre-existing unquoted `${CLAUDE_PLUGIN_ROOT}` in loom-workflow hooks, not
  touched by this change); sync check exit 0.

## 1. 最後審查的 reviewer 共用指引寫明：交付了 intent 沒要求的行為，或 intent 的 Out of scope 排除的行為，必須當作 finding 提出；沒有 spec 的改動同樣適用。

- How I tried it: read `loom-code/agents/reviewer.md` in the clean copy. The
  rule sits at lines 15-20, in the opening reconciliation paragraph that
  precedes `## Your input` and applies to every lens
  (`lens: code | docs | spec | spec+adversarial | design | principles | skill | plan`).
  Confirmed closing-review dispatches reviewers against this same file
  (`loom-code/skills/closing-review/SKILL.md:187`, `:206`, `:261`).
- What came back (verbatim, reviewer.md:17-20):
  "Reconciliation also runs a fourth direction, excess: behaviour the change
  delivers that the intent leaves unrequested, or that the intent's Out of
  scope excludes, is a finding you must raise, and this applies to every
  change, including one that skipped the spec."
- Constraint check: `loom-code/skills/closing-review/references/lenses.md`
  is not in the base..HEAD diff; its spec-conformance row (line 100,
  "Unbuilt requirements and unrequired behaviour are both defects") is unchanged.
- Evidence: reviewer.md:15-20; `git diff 3879464..HEAD --stat` (lenses.md absent).

## 2. 把這條規則刪掉、或改成可以略過時，package suite 會有測試失敗。

- How I tried it: script `<scratchpad>/mut/run_mutations.py` copies the
  pristine reviewer.md, applies each mutation only after asserting its anchor
  matches exactly once, prints `git diff` to prove it landed, runs the
  reviewer-reading modules, then restores the file (final `git status` empty).
  Command per mutation:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q -p no:cacheprovider <modules>`
  Base module set (9): every module under the four test roots whose source
  names reviewer.md and runs fast — test_reviewer_mechanical_evidence,
  test_review_convergence_contract, test_docs_standard_text,
  test_architecture_doc_consumers, test_agy_tool_mapping,
  test_check_contract_citations, test_lenses_deletion_first,
  test_check_skill_crossrefs, test_probes_language_policy.
- Pristine run: `107 passed`.
- Results:

| Mutation | Landed diff | Result | Failing test |
|---|---|---|---|
| M1 delete the rule sentence | 5 lines removed | 1 failed | test_reviewer_raises_unrequested_behaviour |
| M2 "must raise" → "may raise" | 1 line | 2 failed | test_reviewer_raises_unrequested_behaviour, test_excess_rule_has_no_carve_out |
| M3 drop "applies to every change, including one that skipped the spec" | 2 lines → 1 | 1 failed | test_reviewer_raises_unrequested_behaviour |
| M4 adjacent: "You may skip the excess direction when the change is small." | 1 line | 1 failed | test_excess_rule_has_no_carve_out |
| M5 elsewhere (after line 92): "Raise no excess finding for a change that has no spec; the spec lens owns that direction." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| M6 elsewhere: "Under the docs lens, reporting unrequested behaviour is optional." | +2 lines | 1 failed | test_excess_rule_has_no_carve_out |
| M7 elsewhere: "For a change without a spec, skip the fourth direction." | +2 lines | **107 passed** | none |
| M8 elsewhere: "When the change skipped the spec, ignore the fourth reconciliation direction above." | +2 lines | **107 passed** | none |
| M9 elsewhere: "Extra behaviour the intent did not request is not a finding when no spec exists." | +2 lines | **107 passed** | none |

- Widened check for M7-M9: re-ran with 12 more modules that scan agent
  files or all markdown (test_acceptance_test_report_shape,
  test_adversary_protocol, test_agent_model_frontmatter,
  test_contract_manifest, test_loom_runtime_skill_commands,
  test_opencode_loader, test_probes_coldread_abuse_coldread_branch_end,
  test_prose_pin_rule_text, test_write_plan_station_text,
  test_loom_attestation, test_probes_coldread_baselines_four_dirs_n10_sonnet,
  root tests/test_loom_plugin_install_layout): `342 passed` for each of
  M7, M8, M9. The full package suite was not run (left to finalize-review);
  no other module under the four roots names reviewer.md.
- Why they survive: `test_excess_rule_has_no_carve_out`
  (loom-code/tests/test_reviewer_mechanical_evidence.py:46-69) only inspects
  sentences matching `\bexcess\b|\bunrequested\b|Out of scope excludes`. A
  carve-out that names the rule as "the fourth direction" or paraphrases it
  ("did not request", "extra behaviour") is never examined.
- Evidence: script output `<scratchpad>/mut/out.txt`, `<scratchpad>/mut/out2.txt`.

## 3. loom-code 發布新版號，CHANGELOG 寫明這條規則。

- How I tried it: grep of version strings; base and main versions via
  `git show`; `sync_codex_manifests.py --check --all`; ran
  `loom-code/tests/test_write_plan_station_text.py::test_current_release_metadata_is_synchronized`.
- What came back: 3.93.0 in `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json`, `plugin.json`, `package.json`, the three
  loom-code READMEs and root README (lines 17, 105); base and main are
  3.92.0. CHANGELOG.md:3 `## [3.93.0] — 2026-11-28 — Reviewer raises
  behaviour the intent did not ask for`, whose bullet states the excess
  direction, the Out of scope case, "every change, including one that
  skipped the spec", and "under every lens". Pin test `1 passed`.
  The full package suite, which finalize-review runs before accepting the
  change, also contains this pin.
