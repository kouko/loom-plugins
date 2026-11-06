# Relative iteration 2 — candidate behavior

## Outcome

The two previous targeted problems remained absent in their respective single
observations: the ordinary-default invoice reply disclosed the publication
authorization, and the ready code-only case wrote the intent before asking for
confirmation. The complete-CSV intent was in the user's language, unlike round
1. However, the natural-default invoice draft again says the accounting team
exports every day without supporting evidence, despite round 2's explicit
frequency guidance. The newly authored calendar example also says no file was
changed while acknowledging that an intent draft was written.

Two additional unsolicited diagrams failed a width-aware alignment check; in
both cases the actor did not invoke the existing visualization skill. The
explicitly requested held-invoice diagram was aligned and its ongoing hold was
retained. These findings are observations of one output per case; they do not
prove that the source edits caused the improvements or failures.

## Test

Eight isolated native Claude Code sessions used the same cases, first-party
`claude-sonnet-5-5` (confirmed by all modelUsage receipts), and requested
medium effort. Original hook and isolation preflight passed; all sessions
completed without permission denials, fixture commits or changed input files.
CLI-estimated cost: USD 1.1968631. The complete source overlay, test inputs,
replies, drafts and receipts are retained in `relative-iteration-2-data.json`.
The comparison uses baseline samples from an earlier batch and is not a
statistical error-rate estimate. The author inspected outputs; no independent
review or human-comprehension study was performed.

## Observations

- **Natural-default invoice:** the reply contains the required publication
  conditions, but the saved draft again assigns a daily export frequency not
  established by the source. The previous released-baseline draft did not make
  that particular claim. The reply's statement that currency no longer needs
  checking may imply a broader guarantee than the user supplied.
- **Complete CSV:** the intent is Chinese, as required by the conversation;
  the actor also drew an unsolicited framed comparison without invoking the
  visualization skill. The width checker reports unequal line widths.
- **New inventory PDF:** an unsolicited framed diagram likewise lacks the
  observed visualization-skill invocation and fails the width checker.
- **Explicit hold:** the reply preserves the ongoing hold, and the requested
  framed chart passes alignment.
- **New calendar setup:** the reply says no files were changed, immediately
  after stating it wrote the intent. The released-baseline output distinguishes
  the unchanged setup file from the new intent.
- **Incomplete CSV and unknown date:** both remain in an interview rather than
  demanding a ready confirmation. The unknown-date reply conflates a marked
  unknown label with an unsupported date in its rationale, a known limitation.
- **Code-only existing setup:** an open intent was written before the ready
  confirmation. Future publication wording in that wrapper remains ambiguous.

Frequency broadening has survived an explicit round-2 reminder. Do not add
another equivalent general warning as if it established a new mechanism; test
a meaningfully different and small approach, or accept the residual with an
explicit user-facing risk if the relative evidence justifies it. No actual
publication, post-confirmation execution or installed-host behavior was tested.
