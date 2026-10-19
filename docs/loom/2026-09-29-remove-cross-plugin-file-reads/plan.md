# Each plugin uses only its own files — plan
intent: 2026-09-29-remove-cross-plugin-file-reads@879dd3a9
spec: docs/loom/2026-09-29-remove-cross-plugin-file-reads/spec.md
charter: 1.1

## Current State Evidence
- Forward: loom-design capture-intent/SKILL.md:59-69 runs `<loom-code>/scripts/loom_checker.py contract`; five design skills do the same via references/locate-loom-code.md.
- Reverse: loom-code write-plan/SKILL.md:203-210 skips ① for a confirmed intent, so `loom_checker.py intent` never runs there.
- Error: loom-workflow distill-sessions/scripts/main.py:79 resolves parents[4]; in an installed cache the SKILL.md read returns empty text.
- Data: templates read from loom-code at capture-intent/SKILL.md:125-126,175-190, second-vendor.md:19-21, write-spec/SKILL.md:111-112, product-principles/SKILL.md:40-44.
- Boundary: scripts/check_plugin_boundaries.py:40-45,158 scans only tracked .md files; CI runs it for loom-code and loom-design only (ci.yml:126-127).

## Task DAG

### Wave 1

**W1-01 write-plan runs the intent check on a confirmed intent**  after: —  acceptance: 4
- Files: loom-code/skills/write-plan/SKILL.md, loom-code/tests/test_write_plan_station_text.py
- Test: A4 positive: broken-confirmed-intent-blocked-at-write-plan; negative: valid-intent-passes-intent-step.
- Risk: agent-decided per spec REQ-4: explicit `intent` step after branch-first, not folded into intake (intake fixtures use uncommitted intents); test_loom_checker_intent.py coverage preserved.

**W1-02 Template copies and parity test**  after: —  acceptance: 2
- Files: loom-design/skills/capture-intent/templates/*.md, loom-design/skills/write-spec/templates/spec-minimal.md, loom-design/skills/write-spec/references/spec-forms.md, tests/test_contract_template_copies.py
- Test: A2 positive: copies-match-originals; boundary: grammar-matches-manifest (one parametrized byte-compare; the one-side edit runs as an adversary probe).
- Risk: agent-decided per spec REQ-2: one byte-compare root test, no sync script; grammar inlined in spec-forms.md and compared with manifest.yaml.

**W1-03 loom-workflow stops reading loom-code**  after: —  acceptance: 1
- Files: loom-workflow/skills/decision-map/SKILL.md, loom-workflow/skills/distill-sessions/SKILL.md, loom-workflow/skills/distill-sessions/scripts/main.py, loom-workflow/tests/distill-sessions/test_main.py
- Test: A1 positive: boundary-check-passes-on-workflow-tree (W3-01); negative: distill-payload-keys-unchanged (existing test_main.py).
- Risk: agent-decided per spec REQ-1: drop repo-root resolver; agent reads target SKILL.md from its loaded base directory; test_main.py payload-key coverage preserved.

### Wave 2

**W2-01 loom-design stops reading loom-code**  after: W1-02  acceptance: 1, 5
- Files: loom-design/skills/*/SKILL.md, loom-design/skills/capture-intent/references/second-vendor.md, loom-design/skills/capture-intent/references/locate-loom-code.md, loom-design/plugin.json, loom-design/.claude-plugin/plugin.json, loom-design/.codex-plugin/plugin.json, loom-design/tests/spec/*.py, tests/test_loom_plugin_install_layout.py
- Test: A1 positive: boundary-check-passes-on-design-tree (W3-01); negative: skill-name-handoff-not-flagged (W3-01). A5 positive: unratified-principles-interview-in-first-confirmation; boundary: ratified-principles-no-interview.
- Risk: agent-decided per spec REQ-1/REQ-5: delete locate-loom-code.md; principles check becomes a PRINCIPLES.md read; refusal-only pin tests deleted, not converted.

### Wave 3

**W3-01 Boundary check scans scripts and loom-code path forms**  after: W1-03, W2-01  acceptance: 3
- Files: scripts/check_plugin_boundaries.py, tests/test_check_plugin_boundaries.py, .github/workflows/ci.yml
- Test: A3 positive: planted-loom-code-read-in-py-and-placeholder-flagged; negative: python-comment-and-skill-name-not-flagged.
- Risk: agent-decided per spec REQ-3: Python comment lines exempt (provenance only); CI adds loom-workflow; test_check_plugin_boundaries.py coverage widened, not narrowed.

**W3-02 Release bump**  after: W1-01, W1-02, W1-03, W2-01, W3-01  acceptance: 6
- Files: loom-*/plugin.json, loom-*/.claude-plugin/plugin.json, loom-*/.codex-plugin/plugin.json, loom-*/CHANGELOG.md, README.md and loom-*/README*.md, version pin tests
- Test: A6 positive: current-release-metadata-synchronized; negative: existing pin test RED after manifest bump, GREEN after rewrite; no new test.
- Risk: agent-decided per spec: loom-code 3.23.0, loom-design 2.7.0, loom-workflow 5.5.5; committed in Build before finalize.

## Simplicity check
- Drop per-plugin A1 scan tests; W3-01's widened boundary check on the live tree proves A1 — taken
- Drop the parity mutation test; adversary runs the one-side edit as a probe — taken
- Version pin negative is the existing test's RED run, not a new test — taken

## Questions asked
① — what — 覆述 v1（刪呼叫＋複製範本，含自動發布授權）→ 「幫我用 codex 獨立 review 一下」
① — consequence — codex review 的費用、資料外送與本機執行揭露 → 「同意」
① — what — 覆述 v2（加入 distill-sessions、write-plan 補 4 項 intent 檢查、原則訪談時機不變）→ 「所以新規劃裡面有移除所有跨plugin 的檔案引用行為嗎？ 替代機制是？」「你評估這是當前的最佳做法嗎？」→ 「對」

## Risks
1. Format errors in a confirmed intent now surface at write-plan, one station later; a needs-design fix costs one new commit carrying the line.
2. W2-01 is the widest task (five skills, manifests, pin tests); one implementer keeps loom-design's pinned station tables consistent.
3. The sync-script idea raised in conversation was replaced by one parity test; if copies drift often, a sync script can follow.
