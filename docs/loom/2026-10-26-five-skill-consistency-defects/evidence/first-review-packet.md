# Independent review request — planned repairs for a skill-package consistency check

You are reviewing a set of planned documentation repairs. The evidence lives in this repository (your working root). Read the cited files to check each claim yourself; do not trust this packet's excerpts.

## Background

A consistency check ran over 26 Loom skill packages, reading each package's Markdown for places where one instruction contradicts another. 18 distinct findings were independently confirmed (21 verdict entries; three loom-visualization entries are duplicates). Each finding below names both sides with file:line in the package root shown, then the repair planned for it. All repairs are documentation-only; no script behavior changes are planned except where stated.

## Your task

For each numbered finding, return:

1. `verdict` — exactly one of:
   - `necessary-and-correct` — the contradiction is real and the planned repair resolves it without changing intended behavior;
   - `correct-with-smaller-repair` — the contradiction is real, but a smaller or different repair is better (name it);
   - `wrong-direction` — the repair would fix the wording by changing behavior or by weakening the rule (say what breaks);
   - `not-a-real-contradiction` — the two sides are compatible as written (say why the verifier was wrong).
2. `why` — 1-3 sentences, citing file:line.
3. `new-conflict` — does the repair create a new contradiction with unmodified text elsewhere? If yes, name it file:line.
4. `priority` — `P1` (blocks an agent following the skill), `P2` (ambiguity, agent may guess wrong), `P3` (cosmetic).

Then add a short section `Missed findings` for any contradiction you find in the cited files that this list misses, and a short section `Cross-fix interactions` for fixes that must land together or that touch the same contract.

Report in English. Be adversarial: the value of this review is finding where the repair plan is wrong, not agreeing with it.

---

## 1. loom-visualization — template 08 draws node edges across subgraphs

Package root: `loom-workflow/skills/loom-visualization`

- Side A: `references/mermaid-cot-spec.md:179-185` — "**No node edge may leave its subgraph. Rows and columns are joined SUBGRAPH to SUBGRAPH.** … mermaid drops a subgraph's `direction` the moment one of its nodes has an edge to anything outside it … never `C -->|…| D` across rows, and never `C -->|…| r2`."
- Side B: `templates/08-system-architecture.md:75-79` — `UI --> API`, `CLI --> API`, `API --> PG`, `API --> R`, `W --> PG`, where UI/CLI are in subgraph P, API/W in APP, PG/R in DATA.

Planned repair: rewrite the template 08 Mermaid example so edges join subgraphs (`P --> APP`, `APP --> DATA`, labelled where informative), and move node-level dependency detail into a note or node card. Do not rename the subgraph ids (a separate PLAUSIBLE item, out of scope).

## 2. loom-visualization — template 13 draws node edges across subgraphs

- Side A: `references/mermaid-cot-spec.md:179-185` (same rule).
- Side B: `templates/13-cross-role-workflow.md:56-57` — `A -->|"handoff: 需求說明"| B`, `B -->|"handoff: 流程稿"| C` across subgraphs Product/Design/Engineering.

Planned repair: replace with subgraph-to-subgraph edges `Product -->|"handoff: 需求說明"| Design` and `Design -->|"handoff: 流程稿"| Engineering`.

## 3. loom-visualization — separator count in template 08

- Side A: `references/mermaid-cot-spec.md:204` — separator is the literal `<br/>━━━━━━<br/>` — six U+2501.
- Side B: `templates/08-system-architecture.md:63` — uses 23 `━`.

