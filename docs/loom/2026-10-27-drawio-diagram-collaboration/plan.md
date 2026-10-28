# 計畫：與 agent 協作編輯 draw.io 圖表以溝通規格與介面設計
originator: kouko
kind: engineering
status: open
needs-design: yes — 已在 spec.md 中落實

## Station summary
| station | artifact | who decides | checker | checkpoint |
|---|---|---|---|---|
| capture-intent | intent — docs/loom/intent/2026-10-27-drawio-diagram-collaboration.md | user — ① | intent.schema, intent.needs-design-reason | N/A |
| write-spec | spec — docs/loom/2026-10-27-drawio-diagram-collaboration/spec.md | user — ② (product only); agent declares pre-build risk | intake.confirmed, standing.product-principles-reject | required: one independent spec+adversarial reviewer; ② not asked for engineering changes |
| write-plan | plan — docs/loom/2026-10-27-drawio-diagram-collaboration/plan.md | agent-decided (runs ① itself when loom-design absent) | intake.confirmed, intake.confirmed-behavior, intake.spec-ready, intake.test-case-pair | a fresh plan-lens reviewer checks for a simpler shape before Build |
| build | diff — commits on the change branch | agent-decided | task and integration tests; at end of Build, independent adversary's adversarial programs and package suite | no formal review during Build; one closing review follows completed functional work |
| closing-review | attestation.json, acceptance test report when needed | fresh-context reviewers | reviewers see only content that passed Build's checks; finalize-review executes package suite and adversarial again on committed content | branch end, or again only after functional content changes |
| ship | diff / PR — pushed change branch and its pull request | automatic for canonical intent authorisation; one user decision for legacy intent; merge separate | push.contextual-body and publish.preconditions; verification status disclosed, not a refusal; no functional replay | before push; publication-only fixes reuse matching evidence |
| maintain | intent — fresh docs/loom/intent/<change-id>.md | agent (dedupe mechanical) | intent.schema, intent.needs-design-reason, intent.needs-design-recompute, intent.product-no-identifiers on a new intent | before hand-off to write-plan |

## Task DAG
- **T1** Integrate diagram collaboration into write-spec: extend SKILL.md with "Diagram collaboration" section, add reference `references/diagram-collaboration.md`, add check script `scripts/check_diagram.py`, diagram file convention `diagrams/<slug>.drawio` with projection `diagrams/<slug>.projection.md` — acceptance: REQ-1 through REQ-6 each own a mechanical or reviewer check; files: `spec.md`, `scripts/check_diagram.py`, `references/diagram-collaboration.md`, `docs/loom/2026-10-27-drawio-diagram-collaboration/spec.md` — risks: none closed yet, all open until Build
- **T2** Write-plan records the questions list and carried details (see ## Questions asked) — acceptance: plan checklist green; files: `plan.md` — risks: none
- **T3** Build runs the package suite and adversarial against the committed change — acceptance: all existing tests green; risks: none unless new checker rules introduced

## Risks
- REQ-1 staleness if VS Code text buffer dirty (mitigation: recommend users enable autosave or save before agent writes)
- REQ-3 projection vs diagram mismatch detection threshold (mitigation: script diff is byte-for-byte; small textual differences flagged)
- REQ-6 desktop autosave default off (mitigation: documented in constraints; user opt-in)
- Merging concurrent edits in same .drawio file (mitigation: design caveats in spec; both editors keep last-write-wins)

## Current State Evidence
- Forward: loom-design/skills/write-spec/SKILL.md §Step 2 "UI flows" — today UI flows are text only, no diagram channel
- Reverse: capture-intent hands confirmed intent to write-spec; this change adds diagram mechanism to write-spec
- Error: no diagram validation exists today; no check script; grep finds no diagram file convention or mechanism in repo
- Data: change folder today contains intent.md, spec.md, plan.md (now), evidence/ — no diagrams/ folder or .drawio files yet
- Boundary: this change stops at write-spec integration + the check script; no new station, no artifact_type glob beyond existing defaults; mechanism count stays at 23 skills (written as extension within existing skill, not a counted standalone)

## Questions asked (verbatim, per decision point)
- ① — what — 「這份研究之後，你想怎麼推進？」(options: 立案/spike/停在報告)
- ① — what — 「你要的是：規格與介面設計的討論改用同一張 draw.io 圖…對嗎？」
- ① — what — 「顯示面要釘成哪一個？（只釘 VS Code／VS Code 為主＋桌面版可用／只釘桌面版）」
- ① — what — 「瀏覽器版要維持這次不做，還是調整？」
- ① — what — 最終重述確認六條驗收條件

## Carried details (user's explicit yes)
- 「理想情境是使用者跟 agent 都可以即時看到圖表並且使用者可以手動編輯圖表」
- 「取代傳統的純文字來回溝通」
- 「同時支援 vs code 與桌面版」
- 「沒有其他不可逆的動作——這次只新增檔案，不動你既有的資料」

## Simplicity check (charter 1.1)
- Each simpler shape taken or declined with reason, or none found.
- Chosen: extend existing skill rather than add new counted skill; convention over artifact type; file-level integration over element-level driving; two-editor sync via file watchers only; immediate互動優於遊標級多人協作，因為後者與「圖檔進版控」不相容。

## Plan-wide Risks
- If users do not enable autosave or save before agent writes, REQ-1 staleness; documented in constraints as opt-in.
- Concurrent edits in same .drawio file across VS Code and desktop; mitigation: documented design caveats; known merge bug #2382 under repair but residual risk low.
- No browser/embed/MCP integration this change; re-trigger: when diagram annotation or agent-on-diagram marking is demanded.