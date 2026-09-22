---
name: write-plan
description: |
  Plan an engineering change or turn a confirmed intent into implementation tasks. Use when planning or starting work without a plan.
version: 1.0.1
---

## What this station does

Relative paths in this document are relative to this skill's own directory.

Turn one intent into `docs/loom/<change-id>/plan.md`: waved tasks with files,
Acceptance ownership, positive and negative or boundary cases, and risk. Do **not**
implement or ask the user to approve task splitting; decide and record why.

## Decision boundary

This station chooses the simplest reversible implementation that satisfies the
confirmed specification. It may split that work into tasks and tests, but it
must not invent or reinterpret product behaviour. A product gap is returned
for clarification instead of being silently filled in the plan.

## Workflow setup

When `loom-design` is installed, an upstream station (`capture-intent`)
has already interviewed the user and confirmed the intent. When it is not
installed, **you also run that confirmation yourself** — step 3 below.

Use the installed checker's host-specific prefix:

| Host | Command prefix |
|---|---|
| Claude Code | `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py` |
| Codex CLI, Antigravity CLI | `python3 <loom-code>/scripts/loom_checker.py` |

`<loom-code>` (this plugin's root) is `${CLAUDE_PLUGIN_ROOT}` on Claude Code;
on any other host it is the directory two levels above this SKILL.md.
Commands below show Claude Code; on any other host substitute `<loom-code>`
for `${CLAUDE_PLUGIN_ROOT}`.
`${CLAUDE_PLUGIN_ROOT}` is substituted by Claude Code. `PLUGIN_ROOT` is provided to Codex plugin hook commands; it is not a general skill-shell variable.
On Antigravity CLI, map tool and agent names with
[`../../references/antigravity-tools.md`](../../references/antigravity-tools.md).

At entry, run `loom_checker.py selection show <change-id>` and omit only the
prose steps it lists as skipped (spec, plan, implementer, tdd,
blind-run); [expert-mode](../expert-mode/SKILL.md) stays an optional route
the user may invoke. The default is the full flow: skip a step only when the
user tells you to in plain words, then tell the user in one line which step is
skipped and continue. Never ask the user for a generated code to skip a step.

## Artifact vocabulary

`kind: product` changes what a user reads, types, or sees happen;
`kind: engineering` covers internal work, tooling, tests, and docs.
`<change-id>` is `<start-date YYYY-MM-DD>-<title-in-kebab-case>`.

## Station summary

| station | artifact | who decides | checker | checkpoint |
|---|---|---|---|---|
| capture-intent | intent — `docs/loom/intent/<change-id>.md`; `PRINCIPLES.md` and `DESIGN.md` at the repo root are side outputs of the tools it calls | user — decision point ① | `intent.schema`, `intent.product-no-identifiers`, `intent.needs-design-reason`, `intent.needs-design-recompute` | N/A |
| write-spec | spec — `docs/loom/<change-id>/spec.md` | user — decision point ②, product only; agent declares pre-build risk | `intake.confirmed`, `standing.product-principles-reject` | `required`: one independent `spec+adversarial` reviewer, no blind run; `not-required`: none |
| write-plan | plan — `docs/loom/<change-id>/plan.md` | agent-decided (runs ① itself when loom-design is absent) | `intake.confirmed`, `intake.confirmed-behavior`, `intake.spec-ready`, `intake.test-case-pair` | no formal plan review; invokes the required spec review only when it authored the spec |
| build | diff — commits on the change branch | agent-decided | task and integration tests; at the end of Build, an independent adversary's committed adversarial programs and the complete package suite, which must pass before hand-off | no formal review during Build; one closing review follows completed functional work |
| closing-review | generated `docs/loom/<change-id>/attestation.json`, plus a blind-run report when needed | fresh-context reviewers; reviewer count comes from the installed Review policy | reviewers see only content that passed Build's checks; `finalize-review` executes the package suite and adversarial programs again on committed content | branch end, or again only after functional content changes |
| ship | diff / PR — the pushed change branch and its pull request | automatic for canonical intent authorization; one user decision for a legacy intent; merge is separate | `push.contextual-body` and `publish.preconditions`; the verification status is disclosed, not a refusal; no functional replay | before push; publication-only fixes reuse matching evidence |
| maintain | intent — a fresh `docs/loom/intent/<change-id>.md` | agent (dedupe is mechanical) | `intent.schema`, `intent.needs-design-reason`, `intent.needs-design-recompute`, `intent.product-no-identifiers` on a new intent | before hand-off to write-plan |

## What you will be asked, in plain words

Give the user this list if they ask what is coming. It is the whole list:
there are no other **decision points**. On Codex there is also one
non-decision authorisation stop, the first time this repo is used (step
0b) — it asks for permission to run, not for a decision about the work.

1. At ①, restate the wanted outcome; merge any expensive-to-undo choice,
   `second-vendor: ask` question, and required principles interview.
2. At ②, only for a product spec you write: confirm visible behaviour and
   carried details. Ask nothing about plan structure; record each agent
   decision and reason.
3. At ③, the user accepts or rejects the report against every Acceptance line.

`second-vendor: suggest` only emits a non-blocking notice after the plan exists.

---

## Step 0 — Check the contract version

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py contract --require 2.1
```

Exit 0: continue. Anything else, the rule is `contract.requires`: print
what the checker printed, tell the user to update `loom-code`, and
**stop**. Do not work around it.

## Step 0b — Codex only: installed hook check

Read `references/codex-first-contact.md`. Confirm the injected checker lists
`push.contextual-body`. No repository-local scaffold, copied checker, probe remote,
or firing ledger is created.

## Step 1 — Find the intent

The intent lives at `docs/loom/intent/<change-id>.md`. Look there first; if
the user named a change, match the slug.

**If an intent exists**, read it and go to step 2.

**If none exists**, there are two cases:

- `loom-design` is installed → this is not your station. Tell the user the
  change starts at `capture-intent`, and stop.
- `loom-design` is not installed → hand the user the template path,
  `contract/templates/intent.md` inside the `loom-code` plugin, and stop
  there **unless** the user wants to describe the change now. If they do,
  run step 3's restate-and-confirm as a short interview instead: ask what
  the problem is, who it hurts, and what they will be able to do when it
  is done; write the file yourself from their answers. Keep it short — an
  engineering intent is normally three to five lines, and writing it by
  hand beats interviewing. The user never hand-writes the file. When you
  write it, `## Open questions` must be non-empty — the checker requires
  the section to have content, so with nothing open write exactly `- none`
  under the heading rather than leaving it blank.

<!-- gate: write-plan.no-plan-without-confirmed-intent -->
**No plan is written without a confirmed intent.** If `status:` is not
`confirmed <date>` by the end of step 3, you stop; you do not draft a plan
"provisionally" and you do not confirm on the user's behalf. The checker
enforces the same rule at step 4 (`intake.confirmed`), so a plan written
early cannot be shipped anyway.
When this station performs code-only intake, use the same capture boundary:
ask only for missing required-field content, never a fixed intake question
quota; existing decision points remain unchanged.
Problem holds present pain, who it affects, and the consequence, with no
diagnosis or fix; Proposed outcome holds the wanted capability;
Acceptance holds each observable delivery outcome, not value, complete
scenarios, UI placement, state transitions, test steps, or implementation;
Constraints are already fixed; product Value case gives beneficiary, urgency,
and GO/NO-GO, while an engineering intent omits obvious value;
Out of scope names excluded capability; Open questions contains only unresolved
outcome or scope choices. After drafting, make one author pass: **Keep,
neutralize, defer, reopen, or delete**. Behaviour defers to spec, method to
plan, and unsupported detail is deleted. This pass creates no field, ID,
requirement, scenario, product behaviour, or review loop.
Publication and second-reviewer authorisation never enter Problem, Proposed
outcome, Acceptance, Constraints, or Out of scope. Keep publication
authorisation in the intent's `publication:` frontmatter line and preserve the
question list for this plan's `## Questions asked` section.
Visible effects with an unknown surface and no spec require
`needs-design: yes` with a surface-neutral reason; internal files alone do not.
Complete the code-only altitude pass before confirmation. A material outcome
or scope fork needs an explicit answer; accepting the restatement is
insufficient; reopen means move it to Open questions, stop confirmation, and
the intent must remain `open`.
<!-- /gate -->

Any intent section may use a Markdown table or a Mermaid `flowchart`; Acceptance stays a
numbered list, diagrams stay at intent altitude (no UI reactions or state
transitions), a product Problem holds no identifiers (Mermaid node ids
included), and chat shows text tables or text diagrams, not Mermaid.

## Step 2 — Standing documents

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py standing docs/loom/intent/<change-id>.md
```

Run this on **every** change, before decision point ①. Print its WARN lines
to the user **verbatim** — do not summarise them, do not add to them, and
do not act on them. `standing.warn` and `standing.silence` are notices;
they never block.

One outcome does block, `standing.product-principles-reject`: `kind:
product` in a repo with no ratified `PRINCIPLES.md` (ratified = the file
carries a `ratified-by: <name> <date>` line and a `## Non-negotiables`
section with at least three items). Then, if `loom-design` is not
installed, you run the interview in
`contract/templates/PRINCIPLES-interview.md` — **inside the same
conversation as step 3**, not as a separate stop. Open with the line that
template gives you, ask its questions until the answers are clear, write
`PRINCIPLES.md`, and restate it together with the intent in step 3. When
the user says yes, write the `ratified-by:` line. If `loom-design` **is**
installed, hand this to its `product-principles` tool instead.

