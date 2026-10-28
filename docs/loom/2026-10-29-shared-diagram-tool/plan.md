# 跨站共用的圖表討論工具（draw.io 為首個後端） — plan
intent: 2026-10-29-shared-diagram-tool@3a626511bc1a134014e046f6d22f2d283c41372b
spec: docs/loom/2026-10-29-shared-diagram-tool/spec.md@1e0adf16
charter: 1.1

## Task DAG

**W0-01 Register the shared tool and its backend contract**  after: —  acceptance: 7
- Files: loom-workflow/skills/loom-diagram/SKILL.md, loom-workflow/skills/loom-diagram/scripts/diagram.py, loom-workflow/skills/loom-diagram/references/backends.md, loom-code/contract/manifest.yaml
- Test: A7 positive: registry-lists-two-backends; boundary: registry-empty-lists-nothing
- Risk: manifest tools entry is counted, so the skill budget rises; default is the declared budget-exception line (agent-decided)

**W0-02 drawio backend**  after: W0-01  acceptance: 1, 4
- Files: loom-workflow/skills/loom-diagram/backends/drawio.py
- Test: A1 positive: drawio-writes-uncompressed-xml; negative: drawio-refuses-compressed-page
- Risk: hand-placed coordinates may look poor; default is the desktop CLI --layout when present, fixed grid otherwise (agent-decided)

**W0-03 Projection generate and compare**  after: W0-01  acceptance: 3
- Files: loom-workflow/skills/loom-diagram/scripts/diagram.py, loom-workflow/skills/loom-diagram/references/projection.md
- Test: A3 positive: projection-regenerates-identical; negative: projection-mismatch-names-node
- Risk: byte comparison may flag cosmetic drift; default is compare on normalised node/edge tuples, not raw bytes (agent-decided)

**W0-04 demo-json backend proves selection**  after: W0-01  acceptance: 7
- Files: loom-workflow/skills/loom-diagram/backends/demo_json.py, loom-workflow/skills/loom-diagram/references/backends.md
- Test: A7 positive: demo-backend-selectable-by-header; negative: unknown-backend-names-registered-ids
- Risk: a demonstration backend may look like dead weight; default is keep it minimal and name it demo in the docs (agent-decided)

**W0-05 Desktop and VS Code setup documentation**  after: W0-02  acceptance: 5, 6
- Files: loom-workflow/skills/loom-diagram/references/editor-setup.md, loom-workflow/skills/loom-diagram/SKILL.md
- Test: A5 positive: setup-doc-reproduces-loop; A6 positive: desktop-autosave-behaviour-documented
- Risk: desktop behaviour changes between releases; default is to pin the verified version and date in the doc (agent-decided)

**W0-06 Station pointers, no restatement**  after: W0-01  acceptance: 8
- Files: loom-design/skills/write-spec/SKILL.md, loom-design/skills/architecture-design/SKILL.md
- Test: A8 positive: two-stations-reference-by-name; negative: no-format-rules-restated-in-stations
- Risk: station text is pinned by tests; default is add the pointer beside the existing diagram sentence and update its pin test (agent-decided)

**W0-07 Mechanism registration and release metadata**  after: W0-01, W0-06  acceptance: 7
- Files: docs/loom/evidence/mechanisms.yaml, loom-workflow/CHANGELOG.md, loom-workflow/.claude-plugin/plugin.json, tests/test_loom_skill_description_catalog.py
- Test: A7 positive: mechanisms-registers-tool-with-eval; negative: missing-budget-exception-is-red
- Risk: mechanism count rises 23 to 24; default is the declared budget-exception CHANGELOG line (agent-decided)

**W0-08 Tests and end-of-Build verification**  after: W0-02, W0-03, W0-04, W0-05, W0-07  acceptance: 1, 2, 3, 4, 5, 6, 7, 8
- Files: loom-workflow/tests/loom-diagram/test_diagram_tool.py, loom-workflow/tests/loom-diagram/test_backends.py, loom-workflow/tests/loom-diagram/test_projection.py
- Test: A3 boundary: projection-of-empty-diagram; A4 negative: malformed-xml-named; A7 boundary: single-backend-registry
- Risk: tests need a fixture .drawio; default is a two-node fixture committed under the test folder (agent-decided)

## Simplicity check
- One shared tool rather than per-station copies — taken
- Backend registry driven by directory listing rather than a framework — taken
- Selection stored in the artifact header rather than a config file — taken
- Second real backend (Penpot) now — declined: the interface plus a demo backend proves the mechanism without owning another tool
- Artifact_type glob for diagrams — declined: artifact_types is reserved and unconsumed; a convention costs nothing

## Questions asked
- ① — what — 「你要走哪條？A：保留窄的另開寬的；B：撤回窄的重寫寬的」
- ① — what — 「請你確認：跨站共用的圖表討論工具…對嗎？」（第一版，七條驗收條件）
- ① — what — 「可以做成 後端可抽換 或是 同時支援多種後端 讓使用者選擇 嗎？」
- ① — what — 「請你確認：跨站共用圖表工具（後端可註冊＋可選擇）…對嗎？」（第二版，八條驗收條件）

## Risks
1. VS Code dirty text buffer stalls agent writes; documented mitigation is autosave or save-before-write.
2. Desktop autosave defaults off, so the default desktop experience is a click-to-sync prompt; documented in editor-setup.
3. Concurrent edits in the same diagram file across two editors keep last-write-wins semantics and can duplicate cells.
4. Skill count rises to 24, allowed only with the declared budget-exception line; a missing line fails check_mechanisms.
5. Backend interface may be shaped wrong before a second real backend exists; the demo backend is the cheap probe for that.
