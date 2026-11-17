---
title: "Replace long-term planning mechanisms with ordinary ROADMAP.md"
type: loom-research
status: concluded
created: 2026-11-16
updated: 2026-11-16
tags:
  - loom/research
---

# Replace long-term planning mechanisms with ordinary ROADMAP.md

## Question and scope

Should Loom retire decision-map and the remaining repository-purpose machinery
in favor of ordinary Markdown planning, following obsidian-researchworker's
finance work? This is a recommendation, not implementation authorization.

Evidence conditions: inspect the actual finance planning artifact and its update
history; identify what ordinary Markdown preserves and loses; trace current Loom
dependencies and deletion scope; distinguish absent local records from global
non-use. Preserve ordinary implementation review, acceptance and authorization.

## Method and rationale

Local source/history inspection plus a qualitative trade study. Criteria are
cross-session continuity, visible priorities and evidence, maintenance burden,
authorization boundaries and compatibility with existing records. External
practice cannot establish this user's needs; no industry-prevalence claim or
external search is necessary. This is not a controlled adoption experiment.

Revisions: Loom 9bbab926b; finance source branch finese-research b7f770d;
finance continuation feat/2026-11-16-finance-research-continuation 8fcc8f0.
Both finance worktrees were read without modification. The initial branch has
untracked local files; they were not used as planning evidence or modified.

## Findings

1. **Ordinary Markdown already carries the relevant long-term information.**
   Finance's root ROADMAP.md is a short general project roadmap. Its finance
   program is actually docs/finance/PLAN-DRAFT.md. In the continuation worktree,
   that document retains the objective, confirmed requirements, open decisions,
   stage exit conditions, current status, evidence and next authorized work.
   Section 14 explicitly separates the program plan, research evidence and
   operational handoffs; its update rule calls for observed results, evidence
   links, changed decisions, failures and a bounded next action. Two inspected
   intents cite it as evidence. Git history shows successive evidence updates
   on November 16, not merely an unused template. This is a working case,
   not proof of comparative efficiency or complete research success.
2. **Copying the finance artifact literally is not the smallest design.**
   Its continuation version is 644 lines and retains superseded operational
   snapshots. The root ROADMAP still says November 14 while finance records
   advance on November 16. This establishes separate scopes and potential
   navigation/maintenance burden, not a proven contradictory current decision.
   Prefer a concise current summary and links to retained evidence/history.
3. **decision-map provides real capabilities beyond a document.**
   It checks ticket evidence, dependency cycles, immutable terminal records,
   monotonic unknown identifiers, exclusive claims and transactional writes.
   start_delivery.py creates a linked intent; map_progress.py resolves stored
   progress, including legacy bindings. Plain ROADMAP.md does not preserve these
   guarantees. Retiring them is a deliberate scope reduction, justified only
   if long-term planning does not require machine-enforced work allocation or
   per-question closure. Normal delivery validation remains separate.
4. **The current local evidence does not demonstrate adoption.**
   No tracked docs/loom/maps files were found at the inspected Loom and finance
   continuation revisions. Earlier Loom proposals reference family-relocation;
   this rules out claiming the system was never used. Other adopting repos,
   installed caches and session telemetry were not inventoried. Do not use
   'unused everywhere' as the premise for immediate destructive removal.
5. **There is a substantial dedicated maintenance surface.**
   Counting regular files recursively under the skill yields 21 files / 6,551
   lines, including 17 Python files / 221 function definitions. Its dedicated
   tests yield 16 files / 6,909 lines / 312 function definitions. The combined
   37 files / 13,460 lines are a candidate retirement surface, not an exact
   final diff. Shared checker/manifests/docs and compatibility work are extra.
6. **Purpose and session execution goals must be separated.**
   PURPOSE.md's remaining template and goal-create ARC draft a repository-wide
   Why and Done when. Loom 1.0 no longer makes PURPOSE a standing document;
   its test migration note explicitly records this. goal-create SESSION serves
   native host execution goals and is independent of roadmap storage. Removing
   the entire skill would delete a distinct capability without evidence.
7. **Removal is cross-plugin, not one directory deletion.**
   Map-origin checking still resolves both map: and originator: map:<id> in
   the intent checker. Templates, capture-intent guidance, contract manifest,
   plugin manifests, discovery routing, user guides and dedicated tests refer
   to maps. goal-create ARC has tests referencing the purpose template.
   Existing historical records should stay readable, and links must survive.
   DIRECTION.md was already removed; do not build a new migration for it.

## Evidence

- [Map contract](../../../loom-workflow/skills/decision-map/SKILL.md),
  especially lines 15-23, 63-85, 134-157 and 203-218: scope and enforcement.
