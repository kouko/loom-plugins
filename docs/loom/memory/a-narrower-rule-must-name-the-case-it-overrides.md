---
name: a-narrower-rule-must-name-the-case-it-overrides
description: Two rules in one section that decide the same question — a general one stated first, a narrower one a few lines later — are resolved by the executor in reading order rather than by scope, so the narrower rule loses whenever the general one was read first; the narrower rule states which case it overrides, or the general rule names the exception, and neither is left to the reader's sense of precedence
type: gotcha
sources:
  - resource: loom-workflow/skills/loom-visualization/SKILL.md — the registered gate block on client choice and the "Within the table plus ASCII form" bullets a few lines below it
  - resource: 2026-09-16 plain-language-replies arc — the agent that wrote both rules applied the wrong one in its own next reply
---

One section of `loom-workflow/skills/loom-visualization/SKILL.md` carried
two rules that decide the same question. The gate block says that when the
client check reports a remote viewer, the ASCII form is sent in a code
block and the table added only when exact values matter. Five lines below,
the form rules say an option comparison always uses a markdown table, in
every client.

Both sentences are clear. Neither says what happens when the reply is an
option comparison *and* the viewer is remote, which is a common case, not
an exotic one. An agent following the skill — this arc's own orchestrator,
immediately after writing both rules — read the gate sentence as governing
and sent a hand-padded ASCII table for an option comparison. Reading order
decided it. The same lapse carried two further violations of the same
skill: the generator was skipped and the alignment check never run, which
is what a hand-padded table costs.

**Why:** a human reader resolves a general rule and a narrower one by
scope, because "always, in every client" is recognisably an exception
clause. An executing agent resolves them by whichever it read first and
found sufficient to act on — it stops looking once a rule answers the
question in front of it. Proximity in the document does not encode
precedence, and the section heading that groups the two rules does not
either. The failure is silent: each rule is individually satisfied by a
reader who never noticed the other, so a review of either sentence alone
passes.

**How to apply:** when a section states a general rule and a narrower one
that can both decide the same case, make the precedence textual. Either
the narrower rule names what it overrides ("this holds even when the
client check asks for the ASCII form"), or the general rule names the
exception ("except an option comparison, which is always a markdown
table"). Writing both rules in the same edit is when to check: list the
inputs each rule keys on and look for an input pair both rules match. The
author is the worst-placed reader here — knowing both rules is exactly
what makes the gap invisible — so the check is mechanical, not a re-read
for feel.

Related: [[making-a-vague-rule-executable-can-activate-a-dormant-contradiction]]
(hardening one rule makes a latent conflict bind),
[[a-rule-edit-falsifies-the-unchanged-prose-composed-with-it]] (the
unchanged neighbour is where the contradiction lands).
