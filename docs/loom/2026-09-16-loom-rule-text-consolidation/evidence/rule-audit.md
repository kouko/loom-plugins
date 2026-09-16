# Loom rule-text baseline audit

Repo: loom-plugins, main @ dec4e927, audited 2026-09-16. Read-only; no repo file modified.
Scope: 96 `*.md` under loom-code/{skills,agents,references}, loom-design/skills, loom-workflow/skills (CHANGELOG/README excluded) = 105,815 words (loom-code 22,670; loom-design 15,011; loom-workflow 68,134). docs/loom/README.md was checked as well, because the brief asks about it.

## Conclusions

- **Contradictions / stale references: 19 findings.** 7 affect how the flow runs: C2 (docs/loom/README sequence), C5 (dead attack catalogue), C6 (spec review sent to a station that cannot run it), C7 (`questions[]` nobody reads), C11 (Ship folding nits), C13 (implementer "mandatory" missing the skip exception), C14 (write-spec's "cannot read loom-code" premise). The rest are wording drift.
- **Three decisions must come before editing** because each one decides the scope of later waves: who runs the pre-build spec review (C6); restore or delete the attack catalogue (C5); whether loom-design may read loom-code files through the `<loom-code>` path it already resolves (C14). C14 alone decides about 1,700 words of wave 2.
- **Duplication: 11 duplicated blocks.** The largest: the station summary table (304 words × 5 byte-identical copies, enforced by two tests); intake/confirmation text copied between capture-intent and write-plan (about 1,000 words per side); the adversary procedure in adversary.md vs adversarial.md (570 / 413 words).
- **Emphasis: less of a problem in core Loom than assumed.** loom-code has **0** all-caps MUST/NEVER/CRITICAL/ALWAYS. loom-design has 13, all in design-md-schema.md. 64 of the 77 all-caps words are in loom-workflow (dbt-model-style alone has 34). Lowercase must/never/always: 562 in total, 234 in core. Core emphasis is mostly **bold** (43–49 bold lines per large station) plus lowercase "never".
- **Pins are everywhere.** 89 of the 96 rule files contain text matched by test literals; all 7 unpinned files are in loom-workflow. 131 of 291 test/script files hold literals found in rule text, about 2,767 literal matches in total (a heuristic upper bound). 19 probe programs under docs/loom/*/evidence/probes/ anchor on core rule text, about 150 matches. Practically nothing in core is "safe to change, no pins".
- **Size:** only write-plan/SKILL.md is past the soft cap: 4,182 body words, about 5,576 tokens estimated as words × 1.33 or about 7,101 estimated as chars/4. That is over the 3,750-word soft cap and near or over the 6,000-token hard cap depending on the proxy. capture-intent (3,116), write-spec (3,091) and dbt-model-style (3,160) are under the soft cap by words but over it by chars/4.
- **Words removable with no behaviour change (estimate):** wave 1 about 150 in rule text (plus about 600 in docs/loom/README); wave 2 about 2,300 if loom-design copies are kept, about 4,600 if C14 allows pointers across plugins; wave 3 about 0–300 net (reasons add words back). Rough total: **2,500–5,000 words, 2.4–4.7% of the scope, or about 7–13% of core loom-code + loom-design.**
- **Mechanical gates are green today.** `check_mechanisms.py`: all clear, net 136 mechanisms, 17 prose gates. `check_contract_citations.py`: OK, 4 known debt files. `check-skill-crossrefs.py`: OK. It still misses the dead attack-catalogue links because it does not scan `references/*.md` or paths written in backticks. That is a checker gap worth closing in wave 1.

## 1. Contradictions and stale references

| # | Where | Problem | Evidence against | Pins / notes |
|---|---|---|---|---|
| C1 | docs/loom/README.md:14 | Links `evidence/attack-catalogue.md`; docs/loom/evidence/ holds only mechanisms.yaml and outcome-map-v3/ | `ls docs/loom/evidence` | README only (see C2 pins) |
| C2 | docs/loom/README.md:48-161 | The sequence contradicts the current flow. Step 1 build→adv writes probes before implementation. Steps 4a and 8 have review→adv. Step 7 has review→impl. :146/:157 "完整車道／小車道" (lanes). :154 `reviewed_sha→HEAD^`. :153 forbids amend. | build/SKILL.md:86-91 (adversary after tasks, end of Build); adversary.md:3 "after all tasks land"; closing-review/SKILL.md:177 "dispatches no adversary"; :196-198 fixes return to Build; lanes removed in #20; adversary.md:113 amend allowed | test_readme_review_order.py:108-140 (a unit must place the adversary at end of Build; no unit may tie review to the adversary). test_probes_coldread_readme_role_section_has_three_way_paragraph.py:4-15 (keep heading + the 三方 paragraph). The rewrite must keep both. |
| C3 | docs/loom/README.md:13 | Change folder lists `review.json` (verdicts, dispatch record, probes) | closing-review/SKILL.md:12-13 produces attestation.json; maintain/SKILL.md:23; no `review.json` anywhere in loom-code/scripts or contract | — |
| C4 | docs/loom/README.md:15 | Memory is written by "build station's memory step (before the branch-end checkpoint)" | build/SKILL.md has no memory step; closing-review/SKILL.md:229-240 places the lesson at convergence | — |
| C5 | loom-code/agents/adversary.md:59; closing-review/references/adversarial.md:83 | Point to `closing-review/references/attack-catalogue.md`, which does not exist. adversary.md:3 (description), :110-111 and adversarial.md:94-95 ("turns the catalogue into an eval") depend on it. | `ls` of references/; plan 2026-09-15-mechanical-checks-before-review/plan.md:80 lists it as known out-of-scope | Not pinned by any test. check_contract_citations.py:134-137 exempts the filename. check-skill-crossrefs.py misses it (scope gap). **Decision: restore the catalogue or rewrite the skill/gate recipe inline.** |
| C6 | loom-design/skills/write-spec/SKILL.md:320-326; loom-code/skills/write-plan/SKILL.md:356-360 | Hand a pre-build spec to `loom-code:closing-review` "with scope `spec`" for one spec+adversarial reviewer | closing-review/SKILL.md:4 "Use after Build completes"; §1 :17 reads the plan (none exists yet); §5 :270-282 finalize-review runs the package suite and writes the attestation; no spec scope anywhere; using-loom-code/SKILL.md:16 routes only after Build | Pinned in write-spec (40 literals) and write-plan. **Decision: give closing-review a spec mode, or let write-spec/write-plan dispatch `loom-code:reviewer` directly.** |
| C7 | write-plan/SKILL.md:442-446 | "closing-review station reads this section … copies it into `questions[]`" | No `questions[]` in closing-review/SKILL.md or any loom_checker code; only intake.py:403 checks Open questions | Also the reason the capture-intent:272-279 / write-spec:309-315 "question list" hand-off exists; dead end |
| C8 | write-plan/SKILL.md:262 | "The §11 measurement of how often loom interrupts…" | Refers to concept-model §11, a design record no runtime reader can resolve (AGENTS.md contract-citation spirit) | — |
| C9 | write-plan/SKILL.md:360 "existing passing review record"; agents/blind-runner.md:49 "review record's findings" | Refer to the retired review ledger | maintain/SKILL.md:23; ship/SKILL.md:102-103 "retired … ledgers … not valid inputs" | — |
| C10 | agents/implementer.md:3 "one commit carrying the task trailer"; adversarial.md:111-112 "task-accounting trailer" | Trailer mechanism no longer exists | No `trailer` in loom-code/scripts or contract; build/SKILL.md never mentions one | — |
| C11 | agents/reviewer.md:106-108 | "`ship` folds [nits] into one commit before push and you confirm each fix" | ship/SKILL.md has no nit step; ship:105-106 publication-only edits never return to review; lenses.md:26-27 "Ship *may* batch" | test_reviewer_mechanical_evidence.py pins reviewer.md (12) |
| C12 | agents/blind-runner.md:72-73 | "Green tests are the package-tests probe's job" | Package suite runs in Build §3 (build:92-96) and finalize-review (closing-review:276) | — |
| C13 | write-plan/SKILL.md:409-410 | "Implementer dispatch is mandatory for every implementation task" (no exception) | build/SKILL.md:61-68 "Unless `selection show` lists `implementer` as skipped" | Pinned (test_simplified_station_text.py) |
| C14 | write-spec/SKILL.md:221-223 "one-way-door.md … which you cannot read from here" | The same skill resolves `<loom-code>` (:61-79) and reads its `contract/templates/spec-minimal.md` (:126-127); product-principles:68 reads `<loom-code>/contract/templates/…` | The premise behind three hand copies (test_one_way_door_copies.py:3-9) and behind D1/D2/D6/D7/D8 | **Decision: allow reading loom-code references via `<loom-code>`?** |
| C15 | capture-intent/SKILL.md:39-40 "It is the whole list; nothing else in the change stops for them" | Other stops exist | ship:22-23 legacy publication decision; closing-review:210-212 asks when requirements change; expert-mode typed confirmation; write-plan:74-77 names the Codex authorisation stop (capture-intent:56 hints at it) | Low |
| C16 | closing-review/references/lenses.md:3 "six lenses" | reviewer.md:33 lists seven lens values | — | Low |
| C17 | closing-review/SKILL.md:245; loom-workflow/skills/loom-memory/SKILL.md:97 | "an unfinished item in an intent or a backlog entry" | docs/loom/README.md:37: backlog is frozen; recurring items become intents | Low |
| C18 | closing-review/references/adversarial.md (location) | Build's procedure lives under closing-review; build/SKILL.md never links it; closing-review:177 says review has no adversary | adversarial.md:4 "It runs at the end of Build"; only adversary.md:30 points to it | Moving it changes pinned paths (test_build_mechanical_checks.py: 71 literals) |
| C19 | loom-workflow: git-memory/protocols/recall.md:77 (`loom-code:brainstorming`, `writing-plans`); git-memory/protocols/compose-commit.md:153 (`loom-code:finishing-a-development-branch`); distill-sessions/agents/prompt-failure-analysis.md:23,152, prompt-success-analysis.md:179 (`loom-code:dispatching-parallel-agents`, 8 refs total); loom-visualization/references/fidelity-check.md:102 (provenance) | Skills that no longer exist | `ls loom-code/skills` = build, closing-review, expert-mode, maintain, ship, using-loom-code, write-plan | recall.md is unpinned; compose-commit pinned (19) |

## 2. Duplication

Word counts are `wc -w` over the cited ranges. A 12-word shingle scan confirmed the overlaps.

| # | Block | Copies (file:lines, words) | Single source | Removable (est.) | Pinned by |
|---|---|---|---|---|---|
| D1 | Station summary table | capture-intent:25-35; write-plan:60-70; write-spec:32-42; design-system:19-29; product-principles:27-37 (304 w each, byte-identical) | write-plan (loom-code owns the contract), or the contract manifest | 608 (drop from the two tools, low risk); up to 1,216 with C14 | **Enforces duplication:** test_capture_intent_contract.py:199-200, test_design_system_skill.py:71-75 (byte equality) |
| D2 | Step 0 "locate loom-code + contract --require 2.1" | write-spec:61-87 (232); design-system:31-56 (215); product-principles:39-64 (215); capture-intent:58-77 (162) | One loom-design file, e.g. capture-intent/references/, linked by sibling path (same pattern as build → ../expert-mode) | ~450 | scripts/test_loom_plugin_install_layout.py:626 ("two levels above this SKILL.md" in each skill's row) |
| D3 | "At entry, run `selection show`… may suggest at most once per change…" | build:18-26 (93); closing-review:22-30 (97); ship:26-35 (92); write-plan:44-52 (92); partial in using-loom-code:21-25 | expert-mode/SKILL.md; each station keeps one sentence plus the step list | ~250 | **Enforces duplication:** test_expert_mode_skill.py:269-278 (the phrase must occur exactly once per station); test_selection_capture.py |
| D4 | Dispatch-profile invocation paragraph | build:30-53 (196); closing-review:34-59 (216) | loom-code/references/dispatch-profile.md | ~330 | test_dispatch_profile_contract.py (18 CR / 5 build / 37 ref); test_dispatch_profile_resolver.py:482 |
| D5 | Adversary reuse / update / mutation / discard-command procedure, attack classes, recording | agents/adversary.md:37-88 (570) + :97-115; closing-review/references/adversarial.md:8-44 (413) + :53-69 + :97-117 | adversarial.md holds the procedure (adversary.md:30 already says "read it first"); adversary.md keeps role, inputs, return format | ~400 | test_build_mechanical_checks.py (87 adversary / 71 adversarial literals); probe 2026-09-15-adversary-probe-maintenance/…/test_probe_maintenance_abuse.py (7+7) |
| D6 | Second-vendor availability probe + `ask` + fixed CLI | loom-design capture-intent/references/second-vendor.md:3-56 (515); loom-code write-plan/references/second-vendor-ask-and-docs-lint.md:6-30, 79-116 (577); ~270 words verbatim | loom-code reference | ~250 (needs C14) | test_write_plan_station_text.py (31 / 12), test_capture_intent_contract.py (15 / 19), test_agy_tool_mapping.py |
| D7 | Intake/confirmation text copied for the "loom-design absent" path: restatement + publication (cap:205-220, 132 / wp:196-210, 116); on-yes (87 / 79); needs-design rule (cap:140-151, 100 / wp:294-309, 128); altitude pass (cap:98-118, 168 / wp:135-158, 232); standing docs (cap:174-198, 182 / wp:166-187, 161); question list (cap:266-279, 145 / wp:240-264, 209 / ws:309-315, 83); carried details (cap:281-291, 142 / wp:266-275, 123 / ws:176-184, 123); Mermaid-not-in-chat (cap:120-125 / wp:161-164 / wp:362-365 / ws:210-214) | ≈1,030 (cap) / 1,096 (wp) / ~290 (ws) | loom-code (must work without loom-design): one loom-code reference both stations read | ~800–1,000 (high risk; needs C14) | test_capture_intent_contract.py (95 cap / 49 wp), test_write_plan_shape_text.py (67 / 28), test_write_spec_contract.py (40 / 18); probes readable-flow-details/test_probe_carried_details_routing.py, test_probe_prose_pin_mutants.py |
| D8 | One-way-door classes + four gates | write-spec:219-260 (421); capture-intent:222-242 (212); source loom-code/skills/write-plan/references/one-way-door.md | one-way-door.md | ~550 (needs C14) | **Enforces duplication:** test_one_way_door_copies.py |
| D9 | Severity → verdict rules; "reviewers never run suite/programs" | agents/reviewer.md:93-131 (362), :70-78; lenses.md:9-39 (294) | lenses.md (reviewer.md:41 already defers to it for severity) | ~250 | test_reviewer_mechanical_evidence.py (12 / 8); probe mechanical-checks-before-review/test_reviewer_runs_probes.py |
| D10 | "Use the host's edit tool … never sed -i" trap-guard | adversary:126-129, reviewer:191-194, implementer:70-73, blind-runner:77-80 (38 w each) | keep (each agent contract must stand alone) | 0 | — |
| D11 | "Almost nothing qualifies" durable-lesson paragraph | closing-review:242-248 (76); loom-memory/SKILL.md:94-100 (87) | keep both (across plugins); fix C17 only | 0–70 | loom-memory pinned (32) |

Duplication total (estimate): about 2,300 words with D1-tools, D2, D3, D4, D5, D9; about 4,600 words adding D1-rest, D6, D7, D8 once C14 allows it.

## 3. Emphasis

Counts are whole-word matches. Caps = MUST/NEVER/CRITICAL/ALWAYS; low = must/never/always.

| Group | Caps (M/N/C/A) | Low (must/never/always) |
|---|---|---|
| loom-code (22,670 w) | 0 (0/0/0/0) | 155 (59/89/7) |
| loom-design (15,011 w) | 13 (6/7/0/0), all in design-system/references/design-md-schema.md | 79 (21/56/2) |
| loom-workflow (68,134 w) | 64 (56/8/0/0) | 328 (120/182/26) |
| **Total** | **77 (62/15/0/0)** | **562 (200/327/35)** |

Top files (caps + low): dbt-model-style/SKILL.md 47 (34 MUST); independent-advisor/SKILL.md 30; write-plan/SKILL.md 20; page-mode.md 19; handoff-schema.md 19; write-spec/SKILL.md 18; capture-intent/SKILL.md 17; closing-review/SKILL.md 17; dispatch-profile.md 16 (13 must; 12.8 per 1k words); privacy-judge-spec.md 15 (16.4 per 1k words, the highest density). Core stations also carry heavy **bold**: lines containing `**` number write-plan 49, capture-intent 44, write-spec 43.

10 densest paragraphs (≥3 emphatic tokens; ranked by count, then density):

| # | file:lines | Hits | Keep firm? | Rewrite note |
|---|---|---|---|---|
| E1 | loom-workflow/skills/dbt-model-style/SKILL.md:88-93 | 8 (6 MUST), 11 bold | **Partly hard:** "don't rename pushed model/column names" (downstream BI breaks) | Other bullets are style: turn MUST into plain rules; reasons already exist |
| E2 | dbt-model-style/SKILL.md:55-59 | 7 (5 MUST) | No | CTE naming conventions; reasons present, caps add nothing |
| E3 | loom-design/skills/design-system/references/design-md-schema.md:325-345 | 6 NEVER | No (taste), except "token must not contradict PRINCIPLES" | "Avoid X because Y"; the reasons are already written |
| E4 | loom-design/skills/write-spec/references/spec-forms.md:12-24 | 5 never | **Hard** (REQ id stability is checked by the machine) | Keep the rule; cut the repeated "never" |
| E5 | loom-workflow/skills/distill-sessions/agents/prompt-success-analysis.md:141-163 | 5 (2 NEVER) | **Hard:** no ground-truth leakage; no private-memory citations | Keep firm; shorten |
| E6 | dbt-model-style/SKILL.md:163-168 | 4 MUST | Firm (a validator reads the fields) | Use SHOULD/MAY vocabulary consistently; drop the caps |
| E7 | loom-design/skills/product-principles/SKILL.md:131-140 | 4 | No: it describes checker behaviour, not a prohibition | Plain description |
| E8 | loom-design/skills/write-spec/SKILL.md:137-151 | 4 | Partly: "never shown to the user" repeats the gate at :197-202 (hard) | Delete the repeat; keep the gate |
| E9 | loom-code/agents/implementer.md:27-61 | 4, 10 bold | **Hard:** "failing test first", "never delete/skip/weaken a test" (:30-33), "never git add -A" | Keep those; the rest of the list can lose the bold |
| E10 | loom-workflow/skills/independent-advisor/SKILL.md:151-173 | 4, **25 bold** | **Hard:** no completeness claims; delivery refused without coverage_disclaimer | Bold density is the problem; keep the hard two |

Hard prohibitions in core that must stay firm (do not soften in wave 3): write-plan:130-134 (gate: no plan without a confirmed intent); write-plan:491-499 (gate: conservative default); capture-intent:294, :318-320 (never confirm on the user's behalf); write-spec:197-202 (gate), :305-307 (never write confirmed-behavior for the user); ship:95-98 (secret findings cannot be bypassed); ship:178-180 (never `gh pr merge`); closing-review:128-131 (do not move Claude credentials), :200 (never Round 4); adversary.md:85-88 and adversarial.md:41-44 (no discard commands); reviewer.md:8-11 (do not modify). dispatch-profile.md:110-117 uses "must" for deterministic routing that the resolver also codes; it is contract wording, not emphasis.

**Wave-3 pin trap:** loom-code/scripts/prose_pin.py:23-26 makes every prose-pin test reject any sentence containing not/never/no/cannot/without/neither/nor. Rewriting a pinned affirmative sentence into a negated form fails its test. Rewriting "never X" into "X is avoided because…" is fine only when the new sentence is not itself pinned.

## 4. Size and constraints

### SKILL.md budget (AGENTS.md:39: hard ~6,000 tokens ≈ 4,500 words; soft ~5,000 tokens ≈ 3,750 words)

| SKILL.md | Body words | Tokens (w × 1.33) | Tokens (chars/4) | Status |
|---|---|---|---|---|
| loom-code/skills/write-plan | 4,182 | 5,576 | 7,101 | **Over soft by words; over hard by chars/4** |
| loom-workflow/skills/dbt-model-style | 3,160 | 4,213 | 5,277 | Under soft by words; over by chars/4 |
| loom-design/skills/capture-intent | 3,116 | 4,154 | 5,218 | Same |
| loom-design/skills/write-spec | 3,091 | 4,121 | 4,960 | Near soft |
| loom-workflow/skills/distill-sessions | 2,483 | 3,310 | 4,589 | OK |
| loom-code/skills/closing-review | 2,183 | 2,910 | 3,815 | OK |

Non-SKILL references with no cap but large: handoff/references/handoff-schema.md 5,021 words; recap-state/references/seven-block-schema.md 3,678; loom-visualization page-mode.md 3,130 and mermaid-cot-spec.md 3,116. D1 + D3 + D7 would take write-plan down about 700–1,400 words, back under the soft cap.

### Constraints and how each limits editing

| Constraint | Current state | Limit on the consolidation |
|---|---|---|
| Prose pins (tests) | 131 / 291 test+script files; ~2,767 literal matches; 89 / 96 rule files pinned. Heaviest: write-plan 260 literals / 39 files; capture-intent 211 / 35; closing-review 175 / 28; independent-advisor 144 / 6; build 139 / 24; write-spec 112 / 32; ship 99 / 15; adversary.md 91 / 5; map-format.md 86 / 21; adversarial.md 81 / 5. Biggest test files: test_build_mechanical_checks.py (247), test_capture_intent_contract.py (204), test_simplified_station_text.py (204), test_write_plan_shape_text.py (127), test_review_convergence_contract.py (99) | Every core edit is "pinned: tests change with it". Three tests **require** duplication (D1, D3, D8), so merging means rewriting them, not just updating strings. |
| Safe (no pins) | Only 7 files, all loom-workflow: critique/references/mindset-{data-over-abstractions, design-is-taking-apart, expensive-to-add-later, simplicity-vs-easy}.md; dbt-model-style/references/dotstar-passthrough.md; git-memory/protocols/recall.md; loom-visualization/NOTICE.md. Low-pin core files: using-loom-design (1), engineering-baseline (1), one-way-door (2), maintain (3), blind-runner (3) | recall.md:77 (C19) is the only stale fix with no pin at all |
| Gate markers | 17 `<!-- gate: -->` markers: write-plan ×3, capture-intent ×2, write-spec ×2, closing-review ×2, lenses ×1, dispatch-profile ×1, codex-first-contact ×1, product-principles ×1, design-system ×1, goal-create ×1, loom-visualization ×2. lenses.md:110 only mentions the syntax. | Moving or merging gated text must move the marker too; check_mechanisms.py diffs the prose-gate count against mechanisms.yaml (17 registered). Removing one needs a mechanisms.yaml edit, and a net-count change needs a `budget-exception` CHANGELOG line (mechanisms.yaml header). |
| Mechanism inventory | `check_mechanisms.py`: skill 22, checker-rule 25, hook 10 (9 registered + 1 host-hygiene), contract 63, prose-gate 17; net 136; all clear | Merging skills or splitting gates changes the counts; pure prose dedup does not |
| Probe programs | 19 files under docs/loom/2026-09-*/evidence/probes/ match ~150 core literals. Heaviest: closing-review-station-name/test_abuse_station_name.py (33, 13 files); adversary-probe-maintenance/test_probe_maintenance_abuse.py (25); readable-flow-details/test_probe_carried_details_routing.py (17); mechanical-checks-before-review/test_selection_skip_gates.py (15) | This is change-scoped evidence and not part of the package suite, but a re-run after consolidation will go red wherever anchors move. Either accept that and record it, or re-run before and after. Graduated copies inside loom-code/scripts (test_probes_*.py) **are** in the suite. |
| Contract citations | OK; DEBT_LIST 4 files, shrink-only | New pointers must not cite `docs/loom/<change>` records (C8 is the same smell in prose form). A shared reference in `loom-code/references/` is allowed. |
| Skill folder structure | validate-skill-folder-structure.sh: one level of subfolders | A shared loom-design reference must sit at `<skill>/references/x.md`, not in a nested folder |
| docs/loom/README tests | test_readme_review_order.py:108-140; test_probes_coldread_readme_role_section_has_three_way_paragraph.py | The C2 rewrite must keep an "adversary at end of Build" unit, no review↔adversary unit, the role-trigger heading, and the 三方 paragraph |
| Crossref checker gap | check-skill-crossrefs.py scans skills/*/SKILL.md and agents/*.md links only | Neither C5 link is caught; extending it to references/*.md and backtick paths is a small wave-1 add |

## Recommended scope (waves by risk)

Wave 0 (decisions, no edits): C5 restore or delete the catalogue; C6 spec-review owner; C14 whether loom-design may read loom-code references. Record them in the intent's Constraints.

Wave 1 (stale references and contradictions; low risk, few pins): C1–C4 + C2 README rewrite (keep the pinned units); C5 per decision; C7–C13, C16, C17, C19; C15 wording; extend check-skill-crossrefs.py to references/ and backtick paths. About 150 rule words plus about 600 README words removed. Pins touched: test_simplified_station_text (C13), test_reviewer_mechanical_evidence (C11), README tests; C6 per decision (write-spec/write-plan pins).

Wave 2a (duplication inside one plugin; medium risk): D9 → lenses.md; D4 → dispatch-profile.md; D3 → expert-mode (rewrite test_expert_mode_skill:269-278); D5 → adversarial.md (rewrite about 150 literals in test_build_mechanical_checks); D1 drop from design-system/product-principles (rewrite the two byte-equality tests); D2 → one loom-design reference. About 2,300 words.

Wave 2b (duplication across plugins; only if C14 = yes; high risk): D6, D7, D8, D1 rest. About 2,300 more words; rewrite test_one_way_door_copies, test_capture_intent_contract, test_write_plan_shape_text, test_write_spec_contract; re-run readable-flow-details probes.

Wave 3 (emphasis; low word yield): core bold normalisation in write-plan, capture-intent, write-spec; loom-workflow caps in dbt-model-style (34), design-md-schema (13), distill-sessions agents (14). Keep the hard-prohibition list above. Watch prose_pin negation rules.

Verification per wave: `check_mechanisms.py` (17 gates unchanged unless intended), `check_contract_citations.py`, `check-skill-crossrefs.py`, the package suite, re-running the 19 anchored probes, and a cold read of each changed station on one real task. The background note (§7) says trimming without running a real task afterwards is a gamble.

## Method and caveats

- Pin counts: Python AST string literals of ≥12 characters containing a space, matched as exact substrings (whitespace-normalised) against each rule file. This misses regex and fragment pins and path-only asserts; a phrase shared by several files is counted for each of them. Treat the numbers as indicative, not exact.
- Duplication: 12-word shingles over loom-code and loom-design; block word counts come from `wc -w` on the cited line ranges.
- Token figures are proxies (words × 1.33 and chars/4); the repo's own token counter was not found.
- Emphasis counts ignore SHOULD, "do not" and bold; the bold line counts are listed separately.
- loom-workflow was covered by counts, crossref and stale-name scans, and the dense-paragraph ranking only; its prose was not read line by line for contradictions beyond C17 and C19.
