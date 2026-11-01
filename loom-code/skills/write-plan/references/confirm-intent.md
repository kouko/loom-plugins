# Decision point ①: restate and confirm

Loaded by step 3 of `../SKILL.md` when the intent's `status:` is not already
`confirmed`. Relative paths here are relative to this file's directory; step
numbers are that SKILL.md's. `${CLAUDE_PLUGIN_ROOT}` is substituted by Claude
Code; on any other host substitute `<loom-code>`, the directory three levels
above this file.

<!-- gate: write-plan.no-plan-without-confirmed-intent -->
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
outcome, Acceptance, or Out of scope. Keep publication authorisation in the
intent's `publication:` frontmatter line. The sole Constraints exception is
`- user-decided — second-vendor selection-confirmed: <vendor>` when plan is
skipped; it records the selected family, not the user's quoted request. Keep
that verbatim quote, target and final `selected_executor` in JSON
`authorization_source` at dispatch, and preserve only actual questions for
this plan's `## Questions asked` section.
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

Compose **one message**. Everything below goes in it; you do not stop
twice.

1. **The restatement.** Problem and Acceptance in the user's own plain
   words — no file paths, no identifiers, no mechanism names:

   > 你要的是 ___，做完後你可以 ___、___、___。對嗎？
   >
   > (You want ___, and when it is done you will be able to ___, ___ and
   > ___. Is that right?)

   For the current contract, automatic publication is the default. This same
   restatement explicitly says that answering yes authorizes a later non-forced
   push and Ready PR after `closing-review` and publication checks pass, while merge
   remains a separate decision. Say that the user may explicitly opt out before
   publication. Write
   `publication: automatic — authorized <date> by <name>` only after that
   informed yes; an opt-out leaves the field absent.

2. **The engineering one-way doors found so far**, in consequence form, per
   `one-way-door.md` — load that file before deciding whether a question is
   needed. Check existing decisions and evidence first: ask for the unresolved
   outcome preference only when alternatives materially change what the user
   receives, or ask for missing authorization. A pinned user choice is not
   asked again. Disclose material consequences even when the technical choice
   is agent-decided. A class (e) action on the user's existing data needs
   explicit consent even when there is no fork, unless the user already
   authorized that action. A product change's unresolved outcome or
   authorization questions are asked at decision point ② of the station
   writing its spec — `write-spec`, or this station (step 4) — when a spec
   will be written. They are asked in this message instead when no spec will
   be written (step 4 forces none); a spec written later in step 4 does not
   ask them again at ②. When the intent already authorizes how existing
   data is handled, do **not** ask again — restate the handling in consequence
   form inside this same message ("this will rewrite your ___, I am doing it
   the way you said: ___").

3. **The cross-model review question, only for `second-vendor: ask` without
   a qualifying direct user request.** Load
   `second-vendor-ask-and-docs-lint.md` before composing this
   message. A missing line is initialized as `second-vendor: suggest`; it
   does not add a question. When the user already named an outside coding
   agent and the review target is explicit or unambiguous from the active
   task, use that direct user request without a second per-change question.
   Store its verbatim quote, target and final `selected_executor` in JSON
   `authorization_source` at dispatch; the selected provider family uses the separate machine line in
   plan Risks or, when plan is skipped, bulleted intent Constraints. The direct
   request is not a question and does not enter `## Questions asked`. Otherwise `ask` puts
   its host-aware question here using the native interface or documented
   fallback and records the answer. A fixed CLI and `suggest` add no
   question here. Before outside discovery or execution, show the cost,
   egress, `review_root` and local-execution disclosure without blocking
   on another yes/no answer; an ambiguous choice or expanded material scope
   still needs the missing choice.

4. **The principles interview**, if step 2 demanded it.

5. **The carried details, `kind: engineering` only.** Show them as a table,
   one row per detail in the user's language, confirmed by the same yes; no
   extra stop. With an empty list, no table appears. A product change shows
   them at decision point ② of the station writing its spec — `write-spec`,
   or this station (step 4). A product change's carried details never appear
   in this message.

**Every question in this message must be one of three types, or the
consequence form for an unresolved user outcome or authorization**, and you check the list before
sending:

- what do you want (the restatement),
- what will you see (visible behaviour — product only, and it belongs to
  decision point ②),
- did it work (acceptance — decision point ③),
- or the consequence form for an unresolved user outcome or authorization.

A question that fits none is not the user's decision. If answering requires
reading code, follow repository precedent, decide it yourself, and record the
reason as `agent-decided`.

The closing-review station has a dimension for exactly this, `user-judgment-leak`,
and it returns NEEDS_REVISION when it finds one. Ask nothing about spec
quality, task splitting, or review verdicts.

**Write down every question you asked.** Keep a running list from this
point — every question put to the user at ①, and at ② if you run it here —
as `{decision_point, text, type}` with `type` one of `what` / `behaviour` /
`done` / `consequence`. It goes into the plan's `## Questions asked`
section at step 5. The list shows how often loom interrupts the user; a
question asked and not
recorded makes the flow look quieter than it is.

**Keep a carried-details list** too: only details the user stated or
explicitly agreed to. Only an explicit yes from the user counts as
agreement: a proposal left unanswered, deferred ("later"), or answered about
something else is dropped. Never carry an agent proposal the user did not
agree to, or detail you inferred. Carry only details about what the command
or screen does or how it reacts. A remark about background or usage context,
such as when or where the user runs it, is not a carried detail. Quote the
user's words for each carried detail — for an agreed proposal, quote the
proposal the user said yes to. Add no explanation, implication, or inference
of your own. It never enters the intent file.

**On "yes":**

1. Write `status: confirmed <date>` into the intent. When the confirmed
   restatement explicitly authorizes automatic publication, also write
   `publication: automatic — authorized <date> by <name>`; never derive it
   from status or prose.
2. Commit it on the change branch, branching first per SKILL.md's
   **Branch before the first commit** rule. The message is `docs(loom): intent <change-id> confirmed`,
   and its body **must contain the `needs-design:` line verbatim** — the
   checker compares the two strings character for character.
3. Verify: `"${CLAUDE_PLUGIN_ROOT}/scripts/loom-python" --repair intent docs/loom/intent/<change-id>.md`
   Fix what it names and re-run until it exits 0.

**On "no" or a correction:** rewrite the intent, restate again. There is no
limit on rounds here; there is on guessing.