Planned repair: change the template 08 separator to exactly six. No other file changes (the spec's own examples already use six).

## 4. loom-visualization — page-mode three commands vs fidelity-check two

- Side A: `references/page-mode.md:256-263` — "**Three commands, and the third is not optional**": render, verify `--render --stamp`, render again.
- Side B: `references/fidelity-check.md:56-62` — "run the two commands that carry the verdict onto the page": verify `--render --stamp`, render.

Planned repair: make fidelity-check say its two commands are the last two of page-mode's three-command sequence, so no reader can take it as a complete two-step flow.

## 5. loom-visualization — "read the one template, and no other" vs template citing the spec

- Side A: `SKILL.md:78-82` — "Read the one template file from Step 1, and no other."
- Side B: `templates/04-reasoning-chain.md:62-64` — "Follows the row convention of `references/mermaid-cot-spec.md` …".

Planned repair: in SKILL.md Step 2, permit opening a file the template cites, but only when the client check selects Mermaid (the only path that needs the spec). Keep the one-template default for table and ASCII forms.

## 6. loom-visualization — quantity "markdown table only" vs template's draw form

- Side A: `SKILL.md:110` — "Data model and quantity need only the markdown table."
- Side B: `templates/11-quantity.md:21-22` — "A reply defaults to the table above; draw this when the shape itself is the information, or when the destination does not render markdown."

Planned repair: qualify `SKILL.md:110` — quantity defaults to the markdown table but may be drawn when the shape is the information, per `templates/11-quantity.md`.

## 7. closing-review — pytest probe command form (rule vs examples)

Package root: `loom-code/skills/closing-review`

- Side A: `references/adversarial.md:146-147` — "A probe file that defines test functions or test classes must be recorded as `python -m pytest <artifact>`: `finalize-review` refuses a bare `python3 <artifact>` run of it."
- Side B: `references/adversarial.md:134,136` — examples record `python3 -m pytest <path>`.

Planned repair: reword the rule to the checker's actual acceptance: record a pytest-style file as a `python`/`python3 -m pytest <artifact>` run; a bare `python3 <artifact>` is refused. Evidence: `loom-code/scripts/loom_checker/probes.py` `runs_pytest()` accepts any executable whose name starts with `python`, and `direct_pytest_style_failure()` refuses only a non-pytest run.

## 8. closing-review — same rule vs SKILL.md's finalize-review input example

- Side A: `references/adversarial.md:146-147` (same rule).
- Side B: `SKILL.md:402` — `{"command":"python3 -m pytest <path>","artifact":"<path>"}`.

Planned repair: resolved by the same rewording as finding 7; the `python3 -m pytest` example then matches the rule, and SKILL.md:402 stays unchanged.

## 9. closing-review — a third execution of adversarial programs

- Side A: `references/lenses.md:36-39` — "reviewers never run the complete package suite or the adversarial programs … both run mechanically at the end of Build, and `finalize-review` executes them again and records the result."
- Side B: `SKILL.md:174-179` — before dispatching reviewers, run once at HEAD each adversarial program whose command is not pytest, shell or direct execution, and hand the output paths to reviewers.

Planned repair: add one clause to lenses.md acknowledging the closing-review pre-dispatch run of non-pytest programs as evidence for reviewers, while keeping "reviewers never run them themselves".

## 10. closing-review — absence recovery says ask, bounded episode says do not ask

- Side A: `SKILL.md:109-114` — "Stop and ask when producing an absent item needs a decision point the user has not answered for this change … When the user has answered it, including a general delegation such as 'you decide', proceed and record the choice as user-decided."
- Side B: `SKILL.md:334-338` — "Do not ask the user whether to continue a technical fix or which technical repair to choose … Ask only when resolving the blocker would change requirements, visible behavior, or guarantees."

Planned repair: scope §2's ask to user-decision-shaped questions (requirements, visible behavior, guarantees) and state that §4 governs technical repair choices, which the agent decides itself. No behavior change for the technical case.

## 11. external-review — "one execution call" vs a separate `--list-candidates`

Package root: `loom-code/skills/external-review`

- Side A: `SKILL.md:87-88` — "One execution call runs discovery, preflight, and review consecutively."
- Side B: `SKILL.md:101-106` — "After this consent, list candidates with: … --list-candidates …"; `SKILL.md:126-130` shows a separate execution command without `--list-candidates`.

Planned repair: state that `--list-candidates` is an optional pre-execution listing used to choose a model, and that the execute call performs its own discovery while validating consent and the selected model. Evidence: `loom-code/scripts/external_review.py` `execute()` calls the candidate lister before probe and review; `main()` routes `--list-candidates` to `discover()` only when that flag is present.

## 12. external-review — "the script performs bounded discovery" vs the separate listing

- Side A: `SKILL.md:140-141` — "The script first verifies the consent and explicit selection. It then performs bounded discovery, one short preflight, and one bounded review with the same model and effort."
- Side B: `SKILL.md:101-106` (separate `--list-candidates` invocation).

Planned repair: same rewording as finding 11; line 140 then describes the execute path accurately and the listing is explicitly optional.

## 13. external-review — "checks model and effort" vs the primary consent form

- Side A: `SKILL.md:76-78` — "The script checks required source fields and their binding to the selected executor, review root, disclosures, model, and effort."
- Side B: `SKILL.md:43-59` — the primary record form has `family` and `allowed_efforts`, not `model`/`effort` (the exact form appears later at 62-71).

Planned repair: say the script checks the selected model and effort against whichever form the record uses — exact (`model` + `effort`) or bounded (`family` + `allowed_efforts`). Evidence: `external_review.py` `_consent_valid()` returns `exact or bounded`.

## 14. loom-memory — Reconcile trigger scope

Package root: `loom-workflow/skills/loom-memory`

- Side A: `SKILL.md:143-145` — "**Trigger:** a new lesson contradicts or narrows a current entry."
- Side B: `references/operations.md:92-94` — "Reconcile activates when a new lesson contradicts or narrows a current entry found during Recall or Record's search step — never as a separate discovery pass."

Planned repair: narrow SKILL.md's trigger to "found during Recall or Record's search step", matching operations.md.

## 15. ship — five body-rejection criteria vs the publish command's four refusals

Package root: `loom-code/skills/ship`

- Side A: `SKILL.md:142-145` — "Before publication, reject a body with a missing heading, evidence source that was silently ignored, unsupported decision claim, hidden-reasoning claim, or a diagram that is required by the relationships above but absent."
- Side B: `SKILL.md:185-189` — "Before pushing, beyond authorization and repository safety, it refuses only a malformed body (naming the heading), a `Verification status:` line that differs from the computed status …, an attestation left uncommitted, and an unidentified change."

Planned repair: name the actor in §2 — those five are the author's pre-publication self-check, so a body failing any of them must never be submitted; §3's "refuses only" describes the publish command's narrower mechanical refusal list and is not a claim that the other defects are publishable.

## 16. skill-retro — prompt frontmatter literal model id vs the dispatch alias

Package root: `loom-workflow/skills/skill-retro`

- Side A: `agents/prompt-failure-analysis.md:3`, `agents/prompt-success-analysis.md:3`, `agents/prompt-advisory-analyst.md:3` — `model: claude-sonnet-4-6`.
- Side B: `references/claude-code-tools.md:50-54` — "Passing the literal model id `"claude-sonnet-4-6"` … fails `Agent()`'s enum validation — always dispatch with the alias, not the literal id."

Planned repair: change the three prompt frontmatter lines to the dispatch alias `model: "sonnet"`, and update `loom-workflow/tests/skill-retro/test_prompts_parseable.py`'s `EXPECTED_MODEL` in the same change. `scripts/main.py`'s `SUBAGENT_MODEL_ID` payload value stays `claude-sonnet-4-6` (it is the recorded standard, not the `Agent()` argument).

## 17. skill-retro — test verbosity flag differs between two copies of one command

- Side A: `SKILL.md:39` — `PYTHONDONTWRITEBYTECODE=1 python -m pytest loom-workflow/tests/skill-retro/ -q`
- Side B: `references/runtime-protocol.md:122-123` — `PYTHONDONTWRITEBYTECODE=1 python -m pytest \` / `  loom-workflow/tests/skill-retro/ -v`

Planned repair: unify on one flag. Proposed: change `SKILL.md:39` to `-v` to match runtime-protocol, or alternatively have SKILL.md reference runtime-protocol instead of restating the command. State which is better.

## 18. write-plan — confirm-intent.md contradicts itself on where product one-way doors are asked

Package root: `loom-code/skills/write-plan`

- Side A: `references/confirm-intent.md:33-35` — "A product change's one-way doors, class (e) actions included, are asked at decision point ② of the station writing its spec — `write-spec`, or this station (step 4) — when a spec will be written."
- Side B: `references/confirm-intent.md:36-37` — "They are asked in this message instead when no spec will be written (step 4 forces none); a spec written later in step 4 does not ask them again at ②."

Planned repair: delete the trailing clause "a spec written later in step 4 does not ask them again at ②" and make the ①/② choice depend solely on whether step 4 will write a spec.

---

## Repository policies the repairs must respect

- Documentation-only edits; no runtime script change except the one test constant named in finding 16.
- Skill package folders are flat: one level of subfolders only.
- A repair must not weaken a rule to make it consistent; where the code is the authority (findings 7, 11-13, 16), the prose follows the code.
- Tests pin prose contracts in places; name any test that must change with a repair.
