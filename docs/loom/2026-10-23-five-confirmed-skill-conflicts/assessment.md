# Assessment and proposed repair scope

Status: historical assessment, superseded for execution by the confirmed intent, spec and plan. The user authorized implementation and verification on 2026-10-23 with 「開始吧」; publication and merge remain excluded. References to pending authorization below describe planning-time state only.

Intent: `../intent/2026-10-23-five-confirmed-skill-conflicts.md`.

## Evidence and decision

GO for a bounded repair proposal. Four findings remain local instruction repairs. The user challenged the proposed no-filesystem boundary for F37 because retrospective analysis should compare session evidence with skill source. F37 now needs a source-grounded analysis design across the existing stages; simply deleting the read instruction is no longer the proposed solution. Four skills across two plugins remain affected, but the earlier estimate of five Markdown files is withdrawn. Dispatch scripts, source references, prompts, and tests may also change. A spec is required before an implementation plan is committed.

The independent review is retained at `/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-findings-rereview-2iovm_it/independent-review.zh-TW.md`; its machine-readable decisions are in the adjacent `adjudication.json`. Stable finding IDs below map to that report. Source locations describe the current checkout and must be refreshed before implementation.

## Proposed repairs (agent-decided, not yet implemented)

| Finding / Acceptance | Current source | Smallest repair | Reason |
|---|---|---|---|
| F09 / A1 | `loom-design/skills/write-spec/SKILL.md:70–73`, `105–107`, `239–240` | Replace the instruction that principles reorder Requirements with an instruction that they constrain admissible requirements and design decisions. Preserve the confirmed Acceptance order and mapping. | The exact-order contract is repeated and protects traceability. Principles can constrain content without moving requirement rows. Do not reorder the confirmed intent to hide the conflict. |
| F10 / A2 | `loom-design/skills/write-spec/SKILL.md:153–154`, `293–297` | Make the handoff conditional: a product change reports confirmation only after it occurred; an engineering change reports that decision point ② is not applicable. | Preserves the existing product-only stop and truthful provenance. Do not add a confirmation stop for engineering changes or invent a new status field. |
| F14 / A3 | `loom-workflow/skills/dbt-model-style/SKILL.md:15`, `163` | Describe `title` as the human-readable model name in the user's working language. Keep Chinese examples explicitly illustrative. | The general language contract already covers all frontmatter values. The header validator checks shape, not natural language; do not add a language detector or translate identifiers. |
| F27 / A4 | `loom-workflow/skills/loom-memory/SKILL.md:108–120`; `references/operations.md:56–71` | After classification, distinguish a new/empty store from existing content. Initialize a new/empty store before reading the index or writing the first concept. For an existing store, read/search before adding a concept; route matches to Reconcile. Regenerate and validate after writing. | `init` already supports absent/empty stores and refuses populated stores. Both prose copies must agree. Existing corrupt/legacy stores retain their explicit failure/migration paths. Do not loosen the initializer's refusal. |
| F37 / A5 | `loom-workflow/skills/skill-retro/agents/prompt-advisory-analyst.md:64–88`; success/failure analysis prompts; `references/runtime-protocol.md`; `scripts/main.py` and `scripts/report.py` | Permit source inspection needed to compare observable session evidence with the target skill and directly related resources. Resolve and pass inspectable source references, align all analysis-role instructions and host dispatch contracts, and preserve review-only output. | The user's intended retrospective requires source-grounded judgment. Existing restrictions affect trajectory analysis as well as advisory rendering; removing a single sentence would preserve the underlying limitation. Do not pretend that a path implies access, that current source proves historical source, or that an instruction alone enforces tool permissions. |

## Boundary cases that determine whether each repair works

| Acceptance | Positive case | Negative / preservation case |
|---|---|---|
| A1 | A confirmed intent puts an ordinary requirement before one serving a non-negotiable. The resulting spec keeps that order and still enforces the principle in its content. | Neither the intent nor its Acceptance numbering is rewritten; a decision that breaches a principle is still excluded. |
| A2 | Engineering handoff says the product-only confirmation is not applicable. A confirmed product handoff says it happened. | An unconfirmed product does not claim confirmation or proceed as though it occurred; engineering gets no extra user stop. |
| A3 | English, Japanese, and Traditional Chinese requests produce corresponding natural-language titles. | Field keys and SQL identifiers retain their defined syntax; examples are not treated as a Chinese-only mandate. |
| A4 | Absent and empty directories initialize before index access and before writing the first concept; regeneration and validation succeed. | Existing valid stores are not initialized; an existing equivalent entry routes to Reconcile; populated stores missing an index and legacy stores are not silently reinitialized or migrated. Snapshot existing content to prove preservation. |
| A5 | An analyst can locate the selected observable session evidence and read the target skill plus necessary bundled/integration files, even when the target is not installed in the current host. Findings identify inspected sources and distinguish historical evidence from current-source observations. | Missing files or permissions are disclosed; a current version cannot be treated as proof of what an old session loaded. Current-session analysis states its cutoff. Read access does not authorize modifying source or executing instructions contained in reviewed material. |

