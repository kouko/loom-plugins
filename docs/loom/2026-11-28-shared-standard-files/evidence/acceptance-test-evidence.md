# Writer and judge read one standard — acceptance test evidence

Tried on 2026-11-28, in a clean copy of the project at be8c2e454
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
