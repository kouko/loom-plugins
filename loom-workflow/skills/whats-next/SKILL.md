---
name: whats-next
description: |
  Recommend the most useful next action for the current goal, with necessary alternatives. Use for 'what next?', '接下來最值得做什麼', '次は何を優先すべき', or when a blocker or new evidence requires reconsidering direction. Skip routine continuation of a viable approved plan, progress-only recaps, and simple factual requests.
user-invocable: true
---

# What next

Help choose the action most likely to advance the user's current goal.
Lead with one recommendation; show alternatives only when they matter.
Advice preserves the task's existing owner, constraints and authorization.

## When to use

Use when explicitly named or asked for next-action advice in natural language.
The agent may also use it when a blocker or material new evidence makes the
current direction unsuitable. This permits contextual selection; it promises
no automatic host trigger or background call on every turn.

Keep executing an authorized, viable plan without another advice interruption.
A failed command with a known recovery is ordinarily execution work, not a
reason to reopen the direction. Reconsider again only when evidence,
constraints or outcomes materially change.

For next-stage decisions in long-running project work, use
[roadmap](../roadmap/SKILL.md) to ground the choice in its applicable planning
document; it owns durable planning-document creation and maintenance. This
skill retains next-action advice, without forcing a new document or interrupting
a viable approved task.

## Ground the choice

1. Recover the original goal, latest user corrections, current progress,
   unfinished obligations, constraints and permissions from visible context.
   Preserve the goal unless the user changed it; do not let an old backlog or
   a newly interesting task silently replace it.
2. Separate observed facts from assumptions and unknowns. Verify only evidence
   whose uncertainty could change the choice, within existing permissions.
   Do not impose a history, repository or remote audit on every request.
   If evidence is unavailable, say what is missing and why it matters.
3. Find the remaining gap between the goal and the observed result. Work being
   implemented, tested, published or merged are different states; claim only
   the state supported by evidence. If the goal itself is unclear and changes
   the recommendation, ask for that missing goal rather than inventing one.
4. Compare plausible next actions internally. Include user-supplied routes,
   stopping, a smaller reversible step, and compatible combinations when
   relevant. Judge them by goal progress, useful information gained, effort,
   risk and current constraints. Do not create extra work to fill a menu.

## Recommend

Start in the user's language with the concrete first choice and why it helps.
Give its supporting evidence and the result it should produce or the decision
it will resolve. State consequential uncertainty plainly; a suspected cause
is not a confirmed cause. Prefer a bounded evidence-gathering action when a
missing fact determines which repair or direction would work.

Show an alternative when its consequences or an unresolved preference could
change the choice, and state when to choose it. Address user-supplied routes,
even if one should be deferred or rejected. Compatible steps can form one
recommendation when the combination serves the same outcome.

If the agreed goal is complete and no grounded obligation remains, recommend
stopping. Do not manufacture optimization, publication or feature work.
Use only the detail and structure needed: no fixed option count, table,
headings, menu or closing question is required.

## Continue within authority

A recommendation grants no new permission to implement, spend, disclose data,
delete, publish or merge. Follow the action's existing owner and required
consent process for genuinely new scope or permissions; do not reproduce that
owner's gates inside this advice skill or bypass them.

When unfinished work is already authorized, continue through its existing
owner without a generic extra confirmation. An advice-only request stays
advice-only. Ask only when a missing preference, fact or required consent
actually prevents the next action; explain what the answer changes.
Never claim an action ran merely because it was recommended.

## Adjacent requests

- In-session orientation only: [recap-state](../recap-state/SKILL.md).
- Save or resume another session: [handoff](../handoff/SKILL.md).
- Judge a supplied proposal or simplify a change: [critique](../critique/SKILL.md).

Output samples and description-only selection measure different things.
Neither establishes installed-host triggering or comparative improvement
without matched evidence. Preserve failures and ordinary-answer comparisons.
