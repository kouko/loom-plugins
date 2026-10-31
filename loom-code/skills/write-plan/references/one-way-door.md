# One-way doors

A one-way door is a choice that is expensive or impossible to undo later.
Its class flags a consequence to explain, not an automatic user question.
Check existing decisions, project evidence, tests, and applicable external sources;
then decide the technical choice and record the reason. Three or more trade-offs
alone do not require a user question. Ask only when alternatives materially
change the outcome the user will receive and the user's preference remains
unresolved after checking, or when an action needs authorization. Merge any
question into an existing decision point when possible. Continue independent
work while awaiting an answer.

## The five classes

Any one of these flags a consequence to disclose:

- **(a) Hard to swap later** — framework, language, database,
  authentication method, hosting platform, package manager.
- **(b) Creates money or a standing obligation** — paid services,
  third-party APIs that need an account, infrastructure someone must
  maintain.
- **(c) Limits what the user can do in future** — data formats, export
  ability, platform lock-in.
- **(d) Sets the ceiling on output quality** — recognition or generation
  model, algorithm, data source, when the candidates differ noticeably on
  an axis the user feels (accuracy, speed, cost per run, language or
  format coverage, privacy): any such axis differing by ≥ 20%, or the
  presence versus absence of money, privacy or coverage. Purely internal
  differences (memory, line count, maintainability) do not count. These
  thresholds flag consequences, not a reason to ask by themselves.
- **(e) An irreversible action on the user's existing state** — rewriting
  or deleting the user's data in place, changing an existing file format
  with no backup, sending the user's data off their machine. Rewriting,
  deleting, or sending the user's existing data off the machine requires
  explicit consent, even when there is no fork and only one way to do it.
  Independent acceptance testing happens in a clean environment, so it
  structurally never touches existing data.

## The four gates, in order

1. **Check first.** If an existing user decision, the intent's Acceptance
   or Constraints, or `PRINCIPLES.md` pins the choice, do not ask again.
   Follow it and cite the line. Check project evidence and applicable
   external sources for technical questions; external sources do not supply
   the user's preference or authorization.
2. **Measure first.** Compare candidates on the user's sample when feasible.
   Decide a technical result from the evidence and record why. If the
   result exposes an unresolved outcome preference, ask about that outcome.
3. **Threshold.** Apply class (d)'s significance test to decide what to
   disclose. The threshold alone does not decide whether to ask.
4. **Merge.** Ask only for an unresolved user outcome or missing authorization,
   inside an existing decision point when possible — ① for engineering,
   ② for product where its spec is written, ① for product when no spec will
   be written. A spec written later does not ask the same question again at ②.

## The consequence form

Disclose the consequences the user will experience for every major choice,
even when no answer is needed. When an unresolved outcome preference remains,
ask in this shape, with no mechanism vocabulary in it:

> Option A: from then on it only runs on ___, it costs ___ per month, and
> swapping it out means rewriting ___. Option B: ___. I suggest A,
> because ___.

Where there is no fork — class (e) — the same shape states the consequence
and the safeguard:

> This will rewrite your ___ into a new format and the old program will not
> read it. I will keep a backup at ___ first. Is that OK?

Record an answer in the spec's `## Design decision` as `user-decided`;
record an evidence-based choice as `agent-decided — <reason>`.

## After the decision point has closed

A technical choice that surfaces later is decided from evidence, marked
`agent-decided — <one-line reason>`, and listed in the acceptance test report's
"I decided for you" section, which decision point ③ reads. An unresolved
user outcome or missing authorization is asked when needed; continue work
that does not depend on the answer.

For classes **(b), (c) and (e)**, when authorization is missing, take a
zero-obligation, reversible option that touches no existing data if it
still meets the user's outcome. Record `agent-decided — not authorised,
took the conservative option`. If none does, ask for the missing preference
or authorization. A committing option needs prior authorization.