- [Map format](../../../loom-workflow/skills/decision-map/references/map-format.md):
  lifecycle, dependencies, stable identities and evidence contracts.
- [Delivery writer](../../../loom-workflow/skills/decision-map/scripts/start_delivery.py)
  and [progress reader](../../../loom-workflow/skills/decision-map/scripts/map_progress.py):
  implementation inspected; no runtime map operations were executed.
- [Intent map checker](../../../loom-code/scripts/loom_checker/rule_checks/intent.py):
  check_map_exists checks actual MAP.md existence for both origin spellings.
- [Purpose template](../../../loom-code/contract/templates/PURPOSE.md),
  [goal-create](../../../loom-workflow/skills/goal-create/SKILL.md),
  [purpose-retarget migration note](../../../loom-design/tests/interface/test_north_star_purpose_retarget.py).
- [Original v3 proposal](../evidence/outcome-map-v3/proposal.md): previous intended
  guarantees; historical proposal, not evidence of current runtime adoption.
- Finance files inspected locally, outside this checkout:
  `/Users/kouko/.herdr/worktrees/obsidian-researchworker/finese-research/ROADMAP.md`
  and `docs/finance/PLAN-DRAFT.md` in that same worktree;
  `/private/tmp/finance-research-continuation/docs/finance/PLAN-DRAFT.md`
  (sections 1, 10, 13 and 14, including lines 384-460).
- Finance continuation intent evidence fields inspected at
  `docs/loom/intent/2026-11-15-finance-work-assessment.md` and
  `docs/loom/intent/2026-11-16-finance-research-continuation.md` in that worktree.
  `git log -5 -- docs/finance/PLAN-DRAFT.md` returned a03b76a, 628e9cf,
  8e01480, 912bac8 and e7faf87: successive retained research/evidence updates.
- Measurement: Python pathlib recursive file enumeration, splitlines counts,
  and ast FunctionDef/AsyncFunctionDef counts; excludes external consumers.
  `git ls-files 'docs/loom/maps/**'` returned no entries in the two inspected
  repositories. No tests were run; tests were read as contract evidence only.

## Decision impact

### Session provenance follow-up

Local session inspection on 2026-11-16 corrects the suggestion that the agent
spontaneously initiated roadmap planning. The user explicitly requested the
planning; the agent selected ordinary Markdown filenames and organization.

- Codex session `01a1aa44-274a-7fa1-b750-f638dda6bfef`, stored at
  `/Users/kouko/.codex/sessions/2026/11/05/rollout-2026-11-05T13-52-35-01a1aa44-274a-7fa1-b750-f638dda6bfef.jsonl`:
  line 623 (2026-11-14 07:13:32 UTC) asks to extract the plugin and plan an
  implementation roadmap; line 680 presents ROADMAP-DRAFT.md; line 687 is user
  confirmation. Line 1133 includes ROADMAP.md as the W2-02 deliverable. Line
  3618 asks whether ROADMAP.md is Loom-defined; line 3631 explicitly answers
  that it is an agent-selected ordinary document, not a Loom-required artifact.
  Git identifies 5c34004 as the commit introducing root ROADMAP.md. Its existence
  predates the finance worktree discussion; the initial commit timestamp alone
  does not identify the exact write action.
- Codex session `01a1dd89-94f4-7de0-a954-80f600d687a7`, stored at
  `/Users/kouko/.codex/sessions/2026/11/15/rollout-2026-11-15T12-49-03-01a1dd89-94f4-7de0-a954-80f600d687a7.jsonl`:
  line 14 begins by asking to inspect the existing roadmap. Line 424 asks
  "繼續吧 先做出一個相對完整的規劃". Line 428 announces a project document;
  line 452 records the actual Add File for docs/finance/PLAN-DRAFT.md at
  2026-11-15 06:48:09 UTC. Line 483 explicitly asks to document the stages
  because multiple sessions will be required. Line 487 says handoff will be
  used while the plan remains the primary document; line 488 loads handoff;
  line 502 adds cross-session progress, decisions and updating rules.
- The dedicated Claude session b92d63c3-c835-40a7-a3f9-fed539fdc542 begins by
  asking to inspect the latest Codex session; its observed role is continuation,
  not creation of the initial roadmap.

These local conversation and tool records support an explicit natural-language
planning request followed by an agent-chosen ordinary document, then an explicit
cross-session retention request and handoff. They do not show decision-map
activation for either establishment episode. This strengthens recommending a
lightweight documented practice; it does not establish that spontaneous or
automatic roadmap creation would occur reliably without such requests.

