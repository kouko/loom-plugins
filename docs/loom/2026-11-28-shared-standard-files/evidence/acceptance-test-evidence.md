# Writer and judge read one standard — acceptance test evidence

Tried on 2026-11-28, in a clean copy of the project at b4f877e83 (second
re-run, after the fix range 1ec1bc12a..b4f877e83; see "Re-run on 2026-11-28,
at b4f877e83" at the end; the first re-run at 750da7564 is kept above it).
Sections 1-10 below record the first run, made in a
clean copy at be8c2e454
(`git worktree add --detach <scratch>/at-clean be8c2e454`; `git status --short`
empty before and after every step). Base for comparison: 847fbb6cd.

## Setup — the change loads in the clean copy
- How I tried it: README "Install" section installs from the GitHub
  marketplace (that would fetch `main`, not this branch, and would overwrite the
  user's real installed copy), so I ran the README's local validation path
  instead: `claude plugin validate ./loom-code` from the clean copy.
- What came back: `✔ Validation passed` (exit 0). One advisory line,
  `ICON_MISSING`, which the validator says does not change the result.
- Evidence: captured output above.

## 1. `loom-code/references/` 下有三份標準檔，各自涵蓋測試、程式碼設計、文件／skill 文字。
- How I tried it: `ls loom-code/references/`; read each file in full.
- What came back: `tests-standard.md` (§1 can-fail, §2 independent expected
  values, §3 public interface, §4 module entry, §5 prose-pin),
  `code-design-standard.md` (§1 names, §2 abstraction, §3 forwarding, §4 Rule of
  Three, §5 module depth + deletion test, §6 testable design, §7 deliberate
  shortcut), `docs-standard.md` (§1 omission … §5 population, §6 polarity,
  §7 deletion-first for docs/skill).
- Evidence: `loom-code/references/tests-standard.md:1`,
  `loom-code/references/code-design-standard.md:1`,
  `loom-code/references/docs-standard.md:1`.

## 2. 這三個主題的每條規則只寫在一份標準檔裡：implementer 讀的基準文件和 reviewer 讀的判準文件都指向標準檔，不再各自重述同一條規則。
- How I tried it: `git diff 847fbb6cd HEAD -- loom-code/references/engineering-baseline.md loom-code/skills/closing-review/references/lenses.md`;
  then grepped `loom-code/**/*.md` for 18 distinctive phrases of the moved rules
  ("Tests verify intent", "cannot fail", "Rule of Three", "only forwards",
  "two concrete", "single use", "premature abstraction", "affirmative verb",
  "non-entry", "upgrade path", "past 20", "denominator", "tautolog",
  "nearly as complex", "private method", "polarity word", "_CAP",
  "two live readings").
- What came back: in the baseline and lenses every hit is a pointer
  ("judged against `../../../references/<x>-standard.md` §n", "follow
  `tests-standard.md` §5"); rule text appears only in the standard files.
  Chain to the writer verified: `loom-code/agents/implementer.md:30` sends the
  implementer to the baseline, whose §5 items 2, 6, 8, 9 point to the three
  standards.
  One copy outside the two named documents: `loom-code/agents/adversary.md:72-75`
  still restates the prose-pin rule verbatim (unchanged by this diff, present at
  base). The adversary is neither the implementer's baseline nor the reviewer's
  lens, so the line as written holds.
- Evidence: diff above; grep output; `loom-code/agents/adversary.md:72`.
  Tests: `loom-code/tests/test_tests_standard_text.py`,
  `loom-code/tests/test_code_design_standard_text.py`,
  `loom-code/tests/test_docs_standard_text.py` — passed (see §10 run).

## 3. 抽象層門檻只有一種寫法，寫的人和審的人讀到的是同一句。
- How I tried it: read baseline GREEN step and §5 item 2, lenses `deletion-first`
  row, and `code-design-standard.md` §2; grepped for "single use" and
  "premature abstraction".
- What came back: baseline GREEN now says "a new abstraction meets the threshold
  in `code-design-standard.md` §2"; item 2 points to the same file; lens
  `deletion-first` row says "judged against … §2–3". The only threshold sentence
  is `code-design-standard.md:19-22` ("two concrete users now, an explicit
  request, or a visible motivation"). "single use" / "premature abstraction":
  0 hits.
- Evidence: `loom-code/references/engineering-baseline.md:36`,
  `loom-code/references/code-design-standard.md:19`.

## 4. 測試標準禁止「期望值用和程式相同的方式算出來」的斷言，並要求期望值來自獨立來源（已知正確的字面值、手算範例或規格）。
- How I tried it: read `tests-standard.md` §2.
- What came back: "A tautological assertion is a finding: its expected value is
  computed the same way the code computes it … Expected values must come from an
  independent source: a known-good literal, a worked example done by hand, or the
  spec." Lens `tests` row lists "tautological assertions" as judged there.
- Evidence: `loom-code/references/tests-standard.md:19-24`;
  `loom-code/skills/closing-review/references/lenses.md:58`.

## 5. 程式碼設計標準含 shallow module 判準（介面幾乎和它做的事一樣複雜）和刪除測試（刪掉這個模組後，複雜度是消失還是散到各呼叫者）。
- How I tried it: read `code-design-standard.md` §5.
- What came back: "A module whose interface is nearly as complex as what it does
  … imagine deleting it: if the complexity vanishes with it, the module was a
  pass-through; if the complexity reappears across its callers, the module earns
  its place." Reviewer reaches it through the `architecture` row ("§5–6").
- Evidence: `loom-code/references/code-design-standard.md:43-51`;
  `lenses.md:55`.

## 6. 測試標準禁止綁實作的測試：mock 內部元件、測私有方法、繞過公開介面去驗證結果；判斷依據是「沒改行為的重構會讓它失敗」。
- How I tried it: read `tests-standard.md` §3.
- What came back: "A test coupled to the implementation is a finding: one mocking
  an internal collaborator, one testing a private method, or one verifying
  through a side channel instead of the public interface. The tell: a
  behaviour-preserving refactor breaks the test."
- Evidence: `loom-code/references/tests-standard.md:26-31`.

## 7. 程式碼設計標準含可測試的設計：依賴由外部傳入而不是在內部建立，優先回傳結果而不是直接產生副作用。
- How I tried it: read `code-design-standard.md` §6.
- What came back: "Accept a dependency from outside — as a parameter or a
  constructor argument — rather than creating it inside … Where the behaviour
  allows, return a result rather than producing a side effect."
- Evidence: `loom-code/references/code-design-standard.md:53-58`.

## 8. write-plan 為每個 task 切模組邊界時，指向程式碼設計標準。
- How I tried it: read the write-plan task-size paragraph; resolved the relative
  link from `loom-code/skills/write-plan/`.
- What came back: "Read `../../references/code-design-standard.md` when choosing
  each task's module boundary and entry." The link resolves to
  `loom-code/references/code-design-standard.md`, which exists.
- Evidence: `loom-code/skills/write-plan/SKILL.md:268-270`.

## 9. 搬移前 engineering-baseline 與 lenses 裡屬於這三個主題的每條規則，搬移後仍存在且意思不變（禁止沒有變成允許，門檻沒有放寬或收緊，除第 3 條統一的那一處）。紅 → 綠 → 重構的循環維持不變。
- How I tried it: took every line removed from baseline and lenses
  (`git diff 847fbb6cd HEAD`) and found its new home, comparing direction words.
- What came back (base → HEAD):

  | Removed at base | Now | Direction |
  |---|---|---|
  | baseline item 6 "Tests verify intent…" | tests §1 verbatim | same |
  | baseline item 8 prose-pin | tests §5 verbatim | same |
  | lens tests: cannot-fail finding + 3 shapes | tests §1 verbatim (cross-ref repointed to §5) | same |
  | lens tests: module entry vs internal function | tests §4 verbatim | same |
  | lens naming row | code-design §1 verbatim | same |
  | lens refactoring row | code-design §4 verbatim | same |
  | lens deliberate-simplification row | code-design §7 verbatim | same |
  | lens deletion-first: threshold + "no finding without a concrete alternative" | code-design §2 verbatim | same |
  | lens deletion-first: forwarding finding; "one hiding any of those is not, nor is a re-export…" | code-design §3: "…is outside this rule, and so is a re-export…" | same (exemption kept; wording reworded) |
  | baseline GREEN "no speculative generality, no premature abstraction" + item 2 "no abstraction for a single use" | code-design §2 threshold; item 2 still "Nothing speculative." | changed — the Acceptance 3 unification only |
  | docs omission / ambiguity / inconsistency / incorrect-fact / missing-population | docs §1–5 verbatim; "open the source and read the cited span" kept in lens | same |
  | polarity paragraph | docs §6 (all polarity words, both failure shapes, the not-a-finding carve-out); "severity by consequence" kept in lens | same |
  | Deletion-first for docs and skill paragraph incl. `*_CAP` smell | docs §7 verbatim; severity-by-consequence kept in lens row | same |

  Reviewer-only mechanics (running changed tests, skipped tests, shell-builtin
  artifacts, duplicate-test rules, one-test fix cap, prose-only carve-out) stay in
  the lens `tests` row unchanged. Red → green → refactor: the only edited line in
  that section is the GREEN abstraction sentence above; RED, REFACTOR and the
  cycle order are byte-identical.
- Evidence: diff in §2; `loom-code/references/engineering-baseline.md:28-45`.

## 10. 完整 package suite 通過，loom-code 以新版號釋出。
- How I tried it: ran only the tests covering this change, per station rule
  (not the full suite):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_tests_standard_text.py loom-code/tests/test_code_design_standard_text.py loom-code/tests/test_docs_standard_text.py loom-code/tests/test_prose_pin_rule_text.py loom-code/tests/test_write_plan_entry_definition.py loom-code/tests/test_write_plan_entry_definition_split.py loom-code/tests/test_write_plan_station_text.py`
  plus `loom-code/scripts/check_contract_citations.py`,
  `scripts/sync_codex_manifests.py --check --all`, and read every version string.
- What came back: `82 passed in 0.31s`;
  `test_current_release_metadata_is_synchronized` 1 passed; citations
  `OK: 1 known-violating files unchanged, no new contract citations`;
  manifest sync check exit 0; version 3.91.0 in `.claude-plugin/plugin.json`,
  `.codex-plugin/plugin.json`, `plugin.json`, `package.json`, the three loom-code
  READMEs, root README (table row and section), CHANGELOG `## [3.91.0] — 2026-11-28`
  (base was 3.90.2).
- Full suite: not run here. The full package suite is run by finalize-review,
  which refuses the attestation when it fails. Command:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

## Re-run on 2026-11-28, at 750da7564

Clean copy: `git worktree add --detach <scratch>/at-clean2 750da7564`;
`git status --short` empty before and after. Fix range read in full:
`git diff bf0ae36f6..750da7564` (117aec7e4 scanner scope, f24cfe8ff lens
`tests` rules moved to tests-standard §6 + adversary/implementer pointers,
750da7564 tests-standard §1 and code-design-standard §4 wording).

- Setup: re-tested — `claude plugin validate ./loom-code` from the clean copy:
  `✔ Validation passed`, exit 0; only advisory `ICON_MISSING`.
- 1: re-tested — `ls loom-code/references/`: `tests-standard.md`,
  `code-design-standard.md`, `docs-standard.md` present; read each. tests-standard
  now has §1–§6 (new §6 "A new test earns its place against existing cases",
  test-only content); code-design §1–§7, docs §1–§7 unchanged in scope.
  Evidence: `loom-code/references/tests-standard.md:49-57`.
- 2: re-tested — `git diff 847fbb6cd HEAD` on baseline and lenses, then grep of
  `loom-code/**/*.md` for 22 phrases (the earlier 18 plus "tests of tests",
  "at most one test", "text similarity", "extending an existing test",
  "logic changes", "Duplication and smells"). Rule text hits only in the three
  standards; `lenses.md:58` (tests row) now lists "new tests against existing
  cases" as judged against tests-standard and keeps only reviewer mechanics
  ("Duplicate findings name surviving protection and a smaller shape" stays —
  a reviewer finding format, not a writer rule); `lenses.md:65`, `:80` are
  pointers. Earlier open question confirmed closed: `loom-code/agents/adversary.md:72-73`
  now reads "A test that pins a sentence of prose follows
  `../references/tests-standard.md` §5."; `loom-code/agents/implementer.md:55-56`
  points finding-fix and tests-of-tests to tests-standard §6. One unrelated hit,
  `loom-code/skills/write-plan/SKILL.md:312` "distinct defect", is a planning
  rule outside this fix range and outside the three topics' moved text.
- 3: re-tested — `code-design-standard.md:19-20` still the single threshold
  sentence; `engineering-baseline.md:36-37` GREEN and `lenses.md:65` deletion-first
  point to §2; "single use" / "premature abstraction": 0 hits. The fix touched
  only code-design §4 line 34 ("Duplication and smells; Rule of Three —" →
  "Remove duplication and smells; under the Rule of Three,"; rest verbatim,
  same direction).
- 4: re-tested — `tests-standard.md:16-21` §2 text unchanged by the fix (diff
  shows no hunk in §2); lens tests row still names "tautological assertions".
- 5: carried over — fix diff to `code-design-standard.md` is one line in §4;
  §5 and the lens architecture row (`lenses.md:55`) have no hunk.
- 6: re-tested — `tests-standard.md:23-28` §3 unchanged: mocking an internal
  collaborator, testing a private method, verifying through a side channel;
  "The tell: a behaviour-preserving refactor breaks the test."
- 7: carried over — no hunk in code-design-standard §6.
- 8: carried over — no hunk in `loom-code/skills/write-plan/`; the linked file
  keeps its name and path.
- 9: re-tested — compared every line the fix removed with its new home:

  | Removed in fix range | Now | Direction |
  |---|---|---|
  | lens tests: "compare tests for touched behaviour with existing cases: what distinct defect, input, state, environment or oracle is new?" | tests §6 verbatim | same |
  | lens tests: "ordinary consolidation or deletion requires evidence the retained case detects the old defect, not shared lines, text similarity or counts" | tests §6 verbatim | same |
  | lens tests: "preserve distinct boundary, integration and environment coverage" | tests §6 verbatim | same |
  | lens tests: "unnecessary helpers, harnesses and tests of tests are findings" | tests §6 verbatim | same |
  | lens tests: "the fix for any finding adds at most one test, extending an existing test first" | tests §6 verbatim | same |
  | tests §1 (from baseline item 6 at base): "A test that cannot fail when the logic changes is not a test." | merged: "**Tests verify intent.** A test that cannot fail for the behaviour it names is a finding — …" (the lens's base sentence) | same — judged: both forbid a test that cannot fail; the kept sentence names which change must make it fail. Listed in the report's decisions section. |
  | code-design §4 (lens refactoring row at base) "Duplication and smells; Rule of Three —" | "Remove duplication and smells; under the Rule of Three," | same |

  Red → green → refactor: `git diff be8c2e454 750da7564 -- loom-code/references/engineering-baseline.md`
  is empty, so the cycle is as verified in the first run.
  Outside line 9's two documents: implementer.md "no tests of tests" became
  "tests of tests follow tests-standard §6", whose sentence is "Unnecessary
  helpers, harnesses and tests of tests are findings" — if "Unnecessary"
  qualifies all three, the implementer's absolute ban is now conditional.
  Raised as a nit and an open question in the report.
- 10: re-tested — ran only the tests covering this change and the fix (not the
  full suite):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_tests_standard_text.py loom-code/tests/test_code_design_standard_text.py loom-code/tests/test_docs_standard_text.py loom-code/tests/test_prose_pin_rule_text.py loom-code/tests/test_check_contract_citations.py loom-code/tests/test_write_plan_entry_definition.py loom-code/tests/test_write_plan_entry_definition_split.py loom-code/tests/test_write_plan_station_text.py`
  → `104 passed in 0.45s` (includes
  `test_current_release_metadata_is_synchronized`).
  `python3 loom-code/scripts/check_contract_citations.py` (now scanning
  `loom-code/references`) → `OK: 1 known-violating files unchanged, no new
  contract citations of this repo's records.` exit 0.
  `python3 scripts/sync_codex_manifests.py --check --all` exit 0.
  Version 3.91.0 in all four loom-code manifests, the three loom-code READMEs,
  root README (line 17 table row, line 105 section), CHANGELOG
  `## [3.91.0] — 2026-11-28`.
  Full suite: not run here; run by finalize-review, which refuses the
  attestation when it fails. Command:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.

## Re-run on 2026-11-28, at b4f877e83

Clean copy: `git worktree add --detach <scratch>/at-clean3 b4f877e83`;
`git rev-parse --short HEAD` → `b4f877e83`; `git status --short` empty before
and after; worktree removed afterwards. Fix range read in full:
`git diff 1ec1bc12a..b4f877e83` — two files, one hunk each:
`loom-code/references/tests-standard.md` §6 ("Unnecessary helpers, harnesses
and tests of tests are findings." → "Unnecessary helpers and harnesses are
findings. A test of a test is a finding, except the synthetic self-tests §5
requires.") and the matching pins in
`loom-code/tests/test_tests_standard_text.py` (`MOVED_RULES`,
`RULE_SENTENCES`). Re-tested every row whose surface includes tests-standard
§6 or its pointers (1, 2, 9, 10); others carried over against this diff.

- Setup: re-tested — `claude plugin validate ./loom-code` from the clean copy:
  `✔ Validation passed`, exit 0; only advisory `ICON_MISSING`.
- 1: re-tested — `ls loom-code/references/`: `tests-standard.md`,
  `code-design-standard.md`, `docs-standard.md` present (plus the unrelated
  pre-existing references). Read `tests-standard.md` in full: §1–§6, all
  test-only; §6 now ends "Unnecessary helpers and harnesses are findings. A
  test of a test is a finding, except the synthetic self-tests §5 requires.
  The fix for any finding adds at most one test, extending an existing test
  first." Evidence: `loom-code/references/tests-standard.md:49-58`.
  code-design and docs standards: no hunk in fix range.
- 2: re-tested — grep of `loom-code` for the 22 phrases of the first re-run
  plus "tests of tests", "test of a test", "harnesses", "synthetic
  self-test". Rule text in `.md` files hits only the three standards; the
  remaining `.md` hits are pointers (`lenses.md:58` "every rule in
  `../../../references/tests-standard.md` — … new tests against existing
  cases — is judged here"; `lenses.md:65` "judged against
  `code-design-standard.md`") or unrelated research/example docs
  ("Rule of Three" in `loom-code/research/grounding-v0.1.0.md` and
  `loom-code/docs/examples/typescript-react-toast.md`, "denominator"/"harness"
  in research notes, both outside the baseline and lenses).
  `loom-code/agents/implementer.md:55-56`: "a finding's fix and tests of tests
  follow `../references/tests-standard.md` §6." — pointer only.
  `git diff 750da7564 HEAD` on `loom-code/` touches only tests-standard.md and
  its pin test, so lenses and baseline are as verified in the first re-run.
- 3: carried over — no hunk in code-design-standard.md, baseline or lenses.
- 4: carried over — the only tests-standard hunk is in §6; §2 unchanged.
- 5: carried over — no hunk in code-design-standard.md or lenses.
- 6: carried over — the only tests-standard hunk is in §6; §3 unchanged.
- 7: carried over — no hunk in code-design-standard.md.
- 8: carried over — no hunk in `loom-code/skills/write-plan/`; linked file
  keeps its name and path.
- 9: re-tested — open question from the previous run checked against base:
  `git show 847fbb6cd:loom-code/agents/implementer.md` line 56: "no new test
  harness; no tests of tests" (absolute ban). Base lens `tests` row
  (`git show 847fbb6cd:…/lenses.md` line 58): "unnecessary helpers, harnesses
  and tests of tests are findings". Base baseline line 164 (prose-pin rule):
  "carries synthetic self-tests validating one affirmative example and one
  rejected negated example" — required at base.

  | Base | Now (tests §6) | Direction |
  |---|---|---|
  | implementer "no tests of tests" (absolute) | "A test of a test is a finding, except the synthetic self-tests §5 requires." | same — the only exception is a test the prose-pin rule already required at base; the conflict between the two base rules is now resolved in writing |
  | lens "unnecessary helpers, harnesses and tests of tests are findings" | "Unnecessary helpers and harnesses are findings." + the sentence above | same for helpers/harnesses; tests of tests: no wider than either base reading (absolute minus the base-required self-tests) |

  Red → green → refactor: `git diff 750da7564 b4f877e83 -- loom-code/references/engineering-baseline.md`
  empty, unchanged since the first run. The previous run's nit/open question
  on `implementer.md:55-56` is closed.
- 10: re-tested — ran only the tests covering this change and the fix (not the
  full suite):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python -m pytest -q loom-code/tests/test_tests_standard_text.py loom-code/tests/test_code_design_standard_text.py loom-code/tests/test_docs_standard_text.py loom-code/tests/test_prose_pin_rule_text.py loom-code/tests/test_check_contract_citations.py loom-code/tests/test_write_plan_entry_definition.py loom-code/tests/test_write_plan_entry_definition_split.py loom-code/tests/test_write_plan_station_text.py`
  → `104 passed in 0.40s` (includes the new `RULE_SENTENCES` pin and
  `test_current_release_metadata_is_synchronized`).
  `python3 loom-code/scripts/check_contract_citations.py` → `OK: 1
  known-violating files unchanged, no new contract citations of this repo's
  records.` exit 0. `python3 scripts/sync_codex_manifests.py --check --all`
  exit 0. `"version": "3.91.0"` in all four loom-code manifests; "3.91.0" in
  the three loom-code READMEs and root README (2 hits); CHANGELOG line 3
  `## [3.91.0] — 2026-11-28 — Shared standard files read by writer and judge`.
  Full suite: not run here; run by finalize-review, which refuses the
  attestation when it fails. Command:
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`.
