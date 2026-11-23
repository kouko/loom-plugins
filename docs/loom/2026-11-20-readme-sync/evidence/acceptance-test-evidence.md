# Bring the plugin READMEs back in sync — acceptance test evidence

Tried on 2026-11-23, in a clean copy of the project at 954b0b390
(`git worktree add --detach <scratchpad>/at 954b0b390`, a tree nobody had worked in).

## 1. loom-code's README.ja.md and README.zh-TW.md carry every section and fact of README.md, translated.
- How I tried it: listed headings of all three files (`grep -n '^#'`), then read
  `loom-code/README.md` lines 1-252 and the matching parts of `README.ja.md`
  (1-245) and `README.zh-TW.md` (1-222) paragraph by paragraph. For the install
  sections, diffed the set of backticked tokens (commands, paths) of English vs
  each translation; counted code blocks and links.
- What came back:
  - Headings: 13 sections in each, same order (flow, Skills, Agents, three
    questions, contract package, checker, composing, install with Claude Code /
    Codex / Antigravity CLI / OpenCode, licence).
  - Checker section: every English fact is present in both translations — the
    version-1 `plan`/`intake` result, the five JSON commands, mixed help/JSON
    usage error, delivery's `{state, reason, next, evidence, complete}` plus
    `suggested_next` equal to `next`, the empty-stderr envelope fields, `data`
    only on `contract`/`reviewer-count`, the typed-data table, exit 0/1/2
    meanings, reviewer-count has no blocker, the checked consumer and its three
    commands, `2.99` blocked / `bad` usage error, advice-handling rules, 30-second
    timeout and exit 86, sixteen commands / five JSON modes / two consumers,
    CLI result guide link, "no gain measured", the deterministic checker,
    `PreToolUse` hook and main/master guard, `loom-python --repair/--ready`.
  - Code blocks: 14 / 14 / 14. Links: 20 / 20 / 20. Install-section backtick
    tokens: identical sets (diff empty for both translations).
  - Translations add a few clarifications the English does not state
    (e.g. ja: an invalid `--goal` as an example of a pre-result delivery
    failure; ja/zh-TW: the manifest version is whitespace-stripped and returned
    as `data.contract_version`). No English fact is missing.
- Evidence: `loom-code/README.ja.md:124-228`, `loom-code/README.zh-TW.md:110-207`
  against `loom-code/README.md:124-232`.

## 2. loom-workflow's three READMEs say what an "old map" is (a decision map from before roadmap replaced it) on first use.
- How I tried it: `grep -n -i 'map\|マップ'` over the three READMEs, excluding
  "mapping", to find the first occurrence of the term.
- What came back:
  - `loom-workflow/README.md:70` — "**Old maps** (decision maps from before `roadmap` replaced them) remain"
  - `loom-workflow/README.ja.md:70` — "**旧 map**（`roadmap` が置き換える前の decision map）"
  - `loom-workflow/README.zh-TW.md:64` — "**舊 map**（`roadmap` 取代前的 decision map）保留可讀歷史"
  - Every earlier "map" hit is the word `roadmap` itself; the definition sits at the first use.
- Evidence: the three lines above.

## 3. The complete package suite passes.
- How I tried it (in the clean copy):
  `env -u FORCE_COLOR -u CLAUDE_CODE_SESSION_ID uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`
- What came back: exit 0. Largest pytest batch `2920 passed in 140.31s`; every
  batch line reports passed (one `250 passed, 5 skipped`); no `failed` or
  `error` lines. Shell tests end `13/13 mermaid blocks parsed`, `PASS` lines.
- Evidence: captured log (scratchpad `suite.log`), tail: `exit 0`.
