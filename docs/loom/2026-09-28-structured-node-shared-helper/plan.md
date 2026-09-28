# Shared rendering helpers for loom-visualization generators — plan
intent: 2026-09-28-structured-node-shared-helper@3c173a02
charter: 1.1

## Current State Evidence
- Forward: `scripts/gen_flow.py:113-166` and `scripts/gen_arch.py:194-243` — four near-identical title/separator/body render blocks (string-`\n` + dict branches in each).
- Reverse: `scripts/gen_flow.py:32-41` and `scripts/gen_arch.py:31-40` — byte-identical `_center`; `scripts/gen_tree.py:57` duplicates the empty-body message seen in both flow/arch.
- Error: `scripts/gen_seq.py:70-78` and `scripts/gen_bar.py:29-32` — same `split_lines(x) != [x]` single-line guard, message differs per label kind.
- Data: `scripts/width.py:27-160` — existing shared `display_width`/`wrap_label`/`split_lines`; the home for the new helpers.
- Boundary: `scripts/gen_arch.py:159-162` `_pad_line` vs `scripts/gen_table.py:32-34` `_pad` — different semantics, deliberately not merged.

## Task DAG

**W1-01 Shared helpers land in width.py**  after: none  acceptance: 1,3
- Files: loom-workflow/skills/loom-visualization/scripts/width.py, loom-workflow/tests/loom-visualization/test_ascii_width.py
- Test: A1 positive: width.py exports render_structured_node/center/EMPTY_BODY/require_single_line; boundary: empty-body render raises EMPTY_BODY. A3 positive: helper tests green in package suite; boundary: suite passes clean.
- Risk: helpers must reproduce current rendering byte-for-byte; port exact padding/wrap behaviour from the four blocks, agent-decided.

**W1-02 gen_flow.py consumes the helpers**  after: W1-01  acceptance: 1,2
- Files: loom-workflow/skills/loom-visualization/scripts/gen_flow.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: both flow render branches call the shared helper; negative: no inline duplicate block remains. A2 positive: CJK multi-line node output byte-identical; negative: plain single-line label path unchanged.
- Risk: structured-node and plain-label paths must not cross; existing generator fixtures pin the golden output, agent-decided.

**W1-03 gen_arch.py consumes the helpers**  after: W1-01  acceptance: 1,2
- Files: loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: both arch render branches call the shared helper; negative: no inline duplicate block remains. A2 positive: dict-node output byte-identical; boundary: string-`\n` node output unchanged.
- Risk: arch cell layout differs from flow; helper call must feed per-cell interior widths unchanged, agent-decided.

**W1-04 gen_tree.py shares the empty-body constant**  after: W1-01  acceptance: 1,2
- Files: loom-workflow/skills/loom-visualization/scripts/gen_tree.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: tree raises the shared EMPTY_BODY message; negative: no inline message string remains. A2 positive: tree node output byte-identical; boundary: empty-body ValueError text unchanged.
- Risk: message text is a fixed string elsewhere; export it once, import everywhere, agent-decided.

**W1-05 gen_seq.py and gen_bar.py share the single-line guard**  after: W1-01  acceptance: 1,2
- Files: loom-workflow/skills/loom-visualization/scripts/gen_seq.py, loom-workflow/skills/loom-visualization/scripts/gen_bar.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: both generators route multi-line rejection through the shared guard; negative: no inline guard remains. A2 positive: per-kind rejection message text unchanged; boundary: single-line output byte-identical.
- Risk: guard takes a message arg so each file's wording survives; existing rejection tests pin behaviour, agent-decided.

**W2-01 Golden output comparison and full verification**  after: W1-02,W1-03,W1-04,W1-05  acceptance: 2,3
- Files: docs/loom/2026-09-28-structured-node-shared-helper/evidence/, loom-workflow/tests/loom-visualization/
- Test: A2 positive: pre/post generator outputs diff empty across all shapes incl CJK; negative: align.py reports no drift. A3 positive: package suite green; boundary: full run clean.
- Risk: golden diff is the A2 proof; run every generator on the intent's CJK samples before and after, agent-decided.

**W2-02 Release metadata bump**  after: W2-01  acceptance: 3
- Files: loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md, README.md
- Test: A3 positive: synchronized-release-metadata test green after bump; negative: stale version strings detected by grep pins.
- Risk: patch bump 5.5.1 per repo versioning rule; test_release_metadata pins must move in lockstep, agent-decided.

## Simplicity check
- Add shared helpers to the existing width.py — taken
- A fresh scripts/structured_node.py module — declined: width.py already holds the shared width/wrap primitives; one home, five consumers
- Merge _pad and _pad_line too — declined: different semantics, output would change (intent Out of scope)

## Questions asked
- decision_point_1 — what — 「可以再確認一下是否有其他相關原始碼或是執行散文可以模組化為共用元件嗎？另外也確認一下共用之後是否仍符合 skill 的檔案共用原則」
- decision_point_1 — what — 「C 的話共用規範還符合 anthropic 官方的 skill 建議嗎？」
- decision_point_1 — what — 「做 C 吧」→ C：抽 #1–#4（結構化節點渲染、_center、空 body 訊息、seq/bar 單行驗證），不抽 #5 sys.path bootstrap；官方規範（platform.claude.com overview＋best-practices）與 repo AGENTS.md 皆查證合規

## Risks
1. A helper that drifts from the four blocks' exact output breaks A2 silently — golden diff (W2-01) is the guard; port behaviour, never re-imagine it.
2. `gen_seq`/`gen_bar` error message wording is a fixed string in existing tests — the shared guard must accept a per-call message so text survives.
3. Version pins move in three manifests plus tests — W2-02 bumps patch and syncs all in one commit; stale-string grep is the backstop.