## Step 3 — Decision point ①: restate and confirm

When the intent's `status:` is already `confirmed`, skip this step.
Otherwise read `references/confirm-intent.md` and follow it fully before step 4,
in the single message it describes: the restatement, one-way doors, any
`second-vendor: ask` question, the principles interview, and engineering
carried details, then the intent's confirmation commit. Step 5 writes the
question list kept per that reference.

## Step 4 — Does this need a spec?

Read the intent's `needs-design:` line. It is `yes` when either holds:

- **(a)** the change touches a surface the user reads or types into — a
  GUI, a TUI, CLI arguments and output, an external API, or a file artifact a
  user or external system depends on — and no
  `DESIGN.md` or ui-flows document already covers that surface; or
- **(b)** the behaviour is multi-state or multi-object, and there is no
  spec for it.

Otherwise it is `no`. The same rule applies to every `kind`; product and
engineering are not judged differently here.

You do not get the last word on `no`: the checker recomputes it
(`intent.needs-design-recompute`) against this repo's declared
interface-surface globs, and a diff that touches one of them while the
intent says `no` is blocked.

**`no`** — go to step 5. The plan carries the Current State Evidence
section instead of a spec.

When a task's rationale outgrows its Risk line, write
`docs/loom/<change-id>/spec.md` from `contract/templates/spec-minimal.md` —
Requirements one per Acceptance line, Design decision one line per
agent-decided fork, Alternatives considered, Current state evidence, UI
flows (N/A unless a carried detail is visible) — carrying the template's five
sections and leaving the `confirmed-behavior:` line to product changes.
Decision point ② stays product-only. Declare `pre-build-review: required|not-required — <reason>`
using the risk classes below; only a required spec gets a pre-build review.

