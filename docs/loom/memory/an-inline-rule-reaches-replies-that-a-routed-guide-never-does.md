---
name: an-inline-rule-reaches-replies-that-a-routed-guide-never-does
description: A runtime instruction that routes an agent to a separate guide before deciding changes nothing when the agent never opens the guide — across six recorded trials the guide was opened zero times, and moving the same rule inline into the text the agent already reads produced the required reply shape in five of five; runtime prose that must change a reply states the rule where the agent is already reading, and routing to a separate file is for material the reply does not depend on
type: practice
sources:
  - resource: docs/loom/2026-09-16-plain-language-replies/blind-run-report.md §7 — six recorded trials (five how-questions, one yes-or-no) after the rule moved inline
  - resource: docs/loom/2026-09-16-plain-language-replies/evidence/blind-run/ — the per-trial transcripts and trial-judgments.txt behind that section
---

The per-turn card told the agent to read the writing guide before
deciding: "before deciding, read the guide". The guide held the rule that
a how-question is answered with at least two workable alternatives, one of
them marked as recommended.

The recorded trials show what that bought. Across six trials the guide was
opened **zero** times, and a how-question answered under the
read-the-guide wording produced a single approach with no alternatives at
all. The rule
existed, was correct, and was never executed, because the sentence
pointing at it was the only thing the agent read.

Stating the same rule **inline in the card** — the text the agent reads
every turn, with no file to open — produced two or more workable options
laid out in a table in **five of five** how-questions. The guide was still
opened zero times in those runs; the inline sentence, not the guide, is
what reached the replies.

**Why:** a pointer is executed only if the agent pays the cost of
following it, and a reply-shaping rule competes for that attention at the
exact moment the reply is being written. An agent that has enough context
to answer does not open a file to check how to answer. So the routed copy
of a rule is not a weaker version of the inline copy — it is, for
reply-shaping purposes, no copy at all, while reading as though the
behaviour is covered.

**How to apply:** split runtime prose by whether a reply depends on it.
Anything that must change the shape of the next reply — the decision rule,
the required alternatives, the form the answer takes — is stated inline
where the agent is already reading, in full, not as a pointer. A separate
guide carries what the reply does not depend on: worked examples,
before-and-after material, background a reader consults deliberately. When
a rule has to move inline, budget for the cap it now competes against
rather than shortening the rule into a pointer again. And do not read a
routed rule as evidence of behaviour: the test is a recorded trial showing
the reply changed, never the presence of the sentence.

**Limits:** inline placement buys execution, not completeness. In the same
five trials, three did not mark which option was recommended even though
the inline rule asked for it — a rule that reaches the reply can still be
partly applied, and each clause needs its own recorded check.

Related: [[imperative-placement-prominence-decides-weak-model-firing]]
(prominence within one always-read file, once the rule is already there),
[[prose-only-enforcement-dies-on-weak-executors]] (which consequences a
prose rule loses even when it is read).