| Alternative | Continuity and evidence | Maintenance | Assessment |
|---|---|---|---|
| Keep map and repair discoverability | Preserves strict guarantees | Keeps current scripts/schema | Choose only with concrete need for enforced multi-agent or question closure |
| Rename map or add a roadmap view | Similar guarantees | Keeps map and adds another representation | Does not solve the maintenance concern |
| Ordinary ROADMAP plus existing delivery flow | Retains goals, questions, stages and evidence links; loses map enforcement | Small prose convention, no new parser | Recommended for the demonstrated finance-style need |
| Keep both as equal active stores | Can preserve features | Ambiguous update ownership and duplicate state risk | Reject without separate demonstrated scopes |
| Defer all change | Preserves compatibility | Leaves current maintenance cost | Reasonable only pending a concrete adoption/compatibility inventory |

Smallest end state: one project-owned root ROADMAP.md describing purpose,
checkable target outcomes, current priorities, unresolved questions and evidence
links. Each item needs only its purpose, present status, next bounded action and
what would count as done. This is guidance, not a rigid required schema or a new
skill, CLI, checker, identifier system or lifecycle. Large initiatives may link
to an ordinary detailed document without becoming a second authoritative status
store. Roadmap entries do not authorize implementation or certify acceptance.

Use existing next-action advice to read the roadmap when present; update only
the affected item when direction changes or evidence establishes a new result.
Do not require rewrites on every turn or record PR/task detail already owned by
the delivery artifacts. Preserve actual failures in linked evidence and use Git
history for superseded wording. Do not claim the roadmap prevents stale state.

Critique, complexity mode: selected Design is taking apart (separate planning
from delivery rather than retain a specialized outcome runtime). Q1: the
smallest end state is the prose document plus existing delivery flow above.
Q2: retirement has a measured candidate reduction of 37 dedicated files and
13,460 lines; replacement is zero new executable functions and one short
document/convention. Shared consumer edits and any compatibility handling remain
uncosted, so this is not an exact net-change estimate. Q3: retire map's skill,
scripts, migration and dedicated tests; retire PURPOSE template and ARC-only
guidance/tests after confirming all consumers; preserve SESSION, research,
handoff and existing historical artifacts. Verdict: PROCEED for this bounded
design direction, conditional on accepting the stated loss of strict map
guarantees and checking adopter compatibility before deletion. No implementation
or acceptance verdict is implied.

### Local adoption inventory follow-up

Read-only directory inspection covered 33 accessible checkouts immediately under
`/Users/kouko/GitHub` and the repository/worktree levels of
`/Users/kouko/.herdr/worktrees`. Eight checkouts contain the same map id,
family-relocation, under Monkey Skills: its primary checkout and seven worktrees.
These are copies of one historical initiative, not eight independent users.
The primary MAP.md still says `state: active`; the latest path-specific commit
is 1b534ccdc dated 2026-09-11. It retains open/claimed tickets and explicitly
archives the legacy delivery-ticket path in place. This disproves a blanket
claim that no stored maps remain, but does not establish current live execution.

The retirement proposal therefore preserves all such documents untouched while
disclosing that upgrading removes the operations that formerly managed them.
Historical preservation is not continued executable support. No map was closed,
converted, retired or modified by this inventory. Unchecked directories, remote
adopters and installed-session use remain unknown. The current repo's dependency
search also identifies intent map-origin checking, paired templates, discovery,
contract/plugin manifests and ARC-specific tests as removal consumers.

Agent-decided minimum practice: when a user requests cross-session staged
planning, use a project-owned roadmap; read it when resuming that work or
recommending its next action; update affected content when direction or verified
results change. No background trigger or automatic reliable adoption is claimed.
Keep current status concise and link detailed research rather than accumulating
operational transcripts. Existing session-goal activation remains independent.

Do not ship permanent dual planning stores. If real adopting repositories have
live Maps, preserve them and define their bounded transition/retirement before
removing support; no current evidence establishes that immediate hard deletion
is compatible. Do not build a generic converter without actual input records.

## Limitations and open questions

- No global usage telemetry, adoption rate, maintenance-time benchmark or matched
  agent task comparison exists. Low use is user-reported; zero benefit is unproven.
- Finance has observed iterative Markdown use, not demonstrated superiority or
  a guarantee against stale summaries. The 644-line artifact is also a warning.
- Parallel claim and closure enforcement are intentionally lost. A demonstrated
  requirement for them would change the recommendation.
- A migration/removal PR still requires intent confirmation, focused checks,
  independent review, version metadata and release handling through normal Loom.
- Local source findings do not establish installed-host behavior or publication.