A non-empty carried-details list — from `capture-intent`'s hand-off or your
own intake — forces that spec even when every Risk line fits; record each
item per the `Record each carried detail` bullet below. An empty list forces no spec.

**`yes`, and `docs/loom/<change-id>/spec.md` already exists** — go to the
intake check below.

**`yes`, spec missing, `loom-design` installed** — hand the change to its
`write-spec` station and stop.

**`yes`, spec missing, `loom-design` not installed** — you write a minimal
spec yourself, from `contract/templates/spec-minimal.md`:

- Set `intent: <change-id>@<confirmation-sha>` and agent-decide
  `pre-build-review: required|not-required — <reason>`; require review for
  security/privacy, irreversible data, public contracts, cross-system
  architecture, or materially ambiguous requirements.
- Map each Acceptance line one-to-one to `REQ-<n> — <name> → Acceptance #<n>`.
- Fill UI flows (action and response, or `N/A`), Design decision,
  Alternatives considered, and path-anchored Forward/Reverse/Error/Data/Boundary
  evidence. Do not show those internal sections to the user.
- UI flows form: a short flow is `<action> → <reaction>` lines; several
  parallel cases on one surface, a table `case | what the user does | what
  they see`; states or paths that branch or go back and forth, a Mermaid
  `stateDiagram-v2` or `flowchart`.
