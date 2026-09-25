---
name: a-prose-pin-must-require-an-affirmative-un-negated-sentence
description: A test that pins a contract sentence by keyword co-occurrence is satisfied by the sentence's own negation — "probes are never named test_<unit>_<state>_<expected>; docstrings are in English" passed a probe that looked for the literal plus "English"; the pin must require an affirmative verb before the literal and no negation token in that sentence, and carry synthetic positive and contradictory cases that prove it discriminates; the hole reopens whenever such a pin is relaxed from exact wording to meaning, so the polarity check is what a relaxed pin keeps
type: practice
sources:
  - resource: 2026-09-05 artifact-language-policy (loom-code 1.3.0) — the same defect was raised on two different pin files in one change (the probe-name probe, then the six station-sentence pins), each time by the Codex reader
  - resource: docs/loom/2026-09-16-plain-language-replies/attestation.json — the same defect recurred on a runtime prose card and its writing guide; adversarial probe docs/loom/2026-09-16-plain-language-replies/evidence/probes/test_probe_prose_gate_mutants.py, guard applied at loom-workflow/tests/scripts/test_visualization_card_hook.py
---

A pin on prose is tempting to write as "the file contains X and Y". That
predicate is true of the sentence you want and of its exact opposite: a
contract that says the rule *does not* apply contains the same tokens as
one that says it does. Two readers in one change found the same hole
twice, in two files written by two different agents.

**What holds:** split into sentences; the sentence carrying the literal
must contain an affirmative form (`is named`, `must be named`, `are in
English`, `stays in the user's language`) *before* the literal, and no
negation token — `\b(?:not|never|no)\b|n't` on word boundaries, because
`note` and `nothing` are not negations. Then add self-tests that feed the
matcher three synthetic paragraphs: the real sentence (accepted), the
negated one (rejected), the literal with no verb (rejected). The
self-tests are what make the pin reviewable — a reader can see what it
rejects instead of guessing.

**It recurs on runtime prose, not just on test-name policy.** A later
change pinned a per-turn card and a writing guide the same weak way, by
asserting that required phrases were present. An adversary showed the
whole file stayed green when the card was edited to "Reply to the user
never in their language." or "3) Never literal:", and when the guide said
a yes-or-no question "is never asked directly" with the metaphor ban
deleted: every required token survived each flip. The guard that closed it
is one shared negation matcher applied to the sentence carrying the pinned
phrase (`NEGATION` in `loom-workflow/tests/scripts/test_visualization_card_hook.py`,
used by `rule_polarity_errors` and `inline_decision_rule_errors`), with one
accepted and one rejected example per rule.

**The relaxation is the recurrence path.** In the branch that followed,
the same hole reappeared on two assertions — both had been loosened from
an exact-wording pin to a meaning pin, and the polarity requirement was
dropped along with the wording. Relaxing a pin to accept paraphrase is
often right; relaxing it to accept the paraphrase's negation never is. A
pin that is being widened keeps its affirmative-verb and no-negation
clauses, and the widening round is exactly when to re-run the negated
example.

**The cost side:** the contract sentences themselves must then avoid
negation words in the qualifying sentence ("rather than" instead of
"not"), which is a small rewording, and a fair one: a rule stated
affirmatively is also the one a cold reader applies correctly.

Related: [[a-narrowing-that-leaves-a-substring-passes-every-containment-pin]],
[[adversarial-fix-must-replace-semantics-not-token]].