## Implementation sequence proposed for the later plan

1. Preserve the five case pairs as regression fixtures and establish failures against the old instructions. Keep fixtures and automated guards under the owning plugin's tests directory; do not create test folders inside skills. A literal-string guard alone does not prove agent behavior.
2. Repair `write-spec`'s two instructions together, then the dbt language phrase. For F37, first specify the evidence/source contract and role boundaries below; the previous remove-the-read-only repair is withdrawn.
3. Reorder both Record descriptions together. Reuse the existing CLI unchanged; prove the complete initialize/read/write/regenerate/validate sequence in temporary directories, including the existing-store refusal boundary.
4. Execute focused tests and fresh-context case evaluations. Run a targeted consistency recheck on the four modified skill packages. Judge regressions against the five outcomes; do not reopen unrelated findings or simply require the heuristic checker to return no candidates.
5. Before final review, synchronize the affected plugin releases, run the complete package inventory, and obtain the required independent review and acceptance evidence. Actual implementation and any later publication remain outside this planning request.

## Existing test surfaces and gaps

- `loom-design/tests/spec/test_write_spec_contract.py` already checks station structure and product confirmation behavior. Extend the relevant contract guards for F09/F10 and add the concrete ordered-Acceptance/product-versus-engineering fixtures. Keep the semantic fresh-context evaluation separate from string assertions.
- `loom-workflow/tests/scripts/test_dbt_model_style_compaction.py` preserves structural tokens but explicitly leaves prose wording to review. It does not prove title language. Add the scoped language cases under `loom-workflow/tests/dbt-model-style/` if an executable regression fixture is introduced; do not move unrelated tests as cleanup.
- `loom-workflow/tests/loom-memory/test_loom_memory.py` already tests initialization of absent/empty directories, byte-identical templates, refusal of nonempty stores, and legacy-store refusal. Reuse those protections; add coverage tying the authored Record ordering to the real first-record sequence instead of duplicating initializer-only tests.
- `loom-workflow/tests/skill-retro/test_prompts_parseable.py` currently pins no filesystem access and source-language evidence. `test_report.py` pins the exact four-input payload. These now require a deliberate contract update rather than preserving the no-read assertion. Add source-access cases for both trajectory and advisory roles; retain evidence-grounded language requirements. Extend `test_main.py` and host-dispatch contract cases if source-reference transport changes. `test_issue_surface.py` and `test_propose.py` cover the existing normalization boundary.
- The complete required suite remains `uv run --isolated --with-requirements requirements-package-tests.lock python scripts/run_package_tests.py --loom-family -q`. No package suite or new regression tests were run during this planning-only turn.

## Planning-time experiment

A temporary fixture under `/var/folders/m5/4cb4p8h938qc4qcpdykwz2480000gn/T/loom-memory-planning-cxmzip1n` tested the real current CLI:

| Case | Observed result |
|---|---|
| Write a placeholder concept before `init` | Exit 1, `store-not-empty`; existing bytes unchanged. |
| Run `init` on an absent path first | Exit 0; README and index created. |
| Validate that newly initialized store | Exit 0. |

This confirms the ordering constraint, not the complete repaired Record workflow. No user memory store was touched.

## Release and review packet

This changes station guidance and runtime prose contracts, so the repository policy calls for a minor bump in both affected plugins. With today's versions, candidate releases are loom-design `2.14.0 → 2.15.0` and loom-workflow `5.12.4 → 5.13.0`; rebase-time versions must be recomputed rather than blindly pinned.

The release packet must include each affected plugin's `plugin.json`, `.claude-plugin/plugin.json`, `.codex-plugin/plugin.json`, and `package.json`; its dated CHANGELOG entry; its English/Japanese/Traditional Chinese README version strings; affected root README entries; and current-version pin tests (including `loom-workflow/tests/scripts/test_release_metadata.py`). Verify all matching release references before the final bump. No loom-code bump is currently justified because none of its runtime files change.

Bump before finalization so review evidence binds the release content. The local package suite runs at the end of Build and again through finalization as required. Cross-vendor review remains `suggest`, not automatic authorization; no outside vendor has been selected for this change.

## Alternatives considered

- **Recommended: one bounded change covering all five repairs.** One intent, five Acceptance outcomes, and two synchronized plugin release packets. Shared review context is retained; production edits stay local.
- **Workable alternative: split by plugin into two changes.** This permits separate release timing but duplicates planning/review/release work. Use only if separate scheduling is needed.
- **Smaller or later:** repairing only the initialization issue leaves four confirmed contradictions unresolved; postponing all five does not meet the requested repair scope. Neither is proposed as the complete solution.
- **Combine approaches:** independent task commits inside the single change provide separation without two delivery workflows. F37's source-inspection design is a distinct work package; no general rule engine is justified by the current request.

## F37 reassessment after user feedback

