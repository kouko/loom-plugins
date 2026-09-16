# Decision point ①: restate and confirm

Loaded by step 3 of `../SKILL.md` when the intent's `status:` is not already
`confirmed`. Relative paths here are relative to this file's directory; step
numbers are that SKILL.md's. `${CLAUDE_PLUGIN_ROOT}` is substituted by Claude
Code; on any other host substitute `<loom-code>`, the directory three levels
above this file.

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

2. **The one-way doors found so far**, in consequence form, per
   `one-way-door.md` — load that file before deciding whether a
   fork is one; the five classes and the four gates (check, measure,
   threshold, merge) are there, and a class (e) action — anything
   irreversible to the user's existing data — is asked even when there is
   no fork. Class (e) still yields to the **check** gate: when the intent's
   Constraints or `PRINCIPLES.md` already pin how that existing data is
   handled, do **not** ask — restate the handling in consequence form
   inside this same message ("this will rewrite your ___, I am doing it the
   way you said: ___"), so the user sees it without being stopped for it.

3. **The cross-model review question, only for `second-vendor: ask`.** Load
   `second-vendor-ask-and-docs-lint.md` before composing this
   message. A missing line is initialized as `second-vendor: suggest`; it
   does not add a question. `ask` puts its per-change
   host-aware question here using the native interface or documented fallback,
   and records the answer in the intent decision record. A fixed CLI and
   `suggest` add no question here.

4. **The principles interview**, if step 2 demanded it.

5. **The carried details, `kind: engineering` only.** Show them as a table,
   one row per detail in the user's language, confirmed by the same yes; no
   extra stop. With an empty list, no table appears. A product change shows
   them at decision point ② of the station writing its spec — `write-spec`,
   or this station (step 4). A product change's carried details never appear
   in this message.

**Every question in this message must be one of three types, or the
consequence form for one-way doors**, and you check the list before
sending:

- what do you want (the restatement),
- what will you see (visible behaviour — product only, and it belongs to
  decision point ②),
- did it work (acceptance — decision point ③),
- or the consequence form for a one-way door.

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
2. Commit it. The message is `docs(loom): intent <change-id> confirmed`,
   and its body **must contain the `needs-design:` line verbatim** — the
   checker compares the two strings character for character.
3. Verify: `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/loom_checker.py intent docs/loom/intent/<change-id>.md`
   Fix what it names and re-run until it exits 0.

**On "no" or a correction:** rewrite the intent, restate again. There is no
limit on rounds here; there is on guessing.
