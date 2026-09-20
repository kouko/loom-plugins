---
name: an-ordering-rule-that-is-vacuous-at-its-own-trigger-changes-nothing
description: A precondition added to a station is inert unless some reachable state makes it false — the blind-run "wait until content is frozen" rule was true by construction under the sentence that actually gates the dispatch, and bit only under a second, looser sentence in the same station that it then contradicted; before adding one, name the state in which it blocks and read every sentence already ordering that step
type: gotcha
sources:
  - resource: branch 2026-09-20-cheaper-agent-returns-and-blind-run-order, withdrawn after closing review — two independent reviewers returned NEEDS_REVISION on a 35-line prose change; the ordering half was fatal, and the return-to-file half left the safe path to habit rather than requiring it
---

Two prose changes were withdrawn rather than fixed, because each turned out
to be a protocol redesign wearing a prose edit's clothes. Both defects share
a shape: a rule written from one day's observation, dropped into a document
without reading the sentences that already govern the same step.

**The ordering rule was inert where it counted.** It said to dispatch the
blind runner only once functional content is frozen — no fix round in flight,
Build's checks passed, no reviewer finding outstanding. The station's §2
already requires the report to be committed before the first reviewers run;
at that moment no reviewer has run, so all three conditions hold by
construction and the rule blocks nothing. The station's §3 carries a second,
looser sentence ordering the same step — before the reviewers read the final
digest — and under that one the rule does bite, by contradicting §2. So the
station holds two sentences that disagree about when the step happens, and a
precondition added to one of them is either vacuous or a contradiction
depending on which a reader follows. That disagreement is the durable half of
this lesson. Under the reading where the rule bites it also collides with the
episode's digest cap: the report is functional content, committing it spends
a digest, and a change needing two fix rounds would run out and end
unconverged.

**The return-to-file rule left its safe path to habit.** It told every agent
to write its return to a file "in the host's scratch area" and reply with the
path. That phrase is defined nowhere in the flow, and no committed prose
tells a dispatcher to name a path — `closing-review/SKILL.md` lists what
reviewers are given and a path is not among them, and `build/SKILL.md` names
no dispatch inputs at all. In practice every dispatch in that episode did
name one: nine reviewer verdicts landed at distinct role-named paths with no
collision. The defect is therefore not that the design fails — its good
branch worked nine times out of nine — but that nothing required the good
branch. The reviewer floor is two by default, so two reviewers of one role
run concurrently under one identical instruction; had a dispatcher followed
the contract rather than the habit, both would have chosen the same obvious
name, the second would have overwritten the first, and the orchestrator would
have read one file believing it held two verdicts. No collision occurred. The
exposure was found by reading the contract, not by observing a failure.

The same change also crossed a marked gate without amending it. The one
documented cross-vendor path carries a reviewer's verdict on stdout from a
subprocess the caller must invoke outside its sandbox, and a path into that
subprocess's own scratch area is not *guaranteed* readable by the sandboxed
caller — whose contract forbids requesting the access that would guarantee
it. That was not measured; nobody ran the sandboxed caller against such a
path. The defect is the missing guarantee, not an observed failure.

**Why:** a precondition is only worth its words if some reachable state makes
it false. Adding one without naming that state produces text that reads like
a safeguard, passes review by looking careful, and changes nothing — which is
worse than leaving the gap open, because the gap is now documented as closed.
The second defect is the same failure from the other side: a remedy whose
safe branch depends on a habit no document states is one dispatcher away from
the unsafe one.

**How to apply:** before adding a precondition to a station, name the
reachable state in which it blocks, and read every other sentence in that
document ordering the same step; when two of them disagree, reconciling them
is the change, and adding a third is not. Before changing what an agent
returns, check who reads the return: every dispatch path, every concurrency,
and every marked gate that describes the old shape. Two agents of one role
running at once share every instruction they are given, including the one
that names their output — so an instruction that works because dispatchers
happen to be careful should be rewritten as one that requires it.