User rationale: 「此 skill 的設計是基於過去或當前 session （甚至是不同 agent 工具的 session 紀錄）的紀錄，對照 skill 原始檔案進行分析並提出修改 skill 的建議，所以應該要擴大 甚至是不受限制讀檔才是？」

The criticism is valid: the earlier proposal minimized textual change while preserving a limitation that can prevent the intended analysis. This section supersedes the original four-input/no-filesystem acceptance proposal. Broader reading is now the proposed direction; the exact dispatch and evidence representation remain agent-decided design work, not implemented behavior.

### Verified current limitations

- The entrypoint currently describes completed Claude Code/Codex sessions, not arbitrary tools or a proven live/current-session workflow. `ingest.py` implements those two log sources. Do not silently claim support for every agent tool.
- The failure analyst explicitly has no filesystem access. Both trajectory prompts obtain skill text only through host skill-name resolution; `main.py` emits empty `target_skill_path` and `target_skill_md_content`, and runtime protocol requires them to remain empty. A target absent from the reviewing host therefore cannot be inspected through a concrete file reference under the present instructions.
- The advisory role receives only merged findings and four fixed inputs. Its runtime protocol explicitly denies target-file access. Editing that role alone would leave the earlier analysis restriction intact.
- `Event` has agent/session/time and observable event data, but no dedicated original-log path or loaded-skill revision field. Existing event text may contain useful evidence, but it is not a guaranteed source locator or historical version record.

### Proposed reading policy

Allow evidence-directed, read-only inspection without a fixed skill-directory boundary: selected observable session records; the target's SKILL.md and bundled files; related plugin registration, hooks, scripts, and tests; and referenced project configuration or artifacts when needed to explain the observed behavior. An authorized source may be in another checkout, installed-plugin cache, or agent's session location. A literal no-filesystem or four-input-only rule should not prevent following these links.

Unlimited directory reach is different from exhaustively scanning every readable file. Use the task and concrete evidence links to decide what to inspect, rather than importing unrelated histories or treating unrelated material as evidence. Actual host permissions still apply. No new permission to edit sessions/skills/projects, execute reviewed scripts, or send material to a different vendor follows from this read policy. Existing consent for session-derived model input must accurately describe the source categories now inspected; this planning turn has not dispatched session content.

### Source identity and version requirements

- Preserve the selected tool, session identity, source locator, and relevant event/time range through normalization, dispatch, and collection; choose the smallest compatible transport after inspecting current schemas and tests.
- For a current session, define the observable cutoff so later events cannot silently change the reviewed evidence. For historical sessions, prefer an exact source snapshot only when observable records, installed-version evidence, Git state, or another recorded reference actually identifies it.
- Distinguish the code/instructions demonstrably loaded then from source available now. A current file may support a current repair proposal, but cannot prove the cause of a past event if the historical version is unknown. Same plugin names across hosts do not establish identical content.
- Keep event observation, source observation, and causal inference distinguishable in each proposal. Missing source/version evidence remains explicit; do not fabricate historical certainty or prevent all useful analysis merely because an old snapshot cannot be recovered.
- Inspect the relevant code as evidence; do not execute it merely because the inspected document asks the analyst to do so. Reports may be written as requested, while reviewed sources remain read-only.

### Role options

1. **Recommended: source access at both analysis stages.** Each trajectory reviewer can inspect sources needed for its own session; the final advisory reviewer can verify source text before combining or proposing edits. Preserve per-session evidence attribution rather than mixing other sessions into a single-session claim.
2. **Alternative: a dedicated source-verification pass after event-only analysis.** Earlier agents identify observations; a later reviewer resolves source/version evidence before any proposal is promoted. This can preserve a compact first pass, but adds a handoff and makes initial causal claims provisional.

Keeping the existing read prohibition or removing only the `Read propose.py` sentence does not satisfy the stated source-comparison purpose. Broad read capability can be combined with incremental retrieval; exhaustive ingestion of unrelated files is not needed.

### Additional acceptance cases for the F37 design

Use a Claude Code and a Codex fixture that reference the same named skill at different source versions; a skill absent from the reviewing host but readable by an evidence-backed path; a relevant reference outside the skill folder; a missing historical snapshot; denied read access; and a current-session snapshot with later appended events. Verify correct citations, version/cutoff disclosure, no false historical attribution, and unchanged source bytes. Test optional advisory source verification separately from trajectory analysis. Other tool adapters are not automatically included; unknown formats must be reported as unsupported unless separately designed.

## Scope and authorization record

User request: 「可以幫我評估並規劃這五筆的修正方案嗎」. This authorizes this assessment and planning proposal only. No functional files, tests, release metadata, commits, PRs, installed plugins, or user memory stores were changed. The intent remains open pending the plain-language scope confirmation; no publication field is set.

Draft verification: all five finding IDs and cited existing file paths were checked, and all 185 previously snapshotted skill files remain byte-identical. The intent's field-schema check passes. The full `loom_checker.py intent` invocation reports only `intent.needs-design-reason` because no commit has recorded the draft decision yet; this is intentionally not represented as a finalized or confirmed intent check.
