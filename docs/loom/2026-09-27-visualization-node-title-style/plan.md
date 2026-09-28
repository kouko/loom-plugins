# Unified node text structure for loom-visualization — plan
intent: 2026-09-27-visualization-node-title-style@ef9582e
spec: docs/loom/2026-09-27-visualization-node-title-style/spec.md@cfe7638
charter: 1.1

## Task DAG
<!-- Wave 1: generator support (independent, then Wave 2 docs, Wave 3 release) -->

**W1-01 Structured node input in flow and arch generators**  after: none  acceptance: 1,4
- Files: loom-workflow/skills/loom-visualization/scripts/gen_flow.py, loom-workflow/skills/loom-visualization/scripts/gen_arch.py, loom-workflow/skills/loom-visualization/scripts/width.py, loom-workflow/tests/loom-visualization/test_ascii_generators.py
- Test: A1 positive: flow+arch structured CJK node renders title/separator/body left-aligned; boundary: empty body rejects. A4 positive: seq/bar single-line input unchanged; negative: seq/bar multi-line input rejects.
- Risk: `\n` label maps title→first line, rest→body (spec REQ-1); body wraps width-aware via new `width.wrap_label` (spec Design: Body wrapping); stdlib only. agent-decided.

**W1-02 Tree bulleted continuation + node-structure check**  after: W1-01  acceptance: 1,3
- Files: loom-workflow/skills/loom-visualization/scripts/gen_tree.py, loom-workflow/skills/loom-visualization/scripts/checks_nodes.py, loom-workflow/skills/loom-visualization/scripts/align.py
- Test: A1 positive: tree structured CJK node renders title/body as bulleted continuation lines; boundary: empty body rejects. A3 positive: checks_nodes wired into align.py; negative: multi-line box without separator flagged.
- Risk: check wired into align.py's check list (spec Design: check joins the oracle); mechanisms ledger entry per non-negotiable 4. agent-decided.

<!-- Wave 2: skill docs and templates -->

**W2-01 Node-structure reference and SKILL.md pointers**  after: W1-02  acceptance: 3
- Files: loom-workflow/skills/loom-visualization/references/node-structure.md, loom-workflow/skills/loom-visualization/SKILL.md
- Test: A3 positive: reference states two body forms, separator/bullet marks, left alignment, and the expand-or-delete content rule; negative: unstructured multi-line box and empty separator named as failure modes in SKILL.md
- Risk: one reference home; SKILL.md stays under its ~6,000-token cap (spec Design: docs home). agent-decided.

**W2-02 Templates adopt the node structure**  after: W2-01  acceptance: 2
- Files: loom-workflow/skills/loom-visualization/templates/02-linear-steps.md, loom-workflow/skills/loom-visualization/templates/03-branching-decision.md, loom-workflow/skills/loom-visualization/templates/04-reasoning-chain.md, loom-workflow/skills/loom-visualization/templates/05-state-lifecycle.md, loom-workflow/skills/loom-visualization/templates/07-hierarchy.md, loom-workflow/skills/loom-visualization/templates/08-system-architecture.md, loom-workflow/tests/loom-visualization/test_templates.py
- Test: A2 positive: hand-authored ASCII (03/04/05) shows title/separator/body and passes align.py checks; negative: updated Mermaid blocks still parse (validate_mermaid.mjs) and still start with the expected diagram type
- Risk: flowchart rectangles carry the div/`•` structure; diamonds and states stay title-only (spec Design: per-type capability); test_templates pins stay green. agent-decided.

<!-- Wave 3: release and integration -->

**W3-01 Version bump**  after: W2-02  acceptance: 5
- Files: loom-workflow/plugin.json, loom-workflow/.claude-plugin/plugin.json, loom-workflow/.codex-plugin/plugin.json, loom-workflow/CHANGELOG.md, loom-workflow/README.md, loom-workflow/README.ja.md, loom-workflow/README.zh-TW.md, README.md
- Test: A5 positive: synchronized-release-metadata test green after the bump; negative: stale version strings detected by grep pins.
- Risk: minor bump (skill guidance + generator behaviour); test_release_metadata pins CURRENT to 5.4.0 must move in lockstep. agent-decided.

**W3-02 Mechanism ledger entry**  after: W3-01  acceptance: 5
- Files: docs/loom/evidence/mechanisms.yaml
- Test: A5 positive: mechanism-count check passes with checks_nodes registered; negative: count-and-eval check detects the new entry missing its eval.
- Risk: PRINCIPLES.md non-negotiable 4 — every new mechanism needs a regression eval and a count-line, no net raise without declared budget exception. agent-decided.

## Simplicity check
- none found

## Questions asked
decision_point_1 — what — 「任何節點」的邊界畫在哪裡：只有畫成框的節點，還是所有文字槽（含箭頭標籤、表格儲存格、數值標籤、sequence 參與者與訊息）？
decision_point_1 — what — 只有標題、沒有內文的節點要強制畫分隔線，還是格式當容器？
decision_point_1 — what — 標題與內文對齊：都靠左，還是標題沿用置中慣例？
decision_point_1 — consequence — 發佈授權：closing-review 通過後自動 push 開 PR，還是 merge 前先問？

## Risks
1. Template example drift: generated JSON examples must reproduce their printed output exactly (test_templates pins); regenerate output blocks, never hand-edit.
2. Mermaid parse failures from new label syntax: every updated block must pass validate_mermaid.mjs; quoted-label + single-quoted-attr nesting is the known trap.
3. checks_nodes changes align.py behaviour for existing callers: existing fixtures in test_ascii_checks.py must stay green; widen, never narrow.
