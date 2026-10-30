# 跨站共用的圖表討論工具（draw.io 為首個後端） — plan
intent: 2026-10-29-shared-diagram-tool@93d7b523f79445d925380c9dcbeda8c289537fd6
spec: docs/loom/2026-10-29-shared-diagram-tool/spec.md@7532880f
charter: 1.1

## Task DAG

**W0-01 Register the shared tool and its backend contract**  after: —  acceptance: 7
- Files: loom-workflow/skills/loom-interactive-diagram/SKILL.md, loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py, loom-workflow/skills/loom-interactive-diagram/references/backends.md, loom-code/contract/manifest.yaml
- Test: A7 positive: registry-lists-two-backends; boundary: registry-empty-lists-nothing
- Risk: manifest tools entry is counted, so the skill budget rises; default is the declared budget-exception line (agent-decided)

**W0-02 drawio backend**  after: W0-01  acceptance: 1, 4
- Files: loom-workflow/skills/loom-interactive-diagram/backends/drawio.py
- Test: A1 positive: drawio-writes-uncompressed-xml; negative: drawio-refuses-compressed-page; A4 positive: valid-xml-accepted; negative: malformed-xml-rejected
- Risk: hand-placed coordinates may look poor; default is the desktop CLI --layout when present, fixed grid otherwise (agent-decided)

**W0-03 Projection generate and compare**  after: W0-01  acceptance: 3
- Files: loom-workflow/skills/loom-interactive-diagram/scripts/diagram.py, loom-workflow/skills/loom-interactive-diagram/references/projection.md
- Test: A3 positive: projection-regenerates-identical; negative: projection-mismatch-names-node
- Risk: byte comparison may flag cosmetic drift; default is compare on normalised node/edge tuples, not raw bytes (agent-decided)

**W0-04 demo-json backend proves selection**  after: W0-01  acceptance: 7
- Files: loom-workflow/skills/loom-interactive-diagram/backends/demo_json.py, loom-workflow/skills/loom-interactive-diagram/references/backends.md
- Test: A7 positive: demo-backend-selectable-by-header; negative: unknown-backend-names-registered-ids
- Risk: a demonstration backend may look like dead weight; default is keep it minimal and name it demo in the docs (agent-decided)

**W0-05 Desktop and VS Code setup documentation**  after: W0-02  acceptance: 5, 6
- Files: loom-workflow/skills/loom-interactive-diagram/references/editor-setup.md, loom-workflow/skills/loom-interactive-diagram/SKILL.md
- Test: A5 positive: setup-doc-reproduces-loop; boundary: fresh-checkout-with-installed-prerequisites; A6 positive: desktop-autosave-behaviour-documented; negative: autosave-off-requires-sync-click
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
- Files: loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py, loom-workflow/tests/loom-interactive-diagram/test_backends.py, loom-workflow/tests/loom-interactive-diagram/test_projection.py
- Test: A1 positive: editor-shows-agent-update; boundary: dirty-editor-save-before-write; A2 positive: user-edit-read-back; negative: unsaved-edit-not-on-disk; A3 positive: projection-matches; negative: stale-projection-rejected; A4 positive: valid-diagram-accepted; negative: malformed-xml-named; A5 positive: clean-source-loop; boundary: prerequisites-already-installed; A6 positive: desktop-autosave-sync; negative: autosave-off-prompt; A7 positive: two-backends-selectable; boundary: single-backend-registry; A8 positive: shared-skill-pointed-to; negative: no-station-rule-duplication
- Risk: tests need a fixture .drawio; default is a two-node fixture committed under the test folder (agent-decided)

**W0-09 Graduate defect-catching adversarial probes**  after: W0-08  acceptance: 3, 4
- Files: loom-workflow/tests/loom-interactive-diagram/test_diagram_tool.py; source programs: docs/loom/2026-10-29-shared-diagram-tool/evidence/probes/test_reference_link_invalid_diagram.py, docs/loom/2026-10-29-shared-diagram-tool/evidence/probes/test_parenthesized_link_invalid_diagram.py
- Test: A3 positive: valid-reference-link-passes; negative: reference-style-link-to-malformed-diagram-fails; A4 positive: valid-parenthesized-link-passes; negative: balanced-parenthesis-link-to-malformed-diagram-fails
- Risk: both probes caught real defects, so graduate their cases before finalization while preserving the adversarial execution evidence required by closing review (agent-decided)

**W1-01 Detect a saved diagram edit within the active turn**  after: W0-09  acceptance: 9, 10
- Files: loom-workflow/skills/loom-interactive-diagram/scripts/wait_for_save.py, loom-workflow/skills/loom-interactive-diagram/SKILL.md, loom-workflow/skills/loom-interactive-diagram/references/editor-setup.md, loom-workflow/tests/loom-interactive-diagram/test_wait_for_save.py, loom-workflow release metadata and version-pin test
- Test: A9 positive: changed-content-save-returns-without-message; negative: missing-or-unreadable-diagram-is-named; A10 positive: unrelated-file-change-is-ignored; negative: unchanged-content-save-does-not-return-change
- Risk: event watchers fail with EMFILE inside the sandbox; use a finite Python content poll on one path and state no actor attribution (agent-decided; REQ-9/10)

**W1-02 Graduate the non-finite-duration adversarial case**  after: W1-01  acceptance: 9
- Files: loom-workflow/tests/loom-interactive-diagram/test_wait_nonfinite_arguments.py; source program: docs/loom/2026-10-29-shared-diagram-tool/evidence/probes/test_wait_nonfinite_arguments.py
- Test: A9 positive: finite-duration-wait-starts; negative: nan-or-infinite-duration-is-rejected-before-ready
- Risk: the probe caught a bounded-wait defect, so move it into the permanent suite and keep its concern marker and exact negative cases (agent-decided; REQ-9)

## Simplicity check
- One shared tool rather than per-station copies — taken
- Backend registry driven by directory listing rather than a framework — taken
- Selection stored in the artifact header rather than a config file — taken
- Second real backend (Penpot) now — declined: the interface plus a demo backend proves the mechanism without owning another tool
- Artifact_type glob for diagrams — declined: artifact_types is reserved and unconsumed; a convention costs nothing
- Background host bridge — declined: the user selected active-turn waiting only; the smaller bounded poller needs no persistent service
- Independent review found no simpler shape — taken

## Questions asked
- ① — what — 「你要走哪條？A：保留窄的另開寬的；B：撤回窄的重寫寬的」
- ① — what — 「請你確認：跨站共用的圖表討論工具…對嗎？」（第一版，七條驗收條件）
- ① — what — 「可以做成 後端可抽換 或是 同時支援多種後端 讓使用者選擇 嗎？」
- ① — what — 「請你確認：跨站共用圖表工具（後端可註冊＋可選擇）…對嗎？」（第二版，八條驗收條件）
- ① — what — 「你要的是表中第一種，完成後存檔即可讓正在等待的 agent 讀回修改，對嗎？」

## Risks
1. VS Code dirty text buffer stalls agent writes; documented mitigation is autosave or save-before-write.
2. Desktop autosave defaults off, so the default desktop experience is a click-to-sync prompt; documented in editor-setup.
3. Concurrent edits in the same diagram file across two editors keep last-write-wins semantics and can duplicate cells.
4. Skill count rises to 24, allowed only with the declared budget-exception line; a missing line fails check_mechanisms.
5. Backend interface may be shaped wrong before a second real backend exists; the demo backend is the cheap probe for that.
6. A file-content digest detects a changed file but cannot identify the actor that saved it; the agent must describe observed content, not assert provenance.