- Record each carried detail as a UI flows line when visible, else as a clause
  on a Requirement line — the two parts decision point ② shows; only an
  engineering change may put one on a Design decision line instead. That
  clause goes on the Requirement line of the Acceptance line the detail
  serves, never a new REQ. An agent proposal the user did not agree to is not
  recorded.

Print one line for the user: installing `loom-design` gets them a fuller
spec than this one. For `pre-build-review: required`, dispatch one
fresh-context `loom-code:reviewer` with lens `spec+adversarial`, the spec
commit's parent (`<spec-commit>^`) as `reviewed_sha`, and the intent and
spec as ground truth; it must pass before planning, with no blind run, adversary, or
`finalize-review`. On NEEDS_REVISION, close each finding, commit, and send
only those fixes back to that reviewer. For `not-required`, proceed without a
formal spec review; `intake.spec-ready` blocks a spec with no declaration.

Running ② on a product spec you wrote: when a flow has parallel cases or
branches, lead with a table or a text (ASCII) diagram, then the per-case
sentences; never put Mermaid in this message — a terminal shows it as raw
code.

<!-- gate: write-plan.product-spec-needs-confirmed-behavior -->
**A product spec needs `confirmed-behavior:` before it becomes a plan.**
When `kind: product`, decision point ② belongs to whoever wrote the spec:
if you wrote it, you run it. Present the Requirements and the UI flows in
plain words — "you type ___ and you see ___; when ___ happens it will
___" — and nothing from `## Design decision` down, ever. On "yes", write
`confirmed-behavior: <date> @<spec sha7>` into the spec frontmatter, where
`<spec sha7>` is the first seven characters of
`git hash-object docs/loom/<change-id>/spec.md` run after the spec's last
edit — it pins which text the user said yes to. On a correction, rewrite,
present again, and recompute the hash. Engineering changes skip this
entirely.

### The intake check — both branches, every time

Whichever branch above you took, `no` included, run this before writing a
plan:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py intake write-plan <change-id>
```

Fix and re-run until it exits 0. At this point it checks
`intake.confirmed`, `intake.spec-ready`, and `intake.confirmed-behavior` —
whether the intent, spec declaration, and visible-behaviour confirmation are
ready. When `needs-design: no`, only intent readiness can
block before the plan exists, plus `intake.confirmed-behavior` when a
`kind: product` spec exists.

## Step 5 — Write the plan

Write `docs/loom/<change-id>/plan.md` from `contract/templates/plan.md`.

**Task size.** Each task owns coherent Acceptance lines, one module boundary,
declared dependencies, and positive plus negative/boundary cases. Split
unrelated behaviour; keep scenario detail in the spec and never size by time.

A task that removes or materially rewrites a function, recognizer, or rule
that already has tests names the existing test file on its Risk line and
states whether the change preserves, widens, or narrows what those tests
cover — not just that "tests pass" once the change is made. "Tests pass" is
also true of a change that quietly drops the one case those tests existed to
catch; read the current tests as the coverage spec before touching the code
they protect, and treat any case they exercise today as a fact the new
version must still hold, not a suggestion.

**Shape.**

- Group tasks into **waves** as dependency and integration boundaries. Waves
  do not schedule formal review; after all tasks and package tests pass,
  Build transitions once to the closing `branch-end` review.
- Unless `selection show` lists `implementer` as skipped, implementer dispatch
  is mandatory for every implementation task. Scheduling multiple implementers
  concurrently is optional.
- Task ids are `W<n>-<nn>` and remain stable once written so hand-offs can
  refer to dependencies without ambiguity.
- Dependencies go on the task line as `after: <ids>`. Independent tasks in one
  wave may run concurrently, but disjoint files alone do not prove independence:
  shared symbols, mirrored code/docs, and producer/consumer pairs stay sequential.
- Each non-memory task line carries `acceptance: <numbers>` naming the intent
  Acceptance lines it owns. Each referenced number appears in the task's
  Test line as `A<n> positive: <case-id>; negative: <case-id>` or with
  `boundary:` instead. Empty cases, nonexistent references, and Acceptance
  lines owned by no task are blocked by `intake.test-case-pair`.
- Each task carries three one-line fields -- Files, Test and Risk -- whose
  content kinds and word caps are set by the plan row of the artifact
  charter (`contract/manifest.yaml`, `artifacts.plan.charter`, rendered by
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py charter`). Run
  `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py plan
  docs/loom/<change-id>/plan.md` before the plan commit. Keep the plan useful
  when implementation changes; no separate plan-history ledger is required.

