# Small confirmation template — matched native trial

## Outcome

The prototype does not meet the factual and logical minimum and is not a
release candidate. A small template alone did not remove the previously
observed failures. This trial does not establish why they occurred or whether
template length causes them. The existing unreleased implementation remains
untouched; the prototype is an isolated overlay, not an installed plugin.

## Candidate and method

Both variants use released source `41211a0b`. The candidate adds a narrow
project-overview read at each intake entry and a short five-section ready
confirmation to each owner; the original consent and interview instructions
remain in place. The three-file overlay is retained in
`small-template-trial.patch`. The released visualization card and chart
guidance are unchanged. A short template, rather than the previous reference
packs, was selected to exercise the user's approved alternative.

Four synthetic cases were run once per variant in fresh native Claude Code
sessions, with all baseline sessions preceding all candidate sessions. The
same case inputs and prompts were used in both arms. Both intake owners are
represented: unknown release date, incomplete CSV request, verified setup
command, and invoice currency with a continuing publication hold and explicit
diagram request. The samples are small, order is not randomized, and their
prompts were previously used; no population error rates or causal improvement
can be inferred. This is a direct author read, not an independent blind review.

All eight calls returned `claude-sonnet-5-5` in modelUsage; medium effort was
requested, not independently verified. The CLI-reported total is USD 1.1251566.
Before calls, the isolated hook wrappers denied reading a synthetic private
sentinel, network binding, and writes to the frozen plugin snapshots. Seven
original hook checks passed for each variant. Each actor completed without a
permission denial, the requested skill was observed, the snapshot stayed
unchanged and no fixture commit was made. The actual overview-read witness
was not independently checked for every case. Cases, replies, drafts, model
receipts, and isolation results are in `small-template-trial-data.json`.

## Observations

- **Unknown date:** the candidate says only the user or release records can
  provide the date, which is not established by the supplied request. It offers
  an unrequested temporary-label change. The baseline also offers that
  alternative and its draft says no release record exists, broader than the
  user's statement that they cannot provide one.
- **Incomplete CSV:** the candidate says the list has no download capability;
  the source establishes only that it has no CSV download. It also says two
  required value answers are missing and confirmation cannot proceed, yet
  asks for confirmation in the same message. The baseline likewise presents
  a confirmation request despite declaring required information missing.
- **Setup command:** the candidate provides five sections and retains the
  supplied command correction. It includes internal workflow details and
  treats the wrapper's no-publication instruction as a continuing hold; that
  wrapper is ambiguous about the duration, so do not classify the latter as
  a proven consent error.
- **Currency and hold:** the candidate preserves the explicitly continuing
  publication hold and provides a framed before/after chart. The width-aware
  checker reports no drift for that chart. Its statement that staff will no
  longer need to inspect each invoice goes beyond the supplied correction:
  other reasons for inspection have not been ruled out. The baseline makes a
  similar claim. Both drafts should be read alongside the original request;
  the checks here are examples of material findings, not exhaustive reviews.

The trial is insufficient to claim that the original workflow is reliable,
that the candidate is better or worse overall, or that any version is ready
for release. Tests of installed plugins, other hosts, real repositories,
human comprehension and later workflow stages were not performed.