**Sections.**

The plan itself — `plan.md`, its Current State Evidence section, and every
evidence note — is written in English, though the Questions asked section
copies the user's own words verbatim rather than translating them; the
restatement at decision point ① stays in the user's language, since it is
spoken to the user rather than read as a machine artifact.

- When `needs-design: no`, the plan opens with **Current State Evidence** —
  Forward, Reverse, Error, Data, Boundary, each with a path and an anchor.
  With a spec, that section lives there instead, the plan cites the spec,
  and each task's Risk line points at the spec's Design decision by REQ id
  rather than restating the reasoning.
- A **Questions asked** section carrying the list you kept from step 3 and
  every question you asked at decision point ② in step 4 —
  one line per question, `<decision point> — <type> — <text>`. The intent's `## Open questions` must be exactly
  `- none` before Build; unresolved choices go back to intent work.
- A closing **Risks** section for risks that span the whole plan. When
  there is no spec, this section is also where the answers to one-way-door
  questions live: one `user-decided — <what they chose and why>` line each,
  because with no spec there is no `## Design decision` to hold them.

After the draft exists, run both commands before committing it:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py plan docs/loom/<change-id>/plan.md
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py intake write-plan <change-id>
```

The second run is when `intake.test-case-pair` can inspect the completed
Task DAG and block missing ownership, empty case pairs, or unresolved intent
questions. A pre-plan intake pass cannot substitute for this readiness run.

### Resolve `second-vendor: suggest`

Run this after the plan's Risk lines exist and both checks pass. Load
`references/second-vendor-ask-and-docs-lint.md`. Probe only the eligible
other-vendor CLIs described there, then pass one JSON object on stdin with
exactly these keys: `contract_version` (integer 1), `configured_mode`,
`host_vendor`, `usable_vendors`, `risk_evidence` (anchored risk evidence),
`response` (`pending` | `decline` | `accept`), `response_vendor` (only with
`accept`), `review_started` (whether Closing Review has started), and
`fixed_vendor` (only in fixed mode), to:

```
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/second_vendor_policy.py
```

On any other host, use the `<loom-code>` root defined in step 0. Treat the
JSON result as the decision: render its `notice_kind`, `notice_vendor`, and
`recommendation_reasons`; do not reproduce the risk mapping in prose. A
notice is commentary, not a decision point, and work continues without
waiting. The reference owns response timing and the
no-listener boundary.

**Forks you decided yourself.** Every one gets a one-line reason on its
task: what you chose and why. Any one-way door that surfaces now — after
decision point ① closed — is not a reason to go back to the user: take the
default, mark it `agent-decided`, and list it so the blind-run report can
show it at decision point ③.

<!-- gate: write-plan.post-decision-conservative-default -->
**After the decision point, classes (b), (c) and (e) have no free
default.** For those three classes in `references/one-way-door.md` — money
or a standing obligation, a limit on what the user can do later, and any
irreversible action on the user's existing data — you must take the
zero-obligation, reversible option that touches no existing data, and
record it as `agent-decided — not authorised, took the conservative
option`. Choosing a committing option unasked is never allowed, however
obvious it looks.

## Step 6 — Commit and hand off

**Branch first, if you are still on the trunk.** `git branch --show-current`
naming the trunk means the plan would land there, and every later
checkpoint measures its delta from the branch base — which would then be
the plan commit itself:

```
git switch -c <type>/<change-id>
```

For example `feat/2026-09-14-push-reason`. You pick `<type>` from `feat`,
`fix`, `docs`, `refactor`, `test`, `chore` or `ci` to match what the change
does, and use the same type in the PR title, which becomes the change's
squash-merge commit on the trunk. Individual task commits keep their own
Conventional Commits type as the implementer contract sets it, and the
`docs(loom):` intent and plan commits keep their fixed form.

The intent may already be committed on the trunk; that is fine and nothing
needs moving. It is the plan and everything after it that belongs on the
branch.

Commit the plan with the message `docs(loom): plan <change-id>`. Then hand
the change to the build station — `loom-code:build` — which dispatches one
implementer per task, runs task and integration tests, and calls the
closing-review station once at branch end.
